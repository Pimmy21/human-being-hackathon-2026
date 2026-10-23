# Purrpose Team Handoff

Prepared 23 October 2026 for Shiyuan's one-day absence. English is the working language for this guide.

## Read this first

**Our purpose:** give animal rescue organizations of all sizes a fair chance to be seen, and help supporters examine requests through evidence rather than social media popularity.

**The first demo:** one fundraiser for a cat's medical care. Answer what is being requested, what supports it, how much remains if a calculation is justified, and what is not established. Later updates close the loop. Do not make donation-aftercare the primary experience.

Shiyuan confirmed Purrpose as the main direction for this handoff. The antenna proposal stays in `ideas/` for reference. Do not build both in parallel or claim final mentor/track approval.

## The most important operating rule

Keep building within the product boundaries below. Routine technical choices and reversible fixes should be handled by the team. Contact Shiyuan when a decision changes what the product promises, changes the definition of done, or needs her account authority. If she is unavailable, preserve the existing boundary and work on another task.

This guide is a detailed **implementation contract and handoff**, not a claim that the application already exists. On preparation, this GitHub repository contains proposals and documentation. The earlier local prototype has not been migrated here. Check `docs/handbook/07-status.md` before telling anyone a feature is ready.

## Read according to your role

| Reader | Start here |
|---|---|
| Everyone | This page, then [Product](docs/handbook/01-product.md) |
| Developer or coding assistant | [Engineering](docs/handbook/02-engineering.md), [Integrations](docs/handbook/04-integrations.md), [Delivery and acceptance](docs/handbook/05-delivery.md) |
| Designer or frontend developer | [Interface](docs/handbook/03-interface.md) and the data contract in Engineering |
| Evidence researcher | Product, the source intake rules in Engineering, and the evidence tasks in Delivery |
| Person debugging a blocker | [Troubleshooting and escalation](docs/handbook/06-troubleshooting.md) |
| Mentor | [Short overview](ideas/purrpose.md), acceptance criteria and unresolved questions |
| New teammate | [Status and setup](docs/handbook/07-status.md), then claim one small task |

## Do these things when the team starts

1. Choose a temporary coordination lead from the people actually available. No person is assigned without agreeing.
2. Confirm who owns evidence research, backend and integrations, interface, and review/demo preparation. One person can own multiple roles.
3. Clone this repository, read this guide and inspect the real files. Record tool availability without sharing secrets.
4. Claim a task from Delivery and open a branch. Start with case data and deterministic checks before model prose.
5. Post a short checkpoint when a meaningful task completes or a blocker changes. An update should say: done, evidence, next step, help needed.
6. Leave a restartable handoff before going offline: branch/PR, files, tests, current failure and next action.

## What not to wait for

Do not wait for Shiyuan to fix imports, CSS, broken relative paths, tests, branch conflicts, local setup or a model's missing citation. Use the routing table in Troubleshooting. Do not wait for a failed external API to recover before building labelled missing-data states and fixture-based tests.

Do wait for a product decision before making unsupported claims, expanding the target user, removing required evidence checks, or calling a simulation a real verification. Account owners decide new spending and cloud permissions.

## Give this to your coding assistant

> Read AGENTS.md and START_HERE.md in this repository. Then read the relevant handbook chapters. Inspect the implementation before assuming files or commands exist. Work on issue [number and task]. Preserve the product boundaries, source provenance and explicit live/replay distinction. Make a small reviewable change, run relevant tests, and report what actually ran. Resolve ordinary implementation choices yourself; escalate only the concrete boundary or access decision you cannot make.

Replace the bracketed text before sending. Do not paste API keys into a prompt. A tool cannot work while you are away unless an available person or a separately authorized execution setup actually starts it.
