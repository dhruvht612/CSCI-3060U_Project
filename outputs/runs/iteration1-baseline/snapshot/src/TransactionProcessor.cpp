#include "TransactionProcessor.h"

#include "FileManager.h"
// Creates a processor that reads and writes data through the given FileManager.
TransactionProcessor::TransactionProcessor(const FileManager& files) : files_(files) {}

// Returns true if a user is logged in.
bool TransactionProcessor::isLoggedIn() const {
    return session_.has_value();
}

// Returns the logged-in user. Only call when isLoggedIn() is true.
const User& TransactionProcessor::currentUser() const {
    return session_.value();
}

// Returns the active user accounts for this session. Writes no record.
const std::vector<User>& TransactionProcessor::activeUsers() const {
    return users_.all();
}

// Starts a session for an existing user and loads the users, games, and collections.
// Returns false if already logged in or the user doesn't exist.
bool TransactionProcessor::login(const std::string& username) {
    if (session_) return false;
    users_ = UserManager(files_.loadUsers());
    const User* user = users_.find(username);
    if (!user) return false;
    games_ = GameManager(files_.loadGames(), files_.loadCollections());
    session_ = *user;
    return true;
}

// Ends the session and writes the Daily Transaction File, ending with 00.
// Returns false if nobody is logged in or the file couldn't be written.
bool TransactionProcessor::logout() {
    if (!session_) return false;
    std::vector<std::string> output = records_;
    // TODO(verify): the handout's template gives 00 records the
    // "XX UUUUUUUUUUUUUUU TT CCCCCCCCC" layout, but our Phase 1 fixtures expect a
    // bare "00". Kept as "00" until the TA confirms (docs, section 5).
    output.push_back("00");
    if (!files_.writeTransactions(output)) return false;
    session_.reset();
    records_.clear();
    return true;
}

// TODO(Phase 2): admin only (checked by FrontEnd); new username of at most 15
// characters, unique among current users; type admin, full-standard,
// buy-standard or sell-standard. TC08-TC12.
bool TransactionProcessor::createUser(const std::string& /*username*/, const std::string& /*userType*/) {
    return false;
}

// TODO(Phase 2): an existing user other than the current user; also cancel their
// games for sale. TC13-TC16.
bool TransactionProcessor::deleteUser(const std::string& /*username*/) {
    return false;
}

// TODO(Phase 2): unique name of at most 25 characters, price at most 999.99;
// the game can't be used again until the next session. TC17-TC25.
bool TransactionProcessor::sell(const std::string& /*gameName*/, long long /*priceCents*/) {
    return false;
}

// TODO(Phase 2): game exists, buyer doesn't already own it, buyer has enough
// credit (exact credit allowed); move the credit and add the game to the
// buyer's collection. TC26-TC31.
bool TransactionProcessor::buy(const std::string& /*gameName*/, const std::string& /*sellerName*/) {
    return false;
}

// TODO(Phase 2): buyer and seller are both current users; move the amount from
// the seller to the buyer. TC32-TC35.
bool TransactionProcessor::refund(const std::string& /*buyerName*/, const std::string& /*sellerName*/,
                                  long long /*amountCents*/) {
    return false;
}

// TODO(Phase 2): user exists; at most 1000.00 added to an account in one
// session. TC36-TC43.
bool TransactionProcessor::addCredit(const std::string& /*username*/, long long /*amountCents*/) {
    return false;
}
