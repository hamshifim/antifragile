---
description: Wield organizational task systems, messaging, documentation, diagramming, reporting, and adjacent execution surfaces so implementation work advances explicit organizational goals through configured third-party platforms.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Org Task Wielding

Use this skill when work needs to be represented, routed, communicated,
documented, visualized, or handed off through organizational systems such as
task managers, Slack, email, Google Docs, Drive, Lucidchart, rendered reports,
Python charts, dashboards, or related execution surfaces.

This skill helps Wielder implement organizational goals by configuring and
operating third-party systems in a coherent way.

## Meta Doctrine

The source white paper is the behavioral doctrine for how the task-management
system should act:

[TASK_MANAGEMENT_WHITE_PAPER.md](TASK_MANAGEMENT_WHITE_PAPER.md)

Treat the white paper as the meta guideline for goal linkage, task ontology,
ownership, review, compartment boundaries, progression, escalation, and human
handoff. Read it when designing or changing the task-management ontology or
when a platform workflow must encode those semantics.

## Implementation Rule

Implement the white-paper doctrine through configuration and platform adapters.

Configuration should own:

- target platform and provider
- task space, board, list, channel, folder, document, or destination identity
- state/status mappings
- owner/reviewer/group mappings
- notification routing
- document/report destinations
- goal-to-task projection rules
- human handoff templates

Python should validate the resolved config, call the configured Wielder surface,
and fail loudly when required platform identity or routing is missing.

## API And MCP

Before implementing against a third-party surface, choose the cleanest API or
MCP route and then use the platform-specific skill or integration instructions
when available.

Current local API/MCP guidance:

- [SKILL_MONDAY_MCP.md](SKILL_MONDAY_MCP.md): Monday API/MCP setup, Windows/WSL token bridging,
  token validation, and recovery.
- [SKILL_MCP_BROWSER_BRIDGE.md](SKILL_MCP_BROWSER_BRIDGE.md): browser MCP bridge for UI-only inspection,
  authenticated browser sessions, and browser-mediated validation.

Plugin or connector skills may also apply for Slack, Google Drive, Google Docs,
Google Sheets, Google Slides, GitHub, Canva, or other installed integrations.

Preference order:

1. Platform-native API wrapper when Wielder owns a reusable implementation.
2. Platform MCP or connector when it exposes the needed operation cleanly.
3. Browser MCP when the task requires authenticated UI state, visual
   confirmation, or a capability missing from the API/MCP surface.

Use browser automation only when:

- the platform API/MCP/connector cannot expose the required view or mutation
- visual confirmation is the task itself
- the operator explicitly asks for browser/UI behavior

## API Shape Wrappers

Third-party systems have their own ontologies. Keep those native ontologies
intact at the provider boundary.

Use two layers:

- `<platform>_wrapper`: provider-native API shape and nomenclature. Examples:
  `MondayWrapper.workspaces()`, `MondayWrapper.boards(...)`, a future
  `ClickUpWrapper.spaces()`, or a mail wrapper that speaks folders, messages,
  labels, and threads.
- `W<Platform><Capability>` adapter: Wielder verbs and ontology over that
  provider wrapper. Examples: `WMondayTasker.list_task_spaces()` or a future
  Slack/Docs/Chart adapter exposing generic Wielder communication or reporting
  verbs.

Both layers may be public. The wrapper is useful for diagnostics and full
platform capability; the Wielder adapter is the encouraged surface for normal
scripts and workflows.

Add a generic Wielder verb when the concept is meaningful across plausible providers.
Provider-specific capability remains on the wrapper.

## Wielder Tasker Nomenclature

For generic task-management adapters, prefer Wielder nouns that can survive
across platforms:

- `task_principal_context`: authenticated user/account/workspace context
- `task_space`: a bounded organizational area such as a Monday workspace or a
  ClickUp space/team-like container
- `task_board`: a board/list-like surface where work items are grouped
- `task_item`: a task, item, card, issue, or row that carries work
- `task_state`: the human progression state, mapped from platform-specific
  status columns, labels, sections, or custom fields
- `task_goal`: the organizational goal lineage that justifies the task

Keep provider nouns in raw payloads and wrapper methods. Generic adapters use
Wielder nomenclature; temporary compatibility bridges should be named and
removed once callers migrate.

## Organizational Surfaces

Task management often needs several systems to act together:

- Task managers: create/update work items, states, owners, reviewers, links,
  QA gates, and dashboards.
- Messaging: send concise Slack/email notifications, requests, escalations,
  and handoff summaries.
- Documentation: produce or update Docs, Drive artifacts, Markdown, reports,
  Lucidchart diagrams, slide decks, or other human-readable records.
- Charting/reporting: generate Python charts, tables, diagrams, or PDFs when
  those artifacts make status and QA easier to inspect.
- Code/repo systems: link task items to branches, diffs, commits, PRs, logs,
  and verification commands without duplicating the code review workflow.

Each surface should be selected and parameterized by configuration. Board IDs,
channel names, document destinations, and reviewer mappings belong in config.

## Task Shape

When projecting work into a platform, preserve these fields where the target
system can represent them:

1. Goal: the organizational result.
2. Scope: included and excluded work.
3. Owner: person or agent responsible for progression.
4. Reviewer or QA role: person/group responsible for acceptance.
5. State: proposed, exploratory, in progress, blocked, pivoted, QA handoff,
   done, archived, or a configured local equivalent.
6. Artifact: code path, report, Drive link, chart, document, command, or task
   URL that proves progress.
7. Verification: the smallest live command, QA checklist, or inspection route.
8. Handoff: the next human action required.

Configure a mapping that preserves the semantics with the least distortion the
platform allows.

## Operating Discipline

Prefer:

- Wielder actions and HOCON config for modes, destinations, provider choice,
  task-space identity, and routing.
- The Wielder scripting rule that CLI modulates and config configures; durable
  platform identity, routing, mappings, templates, and notification choices
  belong in resolved config whenever Wielder can own them.
- API/MCP/connector reads before writes, so the current platform shape is known.
- `plan`/`probe` commands before mutating external systems.
- live integration checks when the value is external-system confidence.
- concise human output with exact links, task IDs, and verification commands.

## Planning Scratch Files

For exploratory implementation planning, create a local ignored Markdown scratch
file named `<task_name>_stam.md`. Keep it concise and update it as the task
evolves.

Use the scratch file for:

- operator-alignment notes
- current plan and scope boundaries
- open questions or decisions
- implementation checkpoints
- verification commands
- handoff notes

Promote stable conclusions into versioned docs, skills, config, or code. Keep
the `_stam.md` file as local planning state.

Keep Out Of The Main Path:

- broad browser automation where API/MCP access is available
- generic abstractions that erase platform capabilities
- provider-specific nouns in Wielder generic interfaces
- duplicating tasks, docs, or notifications instead of replacing/updating the
  configured canonical artifact

## QA And Handoff Reports

QA handoff reports are concise, linked artifacts for humans who need to verify
an outcome.

Use a canonical Markdown source when the report should live with project
artifacts or feed later RAG/search. Publish a human-facing document only when
needed for Drive, Monday, Slack, email, or a similar workflow.

The concise handoff shape is:

```markdown
# QA Handoff: <source/task> -> <target/system>

**Status:** Ready for QA
**Date:** <date>

## Summary

<One short paragraph saying what was completed and for which supported scope.>

## QA Scope

- <source links>
- <target links>

## QA Checklist

Confirm that:
- <expected artifact/record/value>
- <relationship or status>
- <known exception handling>

## QA Outcome Needed

Please report mismatches, missing records, incorrect linkage, or confirmation.
```

Keep handoffs short and linked. Include implementation logs or full manifests
only when QA needs them directly.

## Final Task Report

Final responses should name:

- what changed
- which configured platform/surface was used
- where the platform artifact lives
- what command or live check verified it
- what remains intentionally out of scope

Mention explored paths only when they left an artifact, affected risk, or
explain necessary cleanup.
