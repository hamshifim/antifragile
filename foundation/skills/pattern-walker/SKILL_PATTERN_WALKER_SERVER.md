---
description: Build, review, and revive Pattern Walker reverse API servers that expose domain data through generic validated metadata and binary traversal streams.
---

# Pattern Walker Server

Use this skill when designing, implementing, or reviewing a server that presents
domain data through the Pattern Walker protocol.

## Inherit First

Load the relevant upstream Antifragile skills before applying this one:

- Epigenetic config contracts for HOCON as the source of truth and Pydantic as
  the executable contract.
- Configuration guidelines for file layout, local overrides, and server-owned
  paths.
- Wielder scripts for thin, repeatable operational entrypoints.
- Test guidelines for in-process and live API validation.
- Workflow validation guidelines for Wielder `-t/--test` scenario overlays.
- Notebook guidelines for visible API/data inspection surfaces.
- Git versioning when recording completed server changes.

This skill adds Pattern Walker shape. It should not duplicate those rules.

## Server Shape

A Pattern Walker server is a reverse API provider. It adapts one domain's
storage into generic Pattern Walker records and streams while leaving
domain-specific ownership in that domain repo and its HOCON config.

The normal endpoint family is:

- `/metadata`
- `/domain/items`
- `/domain/systems`
- `/topology/{entity_id}?granularity={lod}`
- `/trajectory/{entity_id}?granularity={lod}&frame={n}`
- `/visuals/{entity_id}?granularity={lod}`
- `/layer/{entity_id}/{layer_name}?granularity={lod}`
- Optional `/functions/{behavior_id}` for explicitly advertised behavior.

Servers should validate metadata with the `pattern-walker-lib` protocol models,
serve stream payloads in documented binary formats, and keep topology,
trajectory, visuals, and layers as separate concerns.

## Wieldering Way

Prefer a versioned HOCON contract consumed by `pattern-walker-lib` Pydantic
models over domain code hand-building descriptors. The caller owns config
correctness. The library owns validation and functionality. If the contract
breaks, fail clearly at the boundary instead of hiding it behind defensive
fallbacks.

Domain repos may provide resolved paths, catalogs, and materialization outputs
from their own config, but generic descriptor parsing and protocol semantics
belong in `pattern-walker-lib` once they are shared by more than one domain.

Dockerfiles, deployment manifests, hosted runtime launchers, and
ecosystem-specific image wiring do not belong in the server package. Route them
to the wielding module for the ecosystem, for example `culture-wielding`, and
keep the server as a local, testable protocol surface.

## Test Data Mode

A Pattern Walker server should not be revived against an empty world unless the
task is explicitly about empty-state behavior. Use Wielder test mode to automate
the smallest honest data chain that gives the server something visible to
serve:

- fetch or synthesize a named source fixture;
- ingest it through the domain app's normal entry script;
- harmonize it through the domain harmonization path, preserving raw/native
  records and key lineage;
- materialize Pattern Walker ledgers and streams;
- start the local reverse API; and
- validate with API integration tests and notebook companion views.

`-t/--test` selects the fixture overlay. It does not select the action. The same
entrypoint should support ordinary Wielder actions such as `-w plan`,
`-w apply`, and `-w delete` with the test scenario active. Scenario identity,
fixture size, expected source ids, output roots, cleanup policy, and validation
toggles belong in HOCON, not in pytest-only flags or ad hoc Python branches.

## Implementation Rules

- Back discovery endpoints with a small metadata ledger or index; avoid O(N)
  directory walks on request paths.
- Keep source data, generated chunks, and presentation streams distinct.
- Treat metadata as the UI/control contract: terminology, layers, scales,
  styles, temporal controls, and available functions should be advertised there.
- Serve binary streams as stable protocol payloads, not ad hoc JSON expansions
  of large arrays.
- Gate optional function payloads by metadata/config ids; never serve arbitrary
  filesystem paths.
- Keep ports, hosts, artifact roots, and client config deposit paths in HOCON or
  derived local overrides.
- Keep test fixture outputs in ignored sandbox roots or configured local bucket
  paths. Do not commit generated Arrow, Parquet, screenshots, or notebook output
  data.
- Maintain a small `tests/TESTS.md` or equivalent index for live Pattern Walker
  surfaces when the server owns data-seeding entry scripts.

## Antipatterns

- Domain repos synthesizing generic Pattern Walker descriptors in script code.
- Hardcoded domain labels, ports, hosts, or storage roots in server handlers.
- Treating `config.yaml` or generated client files as the durable source of
  truth when HOCON owns the contract.
- Scanning full artifact trees from API calls.
- Merging server, client, and data-materialization responsibilities into one
  handler because it works for one sample.
- Adding small package-local Dockerfiles or deployment scripts to "just run" the
  server outside the local loop.
- Writing bespoke sample-data scripts that bypass the Wielder entrypoint,
  test-mode HOCON, or the domain ingestion/harmonization path.
- Treating a pytest fixture as the only owner of required source identities or
  generated stream locations.

## Validation Ladder

1. Resolve HOCON config and construct the Pydantic contract.
2. Run the Wielder entrypoint in test mode with `-w plan -t` to show source,
   ingest, harmonization, materialization, cleanup, and validation targets.
3. Run the smallest safe `-w apply -t` path that creates representative visible
   data.
4. Exercise the ASGI app with an in-process test client.
5. Probe live HTTP metadata, discovery, and representative stream endpoints.
6. Audit binary payloads with `pattern_walker_lib.auditor` or equivalent typed
   readers.
7. Verify notebooks can display the seeded raw, harmonized, and Pattern Walker
   stream evidence.
8. Verify a real client can discover terminology, layers, and streams without
   domain-specific edits.
