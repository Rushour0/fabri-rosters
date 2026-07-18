# Bug Triage Crew

Locates a failing module, repairs the smallest defect, and verifies a green test suite. The crew learns from its traces in its own memory collections while keeping each run under its declared COGS ceiling.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/bug-triage-crew my-triage-crew && fabri serve
```

At install time, `__AGENCY_ROOT__` becomes this agency directory, `__AGENCY_SLUG__` makes its memory collections unique, and `__RUN_FROM__` resolves the caller's working directory for the SQLite memory database.
