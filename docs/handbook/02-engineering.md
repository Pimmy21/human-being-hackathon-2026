# Backend Architecture and Data Contract

## 1. Implementation baseline

This chapter specifies the next application; its routes and commands do not exist merely because they are listed here. Check the repository first. Keep a short `docs/runbook.md` with commands that have actually been tested after the backend is created.

Recommended starting structure: a small Python backend, a React and TypeScript frontend, a local SQLite or JSON store for curated cases, and the official Meterless H-MEM reference behind a narrow adapter. FastAPI is a reasonable Python API layer. This is a reversible implementation default, not a requirement to rewrite functioning work. If the team already has a simpler working stack, document the decision and preserve the interfaces below.

Use one backend orchestrator. Do not create an elaborate multi-agent system for the first case. Do not build autonomous browsing, queues or multiple cloud services before the case workflow works. A deterministic checklist can choose the next evidence action and ask the model for bounded assistance.

Suggested folders once implementation starts:

```text
backend/
  api/                  request validation and response shaping
  domain/               case rules and funding calculations
  adapters/             zetaris, hmem, nvidia, meterless
  sources/              approved source retrieval and parsing
  prompts/              versioned extraction and explanation instructions
  storage/              case versions and run records
frontend/
  components/           case, evidence, funding and review components
fixtures/
  synthetic/            explicitly invented, shareable test cases
  public/               permitted public excerpts and provenance
tests/
  unit/
  integration/
  acceptance/
docs/
  runbook.md            actual setup and launch commands
  decisions/            short records of implementation choices
  runs/                 sanitized verification results
```

Do not commit database files containing private state. Do not call a proposed command “tested” until someone has run it from a fresh clone.

## 2. End to end sequence

1. Validate the requested curated `case_id`, demo user and run mode. No arbitrary URL fetching in the MVP.
2. Load the case manifest and source permissions. Reject missing identifiers or unsupported case scope.
3. Recall this user's relevant case history from H-MEM. Empty memory is a normal first visit, not a failure.
4. Retrieve approved public evidence or explicitly selected fixture snapshots. Record every source outcome separately.
5. Query Zetaris for the existing organization identity record if live mode requests it. Keep the filing period.
6. Extract candidate claims from readable text. Preserve values, units and page locations. For the first case, human-curated structured fields are acceptable if labelled; do not claim autonomous extraction.
7. Validate the schema and source IDs. Resolve organization/case linkage. Unresolved linkage prevents combined case conclusions.
8. Run deterministic evidence, currency, time, overlap and funding rules.
9. Choose the next useful action from the allowed checklist: obtain missing cost details, clarify funding inclusion, inspect an identity conflict or explain known facts. Do not invoke unlimited loops.
10. Ask the selected provider for a concise explanation using only the validated bundle and retrieved context.
11. Validate output structure, citation IDs, numeric values and scope. Hold an unsupported draft and show the deterministic evidence summary instead.
12. Persist the sourced case version and H-MEM records. Record source failures and unresolved questions too. Return the user-facing result plus a sanitized run trace.

Save only validated source claims as evidence. A model's summary is a derived artifact with its own label, not a new independent source. Persisting it must not make its claims more credible on recall.

## 3. Entities and required fields

| Entity | Required fields |
|---|---|
| Organization | Stable ID, name, known registry ID or null, identity evidence IDs, filing period |
| Case | Stable ID, organization ID, animal/case alias, request summary, location, scenario type, manifest version |
| Evidence | ID, origin group, source type, URL or permitted file reference, publisher, captured time, source date or null, excerpt, document page or section, hash where relevant, permission note |
| Claim | ID, case ID, field, typed value, unit/currency as applicable, evidence IDs, evidence label, as-of time, reviewer state |
| Funding item | ID, case ID, kind, amount in minor units or null, currency, timestamp, source IDs, received/committed status, overlap relationship and allocation scope |
| Case version | ID, prior version ID or null, creation time, claims, funding result, unresolved questions, source states |
| Run | ID, case/version IDs, mode, provider/model, source statuses, queries/tool calls, memory IDs, failures, usage, publication state, duration |

Use UTC ISO 8601 timestamps in data. Display a timezone in the interface. Distinguish `captured_at` (we read it) from `source_date` (it was published) and `amount_as_of` (the reported balance date).

Origin groups describe the actual source of a claim. Two websites copying the rescue's statement use the same origin group. An audit opinion has its own author and limited scope; it is not proof that a particular fundraiser is authentic.

## 4. Illustrative response contract

The following is a **synthetic API example**, not an existing endpoint or a real case:

```json
{
  "case_id": "synthetic-cat-001",
  "scenario_type": "synthetic",
  "version_id": "v1",
  "mode": "replay",
  "currency": "CAD",
  "cost_estimate_minor": 200000,
  "reported_raised_minor": 70000,
  "grant_minor": 30000,
  "grant_included_in_raised": null,
  "remaining_minor": null,
  "funding_status": "needs_clarification",
  "questions": ["Is the grant already included in the amount raised?"],
  "claims": [
    {
      "id": "COST1",
      "field": "estimated_treatment_cost",
      "value_minor": 200000,
      "evidence_ids": ["SYN-ESTIMATE1"],
      "label": "supported_by_cited_evidence"
    }
  ],
  "sources": [
    {"id": "SYN-ESTIMATE1", "scenario_type": "synthetic", "origin_group": "synthetic-vet", "source_type": "fixture", "source_date": "2026-10-23", "permission_note": "Created for testing"}
  ],
  "explanation_status": "not_requested",
  "provider_status": "offline",
  "memory_status": "empty_first_visit"
}
```

Validate references server-side. The frontend must not accept a citation just because text contains square brackets. The synthetic label remains visible even when the example is combined with a real government record.

## 5. Proposed HTTP interface

| Route | Behavior | Important boundary |
|---|---|---|
| `GET /health` | Backend process status | Does not prove providers are available |
| `GET /api/cases` | Curated case summaries with scenario labels | No popularity or trust ranking |
| `GET /api/cases/{id}` | Latest source-linked record | Unknown IDs return 404 |
| `POST /api/cases/{id}/review` | Start explicit live or replay review | No arbitrary SQL or URLs from the client |
| `GET /api/runs/{id}` | Progress and final result | Expose sanitized trace only |
| `POST /api/cases/{id}/questions` | Answer one bounded follow-up from evidence | Return unsupported/unknown when appropriate |
| `POST /api/cases/{id}/updates` | Add a selected approved update fixture | Preserve original version; no public file uploads yet |
| `GET /api/providers/status` | Per-provider online/unauthorized/offline | Never return keys or auth headers |

Long-running reviews should return a run ID and allow polling. Duplicate submissions with the same idempotency key should not launch additional paid requests. Disable a second “Check” while a request is in progress. Cancellation prevents new calls and labels any still-running external call honestly.

These routes are a proposed contract. The backend owner can simplify their implementation without changing the user-facing behavior. Keep frontend fixtures aligned with the same schema. Document finalized routes and example requests in `docs/runbook.md` after implementation.

## 6. Source intake and permissions

Start with an allowlisted case manifest. For each URL: verify permission and access terms, record expected host and document type, cap download size, enforce timeouts, and reject redirects to unapproved or private network hosts. Do not send cookies or authentication to a redirected host. Never bypass login, robots restrictions or social media access controls.

Server-side arbitrary URL input can expose internal services. Keep public evidence retrieval separate from the explicitly configured loopback model endpoint. Do not reuse the provider's local-network exception for document fetching.

Render source text as escaped text, not raw HTML. Limit PDFs and text to relevant excerpts. Downloaded content must not trigger code execution. Do not upload a private veterinary document to a model provider without permission; a public URL does not remove personal-information concerns. Redact donor names, addresses, phone numbers, signatures and payment details before sharing.

If a safe real case is unavailable, prepare synthetic fixtures and log the data-access blocker. This supports engineering progress, not a claim that current real-world need has been verified.

## 7. Memory and persistence

H-MEM stores sourced claims and unresolved questions with case and user scope, not a permanent “trustworthy” label. Store evidence IDs, source URLs, timestamps, fact versus derived-summary type, version links and reviewer state. Use `source`, `provenance`, `chatId` or equivalent scope, and `derivedFrom`/version relationships.

Retrieve before answering. The retrieved values must actually influence the explanation or update comparison; a hidden unused memory write does not count. Test a restart and a second demo user. Use separate state directories per alias as well as scope filtering. This is a local demo boundary, not production authentication.

The reference's confidence value is not an organization trust score. Its relevance ranking is not proof of truth. Keep the evidence store authoritative, and identify a correction explicitly so an old recalled statement cannot override a newer reviewed claim silently.

## 8. Publication checks and model budgets

Require schema-valid output, existing citation IDs, source-supported assertions, no invented amounts, no new current-status guarantees, and no private data. Calculate the funding result before inference and reject model numerals that disagree. A citation's existence does not prove that it supports a sentence; the first demo requires human review of claim-to-source mapping.

One generation call per user action is the starting budget. No automatic best-of-eight runs, paid retries, or multi-provider fallback. For early adapter development, retain the existing NVIDIA starter's input and output caps; the previous call used a 750 output-token limit. Log usage when provided; unknown usage is null, not zero. Do not invent monetary cost from token count.

If explanation fails, display the structured evidence and questions with “AI explanation unavailable” or “Draft held for review.” A usable evidence result is distinct from completing the model/sponsor acceptance gate. Never claim a successful model integration when the tool did not answer.

## 9. Error and trace contract

Use stable error codes such as `SOURCE_UNAVAILABLE`, `IDENTITY_MISMATCH`, `FUNDING_OVERLAP_UNKNOWN`, `PROVIDER_UNAUTHORIZED`, `MODEL_OUTPUT_HELD`, `MEMORY_UNAVAILABLE` and `INVALID_CASE`.

The donor sees the useful consequence and next step, not a Java stack trace. Developers receive a sanitized run ID, failing stage, status code and elapsed time. Logs exclude full credentials, private endpoints, bearer tokens and raw private documents. Preserve a failed run record instead of overwriting it with the next success.
