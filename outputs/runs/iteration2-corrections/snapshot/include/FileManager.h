#pragma once

#include <string>
#include <vector>

#include "Game.h"
#include "User.h"

// Reads the startup data files and writes the Daily Transaction File.
// All file paths are fixed when the FileManager is constructed.
class FileManager {
public:
    // Stores the paths of the three input files and the Daily Transaction File.
    FileManager(std::string usersPath, std::string gamesPath,
                std::string collectionsPath, std::string transactionsPath);

    // Reads the Current User Accounts File up to its END line.
    // Throws std::runtime_error naming the file and line if it is missing or malformed.
    std::vector<User> loadUsers() const;

    // Parses 48/49-character records (fixture/handout compatibility); requires END.
    std::vector<Game> loadGames() const;

    // Parses 41/42-character records (fixture/handout compatibility); requires END.
    std::vector<CollectionEntry> loadCollections() const;

    // Replaces the Daily Transaction File's contents with `records`, one per line.
    // Returns false if the file could not be written.
    bool writeTransactions(const std::vector<std::string>& records) const;

private:
    std::string usersPath_;
    std::string gamesPath_;
    std::string collectionsPath_;
    std::string transactionsPath_;
};
