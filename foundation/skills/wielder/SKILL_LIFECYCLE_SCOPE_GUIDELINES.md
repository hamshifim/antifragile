---
name: lifecycle-scope-guidelines
description: Wielder doctrine for assigning configuration and provisioning lifecycle ownership across project, ecosystem, app, context, and test scopes. Use when deciding where durable resources, ephemeral resources, app defaults, operator-local values, or test fixtures belong, especially before adding Terraform modules, HOCON leaves, delete gates, or plan/apply behavior.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Lifecycle Scope Guidelines

Use this skill when a Wielder change asks: "Who owns this thing's lifecycle?"
The answer should be explicit before adding config, Terraform, Python branches,
delete behavior, or operator instructions.

## Scope Ladder

Classify the resource or behavior by lifecycle, not by the file you happened to
touch first.

1. **Project scope**
   - Owns durable resources shared across ecosystems, apps, or operators.
   - Examples: Terraform state buckets, shared artifact registries, org/project
     IAM groups, common audit/log buckets, stable DNS zones, reusable secrets
     containers, and project-wide provider defaults.
   - Project-scoped resources must not be destroyed by app or personal
     workstation lifecycles unless an explicit project-level destroy profile
     opts in.

2. **Ecosystem scope**
   - Owns runtime topology and resource phenotype.
   - Examples: local vs cloud surface, provider region/zone, service transport
     mode, selected provision bundles, durable-kernel vs ephemeral-runtime
     overlays, autoscaling shape, and concrete bootability facts.
   - Ecosystem overlays may select project resources, but should not silently
     own their deletion.

3. **App scope**
   - Owns the executable contract and fail-closed defaults for one managed app.
   - Examples: required config schema, default disabled feature gates, app-local
     ports, job inputs, service names, and validation knobs that describe what
     the app needs to run.
   - Apps should not create shared durable substrate at runtime. If an app needs
     a bucket, topic, secret, or registry, it should consume a resolved contract
     or select a configured provisioning bundle.

4. **Context scope**
   - Owns operator-local or workstation-local transient intent.
   - Examples: current user identity, local machine paths, personal PAN
     instance identity, local secret references, temporary branch choices, and
     generated `ephemeral.conf` payloads.
   - Context packs may modulate a lifecycle, but they should not turn hidden
     defaults into durable project truth.

5. **Test scope**
   - Owns reduced pressure and fixture identity for verification.
   - Examples: CPU-only tiers, small disks, synthetic DAGs, short timeouts,
     expected sample inputs, and cleanup assertions.
   - Test overlays must not choose the operator action. `-t` selects fixtures;
     `-w` chooses `plan`, `apply`, `delete`, `run`, or another lifecycle verb.

## Ownership Tests

Before placing a config leaf or Terraform module, ask:

- **Who else uses it?** If several ecosystems or apps depend on it, prefer
  project scope or a reusable ecosystem concern.
- **Who may delete it?** If deletion would break another app, operator, stage,
  or future run, it is not app-ephemeral.
- **Does it define topology or execution?** Topology belongs in ecosystem scope;
  executable requirements belong in app scope.
- **Is it personal or generated?** Put operator-local facts in
  `context_conf/<name>/` or generated `ephemeral.conf`, not neutral defaults.
- **Is it only cheap enough for tests?** Put reduced pressure in `conf/test/...`
  or an explicit transient context, not in app defaults.

## Provisioning Rules

- `plan` should reveal the lifecycle boundary: project resources, ecosystem
  bundles, app modules, preserved resources, and destructive gates.
- `apply` may create prerequisites only when the selected scope owns them or
  has a configured dependency on an earlier owning bundle.
- `delete` and `plan-delete` must preserve broader-scope resources by default.
  Destroying a project-scoped resource requires an explicit project-level
  destroy profile.
- Backend state, shared registries, shared IAM, and common secret containers are
  project resources even when a personal workstation is the first user.
- Ephemeral clusters and personal workstations are ecosystem/app expressions
  that may depend on project resources; they do not own the project substrate.

## Common Mistakes

- Putting a shared backend bucket under a personal PAN lifecycle.
- Letting a workstation `delete` remove project IAM or backend state.
- Encoding provider/project facts in Python instead of resolved HOCON and a
  provider/factory surface.
- Adding app defaults for tiny test resources because the real workload is
  expensive.
- Using context packs as hidden mode defaults instead of explicit operator
  profiles.

## Repair Pattern

When a lifecycle boundary is wrong:

1. Move the durable fact to the smallest broader owning scope.
2. Let narrower scopes reference it through resolved HOCON.
3. Add separate provision and destroy gates.
4. Make `plan` print the boundary and pause cleanly if a prerequisite owner has
   not applied yet.
5. Validate through the canonical Wielder entrypoint rather than a side loader.
