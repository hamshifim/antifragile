---
description: Security, secrets, IAM/RBAC, runtime identity, and cross-cloud credential guidelines for Wielder-managed systems.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Security Guidelines

Use this skill when work touches secrets, credentials, IAM/RBAC, service
accounts, cloud policies, runtime daemon identities, encrypted configuration,
cross-cloud authentication, or permission-bearing infrastructure.

## Core Rule

Classification and compartmentalization reign supreme.

Every security decision starts by classifying the resource, data, identity, and
event surface, then placing it in the smallest compartment that can do the job.
Apps and daemons consume provisioned security resources; they do not casually
create their own identities, topics, buckets, secret containers, or broad
policies at runtime.

## Classification

Classification assigns the sensitivity and operational role of a thing before
permissions are designed.

Classify at least:

- data tier: raw, harmonized, interpreted, derived, audit, or secret
- provider boundary: local, AWS, GCP, Google Drive, Microsoft, or mixed
- stage tier: dev, qa, prod, or another explicit environment
- actor type: human operator, daemon, scheduler, notebook, downstream consumer
- mutability: append-only, mirrored, replaceable, destructive, or ephemeral
- event surface: source event, clone-completed event, deletion alert, or
  downstream analysis trigger

If classification is unclear, do not paper over it with broad IAM. Stop at a
plan boundary, document the uncertainty, and ask or inspect until the category
is explicit.

## Compartmentalization

Compartmentalization turns classification into isolation. A compartment is the
smallest practical blast-radius boundary around a classified resource or actor.

Use separate compartments for:

- stage tiers
- CRO/source systems
- raw evidence versus downstream interpretation
- human users versus daemon identities
- writers versus readers
- source mirrors versus destination mirrors
- secret payload access versus non-secret config access
- clone-completed events versus deletion-alert events

Prefer many narrow grants over one broad grant when the provider supports it.
Do not mix compartments merely because two resources currently share an
implementation. Today's convenience is tomorrow's confused trust boundary.

## Stage-Tier Naming

All durable security resources must carry `stage_tier` in the human-visible
resource name, even when the enclosing account/project is already stage-scoped.
Audit logs, IAM listings, external trusts, and copied examples routinely escape
their original project context.

Apply this to:

- service accounts and runtime identities
- IAM roles, policies, and bindings where the provider name is visible
- secret IDs and credential containers
- KMS keys and key rings
- scheduler/job identities and daemon identities
- provider trust relationships and federation subjects

Preferred shape:

```text
<capability>-<purpose>-<stage_tier>
```

If an agent, daemon, process, or federation subject operates across or outside
its enclosing organization/compartment, prefix the identity with the
organization slug:

```text
<org>-<capability>-<purpose>-<stage_tier>
```

Examples:

```text
workspace-wclone-daemon-dev
wclone-aws-source-access-key-id-dev
wclone-aws-source-secret-access-key-dev
workspace-provider-raw-clone-completed-dev
```

Respect provider limits. For GCP service accounts, keep the account id
lowercase, hyphenated, and within the provider length limit.

## Secret Handling

- Version non-secret configuration shape only.
- Terraform may create secret containers and IAM bindings.
- Real secret payload versions are operator/runtime state unless the repo has
  an explicit encrypted secret-state policy.
- Secret-version pushes should run through a dedicated WArgus/GCPArgus-style
  entrypoint, separate from Terraform. Payload source references may be
  configured, but payload values must stay out of config, Terraform state, and
  logs.
- Do not put OAuth tokens, refresh tokens, AWS keys, service account JSON, or
  one-off migration credentials in tracked HOCON, Terraform variables, Docker
  images, notebooks, or generated docs.
- Prefer short-lived credentials or provider-native federation over static
  cross-cloud keys.

## Runtime Identity

- Every hosted daemon or scheduled job should run as a dedicated service
  account/role for that job family and `stage_tier`.
- The default WArgus security hood is `org`, meaning the normal
  organization-wide security posture. Do not use `standard` as the default
  security identity term.
- Non-default hoods such as `restricted` or `break_glass` should appear in
  permission-bearing identity names when they change access.
- Human operator identities and daemon identities must be separate.
- The daemon should receive only the permissions needed for the configured
  sources, sinks, topics, and secrets.
- Avoid project/account-wide roles when resource-scoped IAM can express the
  contract.

## Group-Bound Human Secret Ownership

Human access to secrets should be assigned through Google Workspace groups, not
individual users.

RBAC groups should live in the resolved security configuration, typically under
`rbac_groups`, and cloud IAM should consume those same config keys. When a
Google Workspace group is required by Terraform IAM, a Workspace Argus preflight
should create or verify the group before Terraform applies the binding.
Provider APIs needed by that preflight should also be declared in config, for
example `google_workspace_argus.required_services`, and enabled by the
provisioning script before the preflight executes.

Keep the split explicit:

- daemon service account: can read only the exact secret payloads it needs
- operator group: can rotate or manage secret versions for its compartment
- break-glass group: can read payloads only if explicitly required

For GCP Secret Manager, prefer secret-level IAM bindings:

- runtime reader: `roles/secretmanager.secretAccessor`
- rotation-only group: `roles/secretmanager.secretVersionAdder` or
  `roles/secretmanager.secretVersionManager`
- full secret administration: `roles/secretmanager.admin`, only when the group
  truly owns the whole secret container

The group name should carry the organization and compartment when it is
permission-bearing, for example:

```text
workspace-wclone-secret-operators-dev@example.com
```

## GCP Pattern

For GCP-hosted WClone or ingestion daemons:

- Use Secret Manager for external provider credentials.
- Use a stage-tier service account such as:
  `workspace-wclone-daemon-dev@workspace-dev.iam.gserviceaccount.com`.
- Grant `roles/secretmanager.secretAccessor` on specific secrets, not the whole
  project.
- Bind human secret rotation/administration through a Google Workspace group,
  not individual users.
- Grant bucket IAM on exact source/destination buckets.
- Grant `roles/pubsub.publisher` on exact event topics.
- Use ADC/metadata credentials for GCP access with backend `env_auth = true`.
- Prefer Workload Identity Federation to AWS when practical; static AWS keys in
  Secret Manager are a transitional mechanism.

## Review Checklist

Before approving or implementing a security plan, check:

- Has each resource, event, and identity been classified before IAM is chosen?
- Is each classified boundary mapped to a clear compartment?
- Does every durable permission-bearing resource include `stage_tier`?
- Does every cross-compartment or externally operating daemon/process identity
  include the organization slug?
- Are secret payloads excluded from tracked config and Terraform variables?
- Is the runtime identity distinct from human/admin identities?
- Are human secret permissions bound to Google Workspace groups rather than
  individual users?
- Are IAM grants resource-scoped wherever the provider supports it?
- Is the fallback from federation to static credentials explicit and temporary?
- Can an operator verify identities, secret IAM, bucket IAM, and topic IAM with
  provider CLI commands?
