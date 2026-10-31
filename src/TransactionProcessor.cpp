#include "TransactionProcessor.h"

#include "FileManager.h"
#include "RecordFormat.h"
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
    records_.clear();
    creditAdded_.clear();
    newGames_.clear();
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

// New accounts start at zero credit and are visible within this session.
bool TransactionProcessor::createUser(const std::string& username, const std::string& userType) {
    if (!session_ || session_->type != "AA" || !record::validName(username, 15)) return false;
    std::string type;
    if (userType == "admin") type = "AA";
    else if (userType == "full-standard") type = "FS";
    else if (userType == "buy-standard") type = "BS";
    else if (userType == "sell-standard") type = "SS";
    else return false;
    if (!users_.addUser({username, type, 0})) return false;
    records_.push_back(record::account("01", username, type, 0));
    return true;
}

bool TransactionProcessor::deleteUser(const std::string& username) {
    if (!session_ || session_->type != "AA" || username == session_->username ||
        !users_.removeUser(username)) return false;
    games_.removeGamesBySeller(username);
    // Phase 1 marks type/credit unused for delete; TA confirmation is outstanding.
    records_.push_back(record::account("02", username, "", 0));
    return true;
}

bool TransactionProcessor::sell(const std::string& gameName, long long priceCents) {
    if (!session_ || session_->type == "BS" || !record::validName(gameName, 25) ||
        priceCents < 0 || priceCents > 99999 || games_.find(gameName) ||
        newGames_.count(gameName)) return false;
    newGames_.insert(gameName);
    records_.push_back("03 " + record::field(gameName, 25) + ' ' +
                       record::field(session_->username, 15) + ' ' + record::money(priceCents, 6));
    return true;
}

bool TransactionProcessor::buy(const std::string& gameName, const std::string& sellerName) {
    if (!session_ || session_->type == "SS" || newGames_.count(gameName)) return false;
    const Game* game = games_.find(gameName);
    const User* seller = users_.find(sellerName);
    const User* buyer = users_.find(session_->username);
    if (!game || !seller || !buyer || game->seller != sellerName ||
        games_.isOwnedBy(gameName, buyer->username) || buyer->creditCents < game->priceCents ||
        (buyer != seller && seller->creditCents > record::maxCreditCents - game->priceCents)) return false;
    // Validate both sides before mutation. A self-transfer has zero net credit.
    if (buyer != seller) {
        users_.adjustCredit(buyer->username, -game->priceCents);
        users_.adjustCredit(sellerName, game->priceCents);
    }
    games_.addToCollection(gameName, session_->username);
    session_ = *users_.find(session_->username);
    records_.push_back("04 " + record::field(gameName, 25) + ' ' + record::field(sellerName, 15) +
                       ' ' + record::field(session_->username, 15) + ' ' + record::money(game->priceCents, 6));
    return true;
}

bool TransactionProcessor::refund(const std::string& buyerName, const std::string& sellerName,
                                  long long amountCents) {
    if (!session_ || session_->type != "AA" || amountCents < 0 ||
        amountCents > record::maxCreditCents) return false;
    const User* buyer = users_.find(buyerName);
    const User* seller = users_.find(sellerName);
    if (!buyer || !seller || seller->creditCents < amountCents ||
        (buyer != seller && buyer->creditCents > record::maxCreditCents - amountCents)) return false;
    if (buyer != seller) {
        users_.adjustCredit(sellerName, -amountCents);
        users_.adjustCredit(buyerName, amountCents);
    }
    session_ = *users_.find(session_->username);
    records_.push_back("05 " + record::field(buyerName, 15) + ' ' + record::field(sellerName, 15) +
                       ' ' + record::money(amountCents, 9));
    return true;
}

bool TransactionProcessor::addCredit(const std::string& username, long long amountCents) {
    if (!session_ || (session_->type != "AA" && username != session_->username) ||
        amountCents < 0 || amountCents > 100000) return false;
    const User* user = users_.find(username);
    const auto added = creditAdded_.find(username);
    const long long total = added == creditAdded_.end() ? 0 : added->second;
    if (!user || amountCents > 100000 - total || !users_.adjustCredit(username, amountCents)) return false;
    creditAdded_[username] = total + amountCents;
    session_ = *users_.find(session_->username);
    // The fixture profile records the amount added, not the resulting balance.
    records_.push_back(record::account("06", username, user->type, amountCents));
    return true;
}
