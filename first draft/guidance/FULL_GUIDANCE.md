# Purrpose Full Product and Engineering Guidance

Revision 2.1 · Portable implementation specification · Review draft · 24 October 2026

**Publication status: first draft shared for review with owner approval, not production approval.** This specification is self-contained: it does not assume a particular team, chat history, repository, country of residence or existing application. Interfaces and data structures are implementation contracts, not claims that application code exists. First complete the deployment setup in section 3. Unresolved settings are listed in OPEN_DECISIONS.md. HUMAN_GUIDE.md is the plain-English companion; RULE_MAP.md links both versions using stable rule IDs.

## 1. Purpose

Purrpose has two equally important purposes:

1. Help supporters find organizations and specific requests they can reasonably consider supporting, based on evidence about identity, need, funding and relevant risk.
2. Give animal rescue organizations of all sizes a fair chance to be seen, supported by information they can substantiate.

Trust and genuine need are questions the system helps investigate, not guarantees it assumes. Missing information does not prove dishonesty. Registration alone does not prove a particular request is genuine or still needs money. No model, score or polished website certifies an organization.

The system should reduce the time and effort required to find and inspect information. When no case meets the gates, it should still help by organizing known facts, explaining what could not be checked and pointing to useful information channels.

## 2. Scope and versions

### MVP 1

- Animal rescue organizations, not individual fundraisers.
- Organizations operating in the configured region, with cases actually receiving rescue or treatment there, whose identity can be checked through applicable official registration channels. The Ontario reference profile uses applicable Canadian channels: federal incorporation is allowed and Ontario-only incorporation is not required.
- Specific medical fundraising requests for one cat or a group of cats, with identifiable case scope.
- A small curated collection of real organizations/cases. The system does not promise whole-internet discovery.
- Two primary entry points: supporter seeking an organization/case, and an organization seeking a gap review of its public information.
- One controlled later update to demonstrate sourced memory and re-review.
- No collection or processing of payments. No login-based private document intake.

### MVP 2

The second minimum demo must allow continuing operational needs such as cat food, routine medical care and premises. These need purpose-specific records, a budget period, existing resources and a period-specific gap. This is an explicit next-version goal, not an unspecified distant possibility. MVP 1 medical rules must not be blindly reused as operating-budget rules.

### Later capability expansion

Consider rescue teams without formal registration when they can provide other checkable identity evidence. Define a separate identity policy before allowing them into qualified recommendations. Add more regions only after region-specific channels are validated.

Expand evidence analysis through Meterless routing to connected and verified models, with the agent invoking authorized tools for different material types. This does not mean Meterless automatically connects every model, website or tool. Each capability requires access, implementation and acceptance evidence.

### Out of scope

Private file uploads; hosting an organization's proof-submission portal; direct recommendations of individual rescuers; handling payments or payment credentials; autonomous messages to organizations/clinics; trust scores; charity certification; comprehensive legal clearance; broad real-time monitoring; or general charity recommendations outside the validated region/domain.

When a user asks outside scope, explain the limitation, do not apply inapplicable rules, and offer the supported scope with permission. Known information or search channels may be shared as unverified guidance. An out-of-scope request must not become a qualified recommendation.

## 3. Region setup for development assistants

### 3.1 Deployment setup before implementation

Read existing project configuration if available. Ask the person commissioning the implementation for missing deployment facts in one concise setup exchange:

1. Target country and province/state, and whether to use the supplied Ontario reference profile.
2. Workspace/repository to implement in, and any existing code to preserve.
3. Product policy owner, business review operator if any, and holders of tool/account permissions. These are role names, not assumptions about named people.
4. Available NVIDIA, Meterless/Nightshift, H-MEM and Zetaris access, model/runtime capabilities, and permitted budget. Request configuration presence, not secrets pasted into chat.
5. Whether the immediate objective is a fixture demonstration, live integration testing or a deployable application. Agree actual delivery authority before publishing or hosting.

Record supplied choices in a deployment profile, retaining unresolved fields explicitly. Reuse recorded choices until changed. The country where the developer or requester lives is not automatically the target evidence jurisdiction.

The agent must not wait for perfect live access to do safe independent work: implement schema, fixture-based rules and tests while recording blocked integrations. No codebase or account described in an example should be assumed to exist locally.

### 3.2 Region profile

Ontario, Canada is the reference jurisdiction used by this specification's examples. Ask: “Which country and province/state should this implementation cover? Use the Ontario reference profile, or adapt to another region?” If the configuration already answers this question, use it rather than starting a new interview.

For another region, identify applicable identity, sanctions and risk channels; test access and permitted use; record coverage and costs. Search scope may be adjusted for development, but qualification remains disabled until the region profile is approved and tested. Common evidence, uncertainty, funding and no-payment rules cannot be weakened by a regional adapter.

For a new implementation, the commissioning product owner selects the delivery region and records it. Region changes do not relax common gates. The Ontario examples below are reference fixtures: substitute the configured jurisdiction consistently, including public-source channels, geography filters, timezone, currency handling and scope messages. Until a new region's mandatory checks are approved and tested, qualification remains disabled for that region.

## 4. Core concepts

An **organization** has an official identity, names/aliases, identifiers and relevant organization-wide risks. A **case** is a particular request associated with that organization, with its own medical evidence, funding and city. An **evidence item** is source material with provenance and scope. A **claim** is a specific statement supported, reported or left unresolved by evidence. A **review** applies a specific policy version to validated claims at a recorded time. A **run** records the technical execution of that review. A **case version** preserves what changed.

Eligibility is case-specific. One passing case does not approve every case or certify the organization. Organization-wide relevant risk can prevent an otherwise complete case from qualifying. A successful past case does not automatically benefit another organization in a similar situation.

## 5. Supporter journey

### 5.1 Starting inputs

The supporter may say “I want to help a cat” or provide a case link/organization name. Broad discovery is limited to cat medical cases in the configured region. Use the configured animal/purpose scope without asking the user to establish it again.

Ask once about city, substituting the configured region: “Do you prefer a city in [region], or is anywhere in [region] okay?” A stated preference should be used directly. No city preference means the whole validated regional collection. Do not require donation amount, real name, email or contact details to see results. No personal donation profile is created.

If a city has no qualifying cases, say so before asking whether to broaden to other supported cities. Do not silently ignore the preference. A reminder of out-of-scope behavior is sufficient; a global discovery product is not required.

### 5.2 Candidate selection

Load only in-scope cases from the curated, connected set. Match the actual treatment/rescue city, not the organization's headquarters. In the Ontario example, an organization headquartered in Toronto with a case treated in Ottawa belongs under Ottawa for this workflow.

If case city is unknown, do not substitute the headquarters. It cannot satisfy a specific-city query; it may appear in the region-wide pending list if the case's presence in the supported region is otherwise established. Unestablished regional case location prevents qualification.

Apply the six eligibility gates. Put qualifying and pending results in separate lists. Do not force a recommendation if none qualify. Explain known facts, failed/unknown requirements and suggested information channels for pending cases.

### 5.3 Display order

Within each list sort case city A–Z, then full organization name A–Z, then case name A–Z, ignoring case. This is a display order, not a ranking of trust or merit. For a city-specific query, filter first and then apply the same ordering.

Implementation detail for ties/unknowns: use a documented stable normalization and stable case ID as the final tie breaker. Place unknown cities last in a region-wide pending list. Confirm any materially different display rule before changing it. Do not reorder using follower counts, sentiment, model preference or paid placement.

### 5.4 Result contents

For each qualifying case show full organization name and actual registration category; case name/city/medical request; source-linked supporting material; disclosed cost, available funds and remainder with dates; a qualification about disclosed funding coverage; risk-check sources/date/coverage; unresolved limitations; and the checked external donation link.

Funding qualification: “Calculated from the organization's disclosures as of [date]; all funding has not been independently confirmed.” If a different translation is used, preserve its meaning. Show this next to the amount, not hidden in terms.

For pending cases show the organization/case, known information, why the result is not verified to the required scope, missing evidence and where that information could reasonably be sought. Do not describe every pending organization as untrustworthy.

## 6. Organization information-review journey

Organizations publish and update materials on their own websites or suitable public platforms. Purrpose does not accept private evidence uploads or host their proof documents.

Anyone may tell the agent a public page was updated and provide a link. Notification does not prove they represent the organization, grant editing privileges or establish the contents as fact. Apply the same reading and validation rules regardless of who provides a link.

The agent reads authorized public sources, compares relevant validated facts and returns a concrete gap list. For every item include: current condition (satisfied/missing/expired/conflicting); exactly what is missing; why it matters; suggested source/channel for obtaining it; and what will be rechecked after a public update.

Do not instruct organizations to publish private donor details, personal addresses, payment credentials or sensitive unredacted medical information. Suggest an appropriate public redacted statement or supported alternative. If the necessary evidence cannot safely be made available, record the limit rather than demanding disclosure.

An organization is not guaranteed qualification, exposure or donations after following the suggestions. Publication of a new page triggers a new review, not automatic approval.

## 7. Six qualification gates

A case is eligible for the qualified list only when all six pass under a configured region and policy version:

1. **Identity and geography:** checkable applicable official organization identity; organization operates in the configured region; actual case is in that region.
2. **Medical need:** a concrete organization-issued request plus medical material corresponding to that case, with issuer, date and relevant content.
3. **Funding evidence:** usable documented cost and dated, same-case funding information that meet freshness rules; unresolved overlap does not affect the calculation.
4. **Positive disclosed remainder:** a justified positive remaining amount, explicitly described as disclosure-based rather than fully independently confirmed funding.
5. **Donation-channel ownership:** an external donation channel reached from the checked organization website, with organization/payee details consistent enough to establish the channel belongs to it.
6. **Required organization risk checks:** the applicable configured channel checks are complete and no relevant issue triggers a hold.

Administrative identity checks can be reused across cases while valid. Medical and funding gates remain per case. A donation link does not compensate for missing medical evidence. A model's confidence does not pass any gate.

Use separate reasons for pending information, incomplete technical checks, unresolved risk and no current disclosed funding gap. A zero remainder is not misconduct and is not a current money recommendation.

## 8. Evidence standards

### 8.1 Required medical information

The organization must describe which cat/group, what the medical problem/request is, and the support sought. Supporting medical material may include a veterinary estimate, treatment plan or clinic statement that can be connected to the case. Redaction is permitted if issuer/date/case connection and the necessary content remain checkable.

Organization statements, photographs, videos or comments alone do not meet the medical-material gate. They can supplement the record or raise questions. Reading a document is not authentication of its issuer; record what was and was not actually checked.

### 8.2 Every usable evidence record

Store an evidence ID, original URL/source reference, publisher, origin group, source type, relevant excerpt/location or document page, captured timestamp, source date or unknown, claim links, limits, and permission/access notes. Use content fingerprints where appropriate for detecting changes; a fingerprint proves content identity, not truth.

Capture time is not publication time. A website opened today can still contain an old funding total. If a change is first noticed today but its actual date is unknown, say so.

Two reposts of one claim are one origin, not independent confirmation. Organization videos remain organization-origin statements. A person claiming to be a volunteer/donor has unconfirmed identity/experience unless separately supported. Model-generated summaries are derived artifacts, never independent evidence.

### 8.3 Labels on claims

Use “Supported by cited evidence,” “Reported by fundraiser,” “Needs clarification,” “Out of date” or “Not established,” with the specific scope. The first label means that the cited source supports that statement; it does not prove the document is genuine or the organization is safe.

### 8.4 Material relevance

Form does not determine importance; relationship to a current decision does. A video may be background, but a specific statement that the case is fully funded may affect funding. A comment about misused money is a lead, not a proven risk. Screen it for case relevance, specificity and checkable new information before deciding further action.

Unscreened arbitrary comments cannot directly remove qualified status. A meaningful unresolved contradiction or reliable risk evidence can trigger pending/review state. Do not publicly repeat an unverified allegation as fact.

## 9. Funding calculations

Use integer minor units and a single currency per calculation. Preserve whether values are estimates, reported receipts, commitments, grants or paid bills. Missing is null, not zero.

Compute remaining only when costs/funds have the same case and compatible scope/date, funding overlaps are resolved and the disclosure basis is adequate for the stated result. Do not count a grant separately if it is included in reported raised funds. Do not count a pledge as received funds or add an estimate and its later invoice as separate costs.

The base expression is cost minus eligible non-overlapping case funding. When negative, remainder is zero and any excess is recorded separately. Different currencies or unknown inclusion prevent an exact result unless an approved conversion/inclusion basis exists. Organizational reserves do not automatically belong to this case; confirm scope and restrictions.

**Level 1 is sufficient:** the organization supplies dated compatible disclosures, but completeness is not independently confirmed. State that limit adjacent to the number. Extra platform/grant records may add support within their coverage; never imply full visibility of all funding channels.

Synthetic example: estimate CAD 2,000; raised CAD 700; grant CAD 300. Separate grant → remaining CAD 1,000. Included grant → remaining CAD 1,300. Unknown inclusion → exact remaining not established. No independent-coverage claim is made in any of these examples.

Code, not a model, computes eligibility and amounts. The frontend formats values but does not implement a competing funding rule.

## 10. No payment functionality

The agent never receives, transfers, initiates or processes money, connects payment accounts, or handles payment credentials. It only points to an externally checked organization-owned channel. The user chooses whether to leave Purrpose and donate independently.

If channel ownership cannot be established, the case does not qualify and there is no donation action link presented as endorsed/checked. No automatic payment, embedded checkout or private payee verification flow is in scope.

## 11. Freshness and policy configuration

Working MVP defaults confirmed during review:

- Funding progress is dated within 7 days at review.
- Medical estimate/plan uses the stated validity period when supplied. If none is given, default maximum age is 30 days.
- A 24-hour review refresh interval applies when there is no known update signal. It is not an embargo on new evidence or a promise of background monitoring.

Centralize these in versioned configuration, not duplicated constants in code. Record policy version and effective time on each review. Feedback may propose a change, but a single user's suggestion does not alter all cases automatically. Authorized policy changes require the designated product policy owner's recorded approval; do not silently rewrite historical reviews.

For timestamped evidence, equality to the configured maximum age is valid; exceeding it expires the evidence. Date-only evidence uses calendar-date age in the configured region timezone, without inventing a publication timestamp. A date-only expiration remains valid through the end of that local date. Future source dates require clarification and cannot extend validity. Keep these semantics in configuration and boundary tests.

## 12. Updates, caching and current judgments

### 12.1 Current versus historical information

Default current review uses the latest obtained, applicable evidence. Historical evidence cannot override newer reviewed facts merely because it is in memory. Keep history for explicit historical questions, relevant contradictions or still-applicable risk records, not for re-analyzing every old page on every request.

A relevant old confirmed misuse finding does not disappear when the latest website stops mentioning it. A changed amount can require clarification without the old amount replacing the new one.

### 12.2 Review reuse

Before displaying a qualified recommendation, validate scope, current policy version, source freshness, review refresh age and update/risk signals. Reuse an eligible completed result and display its real reviewed time. Never claim it was just rechecked if it was cached.

An explicit request for the latest information or a relevant update notification bypasses cached review reuse. For a screened credible update affecting eligibility, mark “Update awaiting review” and suspend current qualified recommendation until the affected check finishes. Unscreened content is only a lead; it does not control qualification.

There is no continuous background monitor in MVP 1. Without a notification or request, the system cannot guarantee immediate discovery of changed pages. The refresh interval is checked when the result is requested/opened; it does not create a scheduler.

### 12.3 Incremental review

Funding update → recheck amount/date/overlap/remainder. Medical update → recheck case linkage/treatment/cost/freshness. Identity, donation-channel or risk update → recheck relevant qualification and route unresolved risk to human review.

Other checks can be reused only if unexpired, policy-compatible and unaffected. If impact cannot be determined, recheck all six gates. A new rule version requires re-evaluating the relevant policy-dependent checks before qualification.

### 12.4 Partial source success

Track each requested source separately. Critical-source failure or unclear impact means pending. Optional-source failure need not invalidate otherwise complete gates, but show the relevant unverified limitation. Preserve successful results while retrying only still-needed failed steps, unless data or rules changed.

### 12.5 Extraction cache

Reuse validated extraction keyed by content fingerprint, parser/model version, prompt version and extraction schema. This can save model calls for an unchanged estimate. It does not bypass time checks, new funding/risk facts or current gate evaluation. Scope cached data by source/case; user-specific memory must not leak through shared cache.

## 13. Organization risk and applicable channels

### 13.1 Risk actions

- An identifiable, relevant formal finding of corruption/fund misuse prevents qualified recommendation and remains visible with source/date/scope. Restoration requires authorized business review plus all six gates.
- A substantiated ongoing investigation or unresolved allegation requires pending/human review, with no finding of guilt implied.
- Unattributed accusations, generic negative reviews and duplicate hearsay remain leads. Do not automatically suspend on arbitrary comments.
- A financial discrepancy, registration revocation or sanction does not by itself establish corruption. Read the reason and procedural status.

Verify organization/person identity, relationship to the current organization, time and subsequent correction/appeal/reversal. Preserve uncertainty. Do not publish speculative accusations.

Check current registration status separately from matching identity. Valid active status may pass the identity gate only. Dissolved, cancelled or unestablished current validity prevents qualification. Suspension, penalties or revoked qualifications require review of their effect, not an automatic corruption label. Corporate/nonprofit identity and charitable status are separate: loss of charitable status need not dissolve a corporation, but revoked charitable credentials and tax-receipt promises must not remain displayed.

Risk-held cases require checkable new evidence before restoration, such as a formally reversed finding, a demonstrated mistaken organizational match, or a competent authority lifting relevant restrictions. The organization's explanation, apology or remediation statement alone is insufficient. An authorized business reviewer records evidence, decision and reason; the agent rechecks all six current gates. Preserve original risk history. Without sufficient evidence or an authorized reviewer, the hold remains. The agent cannot automatically decide that the past issue has been resolved.

### 13.2 Channel execution states

For each applicable region profile record:

- `completed`: a valid scoped query/read, correct identity matching and recorded outcome.
- `not_applicable`: documented reason the channel does not cover this entity type; not a substitute for an inaccessible required check.
- `incomplete`: not executed, inaccessible, failed or unable to establish correct identity.
- `needs_review`: potentially relevant material or ambiguous match/status requiring business review.

For identity, no match means identity unestablished, not proof that no registration exists. For risk, a valid completed query with no match means “No relevant record found in this channel within the checked scope,” not “No risk.” Empty errors and blank pages do not count as negative results.

Store identifiers, aliases/queries, channel, query time, scope, match basis, outcome and limitations. Do not bulk-search unrelated private individuals or infer relevance from a name collision.

### 13.3 Channel research status

For the Ontario reference profile, candidate first tests are CRA listing/public sanctions for applicable registered charities, and the applicable federal/Ontario organization registry for identity. A non-charitable nonprofit not in CRA is not automatically unregistered. Conversely, an active corporate record does not establish charitable status. Another region needs its own applicable channels, not renamed Canadian ones.

Public court/risk coverage and permitted automated use remain unresolved. Some official portals restrict copying/sharing; CanLII has restrictive terms and incomplete coverage. Do not treat a public search box as an approved data connector. Do not buy access, bypass controls or scrape restricted results by default.

This specification does not ship an approved, end-to-end automated risk profile. Its Ontario channel candidates are research starting points, not a completed service. Therefore a real case cannot be called fully qualified by inventing channel coverage. Keep the necessary risk gate incomplete until a validated profile is approved for the deployment. Synthetic fixtures can test the pass logic, but not prove a real background check.

This is a known dependency, not permission to remove the gate. Channel research findings and remaining access tests are listed in OPEN_DECISIONS.md.

## 14. Feedback and memory

### 14.1 Three kinds of feedback

User preferences can immediately affect that user's current-session filtering. Factual corrections/new evidence are recorded as candidates and checked before changing facts. Rule-change suggestions are recorded with reasons and require authorized policy approval before they become general rules.

“Check volunteer experiences next time” may become a remembered investigation suggestion. “A positive volunteer comment proves trustworthiness” may not become a general rule.

### 14.2 H-MEM's useful job

Persist sourced case findings, unresolved questions, reviewed corrections and version relationships. Recall before subsequent review/answer and consume the recalled information. Recheck freshness and policy before reuse. Do not store a permanent “trustworthy” badge or treat confidence/relevance as evidence truth.

City preference lasts for the current session in MVP 1; no cross-session personal preference or donation history profile. Use separate alias/session scopes and test isolation. Public case evidence may be shared only through the evidence store's appropriate access policy, not by leaking another user's memory.

Show a real save → stop process → restart → retrieve → use sequence. Saving to a file that is never read back does not pass the H-MEM requirement. The memory record must retain source/provenance, case scope and correction lineage.

## 15. Autonomous permissions

The running product may query the configured case collection, read authorized public sources, call configured NVIDIA/Meterless/Zetaris/H-MEM adapters, execute confirmed rules and generate results/gap/review records.

It may not install new tools, register accounts, buy credits, modify policy, bypass access restrictions, expose endpoints, contact third parties or handle money. Unsupported material becomes a recorded capability gap with a suggested next step. Development assistants have their separately granted coding/tool permissions; do not confuse them with runtime permissions.

## 16. Orchestrator workflow

Use a small inspectable orchestration pipeline. A multi-agent architecture is not required. Internal design can vary if contracts and tests hold.

Keep data reality separate from execution mode. `scenario_type` describes each source/case as public real, historical snapshot or synthetic. `execution_mode` is `fixture` (local fixtures/mocked external adapters, no external retrieval/inference), `replay` (explicit saved-source versions; any separately selected real inference call must still be authorized, budgeted and recorded), or `live` (the configured current-source/provider path, with valid caches and reuse still disclosed). Real H-MEM can run in all three modes. A live model call over synthetic data is not real-case verification, and a live run must not silently substitute a snapshot after source failure.

1. **Request:** validate intent, case/organization input, region/session and explicit fixture/replay/live mode.
2. **Scope and preference:** enforce supported scope; ask for city once if discovery needs it.
3. **Candidates:** obtain curated in-scope candidates or resolve the supplied case/source to a candidate. Preserve unconfirmed linkage.
4. **Budget/reuse plan:** check allowed calls, review cache, extraction cache and relevant H-MEM context. Do not spend inference just to sort or compute.
5. **Sources:** read authorized uncached/changed sources; record success, failure, applicability and current evidence versions separately.
6. **Extraction:** parse structured fields locally where possible; when needed make at most the configured one model extraction call for this review action, with bounded source excerpts. Mark unprocessed material if limits are reached.
7. **Validation:** verify proposed fields/citations/case identity/units/date scope. Ambiguous model fields remain unconfirmed.
8. **Gates:** execute the six deterministic checks and applicable risk/channel rules. Calculate disclosure-based remainder in code.
9. **Business review routing:** preserve unresolved matters in a minimal queue/record; no invented human approval.
10. **Persistence:** save reviewed evidence/case version, relevant H-MEM record and technical run trace. Do not overwrite earlier conclusions.
11. **Output:** render structured findings, gap lists and limitations through templates. AI prose is optional and separately checked if requested/authorized.
12. **Result lookup:** return actual review time/version. Revalidation on later display may invalidate the cached qualification.

The technical trace may show actual execution ordering chosen by the implementation. It must expose which step failed, rather than forcing failures into a generic AI error. Retrieval can happen before source fetch, but stale recalled facts cannot bypass validation.

## 17. Model responsibility and output checks

NVIDIA or another explicitly connected appropriate model may propose a material summary, candidate organization/case match, potentially affected gate, extracted facts with original source locations and uncertainty.

Models cannot directly edit authoritative money, evidence state or qualification. The backend validates sources and executes rules. Model confidence does not become trustworthiness. Use suitable modalities; the existing text-only client is not automatically a video reader. Reading a scene is not verifying video authenticity/date/case identity.

Separate provider transport success, extraction validation and explanation-publication success. A fluent returned answer may fail citations or support. Keep unsupported drafts out of user conclusions and preserve a sanitized internal review reason.

If model reading fails, distinguish unreadable content, uncertain extraction and invalid output. Preserve source/issue. No automatic paid retry or provider switch. If critical facts cannot otherwise be validated, remain pending; if only prose fails, display structured evidence with “AI explanation unavailable” or “Draft held for review.”

## 18. Low-credit operation

Current account balances and billing entitlements are not known. Never state a remaining credit amount or guarantee free service. Start with one case reused across the demonstration and a very small curated set.

Use code for sorting, freshness, matching verified identifiers, arithmetic and templates. Default maximum extraction calls per review action: one, only if needed. Do not call the model when compatible validated extraction already exists. Follow-up questions first use structured facts and memory; if inference is needed, permit at most one bounded call and cache only against the same evidence/policy/question version.

No automatic best-of-N, repeated explanation rewrites, multi-model voting or background polling. A provider failure does not authorize another paid attempt. Budget denial is a recorded failed/incomplete step, not absence of evidence.

The project needs configured run/session call and token caps, input caps and timeouts before live use. These must not be guessed as account affordability. Unconfigured hard budget settings block external model execution; fixture-only engineering can continue. Reserve budget before scheduling calls and record returned usage. Unknown usage is null. A timed-out external call may still be billed: record uncertain usage and do not release its reservation as if nothing happened.

Prevent duplicate clicks using an idempotency key. Set per-step deadlines and a run deadline; no endless spinner or unlimited waiting. Retry only explicitly requested eligible failed steps and consider intervening source/policy changes. Cancellation stops new calls and labels any external call already underway honestly.

With more budget, expand cases/regions, refresh frequency and evaluated multimodal reading. Extra credits do not create source permission, prove authenticity or remove gate requirements. Scheduled monitoring is a future feature with separate operational rules.

## 19. Adapter contracts and connection acceptance

Use a shared application envelope: provider/tool ID, requested operation, status, result or null, model/version where relevant, usage or null, source references, latency and sanitized error category. Never expose raw secrets or private endpoint credentials. Configure each adapter in the actual deployment; no local experiments or shared credentials are assumed.

Each of NVIDIA, H-MEM, Nightshift and Zetaris has a separate acceptance record: configured; actual application request; usable result; result consumed in a useful feature; trace/error behavior. A mock tests adapter behavior, not the external service. A successful run elsewhere is not proof of this deployment's connectivity.

### NVIDIA

For NVIDIA hosted inference, verify the selected model's current official API example. The hosted chat-completions endpoint is `https://integrate.api.nvidia.com/v1/chat/completions`, with backend-held bearer credentials. Confirm model and modality access in the actual account. No keys in frontend bundles or prompts. Implement an adapter returning model, text or validated structured candidates, usage, finish reason and sanitized errors, with bounded input/output and timeouts.

Select an available NVIDIA model with the required capability inside the approved budget and record its identifier. Do not assume an example model is accessible. Model changes must preserve capability/budget/output checks and be recorded. Do not substitute silently. Direct NVIDIA calls and Meterless-routed calls are separate trace routes; do not count a direct call as Nightshift success.

### Meterless H-MEM

Use the official spec/reference, retaining relevant upstream instructions and license. Select, record and test a compatible upstream revision rather than assuming it is already installed. Inspect its actual add/query interfaces, persistence options, source/provenance fields and user/case scoping. A Node bridge to a Python backend is acceptable; its JSON arguments must not be shell-interpolated.

Determine the selected reference's actual runtime requirements, including TypeScript execution support where needed. Do not copy unrelated runtime installations to fix a missing tool. Resolve actual runtime compatibility. Run applicable upstream conformance plus new case-specific memory tests.

### Nightshift / Meterless provider

The referenced provider contract describes a configured base such as `http://127.0.0.1:8088/v1`, real bearer token, `meterless-app: purrpose`, and `meterless-scope: user` on chat. Verify the installed version's current official contract. Normalize `/v1` exactly once. Check `/v1/models` for authorized available `meterless/*` modes. 401/403 is unauthorized, not offline. `/healthz` alone does not prove inference works. Discover routing IDs rather than assuming a concrete underlying model.

An actual useful text request must return usable text and be consumed by the application. The referenced provider guidance allows a 180-second loading timeout; verify that against the selected runtime version. It is a compatibility consideration, not permission for indefinite run time. Align user-facing run deadlines with actual adapter timeout configuration.

The backend machine must reach the runtime. A browser replay is not an external listener; a remote backend cannot reach a runtime on another computer merely by using localhost. Do not expose an unauthenticated endpoint to make it work. Nightshift is unverified for a deployment until its actual application request passes.

### Zetaris

Query existing approved configured objects read-only through the real remote SSL JDBC connection. Start with the source repo's instructions and connection preflight, `SELECT 1` and database listing. Use configured driver and credentials, a valid JVM and one SQL statement per call. Never print credentials. New tables/grants/writes/resources need resource-owner approval and reviewed statements.

Discover existing authorized data sources in the configured instance. No database or table name from another deployment is assumed. For any historical charity dataset, record the reporting year and do not treat it as current registration or case need. An upstream HTTP 504 is a source failure, not a failed charity check. Do not rebuild infrastructure or disable SSL as a workaround.

Public case fields extracted from permitted sources may later be structured for Zetaris, but that integration is not already implemented. Preserve source relationships across any joins.

### Codex, Cursor, Claude Code and Gemini

Development assistants help implement and test adapters, workflow and specifications. They are not default production evidence reviewers and do not automatically share account access. Give them this guide and one bounded task in an authorized workspace. They must inspect actual files, source instructions and available tools before acting. No software can produce a reliable complete application solely because it read a document; example-based acceptance catches misunderstandings.

## 20. Internal review, user visibility and run records

Users normally see the result, sources, relevant limits and actual review time, not internal per-step logs or model activity. Evidence links remain accessible without requiring a history request. Keeping the workflow internal must not hide substantive uncertainty.

Every run has a unique ID and step records. Minimum fields: step, operation, source/tool/provider/model, started/ended time, result state, sanitized error/status code, impact on gates, reuse/cache marker and next useful action. Record available usage and its uncertainty. Never record API keys, auth headers, private donor content or unrestricted chain-of-thought. A concise decision reason and evidence mapping are sufficient.

Distinguish inference timeout from output held for invalid citations. In either case qualified structured results can remain if every necessary check was independently completed. Failure in critical extraction/validation does not qualify merely because templates can render a page.

A demo developer/operations view may inspect the trace on request. It is not part of the default supporter journey. Access to debug information must not expose credentials.

## 21. History queries

When users ask “Why did it fail last time?” or “What did you know before [time]?”, return the corresponding recorded conclusion, reasons and evidence available to the system by that cutoff. Do not inject later-discovered facts into a historical answer just because the source itself has an older date.

Maintain both source-effective time and system-known/recorded time. If an old review is missing or permitted retention did not preserve the supporting content, say so. Do not reconstruct a supposedly exact historical judgment and pretend it was recorded then. Public URL disappearance must be disclosed when showing a historical excerpt.

## 22. Business review queue

Business reviewers are authorized product operators, not developers automatically assigned ongoing review duties. MVP 1 needs only a simple queue/record, not a full management UI. Demo reviewer actions must be labelled simulated unless a legitimate operational process exists.

Queue record: case/organization/version, trigger, source links, relevant conflicts, completed checks, current hold, reviewer identity/authority, action/time/reason and subsequent version. No assigned reviewer/no action means still pending. Resolving one disputed item does not skip any other gate. Restoring qualification after risk requires authorized review and all six current gates.

Business reviewers handle evidence disputes within policy. Policy boundaries, thresholds and acceptance changes go to the designated product policy owner. Developers fix code and tests; account holders authorize resources and credentials. Never fabricate a reviewer sign-off.

## 23. Proposed technical interfaces

The following are interface requirements/proposals, not working endpoints. Internal names can change if documented consistently with examples and tests.

- `discover(preferences, session, mode)` → sorted qualified and pending case records plus coverage.
- `review(case_id, reason, mode, idempotency_key)` → run ID and later versioned review.
- `check_public_update(urls, case_hint, session)` → screened leads, per-source read outcomes and affected review status.
- `organization_gaps(organization_or_case, public_links)` → gate-specific missing/expired/conflicting items and recommended channels.
- `ask(case_id, question, cutoff?)` → current structured answer or recorded historical view, with sources and explicit unknowns.
- `get_run(run_id, role)` → sanitized result/trace according to access.
- `get_provider_status()` → distinct configured/online/unauthorized/offline/untested outcomes.

For HTTP implementation, use a validated API layer and run polling for long actions rather than holding a browser indefinitely. Do not let the client supply arbitrary SQL, provider tokens or executable tool names. Public URL fetching must be server-controlled and allowlisted for the curated set. Reject unapproved redirects, loopback/private-network document requests and unsafe types; a configured local provider is a separate explicit adapter exception.

## 24. Required data and configuration

Minimum durable entities: organization, case, evidence item/version, candidate extraction, validated claim, funding item/relationship, review/gate result, risk-channel check, run/step, feedback item, H-MEM record link, business review record and policy version.

Use explicit scenario type (`public_real`, `historical_snapshot`, `synthetic`) at case/source/result level. Real identity mixed with a synthetic case remains a synthetic demonstration, not a real request by that organization.

Policy includes region/domain, applicable channel matrix by entity type, freshness windows, refresh interval, evidence requirements, sort specification, version/effective time, and approved owners. Operational configuration includes provider/model, secrets held locally, bounds, timeouts, caches and state directories. Empty secret placeholders and unapproved required channels fail closed; do not read them as false/optional.

See policy.example.json and EXAMPLES.md. These specify shape and behavior but do not replace runtime validation or actual permissions.

## 25. Implementation roles and handover

At implementation setup, identify responsibility for product policy, coordination, evidence research, backend/integrations, testing and demonstration. One person may hold multiple roles; nobody is assigned implicitly by this document. Keep a short task/owner/branch/status record. Technical owners can use coding assistants with granted permissions.

Build order: (1) confirmed schema/config and labelled fixtures; (2) deterministic gates/funding/sort; (3) supporter and organization outputs; (4) real H-MEM recall and one controlled update; (5) bounded model and data adapters with truthful failures; (6) run trace and acceptance checks; (7) one-case demonstration. Frontend styling is outside this review and must not block core logic.

Independent work can proceed when a provider or risk source is blocked. Mock tests must be labelled. Developers resolve imports, branch conflicts and routine adapter bugs using their granted permissions. Escalate product-boundary/acceptance/policy decisions to the product policy owner; access and spending go to the relevant resource owner. If an owner is unavailable, preserve existing rules and continue independent work.

Route problems to the failing layer: NVIDIA model/account issues → provider owner/account holder; Nightshift runtime/auth → runtime owner/Meterless support; H-MEM persistence/scope → memory developer; Zetaris SQL/JDBC → data owner/Zetaris support; AWS deny/resource changes → AWS owner; source access/terms → evidence/data owner; model correctness → evidence/backend developer; business risk review → authorized business reviewer.

External support messages require human authorization; assistants may draft them. After a bounded debugging attempt without new information, record a sanitized reproduction and move to an independent task rather than repeatedly spending credits. Never bypass a security/access limit to make a demo green.

Handoff format: owner/task, branch/PR, files, actual verification/commit, mode/real integrations, current failure stage, next useful step and decision needed. A product decision request should include current rule, blocker, concrete options, recommendation and work continuing while waiting.

## 26. Acceptance and demonstration

The minimal demo proves four functions:

1. A supporter expresses intent and receives a qualifying case or an honest pending list with full organization information and sources.
2. An organization points to its public information and receives actionable missing-information suggestions.
3. A selected later public update triggers memory recall and the relevant re-review, preserving history.
4. A requested backend view identifies real tool activity, failure stage and available usage.

Use one case across the presentation to reduce complexity/cost. Prepare (a) a gate-complete fixture, (b) a missing-critical-material fixture, and (c) an update resolving a funding ambiguity. Clearly label public real material, historical snapshots and synthetic records. Never invent a real organization's treatment documents to force a successful recommendation.

If real sources cannot satisfy every gate, demonstrate pending real evidence and the successful workflow using synthetic fixtures. That demonstrates mechanics, not real-case verification. The blocked risk profile remains visible as an integration dependency.

Acceptance requires actual tests of calculation, source mapping, source failures, caches, history cutoffs, model output limits, memory restart/isolation, public update screening, sorting and no-payment boundaries. See ACCEPTANCE_CASES.md. A screenshot or a proposed endpoint is not passing execution evidence.

Integration acceptance is independent for each component. This specification includes working NVIDIA, H-MEM, Nightshift and Zetaris roles. Neither direct NVIDIA nor imported H-MEM alone completes the separate Nightshift gate. If implementing for an event, obtain its current submission rules from the commissioning owner and check them separately; do not assume an unidentified event or prior message is available to the implementer.

No test result should be declared passed until it ran against a named commit/mode. Completion report includes tests, real/synthetic data, provider outcomes, remaining dependencies and restart commands validated on a fresh checkout where possible.

## 27. Implementation inventory and delivery evidence

Before implementation, inventory the actual workspace, existing functionality, relevant licenses, configuration presence and permissions. If nothing is implemented, scaffold the smallest application satisfying the contracts. If code exists, preserve working behavior and identify the concrete gap against this specification. Never assume a particular repository, prior experiment or local path.

Write a deployment-specific runbook with actual dependency versions, setup/start/test commands, configuration, state paths and tool verification. A new developer or assistant must be able to reproduce the result without the original chat history. Report current integration evidence, not test results from a different application or machine. Publishing, deployment and sharing require the commissioning owner's explicit authority. Reading this document alone does not grant it.

## 28. Sources for integration and channel research

- Meterless engines/provider guide: https://meterless.ai/engines.html
- H-MEM reference/specs: https://github.com/Meterless/Meterless/tree/main/engines/hmem
- Zetaris JDBC setup: https://zetaris.github.io/getting-started/docs/connections/client-setup.html?protocol=jdbc
- NVIDIA model/API catalog: https://build.nvidia.com/
- CRA charity information and disclosure limits: https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/information-about-a-charity.html
- CRA penalties/suspensions: https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/compliance-audits-and-sanctions/compliance-audits/penalties-suspensions.html
- Corporations Canada data/API entry: https://ised-isde.canada.ca/site/corporations-canada/en/data-services
- Ontario Business Registry: https://www.ontario.ca/page/ontario-business-registry
- Ontario court search restrictions: https://www.ontario.ca/page/search-court-cases-online
- Ontario court decision coverage: https://www.ontariocourts.ca/scj/about-the-court-2/decisions-of-the-court/
- CanLII terms: https://www.canlii.org/info/terms.html

These references establish documentation and constraints, not current service credentials or completed per-organization queries. Do not confuse indexed page retrieval with a tested production connector.
