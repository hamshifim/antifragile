---
name: Service Deployment Guidelines
description: Wielder doctrine for service-named image and deploy entrypoints, including plan/apply/run/delete/monitor command shape, image provenance, WJobBard composition, and hosted runtime boundaries.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

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
- For operator-facing deploy/apply, image ensure should validate that the locked
  image reference exists and is usable. It should not build or push images
  unless the active surface is explicitly an image/artifact production surface.

## Configuration Rules

- Resolve the service through the canonical app accessor, usually `get_app_conf("<app>")`.
- Durable behavior belongs in HOCON: selected jobs, provider surfaces, triggers, identities, timeouts, polling, delete flags, and image app names.
- Kubernetes workload subsets belong in ecosystem HOCON. A workflow should not
  carry a special "runtime enabled" flag when the active ecosystem can choose
  the deployment list, prune list, replica counts, and service deploy steps.
- CLI arguments should stay at Wielder modulation level: ecosystem, stage tier, context, security, canary, and action.
- Developer-local choices belong in `context_conf/<name>/developer.conf`, not ad hoc environment variables or private parsers.
- A service that orchestrates another repo may read that repo through its canonical accessor, but should extract only the fields it needs.

## Composition Rules

- Use [WJobBard Guidelines](SKILL_WJOBBARD_GUIDELINES.md) when the service provisions or runs scheduled/event-triggered jobs.
- Use [Wielder Imager & Staging Sandboxing](SKILL_WIELDER_IMAGER.md) when image staging, Dockerfiles, registry tags, or committed-state provenance are in scope.
- Use [Provisioning Guidelines](SKILL_PROVISIONING_GUIDELINES.md) when the service creates cloud resources, IAM, topics, service accounts, or Terraform-managed assets.
- Use [Security Guidelines](SKILL_SECURITY_GUIDELINES.md) when the service touches secrets, OAuth, IAM, RBAC, cross-cloud credentials, or runtime identities.
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
