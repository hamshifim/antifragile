---
name: Service Deployment Guidelines
description: Wielder doctrine for service-named image and deploy entrypoints, including plan/apply/run/delete/monitor command shape, image provenance, WJobBard composition, and hosted runtime boundaries.
---


# Service Deployment Guidelines

Use this skill when creating, refactoring, or reviewing a Wielder-managed service deployment surface: image scripts, deploy scripts, runtime config, triggered jobs, or operator commands.

## Critical Assessment

- Extract this skill because service deployment is a layer above `WJobBard`, `WCloner`, Terraform, Kubernetes, and image building.
- Do not overload [WJobBard Guidelines](SKILL_WJOBBARD_GUIDELINES.md) with service identity rules. WJobBard is a triggered job mechanism; a service deployment surface is what an operator recognizes and runs.
- Do not create service deployment doctrine for one-off leaf scripts that have no durable image, runtime, or operator lifecycle.
- Do not hide missing framework capability behind app-specific boilerplate. If several services need the same deploy mechanics, improve the local deploy wrapper pattern first; only change Wielder core after explicit architectural review.

## Naming Contract

- Use `<service_name>_image.py` for the image surface.
- Use `<service_name>_deploy.py` for the deploy/run/monitor/delete surface.
- The service name should be the workload a human recognizes, such as `provider_ingestion_dispatcher`, `data_ingestion_job_runner`, or `raw_mirror_manual_sync`.
- Avoid helper-framework names in operator-facing files. Prefer `provider_ingestion_dispatcher_deploy.py` over `provider_ingestion_wjobbard.py`.
- Avoid provider names in service identity unless the service is truly provider-specific. Provider choice should usually live in ecosystem/app config.

## Deployment Contract

- `plan` renders intent and validates config without mutation.
- `apply` reconciles durable infrastructure or deployment state. It should not start dormant jobs by default.
- `run` starts an already-provisioned dormant execution, such as a Cloud Run Job.
- `monitor` observes the current or recent execution without changing infrastructure.
- `delete` removes durable resources only when the delete config explicitly allows it.
- Long-running `apply`, image build/push, sync, or job execution should be handed to the operator unless they explicitly ask the agent to run and wait.

## Service Spec And QA Endpoints

A deployed service often needs a second operator surface that exercises the
already-defined service contract without provisioning, building images, or
deploying workloads. Treat this as a service-spec endpoint, not as part of the
deploy endpoint.

- Use a separate endpoint such as `<service_name>_test.py`, `<service_name>_qa.py`,
  or `<service_name>_spec.py` when the operator intent is "test the service
  contract" rather than "reconcile runtime infrastructure".
- The service-spec endpoint should still use Wielder action/config semantics:
  `plan` reports the resolved service target, test fixture, topics, bucket keys,
  and exact test command; `apply` runs the configured tests or probes; `delete`
  removes only configured test outputs.
- Do not make service-spec endpoints provision dependencies, build images,
  deploy services, install Kafka, or create clusters. If dependencies are
  missing, fail or skip with a clear petition to run the owning deploy/provision
  endpoint.
- Put service-spec command shape in HOCON, usually under a tree such as
  `<service>.service_specs.<spec_key>`. Python should validate and execute the
  resolved spec, not hardcode test files, fixture UUIDs, or provider endpoints.
- Test fixtures still belong in `-t` overlays. A service-spec endpoint may
  require `-t` for destructive or fixture-backed QA, and should say so in plan.
- Keep cleanup scoped to the spec's configured outputs. A service-spec `delete`
  should not imply infrastructure teardown.

## Runtime Observability

Use [Runtime Event Logging](../ops_skills/SKILL_RUNTIME_EVENT_LOGGING.md) for
long-running services, model workers, black-box subprocesses, Kafka consumers,
Spark jobs, and workflow steps whose lifecycle is otherwise hidden behind a
quiet log. A deployment surface should expose or compose the app's own typed
status, heartbeat, monitor, and runtime-stat contracts instead of reconstructing
them in the parent workflow.

## Operator GUI Apply And Version Locks

Operator-facing GUI apply is a deployment operation, not a build operation.
It must consume an immutable version lock produced upstream by a stage-tier
promotion and CI/CD artifact materialization path.

- The selected `stage_tier` may identify a tier branch such as `dev`, `stage`,
  or `prod`, but the GUI must resolve that branch to a concrete super-repo SHA
  and artifact manifest before applying.
- The manifest is the runtime lock. It must include all artifacts required by
  the workload: image digests, resolved config artifacts, Kubernetes or Helm
  manifests, Terraform/OpenTofu module or plan refs, WJobBard/workflow/DAG
  specs, Spark packages, Python package refs, schema versions, lookup tables,
  model weights, database/index refs, and any other workload-specific runtime
  artifacts.
- If the manifest is absent or incomplete, GUI apply must fail closed and tell
  the operator which artifact class is missing. It must not pack images,
  generate missing deploy artifacts, or use dirty checkout state as runtime
  truth.
- Apply should record the consumed version lock so later `run`, `monitor`, and
  result callbacks can reference the active source/artifact set.
- Advanced or CI/CD views may expose build/pack commands as handoff actions,
  but those actions are not the default GUI apply path.

Local development and integration harnesses may still offer an explicit
build-and-apply workflow when the operator deliberately asks to validate image
or artifact production itself. Name that path as CI/dev artifact production,
not as ordinary GUI apply.

## Image Provenance

- If hosted runtime code or Docker assets changed, commit the owning submodule before relying on a rebuilt hosted image.
- Image ensure may check registry state and build when configured, but it must not pretend uncommitted local code exists inside an already published image.
- Image scripts may compose shared base images, but the service image name should remain workload-oriented.
- Service image materialization should be exposed as a small reusable leaf helper. Parent wielders may call it in an early `images` class pass, and the service deploy path may call it again before deployment. Do not add wielder-only "preflighted" state to suppress a second call.
- Keep image build and image publication as separate image-entrypoint concerns where the backend supports that distinction. If the current helper performs build-and-publish together, the config should still preserve an explicit image class step so the contract can grow without changing the wielder shape.
- For operator-facing deploy/apply, image ensure should validate that the locked
  image reference exists and is usable. It should not build or push images
  unless the active surface is explicitly an image/artifact production surface.

## Configuration Rules

- Resolve the service through the canonical app accessor, usually `get_app_conf("<app>")`.
- Durable behavior belongs in HOCON: selected jobs, provider surfaces, triggers, identities, timeouts, polling, delete flags, and image app names.
- In hybrid ecosystems, service placement is per service. The deploy surface
  should read its own resolved placement contract, such as local process,
  Kubernetes Deployment/StatefulSet/Job, Spark job, or provider-managed runtime.
  Do not infer placement from the parent workflow name or assume every sibling
  service shares the same local/kube state.
- Kubernetes deploy config is canonical beside the code app it deploys: object
  HOCON, manifests, service accounts, jobs, statefulsets, and deploy entrypoints
  live with the app surface. Ecosystems select and modulate those deploy
  contracts through resolved leaves such as deployment lists, prune lists,
  replica counts, resources, ports, registry authority, and service deploy
  steps. Do not move kube config out of the app merely because a future non-kube
  runtime may exist.
- Kube workload identity belongs in the deploy contract. Deployment,
  StatefulSet, and Job templates should render `pod_security_context` and
  `container_security_context` from resolved config. Keep exact Unix uid/gid
  values in the surface or wrapper ecosystem when they are needed for local
  POSIX storage such as `hostPath`, local PV, mounted buckets, or NFS-like
  volumes.
- Do not generalize local filesystem write fixes into cloud storage doctrine.
  Object stores are credential surfaces; local POSIX storage is an ownership
  surface. A service deploy change may need both a future-write security
  context and a separate local cleanup or ownership repair for old files.
- CLI arguments should stay at Wielder modulation level: ecosystem, stage tier, context, security, canary, and action.
- Developer-local choices belong in `context_conf/<name>/developer.conf`, not ad hoc environment variables or private parsers.
- A service that orchestrates another repo may read that repo through its canonical accessor, but should extract only the fields it needs.

## Composition Rules

- Use [WJobBard Guidelines](SKILL_WJOBBARD_GUIDELINES.md) when the service provisions or runs scheduled/event-triggered jobs.
- Use [Wielder Imager & Staging Sandboxing](../ops_skills/SKILL_WIELDER_IMAGER.md) when image staging, Dockerfiles, registry tags, or committed-state provenance are in scope.
- Use [Provisioning Guidelines](../ops_skills/SKILL_PROVISIONING_GUIDELINES.md) when the service creates cloud resources, IAM, topics, service accounts, or Terraform-managed assets.
- Use [Security Guidelines](../ops_skills/SKILL_SECURITY_GUIDELINES.md) when the service touches secrets, OAuth, IAM, RBAC, cross-cloud credentials, or runtime identities.
- Keep payload domain logic in the payload app. The deploy service should select, provision, run, and monitor; it should not reimplement the domain workflow.

## Operator Handoff

When finishing a service deployment change, provide one-line absolute commands for the relevant actions:

```bash
/home/<operator>/workspace/<repo>/src/.../<service_name>_image.py --ecosystem <ecosystem> --stage_tier <stage> --context_conf <context> -w plan
/home/<operator>/workspace/<repo>/src/.../<service_name>_deploy.py --ecosystem <ecosystem> --stage_tier <stage> --context_conf <context> -w plan
/home/<operator>/workspace/<repo>/src/.../<service_name>_deploy.py --ecosystem <ecosystem> --stage_tier <stage> --context_conf <context> -w apply
/home/<operator>/workspace/<repo>/src/.../<service_name>_deploy.py --ecosystem <ecosystem> --stage_tier <stage> --context_conf <context> -w run
/home/<operator>/workspace/<repo>/src/.../<service_name>_deploy.py --ecosystem <ecosystem> --stage_tier <stage> --context_conf <context> -w monitor
```

Only include commands that actually exist for the service.
