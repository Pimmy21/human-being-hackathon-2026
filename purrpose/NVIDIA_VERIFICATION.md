# NVIDIA adapter verification

24 October 2026. Local uncommitted working tree. One live request explicitly authorized by the product/account operator: synthetic text only, at most one call, 4,000 input characters, 512 output tokens, 30-second timeout, no retry. This authorization is now consumed.

## Actual result

Ran `python -m purrpose.nvidia_demo --env-file ../nvidia-setup/.env.local --output ../outputs/purrpose/nvidia-increment --allow-one-live-request --disable-thinking` once.

- Transport: real hosted NVIDIA HTTPS chat-completions request.
- Configured model: `nvidia/nemotron-3.5-lightning-30b-a3b`.
- Status: `validated_cost_used`; no automatic retry or provider substitution.
- Usage: 281 total tokens, recorded from the provider. No claim about monetary cost or remaining account credits.
- Model candidate identified synthetic treatment estimate CAD 2,000.00 with exact source/case/passage quotation.
- A narrow code validator checked the labelled quote and amount. The accepted cost was consumed in a synthetic arithmetic preview with separately structured CAD 700 raised and CAD 300 separate grant: CAD 1,000 remaining.
- Real-world case qualification: false. No veterinary authentication or real charity recommendation.

## Adapter behavior and tests

The fixed HTTPS transport refuses redirects, bounds response bytes, sanitizes errors and does not retry. Shared per-run budget reservation is lock-protected. Missing configuration blocks dispatch. Timeout/unknown usage retains the reservation; known usage is recorded even when returned output fails validation. A token reservation is planning capacity, not proof of exact billing; actual usage can exceed it and the ledger records this explicitly. This is not a durable cross-process production/session billing service.

Exact quotations establish source grounding only, not semantic truth. Only allowed candidate fields are returned, with domain validation still required. Qualification/risk status fields are rejected. No candidate is automatically written into authoritative case facts. The live proof consumes only the separately code-validated cost in its illustrative arithmetic preview. General document meaning, dates/currency, source independence and issuer correspondence remain separate obligations.

Application regression: **53 tests passed** across core, real local H-MEM, user journeys and extraction. Extraction transport tests use injected local responses and make no network request. Tests include budgets, concurrent reservations, unknown usage, malformed/truncated outputs, incorrect case/source/quotes, prompt-injection separation, invalid amounts, forbidden status fields and incorrect numeric interpretation despite a matching quote.

## Reproduction and authority

Run the local extraction tests with `python -m unittest purrpose.test_extraction -v` without credentials or network. Do not rerun the live demo without a new explicit budget/permission. It reads NVIDIA key/model only from environment or a selected local environment file; no key is printed, embedded in HTML or stored in Git.

The separate request does not prove Nightshift routing. NVIDIA via Nightshift, Zetaris current data, real public evidence retrieval and full case-workflow consumption are still incomplete. No changes were pushed or deployed.
