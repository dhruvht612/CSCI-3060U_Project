"""Render the Phase 2 UML class diagram as a PNG for the design document.

Run from the repository root:  python tools\render_class_diagram.py
Output: docs/phase2_class_diagram.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# (x, y, title, attributes, operations)
BOXES = [
    (0, 5, "FrontEnd",
     ["- processor_ : TransactionProcessor&", "- in_ : istream&", "- out_ : ostream&"],
     ["+ FrontEnd(processor, in, out)", "+ run() : void",
      "- readLine(line&) : bool", "- dispatch(command) : void",
      "- handleLogin() : void", "- handleLogout() : void",
      "- handleCreate() : void", "- handleDelete() : void",
      "- handleSell() : void", "- handleBuy() : void",
      "- handleRefund() : void", "- handleAddCredit() : void",
      "- readField(prompt, field&) : bool"]),
    (7.6, 5, "TransactionProcessor",
     ["- files_ : FileManager&", "- users_ : UserManager", "- games_ : GameManager",
      "- session_ : optional<User>", "- records_ : vector<string>"],
     ["+ TransactionProcessor(files)", "+ isLoggedIn() : bool",
      "+ currentUser() : const User&", "+ login(username) : bool",
      "+ logout() : bool", "+ createUser(username, userType) : bool",
      "+ deleteUser(username) : bool", "+ sell(gameName, priceCents) : bool",
      "+ buy(gameName, sellerName) : bool",
      "+ refund(buyerName, sellerName, amountCents) : bool",
      "+ addCredit(username, amountCents) : bool"]),
    (16.2, 5.2, "UserManager",
     ["- users_ : vector<User>"],
     ["+ UserManager(users)", "+ find(username) : const User*",
      "+ removeUser(username) : bool", "+ adjustCredit(username, deltaCents) : bool"]),
    (16.2, 1.6, "GameManager",
     ["- games_ : vector<Game>", "- collections_ : vector<CollectionEntry>"],
     ["+ GameManager(games, collections)", "+ find(gameName) : const Game*",
      "+ isOwnedBy(gameName, username) : bool",
      "+ addToCollection(gameName, owner) : void",
      "+ removeGamesBySeller(seller) : void"]),
    (16.2, -2.2, "FileManager",
     ["- usersPath_ : string", "- gamesPath_ : string",
      "- collectionsPath_ : string", "- transactionsPath_ : string"],
     ["+ FileManager(4 paths)", "+ loadUsers() : vector<User>",
      "+ loadGames() : vector<Game>", "+ loadCollections() : vector<CollectionEntry>",
      "+ writeTransactions(records) : bool"]),
    (0, 1.0, "User",
     ["+ username : string", "+ type : string", "+ creditCents : long long"],
     ["(data only - no methods)"]),
    (7.6, 1.0, "Game / CollectionEntry",
     ["+ name : string (Game)", "+ seller : string (Game)",
      "+ priceCents : long long (Game)", "+ gameName : string (CollectionEntry)",
      "+ owner : string (CollectionEntry)"],
     ["(data only - no methods)"]),
]

BOX_W = 6.4
TITLE_H, ROW_H, PAD = 0.75, 0.62, 0.12
BAR = 0.28  # extra height for the divider bars


def box_height(n_attr, n_op):
    return TITLE_H + PAD + n_attr * ROW_H + BAR + n_op * ROW_H + PAD


fig, ax = plt.subplots(figsize=(19, 13.5))
ax.set_xlim(-1, 23.5)
ax.set_ylim(-6.5, 14.2)
ax.axis("off")
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

centers = {}
for x, y, title, attrs, ops in BOXES:
    h = box_height(len(attrs), len(ops))
    bottom = y - h / 2
    ax.add_patch(FancyBboxPatch((x, bottom), BOX_W, h,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                linewidth=1.6, edgecolor="#1a1a2e", facecolor="#ffffff",
                                zorder=2))
    # title bar
    ax.add_patch(plt.Rectangle((x, y + h / 2 - TITLE_H), BOX_W, TITLE_H,
                               facecolor="#1a1a2e", edgecolor="#1a1a2e", zorder=3))
    ax.text(x + BOX_W / 2, y + h / 2 - TITLE_H / 2, title, ha="center", va="center",
            fontsize=13, fontweight="bold", color="white", zorder=4)
    # attributes
    ty = y + h / 2 - TITLE_H - PAD - ROW_H / 2 + 0.08
    for a in attrs:
        ax.text(x + 0.22, ty, a, ha="left", va="center", fontsize=10.5,
                family="Consolas", color="#16213e", zorder=4)
        ty -= ROW_H
    # divider
    div_y = ty + ROW_H / 2 - 0.16
    ax.plot([x + 0.08, x + BOX_W - 0.08], [div_y, div_y],
            color="#1a1a2e", linewidth=1.1, zorder=4)
    # operations
    ty = div_y - BAR / 2 - ROW_H / 2 + 0.12
    for o in ops:
        ax.text(x + 0.22, ty, o, ha="left", va="center", fontsize=10.5,
                family="Consolas", color="#16213e", zorder=4)
        ty -= ROW_H
    centers[title] = (x, y, x + BOX_W, bottom, y + h / 2)


def arrow(p1, p2, style="-|>", color="#3a506b", ls="-", rad=0.0, lw=1.5):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=16,
                                 color=color, linewidth=lw, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", zorder=1))


def label(x, y, text, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=9.5, style="italic",
            color="#3a506b",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="none", alpha=0.9), zorder=5)


# FrontEnd --> TransactionProcessor : sends commands
arrow((centers["FrontEnd"][2] - 0.4, centers["FrontEnd"][4] - 0.6),
      (centers["TransactionProcessor"][0] + 0.4, centers["TransactionProcessor"][4] - 0.6))
label((centers["FrontEnd"][2] + centers["TransactionProcessor"][0]) / 2,
      centers["FrontEnd"][4] - 0.15, "sends commands")

# TransactionProcessor --> FileManager : loads at login, writes at logout
arrow((centers["TransactionProcessor"][2] - 1.2, centers["TransactionProcessor"][3]),
      (centers["FileManager"][0] + 1.2, centers["FileManager"][4]))
label(centers["TransactionProcessor"][2] + 0.15,
      (centers["TransactionProcessor"][3] + centers["FileManager"][4]) / 2,
      "loads at login,\nwrites at logout", ha="left")

# TransactionProcessor *-- UserManager  and  *-- GameManager (composition)
arrow((centers["TransactionProcessor"][2] - 2.0, centers["TransactionProcessor"][3]),
      (centers["UserManager"][0] + 1.4, centers["UserManager"][3]))
label(centers["UserManager"][0] + 2.6, centers["UserManager"][3] + 0.45, "owns")
arrow((centers["TransactionProcessor"][2] - 1.0, centers["TransactionProcessor"][3]),
      (centers["GameManager"][0] + 1.0, centers["GameManager"][4] + 0.4))
label(centers["GameManager"][0] + 2.2, centers["GameManager"][4] + 0.85, "owns")

# UserManager *-- User ; GameManager *-- Game ; GameManager *-- CollectionEntry
arrow((centers["UserManager"][0] + 1.0, centers["UserManager"][3]),
      (centers["User"][2] - 1.0, centers["User"][4]))
label(centers["User"][2] + 0.15, centers["User"][4] + 0.3, "holds", ha="left")
arrow((centers["GameManager"][0] + 2.0, centers["GameManager"][3]),
      (centers["Game / CollectionEntry"][0] + 2.0, centers["Game / CollectionEntry"][4]))
label(centers["Game / CollectionEntry"][0] + 2.55,
      (centers["GameManager"][3] + centers["Game / CollectionEntry"][4]) / 2, "holds")

# note: main.cpp wiring
ax.text(2.2, -5.7,
        "main.cpp: FileManager -> TransactionProcessor -> FrontEnd (composition above);\n"
        "stdin = transaction stream, stdout = prompts/results, files = see I/O diagram in the design document.",
        ha="left", va="center", fontsize=10, color="#3a506b",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f4f8", edgecolor="#3a506b"))

ax.set_title("Games Distribution System - UML Class Diagram (CSCI 3060U, Phase 2)",
             fontsize=15, fontweight="bold", color="#1a1a2e", pad=14)

plt.tight_layout()
fig.savefig("docs/phase2_class_diagram.png", dpi=170, facecolor="white",
            bbox_inches="tight")
print("wrote docs/phase2_class_diagram.png")
