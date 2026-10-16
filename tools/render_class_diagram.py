"""Draws the Phase 2 UML class diagram to docs/phase2_class_diagram.png.

Run from the repository root:  python tools/render_class_diagram.py
Requires matplotlib. Coordinates are in inches on a 16 x 11.32 page, the same
aspect ratio as the image slot in docs/Phase2_Design_Document.docx.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

PAGE_WIDTH, PAGE_HEIGHT = 16.0, 11.32
LINE_HEIGHT = 0.21      # height of one attribute/method line
HEADER_HEIGHT = 0.42    # height of the class-name band
PADDING = 0.10          # space above and below each compartment
FONT = "DejaVu Sans Mono"
INK = "#1a1a2e"
LINE = "#34495e"

# Each class: name, (left x, top y, width), attributes, methods.
CLASSES = {
    "FrontEnd": ((0.3, 10.6, 4.5),
                 ["- processor_ : TransactionProcessor&", "- in_ : istream&", "- out_ : ostream&"],
                 ["+ FrontEnd(processor, in, out)", "+ run() : void",
                  "- readLine(line&) : bool", "- dispatch(command) : void",
                  "- handleLogin() : void", "- handleLogout() : void",
                  "- handleCreate() : void", "- handleDelete() : void",
                  "- handleSell() : void", "- handleBuy() : void",
                  "- handleRefund() : void", "- handleAddCredit() : void",
                  "- readField(prompt, field&) : bool"]),
    "TransactionProcessor": ((5.6, 10.6, 5.0),
                             ["- files_ : const FileManager&", "- users_ : UserManager",
                              "- games_ : GameManager", "- session_ : optional<User>",
                              "- records_ : vector<string>"],
                             ["+ TransactionProcessor(files)", "+ isLoggedIn() : bool",
                              "+ currentUser() : const User&", "+ login(username) : bool",
                              "+ logout() : bool", "+ createUser(username, userType) : bool",
                              "+ deleteUser(username) : bool", "+ sell(gameName, priceCents) : bool",
                              "+ buy(gameName, sellerName) : bool",
                              "+ refund(buyerName, sellerName, amountCents) : bool",
                              "+ addCredit(username, amountCents) : bool"]),
    "FileManager": ((11.4, 10.6, 4.3),
                    ["- usersPath_ : string", "- gamesPath_ : string",
                     "- collectionsPath_ : string", "- transactionsPath_ : string"],
                    ["+ FileManager(4 paths)", "+ loadUsers() : vector<User>",
                     "+ loadGames() : vector<Game>",
                     "+ loadCollections() : vector<CollectionEntry>",
                     "+ writeTransactions(records) : bool"]),
    "UserManager": ((3.4, 6.0, 3.9),
                    ["- users_ : vector<User>"],
                    ["+ UserManager(users)", "+ find(username) : const User*",
                     "+ removeUser(username) : bool",
                     "+ adjustCredit(username, deltaCents) : bool"]),
    "GameManager": ((8.6, 6.0, 4.2),
                    ["- games_ : vector<Game>", "- collections_ : vector<CollectionEntry>"],
                    ["+ GameManager(games, collections)", "+ find(gameName) : const Game*",
                     "+ isOwnedBy(gameName, username) : bool",
                     "+ addToCollection(gameName, owner) : void",
                     "+ removeGamesBySeller(seller) : void"]),
    "User": ((3.85, 3.05, 3.0),
             ["+ username : string", "+ type : string", "+ creditCents : long long"],
             ["(data only, no methods)"]),
    "Game": ((7.7, 3.05, 2.85),
             ["+ name : string", "+ seller : string", "+ priceCents : long long"],
             ["(data only, no methods)"]),
    "CollectionEntry": ((10.85, 3.05, 2.85),
                        ["+ gameName : string", "+ owner : string"],
                        ["(data only, no methods)"]),
}


def box_height(attributes, methods):
    return (HEADER_HEIGHT + 2 * PADDING + len(attributes) * LINE_HEIGHT
            + 2 * PADDING + len(methods) * LINE_HEIGHT)


def draw_class(ax, name, geometry, attributes, methods):
    """Draws one class box (name band, attributes, methods) and returns its bounds."""
    left, top, width = geometry
    height = box_height(attributes, methods)
    ax.add_patch(FancyBboxPatch((left, top - height), width, height,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="white", edgecolor=INK, linewidth=1.6))
    ax.add_patch(FancyBboxPatch((left, top - HEADER_HEIGHT), width, HEADER_HEIGHT,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=INK, edgecolor=INK))
    ax.text(left + width / 2, top - HEADER_HEIGHT / 2, name, ha="center", va="center",
            color="white", fontsize=12, fontweight="bold")
    y = top - HEADER_HEIGHT - PADDING
    for line in attributes:
        ax.text(left + 0.12, y - LINE_HEIGHT / 2, line, va="center", fontsize=9, family=FONT)
        y -= LINE_HEIGHT
    y -= PADDING
    ax.plot([left, left + width], [y, y], color=INK, linewidth=1)
    y -= PADDING
    for line in methods:
        style = "italic" if line.startswith("(") else "normal"
        ax.text(left + 0.12, y - LINE_HEIGHT / 2, line, va="center", fontsize=9,
                family=FONT, style=style)
        y -= LINE_HEIGHT
    return {"left": left, "right": left + width, "top": top, "bottom": top - height,
            "cx": left + width / 2}


def draw_arrow(ax, start, end, label, label_offset=(0, 0.14)):
    """Draws a navigable association (open arrowhead at `end`) with a label."""
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=LINE, linewidth=1.5,
                                mutation_scale=18, shrinkA=0, shrinkB=0))
    mid = ((start[0] + end[0]) / 2 + label_offset[0], (start[1] + end[1]) / 2 + label_offset[1])
    ax.text(*mid, label, ha="center", va="center", fontsize=9, style="italic", color=LINE,
            bbox=dict(facecolor="white", edgecolor="none", pad=1))


def draw_composition(ax, whole, part, label):
    """Draws a composition: filled diamond at the `whole` end, plain line to `part`."""
    (wx, wy), (px, py) = whole, part
    length = ((px - wx) ** 2 + (py - wy) ** 2) ** 0.5
    ux, uy = (px - wx) / length, (py - wy) / length   # unit vector whole -> part
    nx, ny = -uy, ux                                  # perpendicular
    size, half_width = 0.24, 0.09
    tip = (wx, wy)
    side1 = (wx + ux * size / 2 + nx * half_width, wy + uy * size / 2 + ny * half_width)
    back = (wx + ux * size, wy + uy * size)
    side2 = (wx + ux * size / 2 - nx * half_width, wy + uy * size / 2 - ny * half_width)
    ax.add_patch(Polygon([tip, side1, back, side2], closed=True, facecolor=LINE, edgecolor=LINE))
    ax.plot([back[0], px], [back[1], py], color=LINE, linewidth=1.5)
    ax.text((wx + px) / 2 + 0.12, (wy + py) / 2, label, ha="left", va="center", fontsize=9,
            style="italic", color=LINE, bbox=dict(facecolor="white", edgecolor="none", pad=1))


def main():
    fig = plt.figure(figsize=(PAGE_WIDTH, PAGE_HEIGHT), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PAGE_WIDTH)
    ax.set_ylim(0, PAGE_HEIGHT)
    ax.axis("off")

    ax.text(PAGE_WIDTH / 2, 11.0, "Games Distribution System: UML Class Diagram (CSCI 3060U, Phase 2)",
            ha="center", va="center", fontsize=15, fontweight="bold", color=INK)

    b = {name: draw_class(ax, name, *spec) for name, spec in CLASSES.items()}

    # FrontEnd -> TransactionProcessor, TransactionProcessor -> FileManager.
    draw_arrow(ax, (b["FrontEnd"]["right"], 9.6), (b["TransactionProcessor"]["left"], 9.6),
               "sends\ncommands", label_offset=(0, 0.3))
    draw_arrow(ax, (b["TransactionProcessor"]["right"], 9.6), (b["FileManager"]["left"], 9.6),
               "loads at login,\nwrites at logout", label_offset=(0, 0.3))

    # TransactionProcessor owns one UserManager and one GameManager.
    tp_bottom = b["TransactionProcessor"]["bottom"]
    draw_composition(ax, (6.6, tp_bottom), (b["UserManager"]["cx"], b["UserManager"]["top"]), "owns 1")
    draw_composition(ax, (9.6, tp_bottom), (b["GameManager"]["cx"], b["GameManager"]["top"]), "owns 1")

    # The managers own their data records.
    draw_composition(ax, (b["UserManager"]["cx"], b["UserManager"]["bottom"]),
                     (b["User"]["cx"], b["User"]["top"]), "0..*")
    draw_composition(ax, (b["GameManager"]["cx"] - 0.6, b["GameManager"]["bottom"]),
                     (b["Game"]["cx"], b["Game"]["top"]), "0..*")
    draw_composition(ax, (b["GameManager"]["cx"] + 0.6, b["GameManager"]["bottom"]),
                     (b["CollectionEntry"]["cx"], b["CollectionEntry"]["top"]), "0..*")

    # FileManager builds the records it reads (dependency, dashed).
    ax.annotate("", xy=(b["CollectionEntry"]["right"], 2.6), xytext=(14.6, b["FileManager"]["bottom"]),
                arrowprops=dict(arrowstyle="->", color=LINE, linewidth=1.2, linestyle="--",
                                connectionstyle="angle,angleA=-90,angleB=0"))
    ax.text(14.45, 7.3, "creates User, Game and\nCollectionEntry records\nfrom the data files",
            fontsize=9, style="italic", color=LINE, va="center", ha="right")

    legend = ("Legend:  +  public    -  private    ->  uses    filled diamond  owns (composition)    "
              "dashed  creates\n"
              "Inputs: stdin -> FrontEnd (commands and fields); users, games and collections files -> FileManager.\n"
              "Outputs: stdout <- FrontEnd (prompts and results); Daily Transaction File <- FileManager at logout.\n"
              "main.cpp builds FileManager, then TransactionProcessor, then FrontEnd, and calls FrontEnd::run().")
    ax.text(0.3, 0.75, legend, fontsize=9.5, va="center", color=INK, linespacing=1.6,
            bbox=dict(facecolor="#eef2f7", edgecolor=LINE, boxstyle="round,pad=0.5"))

    fig.savefig("docs/phase2_class_diagram.png", dpi=200, facecolor="white")


if __name__ == "__main__":
    main()
