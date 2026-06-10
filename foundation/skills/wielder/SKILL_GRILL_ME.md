---
description: Interactive one-question-at-a-time plan interrogation for reaching shared implementation understanding.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Grill Me

Use this skill when the user asks to be grilled on a plan, wants adversarial planning questions, or needs a shared understanding before implementation.

This is a planning skill. It may inspect code, update the planning/task
markdown, and sharpen decisions. It must not implement product/code/config
changes merely because a candidate plan mentions them. Execution starts only
after the user gives a separate explicit implementation instruction once the
plan is stable.

When repeated user corrections are converging into project doctrine, pair this
skill with [SKILL_OPERATOR_ALIGNMENT.md](SKILL_OPERATOR_ALIGNMENT.md): promote settled decisions into task
markdown, docs, config, tests, or glossary entries rather than keeping them only
in conversation.

## Protocol

1. Inspect before asking.
   - If a question can be answered from the repository, configuration, scripts, docs, tests, or existing command output, inspect those sources first.
   - Do not ask the user to restate facts already present in code.

2. Ask exactly one question at a time.
   - Keep the question concrete.
   - Explain why the answer matters only when that is not obvious.
   - Do not bundle several decisions into one prompt.

3. Include a recommended answer.
   - Format it as `Recommended answer: ...`.
   - Base the recommendation on inspected evidence when available.
   - If the recommendation is an inference, label it as such.
   - Do not let the user's current preference be the only basis for the
     recommendation. First test it against independent architecture concerns.

4. Wait for the user.
   - Do not proceed to the next question until the user answers or explicitly asks to skip.
   - After each answer, update the shared plan state in one or two lines, then ask the next question.

5. Stop when the shared understanding is actionable.
   - Produce or update a task markdown file as the durable output of the grilling process.
   - End with a concise plan containing decisions, file targets, validation commands, and unresolved risks.
   - Do not begin implementation unless the user explicitly asks to execute the plan after the planning discussion.

6. Preserve the plan/execution boundary.
   - During Grill Me, phrases like "add", "use", "create", or "wire" usually describe the desired plan unless the user explicitly says to implement now.
   - Keep implementation candidates in task markdown as planned files/steps, not applied code changes.
   - If execution intent is ambiguous, ask one question to confirm whether to keep planning or start implementation.

## Task Markdown Output

The grilling process should converge into a markdown file near the target code or owning app. Use a versioned `*_task.md` file when the task is intended to become durable repository doctrine. Use an ignored `*_stam.md` file for scratch alignment plans that should not be versioned. The task file should contain:

- goal
- inspected evidence
- decisions reached
- implementation steps
- planned files
- validation commands
- open risks or blocked decisions

Do not let the task markdown replace the one-question-at-a-time protocol; it is the artifact produced after the shared understanding stabilizes.

## Question Shape

```text
Question: <one decision or ambiguity>

Recommended answer: <the answer I recommend and why>
```

## Independent Architecture Stance

Before asking or recommending, briefly pressure-test the current plan through
these lenses. Do not roleplay them at length; use them to avoid being led into a
suboptimal architecture.

- System boundary: Is this component owning the right responsibility, or is it
  leaking downstream behavior?
- Data contract: Is the event/path/schema minimal, stable, and explicit?
- Operability: Can it be planned, applied, observed, retried, and rolled back?
- Failure semantics: Is idempotency, partial completion, and duplicate delivery
  accounted for?
- Migration path: Does the design support the known next phase without
  over-generalizing today?
- Provider fit: Is the chosen cloud/service near the consumer and appropriate
  for the required durability, fan-out, and cost?

If the user's answer optimizes one lens while damaging another, say so directly
and propose the smallest correction. Shared understanding is not the same as
uncritical agreement.

## Repository Discipline

- Prefer existing local abstractions and configured entrypoints over new wrappers.
- If the proposed plan implies a new framework abstraction, first ask whether the repeated use case is broad enough to justify it.
- Keep source/sink paths and credentials configuration-driven.
