"""
transaction_processor.py - Applies the day's transactions to the users, games and collections.

The processor holds the in-memory copy of all three data files. Each
transaction code has one method that changes that copy. A transaction that
breaks a business constraint is reported to the ErrorLog and skipped; the
rest of the file is still processed.

Business constraints checked here (from the Back End requirements):
  - no user should ever have a negative account balance
  - a newly created user must have a name different from all existing users
A transaction that names a user who does not exist is also reported and skipped,
since it cannot be applied.
"""

from constants import END_OF_SESSION, CREATE, DELETE, SELL, BUY, REFUND, ADD_CREDIT
from records import UserAccount, GameForSale, OwnedGame


class TransactionProcessor:
    """Applies daily transactions to the user accounts, available games and game collections."""

    def __init__(self, user_accounts, games_for_sale, owned_games, error_log):
        """Start from yesterday's records.

        user_accounts  - list of UserAccount from the old Current User Accounts File
        games_for_sale - list of GameForSale from the old Available Games File
        owned_games    - list of OwnedGame from the old Games Collection File
        error_log      - ErrorLog used to report failed constraints
        """
        # Users are kept in a dictionary by name so they can be found quickly;
        # Python dictionaries keep insertion order, so the output file keeps the input order.
        self.users = {account.username: account for account in user_accounts}
        self.games_for_sale = list(games_for_sale)
        self.owned_games = list(owned_games)
        self.error_log = error_log
        # Which method applies which transaction code.
        self.handlers = {
            END_OF_SESSION: self._end_session,
            CREATE: self._create_user,
            DELETE: self._delete_user,
            SELL: self._sell_game,
            BUY: self._buy_game,
            REFUND: self._refund,
            ADD_CREDIT: self._add_credit,
        }

    def apply_all(self, transactions):
        """Apply every transaction, in the order given."""
        for transaction in transactions:
            self.handlers[transaction.code](transaction)

    def user_accounts(self):
        """Return the updated list of UserAccount records."""
        return list(self.users.values())

    # ---- One method per transaction code ----

    def _end_session(self, transaction):
        """00 - end of a Front End session: nothing to change.

        Front End A writes this line with a blank username and type and zero credit.
        """

    def _create_user(self, transaction):
        """01 - add a new user, unless a user with that name already exists."""
        if transaction.username in self.users:
            self.error_log.constraint_failure(
                "unique user name", f"user '{transaction.username}' already exists", transaction.line)
            return
        self.users[transaction.username] = UserAccount(
            transaction.username, transaction.user_type, transaction.amount)

    def _delete_user(self, transaction):
        """02 - remove a user, the games they have for sale, and their game collection."""
        if not self._user_exists(transaction.username, transaction):
            return
        del self.users[transaction.username]
        self.games_for_sale = [game for game in self.games_for_sale
                               if game.seller != transaction.username]
        self.owned_games = [owned for owned in self.owned_games
                            if owned.owner != transaction.username]

    def _sell_game(self, transaction):
        """03 - put a new game up for sale."""
        if not self._user_exists(transaction.seller, transaction):
            return
        self.games_for_sale.append(
            GameForSale(transaction.game_name, transaction.seller, transaction.amount))

    def _buy_game(self, transaction):
        """04 - move the price from buyer to seller and add the game to the buyer's collection."""
        if not (self._user_exists(transaction.buyer, transaction)
                and self._user_exists(transaction.seller, transaction)):
            return
        if not self._transfer_credit(transaction.buyer, transaction.seller, transaction.amount, transaction):
            return
        self.owned_games.append(OwnedGame(transaction.game_name, transaction.buyer))

    def _refund(self, transaction):
        """05 - move the refund amount from the seller back to the buyer."""
        if not (self._user_exists(transaction.buyer, transaction)
                and self._user_exists(transaction.seller, transaction)):
            return
        self._transfer_credit(transaction.seller, transaction.buyer, transaction.amount, transaction)

    def _add_credit(self, transaction):
        """06 - add credit to a user's account.

        Front End A writes the amount that was added (not the new balance), so it is added on.
        """
        if not self._user_exists(transaction.username, transaction):
            return
        self.users[transaction.username].credit_cents += transaction.amount

    # ---- Shared helpers ----

    def _user_exists(self, username, transaction):
        """Return True if the user exists; otherwise report the failed transaction and return False."""
        if username in self.users:
            return True
        self.error_log.constraint_failure(
            "existing user", f"user '{username}' does not exist", transaction.line)
        return False

    def _transfer_credit(self, payer, payee, amount, transaction):
        """Move amount (in cents) from payer to payee.

        Returns False, and changes nothing, if the payer's balance would go negative.
        """
        payer_account = self.users[payer]
        if payer_account.credit_cents - amount < 0:
            self.error_log.constraint_failure(
                "negative balance",
                f"user '{payer}' has only {payer_account.credit_cents / 100:.2f} credit, "
                f"needs {amount / 100:.2f}", transaction.line)
            return False
        payer_account.credit_cents -= amount
        self.users[payee].credit_cents += amount
        return True
