---
name: Harmonization Guidelines
description: Wielder doctrine for raw-to-harmonized data shape, key lineage, hydration contracts, and notebook visibility.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Harmonization Guidelines

Use this skill when designing, implementing, reviewing, or testing raw artifact
discovery, native result indexing, comparable harmonized records, table schemas,
Spark writes, plan/apply key lineage, or harmonization notebooks.

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
structure set, trajectory set, binding-energy profile, or score table. Use
`output_artifacts` only for native/source files produced by the upstream tool.
Use `output_materializations` only for Culture-derived physical products such
as Parquet tables, serving bundles, notebook bundles, or Pattern Viewer
payloads.

Do not let a domain object become the root operational catalog. For example,
`ComplexStructureSet` should own molecular structure facts and source-reported
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
<native_output_base_key>/molecular_topology_result.json
<native_output_base_key>/prediction/<artifact>.cif
<native_output_base_key>/prediction/<artifact>_mmcif.cif
```

Keep detailed artifact roles in one of these places:

- `output_artifacts`, using role, content type, and `artifact_subkey`
- the native result sidecar read by the hydrator/accessor
- a versioned artifact manifest object referenced by key, when the manifest is
  too useful to derive

Do not put bulky or derivable artifact maps into human-facing or paginated
discovery tables merely for convenience. This keeps Pattern Viewer, notebooks,
and lake scans light while preserving replay through the hydrator.

## Ecosystem Boundaries

Use configured accessors, Bucketeers, Spark wrappers, table schemas, table URIs,
write modes, deduplication keys, and app/runtime configuration. Do not bypass
storage abstractions with local filesystem assumptions.

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
- Spark table writing, when present, runs through an app-owned Spark wrapper
- table schemas, URIs, write modes, and deduplication keys resolve from config
- hot discovery rows avoid bulky derivable manifests and use base-key hydration
  contracts instead
- notebooks expose raw outputs before harmonized views and fail honestly when
  required data is absent
