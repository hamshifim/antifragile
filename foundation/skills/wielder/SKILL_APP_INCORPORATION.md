---
name: App Incorporation
description: Wielder doctrine for incorporating, copying, reviving, or adapting an app/tool/model service from another repo or legacy codebase into a project while preserving config ownership, ecosystem boundaries, fixtures, notebooks, and source provenance.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.
[Read configuration guidelines](SKILL_CONFIGURATION_GUIDELINES.md), [test guidelines](SKILL_TEST_GUIDELINES.md), and [scripting guidelines](SKILL_WIELDER_SCRIPTS.md) before changing config, entrypoints, or fixtures.
Use [Functional Maximization](SKILL_FUNCTIONAL_MAXIMIZATION.md) when the incorporated app wraps a third-party model, scientific tool, or provider API whose full native capability surface must be preserved.

# App Incorporation

Use this skill when moving an app from a legacy repo, resurrected deployment, upstream tool, notebook, or adjacent project into a Wielder-managed project.

The goal is not to jump straight to the clean final form. The safer process is:

1. copy verbosely enough that functionality is unlikely to be lost;
2. make the copied app run with the smallest possible compatibility fixes;
3. inventory and prove what came across;
4. only then migrate the working copy into project-native Wielder form.

This preserves functionality before architecture pressure starts deleting it.

## Incorporation Loop

1. Inventory before copying.
   Find code, configs, notebooks, fixtures, fetchers, storage keys, runtime scripts, deploy shape, tests, docs, examples, and operator commands. Create a functionality ledger with one row per discovered capability: purpose, source file/config, input data, output artifacts, operator command, current status, and destination owner.

2. Copy verbosely into a quarantine shape.
   Prefer an intentionally WET copy under the destination project over an early abstraction. Keep source-adjacent filenames and comments long enough to compare against the original. Preserve fetchers, scripts, notebooks, fixtures, and tests even if they look redundant. Do not scrub aggressively during this phase; mark suspicious names in the ledger.

3. Make the copied app run with minimal fixes.
   Fix imports, package paths, obvious config loading, and missing dependencies only enough to execute the original happy path or closest available smoke path. Avoid moving config ownership, renaming buckets, changing fixture scale, or redesigning entrypoints before the copy has demonstrated life.

4. Prove copied functionality against the ledger.
   For every ledger row, mark one of:
   - imported and passing;
   - imported but failing with evidence;
   - intentionally deferred with reason;
   - intentionally dropped with operator-approved reason;
   - not found in source after search.

   Do not let "clean architecture" hide missing fetchers, delete paths, notebooks, source/sink operations, or advanced native options. If a capability is absent, say so explicitly before refactoring.

5. Decide ownership before refactoring.
   Assign each concern to the narrowest canonical owner:
   - project root: project identity, project-owned buckets, shared providers, durable cross-app data contracts;
   - functional ecosystem: reusable app-family contracts, native tool parameters, shared workflow intent;
   - concrete ecosystem: physical/runtime facts such as local roots, kube context, host ports, credentials surface, and service endpoints;
   - app baseline: fail-closed executable contract and typed schema limits;
   - test overlay: reduced scale, mock or miniature data, cleanup toggles, fixture identities, and apply/delete controls.

6. Move reusable project resources through project config, not side channels.
   Buckets are the canonical example: a project-owned reusable resource/data
   contract included by `project.conf` and consumed after evaluation. Ecosystems
   and apps may reference evaluated `buckets.*` or accessors, but must not
   include bucket files merely to make one app resolve. Apply the same rule to
   other project-owned reusable resources such as shared providers, durable
   schema registries, table catalogs, static artifact roots, and source datasets.

7. Port typed contracts.
   Recreate request/config/result models before runner logic. Pydantic contracts should expose native provider/tool options broadly, with production-grade defaults in ecosystem config and cheap fixtures only in test mode.

8. Keep storage behind accessors.
   Use Bucketeer or a project accessor for materialization, sync, discovery, and deletion. Do not reconstruct local bucket paths or object keys in app logic, tests, or notebooks except through resolved config/accessor output.

9. Preserve native output honestly.
   Keep raw/native artifacts, command JSON, previews, status reports, and failure reasons. Do not rename native metrics into stronger scientific or product claims.

10. Make notebooks executable projections.
   Notebook `.py` sources should use the same canonical accessor and endpoint functions as tests. Regenerate `.ipynb` from source, and make the notebook self-seeding when its purpose is functional exploration.

11. Validate the Wielder surface.
   Exercise plan/apply/delete where relevant, `-t` overlays for minimal fixtures, typed config resolution, notebooks, and focused unit tests. Report which native capabilities are real, skipped, or reserved.

## Functionality Ledger

Maintain a small ledger during incorporation. It can live in the task plan, an
uncommitted `_stam.md`, or a temporary checklist, but it must be updated before
deleting or refactoring copied code.

Suggested columns:

- capability;
- source files/config/notebook;
- source command or usage;
- required data/bucket/key;
- expected outputs;
- copied location;
- status;
- validation evidence;
- disposition.

Use the ledger to drive operator review. The operator should be able to see what
did not get imported without reading the whole diff.

## Legacy Scrubbing

During incorporation, remove or replace:

- old project/repo names from user-facing identifiers, bucket names, fixtures, notebooks, and tests;
- molecule, target, customer, or private fixture names that do not belong in the destination project;
- repo-specific filesystem paths such as `/home/<user>` unless they flow from resolved config;
- legacy CLIs or env vars that duplicate Wielder modes or HOCON;
- copied config leaves whose true owner is project, ecosystem, provider, or test mode.

Keep references to upstream third-party tools, libraries, and public datasets when they are factual and useful. Do not scrub real upstream provenance.

## Acceptance Checklist

An incorporation is ready to commit when:

- the functionality ledger has no silent unknowns;
- every discovered capability is imported, deferred, dropped with reason, or
  proven absent from the source;
- the copied app ran at least once before the architectural refactor, unless the
  source itself cannot run and that failure is documented;
- app baseline is minimal and fail-closed;
- project-owned reusable resources, such as buckets/providers/catalogs, are
  project-included, not ecosystem-included;
- functional configuration lives in a functional ecosystem, not a local/workstation wrapper;
- concrete local/workstation ecosystem contains only physical facts;
- `-t` owns miniature fixtures and pressure reductions;
- tests prove both production/default shape and test overlay shape;
- notebooks run against the canonical accessor path;
- delete behavior is explicit and scoped;
- native tool absence produces a classified skip/failure, not a crash;
- commit provenance lists source context, validation commands, and remaining native/runtime risk.
