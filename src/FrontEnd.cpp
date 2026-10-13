#include "FrontEnd.h"

#include <exception>
#include <istream>
#include <ostream>

#include "TransactionProcessor.h"

namespace {

// True for the transaction codes the handout lists.
bool isKnownCommand(const std::string& command) {
    return command == "login" || command == "logout" || command == "create" ||
           command == "delete" || command == "sell" || command == "buy" ||
           command == "refund" || command == "addcredit";
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
    std::string command;
    while (true) {
        out_ << "Enter command: ";
        if (!readLine(command)) break;
        dispatch(command);
    }
    out_ << '\n';
}

bool FrontEnd::readLine(std::string& line) {
    if (!std::getline(in_, line)) return false;
    if (!line.empty() && line.back() == '\r') line.pop_back();
    return true;
}

void FrontEnd::dispatch(const std::string& command) {
    if (!isKnownCommand(command)) {
        out_ << "Error: unrecognized command \"" << command << "\".\n";
    } else if (command == "login") {
        handleLogin();
    } else if (!processor_.isLoggedIn()) {
        out_ << "Error: you must log in first.\n";
    } else if (command == "logout") {
        handleLogout();
    } else if (!isPermitted(command, processor_.currentUser().type)) {
        out_ << "Error: \"" << command << "\" is not permitted for this account type.\n";
    } else {
        // TODO(Phase 2): read this command's fields and call the matching
        // TransactionProcessor method. Until then the field lines that follow
        // in the input are read as commands.
        out_ << "\"" << command << "\" is not implemented yet; nothing was recorded.\n";
    }
}

void FrontEnd::handleLogin() {
    if (processor_.isLoggedIn()) {
        out_ << "Error: a user is already logged in.\n";
        return;
    }
    out_ << "Enter username: ";
    std::string username;
    if (!readLine(username)) return;
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
        out_ << "Error: no user named \"" << username << "\".\n";
    }
}

void FrontEnd::handleLogout() {
    if (processor_.logout()) {
        out_ << "Logout accepted. Session ended.\n";
    } else {
        out_ << "Error: could not write the Daily Transaction File; still logged in.\n";
    }
}
