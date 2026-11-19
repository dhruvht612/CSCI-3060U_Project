"""
field_format.py - Converts between Python values and fixed-width file fields.

All money is kept inside the Back End as a whole number of cents, so that
adding and subtracting credit never suffers from floating point rounding.
"""


class FieldFormatError(Exception):
    """Raised when a field in an input file cannot be read (for example, a price that is not a number)."""


class FieldFormat:
    """Helper methods that read and write the fixed-width text fields used in every project file."""

    @staticmethod
    def pad_text(text, width):
        """Return text left-justified and filled with spaces to exactly the given width."""
        return text.ljust(width)[:width]

    @staticmethod
    def read_text(line, start, width):
        """Return the text field of the given width starting at column start, with trailing padding removed."""
        return line[start:start + width].rstrip()

    @staticmethod
    def format_money(cents, width):
        """Return cents as dollars with two decimals, zero-filled on the left to the given width (e.g. 1500 -> '015.00')."""
        dollars, remainder = divmod(cents, 100)
        return f"{dollars}.{remainder:02d}".zfill(width)

    @staticmethod
    def read_money(line, start, width):
        """Return the money field of the given width starting at column start as a number of cents."""
        field = line[start:start + width]
        dollars, dot, cents = field.partition(".")
        if dot != "." or not dollars.isdigit() or not cents.isdigit() or len(cents) != 2:
            raise FieldFormatError(f"'{field}' is not a valid money amount")
        return int(dollars) * 100 + int(cents)
