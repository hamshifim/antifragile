---
name: Wielder Scripting & Evaluation Skills
description: Core architectural patterns for writing `Wielder` orchestration and evaluation scripts, focusing on configuration boundaries, dependency inheritance, and physical formatting conventions.
---

[Use Wield Documentation](SKILL_WIELD_DOCUMENTATION.md) when script entrypoints
need durable operator docs and test handoffs in a project `wield_docs/` tree.
[Use Code Scope Extraction](../utility_skills/SKILL_CODE_SCOPE_EXTRACTION.md) before promoting
project-local script or service helpers into Wielder.
[Read Strict FS Agnosticism](../data_skills/SKILL_STRICT_FS_AGNOSTICISM.md) before changing scripts that touch buckets, object keys, table sinks, artifact roots, URIs, Bucketeer, Spark, or provider storage.
[Read Unique Name Identity](../architecture_skills/SKILL_UNIQUE_NAME_IDENTITY.md) before changing scripts that construct, propagate, log, or consume `unique_name`, image tags, Spark/Python artifact versions, resolved-conf roots, Terraform state names, or Kubernetes resource names.

# Wielder Script Architectural Patterns

When writing or modifying `Wielder` orchestration scripts (e.g., K8s deployment wrappers, `bootstrap.py` sequences, or local pipeline evaluators), we generally adhere to the following `Wielder-Antifragile` guidelines to help them scale gracefully across environments. 

## 1. Avoid Reinventing the Wheel
`Wielder` exists as a specialized ecosystem library to handle orchestration heavy lifting. As a rule of thumb, scripts work best when they act as thin, declarative wrappers linking `Wielder` primitives to execution targets. 

If you find yourself writing custom logic to sync directories, parse YAML text, or read `.env` configuration files manually, it usually implies there's a better path:
* Look for established implementations natively within `Wielder` utility modules (`wielder.util`, `wielder.wield.project`, etc.). 
* Depend natively on built-in tools like `KubectlBucketeer`, native PyHocon parsers (`get_app_conf()`), and native deployment classes.

## 2. Configuration-Driven Filesystem Operations
Wielder orchestration scripts shy away from hardcoded directory paths, deeply nested string concatenations, or magic constants pointing to files.

* The preferred way a script relates to the virtual or physical file system is through the centralized Configuration (PyHocon `.conf` files).
* Utilize `get_app_conf()` or native Wielder extraction patterns to determine the contextual `staging_root`, `bucket_path`, or `target_database` dynamically.
* Treat Bucketeer, Spark, catalog, and provider URIs as opaque handles. Do not convert `file://`, `s3://`, `gs://`, or bare object URIs into local `Path` objects, derive parent directories, or print local `serve_command` hints from a generic script. Log `bucket`, `object_key`, table/catalog id, and `object_uri` separately so the same script remains honest on local, remote desktop, S3, and GCS ecosystems.
* Factory or accessor patterns do not forgive filesystem leakage. If a helper secretly assumes local buckets, local mounted roots, or POSIX path behavior, its name and config contract must say that it is local-only; otherwise repair the generic surface to stay key/URI-based.
* When local development context matters, scripts should rely on the active central `context_conf/<name>/developer.conf` pack rather than repo-local `conf/developer/` overrides or ad hoc CLI flags.
* For app-local examples, keep tracked packs under `conf/context_conf_examples/<name>/` and keep `conf/context_conf/<name>/` ignored. The human and agent workflow is always: copy an example pack into `conf/context_conf/`, then edit the copied local pack.

## 2.1 Thin Script, Single Loader
Operational scripts become fragile when they grow a second understanding of configuration structure.

* Strongly suggest resolving application state through the canonical accessor that matches the target domain, rather than re-merging `project.conf`, `ecosystem_manifest.conf`, and `stage_tier` files by hand.
* Strongly suggest keeping the script thin enough that it owns execution sequencing, not config reconstruction.
* Strongly suggest avoiding local parser inventions that partially duplicate Wielder behavior, because those forks tend to drift exactly when ecosystem naming or family extraction changes.
* Non-containerized Wielder scripts and integration tests must still be driven by resolved Wielder configuration, not ad hoc environment variables. Operator-local enable flags, timeouts, endpoints, file names, and mutation toggles belong in `context_conf/<name>/developer.conf` or the owning app config. Environment variables are acceptable as container runtime transport when the configured orchestrator materializes them, but they should not become a second human-facing control plane.
* Runtime identity belongs in resolved config. Scripts must consume `conf.unique_name` and related configured image/artifact identities; they must not reconstruct `unique_name` from flags, environment variables, current directories, or local usernames.
* When a script must orchestrate a child repo, strongly suggest loading that child repo through the child repo's own canonical accessor rather than inventing a second local reader.
* Strongly suggest treating such cross-repo access as explicit dependency wiring, not as a generic framework feature. The script should read foreign owned fields, not absorb the foreign app's whole config identity.
* If the bridge logic is only a few lines, keep it WET and local on purpose. A garden of tiny explicit bridges is healthier than a premature generic loader that hides ownership.
* When incorporating an app from another repo, use [App Incorporation](../utility_skills/SKILL_APP_INCORPORATION.md) to decide what belongs in the project, functional ecosystem, concrete ecosystem, app baseline, and test overlay before writing the entrypoint.

### 2.1.0 Project-Level App Config Entrypoint

Each Wielder-managed project or submodule should expose a local canonical config
accessor, following the project-local accessor pattern:

```python
from <project>_wielder.core.configurer import get_app_conf

APP_NAME = "<app-or/nested/app>"

def main() -> None:
    conf = get_app_conf(APP_NAME)
    ...
```

Leaf scripts should import the project/submodule accessor instead of calling
`wielder.wield.wield_conf.get_wield_app_conf(...)` directly. The project accessor
owns `project_root`, `conf_root`, `project_name`, runtime defaults, project-local
ontology injections, and any sanctioned compatibility options such as `mute`,
`module_paths`, `app_conf_root`, and `resolve`.

Local operator verbs may have a small positional vocabulary, but Wielder action
selection should still enter config before execution, usually through
`cli_overrides={"action": WieldAction.INIT}` or the shared
`build_cli_overrides(...)` helper. Avoid resolving config and then overriding
`action` as a separate Python side channel.

### 2.1.0.1 Runtime-Polymorphic App Shape

Some apps have one stable domain contract but several valid runtime phenotypes.
MSA/MMSeqs is a representative shape: the service can run inside Kubernetes or
on the workstation, use inner or outer Kafka, select CPU or GPU profiles, and
read the same bucket keys through different mounted roots.

Use this app shape when the polymorphism is real:

* Keep the app entrypoint thin: parse Wielder modes, call the project-local
  `get_app_conf(APP_NAME)`, validate the resolved app contract, then delegate to
  deploy/image/runtime helpers.
* Put the domain contract in the functional ecosystem or app namespace that owns
  it: topics, consumer groups, result keys, request payload profiles, model/tool
  parameters, database contracts, and output semantics.
* Put physical facts in thin wrapper ecosystems or context packs: kube context,
  service hostnames, bind/access ports, local bucket roots, mounted bucket roots,
  registry authority, scheduling, and CPU/GPU capacity expression.
* Let runtime code branch only on resolved, typed config leaves such as
  `service_target`, `kafka.endpoint`, `use_gpu`, or `bucket_mount.root`. Do not
  branch by rereading HOCON files, probing the current machine to infer intent,
  or adding bespoke flags.
* If a runtime needs a payload larger than convenient scalar config, stage it as
  a config-selected artifact such as a ConfigMap file or generated ephemeral
  context pack. Do not pass domain payloads through environment variables or
  hidden CLI strings.
* For tests, put reduced databases, tiny sequences, fast polling, and fixture
  payloads under `-t` overlays. The same endpoint should still exercise the real
  service boundary, Kafka topics, bucket paths, and gRPC/API surface.

### 2.1.1 Thin Ecosystem Wrapper Discipline

Scripts should treat local, hybrid, and cloud expressions as phenotypes of the same configured app family whenever possible.

* Strongly suggest designing local and hybrid Wielder entrypoints as thin wrappers over the full ecosystem they are exercising. For example, a local webapp that drives AWS EKS, Kafka, S3, and EMR should resolve an AWS-hybrid ecosystem that includes the full AWS runtime ecosystem and overrides only the local API/web and bridge facts.
* Strongly suggest avoiding scripts that reconstruct a partial version of a remote ecosystem by hand. If the remote runtime already owns topics, buckets, readiness, or workflow target facts, the local wrapper should inherit those facts through config.
* Strongly suggest keeping port-forward setup, local API bind addresses, local Python executable paths, and workstation credential behavior in the concrete hybrid ecosystem or its context pack. Do not smuggle these through bespoke CLI flags or subprocess environment patches.
* Strongly suggest using Wielder entrypoints to operate the hybrid phenotype exactly as the cloud phenotype would be operated, with only the source surface changed.

## 2.2 Local Script Actions vs Wielder Modes
Some scripts need a small local command vocabulary in addition to Wielder topology.

* CLI is for modulation; config is for configuration. A script needs a specific, defensible reason to add a new CLI option. Prefer Wielder's existing action and topology flags, plus HOCON overrides in the active context pack, over bespoke flags for polling, targets, file names, feature toggles, schedules, identities, or test behavior.
* Antipattern: do not create gnostic CLIs or environment-variable side channels that smuggle operation-specific knowledge around the resolver. If a script needs operator intent such as a desired branch, target dataset, runtime profile, approval window, or other durable/replayable choice, put it in resolved HOCON, usually `context_conf/<name>/developer.conf` for local transient intent. If the required config leaf is absent, the script should fail closed with an explicit message naming the missing key and the expected context-pack location.
* Antipattern: do not wrap or hand-forward bundles of Wielder CLI overrides merely to make one entrypoint call another. Let the downstream canonical accessor resolve its own lifecycle fields. If a topology switch is truly required, pass only the narrow required dimension and prefer repairing the ecosystem/app contract over building an override ferry.
* See [`Known Codex Unwanted Tendencies`](../../../../docs/antipatterns/known_codex_unwanted_tendancies_antipattern.md) for the recurring agent-side smells: gnostic CLI, environment-variable side channel, and CLI override wrapping.
* Wielder mode values belong on the human-facing command surface or in an explicitly named operational profile. Do not rely on `context_conf/default_conf/developer.conf` to silently provide `ecosystem`, `stage_tier`, `security`, `destroy`, `canary`, `context_conf`, or `action`; that turns a neutral context pack into a hidden CLI override.
* Environment variables are runtime transport, not the operator control plane. Prefer resolved HOCON config, `context_conf/<name>/developer.conf`, `secrets.conf`, or staged runtime config artifacts for durable choices. Use environment variables mainly where a platform, container, MCP server, or third-party SDK requires them as process input, and bridge them from resolved config or secrets at the boundary.
* Whenever a skill, script, wrapper, MCP bridge, or task workflow introduces a new operator-controlled value, first ask whether it belongs in config. Add ad hoc CLI flags or direct environment-variable instructions only when the value is truly ephemeral, process-native, or outside Wielder's configuration reach.
* `apply` is the default Wielder execution idiom for active entrypoints. Reserve `run` for explicitly starting already-provisioned dormant jobs, such as Cloud Run Jobs or other scheduled/event-driven workloads that normally sit idle. If an active entrypoint exists mainly to trigger dormant jobs, it may support both `apply` and `run`, but operator docs should prefer `apply` for the entrypoint and use `run` only at the dormant-job boundary.
* Strongly suggest keeping those local actions narrow and positional while leaving ecosystem and stage resolution to the normal Wielder/config accessor path.
* Strongly suggest defaulting direct CLI execution to the dominant operational behavior when one obviously exists, rather than multiplexing many loosely maintained modes through one argv surface.
* Strongly suggest separating internal programmatic action hooks from human-facing shell invocation if a script starts accumulating too many modes.

### 2.2.1 Test Mode Endpoint Discipline

The Wielder `-t/--test` mode makes test scenarios available through the same
endpoint that plans, applies, deletes, runs, or monitors the normal workload.
See [Architectural Testing & Live QA Execution Protocols](../test_skills/SKILL_TEST_GUIDELINES.md)
for the fixture philosophy and [Wielder PyHocon Configuration Guidelines](../config_skills/SKILL_CONFIGURATION_GUIDELINES.md)
for overlay precedence.

* A Wielder endpoint that uses `get_ecosystem_parser()` should pass `args.test`
  into `build_cli_overrides(...)` with the other mode dimensions. Do not add a
  sibling `--system-test`, `--test-fixture`, or environment-variable switch when
  the scenario can be expressed by the configured test overlay.
* A parent endpoint that invokes child Wielder apps should propagate the
  resolved test mode through `build_cli_overrides_from_conf(conf, action=...)`.
  This lets every child endpoint see the same scenario envelope without a
  bespoke override ferry.
* Test behavior belongs in resolved HOCON, usually
  `conf/test/<domain>/<ecosystem>/test.conf` for system scenarios and
  `conf/apps/<app>/test.conf` for app-local fixture deltas. Scripts should read
  typed test subtrees such as `deploy_steps`, `delete_steps`, `validation`,
  `foreign_apps`, `cleanup`, `capacity_profiles`, or scenario DAG lists from
  `conf`; they should not synthesize those decisions in Python.
* Workflow child-operation inventories that are reusable across modes should
  live in an app-owned `wield_steps.conf` included by `app.conf`. Mode overlays
  such as `test.conf` should select or modulate named wield step sets while the
  script continues to consume resolved `deploy_steps`, `delete_steps`, or an
  equivalently typed subtree through the canonical accessor.
* App defaults should remain best-practice or production-grade for the normal
  contract. Scripts should not quietly downgrade model loops, sample counts,
  batch sizes, polling windows, data limits, or cleanup behavior to make an
  endpoint cheap. Minimal viability is a test/developer overlay concern: put
  the reduced values in `-t` HOCON or an explicit transient context pack and
  have the script consume the resolved profile by strict config access.
* Antipattern: do not replace real upstream work with a stale summary,
  hand-authored fixture, synthetic payload, or mock output merely to avoid a
  slow run. If a process or dataset is too heavy for the operator's local
  machine, the exception must be explicit: ask for user consent, express the
  substitute in the `-t` test overlay or owning config, label it as synthetic or
  fixture-backed in plan/apply logs, and keep the real entrypoint contract
  intact. Silent mocks and stale summaries are not acceptable proof surfaces.
* `-t/--test` does not select action. A test endpoint should still branch on
  `WieldAction(conf.action)`, and the operator should still use `-w plan`,
  `-w apply`, `-w delete`, `-w run`, or `-w monitor` to choose lifecycle.
* Handoff commands for system scenarios should show test mode as an explicit
  Wielder mode on the same one-line endpoint command, for example:
  ```bash
  /path/to/<endpoint>.py -es <ecosystem> -st dev -se org -dl standard -cn standard -cc default_conf -t -w plan
  ```

## 2.3 Granular Apply/Delete Control
Deployment workflows frequently need asymmetric behavior between `apply` and `delete`. A step that is desirable during bring-up is often dangerous or wasteful during teardown.

* Strongly suggest keeping `apply`/bring-up controls in a dedicated `deploy_steps` block and `delete`/teardown controls in a separate `delete_steps` block rather than reusing one boolean family for both directions.
* Strongly suggest making delete behavior explicitly voidable at the config layer. If a workflow should preserve third-party services, topics, port-forwards, or infrastructure during delete, that decision should be expressed in `delete_steps`, not hardcoded in the script.
* Strongly suggest letting the script branch on `WieldAction` and then read the matching config family, rather than treating `delete` as a blind inversion of `apply`.
* When a deploy script orchestrates several resources, strongly suggest exposing delete granularity per resource class such as third-party services, topics, local port-forwards, workload services, and infrastructure.

## 2.4 Long-Running Operator Handoff
Some Wielder actions are expected to run for minutes or hours, especially bucket mirrors, storage syncs, image builds, Terraform applies, large data ingestion jobs, and cloud workflow executions.

[Use Wielder Handoff & Operator Command Reporting](SKILL_WIELDER_HANDOFF.md) for operator-facing command formatting, validation reporting, and context-recovery notes.

* Agents should run short validation actions themselves, such as `show`, `plan`, `probe`, linting, focused tests, and command construction checks.
* Agents should not start long-running `apply`, sync, mirror, clone, build, or migration jobs unless the operator explicitly asks the agent to run them and wait.
* For long-running jobs, provide the exact absolute one-line command for the operator's terminal, including the repository-root-safe script path and required Wielder modes. Do not require a preceding `cd`.
* If an agent wants to avoid a long apply by using a mock, precomputed summary,
  or synthetic fixture, it must stop and ask first. Approved substitutes must
  run only through `-t`, be config-owned, and print clear logs identifying the
  substitute source and why the real upstream stage was not run.
* Before handing off, verify that config resolves and that the command shape is correct with the lightest available action (`show`, `plan`, or `probe`).
* After handoff, treat pasted terminal output as the continuation point. Diagnose failures from that output and patch the smallest relevant source/config boundary.
* If an agent accidentally starts a long-running local process and it is not needed for immediate inspection, stop it cleanly when safe and give the operator the command to rerun.

## 2.5 Provision Runtime Tooling From Config
When a Wielder script depends on a backend CLI, the script should remove manual setup burden where it can do so safely.

* Prefer generating or ensuring local CLI configuration from the resolved Wielder config before asking the operator to enter an interactive setup flow.
* Keep generated local configuration in developer-local paths, usually under `~/.config/<tool>/`, and point to that path from `context_conf/<name>/developer.conf`.
* For clone backend configuration, prefer a generic WCloner-side config factory such as `WCloner.configure_wclone(...)` that materializes all configured remotes from HOCON before planning or execution.
* Do not version secrets, OAuth tokens, access keys, or one-off migration coordinates. Version only the reusable config shape and examples.
* If a CLI can consume short-lived credentials through environment variables, inject them at execution time rather than materializing tokens into versioned config.
* For GCP-hosted execution, prefer service-account ADC or metadata credentials with backend `env_auth = true`; do not design hosted jobs around interactive `gcloud` OAuth or operator-local tokens.
* For local GCP-dev execution, short-lived `gcloud auth print-access-token` injection is acceptable when it avoids writing tokens into WClone backend config.
* For hosted clone daemons, store external provider credentials in the cloud-native secret manager for that runtime and bind access through the daemon service account. On GCP this means Secret Manager secrets plus resource-scoped IAM for the WClone daemon service account.
* Terraform may create secret containers and IAM bindings, but real secret payload versions should be injected out of band unless the repository has an explicit encrypted secret-state policy.
* Prefer provider-native federation over static cross-cloud keys when the target provider supports it. Static keys in a secret manager are a transitional mechanism, not the desired end state.
* Preserve provider surfaces through factories and accessors. A script should ask a Bucketeer/WCloner-style surface to ensure a bucket or destination, not branch on concrete provider names except at the factory registry boundary.
* Add new reusable capabilities to the Wieldable Functionalities catalog when they become stable operator-facing patterns.

### 2.5.1 No Dirty Source Overlays Into Runtime Staging

With prejudice: copying dirty local module source into a staged Terraform,
image, artifact, or hosted-runtime execution tree is a Wieldering antipattern.
It is a seductive dev-flow shortcut and a provenance trap.

Wielder staging sandboxes may isolate execution from the live checkout, but they
must not smuggle uncommitted local edits into cloud-mutating or runtime-bearing
surfaces. Terraform, image contexts, Spark artifacts, provisioned scripts, and
other distributed/baked inputs are operational truth. They must be traceable to
the committed submodule revision and final super-repo SHA selected by the
resolved configuration.

Rules:

* Do not refresh staged Terraform modules from the dirty developer checkout
  immediately before `plan`, `apply`, `delete`, or `init`.
* Do not copy uncommitted local code into image/build/runtime staging as a
  convenience workaround.
* Deterministic non-source payloads may be copied into an image or staging tree
  when they are selected by resolved config, immutable for the selected version,
  and not source code, not execution config, and not a hidden operator decision.
  Examples include a versioned model weight file, a pinned public reference
  bundle, or a generated asset whose content hash is recorded in the artifact
  manifest. This exception is not a loophole for Python, Terraform, shell,
  HOCON, YAML, notebooks, or runtime scripts.
* If a staged module is missing or stale, fail early and tell the operator to
  review, commit the owning submodule, update the super-repo pointer, and rerun
  the Wielder command from that committed source of truth.
* A read-only local inspection command may print local dirty status for human
  awareness, but it must not use that dirtiness as execution input.
* If a one-off emergency experiment truly requires dirty source, it must be a
  separately named throwaway command or test fixture with loud logs, no
  promotion semantics, and no claim of reproducible runtime truth.

## 2.6 Factory Surfaces and Typed Contracts
When the same abstract operation exists across multiple provider surfaces, prefer a factory/accessor pattern over scattered provider conditionals.

Use [Capability Surface Extraction](../utility_skills/SKILL_CAPABILITY_SURFACE_EXTRACTION.md)
when a script, service wrapper, GUI, API, or notebook is trying to expose the
full useful range of an existing module, model, service, or app. That skill owns
the inventory-to-operator-surface workflow; this section owns the script/factory
boundary discipline.

Use [Functional Maximization](../utility_skills/SKILL_FUNCTIONAL_MAXIMIZATION.md) before or beside
capability extraction when the script wraps a third-party model, provider API,
scientific tool, scoring tool, ingestion tool, or workflow and the immediate
question is whether the tool's full honest native envelope has been exercised,
preserved, and validated.

* Define a shared surface contract for the abstract operation, such as storage cloning, secret management, scheduling, image publishing, monitoring, or provisioning.
* Implement provider-specific classes behind a small factory or accessor boundary. Client scripts should ask for the configured surface and call the common interface.
* When wrapping a third-party API behind a generic Wielder surface, keep provider API nomenclature and full provider API shape in a dedicated `<platform>_wrapper` module/class. The wrapper should speak the platform's native ontology and expose enough platform-native capability for diagnostics, edge cases, and maximal functionality. The Wielder adapter should wrap that provider class and expose generic Wielder verbs and ontology. Both surfaces may be available to callers, but Wielder scripts should prefer the generic adapter unless they are explicitly inspecting provider-specific behavior.
* Validate incoming configuration at that boundary with strict Pydantic models or an equivalent typed contract. Missing, malformed, or unsupported config should fail loudly before any provider mutation.
* Keep provider branching inside the factory registry or provider implementation. Avoid repeated `if provider == ...` / `match surface ...` blocks in application scripts.
* Let configuration own provider choice and resource identity. Python should receive the resolved config, validate it, and execute the selected surface contract.
* Do not hide required configuration behind broad defaults when the value identifies a permission-bearing, billable, destructive, or externally visible resource.
* Optional follow-up operations should be config-gated in the script, not hardwired into the provider implementation. Prefer the simple orchestration shape:
  ```python
  if app_conf.actions.monitor_job:
      wcloner.monitor()
  ```
* When one script spawns or provisions multiple jobs, default the monitor step to `false` and let the operator enable it explicitly for the focused job or action being inspected.

## 2.7 Engine-Native IO Boundaries
Some execution engines are their own storage abstraction. Spark, Flink, DuckDB,
and similar table engines should not be forced through Bucketeer for table-scale
reads and writes.

* Use Bucketeer or a domain accessor for object-key discovery, object inventory,
  small metadata reads, and provider-neutral storage topology.
* Use the engine's configured source/sink abstraction for table or dataframe
  reads and writes.
* For local PySpark execution, prefer Wielder's existing Spark environment
  helper such as `wielder.util.spark_env.scoped_spark_env()` rather than
  mutating `JAVA_HOME`, `SPARK_HOME`, `PYSPARK_HOME`, or `PYSPARK_PYTHON`
  directly in application code.
* Put provider-specific engine options in resolved config: local filesystem
  paths, S3 options, GCS options, catalog names, credential mode, write mode,
  and output table keys/URIs.
* PySpark code artifact publication must use the shared configured artifactory
  contract, not job-local bucket constants. Keep the same bucket-relative key
  layout across local and cloud surfaces, such as
  `spark/python/<job>/<version>/...`, and let the ecosystem choose the concrete
  cloud artifactory bucket. See
  [`Epoch Artifact Governance`](../ops_skills/SKILL_EPOCH_ARTIFACT_GOVERNANCE.md) for the
  full Spark artifact storage contract.
* Keep scripts thin: they should resolve config, validate the selected engine
  surface, and call the engine adapter. They should not hand-build Spark paths,
  branch on `s3` versus `gs`, or route dataframe writes through object-storage
  helper APIs designed for file/object operations.

## 3. Standalone Invocation Formatting
Because Wielder evaluation scripts are often automated or executed directly across various shells (WSL, native Linux, CI/CD), they benefit from secure formatting to prevent common shell evaluation traps (e.g., the ImageMagick `import` bash hijacking).

To avoid silent execution hangs, a standard `*.py` script intended for execution (e.g., containing an `if __name__ == '__main__':` block) typically implements two straightforward conditions:

1. **The Unix Shebang**:
   The first line of the evaluation script designates the Python environment to bypass default Bash interpretation:
   ```python
   #!/usr/bin/env python
   ```
2. **Executable Permissions**:
   The script is granted explicit execution rights at creation:
   ```bash
   chmod +x <filename>.py
   ```

By adhering to this pattern, cross-boundary invocations like `./fetch_model_bundle.py` or `./sanity.py` are free to execute natively as Python processes without relying on the shell's fallback assumptions.

## 3.1 Service-Named Deploy and Image Entrypoints
For workload-facing Wielder scripts, prefer the Kubernetes-style filename pattern already used throughout `workflow-wielder`:

* `<service_name>_image.py` builds or ensures the image for that service.
* `<service_name>_deploy.py` deploys, plans, deletes, runs, or monitors that service.
* The service name should be the workload identity a human recognizes, such as `model_binding_monitor`, `provider_ingestion_dispatcher`, or `data_ingestion_job_runner`.
* Keep provider names out of service identity unless the service is truly provider-specific. Prefer `provider_ingestion_dispatcher` over `provider_s3_ingestion_dispatcher` when the active ecosystem can select AWS S3, GCS, local object storage, Azure, or another storage-event listener.
* Do not name operator-facing entrypoints after the helper framework unless the framework is the workload. Avoid filenames such as `<app>_wjobbard.py`, `<app>_wjobbard_image.py`, or `<app>_terraform.py` for service operations.
* Framework concepts may remain in implementation details and config blocks. The file and command surface should answer: "which service am I operating?" before "which mechanism operates it?"
