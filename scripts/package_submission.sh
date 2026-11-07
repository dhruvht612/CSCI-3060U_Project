#!/usr/bin/env bash
# =============================================================================
# package_submission.sh - builds the Canvas zip: the Front End code, the tests
# and the scripts that run them.
#
# CSCI 3060U Phase 3 - Qudsia Fawad, Diana Riyahi, Dhruv Thakar
#
# Usage: bash scripts/package_submission.sh
# Output: submission/CSCI3060U_Phase3.zip  (the submission/ folder is git-ignored)
# The report (docs/Phase3_Report.pdf or .docx) is submitted separately on Canvas.
# =============================================================================
set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

# Make sure the code we package passes every test before zipping it.
bash scripts/run_tests.sh > /dev/null
if ! bash scripts/validate_tests.sh > /dev/null; then
    echo "Some tests fail - fix them before packaging (run scripts/validate_tests.sh for details)."
    exit 1
fi

mkdir -p submission
zip_file="submission/CSCI3060U_Phase3.zip"
rm -f "$zip_file"

# Source code, tests, scripts and the main documents.
zip -rq "$zip_file" README.md src include data inputs expected outputs tests \
    scripts/run_tests.sh scripts/validate_tests.sh scripts/supplemental_tests.py \
    scripts/package_submission.sh docs/Phase3_Report.md docs/Phase3_Failure_Log.md \
    -x 'outputs/supplemental/*'

echo "Created $zip_file"
