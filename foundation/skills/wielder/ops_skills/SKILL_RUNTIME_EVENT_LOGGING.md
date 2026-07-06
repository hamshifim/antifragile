# Runtime Event Logging

Use this skill when instrumenting long-running workers, Kafka consumers, Spark jobs, Wielder job launchers, model inference, black-box subprocesses, or any runtime where ordinary line-by-line logs hide the actual lifecycle.

## Contract

- Log lifecycle boundaries as framed runtime events with a blank line before and after the block.
- Prefer explicit event names: `Job Received`, `Job Started`, `Busy Heartbeat`, `Job Finished`, `Job Failed`, `Consumer Stopped`.
- Include stable identifiers in every event: job name, run UUID, sequence set UUID, topic/partition/offset, batch/context, worker count, or Spark step ID as applicable.
- Use colored ANSI titles only where logs are human-facing and tolerate ANSI; honor `NO_COLOR`.
- Emit periodic busy heartbeats for long work so a quiet log means idle, not dead.
- Keep machine state in existing status topics/registries; event logs are for operator diagnosis and should not become a second state store.
- Include `started_at` and `finished_at` in durable run reports when a run owns a prediction, model call, job, or black-box subprocess.
- Publish status events for long model or black-box work: start, heartbeat, finish, failure, reuse/skip. Publishing must be best-effort and must not crash successful domain work.
- Keep topic names, consumer groups, heartbeat intervals, and enabled flags in HOCON. Do not invent ad hoc CLI switches or environment variables for observability.

## Generic Model And Black-Box Runs

Use this pattern when the app wraps a model, binary, notebook-derived script,
Spark step, or provider job whose internals are opaque to the Wielder layer.
The domain runner may treat the work as a black box, but its lifecycle must be
observable.

A black-box run should expose:

- resolved input identity: request UUID, run UUID, batch key, sequence set, project key, or equivalent
- resolved output identity: bucket, key path, artifact directory, report path, and minimum success marker
- command or invocation preview when safe to show
- start status before the expensive call begins
- heartbeat status while the expensive call is still active
- finish status with elapsed time and output evidence
- failure status with the exception class, exit code, stderr/log pointer, and partial output evidence when available
- reuse/skip status when an existing success marker prevents recomputation

The status payload should be a typed contract such as `WorkStatusEvent`, not a
raw log string. A monitor should be able to subscribe to the configured status
topic and tell a human what is running, where outputs will land, and whether the
worker is still alive.

## Runtime Stats

When runtime pressure matters, collect local stats at start, heartbeat, and
finish. Stats are diagnostic context, not domain truth. The collector should
live in Wielder or another shared upstream utility so each model app does not
grow its own `nvidia-smi`, `/proc`, or OS-specific probing code.

Use `wielder.util.runtime_stats.collect_runtime_stats` for local CPU, memory,
swap, disk, GPU, heat, platform, and process diagnostics. It accepts the
resolved `runtime_stats` HOCON subtree through its typed
`RuntimeStatsConfig`, returns a JSON-safe `RuntimeStatsSnapshot`, and returns
`None` when disabled or when the current phase is not included.

Collect stats best-effort:

- CPU load and process CPU where available
- memory and swap usage
- disk usage for configured output and cache paths
- GPU name, utilization, memory, temperature, and power where available
- thermal data where the OS exposes it
- process identity for the main model process when it can be known safely

Stats collection must be optional and fail-soft. Missing `nvidia-smi`, missing
NVML support, unavailable sensors, WSL limitations, or unsupported cloud
metadata should appear as absent fields or warnings in the status payload, never
as failed model work.

Prefer a config shape like:

```hocon
<app>.runtime.work_status {
  enabled = true
  interval_seconds = 30.0
  topic_key = "<app>_status_events"

  runtime_stats {
    enabled = true
    include_on = ["start", "heartbeat", "finish"]
    disk_paths = [${local_buckets_root}]
    gpu = true
    cpu = true
    memory = true
    swap = true
    heat = true
  }
}
```

Use test overlays to shorten intervals or disable expensive probes. Do not
disable lifecycle status in tests unless the test is explicitly a unit test that
does not exercise runtime behavior.

## Workspace Pattern

For Workspace Python runtimes, prefer:

```python
from workspace_in_silico.core.runtime_event_log import runtime_event

runtime_event(
    logger,
    "Model Job Received",
    {
        "job": raw_dag["name"],
        "sequence_set_uuid": raw_dag["sequence_set_uuid"],
        "run_uuid": raw_dag["run_uuid"],
    },
    color="cyan",
)
```

Do not replace exceptions with pretty logs. Emit the framed failure event and keep `logger.exception(...)` so stack traces remain visible.
