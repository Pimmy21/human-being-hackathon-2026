# Validation and limitations

## Automated checks

The submission preparation runs the Python suite and JavaScript model checks locally. Tests use fixtures/mocks for remote integrations unless explicitly configured. They are not a substitute for live tool evidence.

```powershell
$env:PURRPOSE_HMEM_REFERENCE=(Resolve-Path '../meterless/engines/hmem/reference/src/index.ts').Path
.\.venv\Scripts\python.exe -m unittest discover -s purrpose -t . -q
node purrpose/test_api_client.cjs
node purrpose/test_agent_map.cjs
node purrpose/test_review_panel.cjs
node purrpose/test_live_panels.cjs
```

Without the reference environment variable, H-MEM integration tests skip. These checks do not automatically spend model credits, execute setup DDL or create cloud resources. `python -m purrpose.doctor` is a read-only local readiness check, not a live integration certificate.

Submission preparation result: **323 Python tests passed with official H-MEM configured, no skips**. All four JavaScript checks above and chat JavaScript syntax passed. The local readiness checker found no missing assets. A clean candidate-file snapshot started successfully without external credentials and served home/chat/architecture/JavaScript on a separate localhost port, without external or model calls. PowerShell launcher syntax passed; script execution was blocked by this machine's execution policy, so the documented explicit Python command was used instead. The instructions do not require changing that policy.

Local Markdown links and known local credential values were checked before publication; no broken links or credential exposure were detected. These are scoped release checks, not a security certification or full cloud reprovisioning test.

## Actually observed in the team's configured environment

- AWS Zetaris JDBC over SSL: SELECT 1, fixed Toronto Cat Rescue identity SELECT and directory SELECT succeeded. Directory returned 376 source rows, 47 cat-name matches, 28 usable unique historic contact addresses and 19 without one. These are observed counts from the 2024 source, not a permanent expectation or coverage of all cat services.
- Official Meterless H-MEM reference on Node: save and scoped recall succeeded. Directory history recall retrieved five stored records in one observed run. Counts depend on local state and are not fixtures a clean clone will reproduce.
- NVIDIA `nvidia/nemotron-3.5-lightning-30b-a3b`: one real natural-language request returned validated `list_organizations` intent and entered the live directory workflow. That observed call reported 573 tokens and 657 ms. Do not hard-code these measurements or promise the same values on another account.
- Community Cats Toronto website: four public pages were read; they provided organizational/service context, not a verified individual medical appeal.
- Guelph Humane Society Lucy appeal and birth update: each was read live after the permitted ten-second delay, saved, then reused for follow-ups. Later date/content is a publisher statement, not independent clinical confirmation. Related-news text was excluded to prevent borrowing other cases' amounts or medical statements.
- Cat Busters/other source access failures stayed incomplete, with no invented evidence or qualification.

Raw execution captures and H-MEM state remain local and ignored rather than being shipped as future live answers. API usage above is a historical observation, not an embedded recording or proof of current account credit.

## Not established

- Independent clinical document authentication, current charity/risk clearance, reliable same-case remaining funding or a real qualified donation recommendation.
- Automatic discovery of a current individual medical appeal for every candidate organization.
- General-purpose LLM conversation or autonomous evidence reasoning from all supported URLs.
- Live Nightshift inference in the team's validated environment. An operator-reported exception is not independently verified by this repository.
- A fresh cloud deployment from scratch or a production hosted multi-user service.

See [Architecture](ARCHITECTURE.md) for the separate curated/synthetic loops and generic live website checks.
