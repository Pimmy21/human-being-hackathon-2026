# Frontend and Design Brief

## 1. Visual goal

Purrpose should feel warm, calm, credible and easy to inspect. The user should immediately understand what help is requested, which facts have sources, and what remains unknown. The primary experience is evaluating a need, not viewing annual changes after a donation.

Suggested starting palette: warm ivory background, deep green text/action, white evidence surfaces, restrained amber for clarification. Treat these as design suggestions. Verify contrast in the actual combinations. Use a readable sans-serif font, body text around 16px, clear headings and a comfortable content width. The designer may refine colors, spacing and component details without waiting for Shiyuan.

Use one modest cat/paw brand detail. Do not create a dashboard full of badges, glowing charts or unnecessary animations. Do not use a green check that implies certification of an organization. Do not rank suffering, use pressure countdowns, or sort cases by social popularity.

## 2. Screens and states

### A. Case entry

Heading: “Understand a rescue request before you help.” Explain in one sentence that Purrpose collects evidence and shows what is still unclear. Offer the curated case and a clear “Check this request” action. If a paste-link field is not implemented, do not display it as functional. A future-feature label is better than a fake interaction.

Display “Synthetic demo,” “Historical replay” or “Public case” near the case title. For a synthetic animal, use an illustration and identify it. Do not use an invented generated photograph as evidence of a real rescued cat. For a real case, verify permission for images and preserve attribution.

### B. Review in progress

Show real stages: reading selected sources, checking case details, reviewing funding, preparing explanation. Only mark a stage complete when the backend reports it. No fake progress percentages or pretend browsing. A source failure should produce a completed-with-gaps state rather than an indefinite spinner.

Allow cancellation of new work and retain the run ID. A long model load may take time; explain this without implying a result is imminent. Prevent duplicate submissions.

### C. Evidence review

At the top: case/organization, requested help, reporting dates and scenario label. Below it, show these sections in order:

1. **What is being requested?** Brief treatment request and source label.
2. **What supports the request?** Claim cards with evidence label and “View source.”
3. **What do we know about funding?** Cost, reported or confirmed funds, remaining value only if justified, timestamp and calculation basis.
4. **What still needs checking?** Specific missing facts or conflicts with a practical next question.
5. **Ask about this case.** Suggested questions and one text question field.
6. **Later updates.** A secondary section showing saved evidence and selected subsequent records.

Keep the unknown-state explanation next to the unknown amount. Never write “CAD 0 needed” because the backend returned null. Never change the backend's evidence label to a more reassuring phrase for presentation.

### D. Source drawer or expanded card

Show source title, author/publisher, original link or permitted file label, excerpt, document page/section, source date, capture time, origin group and the claim it supports. Explain a source's limitation in plain English. Allow keyboard close, visible focus and return focus to the trigger.

Multiple excerpts from one source can share a source ID. Do not inflate the source count. If a source is unavailable, preserve metadata and label it unavailable. A saved snapshot needs a capture date and replay label.

### E. Funding detail

Show the arithmetic in a readable way, for example “Estimate − non-overlapping disclosed funds.” Show a distinction between money received and money pledged. If the grant inclusion is unclear, display “We cannot calculate a reliable remainder yet” and the question that would resolve it.

Use the backend result. The frontend should format amounts and dates, not independently decide what is eligible funding. Avoid progress bars when the denominator or funding completeness is unknown.

### F. Follow-up and memory

The user can inspect a prior reviewed version and add a selected update. Show “Earlier record” and “New evidence,” relevant differences, and unresolved questions. If memory could not be saved, say so; do not display “We will remember this” anyway.

## 3. Required component states

Every main component needs loading, empty, success, partial and error states where applicable. Specifically cover: first visit without memory; historical identity only; no cost document; stale funding; unknown grant inclusion; mismatched case IDs; failed government API; invalid model citation; unavailable provider; and successful evidence comparison without AI prose.

Display friendly messages such as “The government source did not respond. We have not refreshed this identity check,” rather than “The charity failed verification.” Technical failure is not negative evidence about the organization.

## 4. Accessibility and mobile checks

- All essential actions work with keyboard and visible focus.
- Color is not the only evidence label. Use text and optional icons.
- Body text and controls remain readable on a 390px-wide viewport.
- Cards stack on narrow screens; wide numeric tables scroll inside their own container rather than widening the page.
- Links have descriptive names. Charts are optional; numbers and text must remain understandable without them.
- Respect reduced motion. Check headings, button states, screen-reader labels and drawer focus.
- Test real long titles, unknown amounts and multiple source errors, not only the attractive happy path.

## 5. Design models and skills

During development, ChatGPT or Codex can help write the interface brief; an available design skill can implement or critique it; an image model can create optional decorative brand assets. A developer must inspect the result and ensure it follows the source data contract.

These are development tools, not runtime evidence verifiers. Using two models does not make a fact independently corroborated. A runtime vision model for PDF reading is optional and requires an evaluated adapter, document permission and a recorded provider call. Do not introduce another provider simply to claim more integrations.

## 6. Frontend handoff

Build against the response contract in Engineering. Keep mock fixtures in an explicitly synthetic fixture folder. Let the backend integration owner confirm the finalized response before wiring live calls. Record which screen uses fixtures and which actually uses the backend.

A frontend PR includes desktop and mobile screenshots, tested interactions, error-state screenshots and a list of remaining mocked actions. A screenshot alone is not a functioning demo. The main review, source inspection, follow-up and update actions should be exercised in the browser.
