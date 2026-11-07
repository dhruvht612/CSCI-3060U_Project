#!/usr/bin/env bash
# =============================================================================
# run_tests.sh - runs every Front End test and saves its actual outputs.
#
# CSCI 3060U Phase 3 - Qudsia Fawad, Diana Riyahi, Dhruv Thakar
#
# Test layout (one test = one transaction input file):
#   data/                   shared input files used by every test
#       currentaccounts.txt   Current User Accounts File
#       availablegames.txt    Available Games File
#       gamescollection.txt   Games Collection File
#   inputs/TCxx.txt         the commands typed into the Front End for test TCxx
#   expected/TCxx.out       what the user should see on the terminal
#   expected/TCxx.etf       the daily transaction file the test should produce
#   outputs/TCxx.out        actual terminal output        (written by this script)
#   outputs/TCxx.atf        actual daily transaction file (written by this script)
#
# Usage (from anywhere):   bash scripts/run_tests.sh
# Then check the results:  bash scripts/validate_tests.sh
# =============================================================================
set -u

# Work from the repository root, wherever the script was started from.
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root" || exit 1

program="build/games-distribution"
accounts_file="data/currentaccounts.txt"
games_file="data/availablegames.txt"
collection_file="data/gamescollection.txt"

# Step 1: compile the Front End so we always test the current source code.
echo "Compiling the Front End..."
mkdir -p build
if ! g++ -std=c++17 -Wall -Wextra -Iinclude src/*.cpp -o "$program"; then
    echo "Compilation failed - no tests were run."
    exit 1
fi

# Step 2: start with an empty outputs folder so old results can't be mistaken
# for new ones. (Saved evidence from earlier phases lives in archive/, not here.)
mkdir -p outputs
rm -f outputs/TC*.out outputs/TC*.atf

# Step 3: run the program once per input file.
#   - the transaction input file is fed in as standard input
#   - the terminal log (standard output and errors) goes to outputs/TCxx.out
#   - the program writes its daily transaction file to outputs/TCxx.atf
test_count=0
for input_file in inputs/TC*.txt; do
    test_name="$(basename "$input_file" .txt)"   # e.g. inputs/TC07.txt -> TC07
    echo "running test $test_name"
    "$program" "$accounts_file" "$games_file" "$collection_file" "outputs/$test_name.atf" \
        < "$input_file" > "outputs/$test_name.out" 2>&1
    test_count=$((test_count + 1))
done

echo "Ran $test_count tests. Actual outputs are in outputs/."
echo "Next: bash scripts/validate_tests.sh"
