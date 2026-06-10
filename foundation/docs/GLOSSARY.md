# Glossary

## Ecosystem
A distributed execution topology of cooperating apps, services, and surfaces. An ecosystem is broader than any single app and may be centered around a workflow.

An ecosystem is not a cloud account, a Kubernetes cluster, or a single script.
Those can be surfaces or resources inside the ecosystem.

## Workflow
A cohesive unit of functionality that may span multiple apps and services. A workflow can be ephemeral, batch-oriented, or long-running.

## App
A bounded executable or business capability. An app may participate in one or more workflows.

Apps consume provisioned infrastructure contracts. They should not create their
own durable buckets, topics, service accounts, schedules, or cloud projects.

## Service
A functional capability exposed for reuse by apps or workflows. A service is defined by what it does, not by its transport or surface, and may exist on multiple surfaces.

## Surface
A concrete runtime substrate such as local Python, Docker, Kubernetes, WSL, or AWS. A surface hosts app or service instances but is not itself the service.

## Transport
The communication mechanism used to access a service, such as SDK, gRPC, REST, or Kafka. Transport is incidental to service identity and may change without changing the service's function.

## Wieldable
A capability is wieldable when it can be operated through explicit, repeatable
interfaces such as Wielder entrypoints, CLIs, Terraform, HOCON config, or
documented scripts.

Wieldable does not mean over-abstracted. A thin script that resolves config and
calls a proven tool can be more wieldable than a large framework wrapper.

## Commit All Around
Operator shorthand for adding unstaged changes and committing across the
current Wielder super-repo/submodule workspace.

By itself, the phrase names a broad mechanical action: stage unstaged changes
where they live, commit inside owning submodules, then commit the super-repo
gitlink updates. Default commit modulators make that request smaller and safer:
task scope limits what may be staged, and provenance demands an auditable
agent-created commit record unless the operator explicitly says otherwise.

Under the default modulators, commit all around means:

- stage and commit intentional task changes inside each owning submodule first
- stage and commit the super-repo gitlink updates after the submodule commits exist
- leave unrelated dirty files and submodules uncommitted
- include commit provenance according to the git versioning doctrine
- report the resulting commit chain and intentional leftovers

## Commit Scope
The set of files, submodules, generated artifacts, and super-repo pointers that
belong to a commit request.

Commit scope is narrower than workspace dirtiness. It is determined by the
operator request, the current task, repository ownership boundaries, and the
pre-commit audit. If task and non-task changes are mixed in one file and cannot
be safely separated, the agent should stop and ask rather than silently commit
the whole file.

## Commit Modulator
A word or phrase that narrows or changes a commit request without changing the
underlying requested operation.

Default commit modulators apply even when the operator does not say them aloud:
scope of the task and commit provenance. Explicit modulators such as `no
provenance` may override only the specific behavior they name.

## Task Scope
The default commit modulator that restricts a broad commit request to changes
belonging to the current task/thread.

Task scope is inferred from the operator request, files intentionally edited for
that task, repository ownership boundaries, and the pre-commit audit. It is not
the same thing as all workspace dirtiness.

## In Scope
A commit-request modulator meaning "commit only the files, submodules, and
super-repo pointers belonging to the current task."

`In scope` is commonly paired with `commit all around` to emphasize that the
agent should complete the submodule-to-supermodule chain while excluding
unrelated dirty work.

## Entire Scope
A commit-request modulator meaning "treat the whole currently dirty workspace
as the intended commit scope."

`Entire scope` is broader than task scope, but it is still not permission to
commit blindly. The agent must audit the full dirty workspace, respect
submodule ownership boundaries, exclude secrets and accidental generated junk,
and report what is being swept into the commit chain. Provenance still applies
unless separately waived.

## Commit Provenance
The default commit modulator and agent-authored commit metadata that records who
or what created the commit, what audit was performed, which validation was run,
and what residual risk or runtime identity matters remain.

For agent-created commits, commit provenance is the default. It may appear in
the commit message body, a compact versioned provenance report, or both,
according to the git versioning doctrine.

## No Provenance
A commit-request modulator meaning "do not add the default agent provenance
body fields or provenance report for this commit request."

`No provenance` changes the commit message/reporting style only. It does not
remove the need for scoped staging, pre-commit audit, validation reporting, or
honest disclosure of unrelated dirty files left uncommitted.

## WArgus
WArgus is the Wielder security guardian abstraction for provider-backed secrets,
identity, groups, and permission surfaces. It should behave like Bucketeer for
security: a provider-neutral interface with provider implementations such as
`GCPArgus`, `GoogleWorkspaceArgus`, `AWSArgus`, and local/dev variants.

WArgus owns reusable secret value pumping, redacted planning/logging, and
provider dispatch. Project-specific names, groups, and Terraform modules remain
owned by the project/provisioning app.

## WJobBard
WJobBard is the Wielder abstraction for a triggered job: a schedulable or
event-triggered unit that runs a configured target and emits lifecycle or result
events.

WJobBard owns trigger, runtime identity, lifecycle, and provider dispatch
contracts. Payload tools such as WCloner own their own source/sink semantics.

## Security Hood
A security hood is the WArgus security posture selected by the `security`
topology dimension. The default hood is `org`, meaning the normal
organization-wide posture.

Non-default hoods such as `restricted` or `break_glass` should appear in
permission-bearing identity names when they change access.

## Stage Tier
The environment boundary for resources and execution, such as `dev`, `qa`, or
`prod`. Stage tier should drive physical isolation for mutable resources.

## Classification
Classification is the act of assigning a resource, data artifact, identity, or
event surface to its security and operational category before permissions are
designed.

Useful classification axes include data tier, provider boundary, stage tier,
actor type, mutability, and event surface. Classification should precede IAM;
unclear classification is a planning problem, not a reason for broad access.

## Compartmentalization
Compartmentalization is the isolation of classified resources and actors into
the smallest practical blast-radius boundary.

Common compartments include stage tier, CRO/source, raw versus interpreted
data, human versus daemon identity, writer versus reader access, source versus
destination mirror, and secret payload access versus non-secret config access.

## Organization Slug
An organization slug is the short human-readable organization identity used in
resource names when an agent, daemon, process, or trust subject operates across
or outside its enclosing organization or compartment.

For Workspace, the slug is `workspace`. Example:
`workspace-wclone-daemon-dev`.

## Project
A project is the provider or repository boundary that owns resources or source
code. In GCP, a project is a cloud resource container such as `workspace-dev`.
In the Workspace super-repo, a project can also mean a child repository such as
`domain-data` or `workflow-wielder`. Be explicit when ambiguity matters.

## Datalake
A physical and semantic storage system for durable data artifacts. A datalake
should describe what data is, not only which pipeline action produced it.

## Raw
Raw data is empirical input evidence as received or mirrored from a source,
before scientific interpretation or downstream harmonization. Raw ingestion may
standardize extraction and storage shape, but it should not decide assay meaning
or analysis conclusions.

## Harmonization
Harmonization is downstream standardization that maps extracted data into a
target schema or consumer contract. It is not raw mirroring.

## Mirror
A mirror is a provider-specific copy preserving the logical source identity and
object layout as much as possible. Mirrors prioritize fidelity and operator
traceability over interpretation.

## Bucket
A bucket is a provider storage root, such as S3, GCS, or a Google Drive shared
drive treated through Bucketeer. Bucket names are often operator-facing logical
identity and should remain consistent across providers when the project has
declared that contract.

## Key
A key is the provider-neutral object path below a bucket boundary. Use `key`
for object-store semantics instead of filesystem-only language like path when
the resource may live in S3, GCS, Drive, or another object-like store.

## Topic
A topic is a fan-out event contract. Topic names should express the stable
event surface, not the current implementation of subscribers.

## Provisioning
Provisioning creates durable infrastructure such as projects, buckets, topics,
service accounts, schedules, and permissions. Provisioning belongs to Wielder
ops/provisioning apps and Terraform-like surfaces, not to domain apps.

## Project Bootstrap
Project bootstrap is the rare, privileged provisioning step that creates or
discovers cloud projects and enables minimal bootstrap APIs.

## Project Assets
Project assets are durable resources inside an already-bootstrapped project,
such as buckets and topics. They can have separate thin entrypoints from project
bootstrap while staying under the same provisioning app and ecosystem.
