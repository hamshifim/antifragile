---
name: PySpark Guidelines
description: Wielder doctrine for PySpark and PySparker artifact jobs, Spark table IO, and Spark-backed ingestion, harmonization, materialization, or backfill work.
---

# PySpark Guidelines

Use this skill when designing, implementing, reviewing, or testing PySpark,
PySparker, Spark artifact jobs, table-scale reads/writes, or Spark-backed
ingestion, harmonization, materialization, and backfill workflows.

## Core Boundary

The domain app owns source-transform-sink semantics. Wielder owns generic Spark
mechanics.

- Domain code builds domain rows, source discovery, transforms, validation, and
  report meaning.
- Wielder provides reusable Spark contracts, artifact-job execution, table IO,
  schema conversion, row coercion, deduplication, and configured session setup.
- Ecosystem and context config choose physical roots, catalogs, filesystem
  providers, credentials, write modes, runtime placement, and local/cloud
  phenotype.

Do not copy Spark session builders, schema builders, row coercion, or
deduplication helpers into each domain app. Extend the Wielder Spark helper when
the need is generic.

## PySparker Contract

Spark artifact jobs should be expressed as versioned HOCON contracts on the
domain app, then consumed by a Wielder app or workflow.

```hocon
<app> {
  spark_artifact_jobs {
    harmonize_outputs {
      contract_version = "wielder.pyspark_artifact_job.v1"
      job_key = "harmonize_outputs"
      bootstrap_ref_path = ["<app>", "<pipeline>", "spark", "resolved_conf"]
      spark = ${<app>.<pipeline>.spark}
    }
  }
}
```

The Wielder consumer resolves the target app config through the normal config
mode stack, selects `target_app_conf.spark_artifact_jobs.<job_key>`, validates
it with the Wielder contract model, and passes the embedded `spark` block to the
PySparker runtime.

Do not pass gnostic config paths such as `spark_conf_path`. The resolved config
already contains the contract.

## Table IO

Use Wielder Spark table IO helpers for table writes unless a stronger local
abstraction already exists.

- Load configured schemas from HOCON.
- Build Spark sessions from resolved Spark config.
- Convert configured schemas to Spark schemas centrally.
- Coerce Python rows to Spark-compatible values centrally.
- Deduplicate against existing tables centrally when configured.
- Let domain row collections expose a simple `table_rows(table_name)` or
  equivalent domain-owned method.

Spark may read and write tables through native source/sink URIs. Bucketeer is
for object-key discovery, small artifacts, sidecars, manifests, ledgers, and
artifact publication. Do not force Parquet or table-scale Spark writes through
Bucketeer.

## Pipeline Shape

Keep ingestion, harmonization, and materialization separate even when one Spark
job can execute several of them.

- Ingestion preserves source/native facts and raw inventory.
- Harmonization maps native outputs into comparable, replayable records while
  preserving native meaning.
- Materialization writes reproducible derivatives for consumers, services,
  notebooks, reports, or visualizations.

Intermediate tables are first-class. Do not skip them merely because a local
prototype can jump directly to a final serving product.

## Anti-Patterns

- Recreating `_spark_type`, `_spark_schema`, Spark session setup, or
  deduplication code inside each app.
- Walking config with string paths, `.get()` fallbacks, or Python-computed
  runtime defaults.
- Letting code mutate ecosystem, mode, or context choices after resolution.
- Hiding table sink URIs, catalogs, write modes, or dedup keys in Python.
- Mixing raw discovery, harmonized records, and materialized serving products
  in one undifferentiated table.
- Treating local filesystem paths as the source of truth for a Spark job.

## Validation

Test generic Spark mechanics in Wielder. Test domain row construction and
source-transform-sink meaning in the domain app. Test Wielder app/workflow
resolution by proving it resolves the target app contract through the normal
mode stack and does not carry gnostic path keys.

Integration tests should exercise plan/apply/delete surfaces against temporary
or local Spark destinations and assert that intermediate tables exist, not only
that a final file was produced.
