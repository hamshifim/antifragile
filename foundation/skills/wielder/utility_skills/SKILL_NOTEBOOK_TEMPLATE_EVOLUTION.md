---
description: Reuse, improve, and instantiate versioned exploration-notebook templates without suppressing new scientific questions or duplicating scientific calculations.
---

# Antifragile Notebook Template Evolution

Use this skill when creating, repairing, extending, or instantiating an
exploration notebook whose analysis shape may already exist elsewhere.

## Goal

Treat notebooks as an evolving family of reader-facing views over frozen
evidence. Reuse proven structure, improve it when a reusable weakness is found,
and create a new variant only when the scientific question or evidence contract
is genuinely different. A template accelerates inquiry; it must not shackle a
new question to the wrong analysis.

## Required workflow

1. Inventory nearby versioned templates, companion scripts, WET experiment
   copies, reusable renderers, and frozen evidence contracts before writing a
   new notebook.
2. State the question and required evidence contract. Select the closest
   template whose scientific calculation and representation actually match.
3. WET-copy that template into the configured experiment key. Change selectors,
   human-readable labels, and question-specific explanation without silently
   changing the scientific calculation.
4. If the experiment reveals a reusable presentation or validation improvement,
   repair the versioned template and shared renderer, then rematerialize the WET
   copy. Preserve experiment-specific findings in the WET copy.
5. If no template honestly fits, add a clearly named versioned variant. Reuse
   shared components while keeping the distinct question and evidence contract
   explicit.
6. Execute the companion script first, generate the notebook with the Wielder
   converter, execute it against real artifacts when available, and visually
   inspect the rendered outputs.

## Scientific boundary

- Heavy preparation, centroid construction, distance scoring, permutations,
  support decisions, and scientific selection belong upstream in a versioned
  evidence pipeline.
- A notebook selects and renders frozen evidence. It must not recompute a
  scientifically different answer in an interactive cell.
- Missing evidence must remain visibly missing. Never substitute pooled values,
  another cohort, or another representation to make a plot render.
- Record template lineage, evidence lineage, representation, units, cohort
  roles, support thresholds, and exclusions in the notebook.

## Reader-facing form

- Follow compute, explain, display ordering.
- Put one full method explanation near the top. Put a short, local explanation
  immediately before every table or figure.
- State what one row or point means, the units, colors, support, and exclusions.
- Keep description separate from the final `Interpretation` section.
- Use human-readable cohort and study names; retain machine identifiers only as
  lineage fields or trailing table columns.

## Parameterized notebook families

When one analysis supports an explicit zero-to-N-dimensional bin definition:

- zero dimensions means the pooled population;
- one or more dimensions means one explicitly declared conjunction;
- never generate an implicit Cartesian product of bins;
- keep one notebook per selected bin so each report remains readable;
- when the family becomes large, use
  `centroid_displacement/bins/bins_0001/`, `bins_0002/`, and so on;
- place `bins.md` beside the numbered directories and record each bin's
  dimensions, values, continuous boundaries, missing-value policy, donor and
  cell support, representation, centroid definition, and evidence lineage.

## Anti-patterns

- Rebuilding a familiar notebook from memory without inspecting the template.
- Copying scientific calculations into a WET notebook.
- Updating only the WET copy when the improvement is reusable.
- Overwriting an informative existing view while adding a new view.
- Forcing a new scientific question into an incompatible template.
- Expanding cohorts, representations, or filters without an explicit selector.
- Calling pooled cell distances bin-specific because the donor-level evidence
  was stratified.

## Related guidance

Read `SKILL_NOTEBOOK_GUIDELINES.md` for notebook form and conversion. Read
`SKILL_ANTIFRAGILE_EVOLUTION.md` when a live failure should become a durable
architectural rule. Domain skills remain authoritative for the scientific
evidence contract.
