#include "UserManager.h"

#include <utility>

UserManager::UserManager(std::vector<User> users) : users_(std::move(users)) {}

const User* UserManager::find(const std::string& username) const {
    for (const User& user : users_) {
        if (user.username == username) return &user;
    }
    return nullptr;
}

bool UserManager::removeUser(const std::string& /*username*/) {
    return false;  // TODO(Phase 2)
}

bool UserManager::adjustCredit(const std::string& /*username*/, long long /*deltaCents*/) {
    return false;  // TODO(Phase 2)
}
