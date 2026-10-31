#!/usr/bin/env python3
"""Build the human-readable report from preserved, real execution results."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ['iteration1-baseline', 'iteration2-corrections', 'iteration3-regression']


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def safe(text):
    return text.replace('|', '/').replace('\n', ' ')


def main():
    runs = [load(f'outputs/runs/{name}/validation.json') for name in RUNS]
    supplemental = [load(f'outputs/supplemental/{name}/results.json') for name in RUNS]
    rows = []
    roots = {
        '01': ('createUser always returned false', 'Implement type/name/uniqueness checks, zero-credit account insertion and 01 formatting'),
        '02': ('deleteUser and removeUser were stubs', 'Remove account and seller inventory; emit compatibility-profile 02'),
        '03': ('sell always returned false', 'Validate price/name/permission, reserve new names, emit 03'),
        '04': ('buy and game/collection loaders were stubs', 'Parse files, validate ownership/seller/funds, transfer credit and emit 04'),
        '05': ('refund and adjustCredit were stubs', 'Validate both accounts/balances, transfer cents atomically and emit 05'),
        '06': ('addCredit and adjustCredit were stubs; no session totals', 'Track per-account session additions, adjust balance and emit 06'),
    }
    for result in runs[0]['results']:
        if result['passed']: continue
        tid = result['id']
        purpose = (ROOT/f'expected/{tid}.expout.txt').read_text(encoding='utf-8').splitlines()[0]
        purpose = purpose.replace(tid, '', 1).strip(' -â€“')
        expected = (ROOT/f'expected/{tid}.exptf.txt').read_text().splitlines()
        code = expected[0][:2]
        root, fix = roots[code]
        count = len(expected)-1
        actual = f'Iteration 1: valid request(s) rejected; DTF contained only 00; {count} expected {code} record(s) absent. Terminal event check also failed.'
        retests = [next(r for r in run['results'] if r['id']==tid)['passed'] for run in runs[1:]]
        rows.append([tid,purpose,actual,root,fix,'Iterations 2/3: '+('/'.join('PASS' if p else 'FAIL' for p in retests))])
    supplemental_roots = {
        'S01': ('stoll threw on oversized input; main exited with stderr Error: stoll', 'Replace stoll/multiplication with bounded digit accumulation in Money.h'),
        'S03': (roots['04'][0], roots['04'][1]),
        'S04': (roots['05'][0], roots['05'][1]),
        'S05': (roots['02'][0], roots['02'][1]),
        'S06': (roots['03'][0], roots['03'][1]),
        'S07': (roots['06'][0], roots['06'][1]),
        'S08': (roots['01'][0], roots['01'][1]),
        'S12': ('loadGames ignored the games path and returned an empty vector', 'Open file and reject unavailable files before accepting login'),
        'S13': ('loadCollections ignored malformed input and returned an empty vector', 'Validate fixed-width collection records and END'),
        'S14': ('loadGames ignored the missing END marker', 'Require END; report missing terminator as recoverable login failure'),
        'S15': (roots['04'][0], 'Parse documented 49/42 widths as well as original fixture widths; implement buy'),
        'S17': (roots['06'][0], 'Implement addCredit; reset session counters and reload data at login'),
        'S18': (roots['06'][0]+'; '+roots['04'][0], 'Apply credit changes in memory; purchase against updated balance'),
        'S21': (roots['01'][0]+'; '+roots['03'][0], 'Support embedded spaces and exact maximum name widths'),
    }
    for result in supplemental[0]:
        if result['passed']: continue
        tid=result['id']; root,fix=supplemental_roots[tid]
        retests=[next(r for r in run if r['id']==tid)['passed'] for run in supplemental[1:]]
        rows.append([tid,result['purpose'],'Iteration 1: '+ '; '.join(result['failures']),root,fix,
                     'Iterations 2/3: '+('/'.join('PASS' if p else 'FAIL' for p in retests))])
    rows += [
        ['H01','Git Bash wrapper portability','First shell validation failed: WindowsApps/python3 Permission denied',
         'command -v found the unusable Windows Store python3 alias','Probe Python version/execution before selecting python3; otherwise use python',
         'Corrected wrapper validation PASS; full iteration 3 shell run 46/46'],
        ['E01','Baseline launch investigation','Cold first launch delayed output; no test timeout or failing process status was ultimately recorded',
         'Environment delay; no application root cause established','Waited for actual process completion; did not invent a crash or rerun over evidence',
         'All 46 baseline statuses recorded as zero'],
        ['E02','One-off Bash stdin probe','PowerShell-to-Bash probe delivered loginnadminnlogoutn as one command; program rejected it',
         'Probe quoting did not preserve newline escapes','Use fixture-file redirection / Python subprocess input for real runs',
         'Actual input-file runs pass; probe is not counted as an acceptance test'],
        ['E03','PDF dependency installation','Sandboxed pip install made no progress and was interrupted',
         'Environment/access issue; no application defect','Approved install into ignored build/report-deps',
         'ReportLab/pypdf installation succeeded'],
        ['E04','PDF authoring dependencies','First authoring attempt failed with ModuleNotFoundError: reportlab.lib; repair install reported an access-denied cleanup error',
         'Local dependency availability/permissions; the exact first-import cause was not established',
         'Verified module import after installation; retried PDF authoring without changing application code',
         'PDF generated and extracted text verified'],
        ['E05','PDF visual-review tooling','MiKTeX renderers produced no pages and were interrupted; early contact-sheet attempt had no images; sandbox could not read PDFium package',
         'Renderer/environment access and premature contact-sheet creation',
         'Use PDFium with approved access; require rendered pages before making contact sheet; keep failure entries together',
         'All report pages rendered and visually inspected'],
    ]
    table='| Test ID | Test Purpose | Actual Failure | Root Cause | Code/Test Fix | Retest Result |\n|---|---|---|---|---|---|\n'
    table+=''.join('| '+' | '.join(safe(x) for x in row)+' |\n' for row in rows)
    failure_log='''# Phase 3 failure log

Historical failures are retained after correction. Original test fixtures were
not edited. Iteration 1 has 16 original acceptance failures and 14 supplemental
failures; iterations 2 and 3 have none. H01 is a harness defect; E01-E05 record
environment/probe issues separately and do not inflate acceptance-test counts.
The 11 deliberately corrupted temporary runs in validator checks are expected
negative controls, not application regressions.

Evidence: `outputs/runs/<iteration>/validation.json`, per-test stdout/stderr/DTF
and status files; `outputs/supplemental/<iteration>/results.json` and case folders.

'''+table+'''
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
'''
    (ROOT/'docs/Phase3_Failure_Log.md').write_text(failure_log,encoding='utf-8')
    summary='| Execution | UTC start | Original tests | Supplemental |\n|---|---|---|---|\n'
    for name,run,supp in zip(RUNS,runs,supplemental):
        timestamp=load(f'outputs/runs/{name}/manifest.json')['utc']
        summary+=f'| {name} | {timestamp} | {run["passed"]}/46 PASS; {run["failed"]} FAIL | {sum(r["passed"] for r in supp)}/21 PASS |\n'
    archive = ROOT/'outputs/runs/iteration4-archive-smoke/validation.json'
    if archive.exists():
        result=json.loads(archive.read_text())
        stamp=load('outputs/runs/iteration4-archive-smoke/manifest.json')['utc']
        summary+=f'| iteration4-archive-smoke | {stamp} | {result["passed"]}/46 PASS; {result["failed"]} FAIL | Not rerun (application source unchanged) |\n'
    detail='| Test | Baseline | Corrections | Regression |\n|---|---|---|---|\n'
    for cases in zip(*(run['results'] for run in runs)):
        detail+='| '+cases[0]['id']+' | '+' | '.join('PASS' if r['passed'] else 'FAIL' for r in cases)+' |\n'
    report='''# Phase 3 - Front End Requirements Testing

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

'''+summary+'''
All original test processes exited zero with empty stderr in all three executions.
The baseline's 16 failures were content/behavior failures, not crashes. The separate
S01 baseline test did exit 1 with Error: stoll and no DTF, failing graceful recovery.
The baseline's negative-case passes often reflected stubs rejecting everything.

'''+detail+'''
## 9. Complete failure log

'''+failure_log.split('\n',1)[1]+'''
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
build/games-distribution inputs/TC01.user.txt inputs/TC01.game.txt \\
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
'''
    (ROOT/'docs/Phase3_Test_Report.md').write_text(report,encoding='utf-8')
    print(f'Wrote report and failure log: {len(rows)} historical entries')


if __name__ == '__main__':
    main()
