---
description: Shared package-level Wielder skill guidelines for cross-cutting rules that individual skills should reference rather than repeat.
---

# Package Guidelines

Use this skill for cross-cutting Wielder skill-package rules that apply across
many skills and would distract if copied into each one.

Individual skills should link here with a short reminder instead of duplicating
package-level doctrine.

## Cloud And Connector Auth Boundary

If cloud auth, MFA, OAuth, connector auth, or session expiry blocks a cloud or
platform operation, stop and ask the operator to refresh credentials or confirm
the intended profile.

Do not patch around expired auth, add ad hoc credential plumbing, bypass MFA,
persist temporary tokens, or keep retrying.
