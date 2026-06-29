# caffeinate — mechanism and port notes

Detailed reference for the Windows `caffeinate` port. Read this before changing
the wake mechanism, diagnosing why the host still sleeps, or reusing the
approach elsewhere.

## What it is

A faithful port of macOS `caffeinate` to Windows, driven from WSL. It prevents
the Windows host from sleeping (and optionally from blanking the display) for as
long as the process lives.

Two files, kept in the same directory:

- `caffeinate` — WSL bash wrapper, the operator entry point.
- `caffeinate.ps1` — the actual lock, run Windows-side via `powershell.exe`.

Location: `/home/gideon/dev/culture/Wielder/useful/wsl/`.

## Why the lock must be Windows-side

Sleep state is a property of the Windows *host*. WSL is a guest VM and cannot
control the host power state, so the lock has to be taken by a Windows process.
The bash wrapper exists only so the operator never has to touch PowerShell by
hand; it forwards to `powershell.exe -File caffeinate.ps1`.

## The Win32 mechanism

The whole port rests on one call, `SetThreadExecutionState` (kernel32), with
these flags:

- `ES_CONTINUOUS` (0x80000000) — make the request *continuous*: it stays in
  effect until reset or the process exits, rather than nudging the idle timer
  once.
- `ES_SYSTEM_REQUIRED` (0x00000001) — prevent idle *system* sleep (the default,
  and what `-i`/`-s` map to).
- `ES_DISPLAY_REQUIRED` (0x00000002) — also prevent the *display* from
  sleeping (added by `-d`).

The state is per-process. While the process holds a continuous request the host
stays awake; when the process exits, Windows clears the state automatically.

## The two failure modes that break naive ports

Most broken attempts fail one of these:

1. **Missing `ES_CONTINUOUS`.** A bare `SetThreadExecutionState(ES_SYSTEM_REQUIRED)`
   resets the idle timer once and returns; the host sleeps a moment later
   anyway. The request must be continuous.
2. **Not staying alive.** The state dies with the process. A script that sets the
   flag and exits holds nothing. The process must live for the whole wake
   window — which is exactly the `caffeinate` model.

## Windows/PowerShell gotchas handled in this port

- **UNC working directory.** `Add-Type`'s inline C# compiler throws
  "Object reference not set" when PowerShell's current directory is a
  `\\wsl.localhost\...` UNC path — which is how the WSL wrapper launches it. The
  P/Invoke is therefore defined via `Reflection.Emit`, which needs no compiler
  and is immune.
- **`-d` eaten as `-Debug`.** Declaring parameters with `[Parameter()]` promotes
  a script to an *advanced function*, which auto-adds common parameters; `-d`
  then prefix-matches `-Debug` and is swallowed before the script sees it. The
  `.ps1` takes no `param()` block and parses the automatic `$args` array by
  hand, so every token (including `-d` and `--`) arrives verbatim.

## How the wrapper scopes wake to a command

Command mode (`caffeinate -- <cmd>`) holds the lock only while `<cmd>` runs:

1. Start `caffeinate.ps1` in hold mode in the background, with its stdin
   connected to a FIFO whose write end the wrapper keeps open.
2. `caffeinate.ps1`, seeing redirected stdin, blocks reading stdin to EOF
   instead of looping — so the parent's open FIFO write end keeps it alive.
3. Run `<cmd>` in the WSL shell; capture its exit status.
4. Close the FIFO write end → EOF → `caffeinate.ps1` releases and exits. No
   PID-killing, and an abrupt death still releases (OS clears per-process state).
5. The wrapper exits with `<cmd>`'s status.

`-t`/`-w`/bare-hold do not use the FIFO; the wrapper `exec`s the Windows process
and lets it own its own lifetime.

## Verifying

`SetThreadExecutionState` returns the previous state and the `.ps1` throws if it
returns 0, so a successful run confirms the API accepted the request. To see the
live lock, run `powercfg /requests` from an elevated Windows PowerShell while
caffeinate holds; an `EXECUTION:` entry under `powershell.exe` is the lock.
Assertion needs no elevation; only this inspection does.
