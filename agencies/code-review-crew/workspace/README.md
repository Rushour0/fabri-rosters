# Workspace: payment.py

A small billing module with a subtle bug in `apply_late_fee`: `daily_rate`
is meant to be a per-day rate (e.g. `0.01` == 1%/day), but the function
applies it as `1 + daily_rate * days_late` — simple, non-compounding
interest — while the docstring and callers elsewhere in the codebase
assume daily compounding (`(1 + daily_rate) ** days_late`). For balances
left unpaid many days, this under-charges the fee, silently costing the
business money as `days_late` grows.

`split_payment` is included as a correctly-implemented sibling function
(no bug) so the crew has to actually localize the defect rather than
assume everything is broken.
