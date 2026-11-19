"""
backend.py - Games Distribution System Back End (CSCI 3060U, Phase 4 rapid prototype).

Intention
    The Back End is the overnight batch job. It reads yesterday's data files,
    applies every transaction from the Merged Daily Transaction File, and writes
    the new data files that tomorrow's Front End sessions will read.

Input files
    1. Old Current User Accounts File   (28-character lines, ends with END)
    2. Old Available Games File         (49-character lines, ends with END)
    3. Old Games Collection File        (42-character lines, ends with END)
    4. Merged Daily Transaction File    (all Front End daily transaction files
                                         joined together, ending with a 00 line)

Output files
    5. New Current User Accounts File
    6. New Available Games File
    7. New Games Collection File

Terminal output
    One "ERROR: ..." line for each transaction that breaks a business constraint
    (that transaction is skipped). If an input file is found to be bad, one fatal
    "ERROR: ..." line is printed and the Back End stops without writing any output.

How to run (from the repository root)
    python backend/backend.py OLD_ACCOUNTS OLD_GAMES OLD_COLLECTION MERGED_TRANSACTIONS \
                              NEW_ACCOUNTS NEW_GAMES NEW_COLLECTION

    Example:
    python backend/backend.py backend/sample/old_accounts.txt backend/sample/old_games.txt \
        backend/sample/old_collection.txt backend/sample/merged_transactions.txt \
        new_accounts.txt new_games.txt new_collection.txt

Exit status: 0 on success, 1 on a fatal error or wrong arguments.
"""

import sys

from data_files import UserAccountsFile, AvailableGamesFile, GameCollectionFile
from error_log import ErrorLog, FatalBackEndError
from transaction_processor import TransactionProcessor
from transactions import TransactionFileReader

USAGE = ("usage: python backend.py OLD_ACCOUNTS OLD_GAMES OLD_COLLECTION MERGED_TRANSACTIONS "
         "NEW_ACCOUNTS NEW_GAMES NEW_COLLECTION")
EXPECTED_ARGUMENT_COUNT = 7


def run_backend(old_accounts_path, old_games_path, old_collection_path, transactions_path,
                new_accounts_path, new_games_path, new_collection_path, error_log):
    """Read the old files and the merged transactions, apply them, and write the new files.

    Raises FatalBackEndError if any input file is bad; in that case nothing is written.
    """
    user_accounts = UserAccountsFile(old_accounts_path).read_records()
    games_for_sale = AvailableGamesFile(old_games_path).read_records()
    owned_games = GameCollectionFile(old_collection_path).read_records()
    transactions = TransactionFileReader(transactions_path).read_transactions()

    processor = TransactionProcessor(user_accounts, games_for_sale, owned_games, error_log)
    processor.apply_all(transactions)

    UserAccountsFile(new_accounts_path).write_records(processor.user_accounts())
    AvailableGamesFile(new_games_path).write_records(processor.games_for_sale)
    GameCollectionFile(new_collection_path).write_records(processor.owned_games)


def main(arguments):
    """Check the command-line arguments, run the Back End, and return the exit status."""
    if len(arguments) != EXPECTED_ARGUMENT_COUNT:
        print(USAGE)
        return 1
    error_log = ErrorLog()
    try:
        run_backend(*arguments, error_log=error_log)
    except FatalBackEndError as fatal_error:
        error_log.fatal(fatal_error)
        return 1
    except OSError as file_problem:
        # A file that is missing or cannot be opened is also a fatal error.
        error_log.fatal(FatalBackEndError(file_problem.strerror, file_problem.filename))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
