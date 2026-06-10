# Wielder Antifragile Implementation Architecture

## Scope
This document turns the foundation doctrine into an implementation plan for the `wielder-antifragile` repo.

It covers:

- repo layout
- runtime implementation versus doctrine boundaries
- Phase 0 submodule adoption
- semantic inheritance
- source-truth objects and audit rendering
- semantic config versus source-code separation

## Repository Boundary

### Runtime Implementations (e.g., Wielder)
If it executes infrastructure, resolves runtime config, emits downstream config artifacts, or captures runtime evidence, it belongs in a runtime implementation layer (for example `Wielder`).

Suggested `Wielder` layout:

```text
wielder/
  ecosystem/
  epoch/
  orchestrator/
  runtime/
    terraform/
    kubernetes/
    helm/
    storage/
  vcs/
  provenance/
  notebook/
  dag/
  util/
```

### `wielder-antifragile`
If it tells an agent how to think, critique, parcel, inherit, hand off, or govern repo workflows, it belongs in `wielder-antifragile` regardless of which runtime implementation is used.

That includes:

- personas
- skills
- workflows
- contracts
- playbooks
- inheritance schemas

## Repo Layout

```text
wielder-antifragile/
  docs/
    foundation-manifesto.md
    implementation-architecture.md
  foundation/
    personas/
    skills/
    workflows/
    contracts/
    playbooks/
    schemas/
    templates/
  src/
    wielder_antifragile/
      core/
      personas/
      skills/
      workflows/
      contracts/
      conf/
  .foundation_audit/
```

## Transitional State

The current foundation tree contains legacy flat markdown assets migrated from the earlier spec location.

That is acceptable for Phase 0.

The target state is bundle-based, not flat-file based. New work should use object bundles first, and legacy markdown files should be converted incrementally rather than in one destabilizing pass.

## Semantic Config vs Source Code

### Separation Rule
Separate them physically, but keep them path-aligned.

- `src/` contains wrappers, loaders, inheritance logic, validators, and renderers
- `foundation/` contains the semantic instances and authored content
- relative paths should coincide so resolution remains deterministic

### Path Coincidence Model

```text
src/wielder_antifragile/personas/
foundation/personas/

src/wielder_antifragile/skills/
foundation/skills/

src/wielder_antifragile/workflows/
foundation/workflows/

src/wielder_antifragile/contracts/
foundation/contracts/
```

The code side owns behavior. The foundation side owns authored semantic content.

### Object Bundle Convention
Each semantic object should live in its own directory bundle.

Example:

```text
foundation/personas/wielder/git_specialist/
  persona.hocon
  body.md
  examples/
  templates/
```

or:

```text
foundation/skills/wielder/git_specialist/
  skill.hocon
  body.md
  checklists/
  templates/
```

### Bundle Rules

- the semantic metadata file is the structural root
- `body.md` is the human-authored prose body
- both files together form the source bundle
- markdown is authored directly, not embedded into HOCON as a large string block
- audit markdown is rendered output, not hand-maintained source

### Metadata File Responsibilities

The metadata file should remain small and structural.

It should contain fields such as:

- `id`
- `kind`
- `base`
- `extends`
- `final`
- `prompt_body_file`
- tool and output contract references

It should not contain large prompt prose blocks.

### Body File Responsibilities

`body.md` should remain ergonomic for human writing and preserve markdown syntax highlighting in the IDE.

It should also be sectional rather than one undifferentiated essay. Prefer explicit headings such as:

- `## Mission`
- `## Priorities`
- `## Guardrails`
- `## Handoff Rules`

This keeps later section-aware composition possible without requiring arbitrary markdown merging from the beginning.

## Agentic Root Config
The repo should expose a central agentic config that defines the semantic roots and lets object wrappers inherit those roots declaratively.

Example shape:

```yaml
agentic:
  roots:
    foundation_root: ${project_root}/foundation
    personas_root: ${agentic.roots.foundation_root}/personas
    skills_root: ${agentic.roots.foundation_root}/skills
    workflows_root: ${agentic.roots.foundation_root}/workflows
    contracts_root: ${agentic.roots.foundation_root}/contracts
    playbooks_root: ${agentic.roots.foundation_root}/playbooks
  python:
    package_root: ${project_root}/src/wielder_antifragile
```

This should be the only legitimate origin for semantic object roots.

## Bundle Resolution and Audit Rendering

### Resolution Flow

For a persona bundle such as:

```text
foundation/personas/wielder/git_specialist/
  persona.hocon
  body.md
```

the wrapper resolution flow should be:

1. load `persona.hocon`
2. resolve `base` (and enforce that `extends` is empty in Phase 0)
3. validate structural inheritance and `final` constraints
4. load the local prose body from `prompt_body_file`
5. produce canonical resolved state with `to_dict()`
6. render human-readable output with `to_markdown()`
7. emit the audit bundle into `.foundation_audit/`

### Audit Tree

Suggested outputs:

```text
.foundation_audit/
  rendered_markdown/
    personas/
      git_specialist_RESOLVED.md
  resolved/
    personas/
      git_specialist_RESOLVED.json
  inheritance_chains/
    personas/
      git_specialist_CHAIN.json
```

### Rendered Markdown Header

Every rendered markdown file should include:

- object id
- kind
- source bundle path
- inheritance chain
- overridden fields
- final fields
- render timestamp
- resolved object hash or version

### Commit-Time Discipline

Rendering should not exist only as a pre-commit side effect.

Recommended modes:

- on-demand render during development
- pre-commit validation and render for discipline

This preserves fast iteration while still guaranteeing human-auditable snapshots before version control boundaries.

## Phase 0: Submodule Housing

### Objective
Situate the currently ignored and provisional specs, personas, and workflow documents inside `wielder-antifragile`, then consume that repo as a submodule from active projects.

### Deliverables

- create `wielder-antifragile`
- migrate current specs into `foundation/`
- define the baseline root config
- wire one project to consume the repo as a submodule
- verify project-specific extension without copying the entire foundation tree

### QA Handoff

- the repo loads foundation assets from the declared roots
- a consumer project can resolve a baseline persona or skill
- a consumer project can override one foundation asset
- invalid parent references fail explicitly

## Semantic Inheritance

### Principle
Inheritance should be semantic and structural, not markdown include chains.

Every persona or skill should declare:

- `id`
- `kind`
- `base`
- optional `extends`
- optional override operations

### Merge Semantics

- `base`
  Single primary parent
- `extends`
  Optional mixins (disabled in current Phase 0 implementation; must be empty)
- `override`
  Replace inherited field
- `append`
  Add to inherited list
- `prepend`
  Add before inherited list
- `remove`
  Remove inherited field or entry
- `final`
  Prevent downstream override

### Phase 0 Simplification Policy
To keep inheritance predictable while the object system stabilizes:

- only single-parent `base` inheritance is active
- `extends` mixins are rejected when non-empty
- persona overrides are restricted to an explicit allowlist
- inherited `final` fields are enforced before merge

### Persona Override Guidance
Allowed:

- priorities
- domain vocabulary
- scope notes
- escalation behavior

Usually not allowed:

- core safety doctrine
- provenance duties
- mandatory handoff requirements

### Skill Override Guidance
Allowed:

- tool bindings
- repo roots
- examples
- project checklists
- local output paths

Usually not allowed:

- evidence contracts
- required outputs
- mandatory validation steps marked `final`

## Source-of-Truth Object Model

### Rule
Markdown is not the source of truth. Structured objects are.

The object graph should back:

- personas
- skills
- workflows
- contracts

### Base Contract
Each wrapper should support:

- `resolve()`
- `validate()`
- `to_dict()`
- `to_string()`
- `to_markdown()`
- `write_markdown(output_root)`
- `write_snapshot(output_root)`
- `write_audit_bundle(output_root)`
- `get_inheritance_chain()`
- `get_final_fields()`

### Intent

- `to_dict()`
  Canonical machine state for hashing, diffing, and provenance
- `to_string()`
  Compact terminal representation
- `to_markdown()`
  Human-readable audit view
- `write_audit_bundle(output_root)`
  Emit rendered markdown, resolved snapshot, and inheritance metadata together

### Source-of-Truth Clarification

The semantic metadata file is the structural source of truth.

The markdown body is the human-authored content source.

The fully resolved object is produced only after wrapper resolution. The rendered audit markdown is a derived artifact, not an authored source.

## Human Audit Rendering

### Default Behavior
Rendered markdown should default into an ignored audit tree, not into tracked source directories.

Suggested tree:

```text
.foundation_audit/
  rendered_markdown/
    personas/
    skills/
    workflows/
    contracts/
  resolved/
  inheritance_chains/
  diffs/
```

### Required Header Metadata
Every rendered audit artifact should include:

- object id
- kind
- source repo
- inheritance chain
- overridden fields
- final fields
- render timestamp
- object hash or version
- execution identity envelope (`user_name`, `provider`, `agent_type`, `agent_instance_id`, `agent_name`, `agent_version`, `session_id`, `run_id`, `invoked_at_utc`)

### Execution Identity Contract
The configuration must define a strict multi-provider execution identity envelope under `wielder_antifragile.execution_identity`.

`agent_name` must be deterministic and equal:
- `<provider>_<agent_type>_<agent_instance_id>`
- example: `openai_codex-cli_1`

Validation must fail explicitly when any required field is missing/empty or when `agent_name` does not match the canonical pattern.

## Initial Object Resolution Flow

1. load base object bundle
2. load single `base` parent (reject non-empty `extends` in Phase 0)
3. apply structural merge rules
4. validate `final` constraints
5. emit canonical `to_dict()`
6. derive `to_string()` and `to_markdown()`
7. write the audit bundle

## Next Implementation Step
The next concrete step after this skeleton is to define one real object type end to end, preferably `persona`, including:

- bundle schema
- Python wrapper
- inheritance resolver
- markdown renderer
- audit-bundle writer
