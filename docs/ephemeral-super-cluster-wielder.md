# Ephemeral Super Cluster Orchestration

## 1. Ontological Glossary

**Ecosystem**: A specific, contextually bound set of distributed surfaces mapped to a defined workload. For example, an ecosystem can be actively defined as DAGs running on AWS alongside Kubernetes services and Airflow, or alternatively operating locally on WSL and Docker Kubernetes—with all underlying operational deltas fully abstracted, anchoring semantic alignment and explicit execution topologies across distributed domains.

**Mode**: An operational variation (e.g., DevOps, MLOps, SecOps) acting on the central theme of business logic and functionality. Mode actively routes the operational behavior of the workload—dictating execution scope, cloud provider abstraction, or how APIs are exposed and consumed (e.g., a service running on AWS explicitly calling a remote GCP API versus hitting a local emulator). These operational modes are dynamically modulated by the surrounding `ecosystem`, `stage_tier`, or `security` dimensions.

**Stage Tier**: The chronological or environmental isolation level of the deployment (e.g., `dev`, `qa`, `staging`, `prod`). This bounds the configuration lifecycle, establishing a baseline for reproducibility as state transitions from development towards production.

**Security Mode**: The compartmentalization dimension determining RBAC and data sensitivity rules. This governs structural shielding, such as deploying symmetric "dud-services" when operating in highly classified bounds.

**Ephemerality Policy**: The strict behavioral contract dictating exactly how and when an ecosystem transitions into the `DELETE` phase (e.g., `full_ephemeral`, `partial_recycle`, or `persistent`). It completely eliminates auto-destruction ambiguity by forcing developers to explicitly declare the teardown calculus within the foundational PyHocon configuration. Crucially, like `stage_tier`, this policy is natively dynamic—it can vary between CI/CD pipeline stages and can be explicitly overridden by a local engineer via their `developer.conf` to easily retain a dying cluster for active debugging.

**Deploy Strategy**: The execution layout parameter (e.g., `standard`, `canary`, `blue_green`). This formal lifecycle dimension physically configures the underlying infrastructure generation (like fractionally scaling redundant pods or configuring separate traffic routing nodes) strictly at the configuration abstraction layer. Similar to `mode` or `stage_tier`, this strategy is highly fluid; it allows an engineer to seamlessly pivot a standard local deployment into a complex canary rollout simply by altering a single key in their `developer.conf`.

**Surface Polymorphism** (Mixability): The architectural capability to pick and choose different distributed surfaces (e.g., local containers vs. managed cloud clusters), abstracting their implementation details behind a unified interface analogous to the Factory Pattern. This property enables maximum local emulation of cloud-native execution states, allowing developers to construct ecosystems that operate primarily locally while explicitly bridging to remote datastores or compute nodes; minimizing "It worked on my computer" bug scenarios.

**Ephemeral Super Cluster**: An orchestrated engine that algorithmically provisions, validates, and ultimately destroys a designated synthesis of ecosystems (such as combined Kubernetes, Apache Spark, and Elastic Stack footprints) on a transient, as-needed basis.

**Antifragility**: The structural evolution beyond reactive infrastructure. While reactive systems respond predictably to predefined triggers, true antifragility will be reached by deploying autonomous agents that continuously monitor, analyze, and reconfigure the distributed super cluster in real time. By isolating cloud-provider deltas and prioritizing agnostic workload definitions, the underlying infrastructure withstands scale and variance through low coupling and explicit substitution—forming a foundation for agentic governance.

**Epoch**: A strictly defined, forensically accountable execution state bound to a runtime configuration, establishing a baseline for reproducibility across deployments and real-time reconfigurations. When Epochs change they are kept in a versioned repository for audit forensics and reproducibility purposes. The resolved configuration is the actual state of the cluster at the time of the epoch and any change is kept in a versioned repository.

---

## 2. Infrastructure as a Reactive Modulation

Proprietary cloud wrappers like AWS EKS/EMR, GCP GKE/Dataproc, and base provisioning tools like Terraform function as execution toolboxes—transient runtime implementations executed by a core orchestration semantic. 

The core orchestration logic modulates to run across varying physical topologies, maximizing surface polymorphism and local emulation:
* **Locally**: Deploying to local Docker clusters, minikube, or local standalone services to emulate cloud states.
* **AWS**: Modulating natively to Elastic Kubernetes Service (EKS) and Elastic MapReduce (EMR).
* **GCP**: Modulating to Google Kubernetes Engine (GKE) and Cloud Dataproc.

This polyglot deployment model provides a **reactive, fault-tolerant** environment where the fundamental technology abstractions (Kubernetes, Spark) resolve predictably. The polymorphic interface bridging local and cloud systems empowers developers to construct an ecosystem that acts locally but explicitly taps into remote infrastructure.

---

## 3. Strict Contracts, Loose Usage

When bridging local development, simulation testing, and massive cloud production environments, traditional Infrastructure-as-Code (IaC) is highly susceptible to configuration drift and implicit assumptions (WET configuration). 

Wielder secures architectural stability by enforcing strong contracts around a loose, flexible usage model:
* **Explicit Epochs**: Base configurations exist in hierarchical HOCON (`.conf`) files. PyHocon natively acts as a dynamic superset of JSON and YAML. Through Wielder, it serves as the supreme configuration interface: `tfvars`, cloud CLI inputs, APIs, runtime objects, Maven/Gradle builds, Spark jobs, Airflow DAGs, and Kubernetes YAMLs—everything gets configured exclusively by HOCON. Runtime deployment bounds (scale, mock isolation, target platform) are evaluated dynamically, anchoring each execution as a strict, forensically accountable epoch.
* **Isolating Deltas**: Cloud-specific surface deltas are pushed to the absolute periphery of the runtime adapters. For example, a Kubernetes **storage class** interpolation might be the *only* operational difference between a stateful pod running on local Docker, KIND, AWS EKS, or Google GKE. The core semantic orchestration remains unified.
* **Abstracting the Basic Tech**: By standardizing the interfaces to the foundational technologies rather than the provider-specific wrappers, the orchestration structure resists builder's bias and silent architectural drift.
* **The Structural Distaste for Mocks**: Wielder maintains an inherent, structural distaste for mocks. The primary orchestration objective is to deploy and interact with exact, unadulterated production equivalents (e.g., orchestrating native Postgres or Spark containers locally) rather than substituting behavior with software mocks or fake APIs. Mocks are explicitly treated as a last resort—utilized *only* when the local topological surface physically cannot bear the compute, memory, or data load of the native service.
* **Load-Test Supremacy**: Wielder actively discards fragmented testing models. A fully parameterized load test acts as the supreme architectural verification. Integration and unit tests are simply down-scaled modulations of this ultimate load test. For example, tearing down and algorithmically reprovisioning an entire local environment serves as a definitive integration test; identically, modulating the deployment to a lightweight cloud environment with restricted data volume achieves the same verification. The orchestration remains unified; only the scale and data dimensions vary.

---

## 4. Reified Python DAGs & Auditability

Instead of isolated, static declarative YAML or HCL arrays, deployment executes as an event-driven Python DAG (Directed Acyclic Graph). This yields structural accountability and verifiable provenance across test and deployment sequences:
* **Local Developer Sovereignty**: A developer evaluates an infrastructure stepping stone by running the `wield_super_cluster()` logic from their local IDE directly against Docker, gaining immediate feedback through accurate local emulation.
* **Pipeline Automation**: Continuous integration layers leverage the identical function to deploy an ephemeral super cluster in the cloud, execute explicit handoffs and live verifications, and programmatically tear it down. 

Loose usage paired with strong contracts creates an adaptive, fault-tolerant integration ecosystem, driving resilience against accumulated state and static resource costs.

---

## 5. Compartmentalization & RBAC Security Mode

Because the orchestration is configuration-driven and built on discrete modules, user classification and Role-Based Access Control (RBAC) compartmentalization can be strictly maintained at every level—ranging from fine-grained submodule permissions to entirely differing super-module subsets. 

To formalize this, a distinct **security mode** will be engineered as a primary topological dimension, layering directly on top of the established `ecosystem` and `stage_tier` axes.

### The "Dud-Service" Paradigm for Secret Interleaving
An extreme but robust example of this compartmentalization is the polymorphic substitution of highly sensitive services. Within a classified architecture, sensitive modules can be programmatically swapped for "dud" services. These dud services bind to the exact same interfaces—outputting benign nonsense to the same Kafka topics or exposing an identical API serving randomized dummy data.

This structural shielding enables distinct RBAC groups (such as DevOps or platform engineering) to fully orchestrate, debug, and load-test the entire distributed super cluster without ever requiring exposure to the secret code or proprietary intellectual property.

---

## 6. The Roman Pantheon Strategy

In an antifragile ecosystem, theological adherence to a single provisioning paradigm operates as a critical vulnerability. Instead, Wielder adopts the **Roman Pantheon Strategy**: willingly aggregating, integrating, and commanding any provisioning or build tool that successfully achieves the workload objective, continuously subordinating them beneath the supreme PyHocon configuration layer.

This "polytheistic" infrastructure approach willingly incorporates and commands:
* **Declarative "Uncool" Tools**: Such as Terraform, utilized purely as brute-force, disposable execution toolboxes for base hardware footprints.
* **Declarative "Cool" Tools**: Such as raw `kubectl`, providing direct, predictable stateless control.
* **"Semi-Cool" Tools**: Such as Helm, facilitating rapidly templated baseline deployments.
* **"Semi-Cooler" Tools**: Such as native Kubernetes Operators, introducing active, intelligent control loops to complex stateful services.
* **"Super Cool" Tools**: Such as deeply integrated Wielder deployments and Reified Python DAGs, choreographing the holistic lifecycle across these disparate tools with explicit, event-driven precision.

By absorbing these diverse tools into the pantheon rather than dogmatically competing against them, Wielder acts as the overarching empire—providing strict `epoch`, `mode`, and `stage_tier` contracts, while letting the individual deities execute the physical heavy lifting.

---

## 7. Appendix: Mandatory Execution Contracts

### 7.1. Epoch Required Fields
Every explicitly anchored Epoch must resolutely capture the following footprint:
* `epoch_id`: Strict UUID identifying the deployment matrix.
* `run_id`: The CI/CD or explicit invocation execution trace.
* `config_hash`: A cryptographic fingerprint (e.g., SHA-256) of the resolved, flattened PyHocon dictionary. To guarantee deterministic hashing and prevent false drift, the dictionary must be strictly serialized via canonical JSON (alphabetically sorted keys, normalized primitives) prior to hashing.
* `git_matrix`: Submodule commit hashes confirming exact spatial code relativity.
* `stage_tier` & `mode`: The topological and behavioral routing boundaries.
* `security_mode`: The active RBAC compartmentalization state.
* `ephemerality_policy` & `deploy_strategy`: The behavioral lifecycle parameters explicitly regulating precisely how the cluster scales (e.g., `canary`) and tears itself down (e.g., `full_ephemeral`).
* `timestamp`: The precise temporal synchronization.

### 7.2. Epoch Enforcement by Artifact Class

The epoch contract is not enforced by a single Python-level gate. It is enforced
structurally, and the mechanism differs by artifact class. See
[`SKILL_EPOCH_ARTIFACT_GOVERNANCE.md`](../foundation/skills/wielder/SKILL_EPOCH_ARTIFACT_GOVERNANCE.md)
for the full specification. Summary:

| Artifact Class | Mechanism |
|---|---|
| Terraform infrastructure | Config-generated tfvars (same epoch chain as resolved conf) + remote state backend |
| Container images | Tag = `unique_name + git.commit`; registry immutability |
| Resolved conf | `latest.conf` (one active per `unique_name`) + content-addressed forensic trail |
| Python/Spark code bundles | Content-addressed bundle key (see below) |

**Resolved conf** materializes the fully resolved PyHocon tree scoped to a
`unique_name`. There is exactly one valid config per `unique_name` at any time:
`latest.conf`, which is overwritten on every publish. The versioned keys
(`epoch_ms--git_sha--conf_hash`) are kept purely for forensics and
reproducibility — not as simultaneously active states. The `conf_hash` is a
SHA-256 of the HOCON payload, making each forensic record content-addressable
for exact epoch reconstruction. Pods bootstrap from the versioned artifact in
object storage, so a dirty local tree cannot affect a running pod.

**Python/Spark code bundles** must be content-addressed at the storage key level
so that a dirty-tree republish at the same git SHA cannot silently overwrite a
previously published bundle. The per-artifact SHA-256s already computed during
publication should be used to derive a `bundle_content_hash` included in the
`bundle_root_key`. This is a standalone fix to `Wielder/wielder/python/artifactor.py`
and does not affect resolved conf, container images, or provisioning.

### 7.2. Lifecycle States & Required Transitions
Ephemeral orchestration strictly honors the `PLAN -> APPLY -> PROBE -> DELETE` semantic flow:
* **PLAN**: Evaluates configuration boundaries dynamically and generates the explicit contextual plan.
* **APPLY**: Executes the physical provisioning of the varied cluster and module footprints.
* **PROBE**: Validates liveness, interface parity, and readiness of the deployed ecosystem against explicit quantitative SLO thresholds (e.g., `< 200ms` API latency, `100%` data ingestion success rate). To prevent subjective compliance, these probes must query a canonical, centralized telemetry gateway (e.g., Prometheus) over a strict, predefined time window (e.g., a continuous 5-minute rolling window post-deployment).
* **DELETE**: Destroys transient architecture completely. To resolve the tension between absolute ephemerality and iterative development speed, a run must declare one of two explicit policy classes:
  * `full_ephemeral`: Enforces a true zero static footprint (the "giant Spark job" terminating entirely).
  * `partial_recycle`: Authorizes tiered/cherry-picked destruction, preserving foundational architecture specifically for rapid iterative emulation.

**Sanctioned Execution Scopes**: 
While the continuous semantic flow is mandatory for full epoch cycles, Wielder explicitly sanctions partial executions for debugging and CI gates:
* **Plan-Only (`PLAN`)**: Halts before execution; used extensively for CI drift detection and PR validation.
* **Persisted Emulation (`PLAN -> APPLY -> PROBE`)**: Intentionally halts before `DELETE` under `partial_recycle` policies to allow active human debugging or to sustain long-running integration environments.

### 7.3. Ephemerality
True ephemerality demands that infrastructure does not merely exist, but algorithmically vanishes with absolute precision. To operationalize the "giant Spark job" philosophy, the architecture enforces the following parameters:

#### Teardown Guarantees
* **Destroy Order**: Reverse topological dependency destruction (e.g., orchestrators and pods terminate before stateful persistence layers).
* **Shared-Resource Guardrails**: Strict protection boundaries preventing the deletion of statically persisted external assets (e.g., central Data Lakes or persistent event streams).
* **Orphan Checks**: Post-destroy telemetry confirming zero floating NAT gateways, unattached EBS volumes, or rogue load balancers.
* **Destruction Tiers, Cherry-Picking, & Canary Sub-Deployments**: Because every service, deployment, and provisioning unit is strictly encapsulated into discrete topological modules, teardowns extend far beyond binary or static hierarchical tiers:
  * **Tiers**: The orchestrator can algorithmically destroy ephemeral application workloads while leaving foundational architecture (like VPNs, raw Kubernetes clusters, or Spark infrastructure) running to rapidly accelerate the next iteration cycle.
  * **Cherry-Picking**: Individual components can be securely cherry-picked for targeted destruction just as easily as re-configuring a module metric at runtime.
  * **Canary Sub-Deployments**: As the ultimate granular control, this modular ephemerality natively supports canary sub-deployments—allowing fractional destruction and rolling re-provisioning of specific nodes or services to observe live topological behavior without declaring a full-scale cluster teardown.

### 7.4. Security-Mode Substitution Constraints
When operating under restricted security modes utilizing the "Dud-Service" Paradigm:
* **Interface Parity**: Non-sensitive mock modules must expose the exact identical gRPC/REST APIs and expected schemas as their hidden counterparts.
* **Sanitized Outputs**: Immediate failure if mock modules log, broadcast, or write any proprietary shapes, structures, or intel to topics/metrics.

---

## 8. Fail-Closed Rules
If an architectural contract violation is detected, Wielder adopts a **fail-closed** doctrine, halting orchestration rather than attempting a degraded execution:
* **Missing Config Dimensions**: If `mode`, `stage_tier`, `ecosystem`, `ephemerality_policy`, or `deploy_strategy` fail to explicitly resolve, the orchestrator triggers an immediate `ConfigMissingException`.
* **Submodule Drift**: If the expected git matrix does not match the active super-repository manifest, execution halts to protect topological integrity.
* **Probe Failure**: If the `PROBE` state detects missing interfaces or unauthorized data leaks, it triggers a policy-gated fast-forward to the `DELETE` phase. Rather than executing an unconditional auto-destruction, this mandatory teardown remains strictly governed by explicit operator or CI/CD safety protocols to systematically burn the compromised footprint.

---

## 9. Minimum Compliance Checklist
For DevOps, MLOps, or feature teams implementing infrastructure via Wielder, minimum structural compliance is defined as:
- [ ] Ecosystem, Mode, Stage Tier, and Security axes are explicitly declared in the root `.conf` module.
- [ ] No `os.environ` or volatile CLI arguments bypass the PyHocon resolution hierarchy.
- [ ] Deployments follow the strict and explicit `PLAN -> APPLY -> PROBE -> DELETE` protocol.
- [ ] `DELETE` phase execution is successfully tested locally, securing 100% ephemeral teardown metrics without orphans.
- [ ] "Dud-services" deployed for secret bounds expose 1:1 identical interfaces without logging sensitive tokens to stdout.
