# User-journey increment verification

24 October 2026. Windows, Python 3.12.14, Node 24.18.0. Local uncommitted code; nothing uploaded or deployed.

Executed with the official local H-MEM reference configured:

`python -m unittest purrpose.test_core purrpose.test_memory purrpose.test_journeys -q`

**36 tests passed:** 18 original core, 6 real H-MEM integration and 12 journey tests. No external paid inference or web requests.

Journey checks cover: city prompt without personal data; actual case city rather than headquarters; explicit expansion with and without matching pending cases; stable city/name ordering and separated lists; sourced output without default internal trace; unknown-city pending behavior; actionable organization funding gaps; failed-gate explanations even without missing fields; refusing unapproved/private URLs; fully funded cases separated; HTML escaping; mixed permitted/unpermitted URL rejection.

The example `journey_demo` command was run with scenario exhausted and real local H-MEM enabled. It generated supporter and organization results plus separate developer-run JSON. Both remain based on synthetic fixture evidence. No supplied URL was fetched, including the displayed example.invalid URL. The resulting HTML is a saved report, not an interactive web server or natural-language agent.

Headless Chrome verified two user-journey sections, no page errors and no horizontal overflow at 390 pixels. A desktop screenshot was visually inspected. `git diff --check` passed (only an informational Windows line-ending warning).

Current limitations: real evidence ingestion, generalized region/schema validation, conversational sessions, production source/model adapters, historical cutoff API and concurrent operation are incomplete. These checks do not establish all 127 guidance acceptance requirements.
