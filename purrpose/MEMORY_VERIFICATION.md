# Real H-MEM integration evidence

24 October 2026 · Windows · Python 3.12.14 · Node 24.18.0. Local uncommitted working tree based on repository commit `5a8a208`. No upload/deployment.

## Upstream implementation

Used the existing official Meterless reference at revision `1742dec56a66e58eef9dda2d2b865823758ca8cd`, package `@meterless/hmem-reference` 0.1.0, Apache-2.0. The reference is a minimal runnable implementation, not a production library. No upstream code was modified or redistributed.

Actually ran `engines/hmem/conformance/runner.ts` with Node TypeScript transforms: **13/13 passed**. This establishes reference behavior, not complete application acceptance.

## Application tests

With `PURRPOSE_HMEM_REFERENCE` configured, executed `python -m unittest purrpose.test_core purrpose.test_memory -q`: **24/24 passed**, comprising the original 18 core tests and six real H-MEM tests:

- Save, fresh-process recall, useful incremental revalidation, both versions retained and real audit ledger present.
- Workspace/case isolation and path traversal rejection.
- Unchanged but expired evidence rejected.
- Established risk hold preserved despite a changed source omitting it.
- Duplicate save reuses memory ID; missing runtime fails explicitly.
- Cancelled review does not overwrite the previous useful snapshot.

Every save/recall starts a fresh Node process against the actual reference. No memory mocking or external embedding service.

## Restart demonstration actually executed

Ran `purrpose.memory_demo --phase first` and `--phase update` as separate Python invocations, same configured reference/state directory and workspace `demo-20261024-a`. README contains portable commands.

| Phase | Actual memory result | Review consequence |
|---|---|---|
| first | Saves `mem-1` with sourced unresolved grant-inclusion issue | Pending; remainder null; four fixture source reads |
| update | Recalls `mem-1`; consumes six revalidated unchanged fields and prior issue; saves `mem-2` | Only changed funding source read; synthetic qualified; CAD 1,000 remaining |

Dates 24/25 October are simulated evidence/review dates, not a day of monitoring. Registration/risk, medical and funding sources remain synthetic. External retrieval/inference calls: zero. The real component is official local H-MEM persistence, query, provenance and ledger.

## Limits

This demonstrates a useful narrow memory feature, not a production memory service. Retrieval uses the real H-MEM API with threshold 0 over at most 500 scoped snapshots, then selects latest sequence. No concurrent writes, historical-time API, automatic retention/sleep/dream processing or comprehensive schema migration. NVIDIA, Nightshift and Zetaris remain unconnected in this new app. Full user journeys and general dispute resolution remain incomplete.
