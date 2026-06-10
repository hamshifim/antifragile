---
description: Wielder-style operator handoffs with config-owned intent, root-safe absolute commands, plan/apply reporting, and clear separation between agent-internal validation and human-run commands.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Wielder Handoff & Operator Command Reporting

Use this skill when preparing a handoff, context-recovery note, operator command,
or final report for Wielder-managed work.

## Core Rule

A Wielder handoff is a reproducible continuation surface. It should carry the
minimum concrete context needed for the operator or next agent to continue
through canonical entrypoints, with operator intent owned by resolved config.

Do not hand off a loose shell ritual. Hand off:

- the app or workflow identity
- the config owner for transient intent
- the exact plan/apply/test commands
- the dirty or committed repo state that changes the next decision
- the validation already performed and the remaining risk

## Operator Command Shape

Commands shown to the operator must be root-safe and current-directory agnostic.

- Use absolute script paths rooted at the shared checkout, for example:
  ```bash
  <workspace>/workflow-wielder/src/workspace_wielder/deploy/apps/wgit_toolbox/wield/wgit_toolbox_branch_all_around.py -es wgit_toolbox -st dev -se org -dl standard -cn standard -cc default_conf -w plan
  ```
- Do not require a preceding `cd`.
- Do not prefix Wielder script handoffs with `python`, `python -m`, `uv run`,
  virtualenv activation, shell aliases, or environment-variable incantations.
- Assume the operator's uvenv/shell is already active unless the task is
  explicitly about workstation bootstrap.
- If a script cannot be run directly, fix the script boundary with a shebang and
  executable bit according to `SKILL_WIELDER_SCRIPTS.md`; do not normalize the
  bad boundary by handing off `python path/to/script.py`.

For tests, use `pytest` directly:

```bash
pytest <workspace>/Wielder/wielder/test/test_wgit_branch_all_around.py -q
```

Do not hand off `python -m pytest ...` unless the operator explicitly asks for
that form.

## Config-Owned Intent

Operator choices that need to be repeatable belong in resolved HOCON, usually
the active `context_conf/<name>/developer.conf` for transient local intent.

Examples:

- desired branch: `wgit.desired_branch`
- selected workflow batch payload: generated or included context payload
- reusable app identity: app or ecosystem config, not a CLI side channel
- session or auth timeout: owning app/ecosystem config, not an env var

If a required config leaf is missing, the entrypoint should fail closed with a
message that names the missing key and the expected context-pack location.

## Plan, Apply, And Delete Handoffs

Prefer `-w plan` as the handoff verification surface. It should inspect and
report state without mutating.

For plan:

- report dirty repos, missing config, missing remote branches, or unresolved
  cloud/Kubernetes context before proposing mutation
- include the exact next `-w apply` command only when the plan shape is clear
- do not hide plan failures behind code patches or speculative commands

For apply:

- fail closed before mutation when preconditions are not met
- use the same canonical script path and Wielder modes as the plan
- for long-running applies, hand the command to the operator unless they
  explicitly ask the agent to run and wait

For delete:

- state exactly which resources are owned by the delete action and which are
  intentionally preserved by config
- do not imply durable infrastructure is protected unless the owning config or
  provider resource enforces that protection

## Runtime Boundary Handoffs

When a change crosses a runtime boundary, the handoff must include the matching
operator action. Do not report the source diff as if it were enough for the
operator to validate live behavior.

For Kubernetes-hosted code:

- If Python, frontend, image context, Dockerfile, dependency, or runtime config
  changes affect code that runs inside a Kubernetes pod, hand off the relevant
  image build command and the deploy/apply command.
- If only Terraform/Kubernetes manifest wiring changes, hand off the deploy/apply
  command and name whether an image rebuild is intentionally unnecessary.
- If a pod restart or rollout is required but no image rebuild is required,
  hand off the canonical Wielder deploy/apply command rather than a raw
  `kubectl rollout restart`, unless the task is explicitly a Kubernetes
  emergency workaround.

For Spark or EMR-running code:

- If Spark job code, artifact packaging, Spark dependency config, or table schema
  changes affect a job executed on Spark/EMR, hand off the artifact/build step
  and the exact Spark job Wielder apply/run command needed to exercise it.
- If the change only affects a local consumer of already-materialized Spark
  outputs, say that no Spark artifact rebuild is needed.
- Always state whether the operator should expect a long-running EMR job and
  whether credentials may expire during monitoring.

For local server/client loops:

- If local API server code or server config changes, hand off the stop/start
  command for that local server entrypoint.
- If local client code, Vite config, package scripts, or frontend state handling
  changes, hand off the local client restart command, or the combined local
  launcher command if one entrypoint starts both server and client.
- If both server and client are started by one configured Wielder entrypoint,
  prefer handing off that single entrypoint over separate `npm` and API commands.

For mixed local/AWS hybrid ecosystems:

- Keep local restart handoffs separate from AWS runtime build/apply handoffs.
  A local launcher restart validates workstation code; an image build/apply
  validates hosted Kubernetes code.
- When a local hybrid launcher targets AWS Kafka, EKS, S3, or EMR, include the
  bridge or monitor command only if the operator must start or verify that
  bridge for the next step.

## Inner Agent Usage

Agents may use internal validation commands while working, including direct
Python compilation, focused shell probes, git inspection, and other local checks.
Those internal commands are not automatically the operator handoff commands.

When reporting internal validation:

- summarize the result in prose
- include the command only if it helps reproduce the verification
- if it is a test, rewrite it in operator form using `pytest`
- if it is a Wielder script, rewrite it as an absolute executable script path
- if it is a one-off diagnostic command, label it as diagnostic rather than an
  operator runbook step

The operator-facing command block should stay clean enough to paste from any
directory.

## Reporting Shape

The operator does not see tool output. A handoff report must relay the important
facts from commands that were run.

Include:

- **Scope:** what this handoff is and is not trying to continue
- **Repo State:** branch, dirty state, relevant commits, and uncommitted files
- **Config Ownership:** which config pack or app/ecosystem config owns the next
  intent
- **Commands:** exact plan/apply/test commands in operator command shape
- **Validation:** checks already run, pass/fail status, and important output
- **Next Action:** one concrete continuation step
- **Caution:** only risks that change what the operator should do next

Keep it concise. Prefer one command block per action over prose that requires
the operator to reconstruct a command.

## Anti-Patterns

- Prepending `cd`, `source .venv/bin/activate`, `python`, `python -m`, or
  `uv run` to normal Wielder entrypoints in handoff commands.
- Creating bespoke CLI flags or env vars instead of adding config-owned intent.
- Reporting "tests passed" without naming the tests or materially summarizing
  failures.
- Treating plan output as decorative instead of as the first forensic report.
- Handing off a command that only works from the agent's current working
  directory.
