#include "GameManager.h"

#include <utility>
#include <algorithm>

GameManager::GameManager(std::vector<Game> games, std::vector<CollectionEntry> collections)
    : games_(std::move(games)), collections_(std::move(collections)) {}

// Creates the manager from the games and collection entries loaded at login.
const Game* GameManager::find(const std::string& gameName) const {
    for (const Game& game : games_) {
        if (game.name == gameName) return &game;
    }
    return nullptr;
}

// Returns true if the user owns the game.
bool GameManager::isOwnedBy(const std::string& gameName, const std::string& username) const {
    for (const CollectionEntry& entry : collections_) {
        if (entry.gameName == gameName && entry.owner == username) return true;
    }
    return false;
}

// A collection is a set of game/owner pairs.
void GameManager::addToCollection(const std::string& gameName, const std::string& owner) {
    if (!isOwnedBy(gameName, owner)) collections_.push_back({gameName, owner});
}

// Cancel the listings, preserving copies already owned by other users.
void GameManager::removeGamesBySeller(const std::string& seller) {
    games_.erase(std::remove_if(games_.begin(), games_.end(), [&](const Game& game) {
        return game.seller == seller;
    }), games_.end());
}
