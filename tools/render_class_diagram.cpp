// Draws the Phase 2 UML class diagram as an SVG image.
//
// This is a stand-alone documentation tool, not part of the Front End: it is
// kept in tools/ so that `src/*.cpp` still builds only the Front End.
//
// Build and run from the repository root:
//   g++ -std=c++17 -Wall -Wextra tools/render_class_diagram.cpp -o build/render_class_diagram
//   build/render_class_diagram
// Output: docs/phase2_class_diagram.svg (open it in a browser, or insert it in Word).
//
// All coordinates are in pixels, with y growing downwards as in SVG.

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {

const int kPageWidth = 1600;
const int kPageHeight = 1132;
const int kLineHeight = 21;    // height of one attribute or method line
const int kHeaderHeight = 42;  // height of the band holding the class name
const int kPadding = 10;       // space above and below each compartment
const char* const kInk = "#1a1a2e";   // box outlines and text
const char* const kLine = "#34495e";  // relationship lines and labels

// One class box: its name, position, and the lines in its two compartments.
struct ClassBox {
    std::string name;
    int left;
    int top;
    int width;
    std::vector<std::string> attributes;
    std::vector<std::string> methods;

    int height() const {
        return kHeaderHeight + 2 * kPadding + static_cast<int>(attributes.size()) * kLineHeight +
               2 * kPadding + static_cast<int>(methods.size()) * kLineHeight;
    }
    int right() const { return left + width; }
    int bottom() const { return top + height(); }
    int centerX() const { return left + width / 2; }
};

// Replaces the characters that have a special meaning in SVG text (<, >, &).
std::string escapeXml(const std::string& text) {
    std::string escaped;
    for (char c : text) {
        if (c == '<') escaped += "&lt;";
        else if (c == '>') escaped += "&gt;";
        else if (c == '&') escaped += "&amp;";
        else escaped += c;
    }
    return escaped;
}

// Writes one line of text. `anchor` is "start", "middle" or "end"; `style` is
// extra SVG attributes such as a font or colour.
void writeText(std::ostream& svg, int x, int y, const std::string& text,
               const std::string& anchor, const std::string& style) {
    svg << "<text x=\"" << x << "\" y=\"" << y << "\" text-anchor=\"" << anchor
        << "\" dominant-baseline=\"middle\" xml:space=\"preserve\" " << style << ">" << escapeXml(text) << "</text>\n";
}

// Writes a label for a relationship line: small italic text on a white background.
void writeLabel(std::ostream& svg, int x, int y, const std::string& text, const std::string& anchor) {
    writeText(svg, x, y, text, anchor,
              std::string("font-size=\"12\" font-style=\"italic\" fill=\"") + kLine +
                  "\" stroke=\"white\" stroke-width=\"4\" paint-order=\"stroke\"");
}

// Draws one class box: dark name band, attributes, a divider, then methods.
void drawClass(std::ostream& svg, const ClassBox& box) {
    svg << "<rect x=\"" << box.left << "\" y=\"" << box.top << "\" width=\"" << box.width
        << "\" height=\"" << box.height() << "\" rx=\"6\" fill=\"white\" stroke=\"" << kInk
        << "\" stroke-width=\"2\"/>\n";
    svg << "<rect x=\"" << box.left << "\" y=\"" << box.top << "\" width=\"" << box.width
        << "\" height=\"" << kHeaderHeight << "\" rx=\"6\" fill=\"" << kInk << "\"/>\n";
    writeText(svg, box.centerX(), box.top + kHeaderHeight / 2, box.name, "middle",
              "font-size=\"17\" font-weight=\"bold\" fill=\"white\"");

    const std::string memberStyle = "font-family=\"monospace\" font-size=\"13\"";
    int y = box.top + kHeaderHeight + kPadding;
    for (const std::string& attribute : box.attributes) {
        writeText(svg, box.left + 12, y + kLineHeight / 2, attribute, "start", memberStyle);
        y += kLineHeight;
    }
    y += kPadding;
    svg << "<line x1=\"" << box.left << "\" y1=\"" << y << "\" x2=\"" << box.right() << "\" y2=\""
        << y << "\" stroke=\"" << kInk << "\"/>\n";
    y += kPadding;
    for (const std::string& method : box.methods) {
        const bool isNote = method[0] == '(';  // e.g. "(data only, no methods)"
        writeText(svg, box.left + 12, y + kLineHeight / 2, method, "start",
                  memberStyle + (isNote ? " font-style=\"italic\"" : ""));
        y += kLineHeight;
    }
}

// Draws a "uses" association: a straight line with a filled arrowhead at the end.
void drawArrow(std::ostream& svg, int x1, int y1, int x2, int y2) {
    svg << "<line x1=\"" << x1 << "\" y1=\"" << y1 << "\" x2=\"" << x2 << "\" y2=\"" << y2
        << "\" stroke=\"" << kLine << "\" stroke-width=\"2\" marker-end=\"url(#arrowhead)\"/>\n";
}

// Draws a composition: a filled diamond on the owning ("whole") end and a plain
// line to the owned ("part") end.
void drawComposition(std::ostream& svg, int wholeX, int wholeY, int partX, int partY) {
    svg << "<line x1=\"" << wholeX << "\" y1=\"" << wholeY << "\" x2=\"" << partX << "\" y2=\""
        << partY << "\" stroke=\"" << kLine << "\" stroke-width=\"2\" marker-start=\"url(#diamond)\"/>\n";
}

}  // namespace

int main() {
    const std::vector<ClassBox> boxes = {
        {"FrontEnd", 30, 72, 450,
         {"- processor_ : TransactionProcessor&", "- in_ : istream&", "- out_ : ostream&"},
         {"+ FrontEnd(processor, in, out)", "+ run() : void", "- readLine(line&) : bool",
          "- dispatch(command) : void", "- handleLogin() : void", "- handleLogout() : void",
          "- handleCreate() : void", "- handleDelete() : void", "- handleSell() : void",
          "- handleBuy() : void", "- handleRefund() : void", "- handleAddCredit() : void",
          "- readField(prompt, field&) : bool"}},
        {"TransactionProcessor", 560, 72, 500,
         {"- files_ : const FileManager&", "- users_ : UserManager", "- games_ : GameManager",
          "- session_ : optional<User>", "- records_ : vector<string>"},
         {"+ TransactionProcessor(files)", "+ isLoggedIn() : bool", "+ currentUser() : const User&",
          "+ login(username) : bool", "+ logout() : bool",
          "+ createUser(username, userType) : bool", "+ deleteUser(username) : bool",
          "+ sell(gameName, priceCents) : bool", "+ buy(gameName, sellerName) : bool",
          "+ refund(buyerName, sellerName, amountCents) : bool",
          "+ addCredit(username, amountCents) : bool"}},
        {"FileManager", 1140, 72, 430,
         {"- usersPath_ : string", "- gamesPath_ : string", "- collectionsPath_ : string",
          "- transactionsPath_ : string"},
         {"+ FileManager(4 paths)", "+ loadUsers() : vector<User>", "+ loadGames() : vector<Game>",
          "+ loadCollections() : vector<CollectionEntry>", "+ writeTransactions(records) : bool"}},
        {"UserManager", 340, 532, 390,
         {"- users_ : vector<User>"},
         {"+ UserManager(users)", "+ find(username) : const User*", "+ removeUser(username) : bool",
          "+ adjustCredit(username, deltaCents) : bool"}},
        {"GameManager", 860, 532, 420,
         {"- games_ : vector<Game>", "- collections_ : vector<CollectionEntry>"},
         {"+ GameManager(games, collections)", "+ find(gameName) : const Game*",
          "+ isOwnedBy(gameName, username) : bool", "+ addToCollection(gameName, owner) : void",
          "+ removeGamesBySeller(seller) : void"}},
        {"User", 385, 827, 300,
         {"+ username : string", "+ type : string", "+ creditCents : long long"},
         {"(data only, no methods)"}},
        {"Game", 770, 827, 285,
         {"+ name : string", "+ seller : string", "+ priceCents : long long"},
         {"(data only, no methods)"}},
        {"CollectionEntry", 1085, 827, 285,
         {"+ gameName : string", "+ owner : string"},
         {"(data only, no methods)"}},
    };
    // Named references into `boxes`, in the order listed above.
    const ClassBox& frontEnd = boxes[0];
    const ClassBox& processor = boxes[1];
    const ClassBox& fileManager = boxes[2];
    const ClassBox& userManager = boxes[3];
    const ClassBox& gameManager = boxes[4];
    const ClassBox& user = boxes[5];
    const ClassBox& game = boxes[6];
    const ClassBox& collectionEntry = boxes[7];

    const std::string outputPath = "docs/phase2_class_diagram.svg";
    std::ofstream svg(outputPath);
    if (!svg) {
        std::cerr << "Error: cannot write " << outputPath << " (run from the repository root)\n";
        return 1;
    }

    svg << "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"" << kPageWidth << "\" height=\""
        << kPageHeight << "\" viewBox=\"0 0 " << kPageWidth << " " << kPageHeight
        << "\" font-family=\"Segoe UI, DejaVu Sans, Arial, sans-serif\" fill=\"" << kInk << "\">\n";
    // Arrowhead, open arrowhead and composition diamond, used by the lines below.
    svg << "<defs>\n"
        << "<marker id=\"arrowhead\" viewBox=\"0 0 10 10\" refX=\"10\" refY=\"5\" markerWidth=\"9\""
           " markerHeight=\"9\" orient=\"auto\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"" << kLine << "\"/></marker>\n"
        << "<marker id=\"openhead\" viewBox=\"0 0 10 10\" refX=\"10\" refY=\"5\" markerWidth=\"9\""
           " markerHeight=\"9\" orient=\"auto\"><path d=\"M0,0 L10,5 L0,10\" fill=\"none\" stroke=\""
        << kLine << "\" stroke-width=\"1.5\"/></marker>\n"
        << "<marker id=\"diamond\" viewBox=\"0 0 24 12\" refX=\"0\" refY=\"6\" markerWidth=\"24\""
           " markerHeight=\"12\" markerUnits=\"userSpaceOnUse\" orient=\"auto\">"
           "<path d=\"M0,6 L12,0 L24,6 L12,12 z\" fill=\"" << kLine << "\"/></marker>\n"
        << "</defs>\n";
    svg << "<rect width=\"100%\" height=\"100%\" fill=\"white\"/>\n";

    writeText(svg, kPageWidth / 2, 32,
              "Games Distribution System: UML Class Diagram (CSCI 3060U, Phase 2)", "middle",
              "font-size=\"22\" font-weight=\"bold\"");

    for (const ClassBox& box : boxes) drawClass(svg, box);

    // FrontEnd -> TransactionProcessor -> FileManager.
    const int arrowY = 172;
    drawArrow(svg, frontEnd.right(), arrowY, processor.left, arrowY);
    writeLabel(svg, (frontEnd.right() + processor.left) / 2, arrowY - 40, "sends", "middle");
    writeLabel(svg, (frontEnd.right() + processor.left) / 2, arrowY - 24, "commands", "middle");
    drawArrow(svg, processor.right(), arrowY, fileManager.left, arrowY);
    writeLabel(svg, (processor.right() + fileManager.left) / 2, arrowY - 40, "loads at login,", "middle");
    writeLabel(svg, (processor.right() + fileManager.left) / 2, arrowY - 24, "writes at logout", "middle");

    // TransactionProcessor owns one UserManager and one GameManager.
    drawComposition(svg, 660, processor.bottom(), userManager.centerX(), userManager.top);
    writeLabel(svg, 612, (processor.bottom() + userManager.top) / 2 + 4, "owns 1", "start");
    drawComposition(svg, 960, processor.bottom(), gameManager.centerX(), gameManager.top);
    writeLabel(svg, 1045, (processor.bottom() + gameManager.top) / 2 + 4, "owns 1", "start");

    // Each manager owns any number of its data records.
    drawComposition(svg, userManager.centerX(), userManager.bottom(), user.centerX(), user.top);
    writeLabel(svg, userManager.centerX() + 12, (userManager.bottom() + user.top) / 2, "0..*", "start");
    drawComposition(svg, gameManager.centerX() - 60, gameManager.bottom(), game.centerX(), game.top);
    writeLabel(svg, game.centerX() + 35, (gameManager.bottom() + game.top) / 2, "0..*", "end");
    drawComposition(svg, gameManager.centerX() + 60, gameManager.bottom(),
                    collectionEntry.centerX(), collectionEntry.top);
    writeLabel(svg, collectionEntry.centerX() - 20, (gameManager.bottom() + collectionEntry.top) / 2,
               "0..*", "start");

    // FileManager creates the data records it reads (dependency: dashed line, open arrowhead).
    const int dependencyX = 1460;
    const int dependencyY = collectionEntry.top + 45;
    svg << "<polyline points=\"" << dependencyX << "," << fileManager.bottom() << " " << dependencyX
        << "," << dependencyY << " " << collectionEntry.right() << "," << dependencyY
        << "\" fill=\"none\" stroke=\"" << kLine
        << "\" stroke-width=\"1.5\" stroke-dasharray=\"7,5\" marker-end=\"url(#openhead)\"/>\n";
    writeLabel(svg, dependencyX - 15, 390, "creates User, Game and", "end");
    writeLabel(svg, dependencyX - 15, 407, "CollectionEntry records", "end");
    writeLabel(svg, dependencyX - 15, 424, "from the data files", "end");

    // Legend, with where the program's inputs and outputs fit.
    const std::vector<std::string> legend = {
        "Legend:  + public  |  - private  |  arrow = uses  |  filled diamond = owns (composition)  |  dashed = creates",
        "Inputs: stdin -> FrontEnd (commands and fields); users, games and collections files -> FileManager.",
        "Outputs: stdout <- FrontEnd (prompts and results); Daily Transaction File <- FileManager at logout.",
        "main.cpp builds FileManager, then TransactionProcessor, then FrontEnd, and calls FrontEnd::run()."};
    const int legendTop = 1000;
    svg << "<rect x=\"20\" y=\"" << legendTop << "\" width=\"720\" height=\""
        << 20 + 24 * static_cast<int>(legend.size()) << "\" rx=\"6\" fill=\"#eef2f7\" stroke=\""
        << kLine << "\"/>\n";
    for (std::size_t i = 0; i < legend.size(); ++i) {
        writeText(svg, 32, legendTop + 22 + 24 * static_cast<int>(i), legend[i], "start", "font-size=\"13\"");
    }

    svg << "</svg>\n";
    svg.close();
    if (svg.fail()) {
        std::cerr << "Error: failed while writing " << outputPath << "\n";
        return 1;
    }
    std::cout << "Wrote " << outputPath << "\n";
    return 0;
}
