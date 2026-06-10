# RND UI Manifesto

Research and development UI is not a place to run science. It is a thin, authenticated control plane for wielding versioned remote systems.

## Core Claim

A weak client should be able to launch, inspect, interact with, and terminate a production-like environment without becoming part of the workload.

The browser submits intent, shows status, streams interaction, and requests teardown. Heavy computation, rendering, storage, orchestration, and cleanup run remotely through Wielder-managed infrastructure.

## Wielder First

Wielder entrypoints are already state-machine steps.

Hosted workflow services such as AWS Step Functions may be useful durable expressions of that state machine, but they must not replace the conceptual model. The canonical workflow remains:

1. Resolve configuration.
2. Pin committed code and submodule state.
3. Apply the selected Wielder entrypoint.
4. Observe progress and emitted state.
5. Delete through the matching Wielder entrypoint.

Hosted orchestration should wrap this lifecycle, not reinterpret it.

## Launch Identity

Launch identity is the exact committed version, not a moving branch name.

A branch such as `production-launching` is a policy gate and source lane. The executable identity is the resolved full commit SHA plus captured submodule SHAs plus the resolved configuration artifact for that run.

Every launch must persist:

- run id
- owner
- branch gate
- full commit SHA
- resolved configuration artifact
- launch parameters
- TTL
- status
- cleanup state

## Configuration Is The Form

The UI should not invent a parallel parameter model.

User-facing launch forms are a human interface for generating a transient HOCON context. That transient context should be resolved by the canonical accessor, saved per run, and stored under the run/version lineage.

The durable object is not "form input"; it is the resolved configuration phenotype that Wielder actually ran.

## Ephemeral Superclusters Are Jobs

An ephemeral Kubernetes, Spark, service, data, or scientific cluster is conceptually a job.

It may contain Kubernetes services, Spark jobs, ingestion pipelines, Kafka topics, notebooks, render workers, analysis stages, or domain-specific compute, but lifecycle-wise it behaves like a remote Wielder job:

- submit
- provision/apply
- run
- observe
- complete/fail/timeout
- delete

The UI must make this lifecycle legible without pretending the client owns the work.

## Weak Client Rule

Weak clients are first-class.

The browser must not require local GPUs, powerful CPUs, WebGPU support, local molecular rendering, local repository checkout, local Terraform, local Spark, or local scientific execution.

The browser may handle:

- login
- launch forms
- status views
- logs and links
- lightweight tables and charts
- terminate buttons
- streamed interactive viewport controls

The browser must not handle expensive compute.

## Remote Visualization

Heavy visualization belongs on remote GPU infrastructure.

The UI should expose a stable viewport abstraction while the backend chooses the render transport:

- `remote-desktop` for rapid internal prototyping
- `remote-webrtc` for embedded production pixel streaming

The browser receives frames or a video stream and sends camera, selection, mouse, keyboard, and control events back to the remote render session.

Render sessions are not special exceptions. They are run-bound ephemeral resources with the same owner, TTL, auth, status, tags, and delete lifecycle as the rest of the launched environment.

## Cleanup Is A Primary Feature

Creation without deletion is not an RND UI feature.

Every resource created by a launcher must be traceable by tags or equivalent metadata:

- `RunId`
- `Owner`
- `CreatedBy`
- `TTL`
- `Branch`
- `Commit`

The normal exit path is the matching Wielder `delete` action. Grave errors, user termination, timeout, browser disconnect, and orchestration failure must all route toward the same idempotent delete path.

A janitor may exist, but it is a backstop, not the main design.

## Auth And Control

Authentication is the front door; backend authorization is the lock.

Backend authorization must validate the user on every launch, terminate, render, and inspection action. UI session expiry alone is not enough. Expensive remote control actions must fail closed after backend session expiry.

## First Concrete Apps

The first RND UI apps should wrap existing wieldable backends rather than recoding domain behavior into a web application.

A domain prototype may be useful WET source for interaction expectations, scoring vocabulary, viewport affordances, and file-level ergonomics. It is not automatically the target architecture.

## Design Tests

Before adding an RND UI feature, ask:

1. Does this keep the browser thin?
2. Does heavy work run remotely?
3. Is launch identity pinned to committed code?
4. Is user input translated into canonical HOCON instead of a parallel config path?
5. Is the resolved configuration saved with the run?
6. Is `delete` already designed for everything this feature can create?
7. Can a weak client use it?
8. Can a human inspect status without SSH?
9. Can an orphaned run be cleaned by run id?
10. Does this compose with Wielder entrypoints instead of bypassing them?

If the answer to any of these is no, the feature is not ready for the RND UI foundation.
