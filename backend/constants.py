"""
constants.py - Field widths, transaction codes and limits used by the Back End.

These values come from the project handout and from the Front End we now use
(Front End A from the "NewFrontEnds3" folder). Front End A writes every file
exactly as the handout describes, with game names 26 characters wide.

If the client changes a field width or a limit, this is the only file that
should need to change.
"""

# ---- Field widths in the fixed-width files ----
USERNAME_WIDTH = 15      # left-justified, padded with spaces
USER_TYPE_WIDTH = 2      # AA, FS, BS, SS
CREDIT_WIDTH = 9         # e.g. 001000.00
GAME_NAME_WIDTH = 26     # left-justified, padded with spaces
PRICE_WIDTH = 6          # e.g. 015.00
TRANSACTION_CODE_WIDTH = 2

# ---- Expected line lengths (without the newline) ----
USER_ACCOUNT_LINE_LENGTH = USERNAME_WIDTH + 1 + USER_TYPE_WIDTH + 1 + CREDIT_WIDTH        # 28
AVAILABLE_GAME_LINE_LENGTH = GAME_NAME_WIDTH + 1 + USERNAME_WIDTH + 1 + PRICE_WIDTH       # 49
COLLECTION_LINE_LENGTH = GAME_NAME_WIDTH + 1 + USERNAME_WIDTH                             # 42

# Daily transaction file lines (the two-digit code and a space come first)
ACCOUNT_TRANSACTION_LINE_LENGTH = TRANSACTION_CODE_WIDTH + 1 + USER_ACCOUNT_LINE_LENGTH   # 31: codes 00, 01, 02, 06
REFUND_TRANSACTION_LINE_LENGTH = (TRANSACTION_CODE_WIDTH + 1 + USERNAME_WIDTH + 1
                                  + USERNAME_WIDTH + 1 + CREDIT_WIDTH)                    # 44: code 05
SELL_TRANSACTION_LINE_LENGTH = TRANSACTION_CODE_WIDTH + 1 + AVAILABLE_GAME_LINE_LENGTH    # 52: code 03
BUY_TRANSACTION_LINE_LENGTH = (TRANSACTION_CODE_WIDTH + 1 + GAME_NAME_WIDTH + 1
                               + USERNAME_WIDTH + 1 + USERNAME_WIDTH + 1 + PRICE_WIDTH)   # 68: code 04

# ---- The special record that ends every data file ----
END_OF_FILE_NAME = "END"

# ---- User types ----
ADMIN = "AA"
FULL_STANDARD = "FS"
BUY_STANDARD = "BS"
SELL_STANDARD = "SS"
VALID_USER_TYPES = (ADMIN, FULL_STANDARD, BUY_STANDARD, SELL_STANDARD)

# ---- Transaction codes in the daily transaction file ----
END_OF_SESSION = "00"
CREATE = "01"
DELETE = "02"
SELL = "03"
BUY = "04"
REFUND = "05"
ADD_CREDIT = "06"
