# Purrpose Guidance v2.1

**First draft published for review with owner approval. Not approved for production deployment.**

Revised 24 October 2026. This package is intended for any authorized implementer and their AI development assistant. It requires no knowledge of the original conversation, a particular team, a particular repository or a developer's country of residence. This copy is published for review with owner approval. It is not a completed product or production deployment approval.

## Two versions of the same product rules

- **For people:** [Human guide](HUMAN_GUIDE.md), a plain-English explanation of what the product does and what to approve.
- **For development assistants:** [Full implementation guidance](FULL_GUIDANCE.md), precise workflows, data responsibilities, integrations, errors and acceptance behavior.
- **For comparison:** [Rule map](RULE_MAP.md), stable rule IDs linking the human explanation to exact specification sections and acceptance tests. The human guide simplifies language, not requirements.

Implementation supporting files:

1. [Input and output examples](EXAMPLES.md): concrete behavior and failure scenarios.
2. [Acceptance cases](ACCEPTANCE_CASES.md): observable checks to implement and run.
3. [Open decisions](OPEN_DECISIONS.md): unresolved policy and operational settings, with the responsible role.
4. [Configuration example](policy.example.json): the Ontario reference configuration and explicit unconfigured blockers, not a deployed application.

[AGENTS.md](AGENTS.md) gives implementation assistants a short entry point. All normative rules are in the linked documents. No credentials, account access, permission to publish or unattended execution are provided by this folder.

## Status terminology

- **Specified product rule:** a product requirement written in this package, independent of any original conversation.
- **Implementation contract:** a concrete proposed representation that implements confirmed behavior; developers may improve internal structure while preserving observable behavior.
- **Open:** requires access, source validation, a configured operational value or a product decision. Do not interpret an empty setting as permission to skip a check.
- **Reference example:** an illustrative configuration or scenario, not proof of a deployed implementation.

Frontend design is intentionally deferred. Required information and interactions remain specified so that backend work does not depend on a visual design choice.

## What this draft is not

It is not a complete runnable application, a successful live all-provider demo, a legal background check, or proof that a real fundraising case meets the gates. Acceptance cases are requirements to implement, not passing test results.

This first draft is shared in the project repository for review. It does not authorize live deployment, paid integrations or product-policy changes. No prior account, prototype, dataset table or local filesystem path is assumed.
