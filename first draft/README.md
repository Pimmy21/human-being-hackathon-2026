# Purrpose First Draft

Local v2.2 guidance revision: adds evidence-driven agent roles and bounded dispute resolution. Not yet uploaded. The wireframe remains the earlier synthetic illustration and does not implement this agent loop.

Three things to review together. This is an initial workflow and implementation draft, not a live product.

## 1. Interactive workflow wireframe

[Wireframe files](wireframe/) · [Instructions](wireframe/README.md) · [Prompt for a coding assistant](wireframe/PROMPT_FOR_AGENT.md)

Download or clone the repository, then open `first draft/wireframe/index.html` locally in Chrome or Edge. GitHub shows HTML source rather than running the interface. Keep its CSS and JavaScript files in the same folder. No install, API keys or backend are needed.

Try Supporter → Organization → public-update fixture → History → Developer trace. All case data, evidence and tool outcomes are synthetic. External API calls: zero. This does not integrate NVIDIA, Zetaris, H-MEM or Nightshift.

## 2. Plain English guide

[Read the human guide](guidance/HUMAN_GUIDE.md)

Start here for the product purpose, both user journeys and the main rules without implementation detail.

## 3. Full implementation guidance

[Read the full specification](guidance/FULL_GUIDANCE.md) · [Rule comparison map](guidance/RULE_MAP.md) · [Examples](guidance/EXAMPLES.md) · [Acceptance cases](guidance/ACCEPTANCE_CASES.md) · [Open decisions](guidance/OPEN_DECISIONS.md)

The human and detailed versions use R01–R17 to make comparison easier. A development assistant should read the relevant instructions and inspect actual files before assuming services or accounts exist. The acceptance cases describe work to verify; they are not passing implementation tests.

## Review with a development assistant

Open the downloaded repository as its workspace and provide `first draft/AGENTS.md`, then `first draft/wireframe/PROMPT_FOR_AGENT.md`. Ask it to inspect and exercise the workflow with existing tools and record findings in `first draft/wireframe/REVIEW_NOTES.md`.

Focus on workflow questions, contradictions and missing behavior. Do not introduce paid calls or real services just to review this wireframe. Running the assistant itself may use its own subscription quota.

## Status

The owner authorized sharing this first draft for team review. Core workflow, adapters, source permissions and real-case checks still require implementation/validation. Some policy and operational decisions remain explicitly open. No production deployment or product-policy change is authorized by this upload.
