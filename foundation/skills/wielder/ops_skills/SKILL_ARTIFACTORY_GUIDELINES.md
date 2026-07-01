---
description: Wielder artifactory doctrine for Python/Spark code bundles, runtime artifacts, configured py-file sources, artifact buckets, and artifact publication through PySparker/Artifactor.
---

# Artifactory Guidelines

Use this skill when adding, reviewing, or debugging Wielder artifact
publication, especially Python/Spark code bundles, PySparker artifact jobs,
runtime entrypoints, shared Spark runtime archives, or artifact bucket/key
contracts.

## Core Principle

Artifactory is a configured publication surface, not a local packaging shortcut.

Wielder code artifacts should be published by the reusable Artifactor/PySparker
path from resolved HOCON. Destination bucket, root key, version, entrypoint,
py-files, archives, and cleanup policy should come from config.

Validate runtime artifact config with Wielder-owned Pydantic contracts such as
`PythonRuntimeArtifactContract` and `PythonArtifactSourceContract` before
building an artifact bundle spec. Do not pass raw HOCON/`Any` through the
publication path once it crosses into Wielder.

## Source Archive Shape

Use existing Artifactor source kinds before inventing source packaging.

- Use `artifact_kind = "file"` for a single Python entrypoint or file.
- Use `artifact_kind = "zip"` for a package directory. Artifactor already zips
  the directory so its basename is the import root. For a `src/<package>`
  layout, set `source = "repo/src/<package>"`; the zip will expose
  `<package>/...`, which is what Spark imports need.
- Use multiple `py_file_sources` when a runtime needs several packages. Spark
  accepts multiple py-files, and Artifactor publishes them as one bundle with
  one manifest.
- For one shared Python runtime bundle spanning several packages, configure the
  existing zip source shape:

```hocon
python_runtime_artifact {
  name = "shared_python_runtime"
  source_root = ${super_project_root}
  entrypoint = "Wielder/wielder/spark/runtime_entrypoint.py"
  entrypoint_artifact_name = "spark_runtime_entrypoint.py"
  py_file_sources = [
    {
      name = "wielder"
      source = "Wielder/wielder"
      artifact_name = "wielder.zip"
      artifact_kind = "zip"
    },
    {
      name = "domain_pkg"
      source = "domain-repo/src/domain_pkg"
      artifact_name = "domain_pkg.zip"
      artifact_kind = "zip"
    }
  ]
}
```

Do not create a custom assembly format unless the existing `py_file_sources`,
`archive_sources`, and Spark `--py-files` contract genuinely cannot express the
runtime.

## Runtime Entrypoints

Prefer one shared runtime artifact with a generic runtime entrypoint when
several Spark jobs need the same code closure.

- The runtime entrypoint may receive `--module <python.module>` to select the
  actual job module.
- Individual app configs should declare their job semantics and choose the
  shared runtime artifact through HOCON.
- Workflow/app code should pass the resolved runtime artifact subtree into
  PySparker. Do not synthesize Python descriptors in the domain app.

## Publication Contract

- Publish artifacts through Wielder Artifactor/PySparker.
- Keep artifact bucket, root key, version, and cleanup policy in config.
- Keep bucket-relative layout stable across local and cloud surfaces, for
  example `spark/python/<job>/<version>/...`.
- Let the ecosystem choose the concrete artifactory bucket/provider.
- Use resolved config bootstraps for runtime config payloads; do not rely on
  local files being present beside the Spark driver.
- In DAG-shaped wielder step config, keep a class step such as
  `steps.<set>.artifacts` above per-artifact leaf entrypoints such as
  `<runtime>_artifacts`. Even one shared Python runtime artifact should use the
  class/leaf pattern so later artifacts can join without changing the wielder
  shape.
- A wielder may publish runtime artifacts before provisioning services or
  submitting jobs. The job/app submit path may still call the same artifact
  publication helper; Artifactor/PySparker reuse should make that call cheap
  when the bundle already exists.
- The wielder should call app-owned artifact publication entrypoints, not
  prepare Spark runtime artifacts by reaching into the child app's lower-level
  context. The artifact app owns config resolution, bootstrap publication, and
  versioned skip/reuse behavior.

## Anti-Patterns

- Recursive `rglob`, ad hoc `zipfile`, or `shutil.copytree` packaging of the
  live worktree when Artifactor's configured `zip` source kind already handles
  the package.
- `workspace_zip`-style custom source walkers with local ignore rules.
- Adding new WGit helpers or archive kinds before checking whether existing
  Artifactor `zip`, `file`, `archive_sources`, or base app patterns already
  solve the case.
- Reading a stale staging clone or preexisting stage directory as artifact
  truth.
- Extracting Python/Spark code bundles from a Docker image. Image builds and
  Spark artifact publication are separate artifact classes.
- Hard-coded artifact buckets, local paths, or environment variables in Spark
  job code.
- Rebuilding the same source closure separately for each app when a shared
  runtime artifact plus module selector is the intended shape.
- Folding artifact publication into a vague wielder "preflight" flag that
  cannot distinguish image builds, artifact publication, config staging, and
  fixture generation.

## Validation

Before claiming artifact work is ready:

1. Run a focused config-resolution test proving the app sees the intended
   runtime artifact subtree.
2. Run an Artifactor/PySparker unit test proving the published Spark command
   receives the expected entrypoint, py-files, and module args.
3. Inspect the produced zip or published manifest for any new source shape so
   package roots inside the zip match Python import roots.
4. Run `plan` for the wielded app and confirm it reports the artifact manifest
   and object keys before any expensive `apply`.
