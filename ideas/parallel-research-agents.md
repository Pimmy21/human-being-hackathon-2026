# Idea: Parallel Research Agents

Proposal and to-do list · 24 October 2026 · **Not adopted.** The current build follows the spec in `first draft/guidance/`, which uses one orchestrator (FULL_GUIDANCE §16).

## The idea

Alongside the spec's main review, run a few small research agents at the same time. Each one gathers a different kind of public signal about the rescue. A critic agent then challenges their findings before the result reaches the six checks.

```text
                        ┌─ Registry agent ─────┐  CRA charity listing, Corporations Canada, Ontario Business Registry
 donor's question ──►   ├─ Document agent ─────┤  vet estimate / invoice read by Nemotron (nemotron-3.5-parse)
   orchestrator         ├─ Partnership agent ──┤  does the partner (clinic, shelter) mention the rescue on its own site?
                        └─ Social-signal agent ┘  public organization accounts only: age, name changes, activity
                                  │
                                  ▼
                           Critic agent  ── sends weak findings back for one retry
                                  │
                                  ▼
                      six checks (unchanged, in code) ──► answer with sources
```

## Why it might be worth it

- **Judging:** judges reward agents that delegate, critique, retry and branch, and call a straight A→B→C pipeline weak (`resources/57_Strong Submission Examples`, `55_Weak Submission Examples`). The spec's single orchestrator risks reading as a pipeline.
- **Track 2 fit:** a partnership confirmed by the partner itself is independent evidence. Several reposts of the same story are not (R07).
- **No rule changes needed:** the agents only gather evidence. The six checks, the money calculation and the "unknown is not zero" rule stay exactly as written.

## The original sketch, revised

The first sketch (brainstorm drawing, 22 Oct) had four steps. Here's what happens to each:

| Original step | Decision | Why |
|---|---|---|
| 1. Scrape Facebook/Instagram data for the rescue | **Change.** Don't scrape. Use Exa search over public pages, or Bright Data (a hackathon sponsor) if credits exist. | Meta's terms ban scraping, and pages need a login. |
| 2A. Account age, name changes, partnerships | **Keep, partly.** Use it only where a legitimate source returns it. | Instagram's "About this account" and Facebook's Page Transparency panel are only shown in the app or web page, with no API for them. |
| 2B. Confirm partnerships by finding mentions on the partner's side | **Keep: the strongest step.** | It's cheap, public, independent and easy to cite. |
| 3. Check founders' private social media | **Drop.** Check the organization against the directors the CRA charity listing publishes instead. | It targets private people, raises Canadian privacy-law questions, and conflicts with R15. |

## To-do (only if the team adopts it)

- [ ] Agree with the product policy owner on whether this changes FULL_GUIDANCE §16, or sits beside it.
- [ ] Decide whether the app calls Exa's API directly (`exa-py`) or Zetaris registers it as a REST table (unverified).
- [ ] Check whether Bright Data gives participants credits (ask in its HackOS Help channel).
- [ ] Build the partnership agent first: one source, one Exa query, cited result.
- [ ] Build the critic: one bounded retry, logged, with no paid retries beyond the budget (R13).
- [ ] Add a sample mode that replays stored Exa responses, so judges can run it without keys.
- [ ] Write tests: a partnership found, a partnership not found ("not found" is not a negative finding), and a critic downgrade.

## Open questions

- Does this add enough to the score to justify the time? About 3.5 days remained as of 24 Oct.
- Who owns it?
