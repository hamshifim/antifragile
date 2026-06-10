# Adversarial Messaging Protocol Plan (Slack or Local Kafka by Configuration)

## 1. Purpose
Define a planning-level protocol for adversarial agent messaging that:
- mitigates context decay and context drift
- preserves strict attribution (user intent vs agent inference)
- supports configurable transport selection: `slack` or `kafka` (or both)
- aligns with existing Wielder antifragile doctrine and PEPS third-party Kafka deployment patterns

This document is planning-only and does not introduce implementation code.

## 2. Inputs Re-Read and Design Constraints

### 2.1 Antipattern constraints (wielder-antifragile)
1. [context-drift.md](antipatterns/context-drift.md)
- context drift is multi-axis (`semantic`, `structural`, `spatial`, `temporal`)
- protocol must enforce attribution and bounded stepping stones

2. [hard-stopping.md](antipatterns/hard-stopping.md)
- high-risk actions should be wrapped and auditable rather than permanently blocked
- Slack/MCP-like channels are valid governance surfaces

3. [style-drift.md](antipatterns/style-drift.md)
- protocol must keep OOD rulebooks loaded in-loop, not only in docs

4. [AGENTIC_ADVERSARIAL_WORKFLOW.md](../foundation/workflows/adversarial/AGENTIC_ADVERSARIAL_WORKFLOW.md)
- stepping stones are mandatory
- red-team handoff with attribution check is mandatory

### 2.2 Kafka deployment constraints (PEPS third-party)
From `~/dev/peps/pep-services/src/wield_services/apps/third_party/helm/kafka`:
- Kafka is deployed via Helm (`kafka_deploy.py`) and environment-scoped HOCON (`aws/docker/kind`)
- local environments (`docker`, `kind`) expose domain `127.0.0.1` with external access config
- node ports are auto-populated from `30000 + i` for `replicaCount`
- this supports a realistic local transport for adversarial messaging without cloud dependency

## 3. Protocol Objectives
1. Prevent conflation of agent assumptions with user-stated intent.
2. Force explicit handoff artifacts between personas.
3. Ensure every step is auditable and replayable.
4. Keep transport pluggable without changing workflow semantics.
5. Support fail-closed behavior on missing critical artifacts.

## 4. Transport-Abstraction Model

## 4.1 Logical interface
The protocol uses one logical messaging interface:
- `publish(message)`
- `subscribe(stream)`
- `ack(message_id)`
- `dead_letter(message, reason)`

Transports implement the same semantics:
- Slack transport (`channels` + thread IDs)
- Kafka transport (`topics` + keys + offsets)

## 4.2 Configuration switch
Single config key selects behavior:
- `transport = slack | kafka | dual`

`dual` is recommended for early rollout:
- Slack for human visibility/governance
- Kafka for durable replay and machine audit

## 5. Message Contract (Canonical Envelope)
Every protocol message must include:
- `protocol_version`
- `workflow_id`
- `stepping_stone_id`
- `message_id`
- `parent_message_id` (nullable)
- `timestamp_utc`
- `author_persona` (`planner`, `blue_team`, `red_team`, `governor`)
- `message_type`
- `user_request_ref` (pointer or digest)
- `agent_assumptions` (explicit list)
- `scope_in` and `scope_out`
- `artifacts` (test report refs, diff refs, config refs)
- `decision` (`pass`, `fail`, `needs_clarification`)
- `integrity_hash`

## 5.1 Core message types
- `SCOPE_DECLARATION`
- `IMPLEMENTATION_PROOF`
- `RED_TEAM_REPORT`
- `ATTRIBUTION_CHECK`
- `DECISION_GATE`
- `REWORK_ORDER`
- `STEP_CLOSED`
- `DRIFT_ALERT`

## 6. Persona Messaging Sequence
1. Planner emits `SCOPE_DECLARATION`.
2. Blue Team emits `IMPLEMENTATION_PROOF`.
3. Red Team emits `RED_TEAM_REPORT` + `ATTRIBUTION_CHECK`.
4. Governor emits `DECISION_GATE`.
5. If failed, Governor emits `REWORK_ORDER` and loop continues.
6. If passed, emit `STEP_CLOSED` and advance stepping stone.

Fail-closed rule:
- advancing is forbidden if `ATTRIBUTION_CHECK` is absent.

## 7. Slack Mapping Plan
Use channels by lifecycle:
- `#adversarial-scope`
- `#adversarial-redteam`
- `#adversarial-gates`
- `#adversarial-alerts`

Threading:
- one Slack thread per `workflow_id`
- one thread segment per `stepping_stone_id`

Governance:
- `DECISION_GATE` requires explicit approver identity in message metadata

## 8. Kafka Mapping Plan
Use topics by contract type:
- `wielder.adversarial.scope`
- `wielder.adversarial.proof`
- `wielder.adversarial.redteam`
- `wielder.adversarial.gates`
- `wielder.adversarial.alerts`
- `wielder.adversarial.dlq`

Partitioning key:
- `workflow_id`

Ordering goal:
- preserve per-workflow ordering while allowing cross-workflow parallelism

Retention:
- short retention for high-volume proof topics
- extended retention for `gates` and `alerts`

## 9. Drift Controls Embedded in Protocol
1. Attribution Control
- every step must separate user requirements vs agent assumptions.

2. Scope Control
- each message carries `scope_in` and `scope_out`.

3. Temporal Control
- strict `parent_message_id` chain prevents context jumps.

4. Spatial Control
- artifact references must point to canonical repository/data-lake locations only.

5. Structural Control
- schema validation on every message envelope before accept.

## 10. Critical Audit Rules
1. Block progression if:
- missing `SCOPE_DECLARATION`
- missing `ATTRIBUTION_CHECK`
- missing `DECISION_GATE`

2. Raise `DRIFT_ALERT` if:
- assumptions grow between steps without user re-ack
- scope_out expands without planner authorization
- repeated rework loops exceed threshold

3. Require explicit closure summary at each `STEP_CLOSED`:
- what changed
- what was rejected
- what remains out of scope

## 11. Incremental Rollout Plan (Stepping Stones)
1. Stepping Stone A: Canonical envelope + message types (docs only)
2. Stepping Stone B: Slack-only manual protocol trial
3. Stepping Stone C: Kafka-only local protocol trial (docker/kind)
4. Stepping Stone D: Dual transport mirror (`slack` + `kafka`)
5. Stepping Stone E: Fail-closed gate enforcement and drift alerts

Each stone requires a red-team audit before advancing.

## 12. Configuration Plan (Planning Schema)
Proposed config tree:
- `adversarial_messaging.transport`
- `adversarial_messaging.protocol_version`
- `adversarial_messaging.slack.channels.*`
- `adversarial_messaging.kafka.bootstrap_servers`
- `adversarial_messaging.kafka.topics.*`
- `adversarial_messaging.kafka.retention.*`
- `adversarial_messaging.gates.max_rework_loops`
- `adversarial_messaging.audit.require_attribution_check`

## 13. Risks and Mitigations
1. Risk: Message overload in large workflows.
- Mitigation: strict message types + bounded artifacts + topic/channel separation.

2. Risk: Slack-only mode lacks durable replay.
- Mitigation: prefer `dual` for critical phases.

3. Risk: Kafka-only mode reduces human visibility.
- Mitigation: emit gate summaries to Slack even in Kafka-primary mode.

4. Risk: Protocol bypass through direct chat.
- Mitigation: hard rule that gate decisions outside protocol are invalid.

## 14. Success Criteria
- Zero stepping-stone advancement without attribution check.
- Measurable reduction in context-drift incidents during adversarial loops.
- Deterministic replay of workflow decisions from message log.
- Equivalent workflow semantics under both Slack and Kafka transports.
