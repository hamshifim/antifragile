---
description: Recover an interrupted or unclear Wielder task from current repository evidence without losing scope or existing work.
---

# Context Recovery Alignment

Recover the intended outcome, the work already completed, the remaining work,
and the authority to continue.

## Evidence to inspect

Start with the host safety contract and
[Foundations](../../../../FOUNDATIONS.md). Use the
[skills catalogue](../../../docs/catalogs/MASTER_SKILLS.md) for the surfaces
actually involved.

Inspect the current branch, dirty files and relevant submodule pointers.
A dirty gitlink alone does not describe the changes inside the submodule.
Read the relevant diffs, recent commits and task artifacts. Expand the search
only when these fail to establish the task.

Treat a handoff or summary as an index into evidence, not proof of current
runtime state. Distinguish observed results, intended work and hypotheses.
Do not infer intent from commit subjects alone when the current diff disagrees.

## Resuming

When the user's instruction and current evidence establish the goal and scope,
continue within that authorization. Compaction or a restart does not by itself
require a new approval round.

If there is a material conflict, report it and ask a focused question before
the affected action. Use [Grill Me](SKILL_GRILL_ME.md) when the operator requests
a planning interrogation or the decision genuinely needs that process; it is
not a mandatory gate for every recovery.

Briefly state the recovered outcome, relevant completed work and next action.
No fixed number of summaries or prescribed report headings is required.

## Boundaries

- Preserve existing work; recovery is not permission to clean or revert it.
- Do not revive a stale plan over the user's newer instructions.
- Do not expand commit, deployment or external-action authority through inference.
- Never turn an unverified prior success into a claim about the live system.
