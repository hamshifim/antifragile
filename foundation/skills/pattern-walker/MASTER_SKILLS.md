# Pattern Walker Antifragile Skills

This directory is a Pattern Walker overlay, not a fork of Antifragile. Load the
canonical Wielder/Antifragile skills first when the work touches config,
scripting, testing, notebooks, versioning, recovery, or deployment. These local
skills specialize that doctrine for the Pattern Walker reverse API, client, and
revival workflow.

## Inherited Doctrine

Read these upstream skills when they apply:

- `../wielder/SKILL_CONTEXT_INITIATION_ALIGNMENT.md`
- `../wielder/SKILL_EPIGENETIC_CONFIG_CONTRACTS.md`
- `../wielder/SKILL_CONFIGURATION_GUIDELINES.md`
- `../wielder/SKILL_WIELDER_SCRIPTS.md`
- `../wielder/SKILL_TEST_GUIDELINES.md`
- `../wielder/SKILL_NOTEBOOK_GUIDELINES.md`
- `../wielder/SKILL_WORKFLOW_VALIDATION_GUIDELINES.md`
- `../wielder/SKILL_GIT_VERSIONING.md`

Pattern Walker-specific guidance should compose with those skills. If a local
skill and the upstream doctrine appear to conflict, prefer the upstream doctrine
and update this overlay to express only the specialization.

Deployment, Docker images, hosted runtime wiring, and ecosystem-specific launch
surfaces do not belong in the Pattern Walker server or client packages. They
belong in the appropriate wielding module, such as `culture-wielding`, where
operational ownership, image provenance, and environment contracts can be
managed as a first-class Wielder surface.

Pattern Walker revival must also create something real to see. Use Wielder
`-t/--test` mode as the scenario overlay for fetching, ingesting, harmonizing,
and materializing a small representative dataset. The test overlay should drive
the same entry scripts, API integration tests, and notebook companions used by
ordinary local operation. It should not become a second hand-built fixture path.

## General Shape

Pattern Walker is a domain-neutral traversal runtime for large hierarchical
datasets. Domain repos own their data lake, indexing, and materialization paths.
`pattern-walker-lib` owns generic protocol contracts, typed validation, and
shared client/server configuration semantics.

The server side acts as a reverse API: it adapts arbitrary domain storage into
Pattern Walker-compatible metadata, discovery records, and binary streams. The
client side stays dense and generic: it fetches metadata, renders columnar
topology/trajectory/visual/layer streams, and lets server-provided metadata name
domain terms and controls.

The core conceptual split is:

- Domain truth: source files, catalogs, Parquet stores, or generated artifacts
  owned by a domain repo.
- Discovery ledger: small, indexed metadata that answers item/system questions
  without scanning the world.
- Pattern Walker schema: validated metadata and binary payloads suitable for
  traversal, rendering, and auditing.
- Topology: mostly static relationships, hierarchy, identifiers, and semantic
  structure.
- Trajectory: time-varying coordinates or frames.
- Visuals: rendering channels such as color, scale, shape, labels, and styles.
- Layers: semantic/topological subsets and optional pointer streams.
- Functions: optional advertised behavior payloads, never arbitrary path lookup.

## Visible Test Data

For Pattern Walker work, "the server starts" is not enough. A local revival or
test scenario should be able to seed enough domain data for a human to inspect
the client and notebooks.

The expected local chain is:

- Fetch: acquire or synthesize a small named domain fixture through configured
  source accessors.
- Ingest: write raw/domain truth artifacts through the domain app's normal
  entry scripts.
- Harmonize: produce comparable indexed records without erasing native meaning.
- Materialize: generate Pattern Walker topology, trajectory, visuals, layers,
  metadata ledgers, and optional function payloads.
- Serve: expose the reverse API locally.
- View: prove the same data through API tests, notebooks, and the browser
  client.

The scenario identity, scale, source selection, expected rows, cleanup policy,
and validation toggles belong in Wielder test-mode HOCON such as
`conf/test/<domain>/<ecosystem>/test.conf` or app-local `test.conf` overlays.
Use `-t` with normal Wielder actions such as `-w plan`, `-w apply`, and
`-w delete`; do not invent a separate "sample-data" action when the normal
entrypoint can be phenotyped by test config.

## Local Skill Index

- [Pattern Walker Server](SKILL_PATTERN_WALKER_SERVER.md): build and review
  reverse API servers and domain adapters.
- [Pattern Walker Client](SKILL_PATTERN_WALKER_CLIENT.md): build and review
  metadata-driven browser clients and local config overlays.
- [Pattern Walker Revival](SKILL_PATTERN_WALKER_REVIVAL.md): revive the stack
  from partial state with local-first validation and precise extraction.

## Source Anchors

Use the code as the live contract before inventing new abstractions:

- `/home/gideon/dev/culture/pattern-walker-lib/src/pattern_walker_lib/protocol/schemas.py`
- `/home/gideon/dev/culture/pattern-walker-lib/src/pattern_walker_lib/protocol/server.py`
- `/home/gideon/dev/culture/pattern-walker-lib/src/pattern_walker_lib/schema.py`
- `/home/gideon/dev/culture/pattern-walker-lib/src/pattern_walker_lib/auditor.py`

Useful neighboring project documents live under:

- `/home/gideon/dev/culture/pattern-walker/FOUNDATIONS.md`
- `/home/gideon/dev/culture/pattern-walker/pattern_walker_technical_stack.md`
- `/home/gideon/dev/culture/pattern-walker/webgpu_data_architecture.md`
- `/home/gideon/dev/culture/Tasks/pattern_walker_reverse_api_revival_stam.md`
