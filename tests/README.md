# Terminal behavior oracle and review status

The original 46 `.expout.txt` files are descriptions, not transcripts. They are
preserved byte-for-byte. `terminal_assertions.json` maps each description to an
ordered sequence of expected success/rejection events using regular expressions.
These assertions were authored from the descriptions, input streams and existing
CLI messages **before the baseline run**, not copied from actual output.

Every case must have exactly the expected events in order, no unexpected success
or rejection, a command prompt, a username prompt, exit status zero and empty
stderr. Every original case ends in a valid logout, checked explicitly. Errors
in TC04 and TC25 caused by unused field lines are explicitly represented.
Exact DTF comparison independently verifies that a terminal success actually
produces the required transaction record.

No exact full-console transcript fixtures are introduced. Prompt wording/spacing
is not prescribed by the handout. If the team introduces `.transcript.txt` files
later, author them from specified behavior, obtain human review/sign-off, and
record reviewer/date before enabling them. Do not bless actual output as expected.

## Human review still required

Status: AI-authored behavioral mapping; **team/TA sign-off pending**. Review all
46 mappings alongside the original prose and inputs. A passing event check proves
observable acceptance/rejection, not the internal reason for a generic rejection.
Assess prompt clarity/politeness and intended interaction manually. Approve or
revise the provisional format/edge-case decisions in the accompanying document.

State effects absent from the original streams are covered by 21 supplemental
black-box scenarios in `scripts/supplemental_tests.py`: list-observed balances,
duplicate purchases, seller deletion, credit limits, new listings and recovery.
Expected amounts are specified independently. These scenarios supplement, rather
than overwrite or inflate, the count of 46 original acceptance tests.

The 11 validator mutation checks disable evidence hashing only on temporary copies
so the semantic validator itself must detect corrupted records/status/events.
The original saved evidence is never edited by these checks.
