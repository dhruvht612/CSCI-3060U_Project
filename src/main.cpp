// Games Distribution System - Front End (CSCI 3060U, Fall 2026)
//
// A console point-of-purchase terminal for buying and selling games. It reads
// a stream of transactions (login, logout, create, delete, sell, buy, refund,
// addcredit, list) from standard input, one item per line, and at each logout
// writes the session's transactions to the Daily Transaction File.
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
// When standard input is a file or pipe rather than a terminal, each input line is
// echoed after its prompt so saved terminal logs show what the user would see.
//
// Phase 3: session validation and records 00-06. See docs/Phase3_Execution_Guide.md
// and docs/Phase3_Format_Decisions.md for the file formats used.

#include <exception>
#include <iostream>

#ifdef _WIN32
#include <io.h>
#define STDIN_IS_TERMINAL() (_isatty(_fileno(stdin)) != 0)
#else
#include <unistd.h>
#define STDIN_IS_TERMINAL() (isatty(STDIN_FILENO) != 0)
#endif

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
        // When the transactions come from a file (e.g. "< inputs/TC01.txt"), echo
        // each input line so the terminal log reads like an interactive session.
        const bool echoInput = !STDIN_IS_TERMINAL();
        FrontEnd(processor, std::cin, std::cout, echoInput).run();
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 1;
    }
    return 0;
}
