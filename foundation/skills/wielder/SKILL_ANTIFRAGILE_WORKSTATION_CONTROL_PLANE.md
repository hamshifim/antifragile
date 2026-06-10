---
description: Antifragile workstation and control-plane doctrine for designing, recovering, and operating a human desktop that also serves as an infrastructure cockpit without becoming an irreplaceable pet machine.
---

[Read the package guidelines](SKILL_PACKAGE_GUIDELINES.md) if you haven't recently.

# Antifragile Workstation Control Plane

Use this skill when planning, reviewing, rebuilding, or recovering a developer
workstation that also operates infrastructure: Terraform, Kubernetes, Docker,
cloud CLIs, browsers, IDEs, notebooks, Wielder entrypoints, agent sessions, and
demo-critical local state.

## Core Principle

An antifragile workstation is not a heroic machine. It is a convenient operator
surface whose important state can survive crashes, migration, local deletion,
and human forgetfulness.

Treat the machine as a replaceable control-plane shell with explicitly managed
state. A local desktop, WSL distribution, browser profile, shell file,
kubeconfig, or untracked config must not become the only copy of operational
truth.

## Terms

Use coined terms as intuition pumps, not private passwords. Define the boring
engineering contract beside the term.

- **Antifragile workstation:** a recoverable operator machine whose setup,
  secrets, caches, and operational memory are classified and restorable.
- **Control plane:** the human-facing cockpit for planning, applying,
  observing, and deleting infrastructure, images, artifacts, and workloads.
- **Wielding:** executing a configured lifecycle action such as `plan`,
  `apply`, `run`, `monitor`, or `delete` against a concrete surface.
- **Ecosystem:** the named Wielder configuration phenotype that selects how a
  coherent workload or control-plane intent runs across distributed surfaces:
  vendor clouds, workstation/local machines, on-prem infrastructure, or hybrids
  of those. It is the mix-and-match boundary for surfaces and services, carrying
  the resource ownership model, defaults, and runtime behavior.
- **Surface:** the target substrate or provider boundary, such as AWS,
  Kubernetes, Docker, Terraform, local files, or a job runner.
- **Substrate:** durable shared infrastructure such as DNS, clusters,
  registries, IAM, front doors, and storage foundations.
- **Workload:** app-owned runtime resources that should usually be ephemeral
  and deleteable without destroying the substrate.
- **`unique_name`:** the committed-state runtime identity used to isolate
  staged clones, backend state, artifacts, image tags, and workload resources.
- **`*_stam.md`:** an ignored local thinking/handoff note. Promote durable
  conclusions into versioned docs, skills, config, or code.

## Workstation Classes

Classify the machine before prescribing fixes:

- **Disposable developer shell:** source checkout plus package caches.
- **Operator workstation:** source checkout plus cloud auth, kubeconfig,
  Terraform, Docker, browser, IDE, and Wielder controls.
- **Durable control plane:** operator workstation plus persistent service,
  scheduled jobs, local mirrors, image cache, and recovery runbooks.

The higher the class, the more aggressively setup, secrets, snapshots, and
recovery validation must be scripted.

## State Taxonomy

Before recovery or migration, classify local state:

- **Reproducible:** install scripts, package manifests, dotfile examples,
  Wielder config, generated settings.
- **Secret:** cloud credentials, MFA profiles, SSH keys, tokens, kubeconfigs,
  `.env` files, ignored developer context.
- **Durable local cache:** Docker image layers, local S3/GCS mirrors, large
  model weights, downloaded datasets, staged Terraform clones.
- **Disposable cache:** package manager cache, build artifacts, temporary
  notebook outputs, stale logs.
- **Operator memory:** `*_stam.md`, handoff notes, command transcripts,
  architecture decisions, crash notes.

Only disposable cache may be casually removed. Secret and operator-memory state
must have a deliberate backup or regeneration path.

## Design Rules

- Use coined vocabulary only when it improves reasoning. Pair it with plain
  engineering definitions in durable docs.
- Prefer a real Linux control surface for Linux-native infra tools. Avoid
  relying on fragile host bridges for demo-critical Kubernetes, Docker, GPU,
  filesystem, or auth flows.
- Keep shell files idempotent. Install scripts may append guarded blocks, but
  must not depend on hidden manual edits.
- Keep cloud auth discoverable by standard SDKs and CLIs. Avoid per-command
  environment prefixes when a profile, config file, or project-level ignored
  secret can express the contract.
- Keep infrastructure execution through Wielder entrypoints or provider CLIs
  with visible commands, resolved config, and explicit delete semantics.
- Separate durable substrate ownership from ephemeral workload ownership.
  Persistent DNS, domains, front doors, clusters, registries, and auth surfaces
  need explicit deletion guards.
- Prefer snapshots for large durable local state, but also keep a scriptable
  rebuild path. Snapshots are fast recovery, not documentation.
- Treat browser and IDE affordances as operator UI, not source of truth.

## Remote Desktop Auth Boundaries

Do not collapse cloud control-plane auth into desktop session auth unless the
remote desktop product explicitly supports that identity path.

- Cloud role assumption controls who may create, inspect, tunnel to, or stop the
  workstation infrastructure.
- Remote desktop login controls who may unlock the graphical OS session.
- Port forwarding through a cloud management plane is network access, not
  desktop login.
- If the desktop server supports external/OIDC/SAML auth, treat that as a
  separate front-door integration with its own threat model. Do not assume it is
  free just because cloud console role switching works.
- For a first durable operator workstation, prefer a narrow and auditable path:
  cloud role -> management-plane tunnel -> OS/desktop authentication.
  Promote SSO/external auth later only if repeated use justifies the added
  surface.

## Recovery Checklist

Use this sequence after a crash, workstation migration, or suspicious local
state loss:

1. Freeze destructive work. Do not rerun deletes, prunes, or Terraform until
   current cloud state and local state are inspected.
2. Capture current evidence: hostname, OS, disk mounts, shell, Git status,
   cloud caller identity, kube contexts, Docker health, Terraform version, and
   Wielder install status.
3. Classify missing state using the taxonomy above.
4. Restore secrets through approved secret stores, ignored project secrets, or
   documented auth flows. Do not paste secrets into tracked files.
5. Rehydrate tooling with idempotent scripts.
6. Reconnect cloud and Kubernetes contexts through standard CLIs/SDKs.
7. Validate with read-only commands before apply/delete commands.
8. Record the recovery delta in an ignored `*_stam.md` or promote it into a
   reusable skill/script when it will recur.

## Control-Plane Validation

A workstation/control-plane rebuild is not complete until these checks pass:

- Git super-repo/submodules visible and no unknown destructive diff.
- Shell starts without errors and exposes required tool paths.
- Cloud CLIs can report caller identity without unexpected MFA loops.
- `kubectl` can list intended contexts or can safely rediscover them.
- Terraform version matches module constraints.
- Docker can run a small container; GPU stacks can run a minimal GPU probe when
  GPU support is in scope.
- IDE and browser can reach the local or hosted control surface.
- Wielder `show` or equivalent dry-run reveals the resolved config and command.

## Anti-Patterns

- Treating a WSL distro, browser profile, or laptop disk as the only control
  plane for expensive cloud resources.
- Debugging a broken workstation by repeatedly applying or deleting cloud
  infrastructure.
- Encoding auth and install state only in a human's shell history.
- Letting GUI convenience decide infrastructure ownership boundaries.
- Mixing persistent control-plane services into ephemeral workload configs
  without explicit substrate-owner guardrails.
- Moving to a more expensive workstation before making the environment
  scriptable and restorable.
