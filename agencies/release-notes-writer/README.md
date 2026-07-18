# Release Notes Writer

Transforms commit messages into a customer-ready `deliverables/release_notes.md`. It builds on useful trace memory while enforcing its per-run COGS ceiling.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/release-notes-writer my-release-notes && fabri serve
```

`__AGENCY_ROOT__` and `__AGENCY_SLUG__` are replaced during installation; `__RUN_FROM__` anchors the installed agency's SQLite memory database to the command's working directory.
