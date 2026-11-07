# Tests

Each test is one transaction input file, `inputs/TCxx.txt`, run against the shared
data files in `data/`. For each test there are two expected outputs:

- `expected/TCxx.out`: exactly what the user sees on the terminal (prompts, the
  typed input, and the Front End's responses)
- `expected/TCxx.etf`: the daily transaction file written at logout

`TEST_CATALOG.md` lists every test with a short description of what it checks.

Run and check all tests from the repository root:

```sh
bash scripts/run_tests.sh
bash scripts/validate_tests.sh
```

## How the expected outputs were written

- The transaction records in each `.etf` file come from the Phase 1 test plan.
  The final `00` record was calculated by hand from the handout: the test's
  starting credit in `data/currentaccounts.txt` plus or minus every buy, refund
  and credit addition in that file.
- Each `.out` file shows the prompts and responses from our terminal design with the
  test's input lines placed after their prompts. Each one was checked against the
  test's description in `TEST_CATALOG.md`.

## Adding a test

1. Add the input as `inputs/TC55.txt` (one entry per line, ending with `logout`).
2. Add `expected/TC55.out` and `expected/TC55.etf`.
3. Add a line for it in `TEST_CATALOG.md`, then run both scripts.
