---
name: Antifragile Evolution During Live System Tests
description: Doctrine for evolving Wielder and Workspace systems while a real workflow/system test is running, using live failures and operator feedback as the highest-value design signal.
---


# Antifragile Evolution During Live System Tests

Wielder systems are allowed to evolve in the middle of a live system test when the test itself exposes the true boundary that needs refinement.

This is not chaos-driven development. It is disciplined live evolution under a configured harness. The workflow, ecosystem, images, publishers, consumers, data lake, and operator feedback are treated as one living test surface.

For reactive-system framing, read the local [Reactive Manifesto 2.0](the-reactive-manifesto-2.0.pdf). Treat it as conceptual grounding for responsive, resilient, message-driven, live-feedback systems; keep durable Wielder-specific rules in this skill, configuration doctrine, workflow validation doctrine, and app-form doctrine.

## Core Principle

A running system test is a legitimate engineering workbench.

When a real workflow exposes a missing config contract, weak orchestration boundary, brittle lifecycle assumption, or incomplete observability surface, the correct response is not to retreat into mocks or defer all change until after the run. The correct response is to make the smallest coherent source change, re-enter through the Wielder entrypoint, and let the system test judge the change.

This is antifragile because the system improves from stress:

- a failed plan sharpens config contracts
- a failed apply sharpens infrastructure and workload contracts
- a stuck pod sharpens scheduling, image, and runtime contracts
- a bad payload sharpens publisher and DAG contracts
- an operator question sharpens the human-facing workflow contract
- an ad hoc reactive mix-and-match run sharpens step configuration, event contracts, and app phenotype boundaries

## Rules

- **Live Feedback Is Signal:** Treat concrete failures from real workflow runs as higher-quality evidence than speculative unit tests or mocked success paths.
- **Evolve Through the Harness:** After changing source, return through the relevant Wielder `plan`, `apply`, `delete`, image, publisher, or workflow entrypoint. Do not make the live cluster the permanent source of truth.
- **Small Coherent Mutations:** Change one contract boundary at a time when possible: config shape, artifact transport, image build policy, scheduling, publisher behavior, or consumer behavior.
- **Do Not Hide the Scar:** If a live run reveals an architectural weakness, encode the improved rule in the foundation, skill, config schema, or workflow rather than leaving it as tribal memory.
- **Prefer System Truth Over Mock Comfort:** If a change only proves itself against mocks while the real workflow remains unexercised, the proof is weak.
- **Keep Provenance Honest:** If runtime code or image contents changed, respect image provenance and commit-pinned build discipline before relying on rebuilt images.
- **No Unowned Hot Patches:** Temporary cluster inspection is allowed. Durable fixes belong in config, Wielder entrypoints, application code, or explicit operational scripts.
- **Operator Ergonomics Matter:** If a human repeatedly asks how to run, observe, or recover a workflow, the workflow contract is incomplete.
- **Reactive Composition Belongs In Contracts:** When live pressure reveals that an app needs ad hoc combinations of entrypoints, promote stable entrypoints into the app contract and let resolved steps config select the transient sequence. Do not encode every combination as a separate script.

## Practical Loop

1. Observe the live system through Wielder logs, workload logs, datalake artifacts, and operator-visible state.
2. Identify the smallest boundary that owns the defect.
3. Make the source/config change at that boundary.
4. Run the narrowest Wielder proof first, usually `-w plan`.
5. Apply through the managed entrypoint.
6. Inspect the resulting workload, artifact, topic, or output.
7. Promote the learned rule into docs, skill, or reusable code if it should survive the incident.
8. When the incident reveals a useful reactive composition, promote the stable capabilities and step-selection contract without freezing the one-off run as the only workflow.

## Anti-Patterns

- Pausing all architectural refinement until after the system test, then forgetting the real failure mode.
- Bypassing Wielder with manual live cluster edits and calling the result fixed.
- Expanding a fix across multiple submodules when the live evidence points to one boundary.
- Treating live operator confusion as a user problem rather than workflow feedback.
- Adding sleeps or polling loops as the final architecture when a reactive event path already exists or is clearly needed.
- Encoding every ad hoc step combination as a new durable entrypoint instead of using a configured step set over stable app capabilities.

## Relationship to Other Skills

This skill complements Workflow Validation Doctrine. Workflow validation says the workflow is a real test harness. Antifragile evolution adds that the harness is also a sanctioned place to learn and improve the system while it is under real pressure.

Use [Wielder App Form](SKILL_WIELDER_APP_FORM.md) when live pressure exposes a new app phenotype, aggregate entrypoint set, or source-transform-sink form. Use the local [Reactive Manifesto 2.0](the-reactive-manifesto-2.0.pdf) as background for reactive design vocabulary, not as a replacement for Wielder-specific contracts.
