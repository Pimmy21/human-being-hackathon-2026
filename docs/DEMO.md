# Demo and recording guide

Start the integrated server as described in [Setup](SETUP.md). Check the model budget before rehearsing; the example allows three model requests, not three unlimited conversations. Do not reveal local environment files, passwords or API keys on screen.

## 1. Find organizations with NVIDIA + Zetaris

On `/app.html`, start a new chat and ask:

> I would like to support a cat rescue around Toronto. Could you help me find options?

Show the returned full names, reported cities and government source links. These are historical directory leads, not trusted/qualified recommendations.

Open **See how this was worked out**, then **Agent map**. On this corresponding reply, show:

- NVIDIA: real request status, intent, measured latency and reported token usage, if configured and a new call actually ran.
- Zetaris: actual fixed directory-query outcome and duration.
- H-MEM: actual save outcome.

Expand **Discovery scope and actual tool results** for structured directory counts and operations. These are application execution records, not the Zetaris console. The separate `/registry.html` page runs a fixed Toronto Cat Rescue identity lookup; do not confuse it with the directory-list query.

Identical message/context pairs may use cached intent and show no new model call. Use a distinct natural phrasing for a new live model demonstration. Do not label a cached answer as a fresh request. There is no requirement that every follow-up use a model.

## 2. Follow a selected organization's observations

For a returned organization, say its full name, e.g. `Tell me about Community Cats Toronto`. This can reuse the existing website read. In the validated run the website yielded four pages describing services, not a verified individual medical fundraiser. Not finding a case does not mean no need exists.

Ask `show website history` from the directory list to recall the saved aggregate directory investigation. After selecting a site, history is scoped to that site; an aggregate directory save does not imply a separate site record exists.

## 3. Inspect a specific real appeal

Explain that the following link is **presenter supplied**, not discovered automatically by the preceding directory query:

> As a supporter, check https://guelphhumane.ca/news/urgent-abandoned-in-a-box-and-pregnant-lucy-needs-your-help/

The site requests a ten-second crawl delay. The reader waits and reads only this explicitly supplied page. Show the title, source quotes, pending status and H-MEM save. Ask:

> What evidence is missing?

> How much is still needed?

These follow-ups reuse the observation. Without verified corresponding costs, total received and other support, remaining funding is unknown.

A later published update is also readable:

> As a supporter, check https://guelphhumane.ca/news/update-lucy-gave-birth-to-her-kittens-at-ghs/

The organization published the first appeal on 13 October 2026 and the birth update on 14 October 2026. Do not present the earlier pregnancy as the latest condition. Reading these two pages does not establish that no newer updates exist. In the generic URL path the presenter supplies each URL; automatic cross-article chronology resolution is a separate curated workflow.

Ask `show website history` to show real H-MEM recall for the currently selected website. The earlier save and this recall are the useful engine feature, not simply an installed dependency.

## 4. Optional organization view

Use a role-play example, without claiming to actually represent the organization:

> I represent a rescue organization. Could you check our website and tell us what public information we should add to help donors understand and assess our work? https://communitycats.ca/

The reply shows a scoped checklist, advice and source observations. Related wording, not found within read pages and unable to assess are different states. General TNR information is not proof of a particular cat's medical need. The system does not edit the organization's website or accept private uploads.

## 5. Honest failure and limitation statements

Website content and access may change. Cat Busters has returned 403 in testing, while other websites redirect or require unsupported scheduling. Stop and disclose the result. Never swap in a saved success without labelling it.

No actual payments, current trust certification or independently authenticated medical documents are demonstrated. Nightshift is not live-connected; retain the operator's reported exception and confirm organizer requirements. NVIDIA direct is not Nightshift.

## Recording target

Keep slides and walkthrough inside the organizer's stated video limit (the team's supplied checklist says 1–4 minutes). A compact recording can show one natural request, one Zetaris result, one explicit case read, one gap/amount follow-up and one H-MEM recall, then briefly state limitations. Optional organization and failure examples can remain backup.

The final slide's localhost link works only on the presenter machine. For an external submission provide an accessible recording and public repository; this repo does not include a hosted production deployment.
