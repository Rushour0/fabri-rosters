# Market Research Brief

Researches the market question in `workspace/source/topic.md` and writes a
decision-ready `deliverables/brief.md`. The crew learns from its traces in
its own memory collections while keeping each run under its declared COGS
ceiling.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/market-research-brief my-research-brief && fabri serve
```

At install time, `__AGENCY_ROOT__` becomes this agency directory, `__AGENCY_SLUG__` makes its memory collections unique, and `__RUN_FROM__` resolves the caller's working directory for the SQLite memory database.
