---
name: Monday MCP
description: Connect WSL-hosted Codex to monday.com through monday.com's MCP server, including Windows token bridging, local stdio registration, validation, and failure recovery.
---

# Monday MCP

Use this skill when Codex must read or update monday.com from a WSL workspace,
especially when the operator's monday API token lives on the Windows side.

## Current Working Shape

Observed on 2026-05-15:

- Node `v22.19.0` and npm `11.6.2` in WSL satisfy the monday MCP package
  requirement of Node 20+.
- The local package is installed at:
  `/home/<operator>/.codex/mcp/monday/node_modules/@mondaydotcomorg/monday-api-mcp`
- Installed package version: `@mondaydotcomorg/monday-api-mcp@3.1.2`.
- The Windows user environment variable is named `monday_token`.
- The MCP package itself accepts the token reliably as `MONDAY_TOKEN`, so the
  bridge exports uppercase `MONDAY_TOKEN` from the Windows-side value.
- Codex MCP tools are loaded at session startup. After changing MCP
  registration, restart Codex before expecting monday tools to appear.
- The current Windows `monday_token` value was a placeholder
  (`YOUR_MONDAY_API_TOKEN`). That is enough to prove process startup and tool
  discovery, but monday API calls return `401 NOT_AUTHENTICATED` until the
  operator replaces it with a real monday API token.
- After replacing the placeholder with a real token and restarting VS Code,
  authenticated validation succeeded: default API mode listed 66 tools and
  `get_user_context` returned successfully.

Register the default API tool mode from WSL:

```bash
codex mcp remove monday || true
codex mcp add monday -- bash -lc 'export MONDAY_TOKEN=$(/mnt/c/windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "(Get-ItemProperty -Path HKCU:\Environment -Name monday_token).monday_token" | tr -d "\r"); exec node /home/<operator>/.codex/mcp/monday/node_modules/@mondaydotcomorg/monday-api-mcp/dist/index.js'
codex mcp get monday
```

Expected registration shape:

```text
monday
  enabled: true
  transport: stdio
  command: bash
  args: -lc export MONDAY_TOKEN=$(...); exec node /home/<operator>/.codex/mcp/monday/node_modules/@mondaydotcomorg/monday-api-mcp/dist/index.js
```

## Why Default API Mode

The package supports `--mode api`, `--mode apps`, and `--mode atp`. The default
is API mode.

For Wielder task-management work, prefer the default API mode because it exposes
the platform tools directly: boards, items, updates, docs, workspaces, search,
users, forms, assets, sprints, and related monday operations.

ATP mode did start successfully, but it exposed only:

```text
execute_code, explore_api
```

That is useful for GraphQL exploration, but it is alpha and less ergonomic for
normal task operations. Use ATP only when the operator explicitly asks for
schema exploration or dynamic GraphQL execution:

```bash
node /home/<operator>/.codex/mcp/monday/node_modules/@mondaydotcomorg/monday-api-mcp/dist/index.js -m atp
```

## Setup From Scratch

Install the package into Codex-owned MCP local state:

```bash
mkdir -p /home/<operator>/.codex/mcp/monday
cd /home/<operator>/.codex/mcp/monday
npm install @mondaydotcomorg/monday-api-mcp@latest
```

Do not add the monday package to the `workspace` super-repo `package.json` unless
the repo itself needs a JavaScript runtime dependency. MCP server installation
belongs in `/home/<operator>/.codex/mcp/monday`.

Store the token outside the repo. On Windows PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("monday_token", "<token>", "User")
```

Replace the whole `<token>` placeholder, including the angle brackets. If the
saved value still contains `<`, `>`, whitespace from the example text, or a
phrase such as `real monday API token`, the MCP server will start but monday
will reject API calls.

Then register the bridge from WSL using the command in `Current Working Shape`.

## Validation

Check that Codex has the server registered:

```bash
codex mcp list
codex mcp get monday
```

If the current Codex session was already running, registration alone is not
enough. Restart Codex, then verify a monday tool is available through the tool
list or by performing a harmless read such as workspace/user context.

On 2026-05-15, a raw `get_user_context` call reached monday through the MCP
server but returned `401 NOT_AUTHENTICATED` because the Windows token value was
still the placeholder. Treat this as an auth boundary, not a WSL transport
failure.

After the operator saved the real token and restarted VS Code, the same raw
stdio validation succeeded. If tools still do not appear inside a Codex chat
after this point, restart the Codex session itself so MCP tool discovery runs
again.

For a raw stdio smoke test without printing the token:

1. Read the token from Windows with PowerShell.
2. Export it as `MONDAY_TOKEN` only for the child process.
3. Start `dist/index.js`.
4. Send MCP `initialize`, `notifications/initialized`, and `tools/list`.

Observed successful default-mode tool listing included:

```text
delete_item, get_board_items_page, create_item, create_update, get_updates,
get_board_schema, get_board_info, list_users_and_teams, search,
get_user_context, create_doc, update_doc, create_workspace, create_folder
```

Observed successful ATP-mode tool listing:

```text
execute_code, explore_api
```

## WSL Failure Modes

- **No monday tools in this Codex session**: Expected after first registration
  or a registration change. Restart Codex.
- **Token present in Windows but server says token missing**: Ensure the WSL
  command exports `MONDAY_TOKEN`. The Windows variable can remain
  `monday_token`; the bridge handles the case conversion.
- **Tool discovery works but monday calls return `401 NOT_AUTHENTICATED`**:
  Inspect only token metadata or the Windows variable name, not the token value.
  A placeholder such as `YOUR_MONDAY_API_TOKEN` starts the server but cannot
  authenticate with monday.
- **The PowerShell command was pasted literally with `<real monday API token>`**:
  Run the setter again with the actual token string only. Do not include angle
  brackets or the explanatory placeholder words.
- **PowerShell command includes `\r` in the token**: Pipe through `tr -d "\r"`.
- **`powershell.exe` resolution is inconsistent**: Use the absolute path
  `/mnt/c/windows/System32/WindowsPowerShell/v1.0/powershell.exe`.
- **Running `npx ... -t <token>` works but is unsafe for handoffs**: It puts the
  token in shell history and process listings. Prefer environment bridging.
- **ATP mode works but task tools are missing**: Remove `-m atp` from the Codex
  registration and restart Codex.
- **A top-level `package.json` appears in `/home/<operator>/workspace`**: Treat it as
  accidental prior-thread residue unless the operator confirms the super-repo
  should own Node dependencies. Local MCP installs should live under
  `/home/<operator>/.codex/mcp/monday`.

## Security Boundary

Never put monday API tokens in tracked config, HOCON, docs, command examples,
package scripts, or final responses.

Prefer this order:

1. Official hosted monday MCP with OAuth when the MCP client supports it.
2. Local stdio MCP with token supplied by environment.
3. One-off `-t <token>` only for an operator-run local diagnostic, never in
   committed files or durable handoffs.

The local WSL bridge is a pragmatic fallback for Codex on Windows WSL. It keeps
the secret outside the repo and avoids printing it during validation.

## Upstream References

- monday.com MCP overview:
  `https://developer.monday.com/api-reference/docs/monday-mcp-overview`
- monday.com MCP security overview:
  `https://developer.monday.com/api-reference/docs/monday-mcp-security-overview`
- monday API MCP package:
  `https://www.npmjs.com/package/@mondaydotcomorg/monday-api-mcp`
- monday API MCP source:
  `https://github.com/mondaycom/monday-ai/tree/master/packages/monday-api-mcp`
