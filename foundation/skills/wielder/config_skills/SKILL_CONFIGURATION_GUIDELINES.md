---
description: Wielder PyHocon Configuration Guidelines (Strict Architectural SOP)
---

[Read lifecycle scope guidelines](SKILL_LIFECYCLE_SCOPE_GUIDELINES.md) when deciding where a durable resource, ecosystem phenotype, app default, context override, or test fixture belongs.
[Use the resolved config guide](../../../docs/configuration/RESOLVED_CONFIG.md) when a surprising value appears at runtime.
[Read Strict FS Agnosticism](../data_skills/SKILL_STRICT_FS_AGNOSTICISM.md) when config names buckets, object keys, table keys, paths, URIs, mounts, artifact roots, or storage providers.
[Read Unique Name Identity](../architecture_skills/SKILL_UNIQUE_NAME_IDENTITY.md) when config defines `project`, `unique_name`, image tags, artifact versions, resolved-conf roots, Terraform state names, Kubernetes resource names, or context-specific runtime siloing.

# Wielder PyHocon Configuration Guidelines

The Wielder framework relies on a configuration layer whose resolution should be deterministic within a given version, while remaining evolvable under real workflow pressure. Configuration is the coded modulation layer that activates, suppresses, routes, and parameterizes system functionalities into concrete operational phenotypes. Because this layer is powerful and complexity-prone, its transient modulation mechanisms must stay explicit, bounded, and inspectable so the system can evolve toward antifragility without drifting into hidden configuration paths.

Wielder configuration names enduring managed units as `apps`. A deployment is an operational expression of an app, and a workflow is the orchestrated harness that coordinates many apps, dependencies, and observers. The configuration tree should preserve that distinction clearly.

---

## Part 1: The Resolving Configuration Ecology

To support a distributed super-repo architecture where applications concurrently bridge different sets of bare-metal development workstations, remote K8s clusters, and localized shadow deployments, Wielder enforces a hyper-granular, predictable resolution hierarchy.

### The Actual Resolution Order

The Wielder resolver has two passes: a project/topography pass, then an app pass. List order below is lowest priority to highest priority.

Project/topography pass (`get_wield_project_conf()`):

1. generated runtime defaults
2. `conf/project.conf`
3. super-repo `conf/super_module.conf`, when present
4. `conf/canary/<canary>/canary.conf`
5. `conf/ecosystem/**/<ecosystem>/ecosystem_manifest.conf`
6. `conf/destroy/<destroy>/destroy.conf`
7. `conf/stage_tier/<stage_tier>/tier.conf`
8. `conf/security/<security>/security.conf`
9. context pack overlays from `conf/context_conf/<context_conf>/` and super-repo `context_conf/<context_conf>/`, including `secrets.conf`, `agents.conf`, generated transient `ephemeral.conf`, and operator-local `developer.conf`
10. `conf/test/**/<ecosystem>/test.conf`, only when `test` is enabled
11. CLI overrides
12. loader-injected path metadata such as `conf_root`, `context_conf_root`, `developer_conf_path`, `ephemeral_conf_path`, and `test_conf_path`

Routing note: `ecosystem`, `stage_tier`, `security`, `destroy`, `canary`, `context_conf`, and `test` are selected from CLI first, then already-loaded context packs, then project defaults. The selected ecosystem manifest is loaded after this routing decision.

App pass (`get_wield_app_conf()`):

1. `conf/apps/<app>/app.conf`
2. `conf/apps/<app>/test.conf`, only when `test` is enabled
3. resolved project/topography config from `get_wield_project_conf(resolve=False)`
4. explicit `module_paths`, in call order, as the highest app-level overlays
5. final PyHOCON substitution resolution

Implication: app baselines declare durable app capability and empty/default contract shape. Runtime ecosystem choices, child app ecosystems, provider surfaces, and local/cloud placement are supplied by ecosystem wrappers, generated transient context, `developer.conf`, test overlays, module paths, or CLI, not by neutral `app.conf`. CLI still trumps transient and developer context.

### Ecosystem Taxonomy: Domain, Surface, Wrapper

Every ecosystem file belongs to one of three families. Treat this as a hard ownership boundary, not a naming preference:

* **Domain ecosystems** (`conf/ecosystem/domain/<domain>/...`) own reusable functional contracts: scientific/data terminology, service topic names, consumer groups, schemas, artifact contracts, table contracts, shared workflow semantics, and app/domain defaults that should remain true across local, Kind, EKS, GKE, EMR, Dataproc, or other surfaces. A domain ecosystem must not know the physical surface that will run it.
* **Surface ecosystems** (`conf/ecosystem/surface/<surface>/...`) own physical execution facts: workstation, local filesystem, Kubernetes flavor, cloud/provider surface, Spark surface, bucket roots, registry authority, kube context, service endpoints, mounts, credentials boundary, ports, and capacity/runtime facts. A surface ecosystem must not embed a domain workflow just because one domain currently uses it.
* **Aggregating wrapper ecosystems** (`conf/ecosystem/wrapper/<wrapper>/...`) are the bootable/app-runtime ecosystems normally passed to entrypoints through `-es/--ecosystem`. A wrapper includes the needed domain ecosystem(s) and surface ecosystem(s), then adds only the narrow glue that phenotypes apps for that environment.

App entrypoints should receive wrapper ecosystems, not bare domain or bare surface ecosystems, except for explicit source-style inspection. A parent Wielder may route a child app through a leaf such as `app_ecosystem_<app>`, but that leaf should name a wrapper ecosystem. If a service topic contract is reusable for multiple wrappers, keep it in the service/domain ecosystem and include it from each wrapper; if a broker endpoint changes because the service runs locally vs in cluster, keep that endpoint selection in the resolved runtime/surface/wrapper layer.

### Hybrid Ecosystems Are Per-Service Phenotypes

Hybrid wrapper ecosystems express per-service placement, not one global local-vs-kube switch. In one wrapper, a preparation service may run as a Kubernetes accelerator-backed service while a model service runs as a workstation process; in another, the model service may be in-cluster while the preparation service is local; a third service may be a Spark job or provider-managed dependency. Each service owns a resolved runtime/deploy contract such as `run_locally`, `placement`, `local_service`, `runtime_app.ecosystem`, resources, ports, and readiness, and those leaves are set by wrapper/context/test overlays rather than Python side channels.

This serves development by preserving the real ecosystem substrate while shortening the inner loop for the service under edit. The developer can run changed source locally, keep Kafka, buckets, GPU nodes, downstream services, and workflow contracts real, and test local/kube permutations without inventing alternate app behavior. `plan`, `apply`, `delete`, `run`, and `-t` should still flow through the same entrypoints and resolved HOCON; only the per-service placement leaves change.

### DAG-Shaped Wielder Apps And Materialization Gates

A `<domain>_wielder` app is a configured DAG switchboard for a bounded domain
capability. Its config owns order and mode handoff; child apps own their own
image, artifact, deploy, delete, run, validation, and evidence behavior.

Recommended config shape:

```hocon
<domain>_wielder {
  selected_steps = "default"

  wielded_apps = [
    "provision"
    "images"
    "artifacts"
    "service_a"
    "service_b"
  ]

  wielded_entrypoints {
    provision = "<domain>_wielder_provision"
    images = "<domain>_wielder_images"
    artifacts = "<domain>_wielder_artifacts"
    service_a_image = "<family>/service_a_image"
    runtime_artifacts = "<family>/runtime_artifacts"
  }

  app_modes {
    default {
      ecosystem = ${ecosystem}
      context_conf = ${context_conf}
    }
  }

  steps {
    default {
      apply = ["images", "artifacts", "provision", "service_a", "service_b"]
      delete = ["service_b", "service_a", "provision"]
      run = ["service_b"]
      provision = ["resource_workflow"]
      images = ["service_a_image"]
      artifacts = ["runtime_artifacts"]
    }
  }
}
```

- **App-owned steps:** Durable reusable DAG step sets live in app-owned config,
  normally `steps.conf` included by `app.conf`. Test, context, or developer
  overlays may select or modulate those sets; they should not be the only place
  the DAG inventory exists.
- **Verb-family order:** The main entrypoint branches by action family first.
  `plan`, `apply`, `show`, `probe`, and `init` use the `apply` family;
  `delete` and `plan-delete` use the `delete` family; `run` uses the `run`
  family. Separate class entrypoints may expose `provision`, `images`, and
  `artifacts` through the same normal Wielder action verbs.
- **Switchboard rule:** The wielder delegates to app-owned sibling entrypoints
  with Wielder mode overrides. It should not load child app configs merely to
  rewrite their deploy/artifact leaves, prepare child Spark artifacts directly,
  or carry Python state about what a child already did.
- **Step naming rule:** Step arrays should name sibling apps or typed sibling
  entrypoints. Use class names such as `images`, `artifacts`, and `provision`
  for the top-level DAG, and workload/runtime names such as `service_a_image`
  or `runtime_artifacts` for leaf entrypoints. Avoid private implementation
  chores such as `build_*`, `publish_*`, or child-specific deploy internals in
  the main DAG.
- **Mode handoff rule:** Aggregate app config may provide per-child `app_modes`
  for Wielder dimensions such as `ecosystem`, `context_conf`, `stage_tier`, and
  `test`. It should not carry child app runtime leaves directly. The child app
  must resolve its own app config and decide its own image, artifact,
  deployment, cleanup, runtime behavior, and evidence.
- **Materialization order:** Production-like DAGs should build/publish images
  and publish runtime artifacts before provisioning scarce or long-lived
  resources. This fails quickly on Docker/artifact problems rather than leaving
  idle clusters, brokers, GPUs, or cloud resources waiting for a late build
  failure.
- **Idempotency boundary:** A service, job, or deploy entrypoint called later by
  the wielder may call its own image or artifact materializer again. That helper
  should be idempotent or reuse-aware. Do not thread ad hoc `preflighted`,
  `already_built`, or similar bypass flags through the DAG.
- **Artifact rule:** Even when a wielder currently has only one shared runtime
  artifact, keep the aggregate `artifacts` class distinct from the specific
  artifact leaf. Singletons grow, and the class/leaf pattern prevents future
  reshaping from becoming a config migration.

### Ecosystem Family Core Before Phenotype Overlays

For ecosystem families and app families, the base configuration should represent the union set of shared contracts. Thin concrete ecosystems should include that core and override only the facts that make the runtime phenotype different.

* **Role of the core:** The core owns shared workflow contracts, app relationships, topics, buckets, artifacts, table contracts, logical storage keys, and default behavior that should not diverge between local, hybrid, and cloud surfaces.
* **Role of thin overlays:** Concrete ecosystems own physical expression facts: surface, kube context, provider endpoints, registry authority, port-forwarding, credential boundary, service hostnames, readiness checks, and scale/capacity phenotype.
* **Guideline:** Prefer `include file("../full_or_family_ecosystem/ecosystem_manifest.conf")` plus a small override block over copying broad configuration into a sibling ecosystem.
* **Guideline:** If a local or hybrid environment needs AWS services, make it a thin local phenotype over the full AWS ecosystem rather than a separate partial AWS imitation.
* **Guideline:** Missing values in a thin overlay usually indicate a missing core contract or a missing physical override. Fix the responsible layer instead of adding a Python fallback or side loader.

### Architectural Mandates
* **No Orphaned Variables**: If app code requires a leaf to exist in every runtime, the neutral app baseline should declare its fail-closed shape. If a leaf exists only to choose a runtime ecosystem, provider surface, local/cloud placement, or child-app handoff, it belongs above the app baseline in ecosystem, context, test, module, or CLI overlays.
* **Fail-Closed Execution**: If an override requires structural evaluation arrays (`[]`), the Baseline establishes the empty array. Masking empty configurations inside comments to "bypass PyHocon overlays" is an antipattern.
* **Mock Isolation**: Experimental boundaries ride explicitly on the Domain Modes (`stage_tier`), avoiding pollution of Tier 1.
* **Baseline vs Fixture Pressure**: Application baselines should express production-grade or best-practice behavior for the app's normal contract. Minimal pressure profiles, tiny model loops, reduced sampling, miniature batches, synthetic row counts, short polling windows, and other "just enough to prove the path" values belong in the `-t` test overlay or an explicit transient context pack, not in neutral app defaults. If a minimal profile is a real supported mode, keep its schema in the app contract, but define or activate the reduced values from the test/developer layer that needs them.
* **No Synthetic Native Success Flags**: Config must not introduce toggles such as `bypass_inference`, `fixture_result_on_bypass`, or similarly named escape hatches that make `apply` write native success markers or plausible model/tool outputs without running the configured executable, service, or model. Test overlays may reduce scale or materialize input sidecars, but they must not change "native output exists" into a fake success state. Parser fixtures belong in explicitly named fixture contracts outside the app's native run success path.
* **Shared Provider Defaults Follow Priority Order**: Shared third-party defaults used by several apps may live in a project-base provider concern included from `project.conf`, then be overridden by ecosystem, stage, context, test, or CLI layers. Apps should stay minimal by declaring which provider config key they consume, while runtime code validates the resolved provider contract strictly. Apps should not include files from `conf/ecosystem/...` directly, and should not copy shared provider leaves merely to make one runner work. Ecosystem files are phenotype overlays above app baseline, not a library of app-side imports.
* **Project-Owned Reusable Resources Follow Project Inclusion**: Durable project-level resources and data contracts belong in project-base concerns included from `project.conf`. Buckets are the canonical example: bucket names, filesystem bucket roots, and shared bucket maps are project-owned reusable resources. Ecosystems and apps consume evaluated leaves such as `buckets.*` and `buckets_root`; they must not include bucket files from another ecosystem to make a local app resolve. Apply the same ownership test to shared providers, schema registries, table catalogs, static artifact roots, and source datasets.
* **App Incorporation Cross-Reference**: When copying or reviving an app from another repo, use [App Incorporation](../utility_skills/SKILL_APP_INCORPORATION.md) before moving config. Incorporation work tends to expose misplaced project buckets, local wrapper bloat, fixture pressure in defaults, and stale legacy vocabulary.

---

## Part 2: Configuration Guidelines (SOPs)

### 1. Strict Attribute Resolution
Configuration dependencies should guide the execution toward immediate awareness if environment parameters are missing.
- **Guideline:** Avoid wrapping configuration extraction blocks in generic `try...except Exception` silencing patterns.
- **Guideline:** Prefer extracting properties natively via dot-notation (e.g., `conf.ecosystem`). Allow PyHocon to natively trigger a `ConfigMissingException` or `AttributeError` trace upon failure. Suppressing missing configurations obscures orchestration defects.
- **Guideline (Loader-Bound Derived Paths):** If the bootloader necessarily computes framework paths such as `conf_root`, `context_conf_root`, `ephemeral_conf_path`, or `developer_conf_path`, inject those concrete values into the resolved configuration exactly once and make downstream code read them by strict attribute access. Do not add narrow convenience paths to broad project/domain HOCON solely because one caller needs them, and do not recompute those paths inside application code after config resolution.
- **Guideline (Numeric-Looking String YAML Emission):** When a value must remain a string inside Kubernetes `ConfigMap.data`, plain HOCON substitution may still be emitted by `Wielder`'s `HOCONConverter` as a bare YAML scalar if the value looks numeric. The source value should still be typed as a string first. If the generated YAML still comes out unquoted, use the escaped-quote adjacency form at the HOCON leaf:
  ```hocon
  AWS_ACCOUNT_ID = "\""${aws_account_id}"\""
  ```
  This is not the default pattern for normal string composition. It is a targeted YAML-emission workaround. Always verify the staged plan file contains a quoted YAML scalar such as:
  ```yaml
  AWS_ACCOUNT_ID: "123456789012"
  ```
  before applying to Kubernetes.

### 2. The Evaluation Trump Model (Ingrained CLI Architecture)
Historically, the Wielder architecture minimized CLI bindings to protect the mathematical purity of the `.conf` file. However, structurally isolating the CLI from the PyHocon loader creates catastrophic Execution Fragmentation (the "Splintering Source of Truth") where scripts evaluate configurations differently depending on how they were executed.
- **Guideline:** The centralized Antifragile parser (`get_ecosystem_parser()`) MUST be natively ingrained into the absolute bottom of the `get_workspace_conf()` evaluation loop.
- **Guideline (The Trump Card):** The practical hierarchy is the two-pass order above: project/topography resolves first, then that tree overlays the app baseline, then explicit module paths and final substitution resolution complete the app config. CLI values remain operator trumps for Wielder modes and explicit overrides; neutral `app.conf` is not the place to pin selected ecosystems.
- **Guideline (CLI Is Modulation, Config Is Configuration):** CLI arguments should exist only for broad Wielder modulation: action/mode selection, topology dimensions, test-fixture selection, and rare operator overrides with a clear cross-script reason. Durable behavior such as polling limits, sync targets, feature toggles, file names, schedules, identities, provider choices, and test behavior belongs in HOCON. Do not add a CLI flag merely because one invocation needs a value; add or override the resolved config instead.
- **Guideline (No Leaf-Level CLI Tunnels):** Do not add generic `--config_override key=value` or service-specific endpoint flags to smuggle individual resolved leaves into an entrypoint. If a local process needs a different Kafka endpoint, binary path, mount behavior, or runtime placement, put that fact in the active ecosystem/context/developer/test/module overlay and let `get_app_conf()` resolve it normally.
- **Cross-Reference:** This native PyHocon trump execution is the foundational bridge permitting safe dry-run Sandboxing natively. See the strict Staging Sandbox bounds mapped formally in [Wielder Imager & Staging Sandboxing](../ops_skills/SKILL_WIELDER_IMAGER.md).
- **Guideline (Workflow Runtime Preference):** For distributed workflow ecosystems, CLI trumps are useful during bootstrap and planning, but runtime components should prefer staged configuration artifacts when native propagation exists. Avoid making container command-line flags the long-term operational source of truth when `context_conf/<name>/developer.conf` or another staged config artifact can be copied into the runtime surface.
- **Guideline (Included Context Artifacts):** When a runtime surface depends on local developer context, treat `developer.conf` and the files it includes (for example `workflow_runs.conf`) as one context pack. Do not stage only the top file if the runtime contract expects included ad hoc content.
- **Guideline (Ephemeral Injections):** For transient execution facts such as snapshot IDs, phase-specific scale targets, generated DAG batches, or smoke-test payloads, prefer named profiles in the owning app/ecosystem config and a small host-side helper that merges the resolved subtree into `conf.ephemeral_conf_path`. Independent app capacity should live with the independent app, while workflow-specific cleanup can compose sibling app profiles. Ephemeral injection profiles should be complete for the resources they control: a search-only workflow composition should explicitly drive downstream model runtime replicas and model runtime node groups to zero rather than merely omitting them. Treat `ephemeral.conf` as generated runtime intent, not as a second hand-maintained configuration source.
- **Guideline (Switchable Generated Payloads):** A stable `developer.conf` should carry durable context identity, topology, and the recipe needed to regenerate a transient payload. Generated runtime DAG payloads, snapshot pins, and one-off batch bindings belong in `ephemeral.conf` so they can be included by file presence or removed without editing the stable context. Do not bake generated publisher payloads back into the default context as permanent intent.
- **Guideline (Transient Batch Naming):** Manual transient batch contexts should mirror the GUI batch identity contract: short user token, default target, target tag or domain context, run slug, and autoincrement suffix. Compose these as named HOCON variables and derive `batch_name`, `batch_slug`, CSV paths, entity-set IDs, run UUID prefixes, and generated search names from that one batch name. Do not hand-type near-duplicate batch strings in several leaves.
- **Guideline (Mode Values Do Not Belong In Neutral Context):** Wielder modes such as `ecosystem`, `stage_tier`, `security`, `destroy`, `canary`, `context_conf`, `test`, and `action` should normally be supplied by the CLI or the Wielder mode layer. Do not put them in `context_conf/default_conf/developer.conf` to create hidden operator defaults. A context pack may define modes only when it is deliberately named as an operational profile, and that profile intent is visible from the context name.
- **Guideline (Live Dates Do Not Belong In Neutral Context):** Live calendar leaves such as `year`, `month`, `day`, `date`, or `timestamp` should not be hardcoded in neutral default developer contexts. Pin dates only in `-t` fixtures, replay contexts, or explicitly named historical profiles. For current lookups, compute the date at runtime from a strict config-selected policy or materialize it into ignored ephemeral config so the durable default context does not silently stale.
- **Guideline (Test Mode Is Overlay Selection, Not Action Selection):** The `-t/--test` mode only selects test overlays. It must not imply, mutate, or default `action`; `-w/--wield` remains the sole operator action selector. In test mode, load `conf/test/**/<ecosystem>/test.conf` above context and below CLI so the fixture can pin DAGs, batch identity, validation toggles, scale, expected inputs, timeout policy, capacity bundles, and apply/delete step controls while the operator still chooses `plan`, `apply`, `delete`, `run`, or `monitor`. App-local `conf/apps/<app>/test.conf` may extend the app baseline only when test mode is enabled. Do not use legacy root-level `conf/test.conf` or context packs for system-test fixtures. See [Architectural Testing & Live QA Execution Protocols](../test_skills/SKILL_TEST_GUIDELINES.md) for the test philosophy and [Wielder Scripting & Evaluation Skills](../script_skills/SKILL_WIELDER_SCRIPTS.md) for endpoint propagation.
- **Guideline (Reusable Wielder Step Sets):** When a `<domain>_wielder` owns literal child Wielder operation sequences, keep those reusable step sets in an app-owned `steps.conf` included by `app.conf`. The canonical `test.conf` overlay should select or modulate a named step set, not carry the only copy of the DAG inventory. Prefer typed leaves such as `steps.<set>.apply`, `steps.<set>.delete`, `steps.<set>.run`, `steps.<set>.provision`, `steps.<set>.images`, and `steps.<set>.artifacts` so scripts can read the resolved contract without inventing a side loader. Do not introduce parallel `deploy_steps`/`delete_steps` inventories for new DAG-shaped wielder apps.
- **Guideline (Test Mode Is Endpoint-Universal):** Any Wielder endpoint that resolves config through the canonical parser/accessor path should become test-scenarioable without adding bespoke CLI flags. Carry `test` through `build_cli_overrides(...)` and `build_cli_overrides_from_conf(...)` alongside `ecosystem`, `stage_tier`, `security`, `destroy`, `canary`, `context_conf`, and `action`. A child app invoked by a parent test endpoint should inherit the same Wielder mode envelope unless the parent intentionally switches a topology dimension through a narrow `cli_overrides` boundary.
- **Guideline (Transitional Workflow Fallbacks):** A dedicated runtime subtree such as `model_workflow.publisher_job` is cleaner than legacy workflow-owned DAG arrays, but during migration an in-cluster runtime may intentionally fall back to included workflow DAG lists from the active context pack. If that fallback is still part of the working contract, document it explicitly rather than “fixing” it by assumption.
- **Guideline (Accessor Preference):** Strongly suggest resolving application or service configuration through the canonical accessor (`get_app_conf()`, `get_service_conf()`, or peer helpers) rather than manually reconstructing HOCON layers inside leaf scripts.
- **Guideline (Project/Submodule Accessor):** Each project or submodule should wrap Wielder's generic loader with its own `core.configurer.get_app_conf(...)`, as in `starget_wielder.core.configurer`. Leaf entrypoints should import that local accessor and call `get_app_conf(APP_NAME)` so the submodule owns `project_root`, `conf_root`, `project_name`, runtime defaults, ontology injections, and sanctioned compatibility arguments (`mute`, `module_paths`, `app_conf_root`, `resolve`). Direct leaf imports of `get_wield_app_conf(...)` are a framework-boundary smell unless the file is itself implementing the project accessor.
- **Guideline (One Accessor Doctrine):** There should be one canonical accessor path for a given config contract. This is not aesthetic minimalism. It preserves one source of truth, one resolution order, one predictable failure boundary for missing variables, and one place to debug precedence. Multiple accessors for the same contract create hidden override paths, unreadable local-vs-ecosystem-vs-app precedence, and eventual configuration drift across modules.
- **Guideline (Operational Reason):** The single accessor rule exists to preserve reproducibility, debuggability, and locality of reasoning in a multi-repo, multi-agent system. If two helpers can resolve the same contract from different file sets, debugging becomes forensics instead of engineering.
- **Guideline (Cross-Repo Ownership):** In a super-repo, the orchestrating repo may need to read config owned by a child repo. That is valid, but ownership must stay explicit. Load the child repo's app conf through the child repo's own canonical accessor, then extract only the owned subtree or fields required by the orchestrator.
- **Guideline (No Mega-Conf Mixing):** Do not merge a whole foreign app tree into the local execution conf just to obtain a few image paths, ports, or service fields. Read the foreign owned contract, extract the minimal fields needed, and keep execution identity in the local caller conf.
- **Guideline (False Genericity):** Strongly suggest resisting the urge to create "generic" cross-repo config loaders inside `Wielder`. Many cross-repo relationships are domain-specific and idiosyncratic. If repetition emerges, abstract it locally in the orchestrating repo, not in the generic framework.
- **Guideline (Leaf Ownership Bridges):** When a leaf module already knows exactly which foreign app it wields, it should depend directly on that foreign app's canonical accessor rather than routing the dependency through a broader orchestrator helper. This keeps ownership honest and the bridge auditable.
- **Guideline (SDK Contract Discipline):** If a client repo appears awkward because of an existing `Wielder` SDK contract, do not silently reshape the SDK to fit the client. First decide explicitly whether the mismatch is client non-conformance or a real SDK deficiency.
- **Guideline (Sanctioned Framework Change):** If the SDK contract is genuinely suboptimal, raise it as an architectural decision with reasons, tradeoffs, and an improvement plan before changing the shared framework. Unsanctioned SDK drift contaminates every client.
- **Guideline (Client Conformance Default):** If no sanctioned framework change exists, the client repo must conform to the existing SDK contract, even when that contract is inelegant. Adjust local config names, local render logic, docs, and examples in the client rather than moving the shared layer underneath them.
- **Guideline (Native Framework Switching):** When one Wielder entrypoint needs to invoke another entrypoint against a different ecosystem, switch only the required topology dimension through `cli_overrides` and let the downstream entrypoint derive its own resolved `conf`, `action`, and other lifecycle state natively. Do not inject pre-resolved config objects or manually forward derived lifecycle fields when the framework can resolve them itself.
- **Guideline (Topology vs App Contracts):** Strongly suggest using the root/topography accessor only for project-scoped resources and early topology decisions. Do not expect late-derived app/service contracts such as `resolved_images`, resolved service image refs, or `resolved_conf` payload keys from the topography loader. Those belong to `get_app_conf()`, `get_ops_app_conf()`, or `get_service_conf()`.
- **Guideline (Root Ecosystem Purity):** Root ecosystem manifests must stay topological. Do not reference late-derived app/service variables such as `resolved_images`, `resolved_conf`, service image refs, or other app-only payloads inside `conf/ecosystem/<ecosystem>/ecosystem_manifest.conf`. Put those overrides in the app or deploy ecosystem manifest loaded through `get_app_conf()` or `get_service_conf()`.
- **Guideline (No Parallel Config Boot Paths):** Strongly suggest avoiding "side loaders" that separately read `project.conf`, individual ecosystem manifests, or stage manifests just to recreate one app tree. Those parallel config boot paths drift quickly and tend to break when ecosystem families are refactored.
- **Guideline (Notebook Contexts):** Strongly suggest giving notebooks an explicit accessor seam for mode overrides at the same boundary where Wielder normally parses topology, rather than mutating `sys.argv` or trying to inject ecosystem changes after project resolution has already happened.

#### Plan-First Config Forensics

- **Guideline:** When a Wielder deploy, image, workflow, Helm, or Terraform operation resolves a surprising value, run the nearest canonical entrypoint in `-w plan` mode before editing code. Plan mode is the first forensic instrument because it exposes the resolved config at the same boundary the real operation will use.
- **Guideline:** Compare the same field across the smallest useful chain of surfaces: root/topography config, app config, third-party or service config, rendered Terraform inputs, rendered Helm values, and the final shell command. The first divergence usually names the config ownership layer that needs repair.
- **Guideline:** If one accessor resolves a value correctly and a sibling accessor resolves a stale default, do not patch the sibling in Python first. Search for an overly broad default or misplaced override in the HOCON precedence chain.
- **Guideline:** Concrete local surface values such as `kube_context = "k3d"` belong in the local ecosystem or surface profile that owns that runtime. They do not belong in neutral `project.conf`, where they can contaminate AWS, GCP, or other remote ecosystems.
- **Antipattern:** Adding context resolvers, string normalizers, fallback rewrites, or special-case Python branches to hide a wrong resolved value is config laundering. It makes the plan look less wrong without fixing source-of-truth ownership.
- **Guideline:** Terraform, Kubernetes, and cloud-provider discovery belong in Wielder-owned provider/factory surfaces. Application repos may consume resolved contracts from those factories, but they should not embed raw boto3, kubectl, Helm, or Terraform discovery logic locally.
- **Guideline:** Patch code only after the plan-first comparison proves that the canonical accessor contract itself is deficient. When the resolved HOCON contains the wrong value, fix HOCON placement first.

#### Dogmatic Warning: Gnostic Configs Are Heresy

- **Definition:** A "gnostic config" is any hidden, private, or ad hoc configuration path that bypasses the canonical resolver and silently creates a second source of truth.
- **Forbidden Examples:** new helper-specific HOCON parsers, leaf-script `ConfigFactory.parse_file(...)` calls, one-off deploy-root loaders, silent ecosystem side loaders, or any accessor that exists only to resurrect one narrow config branch.
- **Judgment:** If a script needs configuration, it MUST come through the canonical accessor surface. Do not invent a new priesthood of loaders just because one caller is inconvenient.
- **Purgatory Rule:** If the existing accessor is too narrow, widen the accessor itself carefully. Do NOT create a parallel "temporary" reader. Temporary readers metastasize into permanent architecture rot.
- **Inquisition Rule:** Before adding any new config seam, prove that the existing canonical accessor cannot be extended cleanly. If that proof is absent, the new seam is presumptively invalid.
- **Failure Smell:** If two different code paths can resolve the same ecosystem, app, or deploy contract by reading different file sets, the design is already contaminated.
- **Failure Smell:** If a caller loads a foreign app conf and then falls back to merging it wholesale into the local conf to "make variables appear," the boundary has already dissolved.
- **Runtime Polymorphism Exception:** A polymorphic app may choose a small runtime implementation branch after canonical resolution when the branch is a real runtime phenotype, not a second loader. Example: a preparation service can resolve one domain config contract, then select in-kubernetes vs host-local service target, CPU vs accelerator workload profile, or mounted-bucket path behavior from strict config leaves. This is valid only when every selectable shape is declared in HOCON, type-validated at the app boundary, visible in `-w plan`, and does not manually read extra files or reconstruct ecosystem layers.

### 2.1 Nested App Identity and Config Namespace
As projects grow, especially data and in-silico projects with many providers, assays, models, engines, and workflow surfaces, app configuration must avoid both excessive flat width and arbitrary deep taxonomies. Wielder supports nested app identities through the same canonical app accessor rather than through project-local side loaders.

- **Guideline:** Nested app identity should be a POSIX relative app path passed directly to the canonical accessor, for example:
  ```python
  get_app_conf("ingestion/provider/assay")
  ```
- **Guideline:** The filesystem layout should mirror the app identity exactly:
  ```text
  conf/apps/ingestion/provider/assay/app.conf
  ```
- **Guideline:** The HOCON tree inside the app config should mirror the same semantic hierarchy:
  ```hocon
  ingestion {
    provider {
      assay {
        source_key = "raw/provider/in-vitro/adme/assay"
      }
    }
  }
  ```
- **Guideline:** Do not flatten a nested app namespace into underscore keys such as `ingestion_provider_assay` merely because the app has multiple hierarchy levels. Flattening erases ownership structure and causes config trees to drift from app identity.
- **Guideline:** Legacy flat app identities remain valid for genuinely flat apps, for example `get_app_conf("drive_fetch")` resolving `conf/apps/drive_fetch/app.conf`.
- **Guideline:** Nested app identities must be normalized relative POSIX paths. Reject absolute paths, `..`, duplicate separators, and Windows `\` separators at the resolver boundary.
- **Guideline:** Wielder owns the generic nested app resolution mechanism; each project owns its taxonomy. Do not encode project-specific categories such as `ingestion`, `msa`, `structure`, `adme`, or vendor names in Wielder itself.
- **Guideline:** Ecosystem names and app names are different contracts. An ecosystem may remain a flat routing identity such as `ingestion_provider_assay`, while the app config identity and tree remain nested as `ingestion/provider/assay` and `conf.ingestion.provider.assay`.
- **Guideline:** For data-domain app taxonomies, prefer stable operational discriminators near the front of the app path when they drive parsing and routing. Example:
  ```text
  conf/apps/ingestion/provider/assay/app.conf
  raw/provider/in-vitro/adme/assay
  ```

### 2.2 Configuration Provenance Hashing and Rehydration
Deterministic configuration identity and payload provenance are framework mechanics, not domain-specific application behavior. Projects should not each invent bespoke hashing or config rehydration functions.

- **Guideline:** Wielder owns generic deterministic hashing for resolved configuration trees and local runtime payloads. Prefer Wielder utilities such as `get_global_conf_hash(...)` and `get_local_provenance_hash(...)` over project-local copies.
- **Guideline:** Wielder owns generic config artifact rehydration from a concrete URI/path or from a hash plus a caller-provided provenance root.
- **Guideline:** Projects own where provenance config artifacts physically live. A project wrapper may resolve a domain root such as `conf.workspace.data.stage_root / "provenance" / "configs"` and then call the Wielder rehydration utility.
- **Guideline:** Volatile runtime fields such as telemetry, `year`, `month`, or `day` should be excluded through the Wielder hashing contract, preferably by explicit exclusion parameters or shared defaults. Do not hardcode volatile-strip logic independently in every project.
- **Guideline:** Keep backward-compatible project wrapper names only as thin bridges when existing callers depend on them. New code should import the Wielder utility directly unless it needs a project-owned provenance root.

### 3. Canonical Structural Mappings over Static Conditionals
A framework built to handle limitless topologies scales significantly better when deferring to explicitly loaded HOCON schemas rather than evaluating static rules.
- **Guideline:** Avoid hard-coding structural environmental identifiers (like `workstation_wsl` or `aws_eks`) directly within Python function logic (e.g., factory if/else statements).
- **Guideline:** Utilize explicit PyHocon mapping registries mapped natively within the project defaults (`e.g., wielder.ecosystem_map`). Use Python `match/case` functional blocks to map the extracted HOCON string cleanly onto an orchestrated class type.
- **Guideline:** When a topological string is unregistered, present the caller with a dedicated `ValueError` advising them to formally declare the new mapping directly in their canonical config tree.

### 4. Semantic Cloud Encapsulation ("Key" vs "Path") & Windows URI Vulnerabilities
In cloud infrastructure, standard POSIX "directory" terminology often implies rigid hierarchical filesystems, whereas blob stores and abstraction layers (S3, Google Drive) operate as flat-key structures.
- **Guideline:** When orchestrating cloud data transfers (like in `Bucketeer`), utilize the terminology `key` (e.g., `object_key`, `dest_key`) rather than `path`. This conceptual shift aligns the tooling seamlessly with the underlying non-hierarchical reality of the storage layer.
- **Guideline (Strict FS Agnosticism):** Bucket/object storage identifiers must stay provider-neutral through the app and test contract. Prefer explicit leaves such as `bucket`, `object_key`, `table_key`, or `output_key`; avoid names and logs that imply a navigable local filesystem unless the contract is explicitly local-only. A `file://`, `s3://`, `gs://`, mounted-volume, or catalog URI is an opaque handle at the application boundary, not permission to derive a local `Path`.
- **Guideline (Opaque Object URIs):** Code MUST NOT branch on a returned object URI to synthesize a local filesystem accessor, parent directory, preview server, or cleanup path. If code would break or mislead when the active ecosystem switches from local buckets to S3 or GCS, it violates the config contract even when hidden behind `Bucketeer`, Spark, a factory, or a helper with a generic name.
- **Guideline (Portable Logs):** Plan/apply/test logs should report bucket, relative key, catalog/table id, and opaque URI separately. Do not concatenate bucket and key into a pseudo-path when the output may live in an object store, and do not print local serve commands from a generic app/test surface.
- **Guideline (The Windows URI Vulnerability):** You MUST NOT use `os.path.join` to construct Cloud Object Storage URIs or Keys. If a pipeline is executed dynamically on a Windows node natively, `os.path.join` will inject `\` backslashes into the string. S3 and GCP treat `\` as a literal character, not a directory separator, resulting in corrupt, flat blob files (e.g., `raw\model\file.json`) instead of physical hierarchical namespaces. ALWAYS use strict POSIX concatenations (e.g., `"/".join(parts)` or `f"{base.rstrip('/')}/{suffix}"`).
- **Guideline (Static Resource Key/Path Harmonization):** For static resources generally, strongly suggest keeping the object-store semantic key and the runtime filesystem relative path identical after the bucket/root boundary unless a centralized accessor explicitly owns the translation. Harmonized key/path layouts simplify configuration, lookup, forensics, and orientation; they also minimize environment-to-environment diffs that otherwise turn into deployment bugs. Mounted volumes, snapshots, image-baked resources, and local mirrors should materialize data at the exact relative path returned by the runtime accessor.
- **Guideline (Ecosystem Boundary):** Ecosystem overlays should choose physical roots, buckets, mounts, storage classes, and snapshots. Strongly suggest avoiding ecosystem-local redefinitions of a static resource's inner semantic layout; if the inner layout is wrong, prefer fixing the canonical accessor/config contract or rebuilding the static resource at the canonical key/path over adding init-container symlinks, ad hoc shell remaps, or path aliases.

### 5. Cross-Topology Flexibility
Core factory functions should support explicit architectural overrides, acknowledging that topologies frequently demand interaction across network boundaries.
- **Guideline:** Expose optional typing identifiers across factory signatures (e.g., `bucketeer_type: str | None = None`). This permits specific components—such as an AWS service needing direct interface with Google Drive—to gracefully bypass standard environment defaults and manually assert their explicitly required target structure dynamically.

### 6. FS Agnostic Storage Boundary Discipline For Data Domains
Filesystem discovery and storage materialization must not leak into DAG logic, business logic, or notebook orchestration simply because the active runtime happens to be local.
- **Guideline:** Any operation that searches storage topology or artifact presence (for example `glob`, recursive file discovery, directory walking, or file existence checks) MUST be routed through a Bucketeer factory method or a domain accessor layered on top of Bucketeer. Application code MUST NOT perform raw OS discovery directly.
- **Guideline:** Any operation that materializes, copies, syncs, or deletes storage artifacts (for example `shutil.copy*`, `os.makedirs`, `os.rename`, `os.remove`, `Path.mkdir`, or ad-hoc directory creation) MUST be owned by Bucketeer or a dedicated accessor, not by the DAG runner.
- **Guideline:** Local filesystem convenience may be exposed only through a local-only contract whose name, config leaf, and logs say so plainly. A generic app, test fixture, or notebook companion must not call `Path(uri)`, inspect `://`, take `parent`, or otherwise reinterpret an object URI as a filesystem path.
- **Guideline (Engine-Native Table IO):** Table engines such as Spark may own table-scale reads and writes through their native source/sink abstraction. Do not force Spark table writes through Bucketeer merely to satisfy the accessor rule. The engine's source URI, sink URI, catalog, filesystem implementation, credentials mode, and provider-specific options for local filesystem, S3, GCS, or other storage surfaces must be resolved from config.
- **Guideline (PySpark Artifact Contracts):** Spark-backed apps should publish versioned `spark_artifact_jobs` HOCON contracts that Wielder validates and executes. Do not invent Python-side config path strings or reconstruct Spark descriptors outside the normal config mode stack.
- **Guideline (Discovery vs Table IO Boundary):** Use Bucketeer or a domain accessor for object-key discovery, small artifact lookups, and storage topology enumeration. Use the configured table engine for dataframe/table reads and writes. Application code should not hand-build either object-store keys or Spark sink paths inline.
- **Guideline:** `os.path.join`, `dirname`, and similar functions are prohibited for storage key construction. Parsing a resolved filename token via `basename` or `splitext` is acceptable, but storage lookup and routing are not.
- **Guideline:** Looking up code paths or configuration paths is still path-boundary logic. If code is deciding where config, parquet, images, or outputs live, that resolution belongs in the configuration bootloader, Bucketeer, or a centralized accessor layer.

### 7. Global Stage Tier Nomenclature (`stage_tier`)
Deployment environments (`dev`, `int`, `qa`, `stage`, `prod`) must be physically segregated to prevent data collisions.
- **Guideline:** Use `stage_tier` to define the target environment. This configuration resolves strictly beneath the active `context_conf` pack to guarantee local sandboxes override production defaults.

### 7.1 Compound Resource Identity (`unique_name`)
`unique_name` is the concrete identity boundary for provisioned and staged
runtime assets. Use [Unique Name Identity](../architecture_skills/SKILL_UNIQUE_NAME_IDENTITY.md)
for the full doctrine.

- **Guideline:** Compose `unique_name` from resolved config leaves such as
  `stage_tier`, `project`, `owner`, `ecosystem`, `slug`, and `incremental_id`.
- **Guideline:** Named context packs may intentionally override `project`,
  `slug`, or `incremental_id` to create a separate runtime silo.
- **Guideline:** Do not synthesize or override `unique_name`, `git.commit`, or
  `git.short_commit` in Python, environment variables, generated shell wrappers,
  or ad hoc CLI flags.
- **Guideline:** Reusing an existing `unique_name` is an intentional attach
  operation and must be visible in the active context pack.

### 7.2 Central Context Packs over Repo-Local Developer Overlays
- **Guideline:** Standardize developer-local overrides in `context_conf/<name>/` at the super-repo root. Do not keep repo-local `conf/developer/` folders as active peers in the load path.
- **Guideline:** `context_conf/default_conf/` is the canonical baseline context. Additional named packs (for example `context_conf/hermes_batch_qa/`) are encouraged when developers need shareable, versioned local contexts.
- **Guideline:** Inside application repos, track only `conf/context_conf_examples/<name>/`. The live local `conf/context_conf/<name>/` tree is purely local state and must be ignored by Git.
- **Guideline:** The sanctioned operator flow is: copy one example pack, then edit it locally.
  - Example: `cp -r conf/context_conf_examples/default_conf conf/context_conf/default_conf`
- **Guideline:** App-scoped service-shape toggles such as `debug_mode` and `local_mount` should remain app-level config values and be overridden from the active `context_conf` pack, not promoted into a global topological tier.
- **Guideline:** Map physical bucket roots via `stage_tier` (e.g., `workspace-<domain>-<stage_tier>`) rather than routing environments manually.
- **Guideline:** Store environment-specific configuration in `domain-data/conf/stage_tier/<stage>/tier.conf` to enforce uniform fallback inheritance.

### 8. Core Topological Dimensions
Agentic configuration reasoning MUST respect the primary topology dimensions engineered into the framework's semantic contract:
- **Ecosystem**: An epigenetic/topological layer over code. Together with other modulators, it defines how code is expressed in a distributed cloud environment: workstation, local filesystem, object buckets, Kubernetes, Spark, EMR, service routes, credentials boundaries, provider surfaces, and other environment-of-environments relationships. An ecosystem is not the app itself and not a single launched resource; it is the resolved operational expression context for code. Ecosystems are separated into domain ecosystems, surface ecosystems, and aggregating wrapper ecosystems; normal app entrypoints run under wrappers.
- **Wielder**: An entrypoint acting under a resolved, modulated, one-source-of-truth configuration. It uses its resolved ecosystem plus transient/context configuration to decide what to plan, apply, delete, provision, route, or invoke.
- **Wielded**: An app or entrypoint whose expression is being controlled by a Wielder. A Wielder may assign the Wielded app a particular ecosystem expression and pass narrow overrides or transient configuration to shape that expression. The Wielded unit may represent only a subset of the larger ecosystem.
- **Compute Surface (`surface`)**: Formally replaces the legacy term `runtime_env`. It strictly defines the material physical execution plane (e.g., `docker`, `kind`, `gcp_gke`). An app-level configuration natively inherits the Ecosystem's default surface but can execute a structural override natively.
- **Stage Tier**: The chronological deployment boundary (`dev`, `stage`, `prod`).
- **Security Mode**: The RBAC and compartmentalization policy (e.g., isolating production secrets via overlapping 'dud-service' architectures).
- **Ephemerality Policy (`deletion`)**: The mandated teardown behavior (`full_ephemeral`, `partial_recycle`, `persistent`).
- **Deploy Strategy (`canary`)**: The overarching deployment footprint trigger (`standard`, `fuzzy_predicates`).

### 8.0.1 Agent Assumption Boundary
When reasoning about ecosystems, agents must distinguish conceptual possibility, roadmap intent, and currently implemented bootability. Do not infer that a topology should be implemented merely because it is conceptually possible, and do not infer that a local GUI should wield a remote ecosystem merely because the configuration vocabulary can express that relationship. State the distinction explicitly during planning and ask before crossing from architecture alignment into implementation.

### 8.1 Service Topology Ownership: Ecosystem over DAG
Distributed service transport selection must ride on the Ecosystem axis, not inside domain DAG payloads.
- **Guideline:** If an application can operate against multiple transport surfaces (for example `sdk` vs `grpc` for a preparation dependency), the active mode MUST be resolved from the ecosystem configuration tree, not embedded repeatedly on each DAG target.
- **Guideline:** DAG payloads should declare domain intent (`use_preparation`, upstream dependency presence, target identifiers), not infrastructure reachability modes such as specific local-kube surfaces, cloud providers, or hostnames. Those are environmental topologies and therefore belong to the ecosystem hierarchy.
- **Guideline:** Development ecosystems are allowed to prefer local-first modes (for example `sdk`) even if production ecosystems ultimately prefer remote service transport (`grpc`). This is not wasteful duplication; it preserves local iteration speed and decouples application development from image-build and deploy latency.
- **Guideline (Per-Service Hybrid Placement):** A hybrid ecosystem should be able to place each service independently through resolved config. Do not collapse the whole wrapper into a single local/kube boolean. Use per-service leaves for local process vs Kubernetes service vs job vs provider runtime so one service can be developed locally while sibling services remain deployed.
- **Guideline (Ecosystem Families):** When several concrete ecosystems share a workload family, use a base ecosystem family manifest to gather shared intent, naming, contracts, and common defaults, then let concrete child ecosystems include that base and express only the minimal surface-specific diff. A concrete ecosystem should not repeat shared domain intent or future-facing contracts merely because it runs on AWS, GCP, Kind, K3d, or another surface.
- **Guideline (Resource Subset Ecosystems):** If the operator is choosing between stable resource shapes such as a durable kernel and an ephemeral runtime expansion, model that as thin ecosystem overlays, not workflow booleans. The base ecosystem should express the zero/off resource subset; the expansion ecosystem should include the base manifest and override only the keys that move resources from 0/off to N/on.
- **Guideline (Thin Runtime Overlays):** A runtime overlay should be as small as possible: one include plus explicit overrides for active third-party deployment lists, prune lists, Terraform module enabled/count values, node-group scale, and service deploy steps. Do not create Python branches, ad hoc CLI flags, or generated injection payloads when a static ecosystem overlay can express the same topology.
- **Guideline (Concern-Split Ecosystem Includes):** When an ecosystem coordinates several functional surfaces, split its manifest into small concern files such as `surfaces.conf`, `wjobbard.conf`, `manual_sync.conf`, and `integration_test.conf`, then have `ecosystem_manifest.conf` include them. This makes the ecosystem readable and lets another ecosystem include the whole family or only the relevant concern files without copying unrelated behavior.
- **Guideline (Reusable Data Contracts Belong in Ecosystem Concerns):** When a schema, table contract, registry, catalog, or serialization surface is intended to be reused by multiple apps, place that reusable contract in one canonical ecosystem concern file such as `schema.conf`, `tables.conf`, or `catalog.conf`, then include it from the owning ecosystem manifest. Keep the app baseline focused on executable defaults, fail-closed toggles, and local behavior needed by that app. This lets consumer apps import code and incorporate the shared ecosystem concern without copying app-local config or inventing a second serialization contract.
- **Guideline (Schema Near Code Without App-Locking):** Keeping schemas close to implementation does not require storing them in `app.conf`. The code should validate against the resolved canonical schema subtree, while the reusable schema subtree lives in an includable ecosystem concern. This preserves code/schema alignment through a single source of truth while allowing other apps and ecosystems to serialize, deserialize, search, or display the same tables.
- **TODO (Project-End Config Hygiene):** Before closing a project that introduces or clarifies reusable ecosystem contracts, scan sibling apps for app-local reusable schemas, table contracts, registries, catalogs, or serialization surfaces that should have been ecosystem concerns. Move confirmed violations into canonical includable ecosystem concern files and update consumers to resolve the shared subtree rather than copying app-local config.
- **Guideline (Consider Shared Config Extraction):** If two ecosystems need the same subtree, consider extracting that subtree into an includable concern file or small config library. Do this when the reuse is stable enough to justify another config boundary. Avoid premature config fracturing: a shared file reduces duplication, but it also adds indirection. If the overlap is small, unstable, or accidental, local duplication with clear ownership may be simpler.
- **Guideline (Ecosystem Boundaries as Imports):** Ecosystem composition should be explicit, much like code imports. An ecosystem that needs another functional concern should include that concern or declare a clear boundary contract to it. Avoid accidental cross-ecosystem leakage where one ecosystem only works because Python side-loads another ecosystem or uses a neutral escape ecosystem.
- **Guideline (Foreign App Boundary Config):** When an app or workflow wields a foreign app, model that relationship explicitly in config under a clearly named boundary such as `foreign_apps`. Include the foreign repo or submodule name, foreign app identity, Wielder modes needed for CLI handoff (`ecosystem`, `stage_tier`, `context_conf`, `security`, `canary`), deploy repo/app/job when a deployment surface is involved, and other durable information necessary for wielding such as verification mode or provider. Keep run/test mechanics such as timeouts, retries, and enabled-for-test switches in the owning test or workflow scope rather than in the durable foreign-app boundary.
- **Guideline (Functional Includes, Not Mode Leakage):** Concern files should describe durable functional topology: cloud surfaces, registries, workflow selections, manual GUI enablement, test harness topology, event consumers, and cross-surface identities. Stage-specific facts such as `dev`, `qa`, and `prod` values still belong in `stage_tier`; developer-local switches still belong in `context_conf`.
- **Guideline (Fail-Closed App Defaults):** If a behavior should only activate inside a specific ecosystem, keep the app baseline fail-closed with empty arrays or disabled toggles, then enable it from the ecosystem concern file. This preserves the app contract while preventing broad app defaults from accidentally deploying a workflow in unrelated ecosystems.
- **Guideline (Concrete Ecosystem Minimalism):** Concrete ecosystems should specialize the physical/runtime surface: provider, bucket roots, registries, IAM/RBAC, trigger topology, mounts, ports, scheduling, and deploy behavior. Keep the concrete overlay thin enough that moving from one surface to another is a visible diff, not a duplicated copy of the whole workflow contract.
- **Guideline (CLI Overrides as Boundary Tools):** CLI overrides may be appropriate when crossing app or submodule boundaries through another canonical accessor, but they should have a concrete reason. Prefer forwarding broad mode identity such as `ecosystem`, `stage_tier`, `context_conf`, `security`, and `canary` over smuggling hidden business topology. Code should not synthesize ecosystems, paths, jobs, or data contracts that belong in resolved config.
- **Guideline (Event Consumer Semantics):** For Pub/Sub-like storage or workflow events, prefer `event_consumer` and `subscribe` language over `listener` and `listen`. The app should ask the generic event consumer factory for the configured consumer and pass a callback; provider polling, subscription registration, queue setup, and native event mechanics belong behind that configured consumer boundary.
- **Guideline (Provider-Qualified Local Surfaces):** When a local runtime still speaks a provider-specific transport, encode both facts in the runtime surface, for example `local_aws` for host-side AWS SNS/SQS polling or `local_gcp` for host-side GCP Pub/Sub polling. Avoid generic `local` for event-consumer surfaces; local Kafka, local AWS, local GCP, and local filesystem semantics are different contracts and should not be collapsed into one string.
- **Guideline:** Container environment variables may mirror topological modes such as `ECOSYSTEM` or `STAGE_TIER` for telemetry and forensic visibility, but application execution logic should prefer resolved configuration trees rather than reading those environment variables as the primary operational truth.
- **Guideline:** Workflow-specific messaging contracts such as Kafka topics and consumer groups should live at ecosystem scope when the workflow is currently 1:1 with that ecosystem. If several ecosystems later share the same workflow contract, extract it into a reusable workflow-level include rather than pushing it back to project root.
- **Guideline (Bind vs Access Ports):** Strongly suggest separating service bind ports from externally consumed access ports. The in-process server bind port belongs to the runtime surface contract, while NodePorts, forwarded ports, or other external access coordinates belong to the deploy/service contract. Do not overload one `grpc_port` field with both meanings.
- **Guideline (No Surface Leak Fixes):** If a deployed service fails due to a port, probe, or container bootstrap mismatch, do not fix it by teaching the application repo about deploy-surface-specific loaders or by making the scientific app reason about Kubernetes particulars. First repair the deploy/service contract and keep the application bound only to a complete ecosystem contract.

### 8.2 Shared Service Layering: Core -> Side-Effect Layer -> Transport
When an application exposes the same capability through both direct API transport and local SDK execution, the implementation must be layered cleanly to avoid WET transport logic.
- **Guideline:** Extract the pure computational core first (for example a preparation function returning a native result payload).
- **Guideline:** Extract a side-effect layer above that core which owns the canonical external effects such as datalake persistence, manifests, telemetry, and completion markers.
- **Guideline:** The direct API transport layer (for example a gRPC servicer) MUST call the extracted side-effect layer rather than containing unique persistence logic inline.
- **Guideline:** The direct SDK path MUST call that same side-effect layer rather than simulating a local gRPC roundtrip.
- **Guideline:** If a producer DAG, an SDK caller, and a direct API surface such as gRPC all expose the same domain capability, they should converge on the same side-effect layer so that canonical external effects are not fragmented across three implementations.
- **Guideline:** If time and scope were unconstrained, a brokered messaging IO architecture would be the more reactive long-term shape than direct API calls. Until that complexity is justified, keep the present direct API layering explicit and local rather than prematurely splitting into micro-micro services.

### 8.2.1 Runtime Failure Triage: Config Truth vs Live Image Truth
- **Guideline:** Strongly suggest distinguishing three layers during service-failure investigation: resolved repository config, applied deploy manifest, and live container behavior. A match between the first two does not prove the live container is running the intended code.
- **Guideline:** Strongly suggest checking live Kubernetes evidence in this order when a service restarts or fails probes: `kubectl describe`, current logs, previous logs, ConfigMap or Secret payload, and the live Deployment manifest.
- **Guideline:** Strongly suggest treating probe failures and exit code `137` carefully. They often indicate the kubelet killed a process for failing health checks rather than an application exception trace.

### 8.3 Workflow Monitors and Sidecar CLIs
Operational monitors often need both Wielder topology and a small local action vocabulary. That combination should not create a second configuration language.
- **Guideline:** Strongly suggest keeping Wielder topology resolution and script-local actions as separate concerns. The script-local action should be narrow and positional, while ecosystem and stage resolution should still come from the canonical config accessors.
- **Guideline:** Strongly suggest avoiding ad hoc argv rewriting, synthetic parser stacking, or manual flag merging between a local operational CLI and the Wielder CLI surface.
- **Guideline:** When a script has a single dominant interactive behavior such as traffic monitoring, strongly suggest defaulting direct invocation to that behavior and reserving extra actions for explicit internal calls or clearly separated entrypoints.

### 9. The `__file__` Context Drift Antipattern
Legacy python patterns frequently use `os.path.dirname(__file__)` to trace project directories relative to the execution script. In a unified orchestration topology, **this is a catastrophic antipattern**.
- **The Bug:** If a module (like `Wielder`) is globally `pip install`ed, `__file__` will traverse backward into the system Python or PyEnv directories (e.g., `~/.pyenv/versions/...`), completely severing the script from the actual codebase root and corrupting staging directories or Docker contexts.
- **Guideline:** NEVER deduce project geometry or staging roots using `__file__`.
- **Guideline:** There is only ONE source of local Filesystem Truth: **The PyHocon Configuration Stream**. Roots must be strictly evaluated at the configuration source (`conf.super_project_root` or `conf.stage_root`) and statically passed down to orchestrators and SDK execution proxies.

### 10. Inline Import Discipline
Inline imports (import statements nested inside functions or methods) obscure dependency trees, trigger unpredictable parsing latency during execution sequences, and fracture static analysis graphs.
- **Guideline:** NEVER use inline imports natively within Wielder execution graphs or applications. ALL imports must be physically hoisted to the global `HEAD` of the module.
- **Exceptions:** Inline imports are strictly forbidden unless mathematically necessary to break confirmed circular dependencies, isolate heavily localized Process/Thread initializations, or conditionally load massive multi-gigabyte Data Lake libraries (e.g., `PyTorch` or `Tensorflow` in a lightweight REST API). Short of those exact hardware/memory constraints, use global imports natively.
