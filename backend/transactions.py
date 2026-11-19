"""
transactions.py - Reads the Merged Daily Transaction File into Transaction objects.

The merged file is every Front End's daily transaction file joined together,
ending with an empty one (just a 00 line). Each line has one of four layouts,
chosen by its two-digit code:

  00, 01, 02, 06   XX_UUUUUUUUUUUUUUU_TT_CCCCCCCCC                              (31 chars)
  05               XX_UUUUUUUUUUUUUUU_SSSSSSSSSSSSSSS_CCCCCCCCC                  (44 chars)
  03               XX_IIIIIIIIIIIIIIIIIIIIIIIIII_SSSSSSSSSSSSSSS_PPPPPP          (52 chars)
  04               XX_IIIIIIIIIIIIIIIIIIIIIIIIII_SSSSSSSSSSSSSSS_UUUUUUUUUUUUUUU_PPPPPP  (68 chars)
"""

from constants import (
    END_OF_SESSION, CREATE, DELETE, SELL, BUY, REFUND, ADD_CREDIT, TRANSACTION_CODE_WIDTH,
    USERNAME_WIDTH, USER_TYPE_WIDTH, CREDIT_WIDTH, GAME_NAME_WIDTH, PRICE_WIDTH,
    ACCOUNT_TRANSACTION_LINE_LENGTH, REFUND_TRANSACTION_LINE_LENGTH,
    SELL_TRANSACTION_LINE_LENGTH, BUY_TRANSACTION_LINE_LENGTH,
)
from error_log import FatalBackEndError
from field_format import FieldFormat, FieldFormatError


class Transaction:
    """One line of the merged daily transaction file, split into named fields.

    Only the fields used by a transaction's code are filled in; the others stay None.
      username   - the account the transaction is about (create, delete, add credit)
      user_type  - the account type (create, delete, add credit)
      amount     - credit (create, add credit), refund amount, or game price, in cents
      buyer      - the buyer (buy, refund)
      seller     - the seller (sell, buy, refund)
      game_name  - the game (sell, buy)
      line       - the original text line, used when reporting an error
    """

    def __init__(self, code, line):
        """Create a transaction with the given two-digit code and its original line."""
        self.code = code
        self.line = line
        self.username = None
        self.user_type = None
        self.amount = None
        self.buyer = None
        self.seller = None
        self.game_name = None


class TransactionFileReader:
    """Reads the Merged Daily Transaction File and turns each line into a Transaction."""

    def __init__(self, path):
        """Remember the path of the merged daily transaction file."""
        self.path = path
        # Which method reads which code, and how long a line with that code must be.
        self.line_readers = {
            END_OF_SESSION: (self._read_account_line, ACCOUNT_TRANSACTION_LINE_LENGTH),
            CREATE: (self._read_account_line, ACCOUNT_TRANSACTION_LINE_LENGTH),
            DELETE: (self._read_account_line, ACCOUNT_TRANSACTION_LINE_LENGTH),
            ADD_CREDIT: (self._read_account_line, ACCOUNT_TRANSACTION_LINE_LENGTH),
            REFUND: (self._read_refund_line, REFUND_TRANSACTION_LINE_LENGTH),
            SELL: (self._read_sell_line, SELL_TRANSACTION_LINE_LENGTH),
            BUY: (self._read_buy_line, BUY_TRANSACTION_LINE_LENGTH),
        }

    def read_transactions(self):
        """Return every transaction in the file, in order.

        Raises FatalBackEndError on an unknown code, a line of the wrong length,
        a bad money field, or a file that does not end with a 00 line.
        """
        transactions = []
        with open(self.path, "r", encoding="utf-8") as transaction_file:
            for line_number, raw_line in enumerate(transaction_file, start=1):
                line = raw_line.rstrip("\r\n")
                transactions.append(self._read_line(line, line_number))
        if not transactions or transactions[-1].code != END_OF_SESSION:
            raise FatalBackEndError("file does not end with an end of session (00) line", self.path)
        return transactions

    def _read_line(self, line, line_number):
        """Turn one line into a Transaction, checking its code and length first."""
        code = line[:TRANSACTION_CODE_WIDTH]
        if code not in self.line_readers:
            raise FatalBackEndError(f"line {line_number} has unknown transaction code '{code}'", self.path)
        read_fields, expected_length = self.line_readers[code]
        if len(line) != expected_length:
            raise FatalBackEndError(
                f"line {line_number} is {len(line)} characters long, expected {expected_length} "
                f"for code {code}", self.path)
        transaction = Transaction(code, line)
        try:
            read_fields(transaction, line)
        except FieldFormatError as bad_field:
            raise FatalBackEndError(f"line {line_number}: {bad_field}", self.path)
        return transaction

    # Each reader below fills in the fields for one line layout. Columns start
    # after the two-digit code and the space that follows it.

    @staticmethod
    def _read_account_line(transaction, line):
        """Fill in username, user type and credit for a 00, 01, 02 or 06 line."""
        column = TRANSACTION_CODE_WIDTH + 1
        transaction.username = FieldFormat.read_text(line, column, USERNAME_WIDTH)
        column += USERNAME_WIDTH + 1
        transaction.user_type = FieldFormat.read_text(line, column, USER_TYPE_WIDTH)
        column += USER_TYPE_WIDTH + 1
        transaction.amount = FieldFormat.read_money(line, column, CREDIT_WIDTH)

    @staticmethod
    def _read_refund_line(transaction, line):
        """Fill in buyer, seller and refund amount for a 05 line."""
        column = TRANSACTION_CODE_WIDTH + 1
        transaction.buyer = FieldFormat.read_text(line, column, USERNAME_WIDTH)
        column += USERNAME_WIDTH + 1
        transaction.seller = FieldFormat.read_text(line, column, USERNAME_WIDTH)
        column += USERNAME_WIDTH + 1
        transaction.amount = FieldFormat.read_money(line, column, CREDIT_WIDTH)

    @staticmethod
    def _read_sell_line(transaction, line):
        """Fill in game name, seller and price for a 03 line."""
        column = TRANSACTION_CODE_WIDTH + 1
        transaction.game_name = FieldFormat.read_text(line, column, GAME_NAME_WIDTH)
        column += GAME_NAME_WIDTH + 1
        transaction.seller = FieldFormat.read_text(line, column, USERNAME_WIDTH)
        column += USERNAME_WIDTH + 1
        transaction.amount = FieldFormat.read_money(line, column, PRICE_WIDTH)

    @staticmethod
    def _read_buy_line(transaction, line):
        """Fill in game name, seller, buyer and price for a 04 line."""
        column = TRANSACTION_CODE_WIDTH + 1
        transaction.game_name = FieldFormat.read_text(line, column, GAME_NAME_WIDTH)
        column += GAME_NAME_WIDTH + 1
        transaction.seller = FieldFormat.read_text(line, column, USERNAME_WIDTH)
        column += USERNAME_WIDTH + 1
        transaction.buyer = FieldFormat.read_text(line, column, USERNAME_WIDTH)
        column += USERNAME_WIDTH + 1
        transaction.amount = FieldFormat.read_money(line, column, PRICE_WIDTH)
