// Games Distribution System - Front End (CSCI 3060U, Fall 2026)
//
// A console point-of-purchase terminal for buying and selling games. It reads
// a stream of transactions (login, logout, create, delete, sell, buy, refund,
// addcredit) from standard input, one item per line, and at each logout writes
// the session's transactions to the Daily Transaction File.
//
// Usage:
//   games-distribution <users-file> <games-file> <collections-file> <daily-transaction-file>
//
// Input files (read at each login):
//   users-file              Current User Accounts File
//   games-file              Available Games File
//   collections-file        Game Collection File
// Output file:
//   daily-transaction-file  Daily Transaction File, rewritten at each logout
// Standard input is the transaction stream; standard output shows prompts and
// results. The program ends when standard input ends.
//
// Phase 2 prototype: login, logout and the prompting for every command work;
// the transactions themselves are stubs until Phase 3. See
// docs/phase2_design_notes.md.

#include <exception>
#include <iostream>

#include "FileManager.h"
#include "FrontEnd.h"
#include "TransactionProcessor.h"

int main(int argc, char* argv[]) {
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0]
                  << " <users-file> <games-file> <collections-file> <daily-transaction-file>\n";
        return 1;
    }
    try {
        FileManager files(argv[1], argv[2], argv[3], argv[4]);
        TransactionProcessor processor(files);
        FrontEnd(processor, std::cin, std::cout).run();
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
