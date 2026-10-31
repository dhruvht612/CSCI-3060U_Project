# Phase 3 - Front End Requirements Testing

CSCI 3060U - Games Distribution System - October 31, 2026

Repository: https://github.com/dhruvht612/CSCI-3060U_Project

Branch: feature/phase3-frontend-testing. Base commit:
5c4ab596aaba6fde08fa2b62338cce8768fc830b.

Deadline supplied by the user: November 6, 2026, 8:00 PM (America/Toronto).
Team/member names: pending user-provided metadata before hand-in.

**Review status:** implementation and executable test evidence prepared. Original
fixture profile passes; official format approval and assignment-specific review
are still pending. The Phase 3 handout and complete AI conversation export have
not been supplied. This report does not claim those requirements are complete.

## 1. Introduction and project overview

The product is a C++17 console Front End for a Games Distribution System. It reads
current users, available games and game collections, validates one transaction at
a time, and writes a Daily Transaction File on logout. The later Python Back End
is outside this phase and is not implemented. Original source structure, four
positional file arguments, stdin/stdout interaction and all 46 Phase 1 cases remain.

## 2. Phase 3 objectives

Complete the six transaction stubs and supporting managers/loaders; test the
Front End against the supplied requirements; automate execution and accurate
verification; preserve initial failures; correct defects and demonstrate regression
results; prepare reproducible scripts, a detailed failure report and review package.

Sources inspected: README, all source/header files, both Phase 2 Markdown design
documents, Phase 1 plan and cases, Project_Docs/README.txt, the original course
project requirements, and every input/expected fixture. Duplicate fixture contents
were inspected as groups. The Phase 3 assignment document was not available; the
user's checklist supplies phase-specific deliverable instructions pending that review.

## 3. Existing Front End architecture

The dependency direction remains FrontEnd -> TransactionProcessor -> FileManager /
UserManager / GameManager. FrontEnd owns prompting and command dispatch;
TransactionProcessor validates operations and owns session state and ordered records;
FileManager owns text-file parsing/writing; managers own accounts, balances,
listings and collections. User/Game/CollectionEntry remain plain data records.
Money parsing and record formatting are small header helpers, not a new architecture.

State is in memory only. Accepted create/delete/buy/refund/addcredit operations
affect subsequent commands. Listings created during a session reserve names but
are not purchasable in that session. Login reloads source data; logout retains the
existing replace-per-session file behavior. No master files are rewritten.

## 4. Testing methodology

Before changing application code, compile the existing source and execute all 46
tests with independently authored terminal assertions and unchanged expected DTFs.
Save actual stdout, stderr, exit status and DTF for every case. Add supplemental
black-box scenarios for uncovered state and robustness requirements, execute them
against the original binary, then implement corrections. Rebuild and rerun both
suites. Finally rebuild again and run the complete original suite through Bash
wrappers, run supplemental checks, and verify saved evidence and validator behavior.

Observed platform: Windows, MSYS2 GCC 13.2.0, C++17, Python 3.14.3 and Git Bash.
The application build uses -Wall -Wextra and completed without compiler warnings.
Linux/macOS instructions are provided but no native run on those systems is claimed.

## 5. Acceptance test organization

TC01-TC46 each have .inp.txt, .user.txt, .game.txt and .collection.txt under inputs/,
and .exptf.txt plus behavioral .expout.txt under expected/. All 276 original files
are unchanged. Coverage includes sessions, authorization, all six transactions,
name/price/credit boundaries, invalid input and transaction formatting. Original
TC25 cannot isolate new-game restrictions; TC13 has no target inventory. S06 and
S05 cover those gaps without overwriting original evidence. Supplemental tests are
reported separately and never counted as additional original acceptance cases.

## 6. Automated execution scripts

scripts/run_tests.sh selects a working Python interpreter and invokes the standard
library harness. The harness discovers exactly 46 IDs, checks fixtures, gives each
test its own output paths, captures stdout/stderr/status, enforces a timeout and
continues after individual failures. Each run receives a new directory; existing
labels fail instead of overwriting history. Source/fixture/oracle snapshots and
SHA-256 manifests identify what was run. scripts/validate_tests.sh independently
checks a saved run. scripts/supplemental_tests.py executes the 21 extra scenarios.

## 7. Output validation methodology

DTFs are compared exactly after CRLF-to-LF normalization only. Checks include code,
schema, ordering, field width, spaces/padding, exact monetary values, final newline
and the single final bare 00 required by the original fixtures. Invalid operations
must not add records. Every original case must exit zero with empty stderr.

The original .expout.txt descriptions are preserved, not compared to terminal
bytes. tests/terminal_assertions.json expresses their acceptance/rejection sequence
as event patterns. It was authored before baseline execution. The validator requires
an exact sequence/count of events and prompt presence, and independently checks
transaction records. No actual-output transcript was copied into an expected file.
Team/TA review of the mapping and prompt quality remains pending; generic errors
do not prove the internal rejection reason. Supplemental list and follow-up
transactions check state effects absent from the original streams.

The validator was tested with 11 deliberate temporary corruptions: padding, code,
money, ordering, end record, newline, exit status, stderr, missing event, extra
success and missing file. All were detected. Evidence hashes were disabled only
in those disposable copies so semantic verification had to detect each mutation.

The format profile remains provisional: original fixtures use 25/15-character game
and user fields, blank delete metadata, addcredit deltas and bare 00. Input loaders
also accept the handout's 26-character padded game field. Conflicting handout
templates are not declared resolved by these passing results. See the format
decisions document for a complete table and TA questions.

## 8. Test execution results

| Execution | UTC start | Original tests | Supplemental |
|---|---|---|---|
| iteration1-baseline | 2026-10-31T19:52:34.738815+00:00 | 30/46 PASS; 16 FAIL | 7/21 PASS |
| iteration2-corrections | 2026-10-31T19:56:13.832098+00:00 | 46/46 PASS; 0 FAIL | 21/21 PASS |
| iteration3-regression | 2026-10-31T19:59:39.697926+00:00 | 46/46 PASS; 0 FAIL | 21/21 PASS |
| iteration4-archive-smoke | 2026-10-31T21:56:10.956911+00:00 | 46/46 PASS; 0 FAIL | Not rerun (application source unchanged) |

All original test processes exited zero with empty stderr in all three executions.
The baseline's 16 failures were content/behavior failures, not crashes. The separate
S01 baseline test did exit 1 with Error: stoll and no DTF, failing graceful recovery.
The baseline's negative-case passes often reflected stubs rejecting everything.

| Test | Baseline | Corrections | Regression |
|---|---|---|---|
| TC01 | PASS | PASS | PASS |
| TC02 | PASS | PASS | PASS |
| TC03 | PASS | PASS | PASS |
| TC04 | PASS | PASS | PASS |
| TC05 | PASS | PASS | PASS |
| TC06 | PASS | PASS | PASS |
| TC07 | PASS | PASS | PASS |
| TC08 | FAIL | PASS | PASS |
| TC09 | PASS | PASS | PASS |
| TC10 | PASS | PASS | PASS |
| TC11 | PASS | PASS | PASS |
| TC12 | FAIL | PASS | PASS |
| TC13 | FAIL | PASS | PASS |
| TC14 | PASS | PASS | PASS |
| TC15 | PASS | PASS | PASS |
| TC16 | PASS | PASS | PASS |
| TC17 | FAIL | PASS | PASS |
| TC18 | PASS | PASS | PASS |
| TC19 | FAIL | PASS | PASS |
| TC20 | PASS | PASS | PASS |
| TC21 | FAIL | PASS | PASS |
| TC22 | PASS | PASS | PASS |
| TC23 | PASS | PASS | PASS |
| TC24 | PASS | PASS | PASS |
| TC25 | FAIL | PASS | PASS |
| TC26 | FAIL | PASS | PASS |
| TC27 | PASS | PASS | PASS |
| TC28 | PASS | PASS | PASS |
| TC29 | PASS | PASS | PASS |
| TC30 | FAIL | PASS | PASS |
| TC31 | PASS | PASS | PASS |
| TC32 | FAIL | PASS | PASS |
| TC33 | PASS | PASS | PASS |
| TC34 | PASS | PASS | PASS |
| TC35 | PASS | PASS | PASS |
| TC36 | FAIL | PASS | PASS |
| TC37 | FAIL | PASS | PASS |
| TC38 | PASS | PASS | PASS |
| TC39 | FAIL | PASS | PASS |
| TC40 | PASS | PASS | PASS |
| TC41 | FAIL | PASS | PASS |
| TC42 | FAIL | PASS | PASS |
| TC43 | PASS | PASS | PASS |
| TC44 | PASS | PASS | PASS |
| TC45 | PASS | PASS | PASS |
| TC46 | FAIL | PASS | PASS |

## 9. Complete failure log


Historical failures are retained after correction. Original test fixtures were
not edited. Iteration 1 has 16 original acceptance failures and 14 supplemental
failures; iterations 2 and 3 have none. H01 is a harness defect; E01-E05 record
environment/probe issues separately and do not inflate acceptance-test counts.
The 11 deliberately corrupted temporary runs in validator checks are expected
negative controls, not application regressions.

Evidence: `outputs/runs/<iteration>/validation.json`, per-test stdout/stderr/DTF
and status files; `outputs/supplemental/<iteration>/results.json` and case folders.

| Test ID | Test Purpose | Actual Failure | Root Cause | Code/Test Fix | Retest Result |
|---|---|---|---|---|---|
| TC08 | – Valid Create User | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 01 record(s) absent. Terminal event check also failed. | createUser always returned false | Implement type/name/uniqueness checks, zero-credit account insertion and 01 formatting | Iterations 2/3: PASS/PASS |
| TC12 | – Username Exactly 15 Characters | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 01 record(s) absent. Terminal event check also failed. | createUser always returned false | Implement type/name/uniqueness checks, zero-credit account insertion and 01 formatting | Iterations 2/3: PASS/PASS |
| TC13 | – Valid Delete User | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 02 record(s) absent. Terminal event check also failed. | deleteUser and removeUser were stubs | Remove account and seller inventory; emit compatibility-profile 02 | Iterations 2/3: PASS/PASS |
| TC17 | – Valid Sell | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 03 record(s) absent. Terminal event check also failed. | sell always returned false | Validate price/name/permission, reserve new names, emit 03 | Iterations 2/3: PASS/PASS |
| TC19 | – Maximum Game Price | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 03 record(s) absent. Terminal event check also failed. | sell always returned false | Validate price/name/permission, reserve new names, emit 03 | Iterations 2/3: PASS/PASS |
| TC21 | – Game Name Exactly 25 Characters | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 03 record(s) absent. Terminal event check also failed. | sell always returned false | Validate price/name/permission, reserve new names, emit 03 | Iterations 2/3: PASS/PASS |
| TC25 | – Transaction on Newly Listed Game | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 03 record(s) absent. Terminal event check also failed. | sell always returned false | Validate price/name/permission, reserve new names, emit 03 | Iterations 2/3: PASS/PASS |
| TC26 | – Valid Buy | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 04 record(s) absent. Terminal event check also failed. | buy and game/collection loaders were stubs | Parse files, validate ownership/seller/funds, transfer credit and emit 04 | Iterations 2/3: PASS/PASS |
| TC30 | – Exact Credit Purchase | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 04 record(s) absent. Terminal event check also failed. | buy and game/collection loaders were stubs | Parse files, validate ownership/seller/funds, transfer credit and emit 04 | Iterations 2/3: PASS/PASS |
| TC32 | – Valid Refund | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 05 record(s) absent. Terminal event check also failed. | refund and adjustCredit were stubs | Validate both accounts/balances, transfer cents atomically and emit 05 | Iterations 2/3: PASS/PASS |
| TC36 | – Valid Add Credit - Standard User | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 06 record(s) absent. Terminal event check also failed. | addCredit and adjustCredit were stubs; no session totals | Track per-account session additions, adjust balance and emit 06 | Iterations 2/3: PASS/PASS |
| TC37 | – Valid Add Credit - Admin | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 06 record(s) absent. Terminal event check also failed. | addCredit and adjustCredit were stubs; no session totals | Track per-account session additions, adjust balance and emit 06 | Iterations 2/3: PASS/PASS |
| TC39 | – Add Exactly $1000 | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 06 record(s) absent. Terminal event check also failed. | addCredit and adjustCredit were stubs; no session totals | Track per-account session additions, adjust balance and emit 06 | Iterations 2/3: PASS/PASS |
| TC41 | – Multiple Credit Additions to $1000 | Iteration 1: valid request(s) rejected; DTF contained only 00; 2 expected 06 record(s) absent. Terminal event check also failed. | addCredit and adjustCredit were stubs; no session totals | Track per-account session additions, adjust balance and emit 06 | Iterations 2/3: PASS/PASS |
| TC42 | – Multiple Credit Additions Over $1000 | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 06 record(s) absent. Terminal event check also failed. | addCredit and adjustCredit were stubs; no session totals | Track per-account session additions, adjust balance and emit 06 | Iterations 2/3: PASS/PASS |
| TC46 | – Daily Transaction File Formatting | Iteration 1: valid request(s) rejected; DTF contained only 00; 1 expected 01 record(s) absent. Terminal event check also failed. | createUser always returned false | Implement type/name/uniqueness checks, zero-credit account insertion and 01 formatting | Iterations 2/3: PASS/PASS |
| S01 | Huge money must reject and continue to logout | Iteration 1: nonzero exit or stderr; DTF mismatch; unexpected error count; did not recover to logout | stoll threw on oversized input; main exited with stderr Error: stoll | Replace stoll/multiplication with bounded digit accumulation in Money.h | Iterations 2/3: PASS/PASS |
| S03 | Duplicate purchase and buyer/seller balance changes | Iteration 1: DTF mismatch; unexpected error count; wrong/missing balance: admin=4985.00; wrong/missing balance: seller1=515.00 | buy and game/collection loaders were stubs | Parse files, validate ownership/seller/funds, transfer credit and emit 04 | Iterations 2/3: PASS/PASS |
| S04 | Refund transfers credit to buyer and from seller | Iteration 1: DTF mismatch; unexpected error count; wrong/missing balance: buyer1=510.00; wrong/missing balance: seller1=490.00 | refund and adjustCredit were stubs | Validate both accounts/balances, transfer cents atomically and emit 05 | Iterations 2/3: PASS/PASS |
| S05 | Deleted seller inventory and account cannot be used | Iteration 1: DTF mismatch; unexpected error count; deleted account still listed | deleteUser and removeUser were stubs | Remove account and seller inventory; emit compatibility-profile 02 | Iterations 2/3: PASS/PASS |
| S06 | New listing unavailable to a buy-capable account; duplicate listing rejected | Iteration 1: DTF mismatch; unexpected error count | sell always returned false | Validate price/name/permission, reserve new names, emit 03 | Iterations 2/3: PASS/PASS |
| S07 | Per-account credit limits independent within session | Iteration 1: DTF mismatch; unexpected error count; wrong/missing balance: buyer1=1500.00; wrong/missing balance: seller1=1500.00 | addCredit and adjustCredit were stubs; no session totals | Track per-account session additions, adjust balance and emit 06 | Iterations 2/3: PASS/PASS |
| S08 | New accounts, duplicate names, all valid type words | Iteration 1: DTF mismatch; unexpected error count; wrong/missing balance: newadmin=0.00; wrong/missing balance: newbuyer=0.00; wrong/missing balance: newseller=0.00 | createUser always returned false | Implement type/name/uniqueness checks, zero-credit account insertion and 01 formatting | Iterations 2/3: PASS/PASS |
| S12 | Missing games file rejects login politely | Iteration 1: DTF mismatch; unexpected error count | loadGames ignored the games path and returned an empty vector | Open file and reject unavailable files before accepting login | Iterations 2/3: PASS/PASS |
| S13 | Malformed collection file rejects login politely | Iteration 1: DTF mismatch; unexpected error count | loadCollections ignored malformed input and returned an empty vector | Validate fixed-width collection records and END | Iterations 2/3: PASS/PASS |
| S14 | Missing END in games file rejects login | Iteration 1: DTF mismatch; unexpected error count | loadGames ignored the missing END marker | Require END; report missing terminator as recoverable login failure | Iterations 2/3: PASS/PASS |
| S15 | 49/42 character handout input compatibility | Iteration 1: DTF mismatch; unexpected error count | buy and game/collection loaders were stubs | Parse documented 49/42 widths as well as original fixture widths; implement buy | Iterations 2/3: PASS/PASS |
| S17 | Credit limit resets and input files reload at next login | Iteration 1: DTF mismatch; unexpected error count | addCredit and adjustCredit were stubs; no session totals | Implement addCredit; reset session counters and reload data at login | Iterations 2/3: PASS/PASS |
| S18 | Buy uses credit added earlier in same session | Iteration 1: DTF mismatch; unexpected error count | addCredit and adjustCredit were stubs; no session totals; buy and game/collection loaders were stubs | Apply credit changes in memory; purchase against updated balance | Iterations 2/3: PASS/PASS |
| S21 | Printable names with embedded spaces and maximum field lengths | Iteration 1: DTF mismatch; unexpected error count | createUser always returned false; sell always returned false | Support embedded spaces and exact maximum name widths | Iterations 2/3: PASS/PASS |
| H01 | Git Bash wrapper portability | First shell validation failed: WindowsApps/python3 Permission denied | command -v found the unusable Windows Store python3 alias | Probe Python version/execution before selecting python3; otherwise use python | Corrected wrapper validation PASS; full iteration 3 shell run 46/46 |
| E01 | Baseline launch investigation | Cold first launch delayed output; no test timeout or failing process status was ultimately recorded | Environment delay; no application root cause established | Waited for actual process completion; did not invent a crash or rerun over evidence | All 46 baseline statuses recorded as zero |
| E02 | One-off Bash stdin probe | PowerShell-to-Bash probe delivered loginnadminnlogoutn as one command; program rejected it | Probe quoting did not preserve newline escapes | Use fixture-file redirection / Python subprocess input for real runs | Actual input-file runs pass; probe is not counted as an acceptance test |
| E03 | PDF dependency installation | Sandboxed pip install made no progress and was interrupted | Environment/access issue; no application defect | Approved install into ignored build/report-deps | ReportLab/pypdf installation succeeded |
| E04 | PDF authoring dependencies | First authoring attempt failed with ModuleNotFoundError: reportlab.lib; repair install reported an access-denied cleanup error | Local dependency availability/permissions; the exact first-import cause was not established | Verified module import after installation; retried PDF authoring without changing application code | PDF generated and extracted text verified |
| E05 | PDF visual-review tooling | MiKTeX renderers produced no pages and were interrupted; early contact-sheet attempt had no images; sandbox could not read PDFium package | Renderer/environment access and premature contact-sheet creation | Use PDFium with approved access; require rendered pages before making contact sheet; keep failure entries together | All report pages rendered and visually inspected |

## Findings not misreported as observed failures

- The original multiplication in Money.h could overflow signed long long after
  stoll succeeded. S02 passed even in the baseline because the transaction stub
  rejected its result; no sanitizer failure is claimed. The bound-checked parser
  removes this code-inspection defect and S01 demonstrates the real exit bug.
- TC25 and TC13 have coverage gaps documented in Phase3_Format_Decisions.md.
  Preserve them and use S06/S05; do not rewrite the original expected results.
- Generic rejection messages alone cannot establish that a specific internal
  validation branch ran. Baseline negative-case passes are not proof of correctness.
- Format disagreements remain pending TA confirmation, not silently fixed tests.
- Archive-readiness review identified that requiring git rev-parse would abort
  outside a Git checkout. Git metadata is now optional; a fresh archive build/run
  with Git metadata deliberately unavailable verifies all 46 cases. This was a
  code-inspection finding, not an invented failed acceptance-suite execution.

## 10. Defects and corrections

createUser now validates names/types and inserts a unique zero-credit account.
deleteUser removes an eligible account and cancels its listings. sell validates
name/price/permission and reserves the new name. buy validates existence, seller,
ownership and balances, transfers cents, and updates the collection. refund checks
both accounts and transfers cents. addCredit tracks a separate per-session total
for each account and enforces the $1000 cap. All six emit ordered records 01-06.

FileManager now parses games and collections with width/separator/field/END checks.
UserManager supports insertion/removal and overflow-safe credit adjustment.
GameManager updates ownership and cancels seller listings. Money parsing rejects
oversized values without exceptions or signed-overflow arithmetic. Permission
checks also exist at the processor boundary. Source/fixture evidence was preserved
before these edits. No original acceptance-test correction was necessary.

## 11. Regression testing

Every one of the 30 originally passing cases still passes, and all 16 original
failures now pass. Supplemental results improved from 7/21 to 21/21. The final
Bash-driven run confirms the wrapper fix and complete suite execution. Revalidating
the saved run checks evidence integrity as well as results. No regression is
observed within this coverage. This is not proof of every possible input or of
format interpretations awaiting TA confirmation.

## 12. Final results and submission contents

46/46 original acceptance cases and 21/21 supplemental cases pass in both correction
and final regression runs. All 11 validator mutation checks pass. The review ZIP
contains complete C++ source/headers, original fixtures and requirements, scripts,
semantic assertions, Markdown reports, PDF report, AI disclosure instructions and
preserved execution evidence. Build products and Python dependency downloads are
excluded. No Canvas submission or merge into main is performed.

Outstanding before final hand-in: obtain/review the actual Phase 3 assignment,
resolve TA format questions, add team/member names, review the terminal oracle,
and export the complete AI prompt-and-response history. AI_USAGE_LOG.md is a truthful
summary and export checklist, not a fabricated replacement for missing history.

## 13. Instructions for the TA

From the repository root, run the following in Bash. Python 3.9+ and a C++17
compiler are needed; the test harness has no third-party Python dependencies.

```bash
mkdir -p build
g++ -std=c++17 -Wall -Wextra -Iinclude src/*.cpp -o build/games-distribution
bash scripts/run_tests.sh
bash scripts/validate_tests.sh
python3 scripts/supplemental_tests.py --label ta-review
python3 scripts/check_validator.py
```

For the requested CLI example:

```bash
build/games-distribution inputs/TC01.user.txt inputs/TC01.game.txt \
  inputs/TC01.collection.txt outputs/TC01.atf.txt < inputs/TC01.inp.txt
```

Use a new label for every named test run. Consult Phase3_Execution_Guide.md for
PowerShell equivalents, artifact locations, baseline reconstruction and packaging.
Inspect the failure log and saved stdout/status/DTFs to verify the improvement.

## 14. Conclusion

The completed Front End preserves the existing design and interface, implements
the required transactions and passes the supplied fixture profile with reproducible
evidence. Baseline failures remain available for assessment. Official specification
and submission review items are explicitly distinguished from executable test success.
