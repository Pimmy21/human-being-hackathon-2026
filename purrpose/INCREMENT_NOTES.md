# Historical development notes

These notes describe earlier increments and contain superseded limitations. Use README.md and HANDOFF.md for current behavior and setup.

# Purrpose core and local H-MEM increment

Offline, standard-library Python prototype. No installation, API keys, network or external inference required. Requires Python 3.10+; validated locally on the runtime recorded in VERIFICATION.md.

From the repository root:

```text
python -m unittest purrpose.test_core -v
python -m purrpose --output purrpose/artifacts
```

Open the generated `purrpose/artifacts/index.html`. The companion `runs.json` contains actual code execution traces. To run one path use `--scenario complete`, `--scenario repair`, or `--scenario exhausted`. No server is started and no payment link is provided.

## What runs

Six named code roles participate as needed: coordinator, identity/risk, rescue need, funding/channel, evaluator and dispute resolver. The coordinator holds shared case state and selects repair only for an unresolved grant-inclusion issue. The evaluator checks source-field support, case scope, type, date and explicit supersession before committing candidate facts. Code computes the remaining amount and provisional fixture gates.

All three scenarios use the same engine and fixture schema. The engine does not branch on scenario names. Input evidence determines whether the resolver runs. Source and task caps, cancellation, deadlines, duplicate attempts and stale-result checks bound execution. This is a synchronous single-writer prototype, not a concurrent scheduler.

## Expected paths

| Input evidence | Action | Result |
|---|---|---|
| Grant already known to be separate | Skip dispute resolution | Synthetic qualifying case; CAD 1,000 remaining |
| Grant inclusion unknown; permitted new page explicitly resolves it | Evaluator flags gap; coordinator revises plan; resolver reads new page; evaluator checks it | Synthetic qualifying case; CAD 1,000 remaining |
| Grant inclusion unknown; permitted new page still omits it | Targeted lookup, then stop at the repair cap | Pending evidence; remainder unknown; no human ticket |

The initial synthetic CAD 2,000 cost, CAD 700 raised and CAD 300 grant are not a real appeal. A grant already included in raised funds produces CAD 1,300 instead.

## Real H-MEM save/restart/recall/update demonstration

The separate `memory_demo` command uses the official Meterless H-MEM reference. No fake store or model embedding API is substituted. Tested reference revision: `1742dec56a66e58eef9dda2d2b865823758ca8cd` (Apache-2.0). Source: https://github.com/Meterless/Meterless/tree/1742dec56a66e58eef9dda2d2b865823758ca8cd/engines/hmem/reference . Upstream code is not vendored in this repository. Point `--reference` at your authorized local checkout's `engines/hmem/reference/src/index.ts`. Requires Node 24 with TypeScript transform support. Do not download/install a runtime merely to open the report.

Run these as separate commands, replacing `/absolute/path/to/index.ts` with that configured file:

```text
python -m purrpose.memory_demo --reference /absolute/path/to/index.ts --state purrpose/.state/hmem --output purrpose/artifacts/memory --workspace fresh-demo --phase first
python -m purrpose.memory_demo --reference /absolute/path/to/index.ts --state purrpose/.state/hmem --output purrpose/artifacts/memory --workspace fresh-demo --phase update
```

Use the same workspace for the two phases and a new unused workspace for an independent demonstration. No deletion/reset is needed. Scope is a development/test namespace, not a donor profile. Each bridge operation starts a new Node process; the commands also restart the Python application between phases. `first.json`, `update.json` and `index.html` record the actual runs. Dates 24/25 October 2026 are a frozen synthetic scenario, not two actual calendar days of monitoring.

The first review remembers the unresolved grant-inclusion issue. The second recalls it, checks fingerprints and current dates, reuses six unchanged validated fields, and reads the new funding source. Expected remaining amount: CAD 1,000. The old snapshot remains available. Exact case/workspace separation prevents cross-scope recall. Confidence/relevance scores never determine truth or qualification. Retrieval deliberately includes up to 500 scoped snapshots using threshold 0; it uses H-MEM's query API, then selects the latest stored snapshot, not the highest score. The demo rejects larger stores and requires sequential access; no production concurrency, retention or backup claim is made.

For real memory integration tests, set `PURRPOSE_HMEM_REFERENCE` to the absolute reference file and run:

```text
python -m unittest purrpose.test_core purrpose.test_memory -v
```

Without that environment setting memory integration tests are explicitly skipped, not marked as tested. No live sources, Nightshift or paid inference are used. Missing reference/runtime is an explicit failure; there is no fallback pretending that a JSON file alone is H-MEM.

## What this does not prove

### User-journey increment

Run `python -m purrpose.journey_demo --scenario exhausted --city Ottawa --output purrpose/artifacts/journeys` for supporter and organization outputs. Add the same `--reference`, `--state` and `--workspace` options as the memory demo to enable real H-MEM. The module uses mapped synthetic pages only; the displayed `example.invalid` link is not fetched. Arbitrary URLs, private hosts and uploaded documents are unsupported. A link does not establish representation authority.

The supporter contract asks city when unspecified, filters actual case city, offers expansion without silently broadening, sorts neutrally and separates qualified/pending/fully-funded outcomes. The organization contract returns per-field/per-gate gaps, reasons, source suggestions and recheck actions. Default output omits internal traces. Developer records are separate JSON files. These are callable backend/CLI entry points and a readable saved report, not a deployed interactive web application or a natural-language intent model.

Run `python -m unittest purrpose.test_journeys -v` for the journey checks. This increment also connects the journey service to optional real H-MEM; it does not add live web retrieval or external inference.

- No live/model-driven agent planning, document reading, registry or medical authenticity checks.
- The default offline command does not use H-MEM. Only the separate memory workflow above has actual H-MEM evidence. One separately authorized NVIDIA candidate-extraction/arithmetic-preview request passed; ordinary fixture journeys do not call it. Nightshift and Zetaris remain unconnected in this new application. Configuration files elsewhere do not establish connectivity here.
- No complete production six-gate implementation. Identity, risk completion, medical linkage and donation-channel ownership are prestructured synthetic assertions. Their real checks remain unimplemented.
- Only grant-inclusion dispute repair is implemented. Other unresolved issues safely remain pending; the full exceptional human queue and restoration workflow are not implemented.
- Memory mode persists/recalls snapshots and demonstrates a synthetic funding update; basic city-filtered discovery and organization gap outputs now run. General durable scheduling, real public update retrieval, preference persistence across UI sessions, regional source configuration, full freshness semantics and concurrency remain incomplete.
- No claim that all 127 guidance acceptance requirements passed. See VERIFICATION.md for the tested subset.

Use the full specification under `first draft/guidance` for the target behavior. The earlier wireframe remains unchanged. This runnable increment is separate from it and from the older annual-financial-report prototype.

Actual memory results and limits: [H-MEM verification](MEMORY_VERIFICATION.md).


## Bounded NVIDIA candidate extraction

`extraction.py` contains a fixed hosted NVIDIA transport, shared per-run resource limits and strict source-grounded candidate schema. It has no implicit credentials, default model, automatic retry or automatic case-approval authority. Call it only when structured reading/cache cannot complete the task and a live budget is authorized. Domain validation is mandatory: an exact quote alone does not establish that the proposed amount means what the model says.

`python -m unittest purrpose.test_extraction -v` runs offline adapter tests. `nvidia_demo.py` is an explicit single-request live integration probe, not part of the ordinary offline journey command. See [actual NVIDIA verification](NVIDIA_VERIFICATION.md) before any live use; the existing one-request permission has been used. The proof consumed one code-validated synthetic cost in an arithmetic preview, not a real-case recommendation. Nightshift and Zetaris remain separate integration gates.


## Recorded NVIDIA response into the case workflow

`python -m purrpose.replay_demo --output purrpose/artifacts/replay` replays the sanitized capture in `fixtures/nvidia-capture.json`. No key/network is needed. Optional `--reference`, `--state` and `--workspace` enable real local H-MEM. The recorded 281-token usage is historical; this command makes zero new inference calls.

The adapter removes the prefilled fixture cost, compares current source fingerprints/version/case, rechecks the exact quote, and independently parses the labelled CAD estimate. Only a matching amount supplies the core cost field. The six gates, arithmetic and supporter output run now, and source/provenance survives memory persistence. A stale/invalid capture leaves the cost unknown; old memory cannot restore it. An accepted cost cannot bypass medical linkage, risk or funding requirements. This narrow format validator is not general veterinary document authentication.

Run `python -m unittest purrpose.test_replay -v` for replay checks. Set `PURRPOSE_HMEM_REFERENCE` for the test involving actual memory restart/reuse. The saved report clearly distinguishes replay from live inference and synthetic qualification from real-world verification.


## Read-only Zetaris identity lookup

`zetaris.py` supports local JDBC preflight and a bounded real read from the existing approved deployment-specific historical identity table. It does not create tables or accept arbitrary SQL. See [actual result and safe setup](ZETARIS_VERIFICATION.md). Another machine needs its own configured .env.local, driver, JVM and Python dependencies; previous success is not portable account access.

The returned real organization is shown in a separate historical identity view, not merged into the fictional Maple case. The source is a 2024 filing and cannot pass current registration or medical-need checks. Current source coverage is still incomplete. Use `python -m unittest purrpose.test_zetaris -v` for offline adapter tests.


## Retained historical reviews

`history.py` answers from stored review summaries, not a recalculation using current evidence. It compares explicit timezone-aware cutoffs against the actual H-MEM record creation timestamp. A source/review date is a separate field and never substitutes for when the system learned it. Older records lacking saved summaries remain explicitly partial; no record means unavailable. Original source URLs are not rechecked by a historical answer, and current qualification is not implied.

Run `python -m purrpose.history_demo --reference /configured/index.ts --state purrpose/.state/hmem --workspace fresh-history --output purrpose/artifacts/history` to demonstrate a first unknown amount, a later resolved amount and an unavailable earlier cutoff. Both reviews execute now; source dates are simulated. No web/model requests are made.

To query an existing workspace rather than create demo reviews: `python -m purrpose.history --reference /configured/index.ts --state purrpose/.state/hmem --workspace fresh-history --case-id SYN-MAPLE --cutoff 2026-10-24T14:00:00-04:00`. Omit cutoff for the latest retained review. Use that workspace's actual recorded timestamps. H-MEM query access updates its local access/audit records, but does not rewrite the original creation time or create a new review.

`python -m unittest purrpose.test_history -v` covers cutoff behavior; configure `PURRPOSE_HMEM_REFERENCE` to include the actual persistence/query test.


## Public update intake

`updates.py` accepts notifications only for explicitly mapped sources. The backend reader is supplied by application configuration, never notification content. Current implementation reads synthetic fixture records only; it does not fetch URLs, install tools or watch websites in the background. No representative authority is inferred from a submitted link.

An ordinary notice starts as a lead. Only a successful scoped source read establishes an observed change. A failed notice read does not silently remove qualification or return the old review as newly verified. An explicit request for current information re-reads its source; a required-source failure blocks current qualification. Changed required evidence marks the case update-awaiting-review before affected checks. H-MEM can reuse only unchanged, still-valid facts; unknown impact conservatively reopens all six gates. Optional material failure is disclosed independently of required gates. The same idempotency key returns its recorded task result, explicitly labelled as a replay rather than a fresh result; different inputs cannot reuse that key.

Run `python -m purrpose.update_demo --output purrpose/artifacts/updates`, optionally adding configured `--reference`, `--state` and `--workspace` to use real H-MEM. It shows baseline CAD 1,000; an observed funding update reducing the gap to CAD 500; duplicate-request reuse; and an explicit latest-source outage becoming pending. `python -m unittest purrpose.test_updates -v` runs focused tests; configure PURRPOSE_HMEM_REFERENCE for the real memory test.

The service is synchronous, with process-local idempotency and state. The fixture reader returns immediately; any future network reader must implement its own approved time/size/access limits before use. Production concurrent scheduling, durable intake queues, arbitrary public-source onboarding and continuous monitoring are not implemented.


## Functional local browser interface

Run `python -m purrpose.server --port 8766` from the repository root, then open http://127.0.0.1:8766. No installation, cloud key or inference is needed for fixture mode. For actual H-MEM, add `--reference /configured/index.ts --state purrpose/.state/hmem --workspace local-demo`. The Node requirement and explicit upstream reference setup described above still apply. The startup message prints the actual local URL. Stop the foreground server with Ctrl+C.

Try: Check cases → Check our information → Demo controls / Clarify separate grant → Check cases again → History. More-funds/fully-funded/source-outage controls modify only simulated public evidence. The history cutoff must use an actual saved system timestamp with timezone, not the simulated source date. Debug details appear only after pressing Show internal execution. No API endpoint triggers paid inference, real web fetching, SQL or resource creation.

Only fixed static assets and validated application operations are served. Binding is restricted to 127.0.0.1; Host is checked, write requests require a local custom header and reject foreign origins; JSON bodies are bounded. This is a serial local demo for a single operator, not a production authentication or multi-user authorization system. Do not expose it publicly. Source state/idempotency are process-local; restarting restores baseline fixtures while configured H-MEM review history remains. There is no private upload, donation processing, arbitrary file/SQL access or background monitor.

Run `python -m unittest purrpose.test_server -v` for local HTTP tests. Full current test discovery: `python -m unittest discover -s purrpose -t . -q`. Set PURRPOSE_HMEM_REFERENCE to include actual memory tests; absent configuration results in explicit skips. See [browser and API verification](WEB_VERIFICATION.md).

Basic chat is available in the local page's Talk to Purrpose view. It currently uses bounded English/Chinese intent matching and current structured evidence, with no new cloud calls. See CONVERSATION_VERIFICATION.md for supported requests and limitations. It is not yet general model-powered conversation.

For attaching a separate design, start with FRONTEND_INTEGRATION.md and web/api-client.js. The existing functional UI already exercises this client; no public deployment or cross-origin hosting is configured.

For a short mentor/coach demonstration and honest integration status, use COACH_DEMO_RUNBOOK.md. It includes exact UI steps and the known fresh-server requirement.
