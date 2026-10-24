# Purrpose Workflow Wireframe

An interactive, hard-coded example for reviewing the product workflow before building integrations. English interface. All organizations, cases, evidence and tool outcomes are synthetic.

## Open it

1. Extract the ZIP completely. Keep `index.html`, `styles.css` and `app.js` together in the `wireframe` folder.
2. Open `wireframe/index.html` in a modern browser such as Chrome or Edge.
3. No install, server, API key, GPU, Java, database or network connection is required.

If reviewing with a coding assistant, open the extracted package folder as its workspace, give it `PROMPT_FOR_AGENT.md`, and ask it to inspect the files before trying to launch anything. A browser-capable assistant can open the HTML file; an assistant without a browser can review the source and have the human open the page.

## The main walkthrough

1. In **Supporter**, select “Anywhere in Ontario” and click **Check selected cases**. The case stays pending because grant inclusion is unclear. Open source cards.
2. In **Organization**, click **Review public information**. Inspect the specific clarification needed and suggested public update channel. No upload is offered.
3. Keep “Grant is separate from the CAD 700 raised” and click **Simulate reading public update**. Return to the supporter result: disclosed remainder is CAD 1,000. Qualification is synthetic and assumes passing synthetic identity/risk fixtures.
4. Open **History**. The original unresolved result remains separate from the later clarified result.
5. Open **Developer trace**. Inspect exact simulated stages, tool states and zero external calls. Download the simulated run record if useful.

## Alternative examples

- Grant already included: remaining is CAD 1,300. Do not subtract it again.
- Fully funded case: remaining zero, not a positive-gap recommendation.
- Updated source cannot be read: remains pending; critical source failure shown in the developer trace.
- Unsupported optional explanation: structured fixture result remains, explanation is withheld; no actual model is called.
- Toronto city filter: no match, because treatment is in Ottawa despite the organization's Toronto headquarters. Expanding region requires a deliberate click.

Use **Reset walkthrough** before a fresh sequence. Browser reload/reset clears all simulated records. There is no real persisted memory, real H-MEM, live source fetch or AI conversation.

## What this proves and does not prove

This wireframe demonstrates intended inputs, outputs, funding arithmetic and user transitions. It does not prove any actual charity, medical need, risk query, donation channel, provider connection or model quality. All passing risk/identity checks are test fixtures.

NVIDIA, Nightshift and Zetaris are not connected. H-MEM is not integrated: a small in-memory JavaScript array represents earlier records so the planned behavior can be discussed. No API credits are used by the wireframe. Running a separate development assistant may consume that assistant's own quota.

There are no real donation URLs or payment buttons. The browser may save a simulated JSON run record only when the user chooses to download it.

## Relationship to the guidance

The sibling `guidance` folder in the handoff ZIP contains the local v2.1 specification and human companion for reference. This is not permission to publish or push those documents. Read the human guide first, then the matching rule/specification sections. The wireframe covers a small example; its hard-coded fixture behavior must not replace the full implementation rules.

Frontend styling here is temporary and may be changed later. The current priority is verifying the product workflow.

## Review checklist

- Pending result does not invent a remainder.
- Organization output says exactly what to clarify and why.
- The notification itself is not presented as verified evidence; a selected new fixture represents the subsequent read.
- Separate/included grant scenarios calculate 1,000/1,300 correctly.
- Source failure is not called a negative finding about the organization.
- No internal step list in the default supporter view.
- History does not silently change when a newer version is added.
- Tool trace does not claim any real integrations.
- No external requests, keys, payments or private uploads.
- Narrow/mobile browser layout remains usable.

Record feedback in `REVIEW_NOTES.md` with the scenario, observed behavior, expected behavior and suggested change. Do not change policy merely to make a scenario pass.
