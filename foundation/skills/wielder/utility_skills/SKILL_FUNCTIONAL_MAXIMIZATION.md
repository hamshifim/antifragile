---
name: Functional Maximization
description: Maximize and audit configurable tools, third-party models, services, and workflows for scenario coverage, advanced configuration, native output preservation, ecosystem boundaries, scientific honesty, fixture design, and maximal knowledge extraction from model or workflow results.
---


# Functional Maximization

## Goal

Maximize what a functional tool can honestly produce, expose, and teach without
confusing convenience outputs with scientific truth.

Use this skill for model-backed tools, search tools, scoring tools, ingestion
tools, simulation tools, provider APIs, or any workflow where the goal is to
prove the full functional envelope rather than merely make the happy path run.

The target is a configurable tool that:

- exercises the important input scenario shapes;
- serializes every supported advanced option;
- preserves maximal native outputs in compact, inspectable artifacts;
- keeps interpretation separate from raw/native evidence;
- keeps identity and role labels provisional when the domain is fuzzy;
- uses configured storage and ecosystem boundaries;
- creates a clean implementation example that older tools can be audited or
  refactored toward.

## First Reads

When working inside a Wielder/Antifragile project, read:

- the local `AGENTS.md`;
- the app/task markdown for the target tool;
- relevant Wielder skills for config, tests, notebooks, handoff, and versioning;
- relevant domain ontology or schema guidance before changing scientific,
  business, entity, project, or score semantics.

Use [Capability Surface Extraction](SKILL_CAPABILITY_SURFACE_EXTRACTION.md) when
the maximized function must become an operator-facing GUI, API, CLI, Wielder
entrypoint, notebook companion, or monitoring panel.
Use [App Incorporation](SKILL_APP_INCORPORATION.md) first when the tool is being
copied, revived, or adapted from a legacy repo so ownership boundaries,
fixtures, and project vocabulary are corrected before maximizing the native
capability surface.
For incorporation work, do not let maximization become early cleanup: first copy
the legacy/app surface verbosely, make it run minimally, and use a functionality
ledger to expose anything not imported.

## Workflow

1. Name the tool and the truth boundary.
   State what the tool natively does, what it does not do, and what would be an
   overclaim. Example: a forecasting model predicts a configured horizon; it
   does not natively explain causality. A ranking model emits native confidence
   or ranking metrics; those are not automatically truth labels.

2. Build scenario coverage before optimizing internals.
   Include positive cases, unsupported cases, edge cases, multi-entity cases,
   provenance/search cases, and failure cases. Unsupported scenarios are useful
   if they produce explicit sidecars and do not fake success.

3. Maximize input expressivity.
   Ensure config/request serialization covers all advanced options the tool
   supports or intentionally reserves. Defaults should live in config, with
   per-row or operator overrides where appropriate.

4. Maximize native knowledge.
   Prefer native calls/APIs that return richer outputs over convenience calls
   that only produce one artifact. Preserve structures, scalar metrics, bounded
   arrays, tensor summaries, parameters, timings, statuses, and failures. Do
   not dump huge tensors or opaque blobs blindly.

5. Keep interpretation honest.
   Preserve native metrics under native names. Do not rename confidence,
   ranking, or convenience scores into stronger scientific claims. Use the
   harmonization skill when downstream comparable records are needed.

6. Keep classification flexible.
   Treat roles such as candidate, target, actor, search hit, source entity, or
   workflow artifact as context-scoped observations unless the source truly
   asserts identity.
   Capture observable features and provenance instead of forcing permanent
   classes.

7. Use ecosystem boundaries.
   Use configured accessors, Bucketeers, app/runtime configuration, and the
   owning project's storage contracts. Do not bypass storage abstractions with
   local filesystem assumptions.

8. Validate with unit and operator surfaces.
   Unit tests should cover serialization, defaults, overrides, scenario
   selection, unsupported rows, and sidecar contracts. Operator validation
   should use the canonical plan/apply/test command only when the user asks to
   run it.

## Acceptance Shape

Functional maximization is acceptable only when:

- all configured scenarios produce inspectable outputs;
- successful scenarios produce real native artifacts;
- unsupported scenarios produce explicit unsupported/failure results and no fake
  artifacts;
- all advanced options serialize with defaults and override paths;
- provenance is preserved without pretending the native tool consumes it when it
  does not;
- cleanup, discovery, reads, and writes use configured ecosystem storage;
- native outputs remain inspectable for downstream harmonization.

## Generic Examples

For a native prediction model:

- unsupported rows should be explicit unsupported cases, not fake native
  files;
- supported rows should produce real native artifacts plus native confidence
  and inference summaries;
- search, preparation, prompt, or provenance inputs should be preserved while the native
  model settings remain honest about which inputs were actually consumed.

For a ranking or scoring model:

- native confidence, ranking, interface, and timing metrics should remain under
  native names;
- any harmonized score should be versioned and caveated;
- multi-payload behavior, success markers, project parsing, and source role
  labels should be audited for overclaim and forced-classification traps.
