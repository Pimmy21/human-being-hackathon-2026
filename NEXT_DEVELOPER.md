# Continue here — current working demo

Read this first, then `START_HERE.md`, `HANDOFF.md` and the product guidance.

## Run
From repository root, with Python 3.12+:
```
python -m purrpose.doctor
python -m purrpose.server
```
Open `http://127.0.0.1:8766/home.html`. This is your own computer, not a shared hosted link. The complete original workspace is `/`; `/organizations.html` is the fictional organization journey; `/architecture.html` explains the backend and sponsor status for the mentor.

No keys or GPU are needed to try the basic pages. H-MEM requires Node 24 and an external official reference: follow `purrpose/README.md`. Do not copy another developer’s local paths or assume credentials exist. Without configured memory the app explicitly reports unavailable. No packages are automatically installed.

## What is done
- Josh’s original design assets are preserved in `design/`; a connected adaptation is in `purrpose/web/design-home.*`.
- Real donor path: one curated Lucy lead, sourced pending findings, unknown remaining amount, explicit bounded article refresh and conditional review; official H-MEM save/recall/history when configured.
- Separate synthetic funding repair and history scenario, and an entirely fictional organization website-improvement walkthrough.
- Feedback categories, source failure states, local debug traces and portable setup documentation.
- Sponsor status is factual: H-MEM used; one NVIDIA test/replay; one separate historical Zetaris query; Nightshift deferred/unconnected. No new paid requests authorized.

## Next agreed priority: one conversation entry
The product owner confirmed that supporter and organization are intents, not mutually exclusive user types. Use one chat entry. Examples:
- “I want to help a cat” → supporter discovery.
- “What evidence should our rescue add to its website?” → organization gap guidance.
- “I run a rescue and also want to support another rescue” → both journeys, with relevant context retained separately.
- Ambiguous request → one short clarifying question, never silently pick a role.
- Switching intent must not reset the conversation or mix organizations/cases. A stated organization role does not establish authority.

The current separate pages are examples of the two flows, not the final intended entry design. Integrate their behavior rather than only adding another link. Keep fictional walkthrough data visibly separate from real evidence. Unknown URLs remain unassessed; do not turn this into arbitrary URL fetching.

Inspect `conversation.py`, `organization_research.py`, `web/design-home.js`, `web/organization-demo.js` and `FRONTEND_INTEGRATION.md`. Use the existing API client and server contracts. Add bounded intent/context tests covering supporter, organization, both, ambiguity and switching. Keep current policy, unknown funding and no-payment rules. Do not broaden model/source access to hide language limitations.

## Collaboration and verification
Check the latest Git state before editing; preserve other work. Make small tested commits and update the handoff so the next developer can continue. Test commands are in `purrpose/README.md`. Set `PURRPOSE_HMEM_REFERENCE` to your own reference file for actual memory tests; skipped tests do not prove integration.

No new model spending, silent provider swaps, automatic paid retries, public deployment or outreach is authorized by this handoff. Product boundaries and definition-of-done changes need the product owner; routine implementation can proceed. The full written acceptance document is a requirements list, not a claim that every case already passes.
