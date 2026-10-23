# Problems Decision Rights and Escalation

## 1. Solve the correct layer

Start by identifying the failing stage: local setup, data retrieval, identity matching, calculation, memory, inference, publication checks or frontend. Keep a short sanitized reproduction. Change one cause at a time. An application error is not automatically a sponsor outage or a product-definition problem.

Use a bounded attempt: reproduce once, inspect the relevant code/docs, try one evidence-based fix and run the smallest relevant check. After roughly 20–30 minutes without new information, route it to the relevant owner and progress on independent work. Do not retry external calls in a loop while everyone waits.

## 2. Who should receive the problem

| Situation | First action and owner | What to avoid |
|---|---|---|
| Import, missing package, wrong command | Developer checks current repo/runbook; pin/install only project dependencies needed | Asking Shiyuan which import to use |
| JVM or JAR failure | Integration owner checks configured JDK, actual JVM DLL and driver file | Copying Java installations, replacing SSL or searching for secrets |
| TCP connection refused | Check configured host and whether authorized runtime/cluster is running | Guessing another endpoint or exposing localhost publicly |
| Government API 504 | Data owner records source timeout, keeps existing evidence dated, enables explicit replay | Treating outage as failed charity identity, rebuilding AWS stack |
| Zetaris SQL/table error | Data owner checks source repo rules and existing objects; ask Zetaris support if needed | Creating/dropping resources speculatively |
| AWS explicit deny/permissions | AWS account/resource owner reviews the exact failed action and policy | Assuming a different IAM dropdown or account upgrade will fix it |
| NVIDIA 401/403 | Key/account holder checks authorized model access privately | Posting key screenshots or repeatedly trying paid alternatives |
| NVIDIA 429 | Stop repeated requests; inspect quota/rate status with account holder | Unbounded retries or purchasing credits without approval |
| Nightshift Web looks active but endpoint fails | Provider owner verifies an actual listener and `/v1/models` from the backend machine | Counting a recorded replay as a provider call |
| Nightshift 401/403 | Runtime holder checks real token; categorize unauthorized | Falling back to a dummy token or logging connect-link secrets |
| Model invents facts or misses citations | Backend/evidence owners hold draft, tighten data contract and evaluate | Treating fluent prose as source evidence |
| Memory empty after restart | Memory owner checks state path, source scope, Node runtime and query threshold | Replacing official H-MEM with an unused dependency claim |
| Frontend and backend disagree | Owners compare payload fixture/contract; fix one shared definition | Adding frontend-only funding logic to hide mismatch |
| Source cannot be used legally/appropriately | Evidence owner finds permitted material or labels a synthetic fixture | Bypassing access controls or uploading sensitive documents |
| Team member unavailable | Coordination lead reassigns an unclaimed task with agreement | Assuming silence means approval or messaging on someone's behalf |

External support contact is sent by a human unless a tool has explicit human authorization to send it. Coding assistants can prepare a concise support draft with redacted errors.

## 3. Decision ownership while Shiyuan is away

### Team may decide

Implementation details, component names, branch structure, accessible styling, reversible refactoring, fixture-based tests, source research, existing approved read-only queries, and a safe no-model UI when inference is unavailable. Record significant choices in a short decision file.

The team may proceed with explicit synthetic fixtures to test mechanics if real evidence cannot yet be obtained. This does not approve claiming a real case was verified. The team may demonstrate an unavailable service honestly; it may not mark its acceptance gate passed.

### Account or resource owner decides

New credentials/access, paid requests beyond an agreed existing budget, account upgrades, additional cloud resources, IAM changes, database writes, public hosting and secret rotation. If the relevant owner is Shiyuan and she is away, pause that action while preparing the plan and progressing elsewhere.

### Ask Shiyuan for a product decision

- Changing the primary user, target domain or core case-first journey.
- Adding certification, a trust score, a fraud verdict or guaranteed outcomes.
- Removing a required evidence/sponsor feature or weakening a completion criterion.
- Using undisclosed simulation as proof of verification.
- Adding actual donation collection, new private-data intake or autonomous outreach.
- A real tradeoff that cannot meet the agreed definition of done without changing it.

Mentor feedback is valuable advice. Record it and distinguish it from an accepted scope change. Shiyuan should receive the smallest decision needed, not a broad request to redesign the entire product.

## 4. How to ask for a decision

```text
Decision needed:
Current agreed rule:
What we tried and what is blocked:
Option A and consequence:
Option B and consequence:
Our recommendation:
When a decision is needed:
Work continuing while we wait:
```

If there is no reply, keep the existing product boundary, leave the blocked gate open and choose independent work. Elapsed time is not consent. Do not delete tests or remove warnings to make the demo appear complete.

## 5. Secret or privacy incident

Stop further exposure. Tell the credential/resource holder privately and arrange revocation/rotation. Removing a file from the latest commit does not erase its public history. Do not paste the secret in an issue to explain the incident. Preserve a sanitized incident record. The team can contain exposure immediately; actions requiring account authority go to that owner.

## 6. Provider and network mistakes to check first

- A configured key may exist on Shiyuan's machine but not yours.
- A successful `/health` response does not prove model access.
- An HTTP 401 differs from a timeout; show the actual category.
- `localhost` refers to the machine making the request, including a hosted container.
- The browser's replay animation may not represent your current task.
- A 2024 source captured today is still a 2024 filing.
- A model's token count is not a dollar amount without the actual pricing/billing basis.
- A model can return text successfully and still fail publication checks.
- The old prototype's passed tests do not mean the new case workflow has passed.

## 7. Instructions to assistants facing a blocker

Read the narrow relevant official documentation and repository instructions. Preserve known-working configuration. Explain the failing stage and the smallest useful next action. Ask only for missing authority or information you cannot infer. Keep working on independent authorized tasks. Never claim the tool is installed, connected or complete solely because a guide or prompt was written.
