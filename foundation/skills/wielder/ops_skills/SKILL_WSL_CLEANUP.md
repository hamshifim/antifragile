---
description: WSL workstation cleanup protocol for disk-pressure recovery, safe cache pruning, active unique_name preservation, fstrim, VHDX compaction, and post-restart verification.
---


# WSL Cleanup

Use this skill when a Windows workstation running WSL is under disk, swap, or
cache pressure and the operator wants a full cleanup plus VHDX compaction.

## Principle

Clean the Linux filesystem first, then release unused blocks to the virtual
disk, then compact the Windows-side `.vhdx`. Deleting files inside WSL is not
the same as shrinking the host disk image.

Treat the workstation as a control plane. Preserve active runtime identity,
secrets, model caches, local buckets, repositories, and operator notes unless
the operator explicitly approves a narrower deletion.

## Safety Gates

- Ask the operator to stop active servers, notebooks, Docker builds, WSL shells,
  and agents before shutdown or compaction.
- Identify the active `unique_name` from resolved config or the active
  `developer.conf` context before pruning staging, image, Terraform, or
  artifact directories.
- Preserve directories matching the active `unique_name`.
- Do not delete Hugging Face, Torch, Ollama, local bucket, repo, Terraform state,
  cloud auth, kubeconfig, SSH, or ignored developer config surfaces casually.
- Use exact paths for deletion. Never run broad deletes against `$HOME`,
  `$HOME/dev`, `$HOME/work`, a repo root, or an uninspected parent.
- Prefer audit output before deletion and verification output after deletion.

## Audit

From PowerShell, measure host pressure and find WSL disks:

```powershell
Get-PSDrive C
Get-ChildItem -Path $env:LOCALAPPDATA,$env:USERPROFILE -Recurse -Filter *.vhdx -Force -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending |
  Select-Object -First 12 @{Name='GB';Expression={[math]::Round($_.Length/1GB,2)}},FullName
```

From PowerShell, measure WSL pressure:

```powershell
wsl -d Ubuntu -- bash -lc 'df -hT / /home /mnt/c 2>/dev/null; free -h; swapon --show || true; docker system df 2>/dev/null || true'
wsl -d Ubuntu -- bash -lc 'du -xhd1 "$HOME/.cache" "$HOME/stage" "$HOME/local_buckets" "$HOME/tmp" 2>/dev/null | sort -h | tail -80'
```

Name the top candidates before cleanup. Typical large surfaces are `uv` cache,
pip cache, Docker volumes/build cache, stale Wielder staging roots, stale temp
swap/VHDX directories, and old generated diagnostics.

## Resolve Active Runtime Identity

Before pruning Wielder staging surfaces, resolve the active identity:

```powershell
wsl -d Ubuntu -- bash -lc 'cd "$HOME/dev/culture" && grep -R "unique_name" -n conf/context_conf conf 2>/dev/null | head -40'
```

Prefer the resolved Wielder config or the current `developer.conf` context over
raw grep when available. The active `unique_name` protects staging clones,
artifactories, image workdirs, Terraform roots, and runtime scratch tied to the
current work.

## Cleanup Order

Clean reversible cache surfaces first:

```powershell
wsl -d Ubuntu -- bash -lc 'uv cache clean 2>/dev/null || true'
wsl -d Ubuntu -- bash -lc 'python -m pip cache purge 2>/dev/null || true'
wsl -d Ubuntu -- bash -lc 'rm -rf "$HOME/.cache/go-build" "$HOME/.npm/_cacache" 2>/dev/null || true'
```

If Docker is stopped or no important local containers depend on old state,
prune generated Docker storage:

```powershell
wsl -d Ubuntu -- bash -lc 'docker builder prune -af 2>/dev/null || true'
wsl -d Ubuntu -- bash -lc 'docker volume prune -f 2>/dev/null || true'
```

Only after identifying the active `unique_name`, remove stale generated
Wielder staging roots by exact obsolete name. Keep the active name:

```powershell
wsl -d Ubuntu -- bash -lc 'find "$HOME/stage" -maxdepth 4 -type d -name "dev--*" 2>/dev/null | sort'
```

Delete only inspected obsolete paths, one exact path at a time:

```powershell
wsl -d Ubuntu -- bash -lc 'rm -rf -- "$HOME/stage/<obsolete-unique-name>"'
```

## Trim WSL

After deleting data inside WSL, release unused ext4 blocks:

```powershell
wsl -d Ubuntu -u root -- fstrim -av
```

This makes blocks available to the virtual disk layer. It does not guarantee the
Windows file has shrunk yet.

## Compact The VHDX

Compaction stops WSL. Confirm with the operator first.

```powershell
wsl --shutdown
Optimize-VHD -Path "<path-to-ext4.vhdx>" -Mode Full
```

If `Optimize-VHD` is unavailable, use the local Wielder helper when present:

```powershell
& "$HOME\workspace\Wielder\wielder\scripts\compact_wsl_vhd.ps1" -DistroName Ubuntu
```

If neither path is available, hand off a manual elevated PowerShell/DiskPart
compaction step. Do not keep relaunching WSL during compaction.

## Verify

After compaction and restart:

```powershell
Get-PSDrive C
wsl -d Ubuntu -- bash -lc 'df -hT / /home 2>/dev/null; free -h; swapon --show || true'
```

Report:

- Windows free space before and after.
- WSL filesystem free space before and after.
- What cache/staging surfaces were removed.
- Which active `unique_name` was preserved.
- Any large remaining candidates intentionally left alone.

## Restart Guidance

Ask for a Windows restart when Windows temp VHDX files remain locked, WSL memory
or swap still looks strained after cleanup, Docker Desktop reports stale
builders, or the operator wants a clean control-plane baseline before resuming
heavy work.

## Anti-Patterns

- Treating `df -h` inside WSL as proof that Windows reclaimed VHDX space.
- Compacting before deleting or trimming inside WSL.
- Deleting every `dev--*` staging root without preserving the active
  `unique_name`.
- Removing model caches or local data buckets just because they are large.
- Running cleanup while another agent, build, notebook, or service is active.
