---
description: Build, review, and revive Pattern Walker clients that consume server metadata, local config overlays, and binary traversal streams without domain-specific assumptions.
---

# Pattern Walker Client

Use this skill when working on a Pattern Walker browser client, stream consumer,
or client-side configuration bridge.

## Inherit First

Load the upstream Antifragile skills for epigenetic config, configuration,
testing, workflow validation, notebooks, scripts, and versioning before
applying this one. This skill only specializes client behavior for Pattern
Walker.

## Client Shape

A Pattern Walker client is a generic traversal and rendering surface. It should
learn domain language, rendering options, layers, and traversal affordances from
server metadata rather than from hardcoded TypeScript constants.

The client usually consumes:

- `/metadata` for domain terminology, endpoint capabilities, layers, styles,
  scales, frame policy, and function ids.
- `/domain/items` and `/domain/systems` for selection and navigation.
- `/topology`, `/trajectory`, `/visuals`, and `/layer` streams for rendering and
  traversal state.

The rendering stack should treat columnar binary streams as the fast path. Static
topology, dynamic trajectory, visual channels, and optional layers should remain
separate enough that updates do not force unrelated payloads to reload.

## Config Bridge

Use versioned public defaults plus transient local overrides when a browser
client needs runtime server coordinates. The durable contract stays in HOCON;
generated YAML or JSON files are deposits for the static client to fetch.

The local override may be absent. Absence means "use the public default", not
"the app is broken". Broken or incomplete fields inside an override should fail
at the typed config boundary.

Client package work stops at local build, local serving, static config deposits,
and browser verification. Docker images, deployment manifests, hosted client
routing, and environment-specific publication belong in the ecosystem wielding
module, for example `culture-wielding`.

## Visible Fixture Expectations

Client verification should prefer a Wielder test-mode data scenario over a
hand-maintained UI fixture. The domain server should expose a small fetched,
ingested, harmonized, and materialized dataset created by normal entry scripts
under `-t/--test`; the client should then consume that server exactly as it
would consume a larger local or hosted dataset.

The client may ship static fallback config and mocked component fixtures for
isolated UI development, but Pattern Walker revival is not complete until a
browser can render test-mode server data through `/metadata`, discovery, and at
least one stream family.

## UI Rules

- Generate labels, tabs, scales, layer names, and temporal controls from server
  metadata.
- Keep domain examples in fixtures, docs, or HOCON, not in reusable client
  components.
- Prefer explicit loading, empty, and stream-error states that distinguish "no
  data available" from "server contract failed".
- Keep the client dense and useful: it traverses, compares, filters, and renders
  what the reverse API advertises.

## Antipatterns

- Hardcoding biology, astronomy, or other domain terms in generic client code.
- Using browser-local assumptions to find server files or workspace paths.
- Treating a generated client config deposit as the source of truth.
- Coupling WebGPU buffer layouts to one domain's artifact names.
- Introducing persistent bidirectional state when simple HTTP binary fetches
  satisfy the traversal flow.
- Hiding deployment or Docker behavior inside the client package instead of the
  ecosystem wielding module.
- Calling a client revival complete with only static mocked UI data and no
  test-mode server stream to view.

## Validation Ladder

1. Build or typecheck the client.
2. Fetch public default config and transient local override from the served app.
3. Confirm the selected server was seeded through the domain Wielder test-mode
   entrypoint or an equivalent documented live fixture.
4. Fetch live `/metadata` and verify UI terminology comes from it.
5. Load representative domain items/systems and at least one stream family.
6. Cross-check a notebook or API test can inspect the same seeded data the
   browser is rendering.
7. Use browser verification for console errors, blank canvases, layout overlap,
   and stream-driven controls when frontend behavior changed.
