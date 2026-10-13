#pragma once

#include <iosfwd>
#include <string>

class TransactionProcessor;

// Console front end: reads one command per line, enforces the login and
// account-type restrictions, and passes accepted commands to the processor.
class FrontEnd {
public:
    // Reads commands and fields from `in` and writes prompts and results to `out`.
    FrontEnd(TransactionProcessor& processor, std::istream& in, std::ostream& out);

    // Processes commands until the end of input.
    void run();

private:
    // Reads one line into `line`, dropping a trailing '\r'. Returns false at end of input.
    bool readLine(std::string& line);

    // Applies the session and account-type checks to one command, then runs it.
    void dispatch(const std::string& command);

    // login: prompts for a username and starts the session if it is accepted.
    void handleLogin();

    // logout: ends the session and reports whether the Daily Transaction File was written.
    void handleLogout();

    TransactionProcessor& processor_;
    std::istream& in_;
    std::ostream& out_;
};
