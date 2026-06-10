---
name: Security Versioning Gate
description: Required pre-commit security/versioning audit for reusable Wielder framework repositories and doctrine repositories before creating clean trunk baselines or framework commits.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Security Versioning Gate

Use this skill before committing to reusable framework repositories such as
`Wielder` and `wielder-antifragile`, especially when creating a clean trunk,
purging contaminated branches, or removing project/domain leakage from generic
code and doctrine.

## Contract

Reusable framework repositories must not learn project-private domain terms,
customer/source names, credential values, or app-specific runtime identities.
Project-specific vocabulary belongs in the owning project repositories and
project-local configuration, not in generic Wielder code, tests, examples, or
skills.

Before committing:

1. Run the reusable security/versioning script from `Wielder`.
2. Supply any task-specific forbidden literals or regular expressions from the
   ignored local audit context for the current cleanup.
3. Fix all findings or explicitly quarantine them into an ignored local report.
4. Record the command and result in the commit validation.

The script is intentionally generic. Do not hardcode project-specific forbidden
terms into the framework script or this skill. The forbidden vocabulary for a
cleanup is a local audit input.

## Command Shape

Run from any repository root:

```bash
/path/to/Wielder/wielder/scripts/security_versioning_check.py \
  --repo /path/to/repo \
  --expected-branch trunk1 \
  --forbidden-token '<literal>' \
  --forbidden-regex '<regex>'
```

Use repeated `--forbidden-token` and `--forbidden-regex` values for the local
audit set. Add `--require-clean` after committing when you want the gate to
prove there is no remaining dirty tree state.

## Branch Baseline Rule

For a clean trunk baseline:

1. Start from an already cleaned working tree.
2. Create the new trunk branch as an orphan or otherwise ancestry-free baseline
   when contaminated history must not be retained.
3. Run the security/versioning gate on the new branch before committing.
4. Commit the squashed clean tree with provenance and validation.
5. Push the clean trunk branch.
6. Delete only branches that have been explicitly classified as contaminated
   and whose required content is represented in the clean trunk.

Do not delete default or protected remote branches until repository governance
has moved the default branch to the clean trunk or explicitly approved the
deletion.

## Commit Message

Security cleanup commits should include:

```text
Agent-Commit: yes
Agent-Platform: OpenAI Codex
Agent-Audit: security versioning gate plus diff/status review
Validation: <exact security_versioning_check command>; <tests>
Risk: <known residual risk>
```
