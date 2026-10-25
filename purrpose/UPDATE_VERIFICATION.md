# Screened update verification

24 October 2026. Local uncommitted working tree. Synthetic source changes, real local H-MEM, zero new external/model requests. Nightshift remains deferred.

Executed the complete suite with the actual local H-MEM reference: **94 tests passed**, including 12 new update checks. Covered unapproved links, observed changes inside freshness window, unchanged notices, failed unconfirmed notices, failed explicit latest requests, idempotency/reused-key rejection, malformed funding facts, wrong-case material, optional failure disclosure, required-source configuration safety, memory failure preserving pending state and useful real H-MEM incremental reuse.

Ran update_demo with workspace updates-20261024-a. Observed: baseline remaining 100000 cents; changed funding re-review remaining 50000 cents; duplicate response flagged replay without a new source read; explicit critical-source failure not qualified. H-MEM reused six unaffected fields and only the changed source needed reading. No live URL was fetched. The example.invalid URL is a fixture mapping, not a working fundraiser.

Limits: process-local synchronous intake/idempotency, fixture reader only, no network-reader deadlines, no durable event queue or continuous website watcher. Unknown/unconfirmed notifications cannot supply facts or representation authority. Current-source access failure is not fraud and does not become a current clean result. Tests are selected acceptance behavior, not all 127 guidance requirements.
