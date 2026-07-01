---
description: Architectural form doctrine for Wielder apps as domain functionality expressed into ecosystem phenotypes through Wielder modes, including service, Spark, ingestion, harmonization, materialization, DAG-shaped wielders, minimal app config, core ecosystem contracts, aggregated app composition, and thin surface wrappers.
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
  + optional DAG-shaped wielder composition
  + thin operator surfaces
  + evidence/provenance
= Wielder app phenotype
```

## Four App Forms

Use four app forms to keep domain meaning separate from runtime expression:

| Form | Orchestrates | Owns |
| --- | --- | --- |
| **Domain app** | One bounded domain function | Domain logic, request/result contracts, state machine, evidence, and owned artifacts |
| **Domain DAG app** | Multiple domain functions in meaningful order | Dataflow, analysis flow, map/reduce shape, harmonization semantics, and domain-level success criteria |
| **Wielding app** | One app's runtime phenotype | Build, deploy, run, delete, test, observe, local/Kube/artifact expression, and owned lifecycle evidence |
| **Wielding DAG app** | Multiple wielding apps as one ecosystem | Provisioning, images, artifacts, topics, services, jobs, tests, monitoring, teardown, and ordered app delegation |

A domain DAG composes domain functions because the data or analysis has
meaningful internal stages. A wielding DAG composes runtime lifecycles because
several apps must be built, provisioned, deployed, tested, run, or deleted in
order.

A domain DAG may contain local map/reduce, streaming, batch, or harmonization
stages, but those are domain execution shapes. The wielding layer decides
whether the same capability runs in-process, as Spark, as a container job, as a
deployed service, or as a hybrid ecosystem.

### Archetype Genetics Example

Use vivid examples when teaching the boundary, but keep the doctrine generic.

- **Domain app:** `archetype_gene_extractor` reads one character dossier and
  extracts fictional phenotype genes such as `BEND_REALITY_XF2A`,
  `LUCK_FIELD_DOMINANT`, or `MONOLOGUE_ARMOR`.
- **Domain DAG app:** `trickster_archetype_research` starts with Bugs Bunny, the
  family hero, then compares neighboring archetype expressions such as Road
  Runner, Loki, and Hermes. It researches traits, extracts candidate genes, maps
  evidence, reduces conflicting observations, and harmonizes the result into
  phenotype tables.
- **Wielding app:** `archetype_gene_extractor_wielder` gives the extractor a
  runtime body: build artifact or image, run locally or as a job/service,
  provision topics, apply fixtures, monitor output, and delete owned outputs.
- **Wielding DAG app:** `scaled_trickster_research_wielder` provisions storage
  and messaging, builds extractors and harmonizers, runs the Bugs Bunny / Road
  Runner / Loki / Hermes research pipeline, trains a phenotype prediction model
  on harmonized data, monitors progress, and tears the ecosystem down.

Domain apps describe what the world means. Wielding apps decide how that
meaning gets a body, runs, scales, heals, and disappears.

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
App: model_inference
Functionality: configured model prediction
Phenotype: accelerator-backed reactive Kube worker
Ecosystem: provider/runtime/storage/event topology that makes it runnable
Surface: CLI/API/notebook/dashboard wrapper over the same core contract
```

At app entrypoints, `-es/--ecosystem` names a wrapper ecosystem: `wrapper/<name>` composes domain functionality with runtime surface. Bare `domain/*` and `surface/*` ecosystems are ingredients, not normal app runtimes.

App profiles may express portable phenotype intent such as GPU, Spark, batch, or reactive behavior. They must not hard-code a named runtime surface such as local Kind, EKS, GKE, EMR, Dataproc, or a child app wrapper; those belong in wrapper/surface ecosystems.

## App Identity And Entrypoints

Keep one app identity when several entrypoints share the same domain contract and
minimum success artifact, and differ only by lifecycle verb, transport,
scenario, or runtime phenotype. A local runner, Kubernetes Job, deployed
service, publisher, service-spec probe, and workflow-triggered run can be
different entrypoints or configurations of one app when they all operate the
same capability.

Split app identities when the durable contract changes: a different minimum
domain output, different cleanup ownership, different resource lifecycle,
different artifact/table contract, or different operator promise. A deployment
and a job are both Wielder app phenotypes; Kubernetes shape alone is not a
reason to merge unrelated capabilities or split one capability into separate
apps.

An app entrypoint should dispatch one of the app's typed capabilities after
canonical config resolution. It should not become a private workflow loader, a
second ecosystem resolver, or a bundle of child-app CLI overrides. Parent
workflows may choose which app entrypoint to call, but the child app still owns
its own resolved contract, lifecycle, cleanup, and evidence.

## Aggregating Wielder App Form

An app may aggregate multiple entrypoints when the domain functionality is naturally a mix-and-match capability rather than one fixed route.

When the aggregate's durable job is to compose a bounded set of Wielder-managed
apps into one ecosystem capability, prefer the `<domain>_wielder` convention.
This names the app as a concrete DAG-shaped switchboard: it selects a configured
set of sibling apps or typed entrypoints, passes the Wielder modes each sibling
needs, preserves ordering, and records evidence for what actually happened.

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
app capabilities: stable sibling apps and typed entrypoints
steps config: selected DAG sequence for this phenotype, test, context, or operator run
wielder: orchestrates selected steps and evidence
```

The steps config should be app-owned when the aggregate owns the reusable DAG.
Use `steps.conf` included by `app.conf` for durable step sets, and let test,
context, or developer overlays select or modulate those step sets. The important
boundary is that transient step choice belongs in configuration, while entrypoint
implementations remain stable typed capabilities.

This gives reactive systems an ad hoc composition surface without turning the app into a pile of one-off scripts. A reactive event can select "search only", "search plus prediction", "prediction plus materialization", or "full workflow" by resolving a configured step set and then emitting evidence for the actual steps executed.

For a `wielder` app, organize steps by verb family first, then by app:

```text
steps.<set>.apply
steps.<set>.delete
steps.<set>.run
steps.<set>.provision
steps.<set>.images
steps.<set>.artifacts
```

The main entrypoint branches by verb family first. `plan`, `apply`, `show`,
`probe`, and `init` normally use the `apply` sequence; `delete` and
`plan-delete` use the `delete` sequence; `run` uses the `run` sequence. Class
entrypoints such as `<domain>_wielder_provision.py`,
`<domain>_wielder_images.py`, and `<domain>_wielder_artifacts.py` expose the
corresponding configured class sequence through normal Wielder actions. Do not
invent global pseudo-actions such as `--images` or `--artifacts` when a typed
entrypoint can use `-w plan/apply/delete`.

The selected step set should name sibling apps or typed sibling entrypoints,
not private implementation chores. It is acceptable to have class steps named
`images`, `artifacts`, and `provision`, and leaf typed entrypoints such as
`model_image` or `runtime_artifacts`; avoid private verbs such as
`build_model_image` or `publish_runtime_artifact` in the top-level DAG. The
aggregate app decides order and mode. Each child app decides its own image,
artifact, deployment, cleanup, runtime behavior, and evidence from its resolved
config.

For Wielder materialization, use the DAG as a switchboard, not as an owner of
child internals. The wielder may call an `images` class entrypoint before
provisioning so image failures appear before scarce resources are allocated;
that class entrypoint then delegates to app-owned image materializers. The same
rule applies to artifact publication and infrastructure provisioning. If a
service deploy path calls its own image or artifact helper again, the helper
should be reuse-aware and idempotent rather than relying on a Python
`already_built` side channel.

## Reactive Resource Preflight And Self-Healing

Reactive apps should expose explicit lifecycle entrypoints for the message
resources they own, such as topics, queues, subscriptions, callback groups, or
dead-letter channels.

Use the aggregate DAG to order those resources before workers:

```text
provision broker/surface
  -> provision app-owned topics/queues
  -> deploy workers/services
  -> start streaming jobs/monitors
```

On delete, stop consumers before deleting their message resources:

```text
stop publishers/workers/streaming jobs
  -> delete or empty app-owned topics/queues
  -> delete broker/surface if selected
```

Each app should own small lifecycle functions for its own reactive resources:

```text
plan_<app>_topics
ensure_<app>_topics
delete_<app>_topics
empty_<app>_fixture_topics
```

The aggregate app may sequence these functions, but it should not reconstruct
topic names, endpoints, consumer groups, or retry policy itself. Those remain
resolved config consumed by the child app's typed contract.

It is good practice for services to retain a self-healing startup path, such as
`ensure_topics_on_start`, when the ecosystem contract allows mutation. This is a
fault-tolerance fallback: it lets a worker recover from a missing topic or a
partial operator run. It is not a substitute for the explicit DAG preflight,
because relying only on lazy startup makes ordering, delete semantics, and test
evidence ambiguous.

Streaming and long-running consumers should use the same pattern. A Spark
streaming job, queue consumer, monitor, or callback listener should verify or
repair its app-owned message resources immediately before subscribing, and
again before writing to error/dead-letter channels. The aggregate DAG still
orders topic/queue preflight first; the consumer-side repair handles races,
operator interruption, stale local bridges, or topic deletion between workflow
apply and runtime startup.

Do not confuse consumer self-repair with durable listening. A one-shot trigger
such as "available now" can finish successfully before a publisher emits later
messages; that is useful for replay/backfill, not for a standing reactive app.
Default workflow phenotypes that are meant to receive future traffic should run
as durable services/jobs with processing-time or equivalent continuous triggers,
and transient test config can select bounded replay behavior when needed.

For data-pipeline aggregates, expose a class entrypoint for the pipeline stage,
such as `harmonization`, the same way an app exposes `images`, `artifacts`,
`topics`, or `provision`. The aggregate may call the class entrypoint inside the
full DAG, while operators can invoke it directly for diagnosis or restart. The
child harmonization apps still own their Spark source, transform, sink,
checkpoint, and cleanup contracts.

Class entrypoint scripts should be stable, thin wrappers over a shared CLI
support module. Avoid copy-pasting source bootstrap logic into every `images`,
`artifacts`, `topics`, `provision`, or `harmonization` file. Keep the old
callable names and paths stable for operators, but centralize the step-family
selection and direct-script bootstrap mechanics.

When a child step fails, the aggregate DAG should record the failed app, family,
action, and exception type/message in the parent report before re-raising. This
is not a retry policy and should not swallow failure. It is an operator
continuity pattern: a failed workflow leaves a crisp breadcrumb about where the
DAG stopped.

A streaming harmonization job must fail loudly before Spark starts if no
streaming source is resolved. In a Kafka shape this means the app validates the
resolved bootstrap endpoint, source topic, error/escalation topic, and
app-owned topic preflight report before creating the streaming reader. Do not
allow an inert Spark query to count as a successful harmonization listener.

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

## Functional Success Boundary

A phenotype's success evidence must prove the app's minimum domain output, not merely a nearby nuisance artifact. Input packages, resolved config sidecars, command previews, staged jobs, log roots, and notebook bundles are supporting materializations. They do not prove preparation, prediction, scoring, harmonization, reporting, or visualization unless the corresponding configured app entrypoint actually produced the domain artifact or table.

Do not let a test fixture, mock binary, bypass branch, or synthetic artifact write native success markers or plausible domain outputs under the app's real output contract. If an app has a "prepare input" capability, model it as its own entrypoint/status; do not let it masquerade as "prediction succeeded".

## Ecosystem Shape

Separate ecosystem concerns by durability and ownership.

- Core ecosystems own shared contracts: buckets, topics, registries, table schemas, artifact roots, app relationships, reusable communication contracts, and default cross-app behavior.
- DAG-shaped wielder apps own reusable app composition and step ordering; wrapper ecosystems select the domain and surface ingredients that make that composition runnable.
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

For cross-app reactive handoffs, the downstream app should ask the upstream
domain service through the service contract, using either an existing result id
or a minimal/full identity that the upstream can resolve. The upstream owns
lookup, materialization, and result/promise semantics. If the result is absent,
the upstream returns a promise and later emits a completion event; downstream
callers subscribe for the relevant promise ids and accumulate completions. Do
not make the downstream app inspect the upstream artifact layout or block a
service call while waiting for a long-running upstream run.

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

Data preparation:

```text
App: data_preparation
Functionality: search, normalization, clustering, or feature preparation
Phenotypes: local SDK runner, batch job, reactive worker, Kube service
Core app config: datasets consumed, input contract, output feature/result schema, validation expectations
Ecosystem config: database storage, image, CPU/memory shape, event topic, artifact bucket, workflow placement
```

Model inference:

```text
App: model_inference
Functionality: configured prediction or scoring
Phenotypes: local accelerator runner, batch prediction job, reactive worker, visualization/report surface
Core app config: model version, input package schema, prediction parameters, output artifact/score contract
Ecosystem config: accelerator class, model artifact mount, image, queue/topic, bucket roots, downstream reporting workflow
```

Result harmonization:

```text
App: result_harmonization
Functionality: map native prediction outputs into comparable result tables
Phenotypes: local dataframe proof, Spark harmonization job, workflow step, notebook review surface
Core app config: source output kind, hydrator version, output schemas, deduplication keys, validation expectations
Ecosystem config: raw artifact roots, table/catalog destinations, Spark surface, write mode, materialization consumers
```

Viewer materialization:

```text
App: viewer_materialization
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
- Use [Unique Name Identity](SKILL_UNIQUE_NAME_IDENTITY.md) when app phenotypes
  provision resources, publish images or Spark/Python artifacts, stage resolved
  config, or need context-selected runtime siloing.
- Use [Ecosystem Guidelines](../config_skills/SKILL_ECOSYSTEM_GUIDELINES.md) for ecosystem-family and concrete overlay design.
- Use [Service Deployment Guidelines](../script_skills/SKILL_SERVICE_DEPLOYMENT_GUIDELINES.md) for service/image/deploy entrypoint shape.
- Use [Wielder Scripting & Evaluation Skills](../script_skills/SKILL_WIELDER_SCRIPTS.md) for thin script and mode propagation discipline.
- Use [Workflow Validation Doctrine](../test_skills/SKILL_WORKFLOW_VALIDATION_GUIDELINES.md) for phenotype validation through real configured workflows.
- Use [Reactive Distributed Integration Testing](../test_skills/SKILL_REACTIVE_DISTRIBUTED_INTEGRATION_TESTS.md) when an app phenotype crosses topics, queues, callbacks, or post-action events.
- Use [Strict FS Agnosticism](../data_skills/SKILL_STRICT_FS_AGNOSTICISM.md) when app handoffs or evidence cross buckets, object keys, table sinks, or opaque URIs.
- Use [Data Ingestion Guidelines](../data_skills/SKILL_DATA_INGESTION_GUIDELINES.md), [Harmonization Guidelines](../data_skills/SKILL_HARMONIZATION_GUIDELINES.md), [PySpark Guidelines](../data_skills/SKILL_PYSPARK_GUIDELINES.md), and [Table Schema Guidelines](../data_skills/SKILL_TABLE_SCHEMA_GUIDELINES.md) for source-transform-sink data app contracts.
- Use [Spark Scalable Validation Doctrine](../test_skills/SKILL_SPARK_SCALABLE_VALIDATION_GUIDELINES.md) for Spark phenotype validation.
