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

## Validation Ladder

1. Resolve HOCON config and construct the Pydantic contract.
2. Exercise the ASGI app with an in-process test client.
3. Probe live HTTP metadata, discovery, and representative stream endpoints.
4. Audit binary payloads with `pattern_walker_lib.auditor` or equivalent typed
   readers.
5. Verify a real client can discover terminology, layers, and streams without
   domain-specific edits.
