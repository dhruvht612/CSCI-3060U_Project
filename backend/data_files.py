"""
data_files.py - Reads and writes the three fixed-width data files.

  Current User Accounts File   one UserAccount per line   (28 characters)
  Available Games File         one GameForSale per line   (49 characters)
  Games Collection File        one OwnedGame per line     (42 characters)

Each file ends with a special record named END. The reading and writing steps
are the same for all three files, so they live in the DataFile base class; each
subclass only says how long its lines are and how to turn one line into a record.
"""

from constants import (
    END_OF_FILE_NAME, USERNAME_WIDTH, USER_TYPE_WIDTH, CREDIT_WIDTH, GAME_NAME_WIDTH,
    PRICE_WIDTH, VALID_USER_TYPES, USER_ACCOUNT_LINE_LENGTH, AVAILABLE_GAME_LINE_LENGTH,
    COLLECTION_LINE_LENGTH,
)
from error_log import FatalBackEndError
from field_format import FieldFormat, FieldFormatError
from records import UserAccount, GameForSale, OwnedGame


class DataFile:
    """Base class for a fixed-width data file that ends with an END record."""

    LINE_LENGTH = 0            # set by each subclass
    NAME_WIDTH = 0             # width of the first field, which holds END on the last line

    def __init__(self, path):
        """Remember the path of the file to read from or write to."""
        self.path = path

    def read_records(self):
        """Read the file and return its records in order, stopping at the END line.

        Raises FatalBackEndError if a line has the wrong length or a bad field,
        or if the file has no END line.
        """
        records = []
        with open(self.path, "r", encoding="utf-8") as data_file:
            for line_number, raw_line in enumerate(data_file, start=1):
                line = raw_line.rstrip("\r\n")
                if len(line) != self.LINE_LENGTH:
                    raise FatalBackEndError(
                        f"line {line_number} is {len(line)} characters long, expected {self.LINE_LENGTH}",
                        self.path)
                if FieldFormat.read_text(line, 0, self.NAME_WIDTH) == END_OF_FILE_NAME:
                    return records
                try:
                    records.append(self.parse_line(line))
                except FieldFormatError as bad_field:
                    raise FatalBackEndError(f"line {line_number}: {bad_field}", self.path)
        raise FatalBackEndError("file does not end with an END line", self.path)

    def write_records(self, records):
        """Write the given records to the file, one per line, followed by the END line."""
        with open(self.path, "w", encoding="utf-8", newline="\n") as data_file:
            for record in records:
                data_file.write(record.to_line() + "\n")
            data_file.write(self.end_record().to_line() + "\n")

    def parse_line(self, line):
        """Turn one line of the file into a record (implemented by each subclass)."""
        raise NotImplementedError

    def end_record(self):
        """Return the special END record written as the last line (implemented by each subclass)."""
        raise NotImplementedError


class UserAccountsFile(DataFile):
    """The Current User Accounts File: UUUUUUUUUUUUUUU_TT_CCCCCCCCC"""

    LINE_LENGTH = USER_ACCOUNT_LINE_LENGTH
    NAME_WIDTH = USERNAME_WIDTH

    def parse_line(self, line):
        """Turn one accounts line into a UserAccount."""
        username = FieldFormat.read_text(line, 0, USERNAME_WIDTH)
        type_start = USERNAME_WIDTH + 1
        user_type = FieldFormat.read_text(line, type_start, USER_TYPE_WIDTH)
        if user_type not in VALID_USER_TYPES:
            raise FieldFormatError(f"'{user_type}' is not a valid user type")
        credit = FieldFormat.read_money(line, type_start + USER_TYPE_WIDTH + 1, CREDIT_WIDTH)
        return UserAccount(username, user_type, credit)

    def end_record(self):
        """Return the END user, with an empty type and zero credit."""
        return UserAccount(END_OF_FILE_NAME, "", 0)


class AvailableGamesFile(DataFile):
    """The Available Games File: IIIIIIIIIIIIIIIIIIIIIIIIII_SSSSSSSSSSSSSSS_PPPPPP"""

    LINE_LENGTH = AVAILABLE_GAME_LINE_LENGTH
    NAME_WIDTH = GAME_NAME_WIDTH

    def parse_line(self, line):
        """Turn one available games line into a GameForSale."""
        game_name = FieldFormat.read_text(line, 0, GAME_NAME_WIDTH)
        seller_start = GAME_NAME_WIDTH + 1
        seller = FieldFormat.read_text(line, seller_start, USERNAME_WIDTH)
        price = FieldFormat.read_money(line, seller_start + USERNAME_WIDTH + 1, PRICE_WIDTH)
        return GameForSale(game_name, seller, price)

    def end_record(self):
        """Return the END game, with no seller and a zero price."""
        return GameForSale(END_OF_FILE_NAME, "", 0)


class GameCollectionFile(DataFile):
    """The Games Collection File: IIIIIIIIIIIIIIIIIIIIIIIIII_SSSSSSSSSSSSSSS"""

    LINE_LENGTH = COLLECTION_LINE_LENGTH
    NAME_WIDTH = GAME_NAME_WIDTH

    def parse_line(self, line):
        """Turn one collection line into an OwnedGame."""
        game_name = FieldFormat.read_text(line, 0, GAME_NAME_WIDTH)
        owner = FieldFormat.read_text(line, GAME_NAME_WIDTH + 1, USERNAME_WIDTH)
        return OwnedGame(game_name, owner)

    def end_record(self):
        """Return the END collection entry, with no owner."""
        return OwnedGame(END_OF_FILE_NAME, "")
