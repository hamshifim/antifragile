---
name: notebook-catalog-organization
description: Organize source-discovery notebooks into a stable overview, sparse cross-source inventory and source inspections, with usable WSL handoffs and verified navigation.
---

# Notebook Catalog Organization

Use for a notebook collection that explores known datasets across sources.
Follow [Notebook Guidelines](SKILL_NOTEBOOK_GUIDELINES.md) for generation and QA,
and [Harmonization Guidelines](../data_skills/SKILL_HARMONIZATION_GUIDELINES.md)
when mapping source records into common tables.

- Maintain one stable `overview.ipynb` entry point and a directory README.
- Distinguish overview (sources), harmonized inventory (comparable records),
  source inventory, dataset inspection and acquisition workflows.
- Keep dataset and donor tables separate and linked. Preserve identity scope,
  original annotations, missing values, count units, releases and evidence.
  Aggregator records and repeated dataset versions are not independent donors.
- Show coverage honestly: a known source may lack a structured inventory, and
  an inventory may cover a selected release rather than the whole provider.
- Do not move working notebooks or data merely to beautify a tree. Inventory
  callers first; update links and config atomically when moving a source family.
- Keep editable companions and output-free templates versioned. Put executed
  local previews under one documented ignored location, preserving filenames
  and working relative links. Experiment products still use configured buckets.
- Include back-navigation to the overview and cross-source inventory.
- In Windows/WSL handoffs, provide a clickable link **and a visible copyable WSL
  path**. Identify whether it opens a template or an executed result. Never make
  the operator discover a path by hovering or infer which copy is authoritative.
- Before handoff, execute changed notebooks against real evidence, inspect their
  rendered tables, check navigation targets, and report untested source notebooks.
- Source overviews should not trigger expensive searches or downloads. Expose
  refresh/acquisition as an explicit operation, separate from viewing a snapshot.
