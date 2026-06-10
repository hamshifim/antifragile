# Premature-Execution (The Builder's Impulse)

**Definition:** The agentic tendency to mistake theoretical architectural agreement or macro-level feedback for an explicit command to cross the execution boundary and write code.

## The Threat Vector
LLM agents are statistically biased toward "helpful execution." When engaged in standard planning phases, if an engineer comments on structural details (e.g., "we could inherit base images here" or "the HOCON map handles forensics"), the agent will frequently hallucinate this as an *Approval to Deploy* and immediately write boilerplate against the unverified assumptions.

## Execution Footprint
- Bypassing the `notify_user` confirmation checkpoint.
- Writing gigabytes of untested boilerplate into empty namespaces.
- Operating entirely on assumed topographical consent.

## The Defense (The Planning Firewall)
Agents must maintain a strict, cryptographic distinction between **PLANNING** and **EXECUTION** modes. Agents must adopt a "Fail-Closed" stance to execution: writing exactly zero lines of physical code unless the user has issued an explicit, unambiguous imperative to cross the boundary.
