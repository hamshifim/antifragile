---
name: Harmonization Guidelines
description: Wielder doctrine for raw-to-harmonized data shape, key lineage, hydration contracts, and notebook visibility.
---


# Harmonization Guidelines

Use this skill when designing, implementing, reviewing, or testing raw artifact
discovery, native result indexing, comparable harmonized records, table schemas,
Spark writes, plan/apply key lineage, or harmonization notebooks.
Also read [Strict FS Agnosticism](SKILL_STRICT_FS_AGNOSTICISM.md) when harmonization names source buckets, native output base keys, artifact subkeys, table keys, materialization keys, URIs, or storage accessors.

## Goal

Map raw/native artifacts into indexed, comparable, replayable records without
erasing native meaning.

## Layer Separation

Keep these layers distinct:

- raw artifact discovery
- experiment/run catalog
- logical output catalog
- native/source artifact inventory
- derived materialization inventory
- entity/component identity tables
- native result rows
- hydration/replay contract
- harmonized comparable views
- serving/detail materializations

Native rows answer "what did the tool report?" Harmonized rows answer "what can
be compared across tools, under which mapping and caveats?"

## Native Output Truth Boundary

Do not synthesize native model/tool success. An input package, resolved config
sidecar, command preview, fixture parser payload, or notebook inspection bundle
is not a native output and must not be cataloged as one.

Never let a test harness, bypass branch, mock binary, or fixture helper write
native success markers, native artifact manifests, native result files,
prepared feature artifacts, score tables, prediction rows, or report outputs
under the real app output contract. If the upstream executable/service/model did not run and
produce the artifact, the harmonization layer should see no ready native output.

Parser-only or schema-only fixtures are allowed only when they live outside the
native run success contract and are named as fixtures. They may test parsing
logic, but they do not prove ingestion, harmonization, prediction, scoring, or
domain result production.

## Experiment Output Catalog Rule

For computational experiment outputs, prefer this operational shape:

```text
experiment_runs
  -> experiment_outputs
       -> output_artifacts
       -> output_materializations
       -> output-kind-specific domain tables
```

Use `experiment_runs` for what was attempted or executed. Use
`experiment_outputs` for logical outputs produced by a run, such as a complex
result set, trajectory set, event profile, or score table. Use
`output_artifacts` only for native/source files produced by the upstream tool.
Use `output_materializations` only for Culture-derived physical products such
as Parquet tables, serving bundles, notebook bundles, or inspection-viewer
payloads.

Do not let a domain object become the root operational catalog. For example,
`DomainResultSet` should own domain facts and source-reported
measurements, not run status, artifact storage layout, or lake materialization
bookkeeping.

Prefer durable table names that describe nouns in the catalog or domain model,
not implementation mechanics. Avoid schema names such as `*_df`, `*_index`, or
`*_projection` unless the table's actual domain concept is an index or
projection. Local notebook variables may still use `_df`.

For source-reported tool values, use names that preserve source semantics.
Prefer `source_reported_metric_types` and `source_reported_metrics` over generic
`quality_metrics` when the values are native confidence or score outputs, not
universal scientific quality claims.

## Base-Key Hydration Rule

Hot discovery rows should carry the smallest stable replay pointer that can
hydrate the rest of the source detail.

Prefer:

```text
native_output_base_key
hydrator_kind
hydrator_version
```

Avoid duplicating every derived artifact key, sidecar key, URI, or large JSON
manifest into the hot row when those values can be reconstructed from the base
key and the versioned hydrator contract.

The base key is a storage-key prefix or blob namespace for the native output. It
is not necessarily a local filesystem directory. A concrete hydrator/accessor
owns how subkeys are appended, such as:

```text
<native_output_base_key>/native_result.json
<native_output_base_key>/prediction/<artifact>.<native_extension>
<native_output_base_key>/prediction/<artifact>_metadata.json
```

Keep detailed artifact roles in one of these places:

- `output_artifacts`, using role, content type, and `artifact_subkey`
- the native result sidecar read by the hydrator/accessor
- a versioned artifact manifest object referenced by key, when the manifest is
  too useful to derive

Do not put bulky or derivable artifact maps into human-facing or paginated
discovery tables merely for convenience. This keeps viewers, notebooks,
and lake scans light while preserving replay through the hydrator.

## Ecosystem Boundaries

Use configured accessors, Bucketeers, Spark wrappers, table schemas, table URIs,
write modes, deduplication keys, and app/runtime configuration. Do not bypass
storage abstractions with local filesystem assumptions.

## Streaming-First Reactive Harmonization

For reactive systems, harmonization should normally be a durable streaming
listener started by the Wielder `apply` DAG before services or publishers emit
work traffic. Backfill is still required, but its role is deterministic
reconciliation: replay missed events, compare stream results with source
artifacts, repair tables, and plan cleanup from watermarks or UUIDs.

A streaming harmonizer must fail loudly if no streaming source is configured.
In a Kafka shape, validate the resolved bootstrap endpoint, source topic,
checkpoint key, error/escalation topic, and topic preflight before creating the
Spark reader. A query that starts without a real source is not a listener.

Small-message test runs may need warmup/canary traffic so micro-batches flush
and error handling is observable. Prefer a deliberately malformed canary that
the stream routes to the configured error/escalation channel, then wait for the
matching canary key before publishing real work. Do not use topic emptying or
delete messages as a readiness mechanism.

## Bucket/Key Path Rule

Human-facing rows, notebooks, ledgers, and plans should prefer `bucket` plus
stable relative keys over expanded local filesystem paths. A configured
accessor owns expansion to a physical URI, local path, cloud URI, or signed
read surface.

Use these forms in hot rows and notebook displays:

```text
bucket
native_output_base_key
artifact_subkey
table_key
hydrator_kind
hydrator_version
```

Avoid copying `${buckets_root}` or absolute local paths into notebooks, table
contracts, or durable rows merely to make local inspection convenient. If size,
existence, or preview information is useful, compute it through a helper that
accepts the configured accessor and still displays the relative key as the
semantic reference.

## Scalable Lookup Rule

Once raw inventory, harmonized outputs, or materialized products are tabled,
perform lookups with Spark predicates and projections. Driver-side loops over
object names are acceptable only for small raw discovery surfaces that have not
yet been ingested; if the surface can grow, first materialize raw inventory
rows, then resolve subsets, identities, joins, and search hits through Spark.

Notebook companions should show at least one bounded Spark-backed lookup when
the data product is intended to scale. The pandas display is a preview of the
Spark result, not the lookup engine.

## Cleanup And Reconciliation

Cleanup for harmonized or materialized data is a data operation, not an event
cleanup side effect. Expose `plan-delete` and `delete` surfaces that discover
owned UUIDs, watermarks, table partitions, and key prefixes through the same
Bucketeer/Spark/table accessors used for ingestion and backfill. `plan-delete`
prints the exact resources; `delete` removes only those resources.

## Serving Materialization Rule

A materialization is a physically written, reproducible derivative of already
ingested or harmonized data. The term is intentional and follows the database
and warehouse meaning of a materialized view: the semantic source remains the
harmonized table or native artifact, while the materialized product is optimized
for a target consumer, lookup pattern, or service-level objective.

Use materialization for products such as viewer bundles, Arrow stream
pages, notebook-ready payloads, or other serving/detail layouts. Do not call
these products harmonization unless they change the canonical comparable data
model. A viewer serving materialization, for example, may project
harmonized domain tables into manifests, lookup pages, visual buffers,
detail buffers, and layer streams without rerunning the source model or
rewriting the harmonized lake tables.

Every serving materialization should expose the normal Wielder lifecycle:

- `plan` shows source tables, output bucket/base key, replacement strategy, and
  planned child keys.
- `apply` writes or rewrites the materialized product according to configured
  write mode.
- `plan-delete` shows the exact materialized product that would be removed.
- `delete` removes only the materialized product, never native artifacts or
  harmonized source tables.

The action surface should be named for the consumer and product, such as
`pattern_walker_materialization`, while the output catalog should record
`materialization_kind` values such as `serving_bundle`, `arrow_stream_page`, or
`notebook_view`.

## Plan/Apply Key Schema

Any harmonization `plan` or `apply` must show:

- configured discovery prefixes
- the base key used for replay
- the hydrator kind and version that own subkey derivation
- the logical output kind and output schema/version
- sidecar pointer keys read from native result payloads when they are material
- raw experiment/output boundary inventory prefixes
- harmonized output base key, table or artifact destination keys, write mode,
  and deduplication keys
- whether the command is a non-mutating plan or an applying write

Column schemas are useful detail, but key lineage is the operator contract.

## Notebooks

Harmonization notebooks should show raw experiment/output inventory before
harmonized tables, use configured accessors for storage, and fail naturally when
required upstream data or tables are missing.

Notebook tables should expose semantic keys, not local filesystem expansion, if
a configured accessor can resolve the expanded path on demand.

## Acceptance Shape

Harmonization is acceptable only when:

- discovery, reads, writes, and cleanup use configured ecosystem storage
- plan/apply output shows where inputs are derived and where outputs will be
  deposited
- native outputs remain inspectable after harmonization
- harmonized records do not hide native meaning
- Spark table writing, when present, follows
  [PySpark Guidelines](SKILL_PYSPARK_GUIDELINES.md)
- table schemas, URIs, write modes, and deduplication keys resolve from config
- hot discovery rows avoid bulky derivable manifests and use base-key hydration
  contracts instead
- notebooks expose raw outputs before harmonized views and fail honestly when
  required data is absent
