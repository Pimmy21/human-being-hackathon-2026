# Open Decisions and Dependencies

Portable review draft. This list assigns unresolved choices to roles. No reader needs to know a named person, original team or previous conversation. Identify the product policy owner and account/resource owners during setup. Nothing here grants publication authority. Existing product rules remain in force while missing settings are resolved.

## 1. Decisions for the designated product policy owner

### P1 — time boundaries — confirmed

For timestamped evidence, equality to the configured maximum age is valid; exceeding it expires the evidence. Date-only evidence uses calendar-date age in the configured region timezone, without inventing a publication timestamp. A date-only expiration remains valid through the end of that local date. Future source dates require clarification and cannot extend validity. Keep these semantics in configuration and boundary tests.

### P2 — registration status — confirmed

Check current registration status separately from matching identity. Valid active status may pass the identity gate only. Dissolved, cancelled or unestablished current validity prevents qualification. Suspension, penalties or revoked qualifications require review of their effect, not an automatic corruption label. Corporate/nonprofit identity and charitable status are separate: loss of charitable status need not dissolve a corporation, but revoked charitable credentials and tax-receipt promises must not remain displayed.

### P3 — final approved risk-channel applicability matrix

The actual minimum channel list must be validated per deployment region. For the Ontario reference profile, CRA listing/sanctions and applicable federal/Ontario identity channels are candidates. Appropriate permitted court/legal-risk coverage remains unresolved. Once access, permitted use and coverage have been tested, present a concrete matrix for approval.

Until then, no real case can silently pass a mandatory risk profile. Synthetic pass fixtures test mechanics only. Choosing to narrow/change the risk promise would be a product decision, not an engineering optimization.

### P4 — restoration standard — confirmed

Risk-held cases require checkable new evidence before restoration, such as a formally reversed finding, a demonstrated mistaken organizational match, or a competent authority lifting relevant restrictions. The organization's explanation, apology or remediation statement alone is insufficient. An authorized business reviewer records evidence, decision and reason; the agent rechecks all six current gates. Preserve original risk history. Without sufficient evidence or an authorized reviewer, the hold remains. The agent cannot automatically decide that the past issue has been resolved.

Deployments still need to designate authorized reviewers and map local procedural statuses; this does not reopen or weaken the confirmed restoration standard.

### P5 — evidence-driven agents and exceptional human review — confirmed

Six roles are coordination, identity/risk research, rescue-need research, funding/channel research, evaluation and dispute resolution. Run only needed roles; critique must cause concrete revised tasks where useful. Ordinary gaps automatically remain pending. Investigate disputes before human escalation; preserve established risk-hold restoration authority. FULL_GUIDANCE section 16 defines the contracts and escalation triggers. One targeted repair round is a low-credit demo cap, not extra inference authority or a production limit. This updates the earlier linear orchestration proposal without relaxing six-gate policy.

### P6 — demo completion — confirmed

The six-part contract in HUMAN_GUIDE R17 and FULL_GUIDANCE section 26 is approved. A real case need not qualify: honestly pending real information plus explicitly synthetic pass-path tests is acceptable. Actual behavior and integration evidence, not written descriptions, determine implementation completion. No renewed product interview is needed for these confirmed requirements. Missing permissions, runtime values and the approved source matrix remain deployment dependencies.

## 2. Access and operational decisions for the appropriate owner

These generally need the configured account/resource or technical owner, not necessarily the product policy owner:

- Actual remaining model credits, permitted spend and session call/token caps.
- Available NVIDIA model and its text/vision/video permissions. Text access is not proof of video access.
- Reachable Nightshift runtime, genuine token and useful application inference. A Web animation/replay is not proof.
- Actual Zetaris connection and source availability from the deployment backend. No credentials in public issues; no data tables are assumed.
- Public-source retrieval allowance, current registry access/terms and any required account subscription. Do not create accounts or purchase reports automatically.
- Run/source/model deadlines and input/output bounds consistent with the intended demonstration and credits. Configuration must be completed before live inference.
- Technical handling of provider errors, cancellation and reserved budget when billing is unknown.

For the current low-credit demo only, the guide fixes one extraction call shared across all six roles per review and one follow-up call if needed; these are upper bounds, not instructions to call. Production must use a separate configured service budget with sufficient bounded work, rather than inheriting demo caps. Service pricing/funding and measurable ordinary-use cost, latency and quality targets remain to be decided by the service owner. A repair cannot borrow the follow-up allowance or reset the review budget. Configure total task/source-read caps and concurrency alongside model budgets before live execution. Overall session spend still needs configuration.

## 3. Evidence work that must still happen

- Choose one real in-scope rescue/case with permitted public medical and funding evidence, or document why that cannot be obtained.
- Check current official identity/status using appropriate identifiers and applicable channels.
- Determine actual source coverage and permissions, including whether excerpts/version records may be retained for the intended use.
- Confirm medical-document correspondence without demanding private information be published.
- Check live funding inclusion/date and organization-owned donation channel.
- Document the real risk gate's uncompleted parts instead of replacing them with a synthetic pass.

A successful synthetic demonstration is useful engineering evidence but must not be presented as completion of these real-case tasks.

## 4. Technical choices implementers can make

Use the smallest working stack implementing the six conditional roles and shared-state feedback loop in FULL_GUIDANCE section 16. A single coordinator process is sufficient; a fixed linear pipeline is not. Choose validated data structures, local storage, adapter implementation, deterministic name normalization and a stable case-ID tie breaker. Place unknown cities last in the region-wide pending list as the suggested neutral representation. These details cannot change gate meaning, alter preference filtering or introduce a trust ranking.

Separate knowledge time from source time for historical queries. Choose a safe evidence-retention mechanism within actual permissions; full HTML/PDF archiving is not automatically allowed. Do not promise exact historical reconstruction where the permitted record is insufficient.

The actual APIs, dependency versions and launch commands need implementation/testing. Developers resolve routine imports and library choices within granted authority instead of escalating each one to the product owner. No package installation or model deployment is needed merely to review this draft.

## 5. Remaining delivery dependencies

- Named people must voluntarily claim task/coordination/review roles.
- Implement workflow code and adapters, or inspect/adapt existing code if the actual workspace contains a prototype. No prior implementation is assumed.
- A clean-checkout runbook and actual acceptance execution are still needed.
- For a hackathon deployment, obtain and check the event's current submission requirements before claiming compliance; event-specific requirements are not universal production rules.
- Frontend visual design remains intentionally deferred by this review request.
- Publication of this first draft for review is authorized. Deployment and further changes to product policy still require appropriate owner authority.

## 6. Grouped review request

The product policy owner first checks rule accuracy and examples, checks the confirmed P1/P2/P4 rules are accurately implemented. P3 still needs tested regional source findings; reviewer appointment remains deployment-specific. Account settings and routine implementation can progress with their appropriate owners without changing product rules.

No response is not approval, and an unresolved value is not an optional check.
