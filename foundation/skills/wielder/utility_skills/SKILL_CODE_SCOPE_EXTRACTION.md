---
name: Code Scope Extraction
description: Extract reusable Wielder code only after a stable seam is visible, preserving app ownership and avoiding premature SDK drift.
---

[Read the configuration guidelines](../config_skills/SKILL_CONFIGURATION_GUIDELINES.md) before
moving code between an app, project wielder, and Wielder.
[Read the scripting guidelines](../script_skills/SKILL_WIELDER_SCRIPTS.md) before changing an
entrypoint shape.

# Code Scope Extraction

Use this skill when a working app has accumulated useful code that might belong
in a reusable SDK layer.

## First Principle

Extraction is not a cleanup reflex. It is a scope decision. A reusable helper
belongs upstream only when the caller contract is stable, the boundary is clear,
and at least one plausible second client would use the same behavior without
absorbing the first app's domain vocabulary.

## Extraction Ladder

1. Keep the first working version local and explicit.
2. Name the repeated behavior in a project-local helper if it repeats inside the
   same project.
3. Extract to Wielder only after the helper no longer mentions the app domain,
   bucket names, project names, concrete topics, image names, or service-specific
   lifecycle policy.
4. Preserve the app as the owner of app-specific config, typed contracts, and
   lifecycle sequencing.

## Good Candidates

- Generic image existence/build orchestration around an already resolved image
  name and tag.
- Generic resolved-config publication primitives.
- Generic provider auth probing where the provider contract is already typed.
- Generic snapshot or disk accessors once provider-specific identifiers and
  ownership are explicit inputs.

## Bad Candidates

- Helpers that synthesize missing config.
- Helpers that hide an app's topology by rereading HOCON files.
- Helpers that move domain policy into Wielder because one app currently needs
  fewer lines.
- Helpers that require Wielder to know project-specific service names, model
  names, viewer names, bucket names, or domain vocabulary.

## Review Gate

Before extracting, write the proposed upstream function signature and answer:

- Which layer owns every input?
- Which layer owns every output?
- What concrete second client would call this without adaptation?
- Does the helper validate a typed contract, or does it manufacture one?
- Does this make plan-mode evidence easier to read?

If the answer is fuzzy, keep the code local and leave a TODO naming the possible
future seam.
