---
description: Create and maintain Wielder operator documentation trees such as `wield_docs/`, with current-directory-agnostic handoffs, test handoffs, config-owned intent, and links to source tests and lifecycle docs.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.
[Use Wielder Handoff & Operator Command Reporting](SKILL_WIELDER_HANDOFF.md) for command formatting.
[Use Architectural Testing & Live QA Execution Protocols](SKILL_TEST_GUIDELINES.md) for test handoffs.
[Use Wielder Scripting & Evaluation Skills](SKILL_WIELDER_SCRIPTS.md) for executable entrypoint boundaries.

# Wield Documentation

Use this skill when creating or updating a project `wield_docs/` tree for
Wielder apps, workflows, third-party services, or installed CLIs.

## Goal

A `wield_docs/` tree is the operator continuation surface for a Wielder project.
It should be organized like an exploration index: compact folder-level pages,
one focused page per app or tool, and handoff commands that can be pasted from
any directory.

## Required Shape

Create a root `wield_docs/README.md` that lists the main operational families.
For each family, create a folder `README.md` and one page per app/tool.

Recommended families:

- `clis/` for installed tools such as `pan`, `merc`, and `nabu`.
- `third_party/` for Helm charts, external runtimes, and shared dependency
  standards.
- Domain folders such as `msa/`, `topological_predictions/`, `ingestion/`, or
  `runtime_stack/` for project-owned workflows.

## Page Contents

Each app/tool page should include:

- Scope: what the entrypoint owns and what it does not own.
- Shortcut boundary: for installed CLIs, state that the CLI is a Wielding
  endpoint shortcut that expands Wielder CLI/action/config semantics, and name
  the source entrypoint or app identity it wraps.
- Config ownership: the config family, app config, ecosystem, context pack, or
  test overlay that owns durable intent.
- Handoffs: exact plan/apply/delete/run/monitor commands in Wielder handoff
  shape.
- Test handoffs: exact `-t` commands or pytest commands when the app has a
  configured test surface.
- Expected evidence: output bucket keys, Kubernetes jobs, topics, reports, or
  files that prove the handoff did the intended work.
- Cautions: only risks that change the next operator decision.

## Command Rules

- Use installed CLI names for installed tools. Do not expose their Python
  internals.
- In each installed CLI page, explicitly say the CLI is a shortcut for a
  configured Wielder entrypoint. Show the source path or app identity in prose,
  while keeping handoff commands on the installed CLI.
- Use executable Wielder script paths rooted at `$HOME/dev/<workspace>/...` for
  project entrypoints.
- Do not require `cd`, virtualenv activation, `python`, `python -m`, shell
  aliases, or environment variables for normal handoff commands.
- If the documented script is not executable, fix the executable bit instead of
  documenting a wrapper command.
- Do not restate default Wielder modes unless they change intent.
- Put repeatable target identity in HOCON, not in bespoke CLI examples.

## Test Handoffs

Every page for a testable app should include at least one of:

- A Wielder lifecycle command with `-t`, for example:
  ```bash
  $HOME/dev/culture/<repo>/src/<pkg>/deploy/apps/<app>/wield/<entrypoint>.py -t -w plan
  ```
- A root-addressable pytest command, for example:
  ```bash
  pytest $HOME/dev/culture/<repo>/tests/<suite> -q -s
  ```

Use `-s` when the test intentionally emits a human-readable evidence report.

## Maintenance Loop

When an app, workflow, or CLI changes:

1. Run the lightest safe validation surface, usually `-w plan` or focused
   pytest.
2. Update the relevant `wield_docs/` page with the current command and expected
   evidence.
3. Remove stale commands, old bucket names, renamed ecosystems, and obsolete
   output paths.
4. If the change crosses a runtime boundary, document the image/build/apply
   action needed to make the change live.
5. Check that the page still obeys the handoff, testing, and scripting skills.

## Anti-Patterns

- A root README that lists apps but no pasteable handoff.
- A page that says "run the tests" without naming the test command.
- Commands that only work from the author's current directory.
- Python wrapper commands for scripts that should be executable.
- Test docs that omit `-t` even though the scenario lives in a test overlay.
- Duplicating large plan output instead of naming the command and expected
  evidence.
