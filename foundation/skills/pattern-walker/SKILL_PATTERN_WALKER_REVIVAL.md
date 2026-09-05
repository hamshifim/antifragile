---
description: Revive a partial Pattern Walker stack by extracting the current protocol shape, restoring local server/client loops, and only then generalizing shared contracts into pattern-walker-lib.
---

# Pattern Walker Revival

Use this skill when Pattern Walker exists in fragments: old docs, partial
servers, sample clients, stale configs, missing generated data, or branch
history that needs careful recovery.

## Inherit First

Start with the upstream context initiation and recovery skills. Add the
configuration, epigenetic config, scripting, testing, notebook, and versioning
skills as soon as they touch the work. This skill is the Pattern Walker revival
overlay on that foundation.

## Revival Shape

Pattern Walker revival is local-first and evidence-led:

1. Read the task document, existing protocol code, and neighboring domain
   servers before inventing new contracts.
2. Audit repo, branch, and submodule state so the current surface is explicit.
3. Repair config resolution and local deposits before changing app logic.
4. Add or repair a Wielder `-t/--test` scenario that creates enough visible
   data through the real fetch, ingest, harmonization, and materialization
   entry scripts.
5. Prove in-process API behavior, then live HTTP behavior, then notebook
   behavior, then browser behavior.
6. Distinguish empty data from broken server contracts.
7. Extract shared HOCON/Pydantic protocol functionality into
   `pattern-walker-lib` only after at least two domain surfaces show the same
   shape.
8. Move Docker, deployment, hosted runtime, and image concerns into the
   ecosystem wielding module, such as `culture-wielding`, only after the local
   loop is healthy.
9. Record versioning and handoff notes once the stack is demonstrably healthier.

## Context And Data Preflight

Run this preflight before treating a disconnected or empty client as a server
failure. A process can be healthy while resolving a context whose serving
materialization is empty, and a populated server can be invisible when the
client deposit points at a different access port.

1. **Name the intended phenotype.** Record the wrapper ecosystem, context pack,
   test overlay, stage tier, domain app, expected entity set, and access port.
   Do not rely on a shell's previous defaults.
2. **Prove that the context exists.** Locate the named context pack and the
   relevant app/ecosystem overlays, then run the nearest canonical entrypoint
   with the intended `-es`, `-cc`, `-st`, and `-t` selectors in `-w plan` mode.
   The plan should expose the resolved source identity, artifact or serving
   root, bind/access port, and client-config deposit.
3. **Check data at the resolved root.** Inspect the configured source,
   harmonized, and Pattern Walker materialization roots. Check for the expected
   manifests, metadata ledger, entity inventory, and representative stream
   files. Never infer deletion from an empty UI before checking the resolved
   storage contract.
4. **Seed only the missing layer.** If source data exists but the serving
   bundle does not, rematerialize Pattern Walker data. If source data is absent,
   run the configured fetch or synthesis, ingestion, harmonization, and
   materialization chain. Prefer the domain's `-t` scenario when it owns the
   smallest honest visible fixture.
5. **Start the server with the same selectors.** Do not start a domain server
   under a neutral/default context after validating a named context. Keep the
   server's resolved access port aligned with the client deposit.
6. **Probe before opening the browser.** Require non-empty discovery plus at
   least one representative binary payload:

   ```bash
   curl -fsS http://localhost:<port>/metadata
   curl -fsS http://localhost:<port>/domain/items
   curl -fsS http://localhost:<port>/domain/systems
   curl -fsS -o /dev/null http://localhost:<port>/trajectory/<entity_id>?granularity=0\&frame=0
   curl -fsS -o /dev/null http://localhost:<port>/visuals/<entity_id>?granularity=0
   ```

   A domain may legitimately populate only items or only systems, but the
   expected discovery collection must be non-empty.
7. **Verify the client deposit.** Inspect the generated/local client config and
   confirm every server id, host, and access port matches the live endpoints.
   Then load each domain in the browser and confirm that its metadata,
   discovery, and representative visuals are parsed without errors.

For a multi-domain stack, repeat steps 1-7 independently for every server. The
aggregate runtime stack proves only that its configured processes started; it
does not prove that every desired domain was included, that each domain used a
populated context, or that the client points at the resulting ports.

### Fast Failure Classification

| Observation | Most likely boundary | Next check |
| --- | --- | --- |
| Connection refused | Process or port | Runtime plan, PID/log, bind and access ports |
| `/metadata` works; discovery is empty | Context or serving materialization | Resolved context, source identity, ledger and stream roots |
| Discovery is populated; a stream fails | Materialization or protocol payload | Representative file, manifest, typed stream audit |
| HTTP probes pass; client says disconnected | Client deposit or browser state | Server id/host/port, metadata compatibility, browser logs |
| One domain works and another is empty | Per-domain context mismatch | Plan and storage checks for the empty domain only |

Stop diagnosis at the first failed boundary. Do not rerun ingestion, delete
artifacts, or modify server code until the preflight localizes the failure.

## Visible Data Workflow

A revival plan must make it clear how a clean local workspace gets something to
see. The preferred route is a configured Wielder test-mode scenario:

1. `-w plan -t` reports the source fixture, expected input identity, raw output
   location, harmonized output location, Pattern Walker materialized stream
   roots, cleanup behavior, and validation targets.
2. `-w apply -t` fetches or synthesizes the small source fixture, runs normal
   ingestion, runs harmonization, and materializes topology, trajectory, visuals,
   layers, metadata ledgers, and optional function payloads.
3. API integration tests validate `/metadata`, discovery, streams, and
   `/functions/{behavior_id}` where applicable.
4. Notebook companions under `explore/` inspect raw inventory, harmonized
   records, and Pattern Walker streams using the notebook conversion workflow.
5. The browser client renders the same seeded data through its normal config
   bridge and live server endpoints.

The test overlay should preserve native meaning and key lineage during
harmonization. It should not fake comparable records purely to satisfy the UI.

## What To Extract

Extract the general Pattern Walker shape, not a single domain's storage story:

- Metadata and discovery schemas.
- Server/client config contracts.
- Endpoint capability descriptors.
- Binary stream naming, validation, and audit helpers.
- Typed representation of topology, trajectory, visuals, layers, and optional
  functions.

Leave domain-specific materialization, indexes, source data ownership, and
ecosystem packaging in the domain repo until the repetition is real.

## Recovery Sources

Useful sources include:

- `/home/gideon/dev/culture/Tasks/pattern_walker_reverse_api_revival_stam.md`
- `/home/gideon/dev/culture/pattern-walker/FOUNDATIONS.md`
- `/home/gideon/dev/culture/pattern-walker/pattern_walker_technical_stack.md`
- `/home/gideon/dev/culture/pattern-walker/webgpu_data_architecture.md`
- `src/pattern_walker_lib/protocol/schemas.py`
- `src/pattern_walker_lib/protocol/server.py`
- Existing domain servers such as `domain-inventory` and `domain-analytics`.

## Antipatterns

- Starting with Docker or image work before a local server/client loop passes.
- Leaving small Dockerfiles, deployment manifests, or hosted runtime scripts in
  the server/client packages instead of moving them to `culture-wielding` or the
  current ecosystem wielding module.
- Declaring revival complete while the client has nothing to render except
  static mocked data.
- Creating special one-off sample-data scripts instead of Wielder test-mode
  entry scripts that exercise fetch, ingestion, harmonization, and
  materialization.
- Hiding required source ids, run ids, output paths, or cleanup policy inside
  pytest fixtures instead of HOCON test overlays.
- Broad branch archaeology without a concrete missing contract to recover.
- Editing notebook JSON directly instead of using the notebook skill workflow.
- Promoting a domain-specific descriptor builder into shared doctrine.
- Treating generated client config files as durable source instead of HOCON
  deposits.
- Calling a browser failure a data failure before probing live metadata and
  stream endpoints.

## Handoff Shape

When pausing or finishing revival work, report:

- Which server endpoint families are live and which are still stubbed.
- Which client config deposits exist and which HOCON owns them.
- Which tests or probes passed, including in-process and live HTTP coverage.
- Which `-t` Wielder scenario seeded the visible data, including fetch,
  ingestion, harmonization, and materialization evidence.
- Which notebooks inspect the same data and whether they were updated through
  the notebook conversion workflow.
- Whether missing visuals are caused by empty data, stream failure, metadata
  mismatch, or client rendering.
- The next small extraction that belongs in `pattern-walker-lib`, if any.
