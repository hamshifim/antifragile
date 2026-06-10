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

**Intended epoch mechanism:** artifacts sourced from the Docker image, not from
the local filesystem.

**Current state (gap):** `artifactor.py:91` reads source files directly from
`repo_root / job_conf.entrypoint` — the live local filesystem. There is no
staging sandbox, no clean clone, and no snapshot step. Uncommitted dirty changes
are published to object storage as if they were committed code.

**Root cause:** the artifact publication path lacks the source isolation that
the other two mechanisms provide structurally:
- Docker images: `pack_image_antifragile` snapshots required modules into a
  UUID-isolated staging sandbox via `shutil.copytree` before `docker build` runs.
  Dirty files cannot enter the build context.
- Terraform: `config_to_terraform` generates tfvars from the resolved PyHocon
  config. Terraform never reads application Python source files.

**Intended fix:** adopt the same staging mechanism the imager uses.

`pack_image_antifragile` runs a staging step — cloning/copying the required
modules into a UUID-isolated directory under `conf.stage_root` — before
`docker build` runs. The epoch guarantee comes from that staging operation, not
from the image format. The artifact publication path must invoke the same
staging logic before reading source files.

The staging logic must be extracted into a shared callable so both the imager
and the artifact wield scripts can invoke it. The artifact wield calls the
shared staging utility, receives the path to the resulting clean staged clone,
and passes that as `repo_root` to `PySparkArtifactJob`. The caller cannot
assume a staged directory already exists or is current — it must trigger the
staging operation itself.

**Fix scope:** extract the staging utility from `pack_image_antifragile` into a
shared function; call it from `model_score_artifacts.py` and
`model_lookup_harmonization_artifacts.py` before constructing
`PySparkArtifactJob`. No changes to `artifactor.py`, `PythonArtifactBundleSpec`,
or the storage layout. See `artifact_fixing_stam.md` for the task detail.

**What this is not:** pointing `repo_root` at a pre-existing `conf.stage_root`
without running the staging step — the directory may be absent or stale.
Content-addressing the key — that labels dirty content reliably, which is the
wrong fix. Extracting from the image filesystem — the staged clone is what feeds
both the image build and artifact publish; the image is downstream of the
staging step, not the source.

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
| Python/Spark bundles | Artifacts extracted from Docker image (intended) | Latest published bundle | All prior bundles at their versioned keys |

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
