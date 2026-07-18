# Code Review Crew

Reviews `workspace/payment.py` for a subtle defect, applies the smallest
correct fix, and explains what was wrong and why the fix is correct. The
crew learns from its traces in its own memory collections while keeping
each run under its declared COGS ceiling.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/code-review-crew my-review-crew && fabri serve
```

At install time, `__AGENCY_ROOT__` becomes this agency directory, `__AGENCY_SLUG__` makes its memory collections unique, and `__RUN_FROM__` resolves the caller's working directory for the SQLite memory database.
