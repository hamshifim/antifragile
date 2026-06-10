---
description: Domain Scope & Boundary Preservation Constants
---
[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

 Scope Enforcement & Boundary Constants

- **Domain Jurisdiction**: The Workspace workspace hosts multiple adjacent submodules (e.g., `pep-services`, `domain-data`, `culture_astrophysics`). You MUST strictly quarantine your code changes directly to your mathematically assigned execution domain to prevent catastrophic git merge conflicts.
- **Scope Creep Prohibition**: Do not attempt to "boil the ocean". Do not arbitrarily refactor adjacent scripts or files simply because you see aesthetic flaws while executing an isolated task. If a flaw exists outside your specific architectural parcel, document it logically and request explicit user authorization to branch execution boundaries.
- **The "Einstein Simplicity" Mandate**: Actively pursue the most straightforward, explicit architectural approach natively supported by the `workspace` PyHocon configuration infrastructure. You MUST explicitly reject over-engineered abstraction layers, custom python wrappers, or deeply nested class architectures unless strictly ordered. Code must remain "as simple as possible, but not too simple."
- **Epistemic Humility in Scope**: Never assume your execution logic "guarantees" vast system stability. Design schemas probabilistically; actively isolate domains so that a failure in one algorithmic node inherently contains the blast radius safely away from the global execution pipeline.
