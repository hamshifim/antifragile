---
name: Capability Surface Extraction
description: Wielder doctrine for deriving the fullest honest operator-facing capability surface from an app, model, service, or module without duplicating domain logic, hardcoding config, or hiding provider-native functionality.
---


# Capability Surface Extraction

Use this skill when turning a working module, model, service, app, or workflow
into an operator-facing surface: GUI, API, CLI, Wielder entrypoint, notebook
companion, or monitoring panel.

Use [Functional Maximization](SKILL_FUNCTIONAL_MAXIMIZATION.md) first when the
main risk is under-exercising a third-party model/tool, dropping native outputs,
or overclaiming scientific meaning. Use this skill to project the maximized
capability into operator surfaces.

The goal is maximal honest functionality, not maximal UI size. A surface is
complete when it exposes the configured capabilities a real operator needs to
plan, configure, run, observe, debug, and clean up the module while preserving
the module's own semantics and source-of-truth boundaries.

This pattern was extracted from concrete app work but should remain generic.
Keep app-specific scientific semantics in the owning domain apps; promote only
the abstract capability-surface rules here.

## Capability Inventory First

Before designing UI or orchestration, inspect the module itself:

- core callable or computational service
- side-effect layer that writes durable outputs
- typed request/result models
- resolved config defaults, bounds, enums, and feature gates
- Wielder entrypoints and existing `plan`, `apply`, `run`, `delete`, `monitor`
  semantics
- event topics, lifecycle states, heartbeats, logs, and failure events
- input manifests, runtime config sidecars, native result artifacts, and
  success markers
- tests, notebooks, and existing operator commands

Do not start from the current GUI. The GUI is a projection of the capability
contract, not the contract itself.

## Capability Matrix

Build or mentally maintain a small matrix for each exposed capability:

- identity: human name, run name, batch/context name, owner, stage tier
- inputs: required fields, optional fields, advanced fields
- defaults: config owner and override path
- bounds: min/max values, enum choices, destructive thresholds
- action: `plan`, `apply`, `run`, `delete`, `monitor`, or domain verb
- state: planned, submitted, published, claimed, processing, stale, error,
  success, or the app's existing equivalent enum
- observability: logs, heartbeats, progress callbacks, status records
- artifacts: object keys, manifests, native outputs, derived outputs
- security: runtime identity, RBAC/IAM, secret boundaries
- validation: direct module test, API test, event-chain test, GUI test,
  workflow apply, hosted apply

Expose the matrix through typed contracts where practical. Pydantic models,
schema JSON, app config, and generated view JSON are better than hand-copied
React literals or ad hoc dictionaries.

## Config Owns Shape

- Defaults, max values, enum choices, test reductions, cleanup behavior,
  polling cadence, and enabled features belong in resolved config.
- The app baseline should be fail-closed when a behavior only belongs to a
  specific ecosystem.
- Production defaults should be meaningful for production. Test mode (`-t`) or
  explicit fixture overlays should carry short, cheap developer settings.
- Do not hardcode capability bounds in a frontend, service model, or runner
  when the app/ecosystem config can own them.
- Do not create a side loader to assemble a wider surface. Use the canonical
  accessor and add missing config to the responsible layer.

## Preserve Native Semantics

When wrapping a model, provider, or scientific service, keep its native shape
available at the correct layer:

- provider or model wrapper: native ontology and full diagnostic capability
- Wielder/app adapter: generic verbs, typed config, workflow identity
- domain app: scientific meaning, artifact semantics, harmonization rules
- GUI/API: operator projection over the typed contract

Do not rename native metrics into product semantics prematurely. For example, a
structure-confidence metric is not a binding score unless a downstream science
contract explicitly derives such a score.

## One Capability, Many Projections

Mini views, expanded views, API endpoints, notebooks, and CLIs must call the
same capability contract.

- A compact GUI view and expanded GUI view should share state, field bindings,
  validators, run actions, and status/log projections.
- The expanded view may show more fields, advanced config, JSON, liveness, and
  artifacts, but it must not become a second implementation.
- Changing a value in one projection must persist when switching projections.
- A run button in two projections must trigger the same function and receive
  the same status updates.
- Disabled controls should explain the minimal missing input on hover or click.
- Destructive or scale-to-zero actions should require explicit confirmation.

## Observability Is Part Of Functionality

A capability is not fully surfaced until the operator can tell what happened.

- Success must come from the runtime/event/artifact trail, not merely from a
  request being accepted or published.
- Workers should emit lifecycle logs and busy/liveness heartbeats that include
  stable run identity and relevant resolved runtime config.
- Servers should intercept runtime events and push compact status updates to
  clients.
- GUI logs should clear at the start of a new focused run, auto-scroll to the
  bottom, retain bounded history from config, and distinguish current run logs
  from older attempts.
- Artifact links and downloads should use server/accessor logic, not browser
  reconstruction of object-store keys.

## Extraction Ladder

Prefer this order when promoting a module into a larger surface:

1. Prove the core function without GUI.
2. Prove the side-effect layer writes the expected manifests, native artifacts,
   telemetry, and success/failure markers.
3. Prove the typed request/result/config round trip.
4. Prove API or entrypoint invocation.
5. Prove event publication, worker claim, liveness, completion, and callback.
6. Prove the GUI projection consumes the same typed shape.
7. Prove local hybrid apply when local iteration is involved.
8. Prove hosted image/deploy/apply when runtime code or containers changed.

Do not skip straight to UI polish if the service cannot yet be operated or
validated without the GUI.

## Consolidation Heuristics

Extract shared layers only after two concrete apps prove the common contract.
Until then, keep app-specific semantics honest and local.

Extract upward when:

- two or more apps need the same typed request/result/status pattern
- the same config-owned defaults/bounds shape appears repeatedly
- the same status/liveness/log panel pattern repeats
- the same artifact access pattern repeats
- the same Wielder entrypoint pattern becomes operator-facing

Do not extract upward when:

- the names only look similar but the science or provider semantics differ
- the shared layer would force one app's vocabulary into another app
- a thin local bridge is clearer than a generic loader
- the abstraction hides missing config or permissions

## Validation Handoff

When finishing a capability-surface change, report which rungs of the extraction
ladder were actually exercised. If hosted behavior depends on committed images,
hand off the exact image/deploy/apply commands or run them only when explicitly
asked.
