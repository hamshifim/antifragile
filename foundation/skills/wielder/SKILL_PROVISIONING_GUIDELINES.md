---
name: Provisioning Guidelines
description: Wielder doctrine for planning and provisioning durable infrastructure across one or more provider surfaces, including cross-cloud dependency checks, best-practice identity federation, and links to wielding surfaces such as Terraform, Kubernetes, WJobBard, storage cloning, and monitoring.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Provisioning Guidelines

Use this skill when planning, reviewing, or implementing durable infrastructure:
cloud projects/accounts, buckets, topics, service accounts, IAM/RBAC, secrets,
registries, scheduled jobs, Kubernetes resources, monitors, and cross-cloud
trusts.

## Core Principle

Provisioning is a dependency graph, not a pile of provider scripts.

Provider-specific resources should remain in provider-owned modules, but the
ecosystem provisioner owns ordering, completeness checks, and cross-provider
fact wiring. A partial resource in one cloud must not silently create a stale or
inconsistent resource in another.

## Shopping-List Provisioning

`workflow-wielder` should compose provisioning resources through configuration,
like a shopping list.

- Provider-owned modules remain reusable units: buckets, registries, pub/sub,
  clusters, front doors, auth, DNS, Spark, and similar durable resources.
- App and ecosystem config chooses bundles/modules by name; Python should
  resolve and order those configured selections, not hard-code one-off resource
  paths per workflow.
- A workflow may select a project/ecosystem-specific bundle list such as
  `static_resources`, `container_registries`, `super_cluster`, `front_door`,
  and `spark`, while the underlying Terraform modules stay reusable by
  provider surface.
- Durable-kernel versus ephemeral-runtime shapes should be selected by
  ecosystem overlays. Prefer a base ecosystem with zero/off defaults and a thin
  `<ecosystem>_ephemeral` include overlay that changes only module enabled
  flags, resource counts, deployment lists, and service activation keys.
- Provision and destroy gates must be separate. Permanent or shared resources
  such as DNS, domains, hosted zones, certificates, auth front doors, and
  shared registries may be provisioned by an app workflow but must only be
  destroyed through explicit opt-in config.
- `plan` must expose the selected shopping list before or alongside provider
  output: bundle names, resolved module names, durable-resource intent, and
  whether each module will create resources, update state only, or do nothing.

## Ecosystem Boundary

- Name ecosystems by operational capability, not by the current provider.
- Use abstract base ecosystems plus minimal concrete child overrides.
- A multi-cloud ecosystem may span GCP, AWS, Google Workspace, SaaS providers,
  local workstations, and Kubernetes surfaces.
- The runtime/control surface is only one property of the ecosystem. Example:
  `datalake_ingestion_raw` can run WJobBard on GCP while reading AWS S3 and
  using Google Workspace RBAC.
- Local machines may plan, provision, or launch; they are not runtime truth for
  hosted jobs.

## Completeness Checks

Before apply, the provisioner should inspect or derive enough facts to prevent
cross-cloud drift:

- identities that must exist or be created
- trust policies and federated issuers/audiences
- service account emails, role ARNs, topic names, bucket names, and regions
- IAM grants scoped to exact buckets, topics, secrets, and jobs
- runtime image references and registry access
- secret containers versus secret payloads
- scheduler/event trigger targets
- destructive/delete behavior and resources intentionally preserved

If one provider depends on a fact from another, that fact must be explicit in
the resolved config or produced by an earlier provision module output. Do not
copy values manually into a second tree.

## Security Rule

Best-practice workload auth is in scope; weaker auth is not a hidden fallback.

- Prefer provider-native workload federation over static keys.
- For GCP Cloud Run accessing AWS, target keyless AWS role assumption through a
  federated trust. Do not use AWS access keys or expiring session tokens as the
  steady-state design.
- Secret managers hold non-federatable secrets only. Terraform may create secret
  containers and IAM; payload versions are controlled by the security surface.
- Human access goes through configured groups, not individual ad hoc grants.

## Wielding Surfaces

Provisioning should link to the relevant wielding skill or functionality:

- Terraform provisioning for durable provider resources.
- Kubernetes workload skills for Deployments, Jobs, ConfigMaps, ServiceAccounts,
  and in-cluster handoffs.
- WJobBard for scheduled or event-triggered jobs and lifecycle/result events.
- WCloner/storage cloning for source/sink contracts and mirror semantics.
- WArgus/security for secrets, RBAC groups, runtime identities, and trust setup.
- Imager for registry, image build, and publication resources.
- Monitoring/observability entrypoints for completion, deletion alerts, and
  operator-facing inspection.

## Operator Plan Output

`show` and `plan` must expose the runtime contract, not only Terraform changes:

- where it will run: provider, region, project/account, surface, job/resource
- exact command and arguments
- materialized environment variables
- secret/env mappings without payload values
- auth type and runtime identity
- source/sink/provider endpoints
- trigger mode: manual, schedule, event, or combined
- inspect and execute commands
- distinction between planning-host paths and hosted runtime paths

## Anti-Patterns

- Asking the operator to export credentials before running a Wielder command.
- Treating `src=aws` and `dst=gcp` as an AWS ecosystem when control runs on GCP.
- Letting apps create durable topics, buckets, service accounts, or roles at
  runtime.
- Hiding durable resource selection in Python instead of expressing it as a
  config-owned bundle/module shopping list.
- Adding workflow-specific runtime booleans or one-off delete branches when an
  ecosystem overlay can express the resource subset as 0/off or N/on.
- Coupling provision and destroy toggles for reusable or permanent resources.
- Duplicating provider facts manually instead of wiring outputs or resolved
  config.
- Using static keys or expiring session tokens when federation is available.
- Hiding hosted runtime paths behind local workstation paths.
