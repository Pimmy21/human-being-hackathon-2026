# Local browser and API verification

> **Update 25 Oct 2026:** with `PURRPOSE_MODEL_PROVIDER` configured, every ordinary chat message is now classified by an explicitly configured model (direct NVIDIA tested; Meterless route untested) and validated before code writes the reply. Without configuration the behaviour below is unchanged. See MODEL_PROVIDER_VERIFICATION.md.

24 October 2026. Python 3.12.14, Node 24.18.0, Windows Chrome. Local uncommitted working tree; no upload/public deployment or new external model request.

## Actually executed

Full discovery with PURRPOSE_HMEM_REFERENCE configured: **103 tests passed**, including nine new HTTP tests. Covered served page/status, actual backend update cycle, organization gaps, explicitly unavailable unconfigured memory, rejected arbitrary fields/actions, cross-origin/local-header restrictions, Host and file-path guards, idempotency, body size and explicit debug access. HTTP tests used ephemeral loopback servers and no cloud credentials.

Started `python -m purrpose.server --port 8766 --reference ../meterless/engines/hmem/reference/src/index.ts --state purrpose/.state/hmem --workspace local-ui-20261024-a`. The instance listens only on 127.0.0.1. It uses the already inspected official local H-MEM reference.

Headless Chrome performed actual form/button operations against the live Python backend:

1. Check cases returned pending with unknown funding gap.
2. History returned the first actual H-MEM creation timestamp.
3. Organization review returned the grant-inclusion gap.
4. Clarify separate grant changed the backend result to 100000 cents.
5. A new supporter query displayed the updated result.
6. Query at the original historical cutoff still returned null; latest retained review returned 100000 cents.
7. No page JavaScript errors; no horizontal overflow at 390 pixels.

The page is functional, not a prerecorded HTML result. All organization/case/source facts remain synthetic. H-MEM persistence/recall/history is real. This server does not make NVIDIA/Nightshift/Zetaris or live website requests; those integrations' separate historical evidence does not imply they run on each button click. No payments, private uploads or arbitrary SQL.

## Remaining work

Natural-language model-driven planning, real permitted case evidence ingestion, current identity/risk coverage and Nightshift remain incomplete. Interface styling is intentionally basic. Serial local HTTP is not production auth, concurrency or public hosting. Source and idempotency state reset at restart; memory stays in the configured local scope. Browser QA changed fixture state during its checks, so the running instance may already show a clarified case. New operators should follow the explicit controls, not assume a pristine first-visit state.
