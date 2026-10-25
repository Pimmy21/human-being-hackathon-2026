# Chat model provider verification

25 October 2026. Branch `feature/model-intent-provider`. Account owner (Josh, own NVIDIA key) approved the caps below and live chat calls on that key. The team's earlier one-call NVIDIA authorization was not used.

## What was built

- `provider.py`: explicitly configured chat provider. `PURRPOSE_MODEL_PROVIDER` selects `nvidia_direct` (fixed `https://integrate.api.nvidia.com/v1/chat/completions`) or `meterless` (loopback base URL only, `/v1` normalized once, real token required, `rt-local` rejected, `meterless-app: purrpose` and `meterless-scope: user` headers). No automatic fallback between providers, no redirects, no retries, bounded response size, sanitized error categories (401/403 → unauthorized, 429 → rate_limited, timeout → offline with uncertain usage). Reuses `extraction.Budget`/`Limits`; adds a per-minute dispatch cap. Missing or invalid caps fail closed.
- `model_intent.py`: every ordinary chat message is sent as untrusted JSON data with a small session context; the model returns one intent object; `chat_intent.validate_intent` checks it; identical message + context + prompt/model version reuses the cached intent.
- `conversation.py`: the validated intent becomes a canonical phrase handled by the existing bounded matcher, so code still writes every reply, amount and status. Code-only before any model call: payment/rule-override refusals, negations, two-city requests and explicit source refreshes (a model cannot trigger a web read). Invalid output or provider failure falls back to bounded matching, labelled `bounded_intent_matching` with `model_intent.status` and the true `new_cloud_calls`.
- Meterless discovery: `Provider.probe()` calls GET `/v1/models` (not inference, not budgeted); 200 with `meterless/*` ids is online and unknown ids are kept, 401/403 unauthorized, network failure offline, a listing without `meterless/*` ids is not online. A successful listing alone is not counted as Nightshift use. The server runs it at startup for the `meterless` route only.
- Organization questions: an `organization_checklist` intent opens Lucy's checklist only inside Lucy context. A fresh session asking what its own rescue should publish gets a code-written pointer to the organization walkthrough and a reminder that a stated role does not verify identity (found in the first live run, fixed and re-verified live).
- Geography and fictional cases (found by the account owner while testing in the browser): "kittens in indonesia" came back as `fictional_demo` and showed the fictional Maple case, and "Canada" was silently treated as anywhere in Ontario. Now a `fictional_demo` intent only switches collections when the message literally contains fictional/synthetic/虚构/模拟 (otherwise code asks which the user wants), and a new `outside_area` intent gets a code-written "only covers Ontario" reply with a one-reply offer; "yes" then shows real Ontario-wide leads. Prompt version intent-v3.
- `server.py`: `--env-file` (or environment variables) loads the provider. `/api/status` reports `model_provider`, `cloud_inference_in_this_server` and `nightshift`; `/api/debug` includes the sanitized `model_trace` (no keys, no message text, no reasoning).

## Caps (approved by the account owner)

| Cap | Value | Basis |
|---|---|---|
| Calls per server run | 200 | Runaway protection; free trial has no credit pool |
| Tokens per server run | 100,000 | ~300-400 tokens per message observed |
| Calls per minute | 20 | NVIDIA states "up to 40 RPM for most models"; community reports 429s at 12-24 RPM |
| Input characters per call | 4,000 | 1,500-char message + prompt + context |
| Output tokens per call | 300 | JSON answer ~50 tokens; thinking disabled |
| Timeout | 30 s (NVIDIA direct) / 180 s (Meterless contract) | Hackathon guide 30-90 s for model calls; Meterless provider contract v4 |
| Retries | 0 | Repository demo rule |

Sources checked 25 Oct 2026: NVIDIA staff on forums.developer.nvidia.com (credits replaced by unpublished per-model trial rate limits, Sep 2025); build.nvidia.com model page (1M context; `chat_template_kwargs.enable_thinking`); meterless.ai/engines.html provider contract v4 (180 s timeout, headers, routing modes, no documented rate caps).

## Actual live results (nvidia_direct, nvidia/nemotron-3.5-lightning-30b-a3b)

- First 8-message run: 7 calls, 2,764 tokens. 3 intents valid; 4 rejected because the model wrote `"region_wide": null`; one misread ("yes please" → select_real_case). Fallback replies stayed correct and labelled.
- Diagnosis: 4 diagnostic calls (1,563 tokens) printed raw output locally. Fix: validator treats `null` as `false` (other non-booleans still rejected, test added); prompt v2 states booleans explicitly and sharpens confirm_expansion/allocation.
- Second run, same 8 messages: 7 calls, 2,986 tokens, 7/7 validated and correctly classified (greet; "kitties near the capital" → Ottawa; "yes please" → confirm_expansion; amount; allocation; Chinese organization question → checklist in Chinese; weather → clarify). The rule-override message made zero model calls. Latency about 1-8 s; no errors.
- Browser: `/home.html` on a model-enabled server answered "kitties anywhere in the province" with the pending Lucy lead and the notice that the configured model classified the message (1 call; usage not captured because that test server was stopped).
- Organization fix, live: the same Chinese rescue question in a fresh session classified as organization_checklist (1 call, 443 tokens) and now returns the walkthrough pointer, with no Lucy checklist and no Lucy context.
- Geography fix, live: 2 diagnostic calls reproduced the Indonesia bug (raw output `fictional_demo`). After the fix, 5 calls / 2,312 tokens: Indonesia and "canadda" → outside_area with the Ontario notice; "yes please" → real Lucy lead; "cats in toronto" → Toronto search; "show me the fictional demo" → fictional mode. Real collection kept in every non-explicit case.
- Session total for development checks: 27 live calls; 10,068 tokens recorded for 24 of them, 3 unrecorded (1 browser, 2 diagnostics). No 429s or timeouts. The account owner's own browser testing is additional and not counted here.

## Tests

`python -m unittest discover -s purrpose -t .`: 210 ran, 200 passed, 10 skipped (H-MEM reference not configured on this machine; skipped is not passed). `node purrpose/test_api_client.cjs` passed. New tests: `test_provider.py` (23), `test_model_conversation.py` (19), 6 more in `test_chat_intent.py`. Offline tests inject fake transports/providers and make no network request.

## Not established

- **Nightshift is still not connected.** These are direct NVIDIA calls and must not be counted as Nightshift (acceptance M18). The `meterless` route (chat and `/v1/models` discovery) is implemented to the published contract and tested only offline, because no runtime was reachable on this machine (Windows without a dedicated GPU).
- The browser chat deadline is 65 s; a first Meterless model load may need up to 180 s. Align before relying on the Meterless route.
- Intent classification only. The model does not write answers, read evidence or affect amounts or qualification. Unified supporter/organization dual-intent chat (NEXT_DEVELOPER priority) is not implemented here.
- Budgets are per server process, not durable billing.
