---
name: local-hybrid-dev-workflow
description: Generic Wielder workflow for fast local application or service iteration against a remote or full ecosystem substrate, using thin hybrid ecosystem overlays, local server/client/service restarts, and provider-backed services without ad hoc config or CLI side channels.
---

# Local Hybrid Dev Workflow

Use this skill when an app or service is developed locally while it talks to
services from a configured full ecosystem: Kubernetes services, object stores,
queues, Spark, EMR, databases, ingress/auth, provider APIs, or remote workers.

The local participant may be a web frontend, API server, workflow launcher,
monitor, notebook companion, CPU service, GPU inference service, or another
locally hosted runtime. The principle is the same: local code supplies one
runtime phenotype while the rest of the ecosystem remains provider-backed.

## Core Contract

- Treat the hybrid ecosystem as a thin phenotype over the full ecosystem family.
- The full ecosystem owns shared contracts: topics, buckets, service names,
  workflow targets, artifact roots, table sinks, and readiness semantics.
- The hybrid overlay owns only local physical facts: local API/client bind
  ports, proxy targets, port-forwards, workstation credential boundary, local
  source tree, local hardware/runtime capabilities, and image-skip behavior for
  services deliberately served from the workstation.
- Use the canonical app/config accessor. Do not reconstruct config layers, add
  ad hoc CLI flags, or inject local overlays in Python.

## Local Service Shapes

Common local participants include:

- frontend or client served locally while calling a local or remote API
- API/server process running locally while using remote buckets, queues, auth,
  and cluster services
- workflow publisher or monitor running locally while observing remote topics
- notebook-adjacent service that uses the same configured storage and table
  contracts as the remote runtime
- GPU or accelerator-backed runtime running on a capable workstation while the
  scheduler, queues, storage, and downstream workers stay in the remote
  ecosystem

Do not make a separate partial ecosystem for each shape. Start from the full
ecosystem family and override only the local participant and bridge facts.

## Local Iteration Loop

1. Inspect the resolved config or nearest `plan`/`show` entrypoint before
   changing behavior.
2. Run the local hybrid launcher/service from the project-owned entrypoint and
   active hybrid ecosystem/context pack.
3. Verify the local participant is serving edited source or runtime code, not a
   stale built image, wheel, model bundle, or remote deployment.
4. Verify the route, API, worker, or service behavior that changed; frontend
   HMR alone is not proof that Python, compiled, or model-runtime code reloaded.
5. Restart local processes when backend, service, model runtime, config, or
   startup state changed.
6. Only rebuild/apply remote services when the change crosses into image,
   Kubernetes, Spark, worker, or cloud runtime code.

## Restart Discipline

- Use a named local supervisor surface when one exists, such as a tmux session,
  process manager, or Wielder local run entrypoint.
- Stop the old local session and check for orphaned bind ports before restart.
- Probe the local frontend, API, worker, or service endpoint after restart.
- A changed frontend module can often appear immediately through HMR.
- A changed Python backend, local worker, or model service normally requires a
  process restart unless reload is explicitly configured.
- If an endpoint returns `404` after adding a route, suspect a stale backend
  first.

## Verification Signals

Use concrete local probes instead of relying on browser appearance:

- process/session exists and was created after the edit
- bind ports match the resolved hybrid config
- served frontend source or bundle contains the changed token
- changed API route returns the expected status shape
- local worker or service logs show the expected startup and readiness signal
- logs show no new startup traceback
- remote substrate probes still hit the configured ecosystem services

## Handoff Rules

- For local server/client/service restarts, provide the exact local restart
  command or session name.
- For image, Kubernetes, Spark, or cloud runtime changes, hand off the build and
  apply/run commands separately from the local restart command.
- Do not ask the operator to rebuild images for app code that is deliberately
  served locally in the hybrid phenotype.
- Do not ask the operator to rebuild remote runtime images for a local service
  phenotype unless the change also affects the hosted runtime.
- Do not hide local routing in shell-only environment variables. Put durable
  developer-local routing in `context_conf/<name>/developer.conf`.

## Failure Triage

- Frontend visible, API missing: stale backend or wrong proxy target.
- API route live, data missing: inspect accessor/config and storage surface.
- Local Spark/YARN warnings in a hybrid app: decide whether this path should use
  local Spark, remote Spark/EMR, or a cached/result snapshot from config.
- Local GPU/accelerator service absent or idle: inspect the hybrid overlay's
  local hardware capability, device/runtime setup, and service readiness fact
  before changing remote workers.
- Browser works locally but cloud app does not: likely image/apply gap.
- Cloud app works but local does not: likely hybrid overlay, port-forward,
  local auth, or local runtime dependency gap.
