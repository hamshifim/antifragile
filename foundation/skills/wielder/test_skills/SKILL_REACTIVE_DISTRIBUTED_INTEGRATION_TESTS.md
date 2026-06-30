---
name: Reactive Distributed Integration Testing
description: Guidance for building live integration tests for any distributed reactive flow: storage events, topics, queues, jobs, callbacks, fanout, downstream ingestion, and human-readable progress reports.
---


# Reactive Distributed Integration Testing

A reactive integration test proves a flow of information across nodes. It is not a unit test, and it is not a log scrape.

Use this skill when work moves through storage, events, queues, jobs, callbacks, services, or downstream ingestion.
When the flow includes bucket objects, table outputs, storage events, artifact roots, provider URIs, or cleanup, also read [Strict FS Agnosticism](../data_skills/SKILL_STRICT_FS_AGNOSTICISM.md).

## First Principles

- Name the flow in plain language.
- Trigger the highest real upstream event the mode can safely support.
- Describe each node in the simplest natural language terms.
- State what each node is waiting for and what evidence will satisfy it.
- Send a small provenance nugget at the source and carry it forward when possible.
- Build a state report as the flow progresses.
- Log meaningful events and print the human report between waits.
- End with a final accumulated report: passed, failed, skipped/no-change, or interrupted.

## Flow Nodes

Model the flow as observable nodes, not implementation trivia.

Good node labels:
- `Source file accepted`
- `Storage event observed`
- `Mirror job completed`
- `Destination file found in S3`
- `Downstream ingestion accepted`

Poor node labels:
- `Python script ran`
- `Destination blobs present`
- `Workflow complete`
- `Logs looked okay`

Each node should declare:
- the plain-language meaning;
- the exact resource or event expected;
- the wait condition;
- the timeout or no-change rule;
- the URL or location a human can inspect.

## Provenance Nugget

At the upstream trigger, create or preserve a tiny identity payload:

- `run_id` or `request_id`;
- source actor or entrypoint;
- created-at timestamp;
- source object, key, URL, or event id;
- mode context if relevant.

Carry that nugget through event envelopes, job environment, emitted messages, reports, and cleanup records. If a boundary cannot carry it yet, say so in the report and use the weakest honest fallback, such as time-bounded evidence.

## State Report

The report is part of the test interface.

It should show:
- current status;
- numbered nodes;
- node status: `pending`, `working`, `done`, `skipped`, `manual`, or `error`;
- what is being waited for now;
- what was checked and when;
- exact source and destination locations;
- useful URLs on their own lines;
- first actionable failure reason.

Print the report repeatedly during long waits, not only at the end. The operator should be able to tell whether the test is progressing, waiting correctly, or stuck.

## Logs

Logs should explain state transitions, not drown the report.

Good logs:
- `waiting for S3 object-created event for run_id=...`
- `checked s3://bucket/prefix/file.xlsx at 10:41:33Z: missing`
- `mirror job completed with no new source files; downstream skipped`

Avoid raw provider output as the main user signal. Capture it in records if useful; keep the visible stream human-oriented.

## No-Change And Skips

No-change is a real result.

If the upstream spring finds nothing new, mark downstream nodes as `skipped` with a reason. Do not leave them pending.

If policy or config prevents a step, mark it `manual` or `skipped` and state the flag or config path that caused it.

## Cleanup

Cleanup should be explicit and configurable.

If cleanup is testing propagation, it gets its own nodes. If cleanup is just test hygiene, the test should clean its own watermarked artifacts through the configured Wielder/accessor cleanup path and report what it removed. `plan-delete` should show the exact watermarked resources first; `delete` should remove only those resources. Do not let cleanup ambiguity obscure whether the main flow passed, and do not use `/tmp` output roots as a substitute for configured dev-tier cleanup.

## Reactive Fixture Hygiene

Topic, queue, and callback fixtures are part of test state. A fixture-backed
reactive test should clear the whole message family that can affect the flow:
request topics, result/update topics, command topics, post-action event topics,
and any configured callback groups. Do this before seeding fixture artifacts and
before starting long-lived consumers.

This matters most when consumers use `earliest` replay or explicit
assign-from-beginning semantics. A stale command from a previous run can mutate
freshly seeded artifacts and make the failure look like a missing download,
broken downstream app, or storage race. Treat stale messages as live state, not
log history.

For reactive cleanup, publish an explicit command and wait for a post-action
event. Subscribe before publishing when collecting the result. Each service
should clean only the resources it owns; downstream cleanup should not cascade
through an upstream service's storage unless the upstream service contract says
so. The final report should say which transport produced the cleanup evidence
and which configured keys or records were affected.

## Minimal Checklist

- One controlled upstream trigger.
- One provenance nugget.
- One shared flow/node contract usable by tests, workflow runs, and GUI monitors.
- One node per observable boundary.
- Whole reactive fixture family cleared before seeding and starting consumers.
- A state report accumulated during the run.
- Meaningful logs that say what is expected next.
- Clear skipped/no-change behavior.
- Final human report plus machine-readable JSON/JSONL when useful.
