---
description: Architectural form doctrine for Wielder apps as domain functionality expressed into ecosystem phenotypes through Wielder modes, including service, Spark, ingestion, harmonization, materialization, workflow, minimal app config, core ecosystem contracts, aggregated workflows, and thin surface wrappers.
---

# Wielder App Form

A Wielder app is a domain or subdomain functionality made ecosystem-capable through Wielder modes.

The app owns the functionality. The Wielder owns everything needed for that functionality to function inside an ecosystem: configuration resolution, runtime expression, deployment shape, workflow composition, artifact handling, event behavior, validation, observation, provenance, cleanup, and handoff.

Runtime surfaces such as Kubernetes, Docker, notebooks, CLIs, and service wrappers are phenotypes. The app is the durable functionality that can be expressed into those phenotypes through the Wielder mode layer and its guidelines.

## Core Form

```text
domain functionality
  + minimal app config
  + mode-guided phenotype expression
  + ecosystem contracts
  + workflow composition
  + thin operator surfaces
  + evidence/provenance
= Wielder app phenotype
```

## App Layer

The app layer should stay close to the domain functionality.

It may own:

- domain inputs and outputs
- typed request/result models
- algorithm, model, or tool parameters
- domain thresholds and validation expectations
- artifact schema and semantic output names
- local runner/service code that performs the functionality
- source, transform, and sink contracts for data/pipeline apps

The ecosystem, deployment, workflow, and context layers own broad operational reality: buckets, mounts, provider routing, queues, registries, GPU node groups, Kube contexts, public routes, workflow fanout, and cross-app topology.

## Minimal App Config

An app baseline should express only the durable contract intrinsic to the functionality and the fail-closed defaults required for safe resolution.

Prefer:

```text
conf/apps/<app>/app.conf
  app identity
  domain parameters
  input/output contracts
  artifact expectations
  provider config keys consumed by the app
  disabled/empty defaults for optional ecosystem behavior
```

Keep out of the neutral app baseline:

```text
conf/apps/<app>/app.conf
  copied bucket maps
  concrete cloud/provider roots
  stage-specific facts
  developer-local toggles
  Kube-only resource topology
  workflow-wide DAG payloads
  fixture pressure from tests
```

If a concrete run needs smaller batches, miniature models, short polling windows, fake payloads, or reduced resources, put that pressure in the test overlay, context pack, or explicit phenotype overlay. The neutral app baseline should remain the durable app contract.

## Phenotypes

Modes create app phenotypes. The mode details live in the Wielder mode/config/deployment skills; this skill only fixes the architectural relationship.

A single app can be expressed as:

```text
<app>.local_tool
<app>.batch_job
<app>.reactive_worker
<app>.kube_service
<app>.spark_job
<app>.ingestion_pipeline
<app>.harmonization_pipeline
<app>.materialization_pipeline
<app>.aggregate_reactive_mixer
<app>.workflow_step
<app>.notebook_companion
<app>.visualization_surface
<app>.report_producer
```

The phenotype is the running shape. The app is the capability.

When designing a phenotype, name the app first, then the ecosystem expression:

```text
App: protenix_prediction
Functionality: structure or complex prediction
Phenotype: GPU-backed reactive Kube worker
Ecosystem: provider/runtime/storage/event topology that makes it runnable
Surface: CLI/API/notebook/dashboard wrapper over the same core contract
```

## Aggregating App Form

An app may aggregate multiple entrypoints when the domain functionality is naturally a mix-and-match capability rather than one fixed route.

This form is useful when an operator, workflow, event, or downstream service needs to choose a transient subset of actions such as:

```text
prepare input
  -> optional search
  -> optional prediction
  -> optional harmonization
  -> optional materialization
  -> optional visualization/report
```

The aggregate app should keep each entrypoint thin and typed. The app-level contract names the available capabilities; the active phenotype chooses which steps to run through resolved configuration.

Use steps config for transient control:

```text
app capabilities: stable available entrypoints
steps config: selected run sequence for this phenotype, test, context, or workflow
workflow: orchestrates selected steps and evidence
```

The steps config may live as an app-owned reusable step set, a test overlay selection, an ephemeral workflow intent, or an ecosystem/workflow concern depending on durability. The important boundary is that transient step choice belongs in configuration, while the entrypoint implementations remain stable typed capabilities.

This gives reactive systems an ad hoc composition surface without turning the app into a pile of one-off scripts. A reactive event can select "search only", "search plus prediction", "prediction plus materialization", or "full workflow" by resolving a configured step set and then emitting evidence for the actual steps executed.

## Data Pipeline Form

Some apps materialize as data jobs or pipelines rather than request/response services.

Their architectural form is:

```text
source contract
  -> transform contract
  -> sink or materialization contract
```

This applies to ingestion, harmonization, derived table building, Spark jobs, serving materializations, report builds, index builds, and lake-to-service projections.

For data apps, the app layer owns the semantic transformation:

- source kind and source contract
- transform identity and transform version
- domain parsing, normalization, harmonization, projection, or materialization logic
- output schema, logical sink names, and comparable table contracts
- deduplication keys, replay keys, and validation expectations
- plan/apply evidence shape for key lineage

The ecosystem layer owns the physical execution and storage expression:

- object store, bucket roots, and table/catalog locations
- Spark, local dataframe, batch, Kube, or managed-cluster execution surface
- executor resources, images, credentials, mounts, and provider routing
- workflow placement, event triggers, schedules, and downstream consumers

Spark is a phenotype for a source-transform-sink app. The same app may express as a local dataframe proof, a Spark job, a scheduled batch pipeline, a reactive consumer, a Kube `SparkApplication`, or a larger aggregated ecosystem workflow step.

## Data Pipeline Instantiation

A data/pipeline app has a different source-transform-sink implementation shape from a request/response service.

Recommended shape:

```text
conf/apps/<app>/app.conf
conf/apps/<app>/test.conf
conf/apps/<app>/schemas.conf        # when schemas are app-owned

src/.../apps/<app>/
  models.py                         # typed source, transform, sink, and evidence contracts
  sources.py                        # configured source discovery and reads
  transforms.py                     # pure or mostly pure domain transformations
  sinks.py                          # configured writes, materializations, and cleanup
  pipeline.py                       # plan/apply/delete orchestration over source -> transform -> sink
  reports.py                        # lineage, validation, and operator evidence
  spark.py                          # optional Spark adapter/session boundary
```

Use this form for ingestion, harmonization, materialization, indexing, table builds, feature builds, and report-producing data flows.

The `pipeline.py` layer should orchestrate the configured lifecycle. The `transforms.py` layer should own domain semantics. The `sources.py` and `sinks.py` layers should route all physical discovery, reads, writes, and cleanup through configured accessors, Bucketeers, Spark wrappers, table catalogs, or equivalent ecosystem-owned boundaries.

## Ingestion, Harmonization, Materialization

Treat ingestion, harmonization, and materialization as app functionality when they own a stable domain transformation. Lightweight glue can remain utility code or workflow internals until its source-transform-sink contract becomes durable.

Use the terms distinctly:

- Ingestion preserves source/native facts and separates protocol, run context, material inventory, empirical rows, and audit leftovers.
- Harmonization maps raw/native artifacts into comparable, replayable records while preserving native meaning.
- Materialization writes reproducible derivatives optimized for a consumer, lookup pattern, service, notebook, report, or visualization.

These are often adjacent phenotypes in one ecosystem workflow, but they should remain separate app forms when their source-transform-sink contracts, validation expectations, or ownership boundaries differ.

## Ecosystem Shape

Separate ecosystem concerns by durability and ownership.

- Core ecosystems own shared contracts: buckets, topics, registries, table schemas, artifact roots, app relationships, workflow contracts, and default cross-app behavior.
- Aggregated ecosystem workflows own how several apps compose into a larger capability.
- Concrete ecosystem overlays own physical expression: surface, provider, Kube context, registry authority, credential boundary, mount topology, node groups, service routes, and readiness checks.
- Context packs own developer-local or operator-local modulation.
- Test overlays own fixture pressure and proof-specific constraints.

Concrete overlays should be thin. Prefer a core or family ecosystem include plus a small explicit diff over copying the whole workflow contract into every provider/runtime surface.

## Thin Surfaces

CLI, API, notebook, UI, and dashboard entrypoints should be thin surfaces over the same app contract.

They should:

- resolve configuration through the canonical accessor
- submit or invoke typed app requests
- expose operator controls without inventing a second config path
- read artifacts and evidence from configured accessors
- keep branching near the boundary that owns it

Keep domain logic in the app service/runner, filesystem geometry in configured accessors, foreign app relationships in explicit boundary config, and ecosystem shape in the resolved Wielder mode envelope.

## Reactiveness

Reactive behavior is a phenotype choice, not a separate app identity.

For a reactive phenotype, keep the app's domain request/result contract stable and let the ecosystem/event layer provide the transport:

```text
event or operator request
  -> resolved app config
  -> typed domain request
  -> runner/service execution
  -> artifacts and metrics
  -> validation
  -> result event or report
```

Use event consumer/subscribe language for Pub/Sub-like behavior. Provider polling, queue setup, subscription registration, retry mechanics, and transport-specific details belong behind the configured event consumer boundary.

For aggregate reactive apps, the event payload should identify scientific or operator intent, while the resolved steps config controls which stable app entrypoints run. Prefer a configured step selection over code-level branching when the same app must support ad hoc combinations of entrypoints.

## Kube Service Instantiation

A Kube service is one concrete phenotype of a Wielder app.

Recommended shape:

```text
conf/apps/<app>/app.conf
conf/apps/<app>/deploy.conf
conf/apps/<app>/test.conf

src/.../apps/<app>/
  models.py
  service.py
  runner.py
  events.py
  steps.py                          # optional aggregate step registry/dispatcher
  reports.py
  deploy/
    image.py
    kube.py
    resources.py
```

The Kube phenotype may use:

- `ServiceAccount`
- `ConfigMap`
- secret references
- `Deployment`, `StatefulSet`, or `Job`
- `Service` or port-forward route
- PVCs, mounted buckets, or model/artifact volumes
- node selectors, GPU class, tolerations, and scaling policy

The deploy/resource layer expresses the app into Kube using resolved configuration and Wielder deployment guidelines.

## Examples

MMseqs:

```text
App: mmseqs_sequence_alignment
Functionality: sequence search, alignment, clustering, or MSA preparation
Phenotypes: local SDK runner, batch job, reactive MSA worker, Kube service
Core app config: databases consumed, input sequence contract, output MSA/hit schema, validation expectations
Ecosystem config: database storage, image, CPU/memory shape, event topic, artifact bucket, workflow placement
```

Protenix:

```text
App: protenix_prediction
Functionality: structure or complex prediction
Phenotypes: local GPU runner, batch prediction job, reactive worker, visualization/report surface
Core app config: model version, input package schema, prediction parameters, output structure/score contract
Ecosystem config: GPU class, model artifact mount, image, queue/topic, bucket roots, downstream topology scoring workflow
```

Complex structure harmonization:

```text
App: complex_structure_harmonization
Functionality: map native prediction outputs into comparable structure/result tables
Phenotypes: local dataframe proof, Spark harmonization job, workflow step, notebook review surface
Core app config: source output kind, hydrator version, output schemas, deduplication keys, validation expectations
Ecosystem config: raw artifact roots, table/catalog destinations, Spark surface, write mode, materialization consumers
```

Pattern Walker materialization:

```text
App: pattern_walker_materialization
Functionality: project harmonized tables into serving bundles and visual lookup artifacts
Phenotypes: batch materialization, reactive rebuild worker, Kube/Spark job, dashboard-fed artifact producer
Core app config: source table contract, materialization kind, output bundle schema, replacement strategy, validation expectations
Ecosystem config: serving bucket/root, table source locations, compute surface, route/index consumers, cleanup policy
```

## Review Heuristics

- If a file says "app" but mostly describes provider, Kube, bucket, or credential topology, move that material toward ecosystem/deploy/context ownership.
- If a wrapper contains domain logic, pull the logic back into the app service/runner.
- If a workflow copies app internals instead of invoking a typed app contract, define the boundary explicitly.
- If an aggregate app grows several near-duplicate scripts, promote the durable entrypoints into typed capabilities and select transient combinations through steps config.
- If two phenotypes require different domain defaults, ask whether they are truly the same functionality or whether the difference belongs in a named profile.
- If a concrete ecosystem repeats a broad core manifest, extract the stable shared contract and keep the concrete overlay thin.
- If a test fixture changes the app's apparent nature, move the pressure into `test.conf` or a named context pack.

## Related Skills

- Use [Configuration Guidelines](../config_skills/SKILL_CONFIGURATION_GUIDELINES.md) for app, ecosystem, context, and test resolution rules.
- Use [Ecosystem Guidelines](../config_skills/SKILL_ECOSYSTEM_GUIDELINES.md) for ecosystem-family and concrete overlay design.
- Use [Service Deployment Guidelines](../script_skills/SKILL_SERVICE_DEPLOYMENT_GUIDELINES.md) for service/image/deploy entrypoint shape.
- Use [Wielder Scripting & Evaluation Skills](../script_skills/SKILL_WIELDER_SCRIPTS.md) for thin script and mode propagation discipline.
- Use [Workflow Validation Doctrine](../test_skills/SKILL_WORKFLOW_VALIDATION_GUIDELINES.md) for phenotype validation through real configured workflows.
- Use [Data Ingestion Guidelines](../data_skills/SKILL_DATA_INGESTION_GUIDELINES.md), [Harmonization Guidelines](../data_skills/SKILL_HARMONIZATION_GUIDELINES.md), and [Table Schema Guidelines](../data_skills/SKILL_TABLE_SCHEMA_GUIDELINES.md) for source-transform-sink data app contracts.
- Use [Spark Scalable Validation Doctrine](../test_skills/SKILL_SPARK_SCALABLE_VALIDATION_GUIDELINES.md) for Spark phenotype validation.
