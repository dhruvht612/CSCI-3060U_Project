#!/usr/bin/env bash
# =============================================================================
# package_phase4.sh - builds the Phase 4 Canvas zip: the Back End's Python
# source code (.py files) plus the sample input files it can be run on.
#
# CSCI 3060U Phase 4 - Qudsia Fawad, Diana Riyahi, Dhruv Thakar
#
# Usage:  bash scripts/package_phase4.sh
# Output: submission/CSCI3060U_Phase4_BackEnd.zip  (submission/ is git-ignored)
# The design document (docs/Phase4_Design_Document.pdf or .docx) is submitted
# separately on Canvas, as the phase handout asks.
# =============================================================================
set -eu

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

mkdir -p submission
zip_file="submission/CSCI3060U_Phase4_BackEnd.zip"
rm -f "$zip_file"

zip -rq "$zip_file" backend/*.py backend/sample -x '*__pycache__*'

echo "Created $zip_file"
