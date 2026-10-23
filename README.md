# Human Being Hackathon Workspace

Shared workspace for our Open Agent Hackathon 2026 ideas, mentor feedback and eventual project submission.

**Purrpose is the active direction for the team handoff.** Start with [START HERE](START_HERE.md) for the detailed execution guide. Final track and submission decisions remain open. The two short overviews are:

- [Purrpose](ideas/purrpose.md): help donors examine animal rescue requests and their supporting evidence.
- [Antenna Design Comparison](ideas/antenna-design-comparison.md): help RF engineers and students compare antenna designs from research papers.

## What we need to decide

1. Which user problem do we want to work on?
2. Can we access enough suitable evidence or papers?
3. What is the smallest convincing demo we can finish?
4. What does our mentor think about the scope and track fit?

## Where files belong

- `ideas/`: short proposals for discussion.
- `docs/`: decisions, mentor feedback, setup instructions and integration responsibilities.
- Application code and tests will be added after we choose the project.
- Final approved presentation, demo instructions and submission links will live here too. Large recordings and datasets should be linked rather than committed.

This repository is the shared home for project files. Secrets stay in each teammate's local environment. Do not upload API keys, passwords, private donor information, or papers and images without permission to share them.

## Detailed team guide

- [Product purpose and boundaries](docs/handbook/01-product.md)
- [Backend architecture and data contract](docs/handbook/02-engineering.md)
- [Frontend and design](docs/handbook/03-interface.md)
- [Tool connections and calling methods](docs/handbook/04-integrations.md)
- [Team execution and definition of done](docs/handbook/05-delivery.md)
- [Troubleshooting and escalation](docs/handbook/06-troubleshooting.md)
- [Actual status, setup and migration](docs/handbook/07-status.md)
- [Copyable task prompts for assistants](docs/handbook/08-task-prompts.md)

Coding assistants should read [AGENTS.md](AGENTS.md). The guide tells people and tools how to work; it does not start unattended agents or provide credentials.

## Project status

The repository contains documentation and proposed implementation contracts, not yet a complete runnable product. Earlier local experiments with H-MEM, Zetaris and NVIDIA are not included here and do not establish that the new case workflow has been built. See the dated status chapter for precise evidence and limits.

See [Working together](docs/working-together.md) and [Tool responsibilities](docs/tool-responsibilities.md).
