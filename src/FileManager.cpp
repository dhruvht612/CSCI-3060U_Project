#include "FileManager.h"

#include <cctype>
#include <fstream>
#include <stdexcept>
#include <utility>

#include "Money.h"

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
            valid = !user.username.empty() && isUserType(user.type);
        }
        if (!valid) {
            throw std::runtime_error(usersPath_ + " line " + std::to_string(lineNumber) +
                                     ": malformed user record");
        }
        users.push_back(user);
    }
    throw std::runtime_error(usersPath_ + ": missing END line");
}

// Reads the Available Games File. Not implemented yet (returns an empty list).
std::vector<Game> FileManager::loadGames() const {
    // TODO(Phase 2): parse gamesPath_. The handout's template is 49 characters
    // (26-char name, space, 15-char seller, space, 6-char price) but its
    // constraint says 42; the Phase 1 fixtures use 48 (25-char name). Confirm with the TA.
    return {};
}

// Reads the Game Collection File. Not implemented yet (returns an empty list).
std::vector<CollectionEntry> FileManager::loadCollections() const {
    // TODO(Phase 2): parse collectionsPath_. The handout says 42 characters
    // (26-char name, space, 15-char owner); the Phase 1 fixtures use 41
    // (25-char name). Confirm with the TA.
    return {};
}

// Writes the records to the Daily Transaction File, one per line.
// Returns true if the file was written successfully.
bool FileManager::writeTransactions(const std::vector<std::string>& records) const {
    std::ofstream file(transactionsPath_, std::ios::trunc);
    for (const std::string& record : records) file << record << '\n';
    file.close();
    return !file.fail();
}
