---
description: Consulting mode for provisional architectural discussion, conflicting hypotheses, tradeoff exploration, and decision hygiene without turning operator indecision into implementation, config, or downstream handoff residue.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Consulting Mode

Use this skill when the operator says "consulting mode", asks to explore
conflicting options, wants critical assessment without implementation, or is
deliberately thinking through unsettled architecture.

## Core Rule

Consulting mode is discussion, not instruction.

Treat operator statements as provisional evidence unless they explicitly mark a
decision or ask for implementation. Do not let exploratory tension become
durable architecture, config, tests, doctrine, commits, or downstream handoff
context.

## Activation And Exit

Activation phrases include:

- "consulting mode"
- "let's talk through options"
- "critically assess"
- "I am not sure"
- "bring up conflicting modes"
- "no implementation"

While active:

- do not edit files
- do not create commits
- do not create durable docs or skills
- do not run mutating commands
- do not convert exploration into requirements

Exit requires an explicit transition such as:

- "decision: ..."
- "promote this"
- "implement this"
- "exit consulting mode"
- "make the change"

If the operator asks for implementation while contradictions remain, first name
the chosen interpretation in one sentence, then proceed only if the request is
clear enough.

## Response Shape

Prefer short, labeled sections:

- **Hypotheses:** plausible explanations or designs
- **Tradeoffs:** what improves and what gets worse
- **Recommendation:** the current best path, if one exists
- **Decision Status:** settled, provisional, or unresolved
- **Next Evidence:** the smallest inspection or plan command that would reduce
  uncertainty

For small questions, a compact version is enough:

```text
Hypothesis A: ...
Hypothesis B: ...
Recommendation: ...
Decision status: unresolved.
No implementation implied.
```

## Decision Hygiene

Use explicit labels so later context recovery can separate signal from
exploration:

- **Hypothesis:** may be wrong; needs evidence
- **Preference:** an operator or agent inclination, not binding yet
- **Tradeoff:** a consequence to consider
- **Rejected Option:** considered and set aside for a named reason
- **Decision:** settled direction
- **Promote:** permission to turn a settled pattern into config, docs, tests, or
  skill doctrine
- **Implement:** permission to make code/config changes

Do not describe a hypothesis as a decision. Do not put a preference in a
handoff as if it were implemented architecture.

## Anti-Poisoning Handoff Rule

When writing a handoff after consulting mode:

- include settled decisions
- include unresolved questions only under **Open Questions**
- omit rejected speculation unless it prevents a likely repeated mistake
- state "No implementation was requested" when the session stayed exploratory
- do not carry over every brainstormed branch as future work

If the operator asks to "promote this", move only the settled rule into the
smallest durable artifact:

- config when execution needs the value
- test when behavior can regress
- task markdown when implementation is planned but not approved
- skill when future agents need the pattern across tasks

## Boundaries

Consulting mode does not block harmless inspection when evidence is needed, but
inspection must be labeled as evidence gathering. Prefer non-mutating commands
such as `git status`, `rg`, `kubectl get`, Wielder `-w plan`, or read-only
cloud queries.

If cloud auth, MFA, or session expiry blocks the inspection, follow the package
auth boundary and ask the operator to refresh credentials rather than patching
around it.

## Anti-Patterns

- Editing code because a hypothetical direction sounded attractive.
- Adding config or doctrine because the operator wondered aloud.
- Treating "critically assess" as permission to refactor.
- Letting old exploratory statements override the newest explicit decision.
- Writing a handoff that preserves all indecision as equal-priority context.
