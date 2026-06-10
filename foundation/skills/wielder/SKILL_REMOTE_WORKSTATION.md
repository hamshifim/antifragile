---
name: Remote Workstation
description: Use when planning, operating, documenting, or handing off work for a configured remote Ubuntu workstation, especially when translating paths, clones, shells, browser access, or Codex/agent workflows between a local laptop/WSL surface and a remote development surface.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Remote Workstation

A remote workstation is a configured Ubuntu control-plane and secure web server
surface. It can operate Wielder workflows from a full Linux desktop, bridge
local/hybrid/cloud ecosystems, and host browser-facing operator surfaces when a
workflow needs a secure workstation-adjacent web server.

Remote workstation access should be owned by the project-specific access helper
and resolved configuration. The generic Wielder doctrine should describe the
shape of the handoff, not expose a project-local workstation name or provider
tunnel mechanics.

## Path Contract

When discussing or scripting remote workstation work, speak from the remote
operator home by default:

- Use `~/work/workspace` for the mutable development checkout.
- Use `~/prod/workspace` for the production-adjacent or clean runtime checkout.
- Use `~/...` in prompts and handoffs unless an absolute path is required by a
  concrete command running on a known machine.

Never transpose the current WSL or laptop path into remote-workstation
instructions. If a path appears in an operator handoff, label the machine
context:

- `local: ~/work/workspace`
- `remote dev: ~/work/workspace`
- `remote prod: ~/prod/workspace`

## Workspace Roles

- `~/work/workspace`: mutable developer workspace. Use for active development and
  local iteration.
- `~/prod/workspace`: clean production-adjacent workspace. Use for running or
  exposing a service from a branch cloned from GitHub.
- `~/stage/...`: Wielder-staged materialization area. Treat staged clones as
  runtime/build inputs, not the human source checkout.

Do not run a production-facing site from a dirty dev checkout. Clone the
intended GitHub branch into the prod workspace and make coordinated branches
there when deployment plumbing needs source changes.

## Init Tooling

Remote workstation init should reuse the generic Ubuntu bootstrapper for reusable
developer and model-artifact tools such as `rclone`, `zstd`, the Hugging Face
`hf` CLI, and Ollama when the bootstrapper's `model-artifact-tools` phase is
selected or included by default.

Do not make remote workstation init fetch concrete model weights. Concrete model
materialize steps belong to the app provision surface and should be idempotent
against an existing nonempty local cache. See
[Model Artifact Provisioning](SKILL_MODEL_ARTIFACT_PROVISIONING.md).

## Prompt And Handoff Rules

- Prefer home-relative paths in remote workstation prompts.
- State whether the command is meant for the local surface, remote dev, remote
  prod, or a staged Wielder clone.
- Do not ask another Codex thread to use absolute paths copied from the current
  session unless those paths were verified on that same machine.
- If two agents are active, do not edit the same site/source surface from both.
  Use the prod clone for run/exposure plumbing and leave the dev clone for the
  thread doing feature work.

## Secure Site Planning

For remote-workstation-run site exposure:

1. Keep the current dev repo as the development workspace.
2. Clone the GitHub branch into `~/prod/workspace`.
3. Create a coordinated submodule/super-repo branch only in the prod clone.
4. Use Wielder configuration and hybrid ecosystem surfaces for plan/apply rather
   than ad hoc path or environment overrides.
5. Treat DNS, TLS, load balancers, auth, and public exposure as durable substrate
   with explicit ownership and delete semantics.
