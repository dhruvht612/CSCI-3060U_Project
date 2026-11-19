"""
records.py - The three kinds of record the Back End keeps in memory.

Each class holds one line of its data file and knows how to turn itself back
into that line, so the file writers do not need to know the field layout.
"""

from constants import (
    USERNAME_WIDTH, USER_TYPE_WIDTH, CREDIT_WIDTH, GAME_NAME_WIDTH, PRICE_WIDTH,
)
from field_format import FieldFormat


class UserAccount:
    """One user in the Current User Accounts File: name, user type and available credit."""

    def __init__(self, username, user_type, credit_cents):
        """Create a user account with the given name, type code (AA/FS/BS/SS) and credit in cents."""
        self.username = username
        self.user_type = user_type
        self.credit_cents = credit_cents

    def to_line(self):
        """Return this account as a 28-character Current User Accounts File line."""
        return " ".join([
            FieldFormat.pad_text(self.username, USERNAME_WIDTH),
            FieldFormat.pad_text(self.user_type, USER_TYPE_WIDTH),
            FieldFormat.format_money(self.credit_cents, CREDIT_WIDTH),
        ])


class GameForSale:
    """One game in the Available Games File: game name, seller and price."""

    def __init__(self, game_name, seller, price_cents):
        """Create a game for sale with the given name, seller username and price in cents."""
        self.game_name = game_name
        self.seller = seller
        self.price_cents = price_cents

    def to_line(self):
        """Return this game as a 49-character Available Games File line."""
        return " ".join([
            FieldFormat.pad_text(self.game_name, GAME_NAME_WIDTH),
            FieldFormat.pad_text(self.seller, USERNAME_WIDTH),
            FieldFormat.format_money(self.price_cents, PRICE_WIDTH),
        ])


class OwnedGame:
    """One entry in the Games Collection File: a game and the user who owns a copy of it."""

    def __init__(self, game_name, owner):
        """Create a collection entry saying that owner owns game_name."""
        self.game_name = game_name
        self.owner = owner

    def to_line(self):
        """Return this entry as a 42-character Games Collection File line."""
        return " ".join([
            FieldFormat.pad_text(self.game_name, GAME_NAME_WIDTH),
            FieldFormat.pad_text(self.owner, USERNAME_WIDTH),
        ])
