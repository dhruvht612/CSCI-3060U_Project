#include "FrontEnd.h"

#include <algorithm>
#include <array>
#include <exception>
#include <istream>
#include <ostream>

#include "Money.h"
#include "TransactionProcessor.h"

namespace {

// The transaction codes the handout lists, in its order. They are lowercase and
// matched case-sensitively, exactly as the handout writes them.
constexpr std::array<const char*, 8> kCommands = {
    "login", "logout", "create", "delete", "sell", "buy", "refund", "addcredit"};

// True for the transaction codes the handout lists.
bool isKnownCommand(const std::string& command) {
    return std::find(kCommands.begin(), kCommands.end(), command) != kCommands.end();
}

// The transaction codes as a comma-separated list, for the unrecognized-command message.
std::string commandList() {
    std::string list;
    for (const char* command : kCommands) {
        if (!list.empty()) list += ", ";
        list += command;
    }
    return list;
}

// Returns `text` without its leading and trailing whitespace (spaces, tabs, etc.).
std::string trimWhitespace(const std::string& text) {
    const char* const kWhitespace = " \t\n\v\f\r";
    const std::size_t first = text.find_first_not_of(kWhitespace);
    if (first == std::string::npos) return "";
    return text.substr(first, text.find_last_not_of(kWhitespace) - first + 1);
}

// True if an account of `userType` may run `command` (any command except login/logout).
// Rules from the handout's Transaction Code Details.
bool isPermitted(const std::string& command, const std::string& userType) {
    // create, delete and refund are privileged: admin only.
    if (command == "create" || command == "delete" || command == "refund") return userType == "AA";
    if (command == "sell") return userType != "BS";  // any type except buy-standard
    if (command == "buy") return userType != "SS";   // any type except sell-standard
    if (command == "addcredit") return true;         // unprivileged
    return false;
}

}  // namespace

FrontEnd::FrontEnd(TransactionProcessor& processor, std::istream& in, std::ostream& out)
    : processor_(processor), in_(in), out_(out) {}

void FrontEnd::run() {
    std::string line;
    while (true) {
        out_ << "Enter command: ";
        if (!readLine(line)) break;
        dispatch(trimWhitespace(line));  // so "logout " is accepted like "logout"
    }
    out_ << '\n';
}

bool FrontEnd::readLine(std::string& line) {
    if (!std::getline(in_, line)) return false;
    if (!line.empty() && line.back() == '\r') line.pop_back();
    return true;
}

void FrontEnd::dispatch(const std::string& command) {
    if (command.empty()) {
        out_ << "Error: no command entered.\n";
    } else if (!isKnownCommand(command)) {
        out_ << "Error: unrecognized command \"" << command << "\". Valid commands: "
             << commandList() << ".\n";
    } else if (command == "login") {
        handleLogin();
    } else if (!processor_.isLoggedIn()) {
        out_ << "Error: you must log in before using \"" << command << "\".\n";
    } else if (command == "logout") {
        handleLogout();
    } else if (!isPermitted(command, processor_.currentUser().type)) {
        const User& user = processor_.currentUser();
        out_ << "Error: \"" << command << "\" is not permitted for " << user.username
             << " (account type " << user.type << ").\n";
    } else if (command == "create") {
        handleCreate();
    } else if (command == "delete") {
        handleDelete();
    } else if (command == "sell") {
        handleSell();
    } else if (command == "buy") {
        handleBuy();
    } else if (command == "refund") {
        handleRefund();
    } else if (command == "addcredit") {
        handleAddCredit();
    } else {
        // Unreachable: dispatch only reaches here for a known command.
        out_ << "Error: \"" << command << "\" has no handler.\n";
    }
}

void FrontEnd::handleLogin() {
    if (processor_.isLoggedIn()) {
        out_ << "Error: already logged in as " << processor_.currentUser().username
             << "; log out first.\n";
        return;
    }
    out_ << "Enter username: ";
    std::string username;
    if (!readLine(username)) return;
    // Matched exactly as typed, including case and surrounding spaces: the handout
    // doesn't say otherwise (docs, section 5 #18).
    bool accepted = false;
    try {
        accepted = processor_.login(username);
    } catch (const std::exception& error) {  // a data file could not be read
        out_ << "Error: " << error.what() << ". Login rejected.\n";
        return;
    }
    if (accepted) {
        out_ << "Login accepted. Welcome, " << username << ".\n";
    } else {
        out_ << "Error: no user named \"" << username << "\". Login rejected.\n";
    }
}

void FrontEnd::handleLogout() {
    const std::string username = processor_.currentUser().username;  // copied: logout ends the session
    if (processor_.logout()) {
        out_ << "Logout accepted. Session for " << username << " ended.\n";
    } else {
        out_ << "Error: could not write the Daily Transaction File; " << username
             << " is still logged in.\n";
    }
}

bool FrontEnd::readField(const std::string& prompt, std::string& field) {
    out_ << prompt;
    if (!readLine(field)) {
        out_ << "\nError: unexpected end of input; command abandoned.\n";
        return false;
    }
    return true;
}

void FrontEnd::handleCreate() {
    std::string username;
    std::string userType;
    if (!readField("Enter the new username: ", username)) return;
    if (!readField("Enter the account type (admin, full-standard, buy-standard, "
                   "sell-standard): ", userType))
        return;
    if (processor_.createUser(username, userType)) {
        out_ << "Create accepted. User " << username << " created.\n";
    } else {
        out_ << "Error: create of " << username << " was not accepted.\n";
    }
}

void FrontEnd::handleDelete() {
    std::string username;
    if (!readField("Enter the username to delete: ", username)) return;
    if (processor_.deleteUser(username)) {
        out_ << "Delete accepted. User " << username << " deleted.\n";
    } else {
        out_ << "Error: delete of " << username << " was not accepted.\n";
    }
}

void FrontEnd::handleSell() {
    std::string gameName;
    std::string priceText;
    if (!readField("Enter the game name: ", gameName)) return;
    if (!readField("Enter the asking price (e.g. 15.00): ", priceText)) return;
    long long priceCents = 0;
    if (!money::parseCents(trimWhitespace(priceText), priceCents)) {
        out_ << "Error: \"" << priceText << "\" is not a price like 15.00.\n";
        return;
    }
    if (processor_.sell(gameName, priceCents)) {
        out_ << "Sell accepted. " << gameName << " is for sale.\n";
    } else {
        out_ << "Error: sell of " << gameName << " was not accepted.\n";
    }
}

void FrontEnd::handleBuy() {
    std::string gameName;
    std::string sellerName;
    if (!readField("Enter the game name: ", gameName)) return;
    if (!readField("Enter the seller's username: ", sellerName)) return;
    if (processor_.buy(gameName, sellerName)) {
        out_ << "Buy accepted. " << processor_.currentUser().username
             << " now owns " << gameName << ".\n";
    } else {
        out_ << "Error: buy of " << gameName << " was not accepted.\n";
    }
}

void FrontEnd::handleRefund() {
    std::string buyerName;
    std::string sellerName;
    std::string amountText;
    if (!readField("Enter the buyer's username: ", buyerName)) return;
    if (!readField("Enter the seller's username: ", sellerName)) return;
    if (!readField("Enter the refund amount (e.g. 15.00): ", amountText)) return;
    long long amountCents = 0;
    if (!money::parseCents(trimWhitespace(amountText), amountCents)) {
        out_ << "Error: \"" << amountText << "\" is not an amount like 15.00.\n";
        return;
    }
    if (processor_.refund(buyerName, sellerName, amountCents)) {
        out_ << "Refund accepted. " << amountText << " moved from " << sellerName
             << " to " << buyerName << ".\n";
    } else {
        out_ << "Error: refund from " << sellerName << " to " << buyerName
             << " was not accepted.\n";
    }
}

void FrontEnd::handleAddCredit() {
    std::string amountText;
    if (!readField("Enter the amount to add (e.g. 15.00): ", amountText)) return;
    long long amountCents = 0;
    if (!money::parseCents(trimWhitespace(amountText), amountCents)) {
        out_ << "Error: \"" << amountText << "\" is not an amount like 15.00.\n";
        return;
    }
    // An admin adds credit to any account and is asked for the username after
    // the amount; everyone else adds credit only to their own account.
    std::string username = processor_.currentUser().username;
    if (processor_.currentUser().type == "AA") {
        if (!readField("Enter the username to add the credit to: ", username)) return;
    }
    if (processor_.addCredit(username, amountCents)) {
        out_ << "Addcredit accepted. " << amountText << " added to " << username << ".\n";
    } else {
        out_ << "Error: addcredit to " << username << " was not accepted.\n";
    }
}
