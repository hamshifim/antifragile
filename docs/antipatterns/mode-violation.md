---
name: The Mode Violation Antipattern
description: Defining the catastrophic structural failure that occurs when orchestration layers natively evaluate domain mode strings (e.g. stage_tier) rather than explicitly deferring to PyHocon overrides.
---

# The Mode Violation Antipattern

In a secure distributed Wielder ecosystem, execution pipelines scale gracefully because configuration resolution is entirely decoupled from Python orchestration scripts. 

## The Violation
A **Mode Violation** occurs when an engineer organically intercepts and parses a "Domain Mode" structural mapping natively inside Python logic to construct structural evaluation loops, rather than shifting the data array securely inside PyHocon `.conf` matrices. 

**Example of the Antipattern (Python Layer):**
```python
# CATASTROPHIC ANTIPATTERN
if conf.stage_tier == "prod":
    target_database = "uniref90"
elif conf.stage_tier == "dev":
    target_database = "mock_uniref90"
```

### Why It's Catastrophic
1. **Splintering Source of Truth**: The architectural bounds are no longer centralized in the Configuration layer; they are scattered across fragmented python deployment blocks.
2. **Hidden Masking Behaviors**: If a system dynamically expands to a `qa` or `load_test` stage_tier, the python orchestration will implicitly fall back or violently crash because the domain modes were hardcoded.
3. **Breach of the "Fail-Closed" Protocol**: An explicit configuration override tree mathematically maps what happens upon domain shifts. Putting "default" fallback parameters natively inside an `if/else` block completely shatters the strict PyHocon MissingKey evaluation.

## Violation 2: Domain Misalignment (Mode Bleeding)
A secondary vector for a **Mode Violation** occurs when engineers physically place configuration attributes into the wrong Domain Mode hierarchy, polluting the clear boundary abstractions.

**Example of Mode Bleeding:**
- Injecting `stage_tier` execution scaling structures (e.g. `mock_database` paths) natively into the global `ecosystem_manifest.conf`.
- Injecting `security` or RBAC constraints natively into a `stage_tier` block.
- Injecting local execution geometric boundaries natively into the Application Baseline `app.conf`.

### Why It's Catastrophic
While PyHocon correctly merges these variables regardless of where they sit, polluting the domains shatters the cognitive abstraction. It forces engineers to hunt across 4 separate domains to trace where a rogue database variable is leaking from.

## The Solution
Structural logic branching must NEVER evaluate Domain Modes natively inside the DAG or Pipeline. Furthermore, when creating PyHocon parameters:
1. The raw `app.conf` sets strict baseline geometric and fundamental parameters (`target_database = "uniref90"`).
2. The `stage_tier/` domains explicitly override deployment boundaries, mock testing, and operational scale limits.
3. The `ecosystem/` domains explicitly govern cross-architecture network bindings, cloud integrations, and OS pathing geometry.
4. The orchestration layer simply pulls the variable natively (`conf.target_database`) without evaluating conditional boundaries.
