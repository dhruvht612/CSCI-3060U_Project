#pragma once

#include <string>
#include <vector>

#include "User.h"

// Holds the user accounts read for the current session and answers lookups on them.
class UserManager {
public:
    // Takes ownership of `users` (empty until the first login loads the file).
    explicit UserManager(std::vector<User> users = {});

    // Returns the user whose username matches exactly, or nullptr if none does.
    // The pointer is valid until the user list changes.
    const User* find(const std::string& username) const;

    // Returns every user read for the current session, in file order.
    const std::vector<User>& all() const;

    // Adds a unique, validated account to the current session.
    bool addUser(const User& user);

    // Removes the user (delete). Returns false if no such user exists.
    bool removeUser(const std::string& username);

    // Adds `deltaCents` (negative to deduct) to the user's credit (buy, refund,
    // addcredit). Returns false for a missing user or an out-of-range balance.
    bool adjustCredit(const std::string& username, long long deltaCents);

private:
    std::vector<User> users_;
};
