# Runtime Event Logging

Use this skill when instrumenting long-running workers, Kafka consumers, Spark jobs, Wielder job launchers, or any runtime where ordinary line-by-line logs hide the actual lifecycle.

## Contract

- Log lifecycle boundaries as framed runtime events with a blank line before and after the block.
- Prefer explicit event names: `Job Received`, `Job Started`, `Busy Heartbeat`, `Job Finished`, `Job Failed`, `Consumer Stopped`.
- Include stable identifiers in every event: job name, run UUID, sequence set UUID, topic/partition/offset, batch/context, worker count, or Spark step ID as applicable.
- Use colored ANSI titles only where logs are human-facing and tolerate ANSI; honor `NO_COLOR`.
- Emit periodic busy heartbeats for long work so a quiet log means idle, not dead.
- Keep machine state in existing status topics/registries; event logs are for operator diagnosis and should not become a second state store.

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
