# CSCI-3060U_Project

Games Distribution System: a console front end written in C++ for CSCI 3060U (Fall 2026).

## Status

Early Phase 2 skeleton. Working so far: the command loop, `login`, `logout` (writes the
Daily Transaction File, currently only the `00` end-of-session record), the "log in
first" check and the account-type checks. `create`, `delete`, `sell`, `buy`, `refund`
and `addcredit` are recognized but **not implemented**. See
[docs/phase2_design_notes.md](docs/phase2_design_notes.md) for the design, file formats,
open questions and remaining work.

## Layout

```text
include/        class declarations
src/            class implementations and main.cpp
docs/           design notes
inputs/         Phase 1 test inputs (see Project_Docs/README.txt)
expected/       Phase 1 expected results
Project_Docs/   project handout, phase assignments and Phase 1 documents
```

## Build

Requires a C++17 compiler. From the repository root, in bash (Linux, macOS, Git Bash or MSYS2):

```sh
mkdir -p build
g++ -std=c++17 -Wall -Wextra -Iinclude src/*.cpp -o build/games-distribution
```

`build/` is ignored by git.

## Run

```sh
build/games-distribution <users-file> <games-file> <collections-file> <daily-transaction-file> < <transaction-input>
```

Commands are read from standard input, one per line, until the end of input. The user
accounts file is read at each login, and the games and collections files once the
username is accepted. The Daily Transaction File is written at each logout. The order of
the arguments is our own choice and doesn't come from the handout.

Example using a Phase 1 test:

```sh
build/games-distribution inputs/TC01.user.txt inputs/TC01.game.txt inputs/TC01.collection.txt \
    build/TC01.atf.txt < inputs/TC01.inp.txt
diff --strip-trailing-cr build/TC01.atf.txt expected/TC01.exptf.txt
```

In PowerShell, pipe the input instead: `Get-Content inputs\TC01.inp.txt | build\games-distribution.exe ...`
