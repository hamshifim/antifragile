---
name: caffeinate-cli
description: Use when keeping a Windows host awake from WSL — preventing idle system or display sleep while a long job runs, holding wake for a fixed window, or wrapping a command so the machine stays awake only for its duration. Covers the `caffeinate` CLI (a macOS-caffeinate port for Windows driven from the WSL shell), its flags, install, and failure handling.
---

# caffeinate CLI

`caffeinate` is a macOS-`caffeinate` port for Windows, driven from the WSL
shell. It keeps the Windows host awake by holding a continuous power request via
the Win32 `SetThreadExecutionState` API for as long as the process lives.

Windows sleep state belongs to the *host*, not the WSL VM, so the lock is taken
Windows-side by `caffeinate.ps1`. A WSL bash wrapper drives it so the operator
works entirely from Ubuntu.

## Source Of Truth

Both files live together in Wielder; the wrapper resolves `caffeinate.ps1` as
its own sibling, so they must stay in the same directory:

- `/home/gideon/dev/culture/Wielder/useful/wsl/caffeinate` — WSL bash entry point.
- `/home/gideon/dev/culture/Wielder/useful/wsl/caffeinate.ps1` — Windows lock.

Read [references/caffeinate.md](references/caffeinate.md) before changing the
mechanism, diagnosing why the host still sleeps, or porting the approach. It
holds the Win32 details and the two failure modes that break naive ports.

## Install

Symlink the wrapper onto PATH once, then invoke it by bare name:

```bash
chmod +x /home/gideon/dev/culture/Wielder/useful/wsl/caffeinate
sudo ln -sf /home/gideon/dev/culture/Wielder/useful/wsl/caffeinate /usr/local/bin/caffeinate
```

## Core Rules

- Hand off the absolute wrapper path or the installed `caffeinate` name. Do not
  hand off `powershell.exe -File ...`, `.ps1` paths, or transient environment
  variables when the wrapper can own the flow.
- The lock lives for exactly as long as the process runs. There is no daemon and
  no persisted state; killing the process (or letting it exit) releases the
  host immediately. The OS clears the per-process execution state on exit, so an
  abrupt death still releases.
- Default holds *system* sleep only. Add `-d` to also hold the *display*.
- Prefer command mode (`caffeinate -- <job>`) over a bare hold for bounded work:
  it scopes the wake to the job's lifetime and exits with the job's status, so
  nothing is left holding the host awake by accident.
- Command mode runs the command in *this WSL shell* (correct cwd and user).
  `-t`/`-w`/bare-hold are pure forwards to the Windows process.

## Common Commands

Keep the system awake until interrupted:

```bash
caffeinate            # system only, until Ctrl+C
caffeinate -d         # system + display
```

Hold for a bounded window, then release:

```bash
caffeinate -t 3600            # awake for one hour
caffeinate -d -t 1800         # system + display for 30 minutes
```

Wrap a job so the host stays awake only while it runs (exits with its status):

```bash
caffeinate -- nextflow run main.nf -profile docker
caffeinate -d -- ./long_train.sh
caffeinate ./build.sh          # the -- is optional before a command
```

Hold until a specific *Windows* process exits:

```bash
caffeinate -w <windows_pid>
```

## Flags

- `-d` — also prevent the display from sleeping (default holds system only).
- `-i` / `-s` — prevent idle/system sleep; this is the default, accepted for
  macOS-caffeinate compatibility.
- `-t <seconds>` — hold for this many seconds, then exit.
- `-w <winpid>` — hold until that Windows PID exits. This is a *Windows* PID, not
  a WSL/Linux PID.
- `-- <cmd...>` — run `<cmd>` in the WSL shell and hold only for its duration.
  The `--` is optional before a bare command.

## Verify The Lock Is Held

`powercfg /requests` needs Administrator. From an elevated Windows PowerShell
while `caffeinate` is running:

```
powercfg /requests
```

An `EXECUTION:` entry attributed to `powershell.exe` is the lock. It disappears
the instant `caffeinate` exits. Lock assertion needs no elevation; only this
inspection does.

## Failure Handling

- Host still sleeps while a bare hold "runs": confirm the wrapper process is
  still alive. The lock dies with the process — a backgrounded hold whose shell
  exited has already released. Use command mode for unattended jobs.
- `caffeinate: cannot find caffeinate.ps1 next to this wrapper`: the wrapper was
  moved away from `caffeinate.ps1`. Keep the pair in the same directory; if the
  installed entry is a symlink, the wrapper resolves through it to find the
  sibling.
- `SetThreadExecutionState failed`: surfaced by the `.ps1` with the Win32 error
  code. Treat as a genuine API failure, not a wrapper bug.
- Command mode shows no wake but the command ran: the wrapper suppresses the
  `.ps1` chatter in command mode by design; verify with `powercfg /requests`
  during a long run rather than expecting on-screen confirmation.

## Documentation Updates

caffeinate documentation belongs in this skill:

- `skills/caffeinate-cli/SKILL.md` for concise operational procedure.
- `skills/caffeinate-cli/references/caffeinate.md` for the Win32 mechanism and
  port-specific gotchas.

The implementation lives in Wielder, not here. Change behavior there; keep this
skill describing the operator surface.
