# The Data Lake Manifesto

## Purpose

A data lake preserves source data with minimal assumptions, then supports standardized and harmonized layers that serve downstream applications without forcing premature modeling decisions.

The lake is not a loose dumping ground. It is an append-only, provenance-rich scientific substrate where source material, transformations, and meaning are kept traceable.

## Core Tiers

### Raw

Raw data preserves the original source material.

- No mutation of the source payload.
- No overwriting of prior ingestions.
- No filtering away observations for convenience.
- Preserve source context, metadata, provenance, timestamps, relationships, and audit leftovers.

Raw ingestion may still organize information into reviewable tables such as protocol, experiment context, material inventory, empirical observations, and unclassified leftovers. That organization must preserve the original facts and keep source pointers.

### Standardized

Standardized data brings source material into consistent technical shape.

- Normalize formats, units, schemas, encodings, and data types.
- Keep transformations minimal, traceable, and preferably reversible.
- Preserve enough provenance to reconstruct the original source context.

Standardization answers: "Can systems read and compare this reliably?"

### Harmonized

Harmonized data aligns meaning across sources.

- Resolve naming differences, identifiers, categories, and semantic mappings.
- Map source-specific labels into shared project, assay, compound, target, organism, and ontology semantics.
- Keep pointer columns back to source, provenance sidecars, resolved configuration, and run identity.

Harmonization answers: "Do these records mean the same thing?"

## Warehouse Boundary

A data warehouse is built from selected lake data. It imposes schema, cleaning rules, and analytical models for efficient, repeatable querying.

The warehouse is not the system of record for source truth. It is a modeled product of the lake.

## Downstream Applications

Downstream applications are systems, reports, notebooks, models, automations, or user-facing tools that consume lake or warehouse data.

When downstream applications are backed by a data lake, they remain adaptable: data can be reshaped and remapped as scientific, operational, and modeling needs evolve.

## Architectural Principles

1. Preserve First
   Capture source material before imposing irreversible structure.

2. Append Only
   Corrections are new records, runs, or lineage links. Existing source payloads are not silently rewritten.

3. Provenance Is Data
   Configuration, code identity, source file, ingestion time, source timestamps, run identity, and transformation lineage are first-class scientific context.

4. Separate Technical Shape From Meaning
   Standardization makes data technically comparable. Harmonization makes it semantically comparable.

5. Delay Irreversible Decisions
   Early schema choices should not trap future analytics, machine learning, or scientific reinterpretation.

6. Access Through Contracts
   Storage paths, cloud object keys, and datalake addresses belong behind accessors and configured adapters, not scattered through business logic.

7. Keep Human Review Surfaces Honest
   Tables and notebooks should lead with scientifically meaningful columns and trail with provenance, hashes, paths, and bookkeeping unless the table exists specifically for forensics.

## Relationship To Modality Contracts

This manifesto defines the conceptual doctrine. Individual modalities may add physical workflow tiers such as `experiment`, `search`, `generation`, `ingestion`, and `harmonization`.

Those physical tiers are valid only when they preserve the manifesto:

- source truth remains traceable
- transformations remain explicit
- semantic alignment is not confused with raw preservation
- query-optimized layers retain deterministic pointers back to provenance

## Conceptual Relationship

A data lake preserves source data first, with minimal assumptions. A data warehouse refines selected data into structured, query-ready forms. Downstream applications consume either layer depending on whether they need source elasticity, semantic breadth, or modeled analytical speed.

This separation delays irreversible modeling decisions and lets scientific applications evolve without being constrained by early schema choices.
