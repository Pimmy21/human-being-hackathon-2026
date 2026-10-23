# Team Execution and Definition of Done

## 1. Assign roles before editing the same files

No named teammate is automatically assigned by this document. The available team chooses owners and a temporary coordination lead. Josh proposed the antenna idea; that does not assign him Purrpose engineering work without agreement. Shiyuan remains the product decision owner during this handoff.

| Role | Accountable output | Can decide without Shiyuan |
|---|---|---|
| Temporary coordination lead | Claimed tasks, review order, useful checkpoints and one restartable handoff | Task order, branch coordination and reviewer pairing |
| Evidence researcher | One permitted case bundle, field definitions, citations, gaps and permission notes | Source search, case research and drafting clarification questions |
| Backend/integration owner | Validated schema, funding rules, adapters, API and sanitized trace | Internal code and library choices within scope |
| Frontend/design owner | Responsive case review, source inspection, honest error/unknown states | Visual refinements, component structure, accessibility fixes |
| Reviewer/demo owner | Acceptance checklist, run evidence, demo script and clean-clone setup check | How to exercise and document existing criteria |
| Shiyuan | Product boundaries, material scope tradeoffs and acceptance changes | Decide only when genuinely required |

People can combine roles. Another available person should review important funding logic and source mapping when possible. If no reviewer is available, label the work unreviewed rather than calling it verified.

## 2. An execution order for the absence window

These are suggested work blocks, not a promise that every integration will be finished in a day. Run independent tasks in parallel only after humans agree on file ownership. Do not have multiple assistants modify the same adapter concurrently.

### Block A — establish a runnable baseline

Clone the repository. Read the status record. Confirm each person's environment and access without revealing credentials. Select a curated case type. If real case access is blocked, use explicitly synthetic fixtures for engineering. Create the shared case schema and a minimal application shell. Write the actual tested launch commands in `docs/runbook.md`.

Frontend may build with synthetic JSON while evidence research continues. Backend implements currency/time/overlap logic without inference. Provider owner separately checks availability. None of these tasks depends on a final color choice or an upstream API recovery.

### Block B — make the main journey work

Wire the case page to the backend. Display evidence and gaps. Implement funding checks. Show the critical ambiguous-grant case and one missing-cost case. Make source inspection useful. Add H-MEM persistence and restart recall.

At this point a person should be able to ask “What is this request supported by?” and receive an inspectable structured result, even if model prose is unavailable.

### Block C — connect model and data adapters

Use the safe public bundle for one bounded NVIDIA request. Add publication checks. Test Zetaris using existing approved objects. Complete the Nightshift adapter and a real runtime request if the endpoint is available. Record each gate separately; do not let a working frontend obscure a missing sponsor integration.

If a source fails, keep that run's failure and show a deliberately selected replay for presentation. Do not silently relabel it live.

### Block D — review and leave a handoff

Run the acceptance cases. Check the browser at desktop and mobile widths. Review generated claims against sources. Record mode, provider calls, token usage, memory trace and limitations. Prepare a short demo and open the review PRs. Leave the current branch, commands, last passing run and next action for whoever comes online next.

## 3. Ready-to-claim work items

Create one GitHub issue per row when an available person claims it. Do not mark an issue assigned without their agreement.

| ID | Task | Deliverable and check | Depends on |
|---|---|---|---|
| P01 | Curate one permitted case | Manifest, sources, dates, gaps; clearly real or synthetic | Product chapter |
| P02 | Define shared schema and fixtures | Typed/validated contract; unknowns as null; example cases | P01 draft |
| P03 | Implement funding rules | Unit tests for inclusion, duplicates, currency, dates and unknowns | P02 |
| P04 | Build case review interface | Main page, source drawer, funding unknown state, mobile | P02 |
| P05 | Add backend review orchestration | Curated case input, bounded steps, source outcomes, run IDs | P02/P03 |
| P06 | Wire H-MEM | Save, restart, retrieve and consume prior evidence; alias isolation | P02/P05 |
| P07 | Connect NVIDIA and publication checks | Real public-evidence request plus invalid-output tests | P02/P05 |
| P08 | Verify Zetaris adapter | Existing read-only query, source-period label, outage state | Authorized connection |
| P09 | Connect Nightshift provider | Unauthorized/offline distinction and useful real request | Reachable runtime/token |
| P10 | Add controlled follow-up/update | Earlier/new version preserved, clarification changes result | P03/P06 |
| P11 | Review UX and evidence | Keyboard/mobile checks, claim-to-source human review | P04–P10 |
| P12 | Prepare restartable demo | Fresh-clone commands, run evidence and known limits | Reviewed baseline |

## 4. Acceptance levels

**Documentation ready:** the instructions and contracts are available. This does not mean the app runs.

**Local workflow ready:** the core journey works with labelled fixtures, deterministic checks, source inspection and real H-MEM use. A synthetic case proves mechanics, not authenticity of an actual rescue request.

**Integration ready:** each claimed external service has a recorded successful application call with the correct mode. If a source is currently down, its gate is marked unavailable, not passed. Historical verification can be cited only as historical.

**Presentation ready:** core workflow checks pass, every demonstration mode is disclosed, generated claims are reviewed, and the sponsor requirements are either actually met or explicitly reported incomplete. Do not remove a requirement merely to make the checklist green.

**Real-case validation:** permitted, current-enough case evidence has been examined by humans; remaining limits are recorded. This is separate from software readiness. A working demo cannot guarantee an organization is trustworthy.

The organizer message supplied by Shiyuan requires a working Meterless Engine feature and Nightshift as an application AI provider. Confirm the current official submission details before final submission. H-MEM alone is not evidence that the separate provider requirement is complete.

## 5. Required acceptance cases

Record result, actual command/manual steps, commit, mode and reviewer for each relevant case. Tests must assert meaningful behavior rather than merely reproduce the implementation.

| Check | Expected behavior |
|---|---|
| First visit | Empty memory is handled; case evidence remains usable |
| Source traceability | Every factual finding opens the correct source and relevant location |
| Independent origin | Two reposts do not count as two independent confirmations |
| Historical identity | Old filing never implies current registration or current treatment need |
| Missing cost | Cost and remaining need stay unknown; a practical question is shown |
| Grant outside raised total | Synthetic 2,000 − 700 − 300 gives CAD 1,000, with assumptions |
| Grant inside raised total | Synthetic 2,000 − 700 gives CAD 1,300; no second subtraction |
| Unknown grant inclusion | Exact remaining is not established |
| Unknown complete funding | No claim of a complete current gap |
| Duplicate cost/funding | Repeated source or payment item is not counted twice |
| Commitment versus receipt | Pledged funds do not silently become received funds |
| Mixed currency | Calculation blocked without an approved conversion basis |
| Stale amount | Old total remains labelled with date; no “current gap” claim |
| Overfunding | Remaining zero plus separate excess; no automatic fraud inference |
| Identity/case mismatch | Combined conclusion blocked; sources preserved |
| Prompt injection in a source | Source instructions cannot alter tool permissions or system rules |
| Provider offline | Structured evidence shown; no fabricated model result |
| Wrong Meterless token | Unauthorized, not generic offline |
| Invalid model citations | Draft held; a deterministic summary remains available |
| Unsupported model amount | Draft held; code-calculated value remains authoritative |
| H-MEM restart | Saved case recalled after process restart and used in the answer |
| User separation | Another demo alias cannot retrieve the first alias's state |
| Correction | New reviewed record preserved alongside old one; no silent history overwrite |
| Duplicate click | Does not launch two paid generation calls |
| Mobile and keyboard | Review, sources and updates usable at 390px and by keyboard |
| Secret handling | No API keys in browser bundle, logs, commits or screenshots |
| Live versus replay | Clear labels in UI and run record; no hidden fallback |

## 7. Pull request and integration rules

Branch names can be `feat/case-review`, `feat/funding-checks` or `fix/provider-status`. Keep changes small. PR body: problem, resulting behavior, tests actually run, scenario/mode, screenshots when UI changed and remaining gaps. Do not paste raw private logs.

The reviewer checks product claims as well as code. Resolve conflicts deliberately and preserve other work. Use the agreed repository review process; no force-push or bypass of review-required checks. If the team has not agreed who can merge, leave a ready PR and ask the coordination lead, not Shiyuan for every code line.

Keep final documents, reproducible code, tests and sanitized run evidence in the repository. Link large videos/data. Never upload full private chat exports, model weights, API credential files or copyrighted PDFs by default. A `.gitignore` does not remove a secret already committed.

## 8. How to demonstrate the product in three minutes

1. State the case type and demo label. Say we examine the request; we do not certify the rescue.
2. Open the case, inspect a treatment claim and its source.
3. Show a funding ambiguity and ask the follow-up that would resolve it.
4. Add a clearly labelled selected update; show how the answer changes and which earlier record H-MEM recalled.
5. Open the integration trace. Name what called Zetaris, which model/provider actually ran, and what is still unavailable.
6. End with the specific mentor question or unresolved product decision. Do not end by claiming donor-level allocation.

## 9. Checkpoint format

```text
Task / owner:
Branch / PR:
What now works:
How verified and at which commit:
Mode and real integrations:
Current blocker and failing stage:
Next useful action:
Decision needed, if any:
```

Post on completion, a material blocker change and before going offline. There is no need for constant chat updates that contain no new information.
