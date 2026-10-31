#pragma once

#include <optional>
#include <string>
#include <vector>

#include "GameManager.h"
#include "User.h"
#include "UserManager.h"

class FileManager;

// Owns the login session and the data read for it, validates transactions,
// and collects the session's Daily Transaction File records until logout.
// Account-type permission checks are done by FrontEnd before these are called.
class TransactionProcessor {
public:
    // `files` supplies the data files and must outlive this object.
    explicit TransactionProcessor(const FileManager& files);

    // True while a user is logged in.
    bool isLoggedIn() const;

    // The logged-in user. Throws std::bad_optional_access if nobody is logged in.
    const User& currentUser() const;

    // The active user accounts for this session (read-only). Writes no record.
    const std::vector<User>& activeUsers() const;

    // Starts a session for `username`. As the handout requires, the user accounts
    // file is read first, and the games and collections only once the username
    // is accepted. Returns false if a session is already active or no such user
    // exists. Throws std::runtime_error if a data file cannot be read.
    bool login(const std::string& username);

    // Ends the session by writing its records followed by the "00" end-of-session
    // record to the Daily Transaction File. Returns false if nobody is logged in or
    // the write fails; on failure the session and its records are kept.
    bool logout();

    // TODO(Phase 2): the transactions below are not implemented. Each returns
    // false and records nothing. Amounts are in cents.

    // create (01): add a user with the given type word, e.g. "full-standard".
    bool createUser(const std::string& username, const std::string& userType);
    // delete (02): remove a user and cancel their games for sale.
    bool deleteUser(const std::string& username);
    // sell (03): put a game up for sale by the current user.
    bool sell(const std::string& gameName, long long priceCents);
    // buy (04): the current user buys a game from a seller.
    bool buy(const std::string& gameName, const std::string& sellerName);
    // refund (05): move credit from a seller to a buyer.
    bool refund(const std::string& buyerName, const std::string& sellerName, long long amountCents);
    // addcredit (06): add credit to an account (the current user's own, for non-admins).
    bool addCredit(const std::string& username, long long amountCents);

private:
    const FileManager& files_;
    UserManager users_;
    GameManager games_;
    std::optional<User> session_;       // the logged-in user, if any
    std::vector<std::string> records_;  // this session's records, not including "00"
};
