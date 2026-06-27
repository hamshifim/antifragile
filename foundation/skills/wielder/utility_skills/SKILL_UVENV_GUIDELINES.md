---
name: uvenv-guidelines
description: Wielder uvenv environment guidelines for uv-managed workspace Python, shell activation, VSCode interpreter binding, and avoiding accidental inheritance from another active virtualenv.
---


# Uvenv Guidelines

Use this skill when creating, repairing, reviewing, or documenting Wielder `uvenv`
behavior: workspace `.venv` creation, shell activation, VSCode/Pyright binding,
package scripts, or bugs where one workspace accidentally inherits another
active virtual environment.

## Core Contract

`uvenv` is the Wielder helper layer over `uv` virtual environments. A workspace
should declare its intended Python environment explicitly, then make shells,
editors, package scripts, and launchers converge on that environment.

The default environment for a workspace should come from workspace-owned state:

- `WORKSPACE_VENV_PATH` for the concrete virtualenv path, normally
  `<workspace>/.venv`.
- `WORKSPACE_UVENV_NAME` or a project-local default name, such as `starget`.
- `UVENV_DEFAULT_VENV` and `UVENV_DEFAULT_NAME` exported from package/bootstrap
  scripts and editor terminal environment.
- `.vscode/settings.json` and `pyrightconfig.json` rendered to the same
  interpreter path.
- The project virtualenv prompt/metadata should use the workspace environment
  name, even when the concrete directory is `.venv`. For example, Starget's
  `/home/gideon/work/starget/.venv` should present as `starget`, not `.venv`.

Do not let an unrelated inherited `VIRTUAL_ENV`, `UVENV_ACTIVE_NAME`, `.zshrc`
default, or global shell profile silently select the interpreter for a
workspace-specific package or editor session.

## Routing Rules

- Use `Wielder/wielder/scripts/uvenv.sh` as the runtime helper. Do not re-create
  activation, name resolution, or `uv venv` creation logic in app-local scripts.
- Use `Wielder/wielder/scripts/install_ubuntu.md` as the detailed installation
  reference for workstation shell blocks, `.venv` creation, and editor binding.
- Keep project package scripts deterministic: choose the workspace environment,
  export `UVENV_DEFAULT_*`, activate that environment, then render IDE config.
- Make VSCode integrated terminals set `UVENV_DEFAULT_NAME`,
  `UVENV_DEFAULT_VENV`, `UVENV_HOME`, and `VIRTUAL_ENV_DISABLE_PROMPT` so editor
  shells resolve the intended workspace environment even when the user's normal
  `.zshrc` points somewhere else.
- If direct `source <venv>/bin/activate` is part of the supported workflow,
  keep `pyvenv.cfg` and the activation script prompt binding aligned with
  `UVENV_DEFAULT_NAME`.
- Prefer `uvenv activate <path>` or `uvenv activate <name>` over direct
  `source <venv>/bin/activate` when the helper is available.

## Validation

For a workspace at `/path/to/workspace` with intended environment
`/path/to/workspace/.venv`, validate the contract with:

```bash
cd /path/to/workspace
bash -n package_py.sh
.venv/bin/python -m json.tool .vscode/settings.json >/dev/null
.venv/bin/python -m json.tool pyrightconfig.json >/dev/null
UVENV_DEFAULT_NAME=<name> \
UVENV_DEFAULT_VENV=/path/to/workspace/.venv \
UVENV_HOME="$HOME/.uvenvs" \
zsh -lc 'source /path/to/workspace/Wielder/wielder/scripts/uvenv.sh && uvenv path <name> && uvenv path'
```

Both `uvenv path <name>` and bare `uvenv path` should resolve to the intended
workspace `.venv`.

## Anti-Patterns

- Rendering VSCode to one interpreter while integrated terminals activate
  another.
- Using the caller's active `VIRTUAL_ENV` as the package script target by
  default.
- Putting workspace-specific defaults only in a personal `.zshrc` instead of
  versioned package/editor configuration.
- Adding Python `sys.path` hacks to compensate for the wrong active
  environment.
