---
description: Preserve task ownership and scope while changing Wielder projects and their shared dependencies.
---

# Scope and Ownership

Work in the repository and domain that own the requested behavior. Inspect
existing changes before editing, and preserve unrelated operator or agent work.

Follow a change through its necessary callers, configuration, tests and
documentation. Crossing a repository boundary can be part of one cohesive task;
it does not authorize unrelated refactoring.

When an adjacent issue is outside the task, report it separately. Ask before a
material expansion of scope, new external action or consequential change of
architecture.

Prefer the simplest design supported by the existing Wielder abstractions.
Helpers and wrappers are justified when they remove demonstrated duplication
or clarify ownership; they are not categorically forbidden. See
[Einstein Simplicity](SKILL_EINSTEIN_SIMPLICITY.md).

Describe validation at the level actually exercised. A passing local check
does not establish the stability of an entire distributed system.
