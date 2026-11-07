#!/usr/bin/env bash
# =============================================================================
# validate_tests.sh - compares the actual outputs of the last test run with the
# expected outputs and reports which tests passed or failed.
#
# CSCI 3060U Phase 3 - Qudsia Fawad, Diana Riyahi, Dhruv Thakar
#
# For every test TCxx, two comparisons are made:
#   outputs/TCxx.atf  vs  expected/TCxx.etf   (daily transaction file)
#   outputs/TCxx.out  vs  expected/TCxx.out   (what the user sees on the terminal)
# A test passes only if both files match exactly. Differences are printed so the
# failure can be recorded in the failure log (docs/Phase3_Failure_Log.md).
#
# Every run appends a dated summary to outputs/test_history.log, so the results
# of each test-suite execution are kept.
#
# Usage: bash scripts/run_tests.sh        (run the tests first)
#        bash scripts/validate_tests.sh
# Exit status: 0 if every test passed, 1 otherwise.
# =============================================================================
set -u

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root" || exit 1

pass_count=0
fail_count=0
failed_tests=""

for input_file in inputs/TC*.txt; do
    test_name="$(basename "$input_file" .txt)"
    echo "checking outputs of test $test_name"
    test_passed=yes

    # Compare the daily transaction file. --strip-trailing-cr lets Windows
    # builds (which write CRLF line endings) be checked against the same files.
    if [ ! -f "outputs/$test_name.atf" ]; then
        echo "  FAIL: no daily transaction file was written (outputs/$test_name.atf)"
        test_passed=no
    elif ! diff --strip-trailing-cr "outputs/$test_name.atf" "expected/$test_name.etf" > /dev/null; then
        echo "  FAIL: daily transaction file differs (< actual, > expected):"
        diff --strip-trailing-cr "outputs/$test_name.atf" "expected/$test_name.etf" | sed 's/^/    /'
        test_passed=no
    fi

    # Compare the terminal output.
    if ! diff --strip-trailing-cr "outputs/$test_name.out" "expected/$test_name.out" > /dev/null; then
        echo "  FAIL: terminal output differs (< actual, > expected):"
        diff --strip-trailing-cr "outputs/$test_name.out" "expected/$test_name.out" | sed 's/^/    /'
        test_passed=no
    fi

    if [ "$test_passed" = yes ]; then
        pass_count=$((pass_count + 1))
    else
        fail_count=$((fail_count + 1))
        failed_tests="$failed_tests $test_name"
    fi
done

summary="$pass_count passed, $fail_count failed"
echo
echo "Summary: $summary"
[ -n "$failed_tests" ] && echo "Failed tests:$failed_tests"

# Keep a record of this test-suite execution.
{
    echo "$(date '+%Y-%m-%d %H:%M:%S')  $summary${failed_tests:+  (failed:$failed_tests)}"
} >> outputs/test_history.log

[ "$fail_count" -eq 0 ]
