"""Draws the Phase 4 Back End UML class diagram to docs/phase4_class_diagram.png.

Run from the repository root:  python tools/render_phase4_class_diagram.py
Requires matplotlib. Coordinates are in inches on a 20 x 13 page. The drawing
helpers follow tools/render_class_diagram.py (the Phase 2 diagram).
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

PAGE_WIDTH, PAGE_HEIGHT = 20.0, 13.0
LINE_HEIGHT = 0.21      # height of one attribute/method line
HEADER_HEIGHT = 0.42    # height of the class-name band
PADDING = 0.10          # space above and below each compartment
FONT = "DejaVu Sans Mono"
INK = "#1a1a2e"
LINE = "#34495e"

# Each class: (left x, top y, width), attributes, methods.
CLASSES = {
    "backend.py  «main module»": (
        (0.3, 12.2, 4.6),
        ["USAGE : str", "EXPECTED_ARGUMENT_COUNT = 7"],
        ["+ main(arguments) : int", "+ run_backend(7 file paths, error_log)"]),
    "TransactionFileReader": (
        (0.3, 9.9, 4.6),
        ["- path : str", "- line_readers : dict[code, (reader, length)]"],
        ["+ read_transactions() : list[Transaction]", "- _read_line(line, line_number)",
         "- _read_account_line(transaction, line)", "- _read_refund_line(transaction, line)",
         "- _read_sell_line(transaction, line)", "- _read_buy_line(transaction, line)"]),
    "Transaction": (
        (0.3, 6.8, 4.6),
        ["+ code : str", "+ line : str", "+ username : str", "+ user_type : str",
         "+ amount : int (cents)", "+ buyer : str", "+ seller : str", "+ game_name : str"],
        ["(data only, no methods)"]),
    "FieldFormat": (
        (0.3, 3.8, 4.6),
        [],
        ["+ pad_text(text, width) : str", "+ read_text(line, start, width) : str",
         "+ format_money(cents, width) : str", "+ read_money(line, start, width) : int"]),
    "TransactionProcessor": (
        (5.3, 12.2, 5.9),
        ["- users : dict[str, UserAccount]", "- games_for_sale : list[GameForSale]",
         "- owned_games : list[OwnedGame]", "- error_log : ErrorLog",
         "- handlers : dict[code, method]"],
        ["+ __init__(user_accounts, games_for_sale, owned_games, error_log)",
         "+ apply_all(transactions)", "+ user_accounts() : list[UserAccount]",
         "- _end_session(transaction)        00", "- _create_user(transaction)        01",
         "- _delete_user(transaction)        02", "- _sell_game(transaction)          03",
         "- _buy_game(transaction)           04", "- _refund(transaction)             05",
         "- _add_credit(transaction)         06", "- _user_exists(username, transaction) : bool",
         "- _transfer_credit(payer, payee, amount, transaction) : bool"]),
    "UserAccount": (
        (5.6, 6.4, 5.3),
        ["+ username : str", "+ user_type : str", "+ credit_cents : int"],
        ["+ to_line() : str          (28 chars)"]),
    "GameForSale": (
        (5.6, 4.45, 5.3),
        ["+ game_name : str", "+ seller : str", "+ price_cents : int"],
        ["+ to_line() : str          (49 chars)"]),
    "OwnedGame": (
        (5.6, 2.5, 5.3),
        ["+ game_name : str", "+ owner : str"],
        ["+ to_line() : str          (42 chars)"]),
    "ErrorLog": (
        (11.7, 12.2, 5.2),
        ["- output : stream (terminal)"],
        ["+ constraint_failure(constraint, description,", "      transaction_line)",
         "+ fatal(error : FatalBackEndError)"]),
    "FatalBackEndError  «exception»": (
        (11.7, 10.3, 5.2),
        ["+ description : str", "+ file_name : str"],
        ["+ __init__(description, file_name)"]),
    "DataFile  «abstract»": (
        (13.0, 8.4, 6.6),
        ["- path : str", "LINE_LENGTH : int", "NAME_WIDTH : int"],
        ["+ read_records() : list[record]", "+ write_records(records)",
         "+ parse_line(line) : record            {abstract}",
         "+ end_record() : record                {abstract}"]),
    "UserAccountsFile": (
        (11.7, 5.5, 2.6),
        ["LINE_LENGTH = 28"],
        ["+ parse_line(line)", "+ end_record()"]),
    "AvailableGamesFile": (
        (14.4, 5.5, 2.6),
        ["LINE_LENGTH = 49"],
        ["+ parse_line(line)", "+ end_record()"]),
    "GameCollectionFile": (
        (17.1, 5.5, 2.6),
        ["LINE_LENGTH = 42"],
        ["+ parse_line(line)", "+ end_record()"]),
}


def box_height(attributes, methods):
    """Return the height of a class box with the given number of lines."""
    return (HEADER_HEIGHT + 2 * PADDING + len(attributes) * LINE_HEIGHT
            + 2 * PADDING + len(methods) * LINE_HEIGHT)


def draw_class(ax, name, geometry, attributes, methods):
    """Draw one class box (name band, attributes, methods) and return its bounds."""
    left, top, width = geometry
    height = box_height(attributes, methods)
    ax.add_patch(FancyBboxPatch((left, top - height), width, height,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="white", edgecolor=INK, linewidth=1.6))
    ax.add_patch(FancyBboxPatch((left, top - HEADER_HEIGHT), width, HEADER_HEIGHT,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=INK, edgecolor=INK))
    ax.text(left + width / 2, top - HEADER_HEIGHT / 2, name, ha="center", va="center",
            color="white", fontsize=11.5, fontweight="bold")
    y = top - HEADER_HEIGHT - PADDING
    for line in attributes:
        ax.text(left + 0.12, y - LINE_HEIGHT / 2, line, va="center", fontsize=8.5, family=FONT)
        y -= LINE_HEIGHT
    y -= PADDING
    ax.plot([left, left + width], [y, y], color=INK, linewidth=1)
    y -= PADDING
    for line in methods:
        style = "italic" if line.startswith("(") else "normal"
        ax.text(left + 0.12, y - LINE_HEIGHT / 2, line, va="center", fontsize=8.5,
                family=FONT, style=style)
        y -= LINE_HEIGHT
    return {"left": left, "right": left + width, "top": top, "bottom": top - height,
            "cx": left + width / 2}


def label(ax, x, y, text, ha="center"):
    """Write an italic relationship label on a white background."""
    ax.text(x, y, text, ha=ha, va="center", fontsize=9, style="italic", color=LINE,
            bbox=dict(facecolor="white", edgecolor="none", pad=1))


def draw_arrow(ax, points, dashed=False):
    """Draw a 'uses' arrow along the given points, with the arrowhead at the last point."""
    xs, ys = zip(*points)
    style = "--" if dashed else "-"
    ax.plot(xs[:-1] + (xs[-1],), ys[:-1] + (ys[-1],), color=LINE, linewidth=1.4, linestyle=style)
    ax.annotate("", xy=points[-1], xytext=points[-2],
                arrowprops=dict(arrowstyle="-|>", color=LINE, linewidth=1.4,
                                mutation_scale=16, shrinkA=0, shrinkB=0))


def draw_composition(ax, whole, part):
    """Draw a composition: filled diamond at the `whole` end (pointing up), plain line down to `part`."""
    (wx, wy), (px, py) = whole, part
    size, half_width = 0.24, 0.09
    ax.add_patch(Polygon([(wx, wy), (wx + half_width, wy - size / 2), (wx, wy - size),
                          (wx - half_width, wy - size / 2)], closed=True,
                         facecolor=LINE, edgecolor=LINE))
    ax.plot([wx, px], [wy - size, py], color=LINE, linewidth=1.5)


def draw_inheritance(ax, parent_bottom, child_tops):
    """Draw generalization lines from each child up to one hollow triangle under the parent."""
    px, py = parent_bottom
    size = 0.22
    ax.add_patch(Polygon([(px, py), (px + size / 2, py - size), (px - size / 2, py - size)],
                         closed=True, facecolor="white", edgecolor=LINE, linewidth=1.4))
    join_y = py - size - 0.25
    ax.plot([px, px], [py - size, join_y], color=LINE, linewidth=1.4)
    xs = [x for x, _ in child_tops]
    ax.plot([min(xs), max(xs)], [join_y, join_y], color=LINE, linewidth=1.4)
    for x, y in child_tops:
        ax.plot([x, x], [join_y, y], color=LINE, linewidth=1.4)


def main():
    """Draw every class and relationship and save the PNG."""
    fig = plt.figure(figsize=(PAGE_WIDTH, PAGE_HEIGHT), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PAGE_WIDTH)
    ax.set_ylim(0, PAGE_HEIGHT)
    ax.axis("off")

    ax.text(PAGE_WIDTH / 2, 12.68,
            "Games Distribution System Back End: UML Class Diagram (CSCI 3060U, Phase 4)",
            ha="center", va="center", fontsize=15, fontweight="bold", color=INK)

    b = {name.split()[0]: draw_class(ax, name, *spec) for name, spec in CLASSES.items()}

    # The records group: TransactionProcessor owns lists of all three record types.
    group_top = b["UserAccount"]["top"] + 0.3
    ax.add_patch(Rectangle((5.4, b["OwnedGame"]["bottom"] - 0.2), 5.7,
                           group_top - b["OwnedGame"]["bottom"] + 0.2,
                           fill=False, edgecolor=LINE, linestyle="--", linewidth=1.2))
    ax.text(10.95, group_top - 0.15, "records.py", ha="right", va="center", fontsize=9, color=LINE)
    draw_composition(ax, (b["TransactionProcessor"]["cx"], b["TransactionProcessor"]["bottom"]),
                     (b["TransactionProcessor"]["cx"], group_top))
    label(ax, b["TransactionProcessor"]["cx"] + 0.15,
          (b["TransactionProcessor"]["bottom"] + group_top) / 2 - 0.1,
          "holds 0..* of each", ha="left")

    # backend.py drives everything.
    draw_arrow(ax, [(2.6, b["backend.py"]["bottom"]), (2.6, b["TransactionFileReader"]["top"])])
    label(ax, 2.75, (b["backend.py"]["bottom"] + b["TransactionFileReader"]["top"]) / 2,
          "reads merged transactions", ha="left")
    draw_arrow(ax, [(b["backend.py"]["right"], 11.4), (b["TransactionProcessor"]["left"], 11.4)])
    label(ax, 5.1, 11.65, "applies")
    draw_arrow(ax, [(1.2, b["backend.py"]["top"]), (1.2, 12.42), (19.35, 12.42),
                    (19.35, b["DataFile"]["top"])])
    label(ax, 18.2, 12.42, "reads old / writes new data files")

    # Reader creates Transactions; processor applies them.
    draw_arrow(ax, [(2.6, b["TransactionFileReader"]["bottom"]), (2.6, b["Transaction"]["top"])])
    label(ax, 2.75, (b["TransactionFileReader"]["bottom"] + b["Transaction"]["top"]) / 2,
          "creates 0..*", ha="left")
    draw_arrow(ax, [(b["TransactionProcessor"]["left"] + 0.25, b["TransactionProcessor"]["bottom"]),
                    (b["TransactionProcessor"]["left"] + 0.25, 6.2), (b["Transaction"]["right"], 6.2)])
    label(ax, 5.05, 6.45, "applies")

    # Processor reports failed constraints; data files and reader raise fatal errors.
    draw_arrow(ax, [(b["TransactionProcessor"]["right"], 11.4), (b["ErrorLog"]["left"], 11.4)])
    label(ax, 11.45, 11.65, "reports")
    draw_arrow(ax, [(b["DataFile"]["left"] + 0.6, b["DataFile"]["top"]),
                    (b["DataFile"]["left"] + 0.6, b["FatalBackEndError"]["bottom"])], dashed=True)
    label(ax, b["DataFile"]["left"] + 0.75, (b["DataFile"]["top"] + b["FatalBackEndError"]["bottom"]) / 2,
          "raises", ha="left")

    # Data file class hierarchy, and the records they read and write.
    draw_inheritance(ax, (b["DataFile"]["cx"], b["DataFile"]["bottom"]),
                     [(b[name]["cx"], b[name]["top"])
                      for name in ("UserAccountsFile", "AvailableGamesFile", "GameCollectionFile")])
    draw_arrow(ax, [(b["UserAccountsFile"]["left"], 4.6), (11.1, 4.6)], dashed=True)
    label(ax, 11.4, 4.35, "creates /\nwrites")

    legend = (
        "Legend:  +  public    -  private    ->  uses    filled diamond  owns    hollow triangle  inherits\n"
        "            dashed arrow  creates / raises\n\n"
        "Inputs (command-line paths, read by DataFile subclasses and\n"
        "  TransactionFileReader): old user accounts, old available games,\n"
        "  old games collection, merged daily transaction file.\n"
        "Outputs: new user accounts, new available games and new games\n"
        "  collection files (written by DataFile subclasses);\n"
        "  'ERROR: ...' lines on the terminal (written by ErrorLog).\n\n"
        "All money is int cents. FieldFormat is used by every reader and\n"
        "  to_line(); it raises FieldFormatError, which the readers turn\n"
        "  into a FatalBackEndError. Field widths live in constants.py.")
    ax.text(11.7, 2.25, legend, fontsize=9, va="center", color=INK, linespacing=1.45,
            family=FONT, bbox=dict(facecolor="#eef2f7", edgecolor=LINE, boxstyle="round,pad=0.5"))

    fig.savefig("docs/phase4_class_diagram.png", dpi=150, facecolor="white")


if __name__ == "__main__":
    main()
