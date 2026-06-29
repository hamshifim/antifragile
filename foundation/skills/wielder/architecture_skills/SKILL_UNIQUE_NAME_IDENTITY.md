---
description: Wielder unique_name identity doctrine for runtime siloing, context-selected project identity, artifact/image epoch tags, Terraform/Spark/Kubernetes resource naming, and the boundary between operational identity and data lookup partitions.
---

# Unique Name Identity

`unique_name` is the resolved runtime identity for a Wielder execution surface.
It is not a display label, a convenience slug, or a substitute for data lineage.
It is the operational namespace that lets several runs, projects, workstations,
contexts, and clusters coexist without stepping on each other.

## Core Shape

Prefer a deterministic compound identity:

```hocon
unique_name = ${stage_tier}"--"${project}"--"${owner}"--"${ecosystem}"--"${slug}"--"${incremental_id}
```

Conceptually:

```text
<stage_tier>--<project>--<owner>--<ecosystem>--<slug>--<incremental_id>
```

Some durable surfaces may use a shorter sanctioned form such as:

```text
<stage_tier>--<project>--<ecosystem>--<incremental_id>
```

Use the project-sanctioned parser/validator for the active repo. Do not invent
a sibling format because one workflow has a special project name.

## Runtime Silo

Use `unique_name` to silo operational products:

- Terraform/OpenTofu backend state and plan roots.
- Kubernetes names, Helm release names, service labels, jobs, pods, and logs.
- Docker/OCI image tags and local image-loading identities.
- Python/Spark artifact bundles and staged Spark job payloads.
- Resolved config payload roots and `latest.conf` channels.
- Staged provision roots, cloned build sandboxes, local plans, and runtime
  materializations.
- Workflow run artifacts, event labels, and operator-visible evidence.

If a context changes the runtime namespace, it should do so by changing the
resolved `project`, `slug`, `owner`, or `incremental_id` inputs that compose
`unique_name`. Code should keep consuming the final resolved `unique_name`.

## Staging Roots

Callers must provide already-namespaced staging roots to generic Wielder
utilities. Utilities such as imagers, artifact publishers, and provisioners
should consume the resolved root they are given; they should not silently append
`unique_name` unless that is their explicit local contract.

For image build sandboxes, prefer:

```hocon
image_staging_root = ${stage_root}"/images/"${unique_name}
```

Then pass `image_staging_root` to the image utility. The utility may append the
image repository/name below that root, but the runtime namespace belongs in
config.

## Context-Selected Project Identity

A named context pack can intentionally choose a runtime project namespace:

```hocon
# context_conf/vona/developer.conf
project = "vona"
unique_name = ${stage_tier}"--"${project}"--"${owner}"--"${ecosystem}"--"${slug}"--"${incremental_id}
```

That is enough for runtime siloing when the resource, artifact, image, and
workflow code already keys from `unique_name`. Do not add Vona-specific Python
branches, environment variables, or CLI flags to recreate what `unique_name`
already provides.

Bucket names may also derive from the same `project` when the bucket contract
supports project-scoped buckets, for example `vona-biochem-dev`. Keep that as a
config expression, not a code branch.

## Runtime Identity vs Data Lineage

Keep these concepts distinct:

```text
project            = context/runtime namespace, for example "vona"
unique_name        = concrete execution namespace derived from project and run axes
project_partition  = table/query partition for fast data lookup
project_id         = project-input or campaign lineage, for example "vona_vdx111"
```

`project_partition` belongs in tables, harmonized rows, and lookup indexes. It
does not replace `unique_name` for provisioned resources. `project_id` preserves
the finer scientific or product lineage inside a broader project namespace.

## Epoch Tags

Images and code artifacts must include both the operational namespace and the
committed super-repo source identity.

Use:

```text
<unique_name>--<super_repo_git_short_sha>
```

Examples:

```text
dev--vona--gideon--hybrid-local--msa-smoke--0--391e2448
dev--biocontext--mmseq2--0--391e2448
```

The super-repo git SHA must come from the Wielder config boot path, normally
`conf.git.commit` and `conf.git.short_commit`. Do not pin `git.commit` or
`git.short_commit` in `developer.conf` to select an image or artifact. If an
operator must attach to a previous immutable artifact, model that as an
explicit image/artifact reference override or an intentional attach operation.

Artifact publishing must fail closed when `artifacts.version = "local"` and no
resolved super-repo git commit is available. A fallback like `--local` destroys
runtime provenance.

## Attach vs New Run

Reusing an existing `unique_name` is an attach operation. It intentionally
targets the same live resources, backend state, images, resolved config channel,
and artifact roots.

Use reuse only when the operator explicitly wants to attach to the same runtime
surface. Otherwise choose a new slug or increment `incremental_id`.

## Permanent Resource Exception

Do not hide stage-tier-permanent resources behind disposable developer
`unique_name` values. Shared DNS zones, long-lived certificates, stable front
doors, reusable registries, and other persistent shared resources need their own
durable stage or project identity and delete policy.

## Script Rules

- Scripts must read `unique_name` from resolved config through the canonical
  accessor.
- Scripts must not construct `unique_name` from command-line flags,
  environment variables, current directory names, local usernames, or ad hoc
  project strings.
- Plan/apply output should print `project`, `unique_name`, `git.short_commit`,
  and the derived image/artifact tag when the action provisions, stages, builds,
  or publishes runtime products.
- Child workflows should receive mode context through Wielder config
  propagation, not through hand-built `unique_name` ferrying.

## Anti-Patterns

- Adding a special-case project branch in Python when a named context pack can
  override `project`.
- Creating a second naming channel such as `vona_unique_name` or
  `artifact_namespace`.
- Building images with one identity and publishing Spark/Python artifacts under
  another.
- Using `project_partition` as the Kubernetes, Terraform, image, or artifact
  namespace.
- Reusing a `unique_name` accidentally because `incremental_id` was not
  changed.
- Printing or storing only a mutable name without the super-repo short hash for
  image or artifact products.

## Review Heuristic

Ask: "If this plan is applied twice from two contexts, will Terraform,
Kubernetes, images, Spark artifacts, resolved config, and materializations
collide?" If yes, fix the resolved `unique_name` inputs in config before adding
code.
