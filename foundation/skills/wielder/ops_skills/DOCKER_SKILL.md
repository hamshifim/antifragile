# Docker Skill

## Purpose

Use this note when local Docker builds feel irrationally unstable, especially for large CUDA or model-serving images.

The main lesson is simple:

- do not judge the machine by host specs alone
- judge the actual Docker surface:
  - Docker Desktop resource budget
  - WSL memory budget
  - Windows disk pressure
  - buildx health
- cache and volume footprint
- WSL VHD compaction behavior on the Windows host

On this workstation, the important observed facts were:

- Docker only saw `8` CPUs and about `7.8 GiB` RAM
- Windows `C:` was `94%` full
- `docker buildx ls` showed `desktop-linux` as broken
- Docker build logs showed buildstore and builder-listener warnings
- local image and volume state had already grown very large

That means "the workstation is huge" and "Docker is unstable" can both be true at once.

## Fast Inspection

Run these first:

```bash
docker info
docker buildx ls
docker system df -v
docker ps -a
docker images
docker volume ls
df -h / /mnt/c
free -h
```

What to look for:

- low effective Docker memory despite a strong host
- Windows `C:` nearly full
- broken builders such as `desktop-linux`
- huge stale images
- huge build cache
- very large local volumes

Useful log locations on this machine:

```text
/mnt/c/Users/<windows-user>/AppData/Local/Docker/log/host/com.docker.build.log
/mnt/c/Users/<windows-user>/AppData/Local/Docker/log/host/com.docker.backend.exe.log
/mnt/c/Users/<windows-user>/AppData/Local/Docker/log/host/docker-desktop.exe.log
```

Good quick grep:

```bash
tail -n 200 /mnt/c/Users/<windows-user>/AppData/Local/Docker/log/host/com.docker.build.log
```

Red flags:

- `Cannot load builder desktop-linux: protocol not available`
- repeated `skip listening node desktop-linux`
- buildstore path or GC failures

## Prune Levels

### Conservative

Only remove dangling junk:

```bash
docker image prune -f
docker builder prune -f
```

### Aggressive

Remove everything not currently used by running containers:

```bash
docker system prune -af --volumes
docker builder prune -af
```

Important:

- this keeps images and volumes attached to running containers
- this does not preserve "useful for later" images unless they are active right now

So before aggressive pruning, decide what "using now" means.

For a local GPU workflow, a good rule is:

- keep the current k3d cluster infrastructure
- optionally keep the current base and service images if you expect to reuse them soon

## WSL Disk Reclaim

Deleting images and clusters inside WSL does not guarantee that Windows immediately recovers the backing disk space. The Linux filesystem may be clean while the host-side `.vhdx` remains inflated.

Use a two-phase cleanup model:

1. Clean Docker, caches, and clusters inside WSL.
2. From elevated PowerShell on Windows, compact the WSL VHDX.

Use the runtime toolkit helper:

```powershell
& "$HOME\workspace\Wielder\wielder\scripts\compact_wsl_vhd.ps1" -DistroName Ubuntu
```

Important:

- run it from elevated PowerShell
- ensure `wsl --shutdown` succeeds
- avoid relaunching Docker Desktop or a WSL shell during compaction

## Resource Tuning From Windows PowerShell

Do not edit Docker Desktop internals by hand unless absolutely necessary.

The main supported PowerShell lever is the WSL config file:

```powershell
@"
[wsl2]
memory=24GB
processors=16
swap=16GB
localhostForwarding=true
"@ | Set-Content -Path "$HOME\.wslconfig" -Encoding Ascii
```

Then fully restart WSL and Docker Desktop:

```powershell
wsl --shutdown
```

After that:

1. quit Docker Desktop
2. start Docker Desktop again
3. verify from WSL:

```bash
docker info | sed -n '1,80p'
free -h
```

The exact values are your choice, but for large model-serving or CUDA builds, `7.8 GiB` is too small to trust.

## Docker Desktop Paths

Useful Windows paths:

- Docker Desktop settings store:
  - `%APPDATA%\Docker\settings-store.json`
- WSL config:
  - `%USERPROFILE%\.wslconfig`

The settings store is useful for inspection, not as the preferred manual edit surface.

## Workspace-Specific Advice

- local Docker is acceptable for lighter images and fast k3d iteration
- large model-runtime builds stress the weakest part of the stack first
- if Docker Desktop is unhealthy, fix Docker Desktop before redesigning Workspace
- do not confuse an image-build failure with an app-architecture failure

If builds still crash after:

- freeing Windows disk space
- increasing WSL resources
- resetting broken builders
- pruning stale cache

then a bootstrap node is justified as a reliability surface, not as a brute-force compute upgrade

## Practical Recovery Order

1. Free space on `C:`
2. Set a real WSL memory and CPU budget in PowerShell
3. Restart WSL and Docker Desktop
4. Check `docker buildx ls`
5. Prune stale images and build cache
6. Retry the build
7. Only then conclude the local Docker surface is not worth more time
