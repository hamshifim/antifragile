---
description: The Wieldering Way for epigenetic configuration contracts: callers provide versioned HOCON and libraries validate strict typed contracts without hand-built descriptors or defensive defaults. Use when Wielder functionality crosses app, library, DAG-shaped wielder, client-generation, reverse API, or UI-config boundaries.
---


# The Wieldering Way: Epigenetic Config Contracts

Use this skill when designing, implementing, or reviewing Wielder functionality where a reusable library, client generator, reverse API, DAG-shaped wielder helper, or UI bridge receives operational intent from a caller.
When that contract includes buckets, object keys, table keys, URIs, artifact roots, or storage accessors, also read [Strict FS Agnosticism](../data_skills/SKILL_STRICT_FS_AGNOSTICISM.md).

## Wieldering Way

The Wieldering Way is to Wielder what Pythonic is to Python: the idiomatic posture that makes the ecosystem coherent under pressure. It is also a deliberate nod to the Wierding Way from Dune: disciplined embodied practice, not merely a rule list.

In this context, Wieldering means functionality is expressed through versioned epigenetic HOCON. Code receives resolved config, validates the owned contract strictly, and acts. Configuration is the modulation layer; libraries are functional organs; generated artifacts are materialized expressions.

## Core Rule

The Wieldering Way is not for domain repos to hand-build Python descriptors for a library. The caller provides a versioned HOCON subtree. The library validates that subtree with a strict typed contract, usually Pydantic, and then performs its functionality.

If the contract breaks, it is on the caller/config boundary. The library must fail closed. Do not add defensive defaults, `.get` fallbacks, adapter callbacks, or descriptor synthesis to hide malformed config.

## Contract Shape

- Durable topology, endpoint lists, feature flags, materialization paths, client config, and behavior selection belong in HOCON.
- Storage contracts should name provider-neutral buckets, object keys, table/catalog ids, and opaque URIs. Do not make reusable libraries accept or derive local filesystem paths when the same contract may resolve to `s3://`, `gs://`, mounted volume, or another storage surface.
- Callers pass the resolved owned subtree across the library boundary.
- Libraries own strict models for the contract they consume.
- Models should forbid unexpected fields unless extension is explicitly part of the versioned contract.
- Missing required fields should raise during validation before side effects occur.
- Transient local artifacts, such as generated browser-readable config files, should materialize from the versioned HOCON contract and remain ignored when developer-local.
- App-to-app handoffs pass wrapper ecosystem names in explicit leaves such as `app_ecosystem_<app>`. Domain ecosystems own reusable functional contracts; surface ecosystems own physical runtime facts; aggregating wrapper ecosystems include the needed domain and surface ecosystems and are the normal app entrypoint ecosystems.
- Hybrid wrapper ecosystems express service placement per service. A service may resolve as local source, Kubernetes Deployment/StatefulSet/Job, Spark job, or provider-managed runtime while sibling services resolve differently under the same wrapper. The library or service entrypoint should consume the resolved placement contract rather than inventing a parallel launch/config channel.
- DAG-shaped wielder materialization controls should have class steps and leaf entrypoints. Use class leaves such as `steps.<set>.images`, `steps.<set>.artifacts`, and `steps.<set>.provision` for app-level DAG intent, plus specific typed entrypoints such as `<service>_image` or `<runtime>_artifacts` for each materializable surface. Wielder code acts as a switchboard: it calls app-owned leaf materializers with Wielder mode overrides, and those app leaves resolve their own config, reuse versioned artifacts/images, and may be called again by the owning service/job path.

## Ownership Boundary

- Caller/domain/app config owns the epigenetic intent.
- Wielder/config accessors own resolution and overlay order.
- The reusable library owns typed validation and generic functionality.
- The generated artifact is an expression of config, not the source of truth.

## Anti-Patterns

- Domain repos provide `ServerDescriptor`, `ClientDescriptor`, or similar ad hoc objects when HOCON can express the same contract.
- A library asks each domain repo for bespoke callbacks to reconstruct config.
- Python fills missing leaves with defaults after config resolution.
- Environment variables or generated YAML become a second operator control plane.
- A library silently ignores malformed or unexpected config.
- A factory, Spark helper, Bucketeer wrapper, or notebook companion converts an opaque object URI into a local `Path`, parent directory, preview server, or cleanup target without an explicitly local-only config contract.
- A service entrypoint adds a leaf-level CLI tunnel such as `--config_override key=value` for facts that should be resolved by ecosystem, context, developer, test, module, or normal Wielder mode overlays.

## Example Pattern

```python
from pydantic import BaseModel, ConfigDict

class PatternWalkerServer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    host: str
    port: int

class PatternWalkerClientConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    servers: list[PatternWalkerServer]
    client: PatternWalkerClient

config = PatternWalkerClientConfig.model_validate(resolved_pattern_walker_subtree)
```

The domain does not build descriptors. It owns HOCON. The library validates and executes.

## Review Heuristic

When a Wielder feature crosses from app/domain code into a reusable library, ask: what is the Wieldering Way here? Could this object, callback, flag, path, or default be a versioned HOCON leaf consumed through a strict model? If yes, express it in config and validate it at the library boundary.
