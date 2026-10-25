# Revision 2.2 — Evidence-driven agent design

24 October 2026. Local review update; not uploaded or implemented by this document revision.

## Confirmed changes

- Six specialized roles with conditional delegation, shared versioned state and evaluator feedback.
- Targeted dispute resolution before exceptional human escalation; ordinary missing evidence stays automatically pending.
- Evidence-dependent task selection, incremental updates and concrete stop reasons, rather than a required linear sequence.
- Demo-only one-extraction/one-repair limits, with no additional paid inference authority. Production has separate service-managed budgets and an explicitly bounded retry policy. Neither profile allows role-specific budget resets. Ordinary users should not need provider-token management; pricing/funding remains a separate business decision.
- Versioned task/issue contracts, stale-result protection and observable plan changes.
- Sixteen new acceptance requirements (A01–A16), with sufficient/repaired/exhausted examples and an exceptional escalation example.

- Confirmed the six-part R17 completion contract and added BUILD_PLAN.md with implementation dependencies and evidence of completion.

## Preserved rules

Purpose, scope, city sorting, all six gates, disclosure-based funding, evidence freshness, no payments/private intake, source permissions, established risk-hold restoration authority and separate NVIDIA/H-MEM/Nightshift/Zetaris integration acceptance remain in force.

## Implementation status

The wireframe still simulates the earlier workflow. It does not implement six agents or prove nonlinear behavior. New acceptance cases are unexecuted requirements. No model/data calls were made for this documentation revision.

The repository's earlier architecture drawings and `ideas/parallel-research-agents.md` are historical proposals, not the normative 2.2 architecture. In particular, optional partnership/social-signal research is not a newly approved mandatory gate or connected capability. Use FULL_GUIDANCE section 16 for current behavior.

Still required before live qualification: approved/tested regional risk-channel matrix, source permissions and real case evidence; configured runtime budgets/access; actual application implementation and executed adapter/behavior tests. These cannot be completed by prose alone.
