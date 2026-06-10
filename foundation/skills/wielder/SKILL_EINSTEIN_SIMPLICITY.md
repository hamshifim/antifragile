---
description: Simplicity discipline for distributed Workspace orchestration
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Einstein Simplicity

Complex distributed systems create a strong temptation to solve every new wrinkle by adding one more wrapper, one more entrypoint, or one more config axis. Most of the time that is the wrong move.

## Rule 1: Keep the Outer Layers Thin
- App entrypoints should load config, instantiate accessors/runners, and dispatch work.
- If an app entrypoint starts encoding distributed dependency choreography, stop and ask whether that logic belongs in the runner or service layer instead.

## Rule 2: Branch Once, Near the Boundary
- When a system supports multiple execution topologies such as local SDK and direct API transport, make the branch once at the dependency boundary.
- Do not let that branching logic leak upward into every caller.

## Rule 3: Let the Responsible Layer Own the Decision
- If a runner already owns dependency resolution, the topology branch likely belongs in the runner.
- If a transport adapter already owns side effects, callers should not duplicate them.
- Avoid adding helper entrypoints whose only purpose is to compensate for logic placed in the wrong layer.

## Rule 4: Prefer Convergence over Coordination
- Shared cores should stay pure.
- Shared side-effect layers should own canonical external effects.
- Multiple orchestrators should converge on those layers rather than coordinate through duplicated glue code.

## Rule 5: New Terms Must Reduce Confusion
- If a new abstraction does not clearly reduce confusion, do not add it.
- Prefer reusing existing topological concepts when they already express the distributed shape cleanly.

## Practical Heuristic
- Fewer entrypoints
- Fewer special-case wrappers
- One place for the branch
- One place for the side effects
- One place for config truth
