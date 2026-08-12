---
name: Strict FS Agnosticism
description: Wielder doctrine for keeping storage contracts portable across local filesystems, mounted buckets, S3, GCS, Spark catalogs, notebooks, tests, scripts, and materializations. Use when code, config, tests, notebooks, or scripts name buckets, object keys, paths, URIs, table sinks, artifact roots, or storage accessors.
---

# Strict FS Agnosticism

Use this skill whenever a change touches storage identity, storage discovery,
artifact materialization, notebook/test output, Spark table IO, Bucketeer usage,
or logs that tell an operator where data lives.

## Core Contract

Storage identity is semantic first and physical second.

- `bucket` names the object-storage container or configured bucket abstraction.
- `object_key`, `base_key`, `artifact_subkey`, `table_key`, and `output_key`
  name provider-neutral keys relative to the bucket or catalog boundary.
- `uri` is an opaque provider handle returned by an accessor, table engine, or
  provider. It may be local, mounted, `s3://`, `gs://`, catalog-backed, signed,
  or remote.
- `Path` means a real local filesystem contract. Use it only when the config,
  function name, logs, and caller contract are explicitly local-only.

## Versioned Storage-Role Ontology

`storage_role` is the semantic responsibility of an artifact or key prefix. It
is not an IAM/RBAC role, provider, location, storage class, availability level,
or replication policy. Treat this list as the canonical version 1 controlled
vocabulary; unknown values must fail strict config validation.

- `control_backend`: Small operational state needed to control or reproduce a
  system, such as Terraform state, manifests, configuration provenance, and
  coordination metadata. It is normally critical, durable, and versioned.
- `dataset_authority`: The authoritative, irreplaceable copy of canonical raw
  or harmonized data. It owns write authority and the strongest preservation
  policy; other copies are replicas.
- `distribution_source`: A packaged, reproducible artifact intended to be
  fetched or hydrated into runtime storage, such as an MSA database copied from
  an object bucket onto a production volume. The package is durable, while
  hydrated runtime copies may be ephemeral.
- `working`: Disposable intermediate storage such as Spark staging, temporary
  indexes, caches, shuffle material, and recomputable outputs. It must not be
  mistaken for an authoritative dataset.

Assign `storage_role` at the artifact, dataset, or key-prefix boundary rather
than to an entire bucket when the bucket contains mixed responsibilities.
Extend this vocabulary only through a versioned doctrine and typed-contract
change.

Keep these independent storage dimensions beside `storage_role`:

- `location`: The physical locality, including conceptual `local` for
  workstation-local storage and provider regions such as `us-central1`.
- `storage_tier`: The provider-neutral or provider-mapped cost/performance tier.
- `availability`: `local`, `regional`, or `global`. `global` means discoverable
  and transferable through Nabu from configured locations; it does not mean a
  copy exists in every region.
- `replication`: The explicit authority and replica policy. Prefer one
  authoritative location and read-only replicas; do not infer replication from
  availability.

## Required Practice

- Keep durable config leaves and test fixtures in key vocabulary: `bucket`,
  `object_key`, `base_key`, `artifact_subkey`, `table_key`, `output_key`.
- Validate versioned storage contracts strictly before side effects. Unknown
  `storage_role` leaves, unexpected fields, and contradictory authority or
  replication declarations must fail closed.
- Report bucket, key, table/catalog id, and URI separately in plan/apply/test
  logs. Do not concatenate bucket and key into a pseudo-path for generic
  surfaces.
- Persist committed source provenance with every durable data output and its
  manifest. Project the super-repository SHA and every owning submodule SHA
  from the canonical resolved `conf.git` tree; do not inspect the live worktree
  or invent a parallel version token. An output generated from dirty code must
  not claim the preceding committed SHA, so commit the owning source and parent
  gitlink before materializing reproducible data.
- Route object discovery, existence checks, reads, writes, and cleanup through
  Bucketeer or a domain accessor layered on Bucketeer.
- Make storage accessors fail honestly. A missing object, failed download, or
  incomplete materialization should raise or return a typed failed state that
  names the bucket and key; it should not print a filename, return a vague
  boolean, or let downstream code discover the absence later.
- Route table-scale reads, writes, joins, filters, and lookups through the
  configured table engine such as Spark. Do not force table IO through
  object-file helpers.
- Let ecosystems choose physical roots, mounts, providers, catalogs,
  credential modes, and local/cloud expression. App and test code consume the
  resolved contract.
- Treat POSIX ownership as a physical-storage concern. If a Kube workload writes
  to local `hostPath`, local PV, mounted bucket, or NFS-like storage, the
  surface or wrapper ecosystem should provide the workload security context
  needed for future writes. Object stores such as S3 and GCS should stay in
  credential/IAM vocabulary, not Unix uid/gid vocabulary.
- Let local preview behavior live only in clearly local-only notebook cells,
  local developer docs, or local-only helper names. Generic surfaces should
  expose the opaque URI or provider view URL instead.

## Anti-Patterns

- Calling `Path(uri)`, taking `parent`, checking `://`, or deriving a local
  serve directory from an accessor-returned URI in generic code.
- Printing `serve_command`, `serve_directory`, or local HTTP preview hints from
  a generic Wielder script, test, or notebook companion.
- Hiding local bucket roots, mounted-root assumptions, or POSIX path behavior
  behind a factory, Spark helper, Bucketeer wrapper, or "portable" accessor.
- Treating a local `runAsUser`, `runAsGroup`, or `fsGroup` value as a domain
  storage fact rather than as a local POSIX surface/wrapper phenotype.
- Letting a local Bucketeer/accessor silently succeed on a missing source
  object, emit stray print output, or behave differently from the remote
  provider contract it represents.
- Using `*_path` names for object-store keys or durable table destinations.
  Use `*_key` or `*_uri` according to the contract.
- Storing `/tmp`, `/home/<user>`, Windows paths, or workstation-only roots in
  test fixtures, durable config, table rows, ledgers, or materialization plans.
- Using `os.path.join` for object keys. Build object keys with accessor helpers
  or POSIX-style key joining.
- Reading an entire table into pandas or driver memory to answer a lookup that
  belongs in Spark or the configured table engine.

## Review Checklist

Ask these questions before accepting storage-touching work:

1. Would this still work and read honestly if the active ecosystem used S3,
   GCS, a mounted remote bucket, or a remote desktop session?
2. Are semantic keys and opaque URIs kept distinct in config, rows, and logs?
3. Does the code use Bucketeer/domain accessors for object operations and Spark
   or the configured engine for table operations?
4. Does a missing object fail at the accessor boundary with bucket/key evidence?
5. Is any local-only behavior named and configured as local-only?
6. Can cleanup find watermarked outputs through the same accessor/table
   contract that created them?
