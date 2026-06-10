---
description: Convert repeated operator corrections and repository evidence into durable doctrine, names, config, tests, and task handoffs.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Operator Alignment

Use this skill when the user is repeatedly correcting architecture boundaries,
naming, ownership, provisioning shape, or operational behavior. The goal is to
compress the shared understanding into the repository so future work does not
depend on conversation memory.

## Core Rule

Treat the operator's corrections as design evidence, but do not obey them
blindly. Reconcile each correction against code, configuration, docs, tests,
and system architecture concerns. Once a correction survives that pressure
test, promote it into durable project artifacts.

## Alignment Loop

1. Inspect first.
   - Read the relevant config, scripts, docs, tests, and task markdown before
     asking the user to restate context.
   - Prefer existing project words and boundaries over invented abstractions.

2. Separate correction from implementation.
   - A correction may settle a concept, naming rule, ownership boundary, or
     future plan without implying immediate execution.
   - If the user is in planning mode, update the task plan or docs first.

3. Promote settled corrections.
   - Put stable naming into config or constants.
   - Put stable behavior into tests or validation commands.
   - Put architecture decisions into task markdown or docs.
   - Put reusable vocabulary into the glossary.

4. Preserve operator sanity.
   - Prefer exact cross-provider names when the project has declared them as
     operator-facing identity.
   - Avoid unnecessary CLI idioms when config can own the decision.
   - Log source/destination/resource pairs in human-readable form when humans
     need to verify movement or provisioning.

5. Keep the model humble.
   - If the repo contradicts the user's recollection, point to the file and
     line or summarize the evidence.
   - If no evidence exists, say so directly and ask one concrete question.

## Architecture Pressure Test

Before adopting a correction, check:

- System boundary: Does this belong to provisioning, an app, a workflow, or a
  downstream consumer?
- Data tier: Is this raw evidence, standardized data, interpretation, or a
  derived product?
- Operability: Can it be planned, applied, retried, observed, and rolled back?
- Naming: Does it preserve human navigation across local, cloud, and documents?
- Migration: Does it support the next known phase without building speculative
  consumers now?

## Failure Modes

- **Performative correction:** Do not change a sound premise merely to satisfy
  a "critical assessment" posture. Critical assessment may conclude that the
  operator's current framing is already adequate, or that the smallest useful
  response is to name a caveat without changing code, schema, config, or
  doctrine.

## Compression Targets

Use the smallest durable artifact that captures the alignment:

- Config: when execution needs the value.
- Test: when behavior or contract can regress.
- Task markdown: when implementation is planned but not yet approved.
- Glossary: when a word is becoming project language.
- Skill: when the pattern should guide future agents across tasks.

## Anti-Patterns

- Keeping settled terminology only in chat history.
- Creating a new app or abstraction for what is only a new entrypoint or config
  subtree.
- Letting raw data ingestion include downstream interpretation.
- Building subscribers, schedules, or app runtimes before event contracts and
  provider boundaries are understood.
- Using provider-specific naming when the project has declared a cross-provider
  logical identity.
