---
description: Convex, evidence-first planning for evolving operating systems toward antifragility without pretending aspiration is done. Inspired by Grill Me, extended with config forensics, maturity honesty, and convex sequencing.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.
[Read Grill Me](SKILL_GRILL_ME.md) — this skill is its antifragile extension and inherits its plan/execution boundary.

# Antifragile Planning

Use this skill when planning a change to a system that **already operates**: a working app, pipeline, or service that has drifted from doctrine, accrued risk, or needs to evolve. Grill Me reaches shared understanding of a plan; Antifragile Planning adds the bias that makes the plan safe to execute on living infrastructure — convex sequencing, maturity honesty, and config-truth forensics.

This is a planning skill. It may inspect code, config, scripts, tests, and command output, and it produces or updates planning markdown. It must **not** implement product/code/config changes merely because the plan names them. Execution begins only after a separate, explicit implementation instruction once the plan is stable. During planning, "add", "use", "create", "wire", "migrate", "rename" describe the desired plan, not applied changes.

## Core stance: plan convexly

Antifragility is convex exposure — cheap if a bet stalls, large if it pays off. Planning inherits this. Order the work so that:

- Early steps are **cheap, reversible, and high-certainty** (hoist imports, route inline keys through an existing accessor, replace `os.path.join` on storage keys). They reduce risk immediately and cannot make things worse.
- High-blast-radius or structural steps (identity renames, schema moves, accessor widening) come **later, behind explicit validation gates**, never first.
- Each step is independently shippable and independently revertible. A plan that only pays off if every step lands is fragile; decompose it until partial completion is still net-positive.

Prefer `delete -> apply` reproducibility as the proof that a change can be reconstructed from committed source, not just patched into place.

## Maturity honesty (load-bearing)

Tag every claim and every plan item by maturity. Collapsing the gap between what operates and what is wished-for is itself an antipattern (it is how "deterministic source repair" gets mistaken for a working feature).

- `OPERATING` — in production use today, proven under real workloads.
- `EMERGING` — partially built, evolving under production pressure, not yet trustworthy unsupervised.
- `ASPIRATIONAL` — intended direction, not yet real. Wishful by honest admission.

When planning a change to `OPERATING` code, say so: the goal is to preserve operating behavior while paying down drift. Never let a planned step read as already-done. Never describe a stochastic actor (an agent, an LLM node) as "deterministic" — only the committed substrate (policies, thresholds, accessors, rollback boundaries) is deterministic; the actor inside it is not.

## Protocol

1. **Inspect before asking — including config truth.**
   - Answer from the repository first: code, HOCON, scripts, docs, tests, existing command output. Do not ask the operator to restate facts present in source.
   - Run **plan-first config forensics** before proposing code edits: resolve the nearest canonical accessor (`get_app_conf(...)`, `get_service_conf(...)`, `-w plan`) and compare the surprising field across the smallest useful chain of surfaces. The first divergence names the ownership layer that needs repair. Do not plan a Python patch to hide a wrong resolved value — that is config laundering.

2. **Ask exactly one question at a time.** Concrete, single-decision. Explain why it matters only when non-obvious. Do not bundle decisions.

3. **Include a recommended answer**, formatted `Recommended answer: ...`, grounded in inspected evidence (label inferences as such). Pressure-test the operator's preference against independent architecture before recommending it — shared understanding is not uncritical agreement.

4. **Wait for the operator.** Do not advance until they answer or skip. After each answer, update the plan state in one or two lines, then ask the next question.

5. **Stop when the shared understanding is actionable.** Converge into a planning markdown file (see Output). End with decisions, ordered convex steps, file targets, validation commands, maturity tags, and unresolved risks.

## Independent architecture + antifragility lenses

Before asking or recommending, pressure-test the plan briefly through these lenses. Do not roleplay them at length.

Grill Me lenses — system boundary, data contract, operability, failure semantics, migration path, provider fit — plus:

- **Convexity:** Is this step cheap-and-reversible or expensive-and-sticky? Is it sequenced accordingly?
- **Blast radius:** What is the worst case if this step is wrong, and is it gated behind validation that would catch it? Prefer the **narrowest mechanism that achieves the goal**. Worked example: changing a canonical `app.conf` baseline propagates to every consumer of that app across every ecosystem (wide, sticky blast radius); expressing the same intent as a local override in the active `context_conf/<name>/developer.conf` pack is narrow and reversible. Reach for the canonical edit only when the change is genuinely durable and shared — and never satisfy "narrow" with a gnostic side-loader or parallel reader (that trades blast radius for a hidden second source of truth, which is worse).
- **Source of truth:** Does the change keep one canonical accessor / one resolution order, or does it spawn a parallel config boot path (a "gnostic config")?
- **Maturity honesty:** Is any item being described as more done than it is?
- **Reproducibility:** Can the result be rebuilt from committed source via `delete -> apply`, or only by re-patching?

If an answer optimizes one lens while damaging another, say so directly and propose the smallest correction.

## Output: planning markdown

Converge into a markdown file near the target code or owning app.

- `*_stam.md` — **ignored scratch** alignment plan (matches the repo `*stam.*` gitignore). Use for transient planning that should not be versioned.
- `*_task.md` — **versioned** when the plan is intended to become durable repository doctrine.

The file should contain:

- **Goal** and the maturity of the thing being changed (e.g. "harden an `OPERATING` pipeline").
- **Inspected evidence** — concrete file:line findings, resolved config values, forensic comparisons. Cite, don't assert.
- **Findings / drift** — each tagged with the doctrine it violates and a severity.
- **Decisions reached** vs **open questions** (queued in one-question-at-a-time shape with recommended answers).
- **Convex step order** — cheap/reversible first, structural/high-blast-radius last behind gates.
- **Planned files** — touched paths, as plan, not applied edits.
- **Validation commands** — the lightest action that proves each step (`plan`, `show`, focused tests, accessor resolution dumps).
- **Open risks / blocked decisions.**

The markdown is the artifact produced *after* understanding stabilizes; it does not replace the one-question-at-a-time protocol.

## Hold the line during execution

The plan is a contract. Once execution begins (under a separate explicit instruction), **do not diverge from the agreed plan or from canon mid-implementation without consulting the operator.** Drift discovered while building is normal — acting on it unilaterally is the failure.

When implementation reveals that the plan or the canonical contract is wrong, incomplete, or in the way:

- **Stop and pitch, do not pivot.** Surface the mismatch, the proposed deviation, its blast radius, and the smallest alternative. Resume only after the operator authorizes the new direction.
- This applies most sharply to **architectural bypasses and shared-framework (SDK/canon) mutations**, scope expansion beyond the agreed steps, and "while I'm here" refactors. A canonical change reached *during* implementation deserves the same planning rigor as one reached during planning — more, because the blast radius is now live.
- Reshaping the shared layer to fit a local inconvenience is exactly the move to escalate, not to make quietly.

## Antipatterns to avoid

Plan and execute against these explicitly. Each is a structural failure mode this skill exists to prevent:

- [Premature Execution](../../../docs/antipatterns/premature-execution.md) — leaving plan-only bounds and starting to build on artifact approval. The plan/execution boundary above is its direct defense.
- [Unilateral Bypass](../../../docs/antipatterns/unilateral-bypass.md) — deploying an architectural bypass or SDK/canon mutation without pitching and securing authorization. The "hold the line" rule above is its direct defense.
- [Context Drift](../../../docs/antipatterns/context-drift.md) — high-velocity scope/fact hallucination. Defended by inspect-before-asking and citing evidence.
- [Style Drift](../../../docs/antipatterns/style-drift.md) — unconsciously regressing idiosyncratic code toward training-set norms. Watch for it during any refactor step.
- [Mode Violation](../../../docs/antipatterns/mode-violation.md) — acting outside the currently sanctioned operating mode.
- [Hard-Stopping](../../../docs/antipatterns/hard-stopping.md) — stunting capability with permanent bans instead of explicit, bounded skill wrappers.
- [Known Codex Unwanted Tendencies](../../../docs/antipatterns/known_codex_unwanted_tendancies_antipattern.md) — gnostic CLIs, environment-variable side channels, and CLI-override wrapping.

## Repository discipline

- Prefer existing local abstractions and configured entrypoints over new wrappers.
- Keep source/sink paths and credentials configuration-driven; CLI is modulation, config is configuration.
- If a plan implies a new framework abstraction, first ask whether the repeated use case is broad enough to justify it.
- When repeated operator corrections converge into doctrine, pair with [SKILL_OPERATOR_ALIGNMENT.md](SKILL_OPERATOR_ALIGNMENT.md) and promote settled decisions into task markdown, docs, config, tests, or glossary — not just conversation.
