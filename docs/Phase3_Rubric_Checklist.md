# Phase 3 rubric checklist

Reviewed November 5, 2026 on `audit/phase3`. Source: the official Phase 3 handout
pasted by the user after the initial audit. This is a working checklist, not a
verbatim copy of the assignment or an estimated grade.

The corrected due date is **Saturday, November 7, 2026 at 8:00 PM**
(America/Toronto). The existing report/generator still say November 6.

## Marking categories

| Category | Weight | Evidence and assessment | Remaining work |
|---|---:|---|---|
| Script quality | 2 | Bash wrappers call documented Python tooling; naming, comments, CLI help, timeouts and separate run folders make the process understandable. Some reporting/packaging code uses compressed statements, but no mark deduction is assumed. | Correct historical suite selection in the validator and reconcile stale documentation. |
| Automation | 1 | The runner discovers fixtures, captures terminal output, stderr, exit status and transaction files, checks expected DTF bytes and terminal events, and reports results. Fresh Git Bash validation passes 54/54. | Resolve whether the semantic terminal oracle meets the required expected-output-file comparison; provide reviewed transcript comparisons or TA acceptance. |
| Failure-log organization and completeness | 5 | Markdown provides test ID, purpose, actual failure, root cause, fix and retest columns across multiple executions. Iterations 1–4 retain intact evidence. | The PDF presents failure details as prose rather than the required table. Recover/disclose missing iteration 5/6 raw evidence; include updated SEARCH failures and retests in the final document. Record later observed harness failures and their eventual fixes accurately. |
| Source correctness | 2 | Fresh compilation has no diagnostics; 54/54 acceptance tests and 21/21 supplemental checks pass. All 11 validator mutation checks pass. | Phase 1 marking feedback and its disposition are not available for verification. Passing existing tests alone does not establish this part of the criterion. |
| Group effort | Discretionary | Repository activity can provide part of the evidence. | Lab presentations, requirement clarifications, peer feedback and fair contribution require team/TA evidence; this audit does not assign a score. |
| Bonus | 0–3 | Awarded to the best three Front Ends by the course, not determined by this audit. | If unwilling to share the Front End, state that in the submission document and forgo bonus eligibility. No opt-out is assumed. |

## Required workflow and deliverables

| Requirement | Status | Evidence or next action |
|---|---|---|
| Organize test inputs and corresponding expected outputs | Present | `inputs/TCxx.*.txt` and `expected/TCxx.*.txt`; shared test IDs associate the files. |
| Store terminal logs and daily transaction files | Present for old runs and fresh local audit; incomplete for SEARCH history | Existing run folders preserve both kinds; iterations 5/6 contain summary/manifest files without the detailed evidence they reference. |
| Command-line application, stdin/stdout and four file arguments | Present | `src/main.cpp` accepts users, available games, collection and output paths; fresh runs exercise that interface. The handout's example executable name is not a required name. |
| Unix shell or DOS scripts for execution and validation | Present | `scripts/run_tests.sh` and `scripts/validate_tests.sh` delegate to included Python tooling. A Python dependency does not itself contradict the rubric's scripts/macros/programs category. |
| Automated daily transaction comparison | Present | Exact expected DTF comparison after CRLF-to-LF normalization; schema and record checks also run. |
| Automated expected terminal-output comparison | Partial / TA interpretation unresolved | Event regexes and selected line checks validate behavior; `.expout.txt` prose is not compared directly with captured terminal output. |
| Multiple executions, failure table, fixes and full regression | Substantial evidence; gaps remain | Historical baseline/correction/regression data and Markdown table exist. PDF table formatting and missing SEARCH evidence need attention. |
| Tests updated for Phase 1 feedback | Unverified | Obtain actual marking feedback and map each applicable item to changed/added tests or an explained no-change decision. |
| Separate `.doc` or `.pdf` with failure table and running instructions | Not ready | Existing PDF has instructions but is stale and converts detailed table rows to prose. Rebuild and visually inspect a current document with the required table. |
| Separate source ZIP including tests, `.sh`, `.cpp` and `.h` files | Not ready | Local review ZIP contains old source and excludes SEARCH fixtures. Rebuild and test an extracted current ZIP. |
| Complete AI prompts/responses | Completeness and final delivery unverified | A Phase 3 history DOCX exists. The ZIP selector omits it; a separate Canvas attachment is allowed. Verify all contributing conversations and later submitted work are covered. The disclosure summary is not a substitute. |
| Commit all submission files to GitHub before the deadline | Partial / final submission state unverified | Code/docs are tracked, but generated `submission/` artifacts are ignored and `docs/AI_USAGE_LOG.md` is untracked. Ensure final required files are committed and pushed as appropriate; a local commit alone is insufficient. |
| Submit through Canvas by the deadline | Unverified | No Canvas submission is performed by this audit. |

The handout explicitly assigns zero if neither the required AI history nor a
truthful no-AI statement is submitted. Because AI was used, a no-AI statement
would be false. Complete history may be submitted separately from the source ZIP.

## Recommended completion order

1. Obtain Phase 1 marking feedback and any outstanding client/TA clarifications.
2. Fix historical validation and settle the terminal-output comparison approach.
3. Preserve real historical evidence, or disclose what cannot be recovered;
   document newly observed failures and fixes without fabricating past results.
4. Run all applicable tests after fixes and commit the resulting source/tests.
5. Produce a current document with the detailed failure table, CLI/script
   instructions, correct deadline, team names and any sharing opt-out.
6. Verify complete AI history, rebuild the ZIP, test the extracted package,
   commit/push the final required files and submit the separate artifacts to Canvas.

See `Phase3_Audit.md` for reproduction commands and the confirmed findings, and
`phase3_audit_evidence.json` for the fresh test results from the initial audit.
