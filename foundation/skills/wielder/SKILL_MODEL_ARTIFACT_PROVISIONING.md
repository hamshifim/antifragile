---
description: Provision reusable model artifact tooling and app-owned model assets through Wielder config, WClone/rclone, Hugging Face, Ollama, and idempotent local caches.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Model Artifact Provisioning

Use this skill when adding, reviewing, or handing off Wielder support for large
model artifacts, model cache directories, Hugging Face downloads, Ollama model
pulls, or rclone/WClone mirrors for model storage.

## Core Principle

Separate tool provisioning from artifact provisioning.

Workstation init owns generic tooling. App provision owns the concrete model.
Repeated app provision must be conditional on existing local artifacts: if the
configured destination already exists and contains payload files, report it as
present and do not fetch again.

## Layer Split

1. Workstation tooling
   - Ubuntu and remote workstation init should ensure reusable CLIs and extractors such as
     `rclone`, `zstd`, the Hugging Face `hf` CLI, and Ollama.
   - This belongs in the generic Ubuntu bootstrap phase, not in a scientific
     app runtime and not in a one-off operator ritual.
   - Remote workstation init may call the same Ubuntu bootstrapper used by local WSL.
     The bootstrapper may safely be rerun because these tools are idempotent or
     version-checked.

2. Account and storage configuration
   - Provider accounts, rclone remotes, buckets, cache roots, and selected
     clone jobs belong in resolved HOCON.
   - `context_conf/<name>/developer.conf` may override account leaves and
     selected jobs for a local developer.
   - Do not version OAuth tokens, Hugging Face tokens, Google credentials, or
     static cloud keys. Let provider CLIs or secret managers own secret payloads.

3. App model provisioning
   - A model-using app should expose a provision step that resolves a typed
     artifact contract from config.
   - The provision step should support `plan` and `apply`.
   - `plan` should show the provider, destination, and command that would run,
     unless the local destination already has payload files.
   - `apply` should fetch only when the destination is missing or empty.
   - `skip_if_destination_exists = true` should be the normal default for
     large immutable model artifacts.

4. Shared cache promotion
   - Uploading a local model cache to a shared bucket is a separate explicit
     WClone job such as `local_to_gcs`.
   - Pulling from a shared bucket into local cache is another explicit job such
     as `gcs_to_local`.
   - Do not make a Hugging Face fetch implicitly upload to shared storage.

## ExampleModelV2 Pattern

The first ExampleModelV2 provisioning phase should fetch from Hugging Face into the
configured local model cache:

```hocon
model_artifacts.fetch.selected_artifacts = ["example_model_v2_huggingface"]
model_artifacts.fetch.artifacts.example_model_v2_huggingface.enabled = true
```

The current model destination is:

```text
~/.cache/workspace/model_artifacts/example_model_v2
```

If that directory already contains files, the provision step should return
`status = "exists"` and skip the download command. If the directory exists but
is empty, the provision step should still fetch.

## Operator Commands

For generic Ubuntu or remote workstation tooling:

```bash
<workspace>/Wielder/wielder/scripts/install_ubuntu.sh --only model-artifact-tools
```

For app-owned model artifact provisioning:

```bash
<workspace>/workflow-wielder/src/workspace_wielder/deploy/apps/model_artifacts/wield/model_artifacts_fetch.py -es eco -st dev -se org -dl standard -cn standard -cc default_conf -w plan
```

```bash
<workspace>/workflow-wielder/src/workspace_wielder/deploy/apps/model_artifacts/wield/model_artifacts_fetch.py -es eco -st dev -se org -dl standard -cn standard -cc default_conf -w apply
```

For explicit cache mirroring through WClone:

```bash
<workspace>/workflow-wielder/src/workspace_wielder/deploy/apps/model_artifacts/wield/model_artifacts_wclone.py -es eco -st dev -se org -dl standard -cn standard -cc default_conf -w plan
```

## Anti-Patterns

- Downloading a model from inside an app request handler or notebook cell when
  a Wielder provision step exists.
- Encoding Hugging Face repo IDs, bucket names, cache paths, or rclone remotes
  as ad hoc environment variables or CLI flags.
- Re-downloading a large model on every `apply` when a nonempty configured
  destination already exists.
- Treating a local cache pull and a shared bucket upload as the same operation.
- Storing provider tokens or OAuth secrets in HOCON or generated rclone config.
