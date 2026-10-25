# Purrpose Plain English Guide

Version 2.2 · Local update, not yet uploaded · Review draft · 24 October 2026

This is the human companion to FULL_GUIDANCE.md. Both describe the same product. Use the rule IDs below and RULE_MAP.md to compare them. This version explains decisions without code; it does not remove evidence requirements. Visual design is a separate later task.

## R01 Purpose

Purrpose helps supporters find organizations and requests they can reasonably trust and consider helping. It also gives animal rescue organizations of all sizes a fair chance to be seen, supported by information they can substantiate.

It explains what the evidence supports and what is still unknown. It does not guarantee that an organization is safe or that every claim is true.

## R02 First setup

The person commissioning the application provides the target country and province/state, workspace, tool access, budget and responsible people. The AI asks for missing information rather than assuming a particular team, account or machine.

Ontario, Canada is a worked reference example. Another region is allowed, but its official identity and risk sources must be checked before the system can call cases qualified. The developer's own location does not decide the search region.

## R03 First and second versions

Version 1 covers registered animal rescue organizations and specific medical requests for one cat or a group of cats, in a small connected collection. It does not recommend individual fundraisers directly.

Version 2 must add ongoing needs such as food, routine medical care and premises, using a defined budget period. Later versions may include unregistered teams with other checkable identity evidence, after separate standards are approved.

## R04 A supporter wants to help

The supporter can ask to find a case or ask about a specific organization/request. For discovery, ask once which city they prefer, or whether the whole supported region is okay. Do not require their name, contact details or intended donation amount.

Show qualified cases separately from pending cases. Order each list by treatment/rescue city, full organization name and case name, A–Z. Use the case's city, not the organization's headquarters. The order does not imply one case is more trustworthy. Ask before expanding beyond the user's preferred city.

## R05 An organization wants its information checked

The organization keeps information on its own website or suitable public platform. It provides public links, not private file uploads. Purrpose checks those pages using the same standards as the supporter journey.

Return a practical list: what is satisfied, missing, expired or conflicting; what to add; why it matters; and where the information could be obtained. Anyone can report a public update, but that report alone is not evidence or proof of authority to represent the organization.

## R06 When a case can be recommended

All six conditions must pass:

1. Official organization identity and in-region activity/case location are checkable.
2. The specific medical request has corresponding medical material.
3. Dated cost and funding information are usable, without unresolved double counting.
4. The disclosed information supports a positive remaining funding amount.
5. The external donation channel can be linked to the checked organization.
6. Required applicable risk checks are complete and do not trigger a hold.

Qualification applies to this case, not every request by the organization. If none qualify, show an honest pending list with known facts, missing information and useful places to look. Missing information does not mean dishonesty.

## R07 Evidence

Every usable fact links to its source, relevant passage/page, publisher and date. Record when the system read it separately from when the source was published.

Videos and comments may add useful information, but understanding content is not proving it genuine. Several reposts of the same story are not independent sources. A material's importance depends on how it affects the current decision, not its format. Vague accusations do not automatically remove a case from recommendations.

## R08 Funding

The system calculates money in code, not through a model's guess. Check whether grants are already included, whether a number is a pledge or money received, and whether all figures concern the same case and currency.

Example: an estimate of 2,000 minus 700 raised and a separate 300 grant leaves 1,000. If the grant is already included in the 700, the remainder is 1,300. If inclusion is unknown, the exact remainder is unknown.

The first version accepts the organization's dated disclosures when otherwise sufficient, but must say that all funding has not been independently confirmed. Unknown is not zero. A fully funded case is not a current positive-gap recommendation.

## R09 Organization risk

Check the configured applicable official channels and record their coverage. “No record found in these checks” is not “no risk.” A failed search is not a clean result. Some channels do not apply to every organization type, and this needs a documented reason.

A relevant formal fund-misuse finding triggers a hold. A suspected relevant investigation is first checked for identity and current status automatically. A confirmed relevant unresolved investigation stays pending and requires exceptional business review, not a statement of guilt. Anonymous or unsupported complaints remain leads. Registration penalties or revoked status are not automatically corruption.

The supplied Ontario source candidates are not a complete approved background-check service. Until mandatory channels are validated, real cases cannot silently pass that gate. Clearly synthetic test cases can still demonstrate how the rules work.

Check current registration status separately from matching identity. Valid active status may pass the identity gate only. Dissolved, cancelled or unestablished current validity prevents qualification. Suspension, penalties or revoked qualifications require review of their effect, not an automatic corruption label. Corporate/nonprofit identity and charitable status are separate: loss of charitable status need not dissolve a corporation, but revoked charitable credentials and tax-receipt promises must not remain displayed.

Risk-held cases require checkable new evidence before restoration, such as a formally reversed finding, a demonstrated mistaken organizational match, or a competent authority lifting relevant restrictions. The organization's explanation, apology or remediation statement alone is insufficient. An authorized business reviewer records evidence, decision and reason; the agent rechecks all six current gates. Preserve original risk history. Without sufficient evidence or an authorized reviewer, the hold remains. The agent cannot automatically decide that the past issue has been resolved.

## R10 Freshness and updates

Starting settings are seven days for funding progress, a medical document's stated validity or thirty days if none is stated, and a twenty-four-hour refresh interval when no update is known. These are adjustable policy settings, not fixed code or industry standards. For timestamped evidence, equality to the configured maximum age is valid; exceeding it expires the evidence. Date-only evidence uses calendar-date age in the configured region timezone, without inventing a publication timestamp. A date-only expiration remains valid through the end of that local date. Future source dates require clarification and cannot extend validity. Keep these semantics in configuration and boundary tests.

A relevant screened update or a request to refresh takes priority over cached results. Old information being within its age limit does not justify ignoring new material. If a critical update cannot be read or checked, keep the case pending. Optional material may fail without blocking otherwise complete required checks, but the limitation must be stated.

Version 1 does not watch every website continuously. Without a notification or request, it cannot promise immediate discovery. The refresh interval is checked when results are requested.

## R11 Memory and history

Remember sourced case facts, open questions and corrections. Reuse useful extraction from unchanged material to save calls, but still apply current time, policy and new evidence.

Normally use the latest applicable evidence. Bring in history when asked, when a relevant contradiction appears or when an old risk finding still matters. A historical answer uses only what the system knew then; it does not rewrite the past using later discoveries.

City preference stays within the current session. There is no personal donation-history profile in version 1.

Feedback has three paths: apply current-session preferences; check factual corrections against sources before changing facts; and record policy suggestions for the designated policy owner to approve. Remembering a suggestion does not make it a universal rule.

## R12 What the tools do

| Component | Job |
|---|---|
| Agent backend | Chooses authorized steps, checks evidence, applies rules and calculates results |
| NVIDIA | Helps read supported materials and proposes extracted facts with source locations |
| Meterless H-MEM | Saves and recalls sourced findings and unanswered questions |
| Nightshift / Meterless provider | Routes inference through a genuinely connected runtime/model path |
| Zetaris | Queries connected structured information with source relationships |
| Codex, Cursor, Claude Code, Gemini or another development assistant | Implements and tests the application using this specification and granted tools |

Models cannot directly change authoritative amounts or qualification. Each integration needs a real useful request and evidence that the application used the result. Installing a library or writing a prompt is not proof of integration.

### How the agents work together

Six roles share the case record: coordination, identity/risk research, medical-need research, funding/channel research, evidence evaluation and dispute resolution. Only needed roles run. They may use the same model, code or tools; six roles do not mean six model calls.

The evaluator challenges findings and identifies an exact problem. The coordinator changes the plan; the dispute resolver and relevant researcher look for evidence that could resolve it. Then the evidence is checked again. For example, an unclear grant inclusion triggers a targeted funding check, not another full organization review.

Complete evidence goes straight to the rule checks. Missing evidence can end as pending. Repeated unsuccessful actions stop at configured limits. New public information can reopen the affected checks. Money and recommendation rules remain enforced by code.

## R13 Efficient use and demo budget

**Current low-credit demo only:** use at most one model extraction call per review, one bounded follow-up call if needed, and one targeted repair round within the same review allowance. These are temporary demo settings, not permanent product limits. Do not spend more without the account owner's authorization.

**Production:** use a separate service-managed budget profile. Allow enough bounded research, extraction and repair to produce a useful, properly checked result; do not inherit the demo's one-call limit. Keep costs low through shared validated evidence, suitable models, code, templates, caching and duplicate-request prevention. Users should not need to manage API keys, tokens or repeated credit top-ups to receive an ordinary supported result. Pricing and who funds the service are separate business decisions; no free or unlimited service is promised.

Both profiles need configured cost, time and retry limits, truthful usage records and clear partial results when work cannot finish. No endless loops or silent provider replacement. Production retries may be enabled only by an explicit bounded policy that accounts for possible billing and avoids duplicate work. Determine an ordinary-use cost and latency target, then measure representative successful and incomplete cases before claiming the service is affordable. More budget cannot replace source permissions or evidence.

## R14 Failures and visibility

Users see results, evidence, review time and relevant limitations. Internal checking steps remain hidden unless an appropriate review/debug view is requested.

The backend records the run ID, exact failing step, tool/source, error, impact and next action. Distinguish a model not answering from a returned answer failing evidence checks. If only prose fails, show completed structured evidence; if a required fact cannot be checked, the case stays pending.

## R15 Permissions and payments

Purrpose does not receive, send or process money, connect payment accounts or handle payment credentials. It only provides a checked external organization link.

The running agent cannot buy services, install tools, create accounts, change policy, bypass access restrictions or send messages to organizations on its own. It may suggest a next step or draft a message. Development tools have only the separate permissions actually granted to them.

## R16 Human responsibility

The product policy owner approves scope, gates and policy changes. Account/resource holders authorize credentials and spending. Developers solve implementation problems. Authorized business reviewers handle evidence disputes and restoration after risk holds; they are not automatically the developers.

Ordinary missing documents, uncertain totals and tool failures do not need a human: return pending with specific gaps. A dispute-resolution agent first investigates conflicts. Escalate only a confirmed relevant unresolved investigation, a material high-credibility conflict still unresolved after bounded checks, restoration of an established risk hold, or a policy exception/appeal/change. A policy decision belongs to the policy owner. If no required reviewer is available, the case stays pending or held. A simple queue is enough for version 1. A simulated reviewer in a demo must be identified as simulated.

## R17 What a working demo must show

Confirmed demo completion contract: use one case to demonstrate all six items below.

1. A supporter receives full organization/case information, need evidence, a justified disclosed funding gap when calculable, and explicit unknowns. If none qualify, show pending cases honestly.
2. An organization provides public links and receives specific evidence gaps and suggested improvements; no private uploads.
3. Evidence changes agent actions: sufficient facts skip extra work; a conflict triggers targeted investigation; an unresolved gap stops without forced approval.
4. A public update triggers real memory recall, re-reading and affected-check revalidation, preserving historical versions.
5. NVIDIA, H-MEM, Nightshift and Zetaris each have separate actual request/result/consumption records for any integration claimed complete. Unconnected or simulated components are labelled and remain incomplete.
6. An on-request backend view shows plan changes, failure stages, available usage and stop reasons; default user output shows sources and relevant limitations.

Also demonstrate three different paths: sufficient evidence skips extra work; a conflict triggers targeted investigation and a revised result; an unresolved gap stops honestly at its limit. The trace must show why the actions changed.

Use real permitted information where it suffices. If the real case cannot meet every requirement, show that honestly and use labelled synthetic cases to test the full pass path. Passing synthetic tests proves mechanics, not real-world verification. Run the acceptance checks; do not call them passed merely because they are written down.

Before any public deployment, the implementing owner must also arrange actual account access, approved source coverage, operational responsibilities and the relevant security/access controls. This specification is a build guide, not proof that those exist.

## How to review this guide

Read R01–R06 first to confirm purpose and the two journeys. Then review the money, risk and update examples. Use RULE_MAP.md to locate exact technical behavior and tests. Unresolved policy questions are grouped in OPEN_DECISIONS.md. Ask the AI to explain a rule by ID rather than guessing technical terms.
