---
name: MCP Browser Bridge
description: Connect Codex running in WSL to a Windows Chrome session through Playwright MCP extension mode.
---

# MCP Browser Bridge

Use this skill when Codex needs to drive a real Windows Chrome session from a
WSL-based Codex workspace, especially when the target site depends on an
already-authenticated browser profile.

## Preferred Shape

Use Playwright MCP in **HTTP mode** from Windows PowerShell, then register the
HTTP endpoint in Codex from WSL.

Do not use manual stdio mode for Codex:

```powershell
npx @playwright/mcp@latest --extension
```

That starts a stdio MCP server, but no MCP client is attached to its stdin/stdout,
so the Chrome extension continues to report no connected clients.

## Windows Chrome Setup

1. Install the Chrome Web Store extension:
   `Playwright Extension`
2. Open the extension status page or popup.
3. Copy the current `PLAYWRIGHT_MCP_EXTENSION_TOKEN`.
4. Keep Chrome open in the profile that has the required login/session.

The extension status page is:

```text
chrome-extension://mmlmfjhmonkocbjadbfplnigmagldckm/status.html
```

## Start Playwright MCP From Windows PowerShell

Run this in Windows PowerShell, replacing `<token>` with the token shown by the
extension:

```powershell
$env:PLAYWRIGHT_MCP_EXTENSION_TOKEN="<token>"
$env:PATH="C:\Program Files\nodejs;$env:PATH"
npx @playwright/mcp@latest --extension --port 8931 --host 0.0.0.0 --allowed-hosts "*"
```

For a less interactive setup, persist the token once at Windows user scope:

```powershell
[Environment]::SetEnvironmentVariable("PLAYWRIGHT_MCP_EXTENSION_TOKEN", "<token>", "User")
```

Then restart PowerShell and start MCP without setting the token in each session:

```powershell
$env:PATH="C:\Program Files\nodejs;$env:PATH"
npx @playwright/mcp@latest --extension --port 8931 --host 0.0.0.0 --allowed-hosts "*"
```

Do not store real extension tokens in tracked repo files. If the extension token
is regenerated, update the Windows user environment variable and restart Chrome
before restarting the MCP server.

Leave the PowerShell process running. Expected output:

```text
Listening on http://localhost:8931
Put this in your client config:
{
  "mcpServers": {
    "playwright": {
      "url": "http://localhost:8931/mcp"
    }
  }
}
```

## Register From WSL Codex

Windows `127.0.0.1` is not WSL `127.0.0.1`. Resolve the Windows host address
from WSL:

```bash
WIN_HOST=$(ip route | awk '/default/ {print $3; exit}')
curl -sS -I --max-time 5 "http://${WIN_HOST}:8931/mcp"
```

An HTTP `400 Bad Request` from `curl -I` is acceptable here; it proves WSL can
reach the MCP endpoint.

Then register Codex:

```bash
codex mcp remove playwright || true
codex mcp add playwright --url "http://${WIN_HOST}:8931/mcp"
codex mcp get playwright
```

Restart Codex after changing MCP registration. The browser tools are loaded at
session startup.

## Validation

After restart, call the Playwright browser tool first:

```text
browser_tabs list
```

Successful connection returns existing Chrome tabs, for example a Playwright
extension `Welcome` or `connect.html` tab.

## Failure Modes

- **`No clients are currently connected` in extension popup**: The Playwright MCP
  server is not connected to the extension. Confirm the token matches, reload
  the extension, and ensure the PowerShell server is running in HTTP mode with
  `--extension`.
- **WSL `curl` cannot connect to `127.0.0.1:8931`**: Expected. Use the Windows
  host IP from `ip route`, not WSL loopback.
- **Codex tool call says `Transport closed`**: The MCP process that Codex loaded
  died. Restart Codex after ensuring the HTTP server is already running.
- **Tool call times out**: The MCP endpoint is reachable, but the Chrome
  extension did not connect to the server. Reload the extension and check token.
- **Multiple Playwright MCP processes exist**: Stop stale `playwright-mcp`,
  `@playwright/mcp`, `node`, or `cmd` processes that belong to old MCP attempts.
  Multiple extension-mode servers can leave the extension connected to the wrong
  process.
- **After WSL restart**: Recompute `WIN_HOST` and update Codex if it changed.

## Useful Inspection Commands

From WSL:

```bash
codex mcp list
codex mcp get playwright
ps -ef | rg 'playwright|mcp|npx|cmd.exe|node'
```

From WSL, inspecting Windows processes:

```bash
/mnt/c/windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command \
  'Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "playwright|@playwright|mcp|npx" } | Select-Object ProcessId,Name,CommandLine | Format-List'
```
