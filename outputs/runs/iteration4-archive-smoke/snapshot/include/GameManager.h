#pragma once

#include <string>
#include <vector>

#include "Game.h"

// Holds the available games and game collections read for the current
// session and answers lookups on them.
class GameManager {
public:
    // Takes ownership of both lists (empty until a login loads the files).
    explicit GameManager(std::vector<Game> games = {}, std::vector<CollectionEntry> collections = {});

    // Returns the available game whose name matches exactly, or nullptr if none does.
    const Game* find(const std::string& gameName) const;

    // Returns true if the collections list `username` as an owner of `gameName`.
    bool isOwnedBy(const std::string& gameName, const std::string& username) const;

    // Records that `owner` now owns `gameName` (buy).
    void addToCollection(const std::string& gameName, const std::string& owner);

    // Removes every game `seller` has for sale (delete).
    void removeGamesBySeller(const std::string& seller);

private:
    std::vector<Game> games_;
    std::vector<CollectionEntry> collections_;
};
