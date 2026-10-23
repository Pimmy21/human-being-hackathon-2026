# Actual Status Setup and Migration

Prepared 23 October 2026. This is a point-in-time record, not continuous monitoring.

## 1. What is actually in this GitHub repository

The repository contains short proposals, collaboration documents and this detailed Purrpose handoff. It does not yet contain a complete frontend/backend application, dependency manifests, model adapters or the earlier prototype code. There is no verified one-command Purrpose startup command yet.

The routes and structure in Engineering are proposed contracts for implementation. A teammate must not infer that `npm run dev`, `uvicorn` or an example endpoint will work before those files are actually added and tested.

## 2. Earlier work on Shiyuan's local machine

| Local component | Prior observed result | Limit |
|---|---|---|
| `pawproof-demo/` | Historical organization-report replay, designed local HTML report | Earlier product emphasis; does not verify a current case's unmet need |
| Official H-MEM reference | Real persistence and recall across processes; 13 reference conformance checks passed | Does not certify the new product or Nightshift provider |
| Earlier application tests | 10 checks passed for comparison, memory and model-output gates | New funding/case rules still need tests |
| `donation-feasibility/` | Two government identity records previously matched via Zetaris | Latest government read returned upstream HTTP 504 |
| `getting-started/` | Configured remote SSL JDBC connection; SELECT 1 and database listing passed | Setup and credentials are local to the machine |
| `nvidia-setup/` | Real hosted Nemotron call; previous assisted demo used 1,715 total tokens | Draft held for missing citations/unsupported attribution; not approved explanation |
| Nightshift | Browser explored and a job attempted | No successful application provider request recorded |

These results were observed during the earlier 22 October local experiment. No new paid/model/data calls were needed just to write this handbook. Do not change the dates or say that all services were re-tested today.

## 3. Starting from a new machine

Clone only the shared repository, then read the current files:

```sh
git clone https://github.com/sjd1ka/human-being-hackathon-2026.git
cd human-being-hackathon-2026
git status
```

Open the repository folder in your chosen coding workspace. Read `AGENTS.md` and `START_HERE.md`; explicitly give those files to an assistant if it does not load them automatically. Claim one task. Use a new branch, for example:

```sh
git switch -c feat/funding-checks
```

Check which Node, Python and Java runtimes are actually installed. Avoid installing another full stack before inspecting the implementation. The old TypeScript reference was run on Node 24. A new frontend/backend must have a committed manifest/lockfile and tested setup steps appropriate to the actual implementation.

Copy `.env.example` to `.env.local` locally when an adapter is ready. Fill only keys you are authorized to use. For fixture work, no cloud credentials should be necessary. Missing credentials must not prevent designing the frontend or testing pure funding rules.

Do not use Shiyuan's absolute Windows paths as your machine's paths. Do not upload the whole ChatGPT project mirror, `sources/`, downloads, screenshots or credential directories into this repo.

## 4. Migrating useful prototype work

The relevant local source folders are outside this repository. A person with authorized file access can review and migrate individual files. Others should not wait indefinitely for them: implement against the handbook contracts and official references.

Migration sequence:

1. Inventory individual source files and licenses, not entire folders.
2. Exclude `.env.local`, `.venv`, `.git`, local memory state, logs and generated artifacts by default.
3. Inspect code for hard-coded cluster endpoints, account identifiers not needed for public evidence, private data and absolute filesystem paths.
4. Preserve upstream notices for reused code. Pin upstream revisions; document how to obtain them. Avoid bundling copyrighted source PDFs by default.
5. Separate the useful H-MEM bridge, provider client and JDBC adapter from the old annual-report workflow.
6. Adapt to the new case schema. Do not rename an annual comparison and call it current-need verification.
7. Add tested environment loading with `.env.local`, explicit replay/live selection and sanitized failure reporting.
8. Run the new acceptance tests and a fresh-clone setup check. Record actual commands in `docs/runbook.md`.

## 5. Minimum runbook when implementation lands

The implementation PR must add: supported OS/runtime versions, dependency install command, local config steps, frontend/backend launch commands, fixture mode command, test command, provider check command, expected output, where state lives and how to stop the app. Distinguish optional external integrations from the credential-free fixture path.

Do not create a runbook with imaginary passing output. Have a teammate run it from a clean clone and record platform, commit and actual results.

## 6. Current work to claim

At publication of this guide, named technical owners are unassigned. The first coordination checkpoint should assign P01–P12 from Delivery. The immediate critical path is case data → schema → funding rules → main case page and backend review. Nightshift availability and real-case permission research can proceed alongside that work.

Team members may leave the provisional stack intact or improve it through a short recorded technical decision. Changing the main product or its acceptance gates goes to Shiyuan.
