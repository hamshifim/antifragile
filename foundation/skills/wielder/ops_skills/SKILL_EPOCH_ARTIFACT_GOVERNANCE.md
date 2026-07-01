---
description: Epoch artifact governance — how the epoch contract is enforced across the four artifact classes (provisioning, container images, resolved conf, Python/Spark code bundles) and what immutability means in each case.
---

# Epoch Artifact Governance

Use this skill when designing, auditing, or extending any publication pipeline
that produces versioned artifacts — provisioned infrastructure state, container
images, resolved configuration snapshots, or Python/Spark code bundles.

## The Epoch Contract

Every execution must be tied to a forensically accountable epoch: a binding
between a resolved configuration state and a versioned code identity. If either
mutates materially, the epoch must advance and the prior state must be
retrievable.

The contract does **not** require a Python-level runtime gate. It requires that
the artifact storage mechanism makes silent overwrites structurally impossible
and that every published state is independently recoverable.

---

## Four Artifact Classes and Their Epoch Mechanisms

### 1. Provisioned Infrastructure (Terraform)

**Epoch mechanism:** Terraform remote state backend + config-generated tfvars.

- `WrapTerraform` in `Wielder` generates `terraform.tfvars` by calling
  `config_to_terraform(tree=conf.tfvars, ...)` at provision time. Terraform's
  variable inputs are derived from the resolved PyHocon config, not from local
  Python source files.
- A dirty Python tree cannot affect what Terraform provisions — the apply
  consumes generated tfvars from the canonical config resolver, not Python
  module state.
- Remote state (S3, GCS, or equivalent) records every `apply` independently
  and immutably.
- `WrapTerraform` wraps the full `PLAN → APPLY → PROBE → DELETE` lifecycle and
  enforces action gating.
- Forensic recovery: inspect the remote state backend for the target
  `unique_name` and stage tier.

**Immutability guarantee:** config-generated tfvars (same epoch chain as resolved
conf) + remote state backend protocol.

---

### 2. Container Images (Docker / OCI)

**Epoch mechanism:** image tag = `{unique_name}--{git.commit}`.

- Image tags are composed in `workspace_wielder/core/image_identity.py` from
  `unique_name` and the git commit SHA.
- Once a tag is pushed to the registry, the registry treats it as immutable
  unless explicitly force-pushed.
- `pack_image_antifragile` in `Wielder` skips rebuild when the tag already
  exists in the registry (`skip_existing_registry_image=True` default).
- A dirty local tree affects the next build; the previously pushed tag is
  unchanged.
- Forensic recovery: pull the image by tag; the tag encodes the exact
  `unique_name` and commit.

**Immutability guarantee:** registry protocol + tag-existence skip logic.

**Note:** Content-addressing at the layer level is handled by the OCI registry
protocol internally. No application-level content hash is needed in the tag.

---

### 3. Resolved Configuration Snapshots

**Epoch mechanism:** one active state per `unique_name`, immutable forensic
trail keyed by `epoch_ms--git_short_sha--conf_short_sha`.

Resolved conf materializes the fully resolved PyHocon tree for a specific
`unique_name` at a specific moment, capturing transient overrides for ephemeral
super clusters, developer context packs, and hybrid topologies.

**Key structure:**
```
resolved_conf/{stage_tier}/{ecosystem}/{unique_name}/{app_name}/
  latest.conf                          ← always overwritten; the active state
  {epoch_ms}--{git_sha}--{conf_hash}.conf  ← immutable forensic record
```

- `latest.conf` is intentionally overwritten on every publish. There is
  **exactly one valid config per `unique_name`** at any time.
- The versioned key is content-addressed: `conf_hash` is a SHA-256 of the
  serialized HOCON payload, so any two distinct configuration states produce
  distinct keys.
- `conf_hash` in the versioned key is **not** about supporting multiple
  simultaneously active states — it makes the forensic record uniquely
  addressable so any historical epoch can be exactly reconstructed.
- Pods bootstrap by fetching their config from the immutable versioned artifact
  in object storage, not from the local filesystem. A dirty local tree cannot
  affect a running pod.

**Immutability guarantee:** content-addressed versioned key (overwrite would
require the same HOCON payload hash, which means same content).

**Forensic recovery:** fetch the versioned key for the target
`unique_name`/`app_name`/`epoch_ms` from the conf bucket.

---

### 4. Python / Spark Code Bundles

**Epoch mechanism:** Wielder Artifactor/PySparker publishes configured code
bundles into a configured artifactory surface.

The artifact identity is the resolved artifact root plus a version derived from
the execution identity, normally `unique_name + git.commit`. The payload is a
published bundle manifest containing the entrypoint, py-files, archives, object
keys, object URIs, and content hashes.

**Source isolation contract:**

- Python/Spark code bundles must use existing Artifactor source kinds before
  adding new archive mechanics. For package directories, `artifact_kind = "zip"`
  already publishes the directory basename as the Python import root.
- Shared runtime bundles that span several repositories should usually use
  multiple configured `py_file_sources` under one artifact manifest, not a
  hand-built assembly archive.
- Spark entrypoint reuse should be handled through a generic runtime entrypoint
  plus module args, not by repacking the same package set for every job.
- Uncommitted source changes are not artifact truth. Commit the owning repo, then
  commit the super-repo pointer when the artifact version depends on the
  super-repo SHA.

For implementation detail, read
[Artifactory Guidelines](SKILL_ARTIFACTORY_GUIDELINES.md).

**Semantic distinction from resolved conf:** Spark artifacts are immutable code
bundles — they should never be sourced from uncontrolled local state. Resolved
conf `latest.conf` is intentionally derived from the live config resolver
because cluster configuration legitimately evolves within the epoch contract.

**Spark artifact storage contract:** PySpark code bundles must publish through a
configured artifactory surface, not through job-local constants or hard-coded
bucket names. The neutral Spark artifact contract should live in the project or
shared app baseline, and concrete cloud ecosystems should override only the
physical bucket/provider expression, for example an AWS `workspace-artifactory-*`
bucket. The bucket-relative key layout must remain stable across local and cloud
surfaces: if local materialization is `artifactory/spark/python/<job>/<version>/`,
then the cloud object key should be `spark/python/<job>/<version>/...` inside the
configured artifactory bucket. Application Spark jobs should reference that
shared contract, such as `${spark.artifacts}`, rather than redefining
`bucket`, `root_key`, or `version` in each job.

---

## Summary Table

| Artifact Class | Epoch Mechanism | Active State | Forensic Trail |
|---|---|---|---|
| Terraform infrastructure | Remote state backend | Backend state | Backend history |
| Container images | Tag = `unique_name + git.commit` | Registry tag | Tagged images in registry |
| Resolved conf | `latest.conf` + content-addressed versioned key | `latest.conf` (one per `unique_name`) | `epoch_ms--git_sha--conf_hash` versioned keys |
| Python/Spark bundles | Artifactor bundle + artifact manifest | Latest published bundle | All prior bundles at their versioned keys |

---

## Anti-Patterns

- **Mutable version strings without content addressing:** `version = "local"`
  or any static string as the sole key component for a code artifact. A
  republish will silently overwrite with different content.
- **Python-level epoch gates:** do not add runtime Python checks that try to
  detect dirty trees or enforce epoch compliance at execution time. Enforce it
  structurally at the publication layer.
- **Conflating artifact classes:** resolved conf, container images, and code
  bundles have different mutability semantics. Do not generalize their epoch
  mechanisms into one abstraction.
- **Content hash in the image tag:** unnecessary. The OCI registry handles
  content addressing internally. The tag's purpose is human-readable identity
  (`unique_name + commit`), not content deduplication.
- **Custom worktree packagers:** do not use recursive globbing, local ignore
  rules, ad hoc `zipfile` writers, stale staging clones, or Docker image
  extraction to publish Python/Spark code bundles. Use existing Artifactor
  source kinds through the configured artifactory surface.
