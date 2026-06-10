---
description: Naming doctrine v2: layered semantics, operational clarity, and enforceable review heuristics
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Wielder Master Skill: Naming Doctrine v2

## Purpose
This guideline defines how to name symbols so humans can infer intent, risk, and action quickly across design, implementation, incident response, and handoff.

The objective is not naming purity. The objective is situated intelligibility.

## Core Principle
Names must represent the most relevant truth for their layer:

- Domain truth for business/scientific modeling.
- Operational truth for protocol boundaries and adapters.
- Infrastructure truth for platform/runtime mechanics.

## Layered Naming Model

### 1) Domain Layer (Business/Science/Pipeline Logic)
Use domain-centered names that encode semantics.

- Prefer: `cohort_demographics`, `harmonized_patient_matrix`, `target_hit_candidates`
- Avoid: `df`, `data_list`, `result_array`, `tmp_payload`

### 2) Operational Layer (Boundaries, IO, Protocols, Contracts)
Use mechanism-aware names when crossing technical boundaries.

- Prefer: `http_headers`, `request_payload_json`, `grpc_metadata`, `cli_args`, `retry_policy`
- Avoid: over-domainizing boundary objects that hide protocol behavior

### 3) Infrastructure Layer (Runtime/Platform Internals)
Use platform-accurate names for execution mechanics.

- Prefer: `subprocess_args`, `env_vars`, `mount_path`, `queue_offset`, `pod_selector`
- Avoid: pseudo-domain naming that obscures implementation responsibility

## Rule Set (Enforced in Review)

### Rule A: Name by Layer, Not by Habit
If code sits in a domain module, choose domain semantics.
If code sits in adapters/runtime/protocol handling, choose operational or infrastructure semantics.

### Rule B: Ban Ambiguous Placeholder Names
Disallow generic placeholders except in tiny local scopes (<= 5 lines).

- Disallowed: `data`, `obj`, `item`, `tmp`, `stuff`, `value`, `thing`
- Disallowed in persistent scope: `df`, `df1`, `new_df`

### Rule C: Require Boundary State in External Coordinates
Any symbol that crosses filesystem/object-store/network boundaries must encode state and medium where relevant.

- Prefer: `raw_origin_payload_uri`, `staging_manifest_path`, `generation_sandbox_key`
- Avoid: `path`, `file`, `uri` without qualifiers

### Rule D: Mechanism Terms Are Allowed When Mechanism Is the Domain
Words like `payload`, `headers`, `args`, `path`, `dict`, `json` are acceptable in operational/infrastructure layers when they improve precision.

### Rule E: Avoid Type-Suffix Theater
Do not append type suffixes purely out of habit (`_dict`, `_list`, `_array`) unless needed to disambiguate two nearby symbols with different structural roles.

## Exceptions (Explicitly Allowed)

1. Notebook scratch scope: short-lived exploration symbols may be concise when confined to one cell and not persisted.
2. Algorithmic conventions: mathematically standard variables (`x`, `y`, `t`, `n`) are allowed inside tightly scoped numeric code.
3. External API parity: keep upstream field names when mirroring third-party specs/contracts.
4. Generated code: do not manually normalize generated symbol names unless post-processing is already part of the build pipeline.

## Severity Model for Reviews

### SEV-1 (Blocker)
- Name misrepresents layer truth and can cause unsafe action.
- Boundary variable lacks state clarity and risks data loss/routing mistakes.
- Ambiguous naming in provenance/audit/security-critical paths.

### SEV-2 (Must Fix Before Merge)
- Persistent generic placeholders (`df`, `data`, `obj`) in non-trivial scope.
- Inconsistent naming within the same module boundary.
- Type-suffix noise that reduces readability.

### SEV-3 (Improve Soon)
- Verbose but understandable names needing simplification.
- Minor drift from module-local naming patterns.

## CI-Checkable Heuristics (Recommended)
These are heuristics, not complete semantic proof.

1. Flag banned placeholders in persistent scope:
   - `\b(df|df\d+|data|obj|item|tmp|thing|stuff)\b`
2. Flag unqualified boundary coordinates:
   - `\b(path|file|uri|key)\b` unless prefixed/suffixed with state qualifiers (`raw`, `staging`, `processed`, `manifest`, `origin`, `sandbox`).
3. Flag habitual type suffixes:
   - `(_dict|_list|_array)\b` (warn-only unless disambiguation is justified in review notes).

## Reviewer Checklist (Fast Audit)

1. What layer is this symbol in: domain, operational, or infrastructure?
2. Does the name encode the most important truth for that layer?
3. Could a new engineer take the correct action from this name in context?
4. For boundary symbols, is state/location explicit enough to prevent routing mistakes?
5. Is any exception used intentionally and locally contained?

## Case Study: `subprocess_args`

- In an infrastructure adapter module, `subprocess_args` is acceptable and often preferred.
- In a domain orchestration module, prefer semantic framing such as `model_execution_flags` when the list primarily expresses business/pipeline intent.

Final rule: choose names that maximize human comprehension and safe action in the local architectural context.
