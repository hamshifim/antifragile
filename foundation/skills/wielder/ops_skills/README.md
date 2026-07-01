# Wielder Ops Skills

This directory groups operational doctrine for infrastructure, runtime
surfaces, security, versioning, artifacts, workstations, images, and cleanup.

## Routing

- [Provisioning Guidelines](SKILL_PROVISIONING_GUIDELINES.md): durable
  infrastructure planning, provider resources, cross-cloud dependencies, and
  provision/destroy boundaries.
- [Security Guidelines](SKILL_SECURITY_GUIDELINES.md): secrets, IAM/RBAC,
  runtime identities, cross-cloud credentials, and stage-tier naming.
- [Security Versioning](SKILL_SECURITY_VERSIONING.md): pre-commit security and
  versioning gates for framework/doctrine repositories.
- [Git Versioning](SKILL_GIT_VERSIONING.md): commit provenance,
  super-repo/submodule ordering, branch parity, and image/deploy version truth.
- [Wielder Imager](SKILL_WIELDER_IMAGER.md): image staging sandboxes, Docker
  context discipline, registry tags, and workflow-driven image validation.
- [Epoch Artifact Governance](SKILL_EPOCH_ARTIFACT_GOVERNANCE.md): immutable
  artifact classes across provisioning, images, resolved config, and code
  bundles.
- [Artifactory Guidelines](SKILL_ARTIFACTORY_GUIDELINES.md): Python/Spark code
  bundle publication, WGit source archiving, shared runtime artifacts, and
  configured artifact bucket/key contracts.
- [Model Artifact Provisioning](SKILL_MODEL_ARTIFACT_PROVISIONING.md): model
  cache, WClone/rclone, Hugging Face, Ollama, and app-owned model asset setup.
- [Antifragile Workstation Control Plane](SKILL_ANTIFRAGILE_WORKSTATION_CONTROL_PLANE.md):
  human workstation design, recovery, local-state taxonomy, and control-plane
  resilience.
- [Remote Workstation](SKILL_REMOTE_WORKSTATION.md): remote Ubuntu workstation
  path geometry, clone roles, browser access, and secure site handoffs.
- [Docker Skill](DOCKER_SKILL.md): Docker/WSL instability diagnosis, build cache
  pressure, VHD compaction, and safe prune levels.
- [Disk Cleanup](SKILL_DISK_CLEANUP.md): safe disk-pressure cleanup order across
  Docker, staging sandboxes, provisioning clones, and local buckets.
- [WSL Cleanup](SKILL_WSL_CLEANUP.md): WSL disk-pressure recovery, cache
  pruning, active `unique_name` preservation, `fstrim`, VHDX compaction, and
  post-restart verification.
- [Runtime Event Logging](SKILL_RUNTIME_EVENT_LOGGING.md): operator-readable
  lifecycle logs, stable identifiers, heartbeats, and failure traces.
