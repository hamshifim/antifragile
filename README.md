# wielder-antifragile

`wielder-antifragile` is the doctrinal and governance layer for wielding complex distributed systems.
It defines how agentic work is structured, inherited, validated, and audited.

## What This Repo Is

- Canonical home for personas, skills, workflows, contracts, and playbooks.
- Source-truth semantic bundles (`*.hocon` + `body.md`) that resolve into auditable artifacts.
- Strict provenance and execution-identity policy for multi-agent environments.

## What This Repo Is Not

- It is not the runtime infra executor.
- It is not coupled to a single runtime implementation.

`Wielder` (the repo/toolkit) is one runtime implementation that can satisfy these contracts, alongside other provider/tooling stacks.

## Current Architectural Position (Phase 0)

- Keep adoption modular: projects consume `wielder-antifragile` as a submodule.
- Preserve flexible usage but enforce strict contracts.
- Use single-parent persona inheritance via `base`.
- Reject non-empty `extends` in persona resolution.
- Enforce explicit override allowlists and inherited `final` constraints.

## Execution Identity Contract

Execution identity is mandatory under `wielder_antifragile.execution_identity` and must include:

- `user_name`
- `provider`
- `agent_type`
- `agent_instance_id`
- `agent_name`
- `agent_version`
- `session_id`
- `run_id`
- `invoked_at_utc`

Canonical naming:

- `agent_name = <provider>_<agent_type>_<agent_instance_id>`
- Example: `openai_codex-cli_1`

Config loading fails explicitly if any required field is missing/empty or if `agent_name` does not match the canonical composition.

## Repository Map

```text
wielder-antifragile/
  conf/
  docs/
    antipatterns/
    ephemeral-super-cluster-wielder.md
    foundation-manifesto.md
    implementation-architecture.md
  foundation/
    personas/
    skills/
    workflows/
    contracts/
    playbooks/
  src/wielder_antifragile/
    core/
    personas/
  tests/
  .foundation_audit/
```

## Quick Validation

Run from `wielder-antifragile/`:

```bash
PYTHONPATH=src pytest -q tests
```

Smoke-check persona resolution:

```bash
PYTHONPATH=src python -c "from wielder_antifragile.personas.object import PersonaObject; print(PersonaObject.from_id('git_specialist').to_string())"
```

## Primary Docs

- [Foundation Manifesto](docs/foundation-manifesto.md)
- [Implementation Architecture](docs/implementation-architecture.md)
- [Ephemeral Super Cluster Architecture](docs/ephemeral-super-cluster-wielder.md)

## Local GPU Surface Heuristic

For local WSL development of GPU-bound services, strongly prefer `kind` as the default Kubernetes surface.

- `kind` plus direct `kind load docker-image` is usually the more stable local loop for large CUDA images.
- `k3d` adds a registry hop that may be acceptable for lightweight services or registry-realistic checks, but it is often the wrong default for image-heavy GPU iteration on WSL.
- The local failure mode to watch is storage churn and virtual disk expansion, not just scheduler CPU or memory pressure.

## Local Context Packs

Tracked example context packs belong in:

- `conf/context_conf_examples/<name>/`

Live local context packs belong in:

- `conf/context_conf/<name>/`

and should remain git-ignored.

The sanctioned workflow is:

```bash
cp -r conf/context_conf_examples/default_conf conf/context_conf/default_conf
```

Then edit the copied local files to match the developer or agent context.

## Markdown Index

### Root

- [README](README.md)

### Docs

- [Adversarial Messaging Protocol Plan](docs/adversarial-messaging-protocol-plan.md)
- [Ephemeral Super Cluster Wielder](docs/ephemeral-super-cluster-wielder.md)
- [Foundation Manifesto](docs/foundation-manifesto.md)
- [Implementation Architecture](docs/implementation-architecture.md)

### Antipatterns

- [Context Drift](docs/antipatterns/context-drift.md)
- [Hard-Stopping](docs/antipatterns/hard-stopping.md)
- [Known Codex Unwanted Tendencies](docs/antipatterns/known_codex_unwanted_tendancies_antipattern.md)
- [Mode Violation](docs/antipatterns/mode-violation.md)
- [Premature Execution](docs/antipatterns/premature-execution.md)
- [Style Drift](docs/antipatterns/style-drift.md)
- [Unilateral Bypass](docs/antipatterns/unilateral-bypass.md)

### Foundation

- [Foundation README](foundation/README.md)
- [Glossary](foundation/docs/GLOSSARY.md)
- [Master Personas](foundation/docs/catalogs/MASTER_PERSONAS.md)
- [Master Skills](foundation/docs/catalogs/MASTER_SKILLS.md)
- [The Antifragile Manifesto](foundation/docs/manifesto/THE_ANTIFRAGILE_MANIFESTO.md)
- [The Data Lake Manifesto](foundation/docs/manifesto/THE_DATALAKE_MANIFESTO.md)
- [RND UI Manifesto](foundation/docs/manifesto/RND_UI.md)

### Personas

- [Persona Planner](foundation/personas/wielder/PERSONA_PLANNER.md)
- [Persona Platform Developer](foundation/personas/wielder/PERSONA_PLATFORM_DEVELOPER.md)
- [Persona QA Architect](foundation/personas/wielder/PERSONA_QA_ARCHITECT.md)
- [Git Specialist README](foundation/personas/wielder/git_specialist/README.md)
- [Git Specialist Body](foundation/personas/wielder/git_specialist/body.md)
- [Wielder Core Body](foundation/personas/wielder/wielder_core/body.md)

### Skills

- [Agent Partner Communication](foundation/skills/wielder/SKILL_AGENT_PARTNER_COMMUNICATION.md)
- [Configuration Guidelines](foundation/skills/wielder/SKILL_CONFIGURATION_GUIDELINES.md)
- [Epoch Artifact Governance](foundation/skills/wielder/SKILL_EPOCH_ARTIFACT_GOVERNANCE.md)
- [Context Recovery Alignment](foundation/skills/wielder/SKILL_CONTEXT_RECOVERY_ALIGNMENT.md)
- [Ecosystem Guidelines](foundation/skills/wielder/SKILL_ECOSYSTEM_GUIDELINES.md)
- [Einstein Simplicity](foundation/skills/wielder/SKILL_EINSTEIN_SIMPLICITY.md)
- [Naming Guidelines](foundation/skills/wielder/SKILL_NAMING_GUIDELINES.md)
- [Package Guidelines](foundation/skills/wielder/SKILL_PACKAGE_GUIDELINES.md)
- [MCP Browser Bridge](foundation/skills/wielder/SKILL_MCP_BROWSER_BRIDGE.md)
- [Monday MCP](foundation/skills/wielder/SKILL_MONDAY_MCP.md)
- [Notebook Guidelines](foundation/skills/wielder/SKILL_NOTEBOOK_GUIDELINES.md)
- [Parcelling Guidelines](foundation/skills/wielder/SKILL_PARCELLING_GUIDELINES.md)
- [Scope Guidelines](foundation/skills/wielder/SKILL_SCOPE_GUIDELINES.md)
- [Test Guidelines](foundation/skills/wielder/SKILL_TEST_GUIDELINES.md)
- [Wielder Imager](foundation/skills/wielder/SKILL_WIELDER_IMAGER.md)
- [Wielder Scripts](foundation/skills/wielder/SKILL_WIELDER_SCRIPTS.md)
- [Yoda Council](foundation/skills/wielder/SKILL_YODA_COUNCIL.md)

### Contracts and Workflows

- [Skill Handoff Protocol](foundation/contracts/handoffs/SKILL_HANDOFF_PROTOCOL.md)
- [Agentic Adversarial Workflow](foundation/workflows/adversarial/AGENTIC_ADVERSARIAL_WORKFLOW.md)

### Rendered / Audit Artifacts

- [Git Specialist Resolved](.foundation_audit/rendered_markdown/personas/git_specialist_RESOLVED.md)
- [Pytest Cache README](.pytest_cache/README.md)

## Agentic Antipatterns

As autonomous orchestration scales, Wielder explicitly defends against mathematical regressions.
- [Context Drift (Fantasia Risk)](docs/antipatterns/context-drift.md): Structural defense against high-velocity scope hallucination.
- [Style Drift (The OOD Paradox)](docs/antipatterns/style-drift.md): Structural defense against agents unconsciously regressing idiosyncratic code towards training-set norms.
- [Hard-Stopping (The Security Straitjacket)](docs/antipatterns/hard-stopping.md): Structural critique of stunting agentic growth through permanent action bans instead of explicit skill wrappers.
- [Known Codex Unwanted Tendencies](docs/antipatterns/known_codex_unwanted_tendancies_antipattern.md): Practical review smells for gnostic CLIs, environment-variable side channels, and CLI override wrapping.
- [Premature-Execution (The Builder's Impulse)](docs/antipatterns/premature-execution.md): Structural defense against agents autonomously violating "plan-only" bounds upon artifact approval.
- [Unilateral Bypass (The Architect's Hubris)](docs/antipatterns/unilateral-bypass.md): Structural defense against agents deploying fundamental architectural bypasses or SDK mutations without pitching and securing human authorization.
