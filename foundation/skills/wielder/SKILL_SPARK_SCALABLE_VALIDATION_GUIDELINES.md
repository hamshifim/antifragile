---
name: Wielder Spark Scalable Validation Guidelines
description: Guidance for treating Spark validation as one scalable continuum from deterministic unit probes through integration, system, and load execution using the same pipeline core.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Wielder Spark Scalable Validation Guidelines

Spark validation should be treated as one scalable continuum rather than a set of disconnected testing species.

The old Nudnik lineage in `~/dev/peps/` shows the pattern clearly:
- small deterministic Spark probes read a tiny resource-backed fixture and assert behavior
- the same pipeline family can read a real source and write to a real sink
- a `pressure` block can then modulate iterations, pauses, channels, and synthetic duplication into a true load surface

## Core Principle

The same Spark pipeline core should be able to express:
- a unit test
- an integration test
- a system test
- a load test

The distinction should come from configuration scale, source choice, sink choice, and pressure settings rather than from proliferating separate logic trees.

The same workflow is epigenetically phenotyped by configuration into a unit-scale Spark probe, a broader integration or system path, and eventually a load surface.

## 1. Resource-Backed Deterministic Unit Probes

- **Guideline:** Strongly suggest keeping a tiny deterministic Spark path that reads small bundled fixtures and executes the real transformation or comparison logic.
- **Guideline:** Strongly suggest using test HOCON resources to describe input pairs, expected values, cutoffs, or other precise assertions.
- **Guideline:** The purpose of the unit-scale Spark probe is not to fake Spark. It is to keep Spark real while shrinking the dataset and the orchestration surface.

## 2. Same Core, Larger Surface

- **Guideline:** Strongly suggest reusing the same `pipe(...)` or equivalent pipeline core as scale increases.
- **Guideline:** Moving from unit to integration or load should primarily mean changing:
  - source keys
  - sink keys
  - test fixture size
  - pressure settings
- **Guideline:** Strongly suggest avoiding a separate "test-only Spark logic" branch when the real pipeline can already be driven with a smaller configuration.

## 3. Pressure as a First-Class Config Surface

The Nudnik pattern uses a `pressure` block rather than a second orchestration language.

- **Guideline:** Strongly suggest expressing Spark load modulation through configuration blocks such as:
  - `iterations`
  - `batch_interval`
  - `read_interval`
  - `channels`
- **Guideline:** Strongly suggest treating pressure as an axis of scale, not as a justification for creating an entirely different load-test harness.
- **Guideline:** When scale matters, the question should be "how does the same pipeline behave under a different pressure profile?" rather than "which separate load script should we trust?"

## 4. Synthetic Duplication over Synthetic Architecture

The stronger pattern is to reuse real schema and real pipeline logic while modulating the workload volume.

- **Guideline:** Strongly suggest generating load by duplicating or perturbing real records within the same schema rather than inventing a fake parallel architecture.
- **Guideline:** If synthetic data is used, strongly suggest preserving structural parity with the real source and keeping the sink contract unchanged.
- **Guideline:** The goal is to stress the real Spark path with altered scale, not to switch to a toy path that only resembles the real pipeline.

## 5. Source and Sink Reality

- **Guideline:** Strongly suggest letting source and sink configuration determine how "live" the test is.
- **Guideline:** Resource fixtures are appropriate for tiny deterministic probes.
- **Guideline:** Real parquet, Cassandra, Kafka, or object-store targets are appropriate when proving integration or system behavior.
- **Guideline:** Load testing should still prefer the real sink contract when the purpose is operational truth rather than abstract throughput theater.

## 6. Spark as a Testing Framework

Spark should be viewed as part of the testing framework, not only as the application runtime.

- **Guideline:** Strongly suggest using the same Spark job family to perform both transformation work and validation work.
- **Guideline:** A Spark validation path may inspect schemas, counts, parity, output structure, or sink materialization while still remaining inside the same orchestrated family.
- **Guideline:** Strongly suggest treating Spark unit-to-load validation as a configurable continuum rather than a split between "real jobs" and "tests."

## 7. Philosophy

- **Guideline:** Strongly suggest viewing unit, integration, system, and load execution as down-scaled or up-scaled modulations of one Spark validation family.
- **Guideline:** This reduces the delta between local Spark development and operational Spark reality.
- **Guideline:** It also reduces the probability of "it worked on my computer" bugs by forcing the same code path, schema shape, and sink contracts to survive across different scales.
