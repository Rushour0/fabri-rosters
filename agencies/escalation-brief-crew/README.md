# Escalation Brief Crew

Turns a stalled support thread into a clear, evidence-based engineering escalation. The context extractor pulls the problem, timeline, and reproduction details from the raw thread; the brief writer shapes them into a handoff engineering can act on.

Deliverable: an engineering escalation brief with a summary, repro steps, customer impact, and a specific ask.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/escalation-brief-crew escalation-brief-crew
```

At install time, `__AGENCY_ROOT__` becomes this agency directory, `__AGENCY_SLUG__` makes its memory collections unique, and `__RUN_FROM__` resolves the caller's working directory for the SQLite memory database.
