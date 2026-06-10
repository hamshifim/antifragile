# Foundation Layout

This tree holds the semantic authored content for `wielder-antifragile`.

## Canonical Foundation Assets

- `docs/manifesto/`
  Antifragile, datalake, RND UI, and related manifesto material.
- `docs/catalogs/`
  Cross-cutting catalogs such as master persona, skill, and wieldable functionality indexes.
- `personas/wielder/`
  Canonical Wielder-base personas.
- `skills/wielder/`
  Canonical Wielder-base skills and skill guidelines.
- `workflows/`
  Multi-step execution workflows.
- `contracts/`
  Handoff and related structural contracts.

## Project-Scoped Material

- `playbooks/projects/ihc/`
  IHC-specific backlog, task, and supporting architecture documents.

These are intentionally separated from the canonical base doctrine so project material can inherit from the foundation without being mistaken for the foundation itself.

## Local Context Workflow

When projects need local developer or agent context packs:

- track examples in `conf/context_conf_examples/<name>/`
- keep live local copies in `conf/context_conf/<name>/`
- do not track the live local copies

Sanctioned flow:

```bash
cp -r conf/context_conf_examples/default_conf conf/context_conf/default_conf
```
