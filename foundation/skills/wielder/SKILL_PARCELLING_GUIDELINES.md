---
description: Stepping Stone Parcelling & Incremental Implementation Strategy
---
[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

 Parcelling Strategy (The Stepping Stone Protocol)

- **Anti-Monolith Mandate**: Never attempt massive, multi-file execution refactors or sweeping architectural deployments in a consolidated single pass. ALL goals MUST be aggressively parcellized into atomic "Stepping Stones".
- **The Atomic Stepping Stone Definition**: 
  1. Contains exactly **one** cohesive logical or structural implementation task.
  2. Culminates explicitly in a standalone, executable live QA integration step (e.g., a specific `pytest` assertion output or an explicit notebook visual).
  3. Acts as an impenetrable workflow barrier; you MUST NOT move to Step `N+1` until Step `N` is physically proven green and formally handed through the Agentic Adversarial Workflow loop.
- **Intrinsic QA Verifiability**: A stepping stone parcel is utterly invalid if it fails to explicitly define how the Red Team QA Architect persona will technically verify its success from the physical state layer.
- **Graceful Pausing**: Each defined parcel intentionally halts the active execution loop. The entity must consciously sever its pipeline context, assume the hostile QA persona, and critically evaluate the mathematical differential before progressing laterally.
