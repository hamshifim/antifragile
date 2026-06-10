---
description: Table Schema Contracts, Column Explanations, and Human Preview Legends
---
[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Table Schema Guidelines

Reusable table schemas are human-facing contracts, not just Spark/Pandas typing hints.

## Schema Ownership

- Reusable schemas belong in canonical ecosystem concern files such as `schema.conf`, included by every app or ecosystem that serializes, deserializes, searches, or previews those tables.
- App-local schemas are acceptable only when the table is genuinely private to that app and not a reusable project asset.
- Keep table sink locations in a sibling `tables.conf` or equivalent concern file. Schema defines row meaning; sink config defines where rows live.

## Column Explanations

- Every new or substantively modified configured table must have a concise table `description`.
- Every new or substantively modified configured column must have a concise `description` that explains the field's operational meaning, not merely restates the type.
- Column descriptions should be short enough to read above a notebook table. Prefer one sentence fragment.
- If a column stores compact JSON, the description must say what family of nested facts lives there and why it was not promoted into flat columns.
- If a column is a key, say what it joins to or what scope makes it unique.
- If a column is a score, say the directionality or interpretation when possible.

## Human Preview Legends

- Notebook and report surfaces that display a configured table should print a readable legend from the schema before the dataframe.
- The legend should include table description, column name, type, nullability, and description.
- Legend generation should be reusable SDK code near the table IO helpers, not repeated notebook boilerplate.

## Column Order

- Put the most discriminating domain fields first.
- Put result/measurement fields before diagnostic and bookkeeping fields.
- Put source keys, hashes, code provenance, and timestamps near the end unless the table exists primarily for provenance inspection.
