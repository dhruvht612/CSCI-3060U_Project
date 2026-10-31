# Phase 3 execution guide

Run from the repository root. Requirements: C++17 compiler, Bash, Python 3.9+
(standard library only for tests). Git is optional for the provenance manifest.
Python scripts are test/report tooling only; no Python Back End is implemented.

## Build and run

```bash
mkdir -p build
g++ -std=c++17 -Wall -Wextra -Iinclude src/*.cpp -o build/games-distribution
build/games-distribution inputs/TC01.user.txt inputs/TC01.game.txt \
  inputs/TC01.collection.txt outputs/TC01.atf.txt < inputs/TC01.inp.txt
```

The four arguments remain users, games, collections, output DTF. The program
reads commands from stdin and writes prompts/results to stdout; main-level fatal
errors go to stderr. Recoverable transaction/login/output-write rejections remain
on stdout and do not produce a nonzero exit status. Input files are never updated.

## Execute and validate all 46 cases

```bash
bash scripts/run_tests.sh
bash scripts/validate_tests.sh
# Optional named execution (each label must be new):
bash scripts/run_tests.sh --label my-regression
bash scripts/validate_tests.sh outputs/runs/my-regression
python3 scripts/supplemental_tests.py --label my-regression
python3 scripts/check_validator.py
```

Use `./scripts/run_tests.sh` and `./scripts/validate_tests.sh` after checkout with
executable modes preserved; if a ZIP extractor loses modes, use Bash explicitly
or `chmod +x scripts/*.sh`. An explicit binary can be passed with `--binary PATH`;
`--timeout SECONDS` defaults to 10 seconds per process. The runner verifies that
exactly TC01-TC46 and all six files per case exist. It records and continues past
nonzero exits, timeout/launch errors and assertion failures. Missing suite fixtures
are infrastructure errors, rather than fabricated individual test results.

Exit statuses: 0 = all checks pass; 1 = one or more test/validation failures;
2 = harness setup or usage error. Supplemental checks return 1 on any failure.
The baseline validator is expected to return 1 because its 16 failures are real.

## Windows / PowerShell

Use Git Bash or MSYS2 Bash, not the Windows WSL launcher unless WSL is configured.
The wrappers test whether `python3` is usable, falling back to `python`; a Windows
Store alias is not treated as a valid interpreter. Set `PYTHON` if needed.

```powershell
New-Item -ItemType Directory -Force build | Out-Null
g++ -std=c++17 -Wall -Wextra -Iinclude src/*.cpp -o build/games-distribution
python scripts/phase3_tests.py run
python scripts/phase3_tests.py validate
python scripts/supplemental_tests.py --label local-check
Get-Content inputs/TC01.inp.txt | build/games-distribution.exe `
  inputs/TC01.user.txt inputs/TC01.game.txt inputs/TC01.collection.txt outputs/TC01.atf.txt
```

For MinGW, put the matching compiler's `bin` directory on PATH so its runtime DLLs
can be found. The provided build command was exercised with MSYS2 GCC 13.2.0.

## Evidence and validation

Every execution has a new `outputs/runs/<label>/` directory containing:

- `transactions/TCxx.atf.txt` and byte-sensitive textual diffs.
- `terminal/TCxx.stdout.txt`, `TCxx.stderr.txt`, `TCxx.status.json`.
- `oracle/` copies of the original expected DTFs and terminal event assertions.
- `snapshot/` source, headers, scripts, original inputs and expected descriptions.
- `manifest.json` with UTC timestamp, platform, executable SHA-256, Git base and
  evidence hashes; `validation.json` with per-test failures and totals.

`outputs/terminal/` and `outputs/transactions/` are convenience copies;
`outputs/latest.txt` points to the latest full run. Historical run directories
are authoritative and are never reused. Supplemental evidence has its own
`outputs/supplemental/<label>/` tree, expected records and test-definition copy.
`outputs/validator_checks.json` records the validator mutation checks.

Validation checks exact DTF bytes after CRLF normalization, schema, code, field
width, padding, amount, record ordering, final newline and exactly one final 00.
It also checks exit status, stderr, prompt presence and ordered success/error
events. See `tests/README.md` for the semantic oracle and human review limits.
Run validation of historical evidence with that run's copied oracle. Hash checks
detect altered evidence; they are reproducibility checks, not digital signatures.

To rebuild the original baseline separately, compile
`outputs/runs/iteration1-baseline/snapshot/src/*.cpp` with its sibling `include/`
directory. Do not replace the current source or reuse an existing run label.

## TA and submission checklist

1. Read `Phase3_Test_Report.md`, `Phase3_Failure_Log.md` and format decisions.
2. Compile, run the 46-case suite, supplemental tests and validator checks above.
3. Review `tests/terminal_assertions.json` against every original `.expout.txt`;
   prompt readability and interpretation of prose remain human review tasks.
4. Resolve the recorded TA questions; check the missing Phase 3 handout and any
   client updates. Add team/member names to the report before hand-in.
5. Export the complete AI conversation using `AI_USAGE_LOG.md`. The disclosure
   summary is not a substitute for the complete history.
6. Rebuild the PDF and ZIP after adding the final metadata/history. The ZIP is a
   review package until those items are complete. Nothing is submitted to Canvas.

## Rebuild report and ZIP

PDF authoring only requires ReportLab and pypdf; neither is needed to build/test
the application. Install them in a virtual environment or an isolated build folder:

```bash
python3 -m pip install --target build/report-deps reportlab pypdf
python3 scripts/prepare_submission.py
```

The script packages source, fixtures, documents, tooling and preserved evidence,
excluding Git internals, binaries, dependency downloads and the ZIP itself. It
includes a SHA-256 manifest. PDF rendering for visual review uses Poppler:
`pdftoppm -scale-to 1200 -png submission/Phase3_Test_Report.pdf build/phase3-page`.


If Poppler is unavailable, install `pypdfium2` into `build/pdf-render` and run
`python scripts/render_report.py`. This optional authoring tool renders all pages
and a contact sheet; it is not needed to compile or test the Front End.
Git metadata is optional: archive runs record a null Git head and still capture
source/fixture and executable hashes. The extracted ZIP was rebuilt and all 46
cases were exercised with Git metadata unavailable; evidence is preserved under
`outputs/runs/iteration4-archive-smoke/` and `outputs/archive_smoke.json`.
