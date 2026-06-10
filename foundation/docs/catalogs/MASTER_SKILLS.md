# Master Skills Index

To ensure architectural alignment across varying Python execution environments and frameworks, ALL agents operating within the `domain-data` Data Lake ecosystem must formally implement the following Operational Skills. These strict guardrails replace ad-hoc reasoning and improve precision across physical artifacts and logic nodes.

## Package-Level Skill Guidelines

- **[Package Guidelines](../../skills/wielder/SKILL_PACKAGE_GUIDELINES.md)**
  *Scope:* Shared Wielder skill-package rules that apply across many skills, including cloud, OAuth, connector-auth, MFA, and session-expiry boundaries that individual skills should reference rather than repeat.

## Defined Engineering Skills

1. **[Configuration & Datastore Lineage](../../skills/wielder/SKILL_CONFIGURATION_GUIDELINES.md)**
   *Scope:* Wielder PyHocon constraint mapping, local environment sandboxing (`developer.conf`), explicit failure rules over protective exceptions, and `<run_uuid>` partition isolation parameters.

2. **[Wielder Ecosystem Guidelines](../../skills/wielder/SKILL_ECOSYSTEM_GUIDELINES.md)**
   *Scope:* Multi-surface ecosystem topology, app-vs-deployment semantics, core-union ecosystem family contracts, thin phenotype overlays, dependency routing, concrete bootable ecosystems, and local WSL GPU cluster surface choices.

3. **[Workflow Validation Doctrine](../../skills/wielder/SKILL_WORKFLOW_VALIDATION_GUIDELINES.md)**
   *Scope:* Front-and-center Wielder doctrine for treating workflow entrypoints as configurable integration, system, load, and production execution surfaces across ecosystems, surfaces, and stage tiers.

4. **[Antifragile Evolution During Live System Tests](../../skills/wielder/SKILL_ANTIFRAGILE_EVOLUTION.md)**
   *Scope:* Treating live Wielder system tests as sanctioned engineering workbenches where real failures, operator feedback, and workflow pressure guide small source/config improvements through managed entrypoints.

5. **[Wielder Scripting & Evaluation Skills](../../skills/wielder/SKILL_WIELDER_SCRIPTS.md)**
   *Scope:* Thin Wielder orchestration scripts, configuration-driven filesystem operations, local action discipline, long-running handoffs, and backend CLI configuration from resolved HOCON.

6. **[Local Hybrid Dev Workflow](../../skills/wielder/SKILL_LOCAL_HYBRID_DEV_WORKFLOW.md)**
   *Scope:* Fast local app or service iteration against a full remote/provider ecosystem using thin hybrid overlays, local server/client/GPU-service restart discipline, provider-backed service probes, and clear handoffs for image, Kubernetes, Spark, or cloud runtime changes.

6. **[Wielder Imager & Staging Sandboxing](../../skills/wielder/SKILL_WIELDER_IMAGER.md)**
   *Scope:* Isolated Docker staging sandboxes, image build/push/runtime topology, committed-state image verification, build-surface detection, and workflow-driven image validation.

7. **[Git Versioning Guidelines](../../skills/wielder/SKILL_GIT_VERSIONING.md)**
   *Scope:* Agent-created commit provenance, adversarial pre-commit audit, super-repo/submodule commit order, and committed-state image/deploy version integrity.

8. **[Docker Skill](../../skills/wielder/DOCKER_SKILL.md)**
   *Scope:* Local Docker instability diagnosis for large images, Docker Desktop/WSL resource surfaces, buildx health, cache pressure, volume footprint, and safe prune levels.

9. **[Disk Cleanup](../../skills/wielder/SKILL_DISK_CLEANUP.md)**
   *Scope:* Safe local disk pressure triage across Docker build cache, unused images, Wielder staging sandboxes, Terraform provisioning clones, local buckets, and workstation caches.

10. **[Spark Scalable Validation Doctrine](../../skills/wielder/SKILL_SPARK_SCALABLE_VALIDATION_GUIDELINES.md)**
   *Scope:* Spark-specific doctrine for treating unit, integration, system, and load execution as one configurable validation family driven by the same pipeline core, source/sink contracts, and pressure settings.

11. **[Interactive Notebook Hygiene](../../skills/wielder/SKILL_NOTEBOOK_GUIDELINES.md)**
   *Scope:* Banning multi-display DOM memory leaks, `# %%` script duality parsing, and the fundamental rejection of defensive error wrappers (`if not df.empty`) inside Jupyter analytical cells.

12. **[Raw Data Ingestion Tiering](../../skills/wielder/SKILL_DATA_INGESTION_GUIDELINES.md)**
   *Scope:* Separating reusable protocol, transient experiment metadata, and empirical measurements; hashing protocol drift; keeping audit leftovers distinct from raw data tiers.

13. **[Table Schema Guidelines](../../skills/wielder/SKILL_TABLE_SCHEMA_GUIDELINES.md)**
   *Scope:* Reusable table schema ownership, mandatory concise table/column descriptions, human-readable preview legends, and column ordering for inspection.

14. **[Live Quality Assurance Testing](../../skills/wielder/SKILL_TEST_GUIDELINES.md)**
   *Scope:* Mandating live endpoint validations over `unittest.mock` illusions, asserting PySpark O(1) dimensionality querying mathematically, using typed human-readable evidence reports for reactive distributed integration tests, and securely abstracting physical image sink footprints into `/tmp/` or ignored artifacts.

15. **[Reactive Distributed Integration Testing](../../skills/wielder/SKILL_REACTIVE_DISTRIBUTED_INTEGRATION_TESTS.md)**
   *Scope:* First-principles live integration tests for distributed reactive flows, using simple node descriptions, provenance nuggets, explicit wait conditions, meaningful logs, and accumulated human-readable state reports.

16. **[Domain Scope & Boundary Preservation Constants](../../skills/wielder/SKILL_SCOPE_GUIDELINES.md)**
   *Scope:* Eradicating scope creep, isolating execution pipelines to assigned architectures, enforcing Einstein Simplicity, and explicitly acknowledging epistemic humility.

17. **[Einstein Simplicity](../../skills/wielder/SKILL_EINSTEIN_SIMPLICITY.md)**
   *Scope:* Simplicity discipline for distributed orchestration: thin outer layers, boundary-local branching, responsible-layer ownership, convergence over coordination, and abstraction restraint.

18. **[Naming Doctrine](../../skills/wielder/SKILL_NAMING_GUIDELINES.md)**
   *Scope:* Layer-aware naming for domain, operational, and infrastructure code, with review heuristics for ambiguity, boundary state, and provenance/security-sensitive symbols.

19. **[Stepping Stone Parcelling Strategy](../../skills/wielder/SKILL_PARCELLING_GUIDELINES.md)**
   *Scope:* Forbidding massive multi-file refactors and requiring incremental, test-gated stepping stones with explicit builder-to-skeptic handoff boundaries.

20. **[Handoff Protocol & Reporting](../../contracts/handoffs/SKILL_HANDOFF_PROTOCOL.md)**
   *Scope:* Formalizing the structured communication standard (Blue Team Proof vs Red Team Report) that must be passed natively between personas during context wiping to ensure execution tracing is never hallucinated.

21. **[Yoda-Led Jedi Council](../../skills/wielder/SKILL_YODA_COUNCIL.md)**
   *Scope:* Governing approval transition from planning to execution, requiring disciplined anti-hubris checks and empirically grounded boundary mathematics.

22. **[Grill Me](../../skills/wielder/SKILL_GRILL_ME.md)**
   *Scope:* One-question-at-a-time adversarial plan interrogation, with repository inspection before asking and a recommended answer for every question.

23. **[Operator Alignment](../../skills/wielder/SKILL_OPERATOR_ALIGNMENT.md)**
   *Scope:* Compressing repeated operator corrections and repository evidence into durable config, docs, tests, glossary terms, and task handoffs without relying on chat memory.

24. **[Security Guidelines](../../skills/wielder/SKILL_SECURITY_GUIDELINES.md)**
   *Scope:* Security, secrets, IAM/RBAC, runtime identities, cross-cloud credentials, and stage-tier naming for permission-bearing resources.

25. **[Security Versioning Gate](../../skills/wielder/SKILL_SECURITY_VERSIONING.md)**
   *Scope:* Pre-commit security/versioning audit for reusable framework repositories, clean trunk baselines, and branch contamination cleanup.

26. **[Concise Operator Communication](../../skills/wielder/SKILL_CONCISE_OPERATOR_COMMUNICATION.md)**
   *Scope:* Short, informative, tangent-free operator answers for unfamiliar technical plans and security-sensitive decisions.

27. **[Agent Partner Communication](../../skills/wielder/SKILL_AGENT_PARTNER_COMMUNICATION.md)**
   *Scope:* External stakeholder messages where an agent speaks as a named partner to a human operator, preserving attribution, clear review asks, and non-impersonating Slack/email/doc tone.

28. **[WJobBard Guidelines](../../skills/wielder/SKILL_WJOBBARD_GUIDELINES.md)**
   *Scope:* Scheduled or event-triggered Wielder jobs, lifecycle/result events, payload target references, and provider-backed runtime handoffs.

29. **[Service Deployment Guidelines](../../skills/wielder/SKILL_SERVICE_DEPLOYMENT_GUIDELINES.md)**
   *Scope:* Service-named image and deploy entrypoints, plan/apply/run/delete/monitor command shape, image provenance, WJobBard composition, and hosted runtime boundaries.

30. **[Provisioning Guidelines](../../skills/wielder/SKILL_PROVISIONING_GUIDELINES.md)**
   *Scope:* Durable infrastructure planning and provisioning across provider surfaces, including cross-cloud dependency checks, workload identity federation, and links to Terraform, Kubernetes, WJobBard, storage cloning, security, imaging, and monitoring surfaces.

31. **[Model Artifact Provisioning](../../skills/wielder/SKILL_MODEL_ARTIFACT_PROVISIONING.md)**
   *Scope:* Generic workstation model tooling, app-owned model artifact provision steps, idempotent existing-cache behavior, and WClone/rclone/Hugging Face/Ollama cache surfaces.

32. **[Context Initiation Alignment](../../skills/wielder/SKILL_CONTEXT_INITIATION_ALIGNMENT.md)**
   *Scope:* Establishing minimal agent base context for a Wielder/Antifragile project through a light project/module role skim, abstraction-layer recognition, configuration ecology orientation, a short gestalt recap, and a final new-work-vs-recovery question.

33. **[Context Recovery Alignment](../../skills/wielder/SKILL_CONTEXT_RECOVERY_ALIGNMENT.md)**
   *Scope:* Recovering lost Workspace Codex thread context through concise alignment summaries over doctrine, task artifacts, dirty super-repo and submodule diffs, and recent commits before running Grill Me until the recovered goal is confirmed.

34. **[Antifragile Workstation Control Plane](../../skills/wielder/SKILL_ANTIFRAGILE_WORKSTATION_CONTROL_PLANE.md)**
   *Scope:* Designing, rebuilding, and recovering a human workstation that also acts as an infrastructure control plane, with explicit local-state taxonomy, auth/tooling validation, snapshots, and crash-recovery discipline.

35. **[Remote Workstation](../../skills/wielder/SKILL_REMOTE_WORKSTATION.md)**
   *Scope:* Remote Ubuntu workstation path geometry, dev/prod checkout roles, local-vs-remote handoff discipline, and secure site run/exposure planning.

36. **[MCP Browser Bridge](../../skills/wielder/SKILL_MCP_BROWSER_BRIDGE.md)**
   *Scope:* Connecting WSL-hosted Codex sessions to authenticated Windows Chrome profiles through Playwright MCP extension mode, including HTTP endpoint registration, host routing, validation, and common failure recovery.

37. **[Task Management White Paper](../../skills/wielder/TASK_MANAGEMENT_WHITE_PAPER.md)**
   *Scope:* Goal lineage, task parcelling, atomic execution visibility, compartmentalized access, ownership traceability, review roles, and asynchronous coordination doctrine.

38. **[Org Task Wielding](../../skills/wielder/SKILL_ORG_TASK_WIELDING.md)**
   *Scope:* Wielding task-management, messaging, documentation, diagramming, reporting, and adjacent organizational systems so configured third-party platforms advance explicit goals from the task-management white paper.

39. **[Monday MCP](../../skills/wielder/SKILL_MONDAY_MCP.md)**
   *Scope:* Connecting WSL-hosted Codex to monday.com through monday.com's MCP server, including Windows token bridging, local stdio registration, validation, and common failure recovery.

40. **[Wielder Handoff & Operator Command Reporting](../../skills/wielder/SKILL_WIELDER_HANDOFF.md)**
   *Scope:* Wielder-style operator handoffs with config-owned intent, root-safe absolute commands, plan/apply/test reporting, and clear separation between agent-internal validation commands and human-run commands.

41. **[Consulting Mode](../../skills/wielder/SKILL_CONSULTING_MODE.md)**
   *Scope:* Provisional architectural discussion, conflicting hypotheses, tradeoff exploration, and decision hygiene without turning operator indecision into implementation, config, or downstream handoff residue.

41. **[Runtime Event Logging](../../skills/wielder/SKILL_RUNTIME_EVENT_LOGGING.md)**
   *Scope:* Framed operator-readable logs for long-running workers, Kafka consumers, Spark jobs, and Wielder launchers, including lifecycle events, stable identifiers, busy heartbeats, and failure stack trace preservation.

## Related Catalogs

- **[Wieldable Functionalities](WIELDABLE_FUNCTIONALITIES.md)**
  *Scope:* Growing index of reusable operator-facing Wielder capabilities such as Terraform provisioning, Kubernetes workloads, storage cloning, and runtime CLI configuration.
