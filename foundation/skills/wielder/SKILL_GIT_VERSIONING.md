---
name: Git Versioning Guidelines
description: Wielder doctrine for agent-created commits, super-repo/submodule version integrity, commit provenance, and adversarial pre-commit audit.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

> save commited not for use without refactoring

# Git Versioning Guidelines

Use this skill when an agent is asked to commit, prepare commit commands, audit version state, explain submodule versioning, or make image-bearing changes that depend on committed source.

## Core Principle

Git history is the forensic record of what was actually wielded. In a Wielder super-repo, the parent commit and submodule commits together define the rebuildable system state.

An agent-created commit must therefore disclose that it was agent-created, identify the platform that produced it, and record the audit and validation that made the commit defensible.

The super-repo is an index of selected module versions. Do not merge feature
branches into the super-repo as the normal promotion mechanism. Merge or
fast-forward inside the owning submodules, then make a new super-repo commit
that records the intended submodule pointers and any super-repo-owned files.
The super-repo commits pointers and itself; it does not perform the product
merge.

## Commit Permission

- Do not create commits unless the operator explicitly asks for a commit.
- Do not treat permission for code edits as permission for commits.
- Do not use destructive git commands such as `git reset --hard`, `git checkout --`, or broad cleans unless the operator explicitly asks for that exact operation.
- Work with dirty trees. Never revert user changes to make the commit easier.

## Coordinated Branch Parity

When working inside a Wielder super-repo on a named feature branch, the active
branch name is part of the version contract. Before agent-created commits,
pushes, image builds, or deploys, verify that every initialized task-relevant
submodule is checked out to the same coordinated branch as the super-repo unless
the operator explicitly declares a different branch mapping.

Required branch audit:

```bash
git branch --show-current
git submodule foreach --recursive 'git branch --show-current && git status --short'
```

If the super-repo branch is `feature/foo/bar`, prefer creating or checking out
`feature/foo/bar` inside each initialized submodule before committing there.
Do not strand task commits on sibling branches such as `feature/foo/main` while
the super-repo records `feature/foo/bar`; that creates ambiguous provenance and
remote push pressure on multiple feature heads.

Before resetting a toe-stepping local sibling branch back to its remote-tracking
origin, prove any local-only tip is preserved by the coordinated branch:

```bash
git -C <submodule> merge-base --is-ancestor <sibling-branch> <coordinated-branch>
```

Reset a local sibling branch with `git branch -f <sibling-branch>
origin/<sibling-branch>` only when the operator explicitly asks for local branch
cleanup and the ancestry check proves no unique commits would be lost. Do not
delete local or remote sibling branches unless the operator explicitly asks for
deletion. If the sibling branch has unique commits not preserved by the
coordinated branch, stop and report the repo, branch names, and commit subjects.

## Coordinated Branch Derivation Workflow

Use this workflow when the operator has merged a working branch into a coordinated
source branch, then wants a fresh sibling branch created all around from that
source branch.

Example intent:

- source branch: `feature/model_score/main`
- new branch: `feature/model_score/workstation1`

The source branch is the branch currently checked out across the super-repo and
initialized submodules. The desired new branch is explicit local operator intent
and belongs in the active context pack, normally:

```hocon
wgit {
  desired_branch = "feature/model_score/workstation1"
}
```

Required procedure:

1. Verify the whole repo family is clean before switching branches:
   ```bash
   git status --short --ignore-submodules=none
   git submodule foreach --recursive 'git branch --show-current && git status --short'
   ```

2. Fetch and check out the coordinated source branch in the super-repo and each
   initialized submodule. Fast-forward local source branches to their remote
   tracking refs. Do not reset or discard local work to make this pass.

3. Add or update `wgit.desired_branch` in the live ignored developer context.
   Do not create a one-off branch CLI flag or environment-variable side channel.

4. Run the project-owned WGit toolbox in plan mode. In Workspace, the operator
   command shape is:
   ```bash
   <workspace>/workflow-wielder/src/workspace_wielder/deploy/apps/wgit_toolbox/wield/wgit_toolbox_branch_all_around.py -es wgit_toolbox -st dev -se org -dl standard -cn standard -cc default_conf -w plan
   ```

   Plan must prove:
   - all worktrees are clean
   - every initialized repo is on the same source branch
   - every source branch is pushed and aligned with origin
   - the desired target branch does not already exist locally or remotely
   - super-repo source gitlinks match the source branch heads of submodules
   - branch and push commands are the intended no-track creation commands

5. Only after plan is clean, apply:
   ```bash
   <workspace>/workflow-wielder/src/workspace_wielder/deploy/apps/wgit_toolbox/wield/wgit_toolbox_branch_all_around.py -es wgit_toolbox -st dev -se org -dl standard -cn standard -cc default_conf -w apply
   ```

6. Report the resulting branch and remote tracking state for the super-repo and
   all initialized submodules.

The WGit toolbox is the convenience entrypoint. The reusable branch mechanics
belong in `Wielder`, while project-specific config resolution belongs in the
project-owned toolbox app.

## Pre-Commit Adversarial Audit

Before staging anything, perform and summarize an adversarial audit:

1. Inspect super-repo state:
   ```bash
   git status --short --ignore-submodules=none
   git diff --submodule=log --stat
   git submodule status --recursive
   ```

2. Inspect every dirty or task-relevant submodule separately:
   ```bash
   git -C <submodule> status --short
   git -C <submodule> diff --stat
   git -C <submodule> diff -- <task-relevant-paths>
   ```

3. Attack the commit scope:
   - Are any unrelated user edits being staged?
   - Are generated artifacts, secrets, credentials, local paths, screenshots, notebooks, or large data files being committed accidentally?
   - Are code, config, docs, tests, and workflow files in the correct owning repo?
   - Are unversioned or local config inputs intentionally excluded from git, or are they neglected runtime dependencies that must be promoted into versioned config, secret management, or explicit build-context overlays? Examples include `developer.conf`, local context packs, credential stubs, and workflow run config.
   - Does the commit include only the intended domain, app, ecosystem, or service?

4. Attack deploy provenance:
   - If a hosted runtime, Docker image, WJobBard, Kubernetes workload, or workflow depends on the change, is the owning submodule committed before image build or deploy?
   - Is the super-repo pointer committed after the submodule commit?
   - Does the image/deploy command resolve to the final super-repo SHA that captures the required submodule pointers?

5. Attack validation claims:
   - Were tests, plans, applies, runs, or monitors actually executed?
   - Are failed or skipped validations disclosed?
   - Is a workflow `plan` being mistaken for runtime proof?

## Staging Discipline

- Prefer path-specific `git add <path>` commands after the audit.
- Avoid `git add .` unless the audit proves every dirty file is intentional.
- Stage submodule contents from inside the submodule, then commit inside that submodule.
- Before committing inside a submodule, verify it is on a human-usable branch.
  Do not strand agent commits on detached HEAD unless the operator explicitly
  asks for a detached/pinned commit.
- Stage the super-repo submodule pointer only after the submodule commit exists.
- If multiple submodules changed, prefer one commit per submodule/domain unless the operator asks for a single coordinated commit set.

## Scoped Commit All Around

Use a scoped commit-all-around procedure when the operator asks to commit the work from the current task/thread across a Wielder super-repo and its submodules.

The base phrase "commit all around" means to add unstaged changes and commit
across the super-repo/submodule workspace. The default commit modulators make
that broad mechanical request smaller:

- `task scope`: stage and commit only changes belonging to the current
  task/thread.
- `provenance`: include the default agent-created commit metadata and, when
  applicable, the compact provenance report.
- `entire scope`: treat the whole currently dirty workspace as the intended
  commit scope, after audit.

Explicit modulators such as `no provenance` override only the named behavior.
They do not remove task scope, scoped staging, validation reporting, or honest
disclosure of intentionally uncommitted dirty work.

`Entire scope` overrides task scope, but it does not override ownership,
secret-safety, generated-artifact review, submodule branch sanity, or
provenance. When the operator says `commit all around entire scope`, audit all
dirty files and submodules, stage only what survives that audit, and report any
excluded dirty state.

This is not permission to commit every dirty file. It is a permission-gated chain that commits only the task-relevant changes inside their owning submodules, then commits the super-repo pointers to those new submodule SHAs.

Required procedure:

1. Confirm commit permission and scope.
   - Proceed only after the operator explicitly asks for a commit, or explicitly confirms a proposed scoped commit-all-around.
   - Name the intended task/thread scope in plain language before staging.
   - List included submodules and excluded dirty submodules/files.

2. Audit before staging.
   - Run the pre-commit adversarial audit from this skill at the super-repo and submodule levels.
   - Treat unrelated user edits, local config, generated artifacts, secrets, large data, notebooks, screenshots, and task-adjacent experiments as excluded by default.
   - If task and non-task edits are mixed in the same file and cannot be separated safely with path-specific or explicit patch staging, stop and ask.

3. Commit inside each owning submodule first.
   - For each included submodule, stage only task-scoped paths from inside that submodule.
   - Review `git -C <submodule> diff --cached --stat` and focused cached diffs before committing.
   - Create one submodule commit per owning domain/module unless the operator explicitly requests a different grouping.
   - Use the agent commit message contract in this skill and record validation, residual risk, and intentional leftovers.

4. Commit the super-repo pointer update last.
   - Return to the super-repo only after the included submodule commits exist.
   - Stage only the intended submodule gitlinks, `.gitmodules` when intentionally changed, and any explicit provenance artifact.
   - Review `git diff --cached --submodule=log --stat` and confirm it shows only the expected pointer movements.
   - Commit the super-repo with `Submodule: <name> <sha>` lines for every included submodule.

5. Report the chain.
   - Report each submodule commit SHA and the super-repo pointer commit SHA.
   - Report validation commands and outcomes.
   - Report dirty files intentionally left uncommitted.
   - If a follow-on build, image bake, deploy, run, or push should use the new state, name the final super-repo SHA as the source of truth.

Under the default modulators, the phrase "commit all around" should therefore
be executed as "complete the task-scoped submodule-to-supermodule commit chain
with provenance," not "stage everything everywhere."

## Super-Repo Commit Order

For image-bearing or deployment-bearing work, the correct sequence is:

1. Commit intentional changes inside each owning submodule.
2. Return to the super-repo and stage the changed submodule pointer.
3. Commit the super-repo pointer update.
4. Build, push, provision, deploy, or run using the final committed super-repo SHA.

Do not rely on uncommitted submodule source for hosted runtime behavior. Local editor state is not image truth.

When Wielder materializes images, Terraform, or artifacts from a `unique_name`
staging clone, the final super-repo commit is the runtime source of truth; the
dirty developer checkout is not. In that case, commit after local preflight,
mark live validation as pending, and run the plan/apply/build against that final
super-repo SHA.

## Tier Branch And Artifact Lock Promotion

Stage-tier branches are promotion channels, not runtime locks by themselves.
Use them to make human and CI/CD promotion legible, then resolve them into an
immutable artifact manifest before any operator-facing apply.

The promotion chain is:

1. Promote each owning submodule with the versioning procedure appropriate for
   the target tier, such as `dev`, `stage`, or `prod`.
2. Commit the super-repo pointer update on the corresponding stage-tier branch.
   That super-repo commit is the source truth for the tier at that moment.
3. Push the updated stage-tier branch only after the submodule and super-repo
   commits are coherent.
4. Immediately after the stage-tier branch is merged and pushed, CI/CD or an
   explicit image/artifact surface must materialize every runtime artifact for
   that exact super-repo SHA. Treat this as part of promotion completion, not a
   later optional cleanup step.
5. CI/CD publishes a version lock/manifest keyed by the stage tier and
   super-repo SHA.
6. Operator-facing deploy surfaces resolve the selected stage tier to that
   immutable manifest and apply only from the locked artifacts.

Do not announce a tier promotion as deployable merely because the branch was
merged or pushed. The promotion is incomplete until required images, configs,
manifests, packages, lookup/model/data artifacts, and other runtime refs are
packed or published and recorded in the lock.

The artifact materialization step must be prompt because the stage-tier branch
is now advertising a source state to humans and automation. If CI/CD cannot
pack all required artifacts for that SHA, fail the promotion visibly and leave
operator-facing apply blocked on the missing artifact classes.

The manifest should include the full runtime artifact set, not only container
images:

- super-repo SHA and submodule SHAs
- image digests or immutable image references
- resolved config artifact URI and config hash
- Wielder context/developer overlay hash when applicable
- Kubernetes, Helm, Terraform/OpenTofu, WJobBard, workflow, and DAG artifacts
- wheel/sdist/package refs and schema or contract versions
- Spark job packages, lookup tables, model weights, database/index refs, and
  other data artifacts required by the workload

If any required artifact is missing for the promoted source SHA, operator-facing
apply must fail closed and demand the missing artifact. It must not silently
build, pack, synthesize, or pull from the dirty developer checkout. The GUI may
link to the image/artifact build command in an advanced or CI/CD handoff path,
but its normal apply path consumes a complete lock.

Commit and provenance records should distinguish:

- **source promotion:** the submodule commits and final super-repo SHA
- **artifact materialization:** the CI/CD or image/artifact run that produced
  immutable artifact refs for that SHA
- **deployment lock:** the manifest consumed by apply and referenced by later
  runs

### Trunk Promotion Pattern

When promoting feature work to trunk in a Wielder super-repo, merge or fast-forward the owning submodules to their trunk branches first, then update the super-repo by committing the resulting submodule pointers. Do not merge the super-repo branch itself to perform this promotion.

- The super-repo trunk should record already-merged submodule trunk SHAs. Do not treat the super-repo as the primary place where submodule feature branches are merged.
- If the operator asks to promote "all locals", "all submodules", "everything
  here", or similar, audit every initialized submodule, not only the files that
  were edited in the current assistant turn. Any initialized submodule checked
  out on the coordinated feature branch is part of the promotion set unless the
  operator explicitly excludes it.
- For each promoted submodule, check out that repository's trunk branch, pull it
  fast-forward-only from origin, merge or fast-forward the coordinated feature
  branch into trunk, and push trunk before returning to the super-repo.
- A super-repo promotion commit stages only intended gitlinks, `.gitmodules`
  when intentionally changed, and files owned by the super-repo such as
  top-level docs or provenance artifacts. It does not merge or resolve
  submodule source files directly.
- In Workspace, the trunk branch is `main` for normal submodules and `workspace` for `Wielder`.
- Touch only the submodules that are part of the intended promotion set. If a module exists on disk but is not tracked by the current super-repo branch, either leave it alone or explicitly add it as a submodule with a `.gitmodules` entry and gitlink.
- Prefer fast-forward merges when the submodule trunk is an ancestor of the feature branch. If a non-fast-forward merge or conflict is required, stop and report the exact branch state before continuing.
- Do not rely on the parenthetical branch label printed by
  `git submodule status` as proof of the active checkout branch. That label may
  name any local branch or remote ref that contains the recorded commit, so it
  can still show `heads/feature/...` after the working tree has been promoted to
  `main`. Verify actual checkout branches with `git -C <submodule> branch
  --show-current` or `git submodule foreach 'git branch --show-current'`.
- After submodule trunks are updated, commit a super-repo pointer update that stages only `.gitmodules` when needed, the intended submodule gitlinks, and any explicit provenance/report artifact.
- Do not stage unrelated untracked directories merely because they are present in the working tree. Ignore or track them through a separate explicit decision.

### Super-Repo Consolidation Workflow

Use this workflow when submodule commits have already been made and pushed, and
the remaining task is to consolidate those new module SHAs into the super-repo
trunk. This is the cleanup path after a broad human command such as
`git submodule foreach ...` or after manually committing in several modules.

1. Audit the super-repo diff before staging:

   ```bash
   git status --short --ignore-submodules=none
   git diff --submodule=log --stat
   git diff --submodule=log
   ```

2. For every changed submodule pointer, inspect the pushed range and capture the
   subject(s) that explain why the pointer moved:

   ```bash
   git -C <submodule> status --short --branch
   git -C <submodule> log --oneline origin/<trunk>..<trunk>
   git -C <submodule> log --oneline <old-sha>..<new-sha>
   git -C <submodule> push
   ```

   If the push says "Everything up-to-date", still include the module in the
   super-repo message when its gitlink changed. If the local branch is not the
   intended trunk, stop and resolve that branch mismatch before consolidating.

3. Stage only the intended gitlinks and super-repo-owned files:

   ```bash
   git add <submodule-a> <submodule-b> <super-owned-file>
   git diff --cached --submodule=log --stat
   git diff --cached --submodule=log
   ```

4. Use a consolidation commit subject that describes the operator-visible
   outcome, not the mechanics. Avoid vague subjects such as "update submodules"
   or typo-bearing scratch messages. The body must list every submodule pointer
   movement and the reason it moved.

Recommended message shape:

```text
Consolidate remote workstation bootstrap ergonomics

Record pushed submodule updates for the remote workstation init flow:

- Wielder c181ead: install full VS Code extension recommendation set from the
  Ubuntu bootstrap script.
- workflow-wielder a5c2d4a: run desktop setup from workstation init and tune the
  left hover dock plus mouse speed.
- wielder-antifragile 6dd5ade: document all-local trunk promotion and
  super-repo consolidation rules.

Supermodule: records pushed submodule SHAs and .vscode extension
recommendations for future remote workstations.
Validation: workstation init completed; bash -n install_ubuntu.sh; py_compile
workstation.py.
Risk: existing pushed submodule commit subjects are preserved; this commit
summarizes their actual content for the super-repo history.
```

When provenance is required, append the normal agent commit-message fields
after the human-readable consolidation summary. If the operator explicitly asks
for "no provenance", keep the structured submodule summary anyway; it is a
human sanity aid, not agent provenance.

## Mode Scope

Versioning review must account for the Wielder mode that the change is meant to affect: `ecosystem`, `stage_tier`, `context_conf`, `security`, `canary`, and any app-local modulation axes.

- If a change is intended for one mode only, verify that it is isolated to that mode's config surface.
- If a change is intended to become shared behavior, verify that it belongs in versioned app/project config rather than local context config.
- If a runtime depends on unversioned mode inputs, disclose that dependency before commit and promote it only through the appropriate config, secret, or build-overlay boundary.
- Do not encode mode decisions in commit commands, ad hoc CLI flags, or narrow Python helpers when the [Configuration & Datastore Lineage](SKILL_CONFIGURATION_GUIDELINES.md) skill says they belong in config.

## Agent Commit Message Contract

If an agent creates a commit, the commit message body must disclose agent provenance and audit status.

Minimum body fields:

```text
Agent-Commit: yes
Agent-Platform: OpenAI Codex
Agent-Audit: diff/status/submodule review before commit
Validation: <commands run, or "not run: <reason>">
```

When applicable, add:

```text
Agent-Model: <model if available, otherwise "unavailable in session">
Agent-Operator: <human operator if relevant>
Agent-Context: <brief task or workflow context>
Submodule: <name> <sha>
Supermodule: pointer update committed after submodule commit
Image-Provenance: final super-repo SHA required before build/deploy
Risk: <known residual risk or "none identified">
```

The commit subject should remain human and domain-specific. Do not put noisy provenance in the subject unless the operator explicitly wants that style.

Do not spoof a human author with `--author` to hide agent work. Use normal repository identity rules and disclose agent participation in the commit message body.

Example submodule commit:

```text
Fix raw mirror Provider fanout config

Agent-Commit: yes
Agent-Platform: OpenAI Codex
Agent-Audit: diff/status/submodule review before commit
Validation: pytest workflow-wielder/tests/test_raw_mirror_integration.py -q
Risk: live deploy not run in this commit
```

Example super-repo pointer commit:

```text
Update workflow-wielder raw mirror fanout

Agent-Commit: yes
Agent-Platform: OpenAI Codex
Agent-Audit: super-repo status and submodule pointer review before commit
Submodule: workflow-wielder <sha>
Supermodule: pointer update committed after submodule commit
Validation: submodule tests passed before pointer commit
```

## Human-Readable Provenance JSON

When an agent creates commits, also write a compact, human-readable provenance JSON artifact for recovery and audit. The artifact should describe what was committed, who requested it, which agent/platform performed it, which modes it affects, and what validation supported it.

Preferred location:

```text
<repo>/reports/git_provenance/report.json
```

Use the stable generic filename `report.json` for versioned provenance and overwrite its contents as the task evolves. Do not encode task, feature, timestamp, branch, or other transient context in the versioned filename; put that context inside the JSON payload. If several specific provenance reports must coexist, put them in an ignored local report directory and garbage collect that directory explicitly instead of accumulating versioned report files.

Minimum shape:

```json
{
  "schema": "wielder.git_provenance.v1",
  "created_at": "2026-05-18T00:00:00Z",
  "operator": "<human operator>",
  "agent": {
    "commit": true,
    "platform": "OpenAI Codex",
    "model": "<model if available, otherwise unavailable in session>"
  },
  "scope": {
    "super_repo": "<path or repo name>",
    "submodules": [
      {
        "name": "<submodule>",
        "commit": "<sha>",
        "paths": ["<path>"]
      }
    ],
    "modes": {
      "ecosystem": "<value>",
      "stage_tier": "<value>",
      "context_conf": "<value>",
      "security": "<value>",
      "canary": "<value>"
    }
  },
  "commits": [
    {
      "repo": "<repo>",
      "sha": "<sha>",
      "subject": "<subject>",
      "kind": "submodule|supermodule|standalone"
    }
  ],
  "audit": {
    "summary": "<short adversarial audit summary>",
    "uncommitted_leftovers": ["<path or reason>"],
    "risks": ["<known residual risk>"]
  },
  "validation": [
    {
      "command": "<command>",
      "result": "passed|failed|not_run",
      "notes": "<short note>"
    }
  ]
}
```

Do not place secrets, access tokens, credential payloads, or private local-only config contents in the provenance JSON. Refer to secret names, config surfaces, or artifact paths instead.

## Reporting Back

After committing, report:

- Commit SHA for each submodule commit.
- Commit SHA for the super-repo pointer commit, if any.
- Provenance JSON path, if one was written.
- Validation commands and outcomes.
- Any dirty files intentionally left uncommitted.
- The next build/apply/run command when image or workflow provenance depends on the new SHA.

Keep this report short. The important point is that the operator can see what was committed, what was not committed, and what SHA should now drive the next Wielder action.
