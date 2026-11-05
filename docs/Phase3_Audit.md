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

**Rubric follow-up:** the user supplied the official Phase 3 assignment after
the initial audit. The revised deadline is **Saturday, November 7, 2026,
8:00 PM** (America/Toronto), replacing November 6. The handout is now available
as conversation evidence; the earlier limitation about the missing Phase 3
rubric is resolved. See `Phase3_Rubric_Checklist.md` for the category-by-category
assessment. This follow-up adds the PDF table finding and clarifies terminal
comparison, Phase 1 feedback and separate AI-history delivery requirements.

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

### P1 — AI-history delivery needs an explicit submission check

`scripts/prepare_submission.py:138–141` selects certain directories and an
explicit root-file list that includes `Phase2_AI_use.docx`, but excludes
`Phase3_AI_Use_History_Diana.docx`. The Phase 3 document is tracked by Git and
present at the root, but absent from the existing ZIP. Simply regenerating with
the current script will still omit it.

The supplied handout requires submission of the complete AI history but does
**not** require it to be inside the source ZIP. A separate Canvas attachment
satisfies that delivery arrangement. The ZIP omission is a risk if relying on
the package alone, not proof that no AI history has been or will be submitted.

**Action:** submit the history separately, explicitly include it in the package,
or place it in a packaged directory and update the references. Verify that it covers
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

### P1 — The PDF replaces the required failure table with prose entries

The rubric assigns 5/10 marks to a full failure log across multiple executions
in clear table form. `scripts/prepare_submission.py:58–66` deliberately converts
rows headed `Test ID` into labeled paragraphs. Page 5 of the existing
`submission/Phase3_Test_Report.pdf` was freshly rendered and visually inspected:
TC08, TC12, TC13, TC17 and TC19 are prose entries, not table rows. Their details
are readable, but the requested table is absent from this part of the submitted
PDF. The Markdown table in the ZIP does not establish compliance of the separate
required `.doc`/`.pdf` document. Regeneration with the current renderer preserves
this problem.

**Action:** render the detailed failure log as an actual table in the final
document, retaining the test ID, purpose, incorrect output, root cause and fix
columns, plus iteration/retest information. Use landscape pages or suitable
column widths and repeated headers; visually verify every failure-table page.

### P2 — Terminal validation does not compare the expected terminal files

The handout asks for a script to compare expected terminal output files with
actual terminal output. `expected/TC*.expout.txt` currently contains behavioral
prose (for example TC08), and `scripts/phase3_tests.py:81,109–127` checks actual
stdout against `tests/terminal_assertions.json` rather than those files. The
prose files are checked for existence and copied into snapshots, but their
contents are not the automated terminal oracle. This is meaningful behavioral
testing, including SEARCH content checks, but not a comparison to the expected
terminal files named in the handout. Most field prompts and other unrecognized
output lines are not fully checked.

**Action:** establish expected terminal transcripts from the requirements and
reviewed interaction, then compare them automatically, documenting any justified
normalization. Alternatively, obtain TA acceptance of the semantic oracle as
the terminal-output comparison. Do not copy actual transcripts into expected
files without independently reviewing their expected behavior. A single
validation script may check both output types; three separate shell scripts
are not required by the wording.

## Submission questions and documentation gaps

- The Phase 3 handout has now been supplied in the conversation. The README,
  execution guide and format decisions still describe it as missing, while the
  test report says it was reviewed earlier. Update the final submission's
  provenance/status wording and the November 6 deadline in the report and its
  generator. The supplied handout does not itself contain the SEARCH change;
  retain the separate client/TA source for that requirement.
- The handout requires tests to reflect Phase 1 marking feedback. No feedback
  record or feedback-to-test mapping was found in the reviewed files. The report
  says all 276 original fixtures are unchanged; supplemental and SEARCH cases
  alone do not prove feedback was addressed. Obtain the feedback, document each
  applicable correction and rerun the suite. Do not infer that changes were
  required if the actual feedback does not call for them.
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
contributions, the entire PDF layout, or completeness of prior AI conversations.
The rubric follow-up inspected existing PDF page 5 specifically to verify the
failure-log layout and reviewed the renderer, terminal oracle and assignment
requirements. It did not rerun the unchanged application tests; the fresh test
results above remain the evidence from the initial audit.
