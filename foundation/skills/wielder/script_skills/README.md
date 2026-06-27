# Wielder Script Skills

This directory groups Wielder scripting and operator handoff doctrine. Keep
entrypoint shape, service deploy surfaces, durable operator docs, and human-run
command rules here. Keep configuration ownership rules in `../config_skills/`.

## Routing

- [Wielder Scripts](SKILL_WIELDER_SCRIPTS.md): central entrypoint doctrine for
  thin scripts, canonical config accessors, Wielder modes, action branching, and
  runtime boundaries.
- [Wielder Handoff](SKILL_WIELDER_HANDOFF.md): operator command shape, plan/apply
  reporting, config-owned intent, and runtime-boundary handoffs.
- [Wield Documentation](SKILL_WIELD_DOCUMENTATION.md): project `wield_docs/`
  trees, durable command pages, and test handoffs.
- [Service Deployment Guidelines](SKILL_SERVICE_DEPLOYMENT_GUIDELINES.md):
  service-named image/deploy/spec entrypoints, hosted runtime locks, and command
  shape.
- [WJobBard Guidelines](SKILL_WJOBBARD_GUIDELINES.md): scheduled or
  event-triggered job semantics, lifecycle events, and payload target contracts.
- [Local Hybrid Dev Workflow](SKILL_LOCAL_HYBRID_DEV_WORKFLOW.md): local
  service iteration against full or remote provider-backed ecosystems.
