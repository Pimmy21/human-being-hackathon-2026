# Purrpose Implementation Tasks

24 October 2026 · Product behavior confirmed; execution and integrations remain to be tested. Local update, not uploaded. Read FULL_GUIDANCE for authority and contracts; this plan does not relax them.

## Starting instruction for an authorized coding assistant

Read AGENTS.md, FULL_GUIDANCE.md, policy.example.json, EXAMPLES.md, ACCEPTANCE_CASES.md and OPEN_DECISIONS.md. Inspect the actual workspace and available configuration. Preserve working code. Reuse recorded setup; ask only for missing deployment facts. Start B01 and continue independent fixture work when live access is blocked. Record actual results and failures. Do not publish, spend beyond configured authority, create external resources or treat synthetic output as real verification.

## Work packages and completion evidence

| Task | Work | Dependencies | Done when |
|---|---|---|---|
| B01 — inventory and contracts | Inventory existing code/licenses/configuration; record region, owners, source permissions, mode and demo/production profile; define validated case/evidence/claim/issue/task/run schemas | Authorized workspace | Deployment-specific inventory and configuration-presence report; no secret values; unresolved settings explicit; fixture clock and schema checks run |
| B02 — rule engine | Implement six gates, integer funding arithmetic, overlap, freshness boundaries, identity/risk statuses and stable city/name ordering | B01 | Relevant G/R/H/S acceptance tests pass on labelled fixtures; current missing risk profile blocks real qualification |
| B03 — adaptive orchestration | Implement six role contracts, shared versioned state, coordinator dispatch, evaluator critique, dispute resolution and exceptional escalation; atomic budgets, attempt ledger, deadlines and cancellation | B01; use B02 for gates | A01–A16 routing assertions run; sufficient/repaired/exhausted paths differ in actions; no fixed all-role chain or budget reset; model-directed decisions labelled separately from fixture routing |
| B04 — user journeys and memory | Supporter outputs, organization public-link gap lists, H-MEM persistence/recall/use, source updates and historical cutoff answers | B02–B03 | Both journeys run; save/restart/recall demonstrably affects update review; only affected checks reopen; historical facts remain scoped and versioned |
| B05 — connected adapters | Independently connect NVIDIA, Nightshift and Zetaris; validate H-MEM actual use; apply configured source, modality and provider contracts | B01; consumption points in B03–B04 | Each claimed component has actual useful request/result/consumption and error evidence; secrets stay backend-only; unavailable components remain explicitly incomplete |
| B06 — demonstration and handover | Assemble one-case demo, readable basic interface, optional trace view, clean-checkout runbook and completion report | B02–B05; blocked live pieces reported | Six R17 items demonstrated or individually marked incomplete; executed acceptance results tied to commit/mode; no claim that fixture success proves real qualification |

B02 and B03 can be developed independently against shared schemas. B05 connectivity investigation need not wait for UI work. This task list is a development order, not the product's runtime flow. Source failures and account blockers must not prevent unrelated fixture engineering. No agent/person is assigned automatically; record task owner, branch and status when work starts.

## Practical first increment

Implement B01–B03 against one labelled synthetic Maple case before adding new external calls. Preserve the existing wireframe as a simulation. Build tests for complete facts, grant-inclusion repair, and exhausted ambiguity; attach actual task traces showing selected/skipped roles and changed plans. This proves orchestration mechanics at low cost. Then use B04–B05 to prove memory and real tool consumption. Never label this first increment a complete integrated agent.

## Completion record

For each task record files/commit, commands actually run, results, scenario/mode, real versus mocked dependencies, cost/usage if known, remaining blocker and next action. Use the completion-report template in ACCEPTANCE_CASES. Unknown usage is not zero; written acceptance rows are not passed tests.

## Remaining decisions are operational, not a new product definition

- Region-specific approved/tested identity and risk-channel matrix, permitted retrieval and real case materials.
- Actual runtime reachability, account access, model capabilities and budgets.
- Configured deadlines/source/task/concurrency caps and service owners.
- For production: separate efficiency targets, retry policy and service funding/pricing.

A frontend visual-design pass is separate. It must not change evidence meaning, hide limitations or block testing the core behavior. Publication/deployment remains separately authorized.
