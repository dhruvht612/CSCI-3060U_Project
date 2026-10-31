# Phase 3 format decisions and TA questions

Status: provisional compatibility decisions, **not TA-approved requirements**.
The original inputs and expected files are unchanged. Source: the repository's
`Project_Docs/Extreme Project - Games Distribution (2026).docx.md`, Transaction
Code Details and file-format sections; compare `docs/phase2_design_notes.md`,
section 5, and `Project_Docs/README.txt`.

The Phase 3 assignment handout was not present in the repository or among the
course documents found in Downloads. Its path/link has been requested. This work
uses the available original handout, Phase 1 plan/cases, Phase 2 design, and the
user's Phase 3 checklist. Assignment-specific compliance remains unverified.

## Explicit compatibility profile

All widths below exclude the newline. Text fields are left-aligned and padded
with ASCII spaces. Money uses integer cents and zero-filled dollars with exactly
two decimal places. No name is silently truncated. Output uses platform newlines;
validation normalizes only CRLF to LF, retaining every other byte.

| Record | Implemented layout | Width | Evidence and conflict |
|---|---|---:|---|
| User input | name 15, space, type 2, space, credit 9 | 28 | Handout and fixtures agree |
| Games input | name 25 or padded 26, space, seller 15, space, price 6 | 48 or 49 | Fixtures use 48; handout heading/template 49, constraint 42 |
| Collection input | name 25 or padded 26, space, owner 15 | 41 or 42 | Fixtures use 41; handout says 42 |
| 01 create | code 2, space, name 15, space, type 2, space, zero credit 9 | 31 | Consistent with fixtures; no initial-credit prompt in handout |
| 02 delete | code 2, space, name 15, space, blank type 2, space, zero credit 9 | 31 | TC13 treats type/credit as unused; handout describes type/available credit |
| 03 sell | code 2, space, game 25, space, seller 15, space, price 6 | 51 | Fixtures accommodate explicit maximum names; handout template is shorter |
| 04 buy | code 2, space, game 25, space, seller 15, space, buyer 15, space, price 6 | 67 | Same conflict with short handout template |
| 05 refund | code 2, space, buyer 15, space, seller 15, space, amount 9 | 44 | Handout and fixtures agree |
| 06 addcredit | code 2, space, name 15, space, type 2, space, amount added 9 | 31 | Fixtures record delta; handout calls field available credit |
| 00 logout | bare `00` | 2 | Original fixtures and merged-file prose; user-layout template conflicts |

`END` followed by spaces (or bare `END`) terminates each input file. Blank lines,
bad separators, duplicate records, invalid types/money/names, and missing END are
rejected with a file/line diagnostic. The two documented game-field widths are
accepted by length, not by arbitrary whitespace tokenization; embedded spaces
in game and user names remain intact. A 26-character game name remains invalid.

## Behavior decisions requiring confirmation

1. Confirm all disputed widths and whether 00 needs user fields. Confirm whether
   delete type/credit should be retained and addcredit should contain a delta or
   resulting balance. No alternative expected fixtures have been silently substituted.
2. Confirm that each logout replaces the output file with that session only
   (existing behavior and TC07). Multiple logins reload the unchanged source
   files; this Front End does not perform the later Back End's persistence work.
3. Confirm immediate visibility of newly created users. Implemented: create,
   delete, buy, refund and credit changes affect current session memory; new
   listings reserve names but are unavailable to buy until reloaded in a later
   session from an externally updated games file.
4. Confirm the balance ceiling. The handout says 999,999; implemented as
   $999,999.00, not the larger $999,999.99 representable by the field. Both sides
   of transfers are checked before mutation; negative balances are rejected.
5. Confirm monetary input grammar. Existing interface requires digits, dot,
   exactly two decimals; negative signs, currency symbols and exponent notation
   are rejected. Zero is accepted because no positive minimum is specified.
6. Confirm name character rules. Names match exactly, are case-sensitive, allow
   internal spaces, and use printable ASCII without boundary spaces. Empty names,
   control characters and reserved `END` cannot round-trip through these files.
   Non-ASCII names are rejected under the byte-width profile; international names
   need a defined encoding/width policy.
7. Confirm self-purchase and same-user refund behavior. Neither is prohibited by
   the handout: permitted if the ordinary requirements hold; credit transfer has
   zero net effect. New-game rejection is enforced first, independently of this.
8. Confirm EOF without logout: existing behavior writes no DTF. EOF in a field
   reports an abandoned command. Output-write failure retains the live session.
9. Confirm any requirement changes issued by the TA/client outside this repository,
   including the existing admin-only `list` command, preserved from Phase 2.

No approval is implied by a passing fixture test. These questions are for the
TA/team to resolve before declaring official format compliance.

## Original test limitations

- TC25 uses an SS account, so buy is rejected before reading its fields; its two
  remaining field lines become invalid commands. Preserve this evidence. S06
  adds a buy-capable admin and verifies new listing and repeated listing rules.
- TC13 deletes `delete1`, which has no games in its fixture. S05 deletes `seller1`,
  attempts a purchase and a credit addition, and checks that the account vanishes.
- TC04 supplies a username after a rejected second login; the existing interface
  treats it as a new invalid command. The terminal assertion records this explicitly.
- Negative cases can pass while every transaction is a stub. Positive cases,
  state-sensitive supplemental cases and preserved baseline failures are necessary.
- TC46 covers create formatting only. Exact DTF validation applies to every case;
  supplemental tests cover mixed transaction sequences and state changes.
