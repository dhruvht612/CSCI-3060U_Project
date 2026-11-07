#include "FileManager.h"

#include <cctype>
#include <fstream>
#include <stdexcept>
#include <utility>
#include <set>

#include "Money.h"
#include "RecordFormat.h"

namespace {

// Current User Accounts File line layout (handout and fixtures agree):
// 15-char username, space, 2-char type, space, 9-char credit "DDDDDD.DD".
constexpr std::size_t kUserLineWidth = 28;

// Returns `text` without its trailing spaces (the padding of a fixed-width field).
std::string trimRight(std::string text) {
    text.erase(text.find_last_not_of(' ') + 1);
    return text;
}

// Returns true if type is one of the four user type codes: AA, FS, BS, SS.
bool isUserType(const std::string& type) {
    return type == "AA" || type == "FS" || type == "BS" || type == "SS";
}

}  // namespace

// Stores the paths of the users, games, collections, and daily transaction files.
FileManager::FileManager(std::string usersPath, std::string gamesPath,
                         std::string collectionsPath, std::string transactionsPath)
    : usersPath_(std::move(usersPath)),
      gamesPath_(std::move(gamesPath)),
      collectionsPath_(std::move(collectionsPath)),
      transactionsPath_(std::move(transactionsPath)) {}

// Reads the Current User Accounts File up to the END line.
// Throws std::runtime_error if the file can't be opened, a record is malformed,
// or the END line is missing.
std::vector<User> FileManager::loadUsers() const {
    std::ifstream file(usersPath_);
    if (!file) throw std::runtime_error("cannot open user accounts file " + usersPath_);

    std::vector<User> users;
    std::set<std::string> names;
    std::string line;
    for (int lineNumber = 1; std::getline(file, line); ++lineNumber) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (trimRight(line) == "END") return users;

        User user;
        bool valid = line.size() == kUserLineWidth && line[15] == ' ' && line[18] == ' ' &&
                     money::parseCents(line.substr(19), user.creditCents);
        if (valid) {
            user.username = trimRight(line.substr(0, 15));
            user.type = line.substr(16, 2);
            valid = record::validName(user.username, 15) && isUserType(user.type) &&
                    user.creditCents <= record::maxCreditCents && names.insert(user.username).second;
        }
        if (!valid) {
            throw std::runtime_error(usersPath_ + " line " + std::to_string(lineNumber) +
                                     ": malformed user record");
        }
        users.push_back(user);
    }
    throw std::runtime_error(usersPath_ + ": missing END line");
}

// Accept the two documented name-field widths (25 in fixtures, 26 in handout).
// The 26th position is padding: the explicit game-name limit remains 25.
std::vector<Game> FileManager::loadGames() const {
    std::ifstream file(gamesPath_);
    if (!file) throw std::runtime_error("cannot open games file " + gamesPath_);
    std::vector<Game> games;
    std::set<std::string> names;
    std::string line;
    for (int number = 1; std::getline(file, line); ++number) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (trimRight(line) == "END") return games;
        Game game;
        bool valid = line.size() == 48 || line.size() == 49;
        if (valid) {
            const std::size_t width = line.size() - 23;
            game.name = trimRight(line.substr(0, width));
            game.seller = trimRight(line.substr(width + 1, 15));
            valid = line[width] == ' ' && line[width + 16] == ' ' &&
                    record::validName(game.name, 25) && record::validName(game.seller, 15) &&
                    money::parseCents(line.substr(width + 17), game.priceCents) &&
                    game.priceCents <= 99999 && names.insert(game.name).second;
        }
        if (!valid) throw std::runtime_error(gamesPath_ + " line " + std::to_string(number) +
                                            ": malformed game record");
        games.push_back(game);
    }
    throw std::runtime_error(gamesPath_ + ": missing END line");
}

// Same compatibility policy as loadGames; ownership pairs must be unique.
std::vector<CollectionEntry> FileManager::loadCollections() const {
    std::ifstream file(collectionsPath_);
    if (!file) throw std::runtime_error("cannot open collections file " + collectionsPath_);
    std::vector<CollectionEntry> collections;
    std::set<std::pair<std::string, std::string>> pairs;
    std::string line;
    for (int number = 1; std::getline(file, line); ++number) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (trimRight(line) == "END") return collections;
        CollectionEntry entry;
        bool valid = line.size() == 41 || line.size() == 42;
        if (valid) {
            const std::size_t width = line.size() - 16;
            entry.gameName = trimRight(line.substr(0, width));
            entry.owner = trimRight(line.substr(width + 1));
            valid = line[width] == ' ' && record::validName(entry.gameName, 25) &&
                    record::validName(entry.owner, 15) &&
                    pairs.insert({entry.gameName, entry.owner}).second;
        }
        if (!valid) throw std::runtime_error(collectionsPath_ + " line " + std::to_string(number) +
                                            ": malformed collection record");
        collections.push_back(entry);
    }
    throw std::runtime_error(collectionsPath_ + ": missing END line");
}

// Writes the records to the Daily Transaction File, one per line.
// Returns true if the file was written successfully.
bool FileManager::writeTransactions(const std::vector<std::string>& records) const {
    std::ofstream file(transactionsPath_, std::ios::trunc);
    for (const std::string& record : records) file << record << '\n';
    file.close();
    return !file.fail();
}
