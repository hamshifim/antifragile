# Wielder Test Skills

This directory groups Wielder and Antifragile testing and validation doctrine.

Keep executable pytest suites in `antifragile/tests/`. Keep operator-facing
testing doctrine here.

## Routing

- [Live Quality Assurance Testing](SKILL_TEST_GUIDELINES.md): general testing
  constraints, fixture shape, evidence reports, pytest handoff norms, and the
  routing hub for specialized validation skills.
- [Workflow Validation Doctrine](SKILL_WORKFLOW_VALIDATION_GUIDELINES.md):
  Wielder workflows as configurable integration, system, load, and production
  validation harnesses.
- [Reactive Distributed Integration Testing](SKILL_REACTIVE_DISTRIBUTED_INTEGRATION_TESTS.md):
  storage-event, topic, queue, job, callback, fanout, and downstream-ingestion
  flow tests with observable nodes and human-readable progress reports.
- [Spark Scalable Validation Doctrine](SKILL_SPARK_SCALABLE_VALIDATION_GUIDELINES.md):
  Spark-specific unit-to-load validation using one pipeline core across source,
  sink, scale, and pressure configurations.
