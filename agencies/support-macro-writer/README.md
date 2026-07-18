# Support Macro Writer

Drafts a helpful, empathetic reply from a support ticket. The agency keeps its own learning memory and declares a hard per-run COGS ceiling.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/support-macro-writer my-support-writer && fabri serve
```

Installation replaces `__AGENCY_ROOT__` with the agency directory and `__AGENCY_SLUG__` with a unique slug. `__RUN_FROM__` records the installer working directory for the SQLite memory database.
