---
description: Raw Data Ingestion Tiering and Provenance Discipline
---

 Data Ingestion Guidelines

Raw ingestion should preserve information while keeping reusable, transient, and measured facts separate.

## Three Raw Tiers

1. **Protocol**
   - Reusable method/assay definition.
   - Assign a stable `protocol_id`.
   - Compute a deterministic `protocol_hash` over normalized stable protocol content.
   - Reuse an existing protocol when the hash matches.
   - If the same nominal protocol family yields a new hash, create a new protocol row and warn the user about possible protocol drift.

2. **Experiment Metadata**
   - Transient run/workbook/sample context.
   - Store source file, study/run identifiers, study dates, sample grouping, compound/batch, matrix/species, and the linked `protocol_id`.
   - It may be a separate keyed table when normalization helps more than reviewability.
   - Prefer names like `experiment_context` when the table is a returned review/audit surface rather than a normalized join table.

3. **Material Inventory**
   - Concrete material instances used in an experiment context.
   - Link to context through a stable inventory-set id rather than embedding many materials into one context row.
   - Use explicit source-label aliases to map vendor/CRO field labels into canonical columns.
   - Preserve raw labels and source cells for every mapped inventory field.

4. **Empirical**
   - Row-level observed measurements.
   - It may be enriched with transient experiment metadata when each measurement row needs to be self-contained for review, export, or downstream handoff.
   - Keep reusable protocol text separate and reference it through a trailing `protocol_id`.

## Audit Leftovers

Keep an audit table for non-empty cells or records not confidently assigned to the three raw tiers. This is not a fourth data tier; it is ingestion accounting. Derived report outputs can live here during raw ingestion until a later derived-data pass explicitly owns them.
When recurring leftovers can be explained, add forensic attribution columns rather than silently dropping them or promoting weakly understood helper cells into scientific tables.

## Storage Keys

Raw inventory rows should preserve storage identity as bucket plus relative key
or base-key plus subkey. The physical URI is an accessor concern. Do not make
absolute local filesystem paths durable ingestion facts.

Prefer:

- `source_bucket`
- `native_output_base_key`
- `artifact_subkey`
- `source_manifest_key`
- `hydrator_kind`
- `hydrator_version`

For table-scale inventory, write raw inventory tables and use Spark for lookup,
subset matching, joins, and backfill planning. Provider-native object listing is
only the discovery step; it should not become the long-term query engine for a
growing dataset.

## Column Order

Column order should optimize human inspection before storage purity.

- Put the most scientifically or operationally discriminating dimension first.
- Put supporting descriptors next.
- Put technical/provenance fields last.
- IDs, hashes, source paths, scope labels, and bookkeeping columns should usually trail unless the table exists specifically to inspect provenance.

Example: an enriched empirical table should lead with dimensions such as `sample_name`, `compound_id`, `species`, `strain`, `matrix`, and `mw`, then observed measurement columns, then supporting run/study descriptors, and end with `source_file` and `protocol_id`.
