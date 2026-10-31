# Phase 3 change inventory

Branch: `feature/phase3-frontend-testing`. Main is unchanged. Changes are prepared
for review locally; no remote push, merge or Canvas submission has been performed.

## Modified files

- `.gitignore`
- `README.md`
- `include/FileManager.h`
- `include/GameManager.h`
- `include/Money.h`
- `include/TransactionProcessor.h`
- `include/UserManager.h`
- `src/FileManager.cpp`
- `src/GameManager.cpp`
- `src/TransactionProcessor.cpp`
- `src/UserManager.cpp`
- `src/main.cpp`

## New implementation, testing and documentation files

- `.gitattributes`
- `docs/AI_USAGE_LOG.md`
- `docs/Phase3_Execution_Guide.md`
- `docs/Phase3_Failure_Log.md`
- `docs/Phase3_Format_Decisions.md`
- `docs/Phase3_Test_Report.md`
- `include/RecordFormat.h`
- `scripts/check_validator.py`
- `scripts/phase3_tests.py`
- `scripts/prepare_submission.py`
- `scripts/render_report.py`
- `scripts/run_tests.sh`
- `scripts/supplemental_tests.py`
- `scripts/validate_tests.sh`
- `scripts/write_phase3_report.py`
- `tests/README.md`
- `tests/terminal_assertions.json`
- `docs/Phase3_Change_Inventory.md` (this inventory)
- `docs/Phase3_File_Manifest.txt` (complete created-file listing)

## Execution evidence

- `outputs/runs/iteration1-baseline/`: 30/46 PASS, 16 FAIL.
- `outputs/runs/iteration2-corrections/`: 46/46 PASS.
- `outputs/runs/iteration3-regression/`: 46/46 PASS, executed through Bash wrapper.
- `outputs/runs/iteration4-archive-smoke/`: extracted ZIP rebuilt, 46/46 PASS without Git metadata.
- `outputs/supplemental/iteration1-baseline/`: 7/21 PASS, 14 FAIL.
- `outputs/supplemental/iteration2-corrections/` and `iteration3-regression/`: 21/21 PASS each.
- `outputs/transactions/` and `outputs/terminal/`: current convenience copies by TC ID.
- `outputs/latest.txt`, `outputs/validator_checks.json`, `outputs/archive_smoke.json`.

Every complete 46-case run includes original fixture/source/script snapshots,
DTFs, stdout, stderr, exit statuses, copied oracles, SHA-256 manifest and validation
JSON. See the adjacent file manifest for every newly created path; per-run manifests
also enumerate and hash their evidence files.

## Local submission files (Git-ignored)

- `submission/CSCI3060U_Phase3_Review.zip`
- `submission/Phase3_Test_Report.pdf`
- `submission/SHA256SUMS.txt`
- `submission/README.txt`

The package remains a review package until the actual Phase 3 handout, team names,
TA format decisions, human oracle review and complete conversation export are
resolved. Build binaries, downloaded PDF libraries and rendered QA images are
kept in ignored `build/` and are not application/runtime dependencies.
