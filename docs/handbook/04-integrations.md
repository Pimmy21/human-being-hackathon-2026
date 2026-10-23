# Tool Connections and Calling Methods

## 1. Development tools versus application tools

Cursor, ChatGPT and Codex help humans build and review the application. The running application invokes adapters for data, memory and model inference. Writing “use Zetaris” in a prompt does not give a model database access. Each adapter needs actual code, configuration, permission and a verified request.

The preferred first implementation has explicit provider selection: `nvidia` or `meterless`. Record which one ran. Do not route a failed Nightshift call to NVIDIA and then claim Nightshift worked. Do not require every request to call every sponsor service; give each integration a real useful job and evidence of execution.

## 2. Configuration and ownership

Use an ignored `.env.local` on the backend machine. Commit only empty placeholders in `.env.example`. Required names:

```dotenv
# Backend only. Fill locally, never in a chat, issue or browser bundle.
APP_MODE=replay
MODEL_PROVIDER=nvidia
NVIDIA_API_KEY=
NVIDIA_MODEL=
ZETARIS_JDBC_URL=
ZETARIS_JDBC_JAR=
ZETARIS_USERNAME=
ZETARIS_PASSWORD=
PAWPROOF_JAVA_HOME=
METERLESS_BASE_URL=http://127.0.0.1:8088/v1
METERLESS_RUNTIME_TOKEN=
METERLESS_MODEL=meterless/auto
```

`PAWPROOF_JAVA_HOME` is the legacy adapter's variable name; retain it during migration or rename it with compatibility and tests. New application paths must be configurable, not Shiyuan's hard-coded Windows directories. The adapter should map the uppercase environment token to the provider contract's `meterless_runtime_token` setting without logging either.

One teammate's environment is not shared automatically. Each person needs authorized access or can use replay mode. Account holders control credentials, quotas and paid changes. Do not request access keys in public issues. Restrict the backend to localhost for the development demo unless a deployment has been deliberately approved and secured.

## 3. Meterless H-MEM

**Purpose:** save source-linked case facts, unanswered questions and corrections; recall them before explanation and update comparison.

Use the official reference or a tested implementation based on its spec. Read the upstream root instructions, then `engines/hmem/AGENTS.md`. Do not install every engine. The earlier prototype used the official reference pinned to commit `1742dec56a66e58eef9dda2d2b865823758ca8cd`; verify that version before reusing its exact interfaces. Retain its Apache 2.0 license and any required notices if vendoring.

Illustrative calls for that reference:

```typescript
const memory = new HMEM({persistDir: userStateDirectory, actor: 'purrpose'});
memory.add({
  content: JSON.stringify(validatedCaseFact),
  type: 'factual', layer: 'working', confidence: 1,
  source: evidenceUrlOrPermittedFileReference,
  provenance: {origin: 'document', learnedAt: Date.now(), label: 'Curated case evidence', refs: evidenceIds},
  chatId: demoUserId, tags: [caseId]
});
const recalled = memory.query(question, {chatId: demoUserId, topN: 5});
```

This is an example, not copy-ready application code: define the variables, import the pinned library, validate scope and handle missing data. Confidence here describes curated capture, not charity trust. Tune relevance thresholds with tests, rather than assuming the reference's default retrieves every case fact.

The Python orchestrator can invoke a small Node bridge through structured JSON stdin/stdout, using an argument array and no shell interpolation. Node must support the reference's TypeScript features; the previous environment used Node 24 with `--experimental-transform-types`. A TypeScript runner is an alternative if deliberately installed and pinned.

Proof: save a fact, stop the process, restart, retrieve the fact for the same alias and use it in a comparison. A different alias must not retrieve it. Show the source and memory trace. Run the applicable upstream conformance suite plus application tests. Do not claim that importing the reference validates the entire product.

## 4. Zetaris

**Purpose:** query registered structured evidence, starting with the government's historical organization identity record. Proposed case/funding tables are not already present.

The existing approved database is `DONATION_FEASIBILITY_20261022`; `tcr_identity` and `ava_identity` are REST-backed tables. `tcr_identity` was matched to Toronto Cat Rescue's BN `720884691RR0001`. Its dataset year is 2024. Do not connect that identity to a synthetic case as though the real rescue requested the invented treatment.

Before work, read the Zetaris repository's own AGENTS and JDBC connection guide. Use configured credentials and driver path. Do not search a teammate's disk for keys. On Windows, verify the JAR and a real `bin/server/jvm.dll`. The earlier scripts' Unix assumptions needed a Windows adapter; use real `.exe` paths, not copied Java shims.

Connection flow: load environment without printing it; start JPype with the configured JVM and JAR; use JayDeBeApi with `com.zetaris.lightning.jdbc.LightningDriver`; use the configured remote SSL JDBC URL and local credentials. Do not change endpoint syntax based on a guess.

Run one statement per call, no trailing semicolon:

```sql
SELECT 1
```

```sql
SHOW LIGHTNING DATABASES
```

```sql
SELECT fact.BN, fact.`Legal Name`, fact.City, fact.Province
FROM DONATION_FEASIBILITY_20261022.tcr_identity
LATERAL VIEW explode(result.records) AS fact
```

Inspect existing source availability; `SHOW DATASOURCES` alone omits Lightning sources. Only use the case's correct identity table. Capture row identity, source year and query outcome in the run. Do not expose the configured cluster URL or credentials in public logs.

Known issue: the upstream Government of Canada API returned HTTP 504 on the latest identity query despite successful JDBC connectivity. This is not evidence that the charity failed a check. Do not recreate the stack, disable SSL or upgrade the AWS account to fix an upstream timeout.

New tables, grants or writes require a concrete plan and resource-owner approval, following the source repo's rules. While waiting, structure and test local case records. A team member may prepare SQL dry runs but must not execute cloud mutations by assumption. Do not repeatedly retry a slow upstream API; record the failure and move to explicit replay for presentation if needed.

## 5. NVIDIA hosted inference

**Purpose:** help extract candidate fields or explain a validated evidence bundle. Inference is not independent verification.

The earlier standard-library client lives in Shiyuan's local `nvidia-setup/nvidia_client.py`; it is not currently in this GitHub repository. Migrate only reviewed source code if needed, not its credential file. Existing interface:

```python
result = complete([
    {"role": "system", "content": system_instructions},
    {"role": "user", "content": public_validated_evidence_json}
], max_tokens=750)
# result: model, text, usage, finish_reason
```

The previously verified official endpoint is `https://integrate.api.nvidia.com/v1/chat/completions`. Send the API key in the Authorization bearer header, content type JSON, a configured model, messages and a bounded output limit. The previous model was `nvidia/nemotron-3.5-lightning-30b-a3b`; confirm current availability in the developer's account before using it. Do not promise unlimited free inference.

The local starter enforces 12,000 input characters, 1–1,024 output tokens and a 90-second timeout, with no automatic retries. These are application limits, not universal NVIDIA limits. Preserve the cap during initial migration. Record returned usage, not guessed billing. Never send private documents merely to test the connection.

System instructions must limit answers to supplied evidence, require source IDs, distinguish historical identity from current need, and prohibit invented amounts or certainty. Extraction should return schema-valid candidate fields with page references. Compare the generated fields to originals in a human-reviewed fixture before claiming extraction accuracy.

Known issue: the previous real explanation returned text but omitted required citations and over-attributed a discrepancy. It was held for review. Reuse the lesson, not the unsafe draft as approved copy. Provider success and answer correctness are separate gates.

## 6. Nightshift / Meterless Runtime provider

**Purpose:** provide a real alternate inference route from our application. This remains open; the earlier browser job failed with “lane did not answer.”

As checked on 23 October 2026, the official provider prompt describes Runtime 1.4 / contract v4. Recheck the official page if the installed version differs. The adapter's minimum behavior:

- Normalize the configured runtime origin to exactly one `/v1`. Default `http://127.0.0.1:8088/v1`.
- Read the real runtime token locally; the contract describes `<stateDir>/proxy-token`. Placeholder `rt-local` is not accepted. Do not log connect links or their fragments.
- Send `Authorization: Bearer <token>` on calls; add `meterless-app: purrpose`; add `meterless-scope: user` on chat.
- Check `GET <base>/models`. 401/403 means unauthorized; a valid list with `meterless/*` IDs means online; other failures mean offline. A process health check alone is insufficient.
- Discover model IDs from that response. They represent routing modes. Keep unknown `meterless/*` IDs rather than removing them. Start with `meterless/auto` when available.
- Send a plain text chat request to `POST <base>/chat/completions`; allow up to 180 seconds as specified for model loading. Preserve text as a string.
- Follow the official auto-detection behavior for approved local host/ports if implementing auto-detect; do not scan unrelated networks. Test wrong-token classification as well as success.

Illustrative JSON body, using the token only in the header:

```json
{
  "model": "meterless/auto",
  "messages": [{"role": "user", "content": "Summarize the supplied public evidence and cite its source IDs."}],
  "stream": false
}
```

The exact response handling must be verified with the available runtime. The adapter returns the same application envelope as NVIDIA: selected provider/model, text, usage or null, finish state and error category.

**Machine placement matters.** A browser tab being open is not proof that an external HTTP server is listening. `127.0.0.1` on a hosted backend points to that backend, not a teammate's laptop. Prefer running the demo backend and the reachable runtime on the same authorized machine. Do not expose an unauthenticated local endpoint publicly to make a connection work.

Proof required: the application calls the runtime, gets a response, records it and exercises a useful feature. A Web replay, installed dependency, copied token or a direct NVIDIA response does not count. If the runtime cannot be made reachable within the bounded troubleshooting attempt, contact Meterless support through a human and keep the requirement marked incomplete. Do not buy a GPU or install large models solely on an assumption.

## 7. Who gets which problem

| Problem | First technical owner | External help if needed |
|---|---|---|
| H-MEM not recalling or persisting | Backend/memory owner using upstream reference and tests | Meterless engine documentation/support |
| Nightshift unauthorized/offline | Provider owner, then runtime/account holder | Meterless runtime support |
| Zetaris SQL, table or JDBC issue | Data/integration owner | Zetaris support |
| AWS permissions or cloud account changes | AWS resource owner | AWS support; do not assume Zetaris can inspect the account |
| Government source 504 | Data owner records source failure | Source publisher if persistent; show honest unavailable state |
| NVIDIA 401/403/429 or model access | Provider owner and NVIDIA account holder | NVIDIA developer support |
| Unsupported generated claim | Backend/evidence reviewers | Fix prompt/rules; this is not automatically a provider outage |
| Layout, interaction or accessibility | Frontend/design owner | Design skill/model for assistance, followed by human inspection |
| Product promise or acceptance change | Shiyuan | Mentor may advise, but record the product decision |

## 8. Reference links

- Meterless provider prompt: https://meterless.ai/engines.html (Power, Add Meterless as a provider).
- Meterless source/specs: https://github.com/Meterless/Meterless.
- Zetaris JDBC setup: https://zetaris.github.io/getting-started/docs/connections/client-setup.html?protocol=jdbc.
- NVIDIA model catalog: https://build.nvidia.com/ (use the chosen model's current API example).
- FastAPI guidance: https://fastapi.tiangolo.com/tutorial/.
- React guidance: https://react.dev/learn.

The first two adapter contracts were checked against official documentation and existing local code while writing this handoff. Stack choices and proposed application routes still require implementation and testing. These links do not grant account access or replace each project's instructions.
