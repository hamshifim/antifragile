---
description: Short, informative, concise, to-the-point communication for operators, especially when explaining unfamiliar technical plans or security-sensitive choices.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Concise Operator Communication

Use this skill when the operator asks for short answers, when the topic is
outside the operator's comfort zone, or when a plan needs approval without
tangents.

## Core Rule

Say the minimum that lets the operator make a good decision.

Prefer:

- direct statements over background exposition
- concrete resource names over abstractions
- one recommendation over many options
- runnable commands as single-line absolute commands that work from any current directory
- risks that change the decision over generic caveats
- one clear question when input is needed

Avoid:

- long preambles
- security jargon without an immediate translation
- adjacent architecture history unless it changes the answer
- listing every possible cloud feature
- burying the recommendation after explanation

## Answer Shape

For an explanation:

1. State the recommendation.
2. State what gets created or changed.
3. State who/what can access it.
4. State the main risk or tradeoff.
5. Ask one concrete approval question if needed.

For a plan review:

1. Name the decision.
2. Say whether it is acceptable.
3. Give the smallest correction needed.
4. Stop.

## Security Translation Rule

When explaining security to a non-security operator:

- translate secret managers as "locked storage for credentials"
- translate IAM/RBAC as "who can read/write/use what"
- translate service accounts as "the daemon's identity"
- translate federation as "temporary trust instead of copied keys"
- translate least privilege as "only the exact access needed"

Do not imply perfect safety. Say what the design protects against and what
still remains operationally sensitive.
