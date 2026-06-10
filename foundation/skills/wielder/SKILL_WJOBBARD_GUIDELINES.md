---
name: WJobBard Guidelines
description: Wielder doctrine for scheduled or event-triggered jobs that execute a configured target and emit lifecycle/result events.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# WJobBard Guidelines

Use this skill when planning, implementing, or reviewing Wielder-managed jobs that are triggered by schedules or event topics and then run a configured payload such as `WCloner`.

For broader service image/deploy entrypoint shape, also apply [Service Deployment Guidelines](SKILL_SERVICE_DEPLOYMENT_GUIDELINES.md). WJobBard is the triggered-job mechanism; the service deployment skill owns the human-facing service command shape.

## Core Contract

- `WJobBard` is a triggered job abstraction, not a clone abstraction.
- `WJobBard` is also not the service identity. Human-facing entrypoints should be named after the service or workload, such as `provider_ingestion_dispatcher_deploy.py`, not after the helper framework.
- The job owns triggering, runtime identity, lifecycle reporting, and the link to the payload target.
- The payload target owns domain details. For clone jobs, `WCloner` still owns source, sink, sync type, flags, backend config, RBAC, and destination creation.
- `apply` reconciles durable job infrastructure; it must not start the job by default.
- `run` starts one job execution; it must not change or delete durable infrastructure.
- `monitor` observes job execution state and logs; interrupting local monitoring must be harmless to the remote job.
- `delete` is the explicit durable-resource cleanup path. Do not hide cleanup in local `finally` blocks.
- A job may be triggered by a schedule, by an event topic, manually, or by several of these at once.
- A job may emit operational lifecycle events and optional domain result events.
- `input_event_types` and `output_event_types` are explicit lists; either list may be empty.
- Workflow grouping is allowed, but batching/ordering belongs above individual job execution. The first implementation may model workflows without executing all workflow semantics.

## Configuration Rules

- The fully qualified identity must be derived from the resolved config tree plus the local job key. CLI flags may select mode; they must not become the identity source.
- Keep app-level defaults empty and override concrete jobs in `context_conf/<name>/developer.conf` or the owning app/ecosystem config.
- The target reference should point to an existing configured contract, such as a `WCloner` job key, rather than duplicating target fields inside `WJobBard`.
- Stage tier must appear in permission-bearing resources such as runtime service accounts, schedules, topics, and secrets.
- Use provider surfaces only for provenance and dispatch. Provider-specific resource mechanics belong in provider implementations or Terraform modules.
- A service that uses WJobBard should expose a thin service-named deploy wrapper that selects the configured job or workflow. Avoid making operators call generic WJobBard scripts with memorized job keys when a stable service exists.
- `image_ensure` belongs to the deploy orchestration layer. It may verify or build the required image before provisioning, but it must not smuggle uncommitted code into a hosted runtime.

## Provisioning Boundary

- Durable cloud resources are provisioned declaratively through the owning provisioning app and Terraform-like modules.
- The Wielder entrypoint owns orchestration: which job config is selected, which module is invoked, and how the resulting runtime command references staged config.
- Do not let domain apps create their own long-lived schedules, topics, buckets, or service accounts.
- For cross-cloud jobs, also apply [Provisioning Guidelines](SKILL_PROVISIONING_GUIDELINES.md): the ecosystem provisioner must wire provider facts, validate completeness, and expose the runtime auth/path/command contract in `show` and `plan`.

## Runtime Surfaces

- GCP: use Cloud Run Jobs for bounded executions, Cloud Scheduler for cron triggers, and Pub/Sub -> Eventarc -> Workflows -> Cloud Run Jobs API for event triggers.
- AWS: use native scheduler/event services and IAM-scoped runtimes when that surface is implemented.
- Local: may run a job process directly for development, but this should still resolve the same config contract.
- Hosted jobs should receive runtime identity through provider-native metadata, federation, or secret-manager bindings. Do not design hosted WJobBard jobs around local OAuth tokens, local `gcloud` state, or a developer's encrypted rclone config.
- If a job can run locally and hosted, encode that as a config-selected runtime surface. Local provider-specific semantics should be explicit, for example `local_aws` or `local_gcp`, not an ambiguous generic `local`.

## Handoff Discipline

- Milestone 1 should validate typed config and show/plan output only.
- Milestone 2 should add provider resource rendering/provisioning and runtime command handoff.
- Agents should run `show` or `plan` locally. Long-running `apply` executions should be handed to the operator unless explicitly requested.
- The final operator handoff should include one-line absolute commands for image, deploy `plan`, deploy `apply`, `run`, and `monitor` when those actions exist.
