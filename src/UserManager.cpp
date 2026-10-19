#include "UserManager.h"

#include <utility>

// Creates the manager from the users loaded at login.
UserManager::UserManager(std::vector<User> users) : users_(std::move(users)) {}

// Returns the user with the given username, or nullptr if there isn't one.
const User* UserManager::find(const std::string& username) const {
    for (const User& user : users_) {
        if (user.username == username) return &user;
    }
    return nullptr;
}

// Removes a user from the current users. Not implemented yet.
bool UserManager::removeUser(const std::string& /*username*/) {
    return false;  // TODO(Phase 2)
}

// Changes a user's credit by the given amount. Not implemented yet.
bool UserManager::adjustCredit(const std::string& /*username*/, long long /*deltaCents*/) {
    return false;  // TODO(Phase 2)

// Returns every user read for the current session, in file order.
const std::vector<User>& UserManager::all() const {
    return users_;
}
}
