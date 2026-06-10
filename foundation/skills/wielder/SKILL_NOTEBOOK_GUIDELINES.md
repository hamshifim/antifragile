---
description: Interactive Exploration & Jupyter Notebook Standards
---
[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

 Jupyter Notebooks & Data Exploration

- **Explore Intent**: In `explore/`-style notebook spaces, notebooks primarily exist for curiosity, analysis, and QA. They are allowed to be WET and investigative; the goal is to make real artifacts and behaviors legible, not to force exploratory work into production-shaped abstractions.
- **Notebook Placement**: Exploration notebooks belong under the repository's `explore/` tree, not inside production app modules. Keep production app directories for reusable code, configs, tests, and docs.
- **Topical Organization Guideline**: Within `explore/`, prefer grouping by topic or investigation surface such as `model_binding/exploration/` or `msa/mmseqs/` rather than by production app module. Treat this as a lightweight guideline for readability, not a rule that should slow down or block exploration.
- **Naming**: Do not include `wet` or `notebook` in notebook filenames. Notebooks in `explore/` are already allowed to be WET and the `.ipynb` extension already says notebook.
- **Displaying DataFrames**: Always use a scrollable frame utility (e.g., `from wielder.visual.display import display_scrollable_dataframe`) instead of raw `.head()` or `.tail()`. This prevents IDE DOM thrashing.
- **DataFrame Nomenclature**: Name Spark DataFrames with an `_sdf` suffix and pandas DataFrames with an `_df` suffix. When previewing Spark results interactively, create the Spark DataFrame first, then materialize only the first configured `N` rows into pandas and display that bounded pandas DataFrame with the scrollable frame utility.
- **1 Display Per Cell**: A single code cell MUST NOT contain multiple visual output calls to avoid crashing the DOM.
- **Script-to-Notebook Duality**: Scripts and Notebooks MUST remain fluid. NEVER manually copy-paste cells. 
  - Python files MUST be strictly delineated by `# %%` block markers. 
  - Aggressively replace `# In[ ]:` cell artifacts with `# %%`.
  - Compile WET codebase translations via Wielder conversion utilities instead of arbitrarily editing internal JSON abstractions.
- **Centralized Notebook Configuration Block**: Exploration notebooks SHOULD expose their topographical modes and target selectors in one early configuration cell. Keep `ecosystem`, `stage_tier`, and adjacent mode toggles together so a reader can quickly retarget the notebook for data exploration without hunting through downstream cells.
- **Notebook User Selector Overrides**: When a companion script backs an interactive notebook, name explicit user-controlled target selectors with the `notebook_user_selected_*` prefix in the early configuration cell (for example `notebook_user_selected_input_index` or `notebook_user_selected_input_key`). These selectors MUST override configured legacy defaults or discovered convenience matches. Companion scripts may display configured values such as `source_filename`, but they MUST NOT silently replace a non-null notebook user selector with a config-derived choice downstream.
- **Anti-Pattern: Defensive Execution Skips**: Interactive notebook blocks MUST NOT rely on protective Python constructs (`if`, `try`, `assert`) to artificially bypass empty states (e.g., `if not df.empty:`). If target payloads are missing, the physical execution block MUST crash organically and distinctly dump a python `std-out` stacktrace. Defensive error-handling suppresses immediate visibility inside Jupyter shells.
- **Wielder Notebook Conversion Protocol**: When editing a Jupyter Notebook, you MUST NOT edit `.ipynb` JSON strings or rely on generic third-party plugins. Instead:
  1. Convert the active `.ipynb` into a flat `.py` script using: `python -m wielder.util.notebook_converter <notebook.ipynb>`.
  2. Implement architectural changes natively against the generated `.py` script.
  3. Execute testing directly against the python interpreter.
  4. Once stable, translate the Python definitions back into `.ipynb` cells using `python -m wielder.util.notebook_converter <script.py>`. This specialized parser ensures `# %%` execution blocks and `if __name__ == '__main__':` scaffolds are compiled gracefully natively inside Workspace without structural `.ipynb` indention shifting.

- **Notebook Import Hierarchy**: All Python imports MUST be strictly hoisted to the very top cell of the notebook (no inline/scattered imports). They must be categorized in the following exact descending order:
  1. Standard lib (`os`, `sys`, `json`, `datetime`)
  2. Common data/ML packages (`numpy`, `pandas`)
  3. Scientific packages (`MDAnalysis`, `py3Dmol`, `rdkit`)
  4. Other external dependencies
  5. `wielder` ecosystem
  6. `workspace` ecosystem
