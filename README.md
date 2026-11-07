# CSCI-3060U_Project

Games Distribution System: a console Front End written in C++ for CSCI 3060U (Fall 2026).

Group: Qudsia Fawad, Diana Riyahi, Dhruv Thakar

## Status

Phase 3 (Front End requirements testing) is complete. All transactions are implemented,
including the client's SEARCH update. All 54 tests and 21 supplemental checks pass.
See the [Phase 3 report](docs/Phase3_Report.md) (also as `.docx`/`.pdf` in `docs/`),
which contains the run instructions and the full [failure log](docs/Phase3_Failure_Log.md).

## Layout

```text
src/, include/  Front End source code and headers
data/           shared input files used by every test
inputs/         one transaction input file per test (TC01.txt ... TC54.txt)
expected/       expected terminal output (.out) and daily transaction file (.etf) per test
outputs/        actual outputs from the latest test run, plus test_history.log
scripts/        run_tests.sh, validate_tests.sh, supplemental_tests.py, package_submission.sh
tests/          TEST_CATALOG.md: what each test is for
docs/           Phase 3 report and failure log, Phase 2 design documents
archive/        saved outputs of Phase 3 test iterations 1-6 (earlier test harness)
Project_Docs/   project handout and phase assignments
```

## Build and run

Requires a C++17 compiler and Bash (Linux, macOS, or Git Bash on Windows).

```sh
mkdir -p build
g++ -std=c++17 -Wall -Wextra -Iinclude src/*.cpp -o build/games-distribution
build/games-distribution data/currentaccounts.txt data/availablegames.txt \
    data/gamescollection.txt transout.atf
```

Arguments: Current User Accounts File, Available Games File, Games Collection File, and the
daily transaction file to write at each logout. Commands are read from standard input; to
replay a saved test, redirect it in: `... outputs/TC01.atf < inputs/TC01.txt`.

## Test

```sh
bash scripts/run_tests.sh        # compile and run every test into outputs/
bash scripts/validate_tests.sh   # diff outputs/ against expected/, print PASS/FAIL
python3 scripts/supplemental_tests.py --label my-run   # optional extra checks
```

## Submission zip

```sh
bash scripts/package_submission.sh   # creates submission/CSCI3060U_Phase3.zip
```
