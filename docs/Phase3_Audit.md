# Phase 3 audit — November 5, 2026

Audited commit: `94a37147bfaaabfe02ae2471f25d89daa7839210`.
Audit branch: `audit/phase3`, created from the current main/Phase 4 branch tip,
which includes the Phase 3 SEARCH update. The older Phase 3 feature branch does
not contain that update.

The current Front End passes a fresh build and the available acceptance and
supplemental suites. The submission is **not ready as currently packaged**:
the local ZIP contains older code, the packaging script omits the supplied
Phase 3 AI-history document, and the SEARCH run summaries lack their underlying
evidence. No application or test implementation was changed during this audit.

## Confirmed findings

### P1 — The existing submission ZIP omits the SEARCH update

`submission/CSCI3060U_Phase3_Review.zip` has 3,328 entries, but contains neither
`inputs/TC54.inp.txt` nor the iteration 6 manifest. Its copies of
`src/FrontEnd.cpp`, `src/TransactionProcessor.cpp`, and
`docs/Phase3_Test_Report.md` differ from the audited working files. Submitting
this ZIP would deliver older implementation and reporting despite the repository
claiming SEARCH support.

**Action:** regenerate the final PDF/ZIP after resolving the items below, then
inspect its contents and build/run the extracted package against all 54 cases.
The previous 46-case archive smoke test does not verify the updated release.

### P1 — Packaging excludes the Phase 3 AI-history document

`scripts/prepare_submission.py:138–141` selects certain directories and an
explicit root-file list that includes `Phase2_AI_use.docx`, but excludes
`Phase3_AI_Use_History_Diana.docx`. The Phase 3 document is tracked by Git and
present at the root, but absent from the existing ZIP. Simply regenerating with
the current script will still omit it.

**Action:** explicitly include the Phase 3 history, or place it in a packaged
directory and update the references. Verify that the provided history covers
all Phase 3 contributions and any subsequent submitted audit/fix work. This
audit establishes the packaging omission; it does not certify the document's
transcript completeness. The existing `docs/AI_USAGE_LOG.md` is untracked and
describes itself as a summary, not a complete transcript; it was preserved.

### P1 — SEARCH execution summaries have no supporting run artifacts

Each of `outputs/runs/iteration5-search-baseline/manifest.json` and
`outputs/runs/iteration6-search-corrections/manifest.json` names 618 evidence
files. **All 618 are missing in each run directory.** Only the manifest and
validation summary are tracked for each run. The iteration 6 supplemental
directory likewise contains a result summary without its case evidence.

Reproduction from the repository root:

```text
python scripts/phase3_tests.py validate outputs/runs/iteration6-search-corrections
```

It exits 2 because `oracle/terminal_assertions.json` is missing. The report's
SEARCH before/after results therefore cannot be independently revalidated from
these saved runs. A fresh passing run verifies current behavior but cannot
reconstruct the historical test-first evidence.

**Action:** recover and commit the original run folders if available. If they
cannot be recovered, disclose that limitation and preserve clearly labeled new
executions; do not present reconstructed results as the original observations.

### P2 — Validation wrongly applies today's test IDs to historical runs

`scripts/phase3_tests.py:80` calls `discover()` on the current `inputs/` directory
inside `validate()`. The current suite has 54 cases, while iterations 1–4 ran
46. The saved oracle is used for expected behavior, but not for selecting the
historical case IDs.

Reproduction:

```text
python scripts/phase3_tests.py validate outputs/runs/iteration3-regression
```

Observed result: **46/54 pass, 8 fail, 0 evidence-integrity errors**, exit 1.
All eight failures are missing TC47–TC54 status files, which were never part
of that run. `outputs/latest.txt` still points to iteration 3, so the documented
default validation command encounters the same issue before any new run.

**Action:** validate against a case list captured with the run, with a compatible
fallback based on the historical snapshot/oracle. Keep current-suite discovery
for new executions. Verify that iteration 3 validates as 46/46, the original
baseline still reports its genuine 16 failures, and a new 54-case run validates
as 54/54. Preserve the historical evidence while fixing the harness.

## Submission questions and documentation gaps

- The official Phase 3 assignment handout is absent from `Project_Docs`.
  `docs/Phase3_Test_Report.md:35–37` says it was reviewed, whereas the README,
  execution guide and format decisions still describe it as missing. This audit
  cannot settle that inconsistency or certify the exact Phase 3 rubric without
  the handout/client updates. It uses the available project requirements and
  Phase 1/3 documentation; the Phase 4 rubric is not applied to Phase 3.
- Team/member names remain placeholders in the report and PDF generator. The
  general project handout requires team and member names on each hand-in.
- Record-layout and SEARCH interpretation questions remain explicitly provisional
  in `docs/Phase3_Format_Decisions.md`. Passing the fixture profile does not
  establish TA acceptance of those choices. Preserve any actual clarification
  and apply it consistently to implementation, expectations and documentation.
- The terminal expectations are behavioral assertions derived from prose, not
  exact terminal transcripts. This is documented; team review of the mapping is
  still pending. Generic error messages cannot prove the intended rejection
  reason. TC13/TC25 coverage limitations are documented and supplemented by
  S05/S06, rather than concealed by editing the original cases.

## Verification and scope

Sources reviewed: the general project handout, README, Phase 3 report/failure
log/format decisions/execution guide, C++ sources and interfaces, test harness,
supplemental checks, validator checks, manifests and package selection logic.

Fresh checks ran in `build/phase3-audit/`, an isolated copy of the source,
headers, fixtures, scripts and terminal assertions. Historical outputs and the
repository's latest-run pointer were not overwritten. No Back End work was done.

Build: MSYS2 GCC 13.2.0, C++17, `-Wall -Wextra`, exit 0 with no diagnostics.
Tests: Python 3.14.3 on Windows.

```text
g++ -std=c++17 -Wall -Wextra -Iinclude src/FileManager.cpp src/FrontEnd.cpp src/GameManager.cpp src/TransactionProcessor.cpp src/UserManager.cpp src/main.cpp -o build/games-distribution.exe
python scripts/phase3_tests.py run --label audit-current
python scripts/supplemental_tests.py --label audit-current
python scripts/check_validator.py
bash scripts/validate_tests.sh outputs/runs/audit-current
```

The source folders and command paths above are relative to the isolated copy.
Fresh acceptance results: **54/54 pass**, with zero evidence-integrity errors.
Fresh supplemental results: **21/21 pass**. All **11/11 validator mutation
checks pass**, and Git Bash revalidation confirms **54/54 pass**. See the accompanying
`phase3_audit_evidence.json` for the recorded results and artifact inventory.
Full fresh run files remain locally under `build/phase3-audit/outputs/` and are
ignored by Git; the JSON is a summary, not a replacement for those raw files.

This is an audit, not a correctness guarantee or an estimated grade. It does not
verify Canvas submission, remote repository permissions, lab attendance, team
contributions, PDF visual layout, or completeness of prior AI conversations.
