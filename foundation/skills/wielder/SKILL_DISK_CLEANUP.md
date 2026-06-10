---
description: Safe local disk cleanup doctrine for Wielder staging, Docker image/build cache, Terraform provisioning clones, and operator workstation disk pressure.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Disk Cleanup

Use this skill when a local operator workstation, Wielder image build, Docker
daemon, or staging/provisioning tree is under disk pressure.

## Audit First

Measure before deleting:

```bash
df -h /
du -xh -d 2 "$HOME/stage" 2>/dev/null | sort -h | tail -40
du -xh -d 2 "$HOME" 2>/dev/null | sort -h | tail -40
docker system df 2>/dev/null || true
```

Name the large surfaces explicitly in the handoff. Typical Wielder workstations
fill from Docker build cache, unused local images, Wielder image staging
sandboxes, Wielder provisioning clones, local bucket mirrors, language caches,
or editor/browser caches.

## Cleanup Order

Prefer generated and cache surfaces first.

1. Remove clearly stale Wielder image staging sandboxes, especially timestamped
   quarantine directories such as `*.stale-*`.
2. Prune Docker build cache:
   ```bash
   docker builder prune -af
   ```
3. If still tight, prune unused Docker images only after confirming the operator
   accepts local rebuild cost:
   ```bash
   docker image prune -af
   ```
4. Inspect Wielder staging under `~/stage`; remove old image staging directories
   only when they are clearly generated sandboxes.
5. Treat Terraform provisioning directories under `~/stage/**/provision` as
   approval-only cleanup. They may contain working clones and state-adjacent
   context. Delete them only by exact obsolete `unique_name` directory after
   confirming live resources are gone or state recovery is irrelevant.

## Safety Rules

- Never run broad `rm -rf` against `~/work`, a repository root, or an
  uninspected parent directory.
- Prefer moving suspicious generated directories aside before deleting when disk
  pressure allows it.
- If root is nearly full, delete only already-identified generated sandboxes or
  Docker build cache first.
- Do not delete Terraform state files, `.terraform` directories, or provisioning
  clones casually.
- Report what was removed, current `df -h /`, and remaining large candidates.
