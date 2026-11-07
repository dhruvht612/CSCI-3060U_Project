#include "UserManager.h"

#include <utility>
#include <algorithm>

#include "RecordFormat.h"

// Creates the manager from the users loaded at login.
UserManager::UserManager(std::vector<User> users) : users_(std::move(users)) {}

// Returns the user with the given username, or nullptr if there isn't one.
const User* UserManager::find(const std::string& username) const {
    for (const User& user : users_) {
        if (user.username == username) return &user;
    }
    return nullptr;
}

bool UserManager::addUser(const User& user) {
    if (!record::validName(user.username, 15) || find(user.username) ||
        (user.type != "AA" && user.type != "FS" && user.type != "BS" && user.type != "SS") ||
        user.creditCents < 0 || user.creditCents > record::maxCreditCents) return false;
    users_.push_back(user);
    return true;
}

bool UserManager::removeUser(const std::string& username) {
    const auto found = std::find_if(users_.begin(), users_.end(), [&](const User& user) {
        return user.username == username;
    });
    if (found == users_.end()) return false;
    users_.erase(found);
    return true;
}

// Check before adding, including for LLONG_MIN/LLONG_MAX deltas.
bool UserManager::adjustCredit(const std::string& username, long long deltaCents) {
    for (User& user : users_) {
        if (user.username != username) continue;
        if (deltaCents < -user.creditCents ||
            deltaCents > record::maxCreditCents - user.creditCents) return false;
        user.creditCents += deltaCents;
        return true;
    }
    return false;
}

// Returns every user read for the current session, in file order.
const std::vector<User>& UserManager::all() const {
    return users_;
}
