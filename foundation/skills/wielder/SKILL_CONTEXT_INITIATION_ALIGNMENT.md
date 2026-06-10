---
description: Initialize agent context for a Wielder/Antifragile project by lightly skimming project/module roles, abstraction layers, and configuration ecology before classifying the session as new work or context recovery.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Context Initiation Alignment

Use this skill at the start of an agent session in a project that consumes Wielder or Wielder Antifragile doctrine, before task-specific planning or implementation, when the agent needs a minimal "where am I" base context.

This is a light orientation skill. Do not audit entrypoints, inspect deep diffs, choose an active runtime phenotype, implement changes, clean files, or create commits during initiation.

## Core Rule

First learn what kind of system you are standing in; then learn the configuration ecology that can express it into many operational phenotypes; then ask whether the operator is starting new work or recovering a lost/stale thread.

The skill output is a super-short report for each initiation step, followed by clarifying questions only when needed for orientation.

## Initiation Sequence

1. Read the local safety contract.
   - Read the host project's local agent contract when present, such as `AGENTS.md`.
   - Note repository boundaries, no-commit rules, no-revert rules, submodule/worktree/monorepo shape, and any host-specific safety rules.

2. Skim project and module roles.
   - Lightly inspect top-level READMEs, manifests, config roots, and package/module layout so the project can declare its own shape.
   - Expect modular and composable surfaces. Multiple entrypoints may simply express different configured uses of the same system.
   - Form a lightweight role/scope map: what each module says it does, what it visibly appears to do, and how confidently that is enough for orientation.
   - If the agent cannot tell where the task belongs or which boundary is authoritative, ask one concrete orientation question.

3. Locate abstraction layers.
   - Treat `wielder-antifragile` as the present open-source doctrine/governance layer; this skill is being read from it.
   - Locate `Wielder`, the expected runtime/toolkit counterpart that implements shared execution, configuration, and orchestration contracts.
   - Actively look for the host project's wielding modules: composition and orchestration surfaces that express modules into operational phenotypes through config.
   - Actively look for business, science, and data logic modules: domain functionality, analytical pipelines, data contracts, and product logic.
   - Actively look for libraries: reusable domain or technical modules shared by other layers.
   - Actively look for infrastructure modules: provider/runtime resources, deployment surfaces, and managed operational substrate.

4. Load configuration ecology.
   - Read [SKILL_CONFIGURATION_GUIDELINES.md](SKILL_CONFIGURATION_GUIDELINES.md) as part of initiation.
   - Treat configuration as the coded modulation layer that activates, suppresses, routes, and parameterizes system functionalities into concrete operational phenotypes.
   - Identify available config modulators and context pack locations at a high level, especially `context_conf`, ecosystem, stage tier, surface, security, app/deploy/workflow identity, and canonical accessors.
   - Do not assume which context pack or phenotype is active unless the user task requires that decision.

5. Route doctrine on demand.
   - Read [MASTER_SKILLS.md](../../docs/catalogs/MASTER_SKILLS.md) only enough to know which detailed skills exist.
   - Load detailed skills only when the task touches their surface.

6. Give a human-digestible gestalt recap.
   - Keep it short.
   - State the inferred project shape, module role map, config ecology, phenotype modulators, and authoritative boundary assumption.
   - Label uncertainty without resolving it unless it blocks routing.

7. End initiation with one question.
   - Ask: "Is this a new task, or are we recovering a lost/stale thread?"
   - Default to new work unless the operator mentions lost context, stale handoff, restart, compaction, confusion, or prior unfinished work.
   - If recovery, switch to [SKILL_CONTEXT_RECOVERY_ALIGNMENT.md](SKILL_CONTEXT_RECOVERY_ALIGNMENT.md).

## Gestalt Recap Shape

```text
Safety: <local contract in one phrase>.
Modules: <role/scope map in one phrase>.
Layers: <Antifragile/Wielder/wielding/business-lib-infra map in one phrase>.
Config: <configuration ecology and phenotype modulators in one phrase>.
Doctrine: <skills to load on demand in one phrase>.
Gestalt: <project shape and boundary assumption in one sentence>.

Is this a new task, or are we recovering a lost/stale thread?
```

## Anti-Patterns

- Turning initiation into a deep architecture audit.
- Validating entrypoint correctness during initiation.
- Choosing an active config phenotype before the task requires it.
- Collapsing Antifragile doctrine, Wielder runtime/toolkit code, libraries, business/science/data modules, wielding modules, and infrastructure into one undifferentiated codebase.
- Continuing into recovery from memory instead of switching to the recovery skill.
