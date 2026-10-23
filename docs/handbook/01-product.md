# Product Purpose and Boundaries

## 1. The product in plain English

Purrpose helps people examine an animal rescue request before deciding whether to support it. We want organizations of all sizes to have a fair chance to be considered. A large following is not evidence that a request is genuine; a small following is not evidence that it is unworthy.

Our main question is:

> I want to help a cat. What is this fundraiser asking for, what evidence supports it, how much is still needed, and what has not been checked?

We do not assume in advance that an appeal has a genuine unmet need. We investigate what the available evidence can support. We also do not treat missing evidence as proof of dishonesty.

The first user is a prospective supporter. Rescues benefit from knowing which documents or explanations would make a request easier to evaluate. We do not initially build a separate rescue dashboard or promise exposure to an audience we do not yet have.

## 2. Working MVP scope

- One curated case involving a cat's medical care in Toronto or Ontario.
- One rescue, one case identifier and a small set of permitted sources.
- English desktop and mobile web experience.
- A dated treatment request or cost document, funding information where available, and clear unknowns.
- A follow-up question and a later evidence update to demonstrate memory.
- No account sign-up or handling of actual donations. Use demo aliases and non-sensitive data.

This is a manageable demonstration scope, not a restriction that the eventual product can only serve small organizations. Broad discovery across all organizations is a future capability.

## 3. User stories and expected answers

**As a supporter, I can review a case without searching ten websites.** Show a concise request, evidence cards, funding information and questions that remain.

**As a supporter, I can ask why a statement is supported.** Show the original source, relevant excerpt, date and limits. Opening a source is optional for the user, but possible.

**As a supporter, I can distinguish a disclosed amount from a confirmed amount.** Put the label next to the figure. Do not hide uncertainty in a footer.

**As a returning user, I can add an update.** Retrieve the saved record, compare the relevant claims and preserve the earlier version. The original need-verification journey remains the main experience.

**As a rescue with little visibility, my case is evaluated using the same evidence fields.** The demo does not sort by follower count or award a better rating for professional graphic design.

## 4. Evidence labels

Apply labels to individual claims, not to an entire organization:

| Label | Meaning | Example |
|---|---|---|
| Supported by cited evidence | A specific, sufficiently scoped statement is supported by a readable source | The dated document lists an estimated treatment cost of CAD 2,000 |
| Reported by fundraiser | The fundraiser states it; independent corroboration is not present | The rescue reports CAD 700 raised |
| Needs clarification | A conflict, overlap or missing connection prevents a conclusion | It is unclear whether the grant is already included |
| Out of date | The information does not meet this case's stated freshness needs | An old fundraising total cannot establish today's balance |
| Not established | Available material does not support an answer | Current remaining funding cannot be calculated |

Do not use overall “verified charity,” “safe donation,” “fraud,” “corrupt,” “guaranteed impact” or a trust score. Registration identifies an organization within the source's period; it does not authenticate a treatment request. A document that looks professional is not authenticated by appearance.

## 5. Funding logic

Use currency amounts in integer minor units, such as cents. Preserve the original text and currency. Store source dates and whether an amount is an estimate, commitment, reported receipt or confirmed receipt.

The simplified calculation is:

`remaining = max(0, eligible case cost - non-overlapping funds available for that case)`

It is permitted only when the case, currency, scope and reporting period are compatible, overlaps are resolved, and the disclosed funding coverage is sufficient for the stated result. A commitment is not cash received. Do not count both. A paid bill and its earlier estimate must not become two separate costs. A grant included in a total must not be subtracted again.

If completeness of funding is unknown, do not call the result the current remaining need. You may show a clearly labelled calculation based on disclosed figures, or show no numeric remainder. An estimated cost cannot become an exact bill. Unspent organization reserves do not automatically eliminate a case's need; restrictions and allocations may differ.

Missing figures are `null`, never zero. Do not invent exchange rates. Different currencies produce a blocked comparison until the scope is resolved. Overfunding produces remaining zero plus a separate excess amount; it is not a finding of wrongdoing.

## 6. Synthetic example for testing

This is invented and must always be labelled synthetic. Treatment estimate CAD 2,000; raised CAD 700; grant CAD 300. If the grant is separate and all eligible funding is covered, disclosed remaining is CAD 1,000. If the grant is included in the CAD 700, it is CAD 1,300. If that inclusion is unknown, the exact remainder is not established. The agent should identify the missing question instead of choosing whichever answer looks better.

## 7. The final layer of the cycle

After support, compare disclosed treatment, receipts and outcomes with the original request. State what the update supports and what is still missing. Public financial reports do not trace an individual contribution to a particular expense. We do not have bank transactions or donor-level allocation records.

A documented successful case adds relevant history for that organization. It does not guarantee its next appeal, nor automatically improve another organization's credibility. Corrections and poor outcomes also remain in the history.

## 8. Changes requiring Shiyuan's product decision

Changing the target from animal rescue to all charities; replacing the main journey with after-donation tracking; adding scoring or certification; adding real payments; accepting private sensitive documents as a new user flow; changing evidence labels; weakening the definition of done; presenting synthetic cases as real; or dropping a required sponsor feature.

Technical choices such as component structure, test tools, accessible colors, data validation libraries and local storage implementation can be made by the team, provided they preserve this contract and add no unauthorized cost.
