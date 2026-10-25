# Historical review verification

24 October 2026. Local uncommitted working tree. Real local official H-MEM, synthetic evidence only. No new model or external-source request; Nightshift remains deferred.

## Actual demonstration

Ran `python -m purrpose.history_demo` with the configured H-MEM reference, local state root and workspace history-20261024-a. Two reviews executed in this session. H-MEM stored original creation timestamps independently of the simulated source/review clock. The query at the first stored timestamp returned the old null remaining amount and grant-inclusion gap. The latest query returned 100000 CAD cents. A cutoff in 2000 returned history_unavailable. The original review was not recalculated or overwritten.

Saved summaries contain gate results, disposition, amount, reasons, disclosure wording, claims, source metadata and unresolved questions as recorded. Legacy snapshots lacking these fields are partial, not reconstructed using newer code. Original URLs are not asserted to remain available. Each answer is scoped to its case and memory workspace.

## Checks actually run

Full suite with actual H-MEM reference configured: **82 tests passed**, including 11 history checks: past unknown versus later known amount; inclusive cutoff; no record; missing system time; legacy summary; case separation; timezone offsets; invalid/ambiguous cutoff; later-discovered old source; immutable saved results; actual H-MEM cutoff query after an update.

Pure history tests make no network calls. The real memory test starts fresh Node bridge processes and verifies actual stored timestamps. Querying updates H-MEM access/audit state only, not its original creation time. No claim of production authorization, archival completeness, full public-web monitoring or current real-case verification.
