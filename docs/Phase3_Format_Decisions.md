# Phase 3 file-format decisions and open questions

The handout's file descriptions disagree with each other in a few places (for
example, the Available Games File is described as both 49 and 42 characters per
line). This file records the layout we implemented for each record and the
questions we still want the TA to confirm. Source: `Project_Docs/Extreme Project -
Games Distribution (2026).docx.md`, file-format sections.

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
| 00 logout | code 2, space, name 15, space, type 2, space, credit at logout 9 | 31 | Handout's end-of-session layout; changed from a bare `00` after Phase 1 feedback |

`END` followed by spaces (or bare `END`) terminates each input file. Blank lines,
bad separators, duplicate records, invalid types/money/names, and missing END are
rejected with a file/line diagnostic. The two documented game-field widths are
accepted by length, not by arbitrary whitespace tokenization; embedded spaces
in game and user names remain intact. A 26-character game name remains invalid.

## Behavior decisions requiring confirmation

1. Confirm all disputed widths. (The 00 record now uses the handout's user layout.) Confirm whether
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
10. Confirm the SEARCH interpretation (client update: list all items and users
   whose names contain the query; non-admins must not see administrators who are
   not selling games). Implemented as command `search` for every account type,
   with one query line (surrounding spaces ignored, blank rejected) and a
   case-insensitive substring match. Items are the games available for sale this
   session; a game sold this session is not shown until the next session, and a
   user deleted this session is not shown. "Selling games" means having at least
   one game available for sale. Games show name, seller and price; users show name
   and account type, never credit. Search writes no DTF record. Tests: TC47-TC54.

These questions are still open with the TA.
