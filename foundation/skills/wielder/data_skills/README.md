# Wielder Data Skills

This directory groups data-shape doctrine: raw ingestion, harmonization, and
table schema contracts. Keep operational runtime/infrastructure guidance in
`../ops_skills/` and notebook mechanics in `../utility_skills/`.

## Routing

- [Data Ingestion Guidelines](SKILL_DATA_INGESTION_GUIDELINES.md): raw data
  tiering, provenance discipline, protocol identity, experiment metadata, and
  material inventory boundaries.
- [Harmonization Guidelines](SKILL_HARMONIZATION_GUIDELINES.md): raw-to-
  harmonized data shape, key lineage, hydration contracts, plan/apply key
  visibility, and notebook inspection.
- [PySpark Guidelines](SKILL_PYSPARK_GUIDELINES.md): PySpark/PySparker artifact
  jobs, Spark table IO, and Spark-backed ingestion, harmonization,
  materialization, or backfill boundaries.
- [Table Schema Guidelines](SKILL_TABLE_SCHEMA_GUIDELINES.md): reusable table
  schema ownership, column descriptions, preview legends, and column order.
