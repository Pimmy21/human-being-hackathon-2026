# Zetaris read-only integration evidence

24 October 2026. Local uncommitted working tree. No resource creation/modification, SSL change, credential disclosure or new model request.

## Preflight and live outcome

Read source-repository connection/SQL instructions first. The official preflight targets localhost and also requires REST; this deployment uses a remote JDBC-only instance. The application uses a scoped Windows/remote adaptation: configured credential presence, existing configured JAR/JVM, actual jaydebeapi/JPype imports and remote SSL check. All nine local checks passed. No dependency was installed or Java runtime copied. REST bearer credentials are not required for this JDBC probe.

The first real probe reached the 45-second client deadline without a usable result; saved as incomplete. It did not prove any connection/registry success. Instrumented per-stage progress and a bounded remote TCP test were then added for one separate diagnostic, not an automatic retry loop. That diagnostic completed SELECT 1, SHOW LIGHTNING DATABASES and the existing authorized tcr_identity SELECT, returning one row.

Actually read through Zetaris:

- TORONTO CAT RESCUE
- 720884691RR0001
- ETOBICOKE, ON
- 2024 reporting-year resource, as configured by the earlier approved table creation.

The returned row is consumed by `supporter_identity_view` as historical information. It never sets current registration, risk completion, medical need or case qualification true. It is not attached to the fictional Maple case or used as treatment-city evidence. Source dataset and reporting-year limitation are shown.

## Reproduction and constraints

Use a Python environment that already has jaydebeapi and JPype. Supply the actual .env.local and installed JVM library path:

`python -m purrpose.zetaris --env-file /configured/.env.local --jvm /configured/jvm-library`

This performs local preflight only. After seeing a passing preflight and with read access authorized, append `--live --output purrpose/artifacts/zetaris` for the bounded worker. SQL is fixed, single-statement and read-only. The current probe is intentionally scoped to the already approved deployment-specific database/table; another deployment must verify its source objects instead of assuming these names exist. Do not create them automatically.

The child worker has a 45-second process deadline. When stopped, remote read cancellation cannot be guaranteed; do not claim it definitely stopped on the server. Output redacts by returning sanitized error categories only, not raw exceptions. Missing/mismatched/historical data and source outages cannot become clean current-status evidence. No silent snapshot fallback.

## Tests and remaining work

Full offline/local-reference suite: **71 tests passed** (eight new Zetaris tests). Tests cover historical-only semantics, mismatches/duplicates, SSL restrictions, error sanitization, useful returned-name consumption, fixed read-only SQL and restricted configuration reading. They do not rerun the remote server.

Actual JDBC diagnostic is separate evidence from those unit tests. Current official registration/status and required risk coverage remain incomplete; no real fundraising case qualifies. Nightshift routing remains an independent uncompleted integration.
