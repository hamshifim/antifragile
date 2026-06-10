---
description: Recover a lost Workspace Codex thread by producing concise alignment summaries from doctrine, dirty diffs, task artifacts, and recent commits, then running Grill Me until the operator and agent agree on the recovered goal.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Context Recovery Alignment

Use this skill when a Workspace Codex thread, planning context, handoff, restart, context compaction, or tool event has lost the working memory for an active task and the operator wants the agent to recover orientation from repository evidence.

This is an inspection and alignment skill. Do not implement, clean files, create commits, delete artifacts, or repair adjacent modules during recovery. Resume execution only after the operator explicitly confirms the recovered goal or gives a separate implementation instruction.

## Core Rule

Do not continue from memory. Inspect first, summarize evidence, estimate the recovered goal, then use [SKILL_GRILL_ME.md](SKILL_GRILL_ME.md) one question at a time until the operator and agent are aligned.

## Concise Alignment Summary

A Concise Alignment Summary is a short, evidence-backed orientation statement.

Rules:

- Use 2-5 crisp sentences.
- State repository facts before inferences.
- Name the relevant module, surface, task artifact, or doctrine area.
- Avoid implementation planning unless the evidence directly shows planned work.
- Mark uncertain goal language as inference.

## Recovery Sequence

1. Announce the recovery boundary.
   - Tell the operator that the current step is context rebuilding only.
   - Do not create commits, clean generated files, or change product/config behavior during recovery.

2. Produce a doctrine-level Concise Alignment Summary.
   - Read [AGENTS.md](../../../../AGENTS.md) at the workspace root.
   - Read the relevant Wielder Antifragile foundation files, starting with:
     - [foundation/docs/catalogs/MASTER_SKILLS.md](../../docs/catalogs/MASTER_SKILLS.md)
     - [foundation/contracts/handoffs/SKILL_HANDOFF_PROTOCOL.md](../../contracts/handoffs/SKILL_HANDOFF_PROTOCOL.md)
     - [foundation/skills/wielder/SKILL_OPERATOR_ALIGNMENT.md](SKILL_OPERATOR_ALIGNMENT.md)
     - [foundation/skills/wielder/SKILL_SCOPE_GUIDELINES.md](SKILL_SCOPE_GUIDELINES.md)
   - Add configuration, workflow, security, provisioning, ingestion, notebook, imager, or Kubernetes workload skills only when the recovered diff or commits touch those surfaces.
   - If the operator asks about a named doctrine, skill, persona, or workflow, read that specific file.

3. Inventory task artifacts.
   - Search for task, TODO, handoff, plan, and report files with `rg --files` or `find`.
   - Read only files that appear relevant from names, recent modification, diff context, or commit history.
   - If task files conflict, are stale, or belong to a different domain, report them as ignored candidates and ask whether to include them during Grill Me.

4. Review the current diff across the super-repo and submodules, then produce a Concise Alignment Summary.
   - Run `git status --short --ignore-submodules=none` at the super-repo root.
   - Run `git submodule status --recursive`.
   - For every dirty submodule, run `git -C <submodule> status --short`.
   - Inspect `git diff --submodule=log --stat` at the super-repo root.
   - For dirty or task-relevant submodules, inspect `git -C <submodule> diff --stat` and focused diffs for changed source, config, workflow, and task files.
   - For untracked directories, list files and sample entrypoints/configs that define behavior before making a judgment.

5. Review recent commits, then produce a Concise Alignment Summary.
   - Read recent commits in the super-repo with `git log --oneline --decorate -n 8`.
   - Read recent commits in dirty or task-relevant submodules with `git -C <submodule> log --oneline --decorate -n 8`.
   - Prefer branch names, commit subjects, touched paths, and nearby diffs over inferred project intent.
   - Do not infer intent from commit history alone when the current diff contradicts it.

6. Estimate the recovered goal.
   - Write 1-2 super concise sentences.
   - Separate fact from inference when the goal is not directly stated in files, commits, or task artifacts.
   - Prefer "The likely goal is..." over overconfident phrasing when evidence is partial.

7. Run Grill Me until aligned.
   - Ask exactly one question at a time.
   - Include `Recommended answer: ...` with each question.
   - Base the recommendation on inspected evidence and label it as inference when needed.
   - After each operator answer, update the recovered goal in 1-2 sentences.
   - Stop when the goal, scope boundary, target files/modules, and next validation step are clear.

## Output Shape

Use this compact order:

1. **Doctrine summary:** Concise Alignment Summary.
2. **Diff summary:** Concise Alignment Summary.
3. **Commit summary:** Concise Alignment Summary.
4. **Recovered goal:** 1-2 sentences.
5. **Grill Me:** one concrete question plus a recommended answer.

Mention task artifacts inside the diff or commit summary when they materially affect the recovered goal. If task artifacts are the dominant evidence, add one sentence to the diff summary rather than creating a long separate report.

## Current-State Heuristics

- If the super-repo shows only submodule dirtiness, do not treat that as a meaningful code diff by itself. Inspect inside the submodules.
- If a submodule contains untracked source and config together, treat it as an active implementation candidate until the operator says otherwise.
- If broad Antifragile skill files changed together, look for a cross-cutting doctrine addition before reviewing each file as separate task work.
- If recent commits mention config, workflow, ingestion, provisioning, cloud auth, or Kubernetes workloads, load the matching foundation skill before proposing next steps.

## Anti-Patterns

- Asking the operator to restate the task before inspecting available evidence.
- Continuing a lost thread from memory without reading the repository.
- Editing code while still discovering which task is active.
- Cleaning generated files, caches, notebooks, or temporary outputs as part of context recovery.
- Collapsing facts and inferences into one confident narrative.
- Starting implementation during the Grill Me loop unless the operator explicitly ends planning and asks for execution.
