---
name: information-presentation
description: Present scientific evidence clearly in notebooks and Pattern Walker titles, explanations, tables, legends and navigation. Use when readers need to understand a result without reconstructing the agent's context.
---

# Information Presentation

The reader is a capable collaborator moving at a higher level than the computation.
Make the evidence understandable without requiring them to inherit the agent's
working context. Concise means removing repetition, not omitting definitions.

## Reuse before redesign

Inspect existing views, evaluation notebooks, shared renderers and source artifacts
before creating another presentation. When the operator mentions an existing
notebook family, locate and read it. Reuse compatible components; explain any
scientific-contract mismatch. Do not replace a requested view with a nearby,
easier computation or silently narrow the population, dimensions or history.

## Explain from the question down

- State the question, what was measured, and how to read the view, in that order.
- Define a short term once, then use it consistently in titles, axes and prose.
  For example, define **Healthy Center** as the mean expression vector of the
  training healthy reference in the stated sex/cell-type group. Say whether cells
  or donors receive equal weight. Explain that distance to this center is a
  heuristic; it is not the only possible description of health.
- Always answer “distance from what?”, “fraction of whom?”, “in which space?”
  and “which groups were used to fit versus evaluate?” when those apply.
- Define split and fold locally: a split assigns donors to training/validation/
  evaluation; a fold repeats an explicitly described assignment. Folds are not
  cell types unless the method actually defines them that way.
- Explain acronyms on first use and give the practical meaning. Keep equations
  and implementation detail available below the essential explanation.
- A cumulative donor fraction counts donors at or below the horizontal value;
  it does not add distances. State this beside a cumulative plot.

## Overview, then detail

Show the whole available scope before a selected example or close-up: all epochs
before a late window, all relevant cohorts/folds before a representative donor.
If history is incomplete, show coverage and the missing interval prominently.
Never interpolate missing evidence or call a retained tail the complete run.

Prefer a readable plot or small human-labelled table before raw metric dumps.
Use meaningful rounding and units; put IDs, hashes, machine column names and
fine-grained diagnostics in secondary detail. Preserve access to that detail.
Choose side-by-side views when comparison is the reader's task. Do not imply
that an average or distance magnitude retains full-vector direction or shape.

## Describe separately from interpreting

Beside each view explain its unit (cell, donor, voxel), axes, reference, colors,
aggregation, and scope. Then give a direct evidence-backed interpretation in the
medium's interpretation section. Lead with what is observed, followed by the
specific limitation that affects that conclusion. Avoid repetitive apologetic
prefaces and lists of claims nobody made. A negative finding is still a result;
missing evidence is not a negative finding.

## Medium-specific use

**Notebooks:** follow the notebook skill's compute → explain → display structure.
Hand off executed outputs when feasible; say exactly what could not be executed.
Inspect the rendered figures and tables, not only successful cell execution.
Do not create companion scripts just to edit notebooks; reusable calculations
belong in the owning library and presentation can remain notebook-native.

**Pattern Walker:** titles identify the phenomenon; subtitles identify the
cohorts/studies and representation. Info entries explain the method and reference.
Keep density, cohort composition, brightness and opacity meanings distinct and
explain each active channel in its legend. A 3-PC projection is not full-space
occupancy: expose retained variance and voxel resolution where relevant. Make
collection hierarchy, current location and scene identity visible so readers
can find the view again. Labels come from domain metadata, not generic-client
hardcoding. Preserve navigation state while changing independent controls.

## Durable handoff

Store result-specific interpretation, artifact selectors and notebook lineage
beside the investigation. Keep reusable presentation principles here, linked
from notebook and Pattern Walker skills. Do not rely on conversation summaries
or copy transient results into this skill. Before handing off, ask: could a
reader returning after a month explain what one mark means and find its source?
