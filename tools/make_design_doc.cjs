// Generates the Phase 2 design document: docs/Phase2_Design_Document.docx
// Run from the repository root:  node tools/make_design_doc.cjs
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun,
  Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  BorderStyle, LevelFormat, PageBreak,
} = require("docx");

const PAGE_W = 12240, PAGE_H = 15840; // US Letter
const MARGIN = 1080;                   // 0.75"
const CONTENT_W = PAGE_W - 2 * MARGIN; // 10080 DXA

const INK = "1A1A2E", ACCENT = "3A506B", LIGHT = "EDF2F7", HEAD_BG = "1A1A2E";

// ---------- helpers ----------

function run(text, opts = {}) {
  return new TextRun({ text, size: 21, color: "222222", ...opts });
}

function para(text, opts = {}) {
  return new Paragraph({
    children: [run(text, opts.run || {})],
    spacing: { after: 160, line: 276 },
    ...opts.para,
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 320, after: 140 },
    children: [new TextRun({ text, size: 28, bold: true, color: INK })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 100 },
    children: [new TextRun({ text, size: 23, bold: true, color: ACCENT })],
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80, line: 276 },
    children: [run(text)],
  });
}

function monoCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({ text, size: 18, font: "Consolas", color: "16213E" })],
      spacing: { after: 0, line: 240 },
    })],
  });
}

function headCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: HEAD_BG },
    margins: { top: 70, bottom: 70, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({ text, size: 19, bold: true, color: "FFFFFF" })],
      spacing: { after: 0 },
    })],
  });
}

function bodyCell(text, width, opts = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: opts.shade ? { type: ShadingType.CLEAR, fill: LIGHT } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({ text, size: 19, color: "222222", ...opts.run })],
      spacing: { after: 0, line: 252 },
    })],
  });
}

function table(colWidths, rows) {
  return new Table({
    columnWidths: colWidths,
    width: { size: colWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    rows,
  });
}

// ---------- content ----------

const classRows = [
  ["FrontEnd", "include/FrontEnd.h, src/FrontEnd.cpp",
   "Runs the console loop: reads each command line, enforces the login and account-type rules, prompts for a command's fields and prints the results."],
  ["TransactionProcessor", "include/TransactionProcessor.h, src/TransactionProcessor.cpp",
   "Owns the login session and the data read for it, validates and applies transactions, and writes the session's records to the Daily Transaction File at logout."],
  ["UserManager", "include/UserManager.h, src/UserManager.cpp",
   "Holds the session's user accounts and answers exact-name lookups and account updates on them."],
  ["GameManager", "include/GameManager.h, src/GameManager.cpp",
   "Holds the session's available games and game collections and answers lookups and ownership queries on them."],
  ["FileManager", "include/FileManager.h, src/FileManager.cpp",
   "Reads the three input data files and overwrites the Daily Transaction File with the session's records."],
  ["User", "include/User.h",
   "Plain data for one account: username, type code (AA, FS, BS, SS) and credit held in integer cents."],
  ["Game", "include/Game.h",
   "Plain data for one game offered for sale: game name, seller's username and price in integer cents."],
  ["CollectionEntry", "include/Game.h",
   "Plain data for one ownership record: the game name and the username of the owner."],
  ["money (namespace)", "include/Money.h",
   "Shared helpers that parse money text such as \"15.00\" into integer cents, used by both FileManager and FrontEnd."],
  ["main program", "src/main.cpp",
   "Checks the command-line arguments, wires FileManager, TransactionProcessor and FrontEnd together and starts the console loop."],
].map(([c, f, d], i) => new TableRow({
  children: [
    monoCell(c, 1900), monoCell(f, 2900), bodyCell(d, 5280, { shade: i % 2 === 1 }),
  ],
}));

const methodRows = [
  ["FrontEnd", [
    ["FrontEnd(processor, in, out)", "processor, input and output streams -> FrontEnd",
     "Sets up a front end that reads commands from in and writes prompts and results to out."],
    ["run()", "-> void",
     "Reads, trims and dispatches commands until the end of the input stream."],
    ["readLine(line&) (private)", "-> line, bool",
     "Reads one input line, dropping a trailing carriage return; returns false at end of input."],
    ["dispatch(command) (private)", "trimmed command -> void",
     "Applies the recognized-command, login and account-type checks in order, then runs the matching handler."],
    ["handleLogin() (private)", "-> void",
     "Prompts for a username, starts the session if the user exists, and reports acceptance or rejection."],
    ["handleLogout() (private)", "-> void",
     "Ends the session by asking the processor to write the Daily Transaction File and reports the result."],
    ["handleCreate() (private)", "-> void",
     "Prompts for the new username and account type and passes them to TransactionProcessor::createUser."],
    ["handleDelete() (private)", "-> void",
     "Prompts for the username to remove and passes it to TransactionProcessor::deleteUser."],
    ["handleSell() (private)", "-> void",
     "Prompts for the game name and asking price, parses the price into cents and passes them to TransactionProcessor::sell."],
    ["handleBuy() (private)", "-> void",
     "Prompts for the game name and the seller's username and passes them to TransactionProcessor::buy."],
    ["handleRefund() (private)", "-> void",
     "Prompts for the buyer, the seller and the amount, parses the amount into cents and passes them to TransactionProcessor::refund."],
    ["handleAddCredit() (private)", "-> void",
     "Prompts for the amount (and for the target username when the current user is an admin) and passes them to TransactionProcessor::addCredit."],
    ["readField(prompt, field&) (private)", "prompt -> field, bool",
     "Prints a prompt, reads one field line, and reports false if the input ends in the middle of a command."],
  ]],
  ["TransactionProcessor", [
    ["TransactionProcessor(files)", "FileManager -> TransactionProcessor",
     "Stores a reference to the file manager used to load and write the session's files."],
    ["isLoggedIn()", "-> bool",
     "Reports whether a user is currently logged in."],
    ["currentUser()", "-> const User&",
     "Returns the logged-in user, throwing std::bad_optional_access if there is no session."],
    ["login(username)", "username -> bool",
     "Reads the user accounts file, accepts the username if the account exists, then reads the games and collections files and starts the session."],
    ["logout()", "-> bool",
     "Writes the session's records followed by the \"00\" end-of-session record to the Daily Transaction File and ends the session, keeping both if the write fails."],
    ["createUser(username, userType)", "username, type word -> bool",
     "Validates the request and records a create (01) transaction. Phase 2 stub: returns false and records nothing."],
    ["deleteUser(username)", "username -> bool",
     "Validates the request, removes the user and their games for sale and records a delete (02) transaction. Phase 2 stub: returns false and records nothing."],
    ["sell(gameName, priceCents)", "game name, price -> bool",
     "Validates the request and records a sell (03) transaction. Phase 2 stub: returns false and records nothing."],
    ["buy(gameName, sellerName)", "game name, seller -> bool",
     "Validates the request, moves the credit, adds the game to the buyer's collection and records a buy (04) transaction. Phase 2 stub: returns false and records nothing."],
    ["refund(buyerName, sellerName, amountCents)", "buyer, seller, amount -> bool",
     "Validates the request, moves the credit from the seller to the buyer and records a refund (05) transaction. Phase 2 stub: returns false and records nothing."],
    ["addCredit(username, amountCents)", "username, amount -> bool",
     "Validates the per-session limit, adds the credit and records an addcredit (06) transaction. Phase 2 stub: returns false and records nothing."],
  ]],
  ["UserManager", [
    ["UserManager(users)", "vector<User> -> UserManager",
     "Takes ownership of the user list read from the accounts file."],
    ["find(username)", "username -> const User*",
     "Returns the user whose username matches exactly, or nullptr if none does."],
    ["removeUser(username)", "username -> bool",
     "Removes the user with that username. Phase 2 stub: returns false."],
    ["adjustCredit(username, deltaCents)", "username, +/- cents -> bool",
     "Adds deltaCents (negative to deduct) to the user's credit. Phase 2 stub: returns false."],
  ]],
  ["GameManager", [
    ["GameManager(games, collections)", "two lists -> GameManager",
     "Takes ownership of the available-games and collections lists read at login."],
    ["find(gameName)", "game name -> const Game*",
     "Returns the available game whose name matches exactly, or nullptr if none does."],
    ["isOwnedBy(gameName, username)", "game name, username -> bool",
     "Reports whether the collections list the user as an owner of that game."],
    ["addToCollection(gameName, owner)", "game name, owner -> void",
     "Records that the owner now owns the game (buy). Phase 2 stub: does nothing."],
    ["removeGamesBySeller(seller)", "seller -> void",
     "Cancels every game the seller has for sale (delete). Phase 2 stub: does nothing."],
  ]],
  ["FileManager", [
    ["FileManager(4 paths)", "four file paths -> FileManager",
     "Stores the paths of the user, games and collections input files and of the Daily Transaction File."],
    ["loadUsers()", "-> vector<User>",
     "Parses the Current User Accounts File up to its END line, throwing std::runtime_error naming the file and line if it is missing or malformed."],
    ["loadGames()", "-> vector<Game>",
     "Parses the Available Games File. Phase 2 stub: returns an empty list; the handout and fixtures disagree on the record width (see open questions)."],
    ["loadCollections()", "-> vector<CollectionEntry>",
     "Parses the Game Collection File. Phase 2 stub: returns an empty list; the handout and fixtures disagree on the record width (see open questions)."],
    ["writeTransactions(records)", "records -> bool",
     "Replaces the Daily Transaction File's contents with one record per line and reports whether the write succeeded."],
  ]],
  ["money namespace", [
    ["money::isDigits(text)", "text -> bool",
     "Reports whether the text is non-empty and contains only decimal digits."],
    ["money::parseCents(text, cents&)", "money text -> cents, bool",
     "Parses digits-dot-two-digits text such as \"15.00\" into integer cents, returning false if the text is not in that form."],
  ]],
  ["main program", [
    ["main(argc, argv)", "command line -> exit status",
     "Checks the four file-path arguments, wires the three objects together, runs the front end and reports any file error on standard error."],
  ]],
];

const methodTables = [];
for (const [cls, rows] of methodRows) {
  methodTables.push(h2(cls));
  methodTables.push(table([2600, 2900, 4580], [
    new TableRow({
      tableHeader: true,
      children: [headCell("Method", 2600), headCell("Input -> output", 2900),
                 headCell("Intention (one sentence)", 4580)],
    }),
    ...rows.map(([m, io, d], i) => new TableRow({
      children: [monoCell(m, 2600), monoCell(io, 2900),
                 bodyCell(d, 4580, { shade: i % 2 === 1 })],
    })),
  ]));
}

const dataFileRows = [
  ["Current User Accounts File (input)", "UUUUUUUUUUUUUUU_TT_CCCCCCCCC (28 chars: name 15, type 2, credit 9)",
   "Parsed by FileManager::loadUsers at each login"],
  ["Available Games File (input)", "Item name, seller, price; handout says 49/42 chars, Phase 1 fixtures use 48 (25-char name)",
   "Loadable by FileManager::loadGames (stub in Phase 2, width conflict is an open question)"],
  ["Game Collection File (input)", "Item name, owner; handout says 42 chars, fixtures use 41 (25-char name)",
   "Loadable by FileManager::loadCollections (stub in Phase 2, width conflict is an open question)"],
  ["Daily Transaction File (output)", "One record per line, codes 01-06 during the session, bare \"00\" at the end",
   "Overwritten by FileManager::writeTransactions at each logout"],
].map(([f, fmt, where], i) => new TableRow({
  children: [bodyCell(f, 3100, { shade: i % 2 === 1, run: { bold: true } }),
             bodyCell(fmt, 3800, { shade: i % 2 === 1 }),
             bodyCell(where, 3180, { shade: i % 2 === 1 })],
}));

const stdinRows = [
  ["login", "username"],
  ["logout", "(none)"],
  ["create", "new username; then user type: admin, full-standard, buy-standard or sell-standard"],
  ["delete", "username to delete"],
  ["sell", "game name; then asking price, e.g. 15.00"],
  ["buy", "game name; then the seller's username"],
  ["refund", "buyer's username; seller's username; amount"],
  ["addcredit", "amount; then the target username, only when logged in as admin"],
].map(([cmd, fields], i) => new TableRow({
  children: [monoCell(cmd, 2000), bodyCell(fields, 8080, { shade: i % 2 === 1 })],
}));

const doc = new Document({
  creator: "Games Distribution Team - CSCI 3060U",
  title: "Games Distribution System - Phase 2 Front End Design Document",
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 21, color: "222222" } },
    },
  },
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 480, hanging: 240 } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
      },
    },
    children: [
      // ---------- title ----------
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 120, after: 60 },
        children: [new TextRun({ text: "Games Distribution System", size: 44, bold: true, color: INK })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 60 },
        children: [new TextRun({ text: "Phase 2 - Front End Design Document", size: 30, color: ACCENT })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: "CSCI 3060U - Fall 2026 - Version 1.0, October 15, 2026", size: 21, color: "666666" })],
      }),

      // ---------- 1. overview ----------
      h1("1. Overview and how to run the program"),
      para("The Games Distribution System is a console point-of-purchase terminal for buying and selling games. This document describes the design of its Front End: the command loop, the session and account-type rules, the prompts for every command, and the files the program reads and writes. This is the Phase 2 rapid prototype; transaction validation behind the prompts is deliberately left for Phase 3."),
      para("The program reads one item per line from standard input: a command, followed by the lines that hold that command's fields. It writes prompts and results to standard output, and file errors to standard error. It ends when standard input ends."),
      h2("Command line"),
      para("games-distribution <users-file> <games-file> <collections-file> <daily-transaction-file>", { run: { font: "Consolas", size: 20 } }),
      para("The four paths are supplied as arguments; passing them this way is the team's choice, as the handout only states that the program is a console application that uses text files. The transaction stream always arrives on standard input."),
      h2("Build"),
      para("g++ -std=c++17 -Wall -Wextra -Iinclude src/*.cpp -o build/games-distribution", { run: { font: "Consolas", size: 20 } }),

      // ---------- 2. structure ----------
      h1("2. Structure of the solution"),
      para("The solution is split so that each class owns one responsibility. FrontEnd handles all console input and output and the account-type permission rules. TransactionProcessor owns the login session, the data read for it and the transaction records. UserManager and GameManager hold the session's user and game data and answer lookups on it. FileManager is the only class that touches files. User, Game and CollectionEntry are plain data with no behaviour. Money parsing is shared through the money namespace so that file records and typed amounts are parsed identically."),
      para("The layers communicate only downwards: FrontEnd sends commands to TransactionProcessor, which loads its data through FileManager and keeps it in UserManager and GameManager. No class reaches upwards; in particular, the data managers know nothing about the console."),
      new Paragraph({
        spacing: { before: 120, after: 60 },
        children: [new ImageRun({
          type: "png",
          data: fs.readFileSync("docs/phase2_class_diagram.png"),
          transformation: { width: 660, height: 467 },
        })],
        alignment: AlignmentType.CENTER,
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [new TextRun({ text: "Figure 1: UML class diagram. Arrows show uses/owns relationships; the composition diamonds of TransactionProcessor over UserManager and GameManager are drawn as \"owns\" links. Regenerate with tools/render_class_diagram.py.", size: 18, italics: true, color: "666666" })],
      }),

      // ---------- 3. classes ----------
      h1("3. Classes"),
      para("Table 1 gives a one-sentence intention for every class in the solution."),
      table([1900, 2900, 5280], [
        new TableRow({
          tableHeader: true,
          children: [headCell("Class", 1900), headCell("Files", 2900),
                     headCell("Intention (one sentence)", 5280)],
        }),
        ...classRows,
      ]),
      new Paragraph({
        spacing: { before: 100, after: 300 },
        children: [new TextRun({ text: "Table 1: Classes and their intentions.", size: 18, italics: true, color: "666666" })],
      }),

      // ---------- 4. methods ----------
      new Paragraph({ children: [new PageBreak()] }),
      h1("4. Methods"),
      para("Tables 2a-2g give a one-sentence intention for every method, its inputs and output, and whether it is implemented in this Phase 2 version. Methods marked \"Phase 2 stub\" exist with the right interface and comments but deliberately return a failure or do nothing; implementing them is Phase 3 work, as the assignment asks for a first version of the Front End rather than a finished product."),
      ...methodTables,
      new Paragraph({
        spacing: { before: 100 },
        children: [new TextRun({ text: "Tables 2a-2g: Methods by class.", size: 18, italics: true, color: "666666" })],
      }),

      // ---------- 5. inputs and outputs ----------
      new Paragraph({ children: [new PageBreak()] }),
      h1("5. Inputs and outputs"),
      h2("Data files"),
      para("Fields in the data files are left-justified and padded with spaces, and money appears as nine characters with cents, e.g. 005000.00. Every input file ends with an END record."),
      table([3100, 3800, 3180], [
        new TableRow({
          tableHeader: true,
          children: [headCell("File", 3100), headCell("Record layout", 3800),
                     headCell("Where it fits", 3180)],
        }),
        ...dataFileRows,
      ]),
      new Paragraph({
        spacing: { before: 100, after: 300 },
        children: [new TextRun({ text: "Table 3: Data files and where they are read or written.", size: 18, italics: true, color: "666666" })],
      }),
      h2("Standard input: transaction stream"),
      para("One item per line: the command, then one line per field, in the order below. Session and account-type rejections happen before any field is prompted for, so a rejected command is followed directly by the next command."),
      table([2000, 8080], [
        new TableRow({
          tableHeader: true,
          children: [headCell("Command", 2000), headCell("Field lines after the command", 8080)],
        }),
        ...stdinRows,
      ]),
      new Paragraph({
        spacing: { before: 100, after: 300 },
        children: [new TextRun({ text: "Table 4: Transaction stream fields.", size: 18, italics: true, color: "666666" })],
      }),
      h2("Standard output and the Daily Transaction File"),
      para("Standard output carries the prompts (\"Enter command: \", \"Enter username: \" and one prompt per field), acceptance messages and errors; all errors begin with \"Error: \". At each logout the Daily Transaction File is replaced with the session's records followed by the bare \"00\" end-of-session record; records 01-06 will be produced once the transaction methods are implemented in Phase 3."),
      para("Where the inputs and outputs fit, in one picture:"),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        children: [new TextRun({
          text: "users file, games file, collections file  ->  FileManager  ->  UserManager / GameManager (loaded at login);  Daily Transaction File written by FileManager at logout.  stdin (commands and fields) -> FrontEnd -> TransactionProcessor -> prompts and results on stdout.",
          font: "Consolas", size: 18, color: "16213E",
        })],
      }),

      // ---------- 6. status ----------
      h1("6. Prototype status and open questions"),
      para("Implemented in this version: the command loop, login, logout with the Daily Transaction File write, the \"log in first\" check, the account-type rules (create/delete/refund admin only; sell for everyone except buy-standard; buy for everyone except sell-standard; addcredit unprivileged), and the field prompting for every command. The six transaction methods of TransactionProcessor are stubs that reject every request, so no 01-06 record is written yet; that behaviour, including all validation limits, is Phase 3 work and is expected to fail many of the Phase 1 requirement tests at this stage."),
      para("Open questions recorded in docs/phase2_design_notes.md (section 5) and awaiting a TA answer include the width of the Available Games and Game Collection file records, the exact layout of the sell, buy, delete, addcredit and 00 records in the Daily Transaction File, and whether the Daily Transaction File is overwritten or appended when a second session runs in the same invocation."),
      para("Sources of the requirements: the project handout (Project_Docs/Extreme Project - Games Distribution (2026).docx.md), the Phase 2 assignment (Project_Docs/2026 CSCI3060U_phase2.docx.md) and the Phase 1 test fixtures in inputs/ and expected/."),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("docs/Phase2_Design_Document.docx", buf);
  console.log("wrote docs/Phase2_Design_Document.docx");
});
