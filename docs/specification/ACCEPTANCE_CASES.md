# Acceptance Contract

**Requirements, not test results.** Implement these as unit, integration or acceptance tests appropriate to their layer. Use frozen clocks and explicit source/provider fixtures. A mock pass is not evidence of external access. Record actual command/steps, commit, mode and result when execution becomes available.

## 1. Overall completion levels

- **Specification review-ready:** confirmed rules are traceable, proposed defaults are labelled, contradictions identified, examples coherent and unresolved decisions visible.
- **Fixture workflow-ready:** the four minimum functions run with clear synthetic labels, real H-MEM use and deterministic tests; no claim of real-case verification.
- **Integration-ready per component:** configured actual request, valid result consumed by the app, trace and failure classification for NVIDIA, H-MEM, Nightshift and Zetaris separately.
- **Real-case qualification-ready:** every applicable gate actually passes under a tested/approved region source profile; no untested mandatory risk channel remains hidden.
- **Presentation-ready:** runnable workflow, disclosed limitations, checked tool evidence and the current organizer's submission requirements met or explicitly incomplete. Do not silently weaken any gate.

Front-end visual styling is excluded from this specification review. Basic user interactions and readable outputs remain required for a runnable demonstration.

## Portable specification checks

| ID | Setup/action | Expected result |
|---|---|---|
| P01 | New implementer has no original conversation or team context | Required purpose, roles, workflow and dependencies are defined in the package |
| P02 | No deployment configuration exists | Assistant asks for missing region/workspace/owners/access/budget; does not assume a prior machine or account |
| P03 | Different region selected | Same shared rules, region-specific validated channels; all user messages and filters use configured region |
| P04 | Person and assistant compare a rule | R01–R17 map to matching human explanation, specification section and acceptance behavior; conflicts are not silently resolved |

## 2. Product, scope and discovery

Named Ontario locations below belong to the reference test profile. Run equivalent parameterized cases for the selected deployment region. Do not treat Ontario as an implied universal target.

| ID | Setup/action | Expected result |
|---|---|---|
| S01 | Requester selects Ontario reference profile | Record target configuration; no assumptions about requester/developer residence |
| S02 | Requester selects another country/province | Consistent configured region throughout workflow; no qualified recommendation until required channels are approved/tested |
| S03 | Supporter asks broadly to help cats | Ask city preference once; no required amount/name/contact |
| S04 | Supporter says no preference | Search connected Ontario collection only |
| S05 | No city match | Explain and ask before expanding to another city |
| S06 | Toronto headquarters, Ottawa treatment | Ottawa case; not a Toronto match |
| S07 | Case city unknown, Ontario otherwise supported | Ontario-wide pending only; unknown city last; no headquarters substitution |
| S08 | Multiple eligible fixtures | City → full organization name → case name A–Z ignoring case; deterministic ties |
| S09 | Mixed qualified/pending cases | Separate lists; no follower-count or trust-score ordering |
| S10 | Individual fundraiser or out-of-scope purpose | Scope explanation, optional unverified channels and supported-scope offer; no forced qualification |
| S11 | Organization lacks registration | MVP 1 pending; future alternative-identity policy not silently activated |

## 3. Six gates and funding

| ID | Setup/action | Expected result |
|---|---|---|
| G01 | All six synthetic gates pass with positive remainder | Synthetic qualified result, full required fields, no real-world verification claim |
| G02 | Any mandatory gate incomplete | Not qualified; specific pending/hold reason |
| G03 | Name resembles another registry organization | No identity match without supporting identifiers |
| G04 | Historical registration record only | No current-registration guarantee; enforce required current check |
| G05 | Only self-description/photo/video/comments | Medical-material gate pending |
| G06 | Redacted medical material retains required fields | Can be evaluated; not rejected merely for appropriate redaction |
| G07 | Medical case identifier cannot be linked | Case gate pending even if cost is readable |
| G08 | Estimate 200000, raised 70000, separate grant 30000 | Remaining 100000 minor CAD units; disclosure qualification present |
| G09 | Same amounts, grant included | Remaining 130000; no double subtraction |
| G10 | Grant inclusion unknown | Remaining null; asks relevant clarification |
| G11 | Amount unknown | Null, not zero |
| G12 | Duplicate invoice/estimate or funding record | No double-counted cost/funding |
| G13 | Grant pledged, not received | Distinguish commitment; do not silently treat as received money |
| G14 | Cost/funds currencies differ | No invented rate/exact remainder |
| G15 | Funds equal/exceed eligible cost | Remaining zero, excess separately recorded where applicable; no positive-gap recommendation or misconduct inference |
| G16 | Level 1 disclosure otherwise sufficient | Eligible under agreed level; adjacent disclaimer that all funding is not independently confirmed |
| G17 | Complete funding scope not sufficiently disclosed | Unknown/qualified calculation as appropriate; not an exact current gap claim |
| G18 | External donation channel ownership unclear | Gate fails; no checked donation action |
| G19 | Any request to collect money/process account/payment | Refuse unsupported action; checked external link only |
| G20 | One case passes for an organization | Other cases unchanged; no blanket certification |

## 4. Risk and channel states

| ID | Setup/action | Expected result |
|---|---|---|
| R01 | Applicable channel successfully checked with exact identity, no record | Completed, scoped no-record statement; not risk-free |
| R02 | Applicable channel timeout/empty error page | Incomplete, not no-record or not-applicable |
| R03 | Non-charitable entity, CRA charity channel inapplicable under approved matrix | Documented not-applicable; identity still requires the applicable registry |
| R04 | Identity query completes with no correct match | Identity not established; not proof of no registration |
| R05 | Formal relevant fund-misuse finding with confirmed identity | Suspend qualification; sourced scope; authorized business review required for restoration |
| R06 | Credible ongoing investigation without final finding | Automatically verify identity/procedural scope first; confirmed relevant unresolved investigation triggers pending/business review; no guilt statement |
| R07 | Generic unverified negative comment | Lead screening, no automatic suspension/public accusation |
| R08 | Revocation for administrative filing reason | Do not label corruption; determine applicable identity/risk effect under policy |
| R09 | Subsequent reversal/correction found | Preserve earlier record and latest procedural status; business review where required |
| R10 | Risk profile unapproved/unconfigured | Required gate incomplete; cannot silently disable it |
| R11 | Reviewer absent | Remains pending; no fabricated approval |
| R12 | Simulated demo reviewer action | Simulation labelled; no actual business authority inferred |
| R13 | Organization apology/explanation alone after a risk hold | Hold remains; no automatic restoration |
| R14 | Checkable reversal/mistaken match/lifted restriction and authorized review | Record decision; recheck all six gates; preserve old risk record |
| R15 | Inactive/cancelled/dissolved or unclear status | No qualified identity pass; exact reason shown |
| R16 | Charitable status revoked but corporate identity still valid | Distinguish statuses; no false charitable/tax-receipt claim; relevant review required |

## 5. Freshness, updates, caches and history

| ID | Setup/action | Expected result |
|---|---|---|
| H01 | Funding older than configured threshold | Pending refresh, not current gap |
| H02 | Medical material has explicit validity | Use stated validity; no blind default-age substitution |
| H03 | No explicit medical validity | Apply configured default 30-day age with documented boundary semantics |
| H04 | Valid cached review, same policy, no known relevant update | Reuse with true review timestamp, not newly checked claim |
| H05 | User requests current refresh within cache interval | Attempt re-read; bypass cached review |
| H06 | Screened relevant public update while old data still within freshness | Update awaiting review; recheck affected gates immediately, do not wait 24h |
| H07 | Arbitrary comment says update without credible specifics | Screen lead before status change |
| H08 | No request/notification after interval | No false promise of background polling; refresh triggered on next access |
| H09 | Critical new source fails | Keep pending; preserve dated old result without calling it current |
| H10 | Optional source fails, all required checks complete | Core result may remain; disclose optional limitation |
| H11 | Impact of changed source cannot be determined | Recheck all gates; do not assume optional |
| H12 | Unchanged material extraction cache hit | No model call; still evaluate current freshness/policy/other facts |
| H13 | Model/prompt/schema changes | Validate cache compatibility or re-extract within budget; no blind reuse |
| H14 | Different case/user scope | No unintended memory/cache cross-scope leak |
| H15 | Page changes but actual modification date unknown | Captured/discovered time separate from publication time |
| H16 | New validated cost/funding version | Original retained; new review reason/version recorded |
| H17 | Question about prior cutoff | Use only system-known records by that cutoff, not later-discovered evidence |
| H18 | No past record retained | Explicit unavailable answer, no fabricated historical review |
| H19 | Relevant old formal risk omitted from new website | Do not erase still-applicable risk automatically |
| H20 | Precisely timestamped evidence at the age limit / just beyond | Valid at equality; expired beyond |
| H21 | Date-only expiration / future-dated source | Valid through local expiration date; future source date needs clarification |

## 6. Models, tools and budgets

| ID | Setup/action | Expected result |
|---|---|---|
| M01 | Structured inputs suffice | No model call for arithmetic/sorting/template result |
| M02 | Low-credit demo: new material needs inference | At most one configured extraction call for review; record unprocessed input if bounds reached |
| M03 | Same question and evidence/policy version repeated | Reuse eligible answer; no duplicate inference |
| M04 | Model returns unsupported dates/amounts/citation IDs | Candidate rejected/held; no authoritative write |
| M05 | Model returns qualified true | Ignored as authority; code computes gate result |
| M06 | Provider returns text but explanation fails checks | Transport success separate from held publication; structured result only if necessary checks completed |
| M07 | Critical extraction unreadable/uncertain | Distinct failure category; pending if no other validated evidence resolves it |
| M08 | Timeout/429/unauthorized | No automatic retry/substitution; correct error stage/category |
| M09 | Duplicate concurrent click with same idempotency key | One task and no duplicate paid generation |
| M10 | Configured budget absent/exhausted | Block new model calls, preserve evidence and uncompleted-step record |
| M11 | Timed-out request with uncertain usage | Usage null/uncertain; no zero-cost assumption or automatic release/retry |
| M12 | Step/run deadline reached | No indefinite waiting; preserve partial results; stop scheduling new calls |
| M13 | Explicit retry after source/policy changes | Revalidate affected successful steps before assembling result |
| M14 | Source contains instructions to change policy/exfiltrate key | Treat as data; tool permissions and policy unchanged |
| M15 | Unsupported video modality on configured text model | Capability gap, not fabricated video understanding |
| M16 | Wrong Nightshift token | Unauthorized, not offline |
| M17 | Runtime health succeeds but model listing/inference fails | Do not mark provider integration passed |
| M18 | Direct NVIDIA call succeeds | Do not count it as a Nightshift call |
| M19 | Actual H-MEM save/restart/recall/use | Retrieval trace demonstrates previous unresolved question affects new review |
| M20 | Different alias reads memory | No first alias's private scoped state returned |
| M21 | Zetaris old dataset/new upstream 504 | Historical information labelled; current required check incomplete; no infrastructure reset |
| M22 | Adapter mock passes | Label mock evidence only; live gate remains untested |
| M23 | NVIDIA/H-MEM/Nightshift/Zetaris success independently | Each actual result consumed in useful feature with own run record |

## 7. Organization output, permissions and observability

| ID | Setup/action | Expected result |
|---|---|---|
| O01 | Organization/person supplies public link | No assumed representative authority; same evidence rules |
| O02 | User tries private file upload | Unsupported MVP flow; no demand to expose sensitive content |
| O03 | Material missing/expired/conflicting | Concrete gap, why it matters, suggested information channel and recheck step |
| O04 | Organization updates its own public page | Re-read authorized source; no Purrpose document-hosting workflow |
| O05 | User only views current result | Sources/limits/review time accessible; no internal step trace by default |
| O06 | Authorized demo debug request | Exact step/tool/status/error/impact shown with sanitized trace |
| O07 | Model extraction timeout versus explanation hold | Different backend states and correct gate impact |
| O08 | Organization gives publication URL to restricted/private-network host | Reject unsafe fetch/redirect; do not borrow local provider exception |
| O09 | Runtime wants to install tool/contact clinic/buy access | Unsupported autonomous action; record gap/suggestion only |
| O10 | Secret handling | No keys/auth headers in frontend, public logs, screenshots, fixtures or source control |
| O11 | Simulated/latest/historical mixture | Scenario/mode labels remain visible; no synthetic case attributed to real organization |

## 8. Minimum recorded demonstration

Use one case through discovery, organization gap list and controlled public update. Include the evidence-driven paths A01–A16 below; the old wireframe alone does not pass them. Include at least one missing-data case and an example of a fully passing synthetic fixture. Show real H-MEM persistence and useful retrieval. Open the backend trace only as an explicit presenter action.

For each external integration claimed complete, attach timestamp, commit, mode, request category, useful returned result, consumption point, error handling and available usage. Do not attach tokens/raw private source data. The real-case risk-channel blocker is explicitly not solved by synthetic checks.

## 9. Completion report template

```text
Commit and platform:
Scenario and run mode:
Implemented operations:
Commands/manual steps actually run:
Passed checks and evidence locations:
Failed/unrun checks:
Real provider/data calls and usage if available:
Mocked/replayed/synthetic components:
Remaining source permissions, credentials or policy decisions:
Fresh-start and restart steps:
Next owner/action:
```

No completion claim until both functional behavior and truthful integration reporting are reviewed. An unresolved required channel can block real qualification while fixture engineering remains productive.

## 10. Evidence-driven agent behavior

All rows below are unexecuted requirements. Use deterministic fixtures to assert routing and a separately labelled live test for any claim of real model-driven delegation. Compare actual task/issue traces, not role names in prose.

| ID | Setup/action | Expected result |
|---|---|---|
| A01 | All required facts already validated and fresh | Reuse results; no unnecessary research/dispute/model task; six code gates still applied |
| A02 | New case has several independent unresolved checks | Coordinator delegates only applicable specialist tasks with shared case/version, tool permissions and resource allocations; concurrency cannot exceed cap |
| A03 | Grant inclusion unknown; approved new disclosure explicitly excludes grant from raised total | Evaluator creates inclusion issue; coordinator revises plan; resolver/funding role reads new source; evaluator validates it; code returns CAD 1,000 with citations |
| A04 | Low-credit demo: same ambiguity but no permitted resolving evidence | One bounded targeted repair at most; remainder null; pending_evidence with useful gap/channel; no human ticket or forced amount |
| A05 | Funding-only public update, other checks still valid | Recall state; reopen dependent funding/evaluation/calculation tasks; no redundant identity/medical provider calls |
| A06 | Proposed medical amount cites unrelated cat's invoice | Evaluator rejects case linkage; precise repair task if available; no gate pass from fluent model output |
| A07 | Adverse name collision resolved before a risk match was established | Resolver obtains incompatible official identifiers; evaluator excludes wrong-entity record with reason; other gates still required; no human ticket |
| A08 | Established risk hold later appears to be mistaken or formally reversed | Resolver prepares checkable basis; cannot clear hold; authorized business review and six current gates required |
| A09 | Conflicting high-credibility eligibility evidence remains after permitted bounded investigation | pending_human packet includes trigger, sources, attempts, affected gates and decision requested; absent reviewer keeps pending |
| A10 | Missing invoice, unavailable credentials, exhausted budget, or unsupported generic accusation | Appropriate pending/blocked/lead state; do not invent a human evidence-review requirement for ordinary gaps |
| A11 | Roles propose same action on unchanged source/state | Attempt ledger prevents repeated ineffective work; terminal reason states no useful permitted action |
| A12 | Low-credit demo: repair needs a second extraction under its one-call cap | Block additional paid extraction; role changes and follow-up allowances cannot reset the review budget |
| A13 | Concurrent roles reserve resources or return after a relevant update | Atomic budget reservation; no overspend race; stale-dependent result rejected/revalidated; no newer-state overwrite |
| A14 | Cancellation/deadline occurs during specialist work | Stop dispatch; late return cannot publish or clear hold; preserve uncertain billing and partial state |
| A15 | Provider 429/timeout or mandatory source outage | No automatic paid retry/provider switch; alternative permitted source only within caps and approved equivalence; named mandatory channel failure not hidden |
| A16 | Compare sufficient, repaired and exhausted scenarios | Traces contain genuinely different selected/skipped tasks, issue-driven plan changes and terminal reasons; no fixed all-role sequence; disclose fixture vs model decisions |

## 11. Production efficiency profile

| ID | Setup/action | Expected result |
|---|---|---|
| E01 | Production selected with missing operational limits | Block external dispatch; request service configuration; do not inherit demo numerical caps |
| E02 | Production allows multiple bounded extractions and repair needs another call | May proceed within shared authorized limits; demo one-call restriction is not applied |
| E03 | Ordinary supported user journey | No demand for provider API keys or token configuration; pricing/funding disclosed separately when established |
| E04 | Representative complete/missing/conflicting/update workloads | Measure useful-result cost, quality, latency and cache reuse against owner-defined targets; no unsupported affordability claim |
| E05 | Production transient-error retry enabled | Only eligible configured retries within caps/deadlines, uncertain billing retained, no duplicate work or silent provider switch |
