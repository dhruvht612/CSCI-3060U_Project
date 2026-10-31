#include "GameManager.h"

#include <utility>

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

// Adds a game to a user's collection. Not implemented yet.
void GameManager::addToCollection(const std::string& /*gameName*/, const std::string& /*owner*/) {
    // TODO(Phase 2)
}

// Removes all games listed by a seller. Not implemented yet.
void GameManager::removeGamesBySeller(const std::string& /*seller*/) {
    // TODO(Phase 2)
}
