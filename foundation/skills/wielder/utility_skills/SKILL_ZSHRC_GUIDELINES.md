---
name: zshrc-guidelines
description: Wielder zshrc and shell startup guidelines for project-local uvenv activation, VSCode terminal isolation, prompt labels, and preventing global .zshrc defaults from leaking between workspaces. Use when editing workstation .zshrc templates, Wielder/useful/zshrc_example, VSCode terminal environment, or debugging wrong Python/venv prompt in zsh.
---


# Zshrc Guidelines

Use this skill when creating, repairing, or reviewing zsh startup behavior for
Wielder workspaces, especially when VSCode terminals or global shell defaults
activate the wrong Python environment.

## Reference Files

- Generic Wielder example: `Wielder/useful/zshrc_example`.
- Starget workstation example: `starget-wielder/conf/workstation/.zshrc`.
- Culture currently consumes the generic Wielder example from
  `/home/gideon/dev/culture/Wielder/useful/zshrc_example`.

Read the relevant file before changing shell startup behavior.

## Core Rules

- Project-local shell routing beats global defaults. If `PWD` is inside a
  workspace root, that workspace's intended `.venv` must win regardless of
  inherited `UVENV_DEFAULT_NAME`, `UVENV_DEFAULT_VENV`, `UVENV_ACTIVE_NAME`, or
  `VIRTUAL_ENV` from another project.
- VSCode workspace settings should still set `python.defaultInterpreterPath`,
  `python.pythonPath`, `UVENV_DEFAULT_NAME`, and `UVENV_DEFAULT_VENV`; zshrc
  should respect those values unless the current path proves the shell is inside
  a different workspace.
- Never place a late unconditional export such as
  `UVENV_DEFAULT_VENV=/home/.../culture12` in global `.zshrc`. Scope it by
  `PWD`, or it will leak into other VSCode windows.
- When available, source `Wielder/wielder/scripts/uvenv.sh` and activate the
  concrete venv path. Fall back to direct `source <venv>/bin/activate` only
  when the helper is unavailable.
- Keep `PYSPARK_PYTHON` aligned with the active project venv.
- Prompt labels should derive from `UVENV_ACTIVE_NAME` or `VIRTUAL_ENV_PROMPT`,
  but interpreter correctness is more important than the label.

## Validation

For a Starget-style workspace, validate the contamination case:

```bash
cd /home/gideon/work/starget
env UVENV_DEFAULT_NAME=culture12 \
  UVENV_DEFAULT_VENV=/home/gideon/.uvenvs/culture12 \
  zsh -ic printenv | grep -E '^(UVENV_DEFAULT_NAME|UVENV_DEFAULT_VENV|UVENV_ACTIVE_NAME|VIRTUAL_ENV|PYSPARK_PYTHON)='
env UVENV_DEFAULT_NAME=culture12 \
  UVENV_DEFAULT_VENV=/home/gideon/.uvenvs/culture12 \
  zsh -ic 'command -v python'
```

Expected result: all active/default venv values and `python` resolve to the
Starget workspace `.venv`.

For a Culture-style workspace, run the inverse test from `/home/gideon/dev/culture`
and expect Culture's configured venv to win.

## Anti-Patterns

- Trusting a global `.zshrc` default more than the current workspace path.
- Fixing only the prompt text while `command -v python` still points to the
  wrong project.
- Editing local `~/.zshrc` without also updating the versioned example that will
  regenerate it later.
- Allowing direct activation to preserve an inherited `UVENV_ACTIVE_NAME` from a
  different project.
