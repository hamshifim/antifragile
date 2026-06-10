---
name: Wielder Workflow Validation Guidelines
description: Meta-level guidance for treating Wielder workflows as configurable integration, system, load, and production execution surfaces across all modes of a distributed system.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Wielder Workflow Validation Guidelines

Wielder workflows are a primary validation surface and a testing framework for distributed systems.

This is a Wielder-specific expression of a broader distributed-systems doctrine: the same orchestrated workflow family can act across many modes of operation without becoming a different species of script each time.

One of the main payoffs is delta reduction. The closer the workstation path is to the build, deploy, and DAG-execution path, the smaller the interpretive gap between local development and CI/CD reality.

Wielder is especially strong when used to assemble ephemeral super-clusters: configurable, multi-surface, multi-tier distributed environments that can be created, exercised, observed, and torn down as one workflow family. In development, testing, QA, and staging, that ephemerality is a feature, not a compromise.

## Core Principle

A workflow entrypoint that resolves topology, builds images, provisions dependencies, deploys services, bridges local access, and runs the target workload should be treated as a unified validation harness.

The same workflow shape can operate as:
- a unit test
- an integration test
- a system test
- a load test
- a production execution path

The same workflow family can also function as a testing framework by coordinating:
- publishers and traffic generators
- monitors and observers
- consumers and workers
- provisioning and teardown steps

The difference is not the existence of a different script. The difference is the resolved configuration across:
- `ecosystem`
- `surface`
- `stage_tier`
- workload scale
- data volume
- retention and teardown policy

In Wielder, those are the local axes of modulation. In the more general distributed-systems sense, the same principle extends across all operational modes that alter topology, scale, durability, safety posture, or execution intensity.

The same workflow can be epigenetically phenotyped by configuration across that spectrum rather than reauthored as a separate script for each test label.

The same family should also support mix-and-match deployment across multi-tiered DAGs, where different tiers, services, and transports are recombined by configuration rather than by inventing a separate workflow for every permutation.

Within that doctrine:
- `app` is the enduring managed unit in configuration.
- `deploy` is an operational expression against an app.
- `workflow` is the orchestrated harness that coordinates multiple apps, dependencies, actors, and teardown behavior across an ephemeral or persistent distributed environment.

## 1. The Workflow as Test Harness

- **Rule:** A workflow `delete -> apply` cycle is a first-class validation surface, not a secondary convenience wrapper.
- **Rule:** If a workflow provisions the real dependencies and runs the real workload path, a successful end-to-end run is already a high-value integration and system proof.
- **Rule:** Down-scaled runs in local or ephemeral ecosystems are not a different category of software truth. They are reduced-scope modulations of the same validation harness.
- **Rule:** Strong workflow unification reduces the delta from workstation coding, through image build, through CI/CD, into configured DAG execution.
- **Rule:** A workflow can act as a testing framework when it coordinates active test actors such as publishers and passive or semi-passive observers such as monitors against the same configured environment.
- **Rule:** An ephemeral super-cluster should be read as a temporary real system slice assembled by the workflow, not as a toy stand-in for the real system.

## 2. The Workflow as a Scale-Modulated Instrument

- **Rule:** A workflow may express integration, system, load, or production operation by changing configuration rather than changing the fundamental orchestrating script.
- **Rule:** `stage_tier` should carry maturity and environmental intent such as `dev`, `qa`, `stage`, or `prod`.
- **Rule:** `ecosystem` and `surface` should carry the execution topology and physical deployment shape.
- **Rule:** Load intensity, batch breadth, retention, replication, and destructive teardown behavior should be modulated through configuration, not by inventing parallel workflow entrypoints for each testing label.
- **Rule:** The same doctrine generalizes beyond Wielder-specific axes. In any distributed system, workflow role should be read as a modulation across modes rather than as a justification for proliferating separate scripts for integration, system, load, and production.

## 3. Image-Bearing Determinism

- **Rule:** When a workflow `apply` bakes images, it should be treated as a committed-state operation keyed by one final committed super-repo SHA.
- **Rule:** If a deployment depends on changes inside a submodule, the correct sequence is: commit the submodule changes, commit the super-repo pointer update, then build and push the image, then deploy.
- **Rule:** The deployment identity is the final committed super-repo SHA, because that SHA captures the tracked submodule pointers that define the image content. Build, push, and deploy must all resolve against that same SHA.
- **Rule:** If a repository participates only as thin deploy wiring and is not part of the baked image, its local diff should not be mistaken for image truth.
- **Rule:** `imagePullPolicy: Always` is the correct default for workflow-managed validation deployments when the objective is to exercise the exact image that was just built and pushed.
- **Rule:** Rollback is achieved through super-repo commit history. A single supermodule commit hash acts as a version boundary because it captures the tracked submodule pointers that define the rebuildable distributed state.

## 4. Stage Tiers and Ecosystems Are Validation Axes

- **Rule:** The same workflow should be able to move cleanly across stage tiers and ecosystems without changing its architectural role.
- **Rule:** A local or k3d workflow run in `qa` can still be a valid system test if it provisions the real service graph and exercises the real workload path.
- **Rule:** A cloud-bound workflow run in `prod` is not a fundamentally different orchestration species. It is the same workflow family operating at a different topological and operational scale.
- **Rule:** Avoid framing local workflows as "fake tests" and cloud workflows as "real tests." In Wielder, they are the same harness modulated across different surfaces and operational bounds.
- **Rule:** Wielder `test` mode is an overlay selector, not an action selector. `-t` should load the ecosystem fixture from `conf/test/<domain>/<ecosystem>/test.conf`; `-w` still independently chooses `plan`, `apply`, `delete`, or another action.
- **Rule:** Ecosystem test fixtures should override developer and ephemeral context for fixture-specific DAGs, batch identity, scale, validation toggles, and expected inputs. They should not smuggle topology modes or actions that belong to the Wielder command surface.

## 5. Delete Then Apply

- **Rule:** If the validation goal is to prove reproducibility and full-environment correctness, prefer `delete -> apply` over incremental patching of a live environment.
- **Rule:** Deletion is part of the proof because it demonstrates that the workflow can reconstruct the environment from its committed source of truth.
- **Rule:** Incremental hot-patching may still be useful for debugging, but it should not be confused with the stronger proof delivered by a clean teardown and rebuild cycle.

## 6. Practical Reading of Outcomes

- **Rule:** A workflow failure after image build but before runtime validation is still a useful systems result. It localizes the defect to provisioning, bridging, config propagation, or runtime topology.
- **Rule:** A workflow that reaches the live foreground workload and holds steady has passed more than a unit or narrow integration check. It has validated the configured environment as a living system slice.
- **Rule:** The resulting local diff after a successful run is a precise record of the deployment and image delta that was actually exercised.
- **Rule:** A live system test may be used as an engineering workbench when the running workflow exposes a real boundary defect. Make the smallest coherent source/config change, re-enter through the Wielder entrypoint, and let the system test validate or reject the change.
- **Rule:** Learning during a system test is not a deviation from antifragility. It is the mechanism by which the workflow, operator, and codebase evolve under real pressure. Durable lessons should be promoted into reusable skills, config contracts, workflow code, or documentation.

## 7. Delta Reduction as a Design Goal

- **Rule:** Strongly prefer workflow designs that reduce the delta between workstation development, image construction, CI/CD execution, and configured DAG runtime.
- **Rule:** When the same workflow family carries code from local edit, to image bake, to deploy, to live DAG execution, fewer environment-specific gaps remain available for bugs to hide in.
- **Rule:** If a proposed shortcut introduces a special local-only path that bypasses the real build or deploy chain, treat that as a delta increase and justify it explicitly.
- **Rule:** One of the direct benefits of this reduction is a lower probability of "it worked on my computer" bugs, because the workstation path is forced to converge earlier with the real build, deploy, and runtime path.
