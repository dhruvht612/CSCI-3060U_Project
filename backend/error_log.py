"""
error_log.py - Writes Back End errors to the terminal in the required form.

Every error line has the form   ERROR: <msg>
  - failed constraint errors name the constraint and the transaction that broke it;
  - fatal errors name the problem and the file that caused it, and stop the Back End.
"""

import sys


class FatalBackEndError(Exception):
    """Raised when an input file is found to be bad; the Back End must stop immediately."""

    def __init__(self, description, file_name):
        """Store a description of the problem and the name of the file that caused it."""
        super().__init__(description)
        self.description = description
        self.file_name = file_name


class ErrorLog:
    """Prints failed constraint errors and fatal errors to the terminal."""

    def __init__(self, output=sys.stdout):
        """Create an error log that writes to the given stream (the terminal by default)."""
        self.output = output

    def constraint_failure(self, constraint, description, transaction_line):
        """Report that a transaction broke a business constraint and was skipped."""
        print(f"ERROR: Failed constraint ({constraint}): {description}. "
              f"Transaction: '{transaction_line}'", file=self.output)

    def fatal(self, error):
        """Report a fatal error (a FatalBackEndError) found while reading an input file."""
        print(f"ERROR: Fatal error: {error.description}. File: {error.file_name}", file=self.output)
