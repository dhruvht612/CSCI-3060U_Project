# CSCI-3060U_Project

Games Distribution System: a console front end written in C++ for CSCI 3060U (Fall 2026).

## Status

Phase 3 Front End implementation and requirements testing. All six transactions
are implemented within the existing C++ class architecture. The preserved baseline
passed 30/46 original acceptance tests; correction and regression runs pass 46/46,
plus 21 supplemental checks. No Python Back End is implemented.

See [the test report](docs/Phase3_Test_Report.md),
[failure log](docs/Phase3_Failure_Log.md),
[execution guide](docs/Phase3_Execution_Guide.md), and
[provisional format decisions](docs/Phase3_Format_Decisions.md).
Passing fixtures does not resolve the handout's conflicting formats. TA confirmation,
the missing Phase 3 assignment handout, team metadata and complete AI-history export
remain submission review items. The Phase 2 documents are retained as historical evidence.

## Layout

```text
include/        class declarations
src/            class implementations and main.cpp
docs/           design notes
scripts/        test execution, verification and submission tooling
tests/          terminal behavioral assertions and review notes
outputs/        preserved baseline, correction and regression evidence
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

## Test

```sh
bash scripts/run_tests.sh
bash scripts/validate_tests.sh
python3 scripts/supplemental_tests.py --label my-check
python3 scripts/check_validator.py
```

Requires Bash, Python 3.9+ (standard library), with optional Git metadata for execution provenance.
Use `python` instead of `python3` on Windows if needed. Each runner label must be
new: historical evidence is never overwritten. Original `inputs/` and `expected/`
files are unchanged. Behavioral `.expout.txt` descriptions are validated through
separately authored event assertions, not compared as literal console transcripts.

## Review package

`python scripts/prepare_submission.py` creates the PDF report, checksum manifest
and ZIP in `submission/` (ignored by Git). PDF authoring requires ReportLab and
pypdf as described in the execution guide. Nothing is uploaded to Canvas or merged
into main by these scripts. Export the complete conversation before final packaging;
see [AI disclosure instructions](docs/AI_USAGE_LOG.md).
