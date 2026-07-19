# Checkout outage timeline

- 09:02 UTC — Release 2026.04.12 deployed to production.
- 09:06 UTC — Checkout error rate alerts fired; customers received HTTP 500 responses.
- 09:10 UTC — On-call rolled back the release; errors began declining.
- 09:18 UTC — Error rate returned to baseline.
- 09:35 UTC — Team found the release expected a new payment-provider environment variable that was absent in production.
