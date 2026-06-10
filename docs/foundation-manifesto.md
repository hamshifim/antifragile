# Wielder Antifragile Foundation

## Purpose
This document defines the doctrinal foundation for `wielder-antifragile`.

It is intentionally not an implementation spec. Its role is to state the architectural philosophy that should govern:

- personas
- skills
- workflows
- contracts
- provenance requirements
- the relationship between capability doctrine and runtime implementations (including `Wielder`)

## Executive Thesis
Runtime toolboxes for orchestration are already viable. `Wielder` is one concrete implementation: it resolves layered configuration, materializes runtime context, provisions infrastructure through ordered modules, deploys distributed resources, and observes live state transitions.

That is the baseline, not the destination.

The antifragile direction is to preserve Wielder's loose toolbox character while strengthening the contracts around it. The goal is not to force every client into one rigid platform. The goal is to make composition safer, more auditable, more adaptive, and more reproducible.

## Baseline Observations

### Reactive Strengths Already Present

- layered configuration
- topology abstraction
- downstream config materialization
- plan and apply observability
- runtime-specific delegation
- wrappers around Terraform, Kubernetes, Helm, storage, and notebook-adjacent workflows

### Antifragile Gaps

- missing first-class ecosystem manifests
- weak epoch and lineage formalization
- insufficiently explicit provenance
- too much CLI-centered activation logic
- broad orchestration scripts instead of tighter unary leaf nodes
- agentic development rules not yet housed in a durable canonical repo

## Core Principles

### 1. Wielder Capability Remains a Loose Toolbox
The capability to wield distributed systems should remain composable and mix-and-match. Users should be able to adopt only the parts they need.

Antifragility here comes from substitution, local adaptation, and low coupling, not from forcing all users through one monolithic orchestrator.

### 2. Contracts Become Strict Even If Usage Stays Flexible
The toolbox can remain loose while the contracts become explicit:

- ecosystem identity
- epoch identity
- evidence
- provenance
- inheritance
- handoff schemas

Loose usage with weak contracts creates drift. Loose usage with strong contracts creates adaptive stability.

### 3. Ecosystem Is the Top-Level Semantic Unit
Execution should be anchored to an explicit ecosystem definition rather than scattered implicit topology assumptions.

An ecosystem should declare:

- topology
- routing domains
- hardware and network structure
- storage and endpoint coordinates
- orchestration boundaries

### 4. Epoch Is the Unit of Forensic Accountability
Every execution should be tied to an explicit epoch:

- resolved configuration
- relevant code identities
- telemetry
- environment context
- evidence outputs

If configuration or code changes materially, the epoch changes.

### 5. Agentic Development Must Be Adversarial, Not Merely Productive
The wetlab direction is correct: builder momentum alone is not enough.

Complex work should proceed through:

- stepping stones
- builder proof
- Red Team critique
- explicit handoffs
- live verification

The purpose is to prevent silent architectural drift and builder's bias.

### 6. Personas and Skills Must Be Canonical but Project-Adaptable
Projects should inherit a shared baseline doctrine rather than copying markdown ad hoc.

That means:

- canonical base personas
- canonical base skills
- explicit project-specific overrides
- structural inheritance with validation

### 7. Markdown Is for Auditing, Not for Being the Source of Truth
Markdown should remain a rendered artifact for human inspection.

The source of truth should be structured semantic objects that can:

- resolve inheritance
- validate constraints
- serialize deterministically
- render to markdown for review

## Relationship to Runtime Implementations

### What Belongs in Runtime Implementations (e.g., Wielder)

- runtime adapters
- config resolution and materialization
- orchestration primitives
- provenance primitives
- VCS primitives
- notebook and DAG tooling

### What Belongs in `wielder-antifragile`

- personas
- skills
- workflows
- contracts
- playbooks
- inheritance rules
- adversarial development doctrine

## Phase 0 Doctrine
The first move is not a grand refactor. The first move is to give the doctrine a stable home.

`wielder-antifragile` should become that home, then be consumed by projects so the doctrine can evolve independently of any specific runtime implementation.

## Final Position
The right future is not “bind antifragile doctrine to one runtime framework.”

The right future is:

- runtime implementations (including Wielder) as execution toolboxes
- `wielder-antifragile` as the doctrinal, agentic, and contractual layer above them
- explicit ecosystems
- explicit epochs
- explicit provenance
- explicit inheritance
- human-auditable rendered doctrine backed by structured objects
