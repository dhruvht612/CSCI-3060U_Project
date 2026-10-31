# Phase 3 failure log

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
