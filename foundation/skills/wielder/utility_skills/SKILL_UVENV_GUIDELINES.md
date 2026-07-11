---
name: uvenv-guidelines
description: Wielder uvenv environment guidelines for uv-managed workspace Python, shell activation, VSCode interpreter binding, and avoiding accidental inheritance from another active virtualenv.
---


# Uvenv Guidelines

[Use Agent Uvenv Accessibility](SKILL_AGENT_UVENV_ACCESSIBILITY.md) when an
agent needs a scoped uvenv invocation for internal validation while preserving
clean operator handoffs.

Use this skill when creating, repairing, reviewing, or documenting Wielder `uvenv`
behavior: workspace `.venv` creation, shell activation, VSCode/Pyright binding,
package scripts, or bugs where one workspace accidentally inherits another
active virtual environment.

## Core Contract

`uvenv` is the Wielder helper layer over `uv` virtual environments. A workspace
should declare its intended Python environment explicitly, then make shells,
editors, package scripts, and launchers converge on that environment.

The default environment for a workspace should come from workspace-owned state.
The source of truth for clone-specific choices is the transient, unversioned
workspace `.env`; package/bootstrap scripts read it and then render shell/editor
bindings from it.

- `WORKSPACE_VENV_PATH` in the transient `.env` for the concrete virtualenv
  path, for example `$HOME/.uvenvs/culture` or `$HOME/.uvenvs/msa`.
- `WORKSPACE_UVENV_NAME` or a project-local default name, such as `starget`.
- `UVENV_DEFAULT_VENV` and `UVENV_DEFAULT_NAME` exported from package/bootstrap
  scripts and editor terminal environment.
- `.vscode/settings.json` and `pyrightconfig.json` rendered to the same
  interpreter path.
- The workspace `.venv` path is the stable IDE/tool handle, not the source of
  truth. It should be a symlink to the `.env`-configured
  `WORKSPACE_VENV_PATH` when the concrete uvenv lives outside the workspace.
- The project virtualenv prompt/metadata should use the workspace environment
  name, even when the concrete directory is `.venv`. For example, Starget's
  `/home/gideon/work/starget/.venv` should present as `starget`, not `.venv`.
- Clone-specific workspaces should keep `.venv` as a symlink to the configured
  named uvenv when the uvenv is outside the clone. For example, a Pan MSA clone
  may use
  `/home/gideon/pan_msa/culture/.venv -> /home/gideon/.uvenvs/msa`. This keeps
  VSCode/Pyright anchored on `${workspaceFolder}/.venv/bin/python` while zsh,
  package scripts, and agent shells activate the target declared in transient
  `.env`.

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
- Package scripts should refresh `<workspace>/.venv` as a symlink to
  `WORKSPACE_VENV_PATH` after loading transient `.env`. This is the preferred
  way to let each clone choose a different named uvenv while keeping tracked
  VSCode and Pyright settings anchored on `${workspaceFolder}/.venv`.
- Do not rely on VSCode `${env:WORKSPACE_VENV_PATH}` interpolation unless that
  variable is exported into the VSCode process itself. A repository `.env` is
  not automatically an interpolation source for VSCode settings.
- Make VSCode integrated terminals set `UVENV_DEFAULT_NAME`,
  `UVENV_DEFAULT_VENV`, `UVENV_HOME`, and `VIRTUAL_ENV_DISABLE_PROMPT` so editor
  shells resolve the intended workspace environment even when the user's normal
  `.zshrc` points somewhere else.
- User shell profiles should be owned by the canonical workstation installer,
  not by an ad-hoc task clone. It is acceptable for the workstation shell to
  activate the canonical Culture uvenv globally. Do not let a branch/task clone,
  such as Pan MSA, rewrite `.zshrc` so every terminal activates that clone's
  special uvenv. Special clones should use their transient `.env`, clone-local
  `.venv` symlink, VSCode terminal settings, or explicit `uvenv activate`.
- If direct `source <venv>/bin/activate` is part of the supported workflow,
  keep `pyvenv.cfg` and the activation script prompt binding aligned with
  `UVENV_DEFAULT_NAME`.
- Prefer `uvenv activate <path>` or `uvenv activate <name>` over direct
  `source <venv>/bin/activate` when the helper is available.

## Validation

For a workspace at `/path/to/workspace`, validate the contract with the stable
workspace `.venv` handle. If `.venv` is a symlink, it should resolve to the
intended named uvenv:

```bash
cd /path/to/workspace
bash -n package_py.sh
test -e .venv && readlink -f .venv
.venv/bin/python -m json.tool .vscode/settings.json >/dev/null
.venv/bin/python -m json.tool pyrightconfig.json >/dev/null
UVENV_DEFAULT_NAME=<name> \
UVENV_DEFAULT_VENV=/path/to/workspace/.venv \
UVENV_HOME="$HOME/.uvenvs" \
zsh -lc 'source /path/to/workspace/Wielder/wielder/scripts/uvenv.sh && uvenv path <name> && uvenv path'
```

Both `uvenv path <name>` and bare `uvenv path` should resolve to the intended
workspace `.venv` target.

## Anti-Patterns

- Rendering VSCode to one interpreter while integrated terminals activate
  another.
- Using the caller's active `VIRTUAL_ENV` as the package script target by
  default.
- Putting workspace-specific defaults only in a personal `.zshrc` instead of
  versioned package/editor configuration.
- Adding Python `sys.path` hacks to compensate for the wrong active
  environment.
