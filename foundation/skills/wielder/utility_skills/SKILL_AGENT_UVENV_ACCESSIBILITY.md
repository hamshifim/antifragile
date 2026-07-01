---
name: agent-uvenv-accessibility
description: Agent-only uvenv access rules for Wielder/Culture workspaces. Use when Codex needs to run internal validation, py_compile, pytest, or executable Wielder scripts from a non-interactive shell while keeping operator handoffs free of interpreter paths, activation rituals, and environment-variable leakage.
---

# Agent Uvenv Accessibility

Use this skill when an agent needs the project Python environment to inspect,
compile, test, or smoke-check Wielder entrypoints from a non-interactive shell.
It is not an operator handoff skill.

## Core Rule

Agents may adapt their own shell environment to reach the configured uvenv, but
must not promote that adaptation into operator-facing commands, `wield_docs/`,
handoffs, or user runbooks.

Operator commands stay in Wielder handoff shape: executable script path or
installed CLI, no `python`, no `python -m`, no activation, no env-var prelude.

## Agent-Internal Invocation

When the non-interactive agent shell cannot resolve project packages through the
shebang interpreter, prefer a scoped `PATH` prefix for the single command:

```bash
PATH=$HOME/.uvenvs/<name>/bin:$PATH <absolute-entrypoint> -es <ecosystem> -w plan
```

For Culture workspace work, `<name>` is usually `culture`.

Use direct interpreter paths only for agent-internal checks that are not
operator Wielder entrypoints, such as:

```bash
$HOME/.uvenvs/culture/bin/python -m py_compile <file.py>
$HOME/.uvenvs/culture/bin/python -m pytest <test-file> -q
```

When reporting those checks, rewrite them into operator form when they become a
handoff:

- `pytest $HOME/dev/culture/<repo>/tests/<suite> -q`
- `$HOME/dev/culture/<repo>/src/<pkg>/deploy/apps/<app>/wield/<entrypoint>.py -es <ecosystem> -w plan`

## Documentation Boundary

Before updating `wield_docs/` or a final handoff, check:

- No pasteable command starts with `python`, `python -m`, `uv run`, `source`, or
  `$HOME/.uvenvs/.../bin/python`.
- No pasteable command starts with `PATH=...`; that is an agent diagnostic
  convenience, not an operator surface.
- No pasteable command hardcodes `/home/<user>/...`; use `$HOME/...`.
- Every documented script path has a shebang and executable bit.

If a direct script fails because it is not executable, fix the script boundary.
If it fails only because the agent shell lacks the uvenv on `PATH`, use the
scoped `PATH` prefix internally and keep the operator command clean.

## Anti-Patterns

- Adding `$HOME/.uvenvs/culture/bin/python` to `wield_docs/` to compensate for
  the agent's non-interactive shell.
- Replacing an installed CLI or executable Wielder script with its Python source
  path plus an interpreter.
- Making a transient agent `PATH` prefix part of a durable handoff.
- Creating Python `sys.path` patches because the agent shell did not use the
  intended uvenv.
