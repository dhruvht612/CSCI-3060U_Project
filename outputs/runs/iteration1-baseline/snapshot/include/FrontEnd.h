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

    // Processes commands until the end of input. Whitespace around a command is
    // ignored; commands stay case-sensitive.
    void run();

private:
    // Reads one line into `line`, dropping a trailing '\r'. Returns false at end of input.
    bool readLine(std::string& line);

    // Applies the session and account-type checks to one command (already
    // trimmed), then runs it.
    void dispatch(const std::string& command);

    // login: prompts for a username and starts the session if it is accepted.
    void handleLogin();

    // logout: ends the session and reports whether the Daily Transaction File was written.
    void handleLogout();

    // create: prompts for the new username and account type, then asks the processor to create it.
    void handleCreate();

    // delete: prompts for the username to remove, then asks the processor to delete it.
    void handleDelete();

    // sell: prompts for the game name and asking price, then asks the processor to list it.
    void handleSell();

    // buy: prompts for the game name and the seller's username, then asks the processor to buy it.
    void handleBuy();

    // refund: prompts for the buyer, seller and amount, then asks the processor to refund.
    void handleRefund();

    // addcredit: prompts for the amount (and the target username for an admin),
    // then asks the processor to add the credit.
    void handleAddCredit();

    // list: prints every active account and its details (admin only).
    void handleList();

    // Reads one prompt and line of a command's fields into `field`. Prints an
    // "unexpected end of input" error and returns false if input ends mid-command.
    bool readField(const std::string& prompt, std::string& field);

    TransactionProcessor& processor_;
    std::istream& in_;
    std::ostream& out_;
};
