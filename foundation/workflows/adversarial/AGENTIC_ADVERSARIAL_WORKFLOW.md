# AGENTIC_ADVERSARIAL_WORKFLOW.md

## Objective
To strictly enforce architectural integrity and avert hubristic "builder's bias" by structurally splitting the Artificial Intelligence into an adversarial Red Team (QA Skeptic) / Blue Team (Developer) loop during implementation runs.
Additionally, this workflow explicitly mitigates **context decay** where agents can accidentally conflate user intent with their own prior assumptions.

## The Execution Pipeline

### Step 1: Parcel and Map ("Stepping Stones")
The global task must NOT be executed as a monolith. The AI must break down the final objective into minimal, viable "Stepping Stones" complete with live `pytest` coverage matrices mapped out beforehand.
Each stepping stone must include a short scope declaration:
- what the user explicitly requested
- what assumptions were introduced by the agent
- what is intentionally out of scope for this step

### Step 2: Implement the Stepping Stone (Blue Team)
The AI Builder executes the absolute minimum amount of WET code or refactoring to push the isolated functionality across the finish line for the **current step only**. No over-engineering.

### Step 3: The System Architect Pause (Red Team Hand-off)
The AI forcefully stops acting as the Builder. It reads [PERSONA_QA_ARCHITECT.md](../../personas/wielder/PERSONA_QA_ARCHITECT.md) to flush out its builder goals and reboot its context into the ultimate skeptic.
- **The Observation**: The QA Architect critically audits the `git diff`, queries the Data Lake output parity, and evaluates the `pytest` results.
- **The Strike**: It evaluates the state strictly according to the Anti-Hubris, Isolation, and Hardcoding protocols embedded in its persona.
- **The Deliverable**: It generates the `Red Team Report` (Bugs, Architectural Deviations, Naming, Test Missingness), including an explicit **Attribution Check** that separates user-stated requirements from agent-inferred additions.

### Step 4: The Pragmatic Review (Blue Team Return)
The AI re-reads [PERSONA_PLATFORM_DEVELOPER.md](../../personas/wielder/PERSONA_PLATFORM_DEVELOPER.md). It ingests the Red Team Report aggressively.
- It rejects constraints that violate "Einstein Simplicity."
- It accepts correct edge cases and structural violations, resolving to implement them cleanly.
- It must not carry over unstated assumptions without re-labeling them as assumptions in the next stepping stone scope declaration.

### Step 5: Implementation & Validation
The Blue Team executes the fixes derived from the QA Report. It re-runs the live test suite on the actual Data Lake/Endpoints to probabilistically prove the change.

### Step 6: The Iterative Loop
Repeat Steps 3, 4, and 5 continuously *for the current stepping stone* until the hostile QA Architect yields an acceptable standard. Only then is the AI authorized to advance to Step 1 for the *next* block of work.
This loop is intentionally adversarial to force recurring context re-synchronization before scope expands.

### Step 7: Provisional Single-Agent Simulation (Pre-Daemon)
*Note: Until the Monday.com and Slack MCP interaction daemons are fully live to delegate multi-threaded agents natively, a single AI model must sequence this entire pipeline alone.*
To enforce structural integrity and legally wipe context without a daemon, the Agent MUST:
1. Physically output the **Handoff Report/Proof** directly into its execution chain.
2. Explicitly execute a `view_file` call against the opposing Persona Markdown document (e.g. [PERSONA_QA_ARCHITECT.md](../../personas/wielder/PERSONA_QA_ARCHITECT.md) or [PERSONA_PLATFORM_DEVELOPER.md](../../personas/wielder/PERSONA_PLATFORM_DEVELOPER.md)) and the required `SKILL_*.md` scopes.
3. **Autonomous Continuation**: The AI MUST NOT halt or demand user approval via rigid blocking boundaries between Stepping Stones. It must recursively swap its own persona, write the internal report, and automatically execute the next step independently until the entire Phase is green.
