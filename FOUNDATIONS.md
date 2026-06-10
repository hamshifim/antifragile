# Foundations

This document states the root-level architectural philosophy of `wielder-antifragile`.

Claims here are tagged by maturity where it matters. `OPERATING` marks capabilities in production use today; `EMERGING` marks partially-built capabilities evolving under production pressure; `ASPIRATIONAL` marks intended direction that is not yet real. Read these tags literally. The gap between what operates and what is aspirational is the most common source of confusion about this system, and collapsing it — in either direction — is itself an antipattern.

## Front-And-Center Concepts

`wielder-antifragile` treats ephemeral super-clusters as a primary engineering strategy.

An ephemeral super-cluster is a configurable, multi-surface, multi-tier distributed environment that can be provisioned, exercised, observed, and torn down as one coherent workflow family. In development, testing, QA, and staging, this ephemerality reduces the delta between workstation coding, image build, CI/CD, and real distributed execution.

The same machinery can also maintain long-lived production surfaces in situ. The difference is carried by configuration and policy, not by switching to a different architectural species.

## Glossary

- `app`: the enduring managed unit in Wielder configuration. An app can be built, deployed, deleted, rebuilt, monitored, load-tested, or maintained while remaining the same configured unit.
- `deploy`: an operational expression or action against an app. Deployment is one important manifestation of an app, but it is narrower than the app itself.
- `workflow`: an orchestrated DAG that coordinates apps, dependencies, publishers, monitors, consumers, provisioning, and teardown.
- `ecosystem`: the resolved execution topology that determines how surfaces, dependencies, transports, and operational modes cooperate.
- `surface`: the material execution plane or transport boundary through which a workload or dependency is expressed.
- `ephemeral super-cluster`: a temporary but real distributed environment assembled from the same workflow family used elsewhere, configured for validation or execution and later torn down when no longer needed.

## Core Thesis

Wielder workflows are a unified validation, testing, and execution surface for distributed systems.

The same workflow family can operate as:
- a unit test
- an integration test
- a system test
- a load test
- a production execution path

The same workflow family can also serve as a testing framework by coordinating:
- publishers and traffic generators
- monitors and observers
- consumers and workers
- provisioning and teardown steps

The distinction is not the existence of a different script. The distinction is the resolved operational mode across configuration axes such as:
- `ecosystem`
- `surface`
- `stage_tier`
- workload scale
- data volume
- retention and teardown policy

This reduces the delta between:
- workstation development
- image build
- CI/CD
- configured DAG execution

One direct consequence is a lower probability of "it worked on my computer" bugs, because the workstation path converges earlier with the real build, deploy, and runtime path.

The same workflow can be epigenetically phenotyped by configuration into a unit test, an integration test, a system test, or a load test without becoming a different workflow species.

The same doctrine extends to mix-and-match deployment across multi-tiered DAGs. Different tiers, services, and transports can be recombined by configuration while remaining inside the same workflow family.

The same doctrine also explains why Wielder keeps the primary noun as `app`. An app is the enduring managed unit. Deployment is one important operational expression of that app inside an ephemeral or persistent distributed environment.

## HOCON as the Canonical Tree

`wielder-antifragile` treats HOCON as the canonical configuration tree.

That tree is the semantic source of truth. Other configuration surfaces are projections or materializations of that source, including:
- YAML
- JSON
- `tfvars`
- build inputs such as Gradle or Maven properties

The value is not that every downstream language becomes inherently reusable. The value is that intent is defined once in a nested canonical tree and rendered outward into the required target surfaces.

This is what enables DRY configuration across multiple runtimes without hand-maintaining parallel truths.

The same idea applies to validation scale. A single canonical configuration tree can modulate the same workload family from a tiny deterministic probe through broader integration, system, and load execution without inventing a second testing architecture.

## Ecosystems as Execution Topology

An ecosystem is a description of execution topology.

It expresses:
- which dependencies are local
- which dependencies are remote
- which surfaces are involved
- how those surfaces cooperate

This allows the same codebase to express different operational phenotypes across different surface sets.

One useful metaphor is:
- the codebase is the genotype
- the resolved configuration is the expression mechanism
- each ecosystem and surface set expresses a different phenotype

This metaphor is useful as intuition, but the mechanism is deterministic. The phenotype is not emergent guesswork. It is the reproducible result of explicit configuration resolution.

## Workflow Unification

A workflow that resolves topology, builds images, provisions dependencies, deploys services, bridges access, and runs the target workload should be treated as a primary harness.

That harness can include active test actors such as publishers as well as observational actors such as monitors. In that sense, the workflow is also a testing framework: it hosts the target system, drives it, and inspects it through the same configured surface.

This is the operational expression of the ephemeral super-cluster idea: the workflow does not just launch isolated deploy artifacts. It assembles a temporary but real distributed system slice that can act as a unit probe, an integration harness, a system test, a load surface, or a production path depending on configuration and policy.

When reproducibility matters, `delete -> apply` is stronger than incremental patching because it proves that the environment can be reconstructed from committed source of truth.

When a workflow `apply` bakes images, that operation is committed-state by design:
- the relevant image-bearing submodule changes should be committed
- the super-repo pointer update should be committed
- then the image builder should be wielded
- then the workflow should deploy that exact version

In this model, the resulting diff is the exact delta that was exercised.

Rollback is achieved through super-repo commit history. In this model, a single supermodule commit hash is a version boundary: it captures the tracked submodule pointers and therefore the exact committed distributed state that can be rebuilt, redeployed, or restored.

## Spark Scalable Validation

Spark validation should be treated as one configurable continuum.

The same Spark pipeline family can operate as:
- a unit-scale deterministic probe over tiny fixtures
- an integration or system path over real sources and sinks
- a load surface modulated by pressure settings such as iterations, pauses, channels, and synthetic duplication

The distinction should come from:
- source size
- sink realism
- pressure configuration
- runtime scale

not from a separate logic tree for each test label.

This was already visible in older Nudnik-style Spark patterns:
- a tiny resource-backed test exercised real Spark logic against precise expected values
- the same family could then restore or synthesize real-shaped records into Kafka or Cassandra
- pressure blocks modulated the same core path into a higher-scale validation surface

This is the Spark form of the same wider Wielder philosophy:
- keep the core path stable
- modulate scale and realism through configuration
- reduce the delta between local validation and operational truth
- epigenetically phenotype the same workflow from unit scale through load scale

## Mix-And-Match Multi-Tier DAGs

Distributed DAGs should be composable across deployment tiers.

That means:
- one tier may run locally while another runs on Kubernetes
- one dependency may stay SDK-local while another resolves through a service boundary
- one DAG slice may remain unit-scale while an adjacent slice is load-oriented

The orchestration goal is not to create a different DAG species for every deployment permutation. The goal is to keep the workflow family stable and let configuration mix and match the participating tiers, surfaces, and transports.

## Deterministic Adaptive State

Status: `OPERATING`.

The first stage of antifragility is deterministic transient adaptation over time without changing the codebase.

Examples:
- high traffic spike triggers `+3` Terraform nodes
- the same event triggers `+20` Kubernetes replicas
- traffic wanes and those quantities are reduced on the same codebase

No new commit is required for each transient adaptation. The agent is not editing source. The agent is navigating an already authorized state space.

This is still deterministic:
- the policies are committed
- the thresholds are committed
- the allowed transitions are committed
- the codebase stays fixed

## Source Repair Under Policy

Status: `ASPIRATIONAL` (in active development). This section describes intended behavior, not current capability. The loop is not yet working unsupervised; it is wishful by honest admission and is evolving under production pressure.

A stronger stage of antifragility is source-changing adaptive repair.

In that envisioned mode, an agent can:
- analyze a bug
- localize the failure
- patch the code or config
- run the relevant validation
- commit
- rebuild
- deploy

This is qualitatively different from transient scaling.

The distinction is:
- transient scaling modulates phenotype on the same genotype
- hotfix repair edits the genotype and then expresses a new phenotype

This mode should remain policy-governed:
- authority boundaries
- allowed files
- required tests
- rollout strategy
- rollback path

The substrate for this loop largely exists already: committed-state determinism, rollback-by-commit-hash, and policy boundaries are delivered by the `OPERATING` rungs above. What remains unproven is the stochastic actor inside that substrate — whether an agent can be trusted to localize, patch, and validate without supervision. That gap, not the harness, is why this rung is aspirational. The bet is on agent competence improving, not on the loop being built.

## Antifragility Trajectory

This trajectory is a roadmap, not a description of the present. The rungs differ sharply in maturity, and that difference is load-bearing.

Maturity vocabulary:
- `OPERATING` — in production use today, proven under real workloads.
- `EMERGING` — partially built and exercised, evolving under production pressure, not yet trustworthy unsupervised.
- `ASPIRATIONAL` — intended direction, not yet real; wishful by honest admission.

The trajectory is:

1. Deterministic workflow unification — `OPERATING`
2. Deterministic transient state adaptation — `OPERATING`
3. Source repair under policy — `ASPIRATIONAL` (in active development)
4. Closed-loop antifragility across both state and code — `ASPIRATIONAL`

The word *deterministic* applies to the committed substrate — policies, thresholds, allowed transitions, rollback boundaries — never to agent behavior, which is stochastic. Rungs 1–2 are deterministic end to end because no stochastic actor sits in the loop. Rungs 3–4 place a stochastic actor (the repairing agent) inside a deterministic harness; calling them "deterministic" would describe only the guardrails, not the agent, and is therefore avoided here.

When all four rungs operate, the system is deployable, adaptive over operational state, and capable of repairing source-level faults over time while remaining auditable and reproducible. Today, rungs 1–2 deliver the operational and transient-adaptive half of that sentence. The source-repair half is the wager — a deliberate convex bet on agent competence, cheap if it stalls and large if it arrives, not a claim about the present.

## Design Biases

`wielder-antifragile` favors:
- one canonical nested configuration tree
- thin orchestration scripts
- reusable workflow families instead of script proliferation
- committed-state image determinism
- explicit topology over hidden local hacks
- reduced deltas between local development and runtime reality
- policy-bounded agentic adaptation instead of improvisational state changes

These are not incidental preferences. They are the foundation that allows deterministic distributed systems to become antifragile over time.
