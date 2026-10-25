# Start here: Purrpose

This repository is a shared implementation workspace. Work can continue as a relay across time zones; no standing task assignment is required. Never assume another person's credentials or local runtime exist.

For local setup, start with [the current application quick start](purrpose/README.md). Run `python -m purrpose.doctor` for a no-network environment check.

## For a person

Read [the plain English guide](first%20draft/guidance/HUMAN_GUIDE.md), then [the current handoff](HANDOFF.md). Record unclear requirements and product questions for discussion. You do not need to understand every technical document to review the purpose and behavior.

## For an authorized coding assistant

1. Read root AGENTS.md and HANDOFF.md.
2. Read [full guidance](first%20draft/guidance/FULL_GUIDANCE.md), [build plan](first%20draft/guidance/BUILD_PLAN.md), [examples](first%20draft/guidance/EXAMPLES.md), [acceptance requirements](first%20draft/guidance/ACCEPTANCE_CASES.md) and [open dependencies](first%20draft/guidance/OPEN_DECISIONS.md).
3. Inspect the actual checkout, working tree, branch and configuration. If the tree is clean, fetch and fast-forward the intended shared branch before work. Preserve local changes; stop to resolve a divergent branch rather than resetting or force pushing.
4. Read [application instructions](purrpose/README.md). Run existing tests and choose the next small incomplete task from actual state. No task is reserved for a particular person. Missing live access does not block fixture-based work.
5. End with a tested, reproducible increment and update HANDOFF.md. Commit/push only when the person operating this assistant has authorized it. A local edit is not a shared GitHub update.

Reading this file does not itself authorize purchases, API spending, publishing or messaging others. Use recorded permissions and ask the current operator for missing access only when needed. Do not reopen confirmed product rules; record proposed changes and continue independent work.

## Relay routine

Before coding, check the latest handoff and commits. Before ending, record what changed, what actually ran, known failures and the next useful step. Prefer a small working increment over unexplained half-finished changes. If interrupted, explicitly mark unfinished behavior and failing/unrun tests. Never claim a provider works because a different machine connected successfully.

If work overlaps unexpectedly, coordinate or use separate branches before editing the same area. Never overwrite another developer's uncommitted work. Secrets, private evidence and local memory stay outside Git. Public deployment is a separate decision.
