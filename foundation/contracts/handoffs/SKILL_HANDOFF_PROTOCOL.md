---
description: Inter-Persona Communication and Context Handoffs
---
# Handoff Protocol & Diagnostic Reporting

To survive the context wipe when switching from the Blue Team Builder to the Red Team QA Architect, the AI must communicate using formalized **Handoff Reports**. Merely saying "I fixed it" is an architectural violation.

For Wielder-managed work, operator-facing commands must also follow [Wielder Handoff & Operator Command Reporting](../../skills/wielder/script_skills/SKILL_WIELDER_HANDOFF.md). In particular, assume the operator is already in the intended zsh/uvenv project shell unless the task is workstation bootstrap, and do not pad handoffs with `cd`, `python -m`, virtualenv activation, shell aliases, or environment-variable rituals when an installed CLI or direct Wielder entrypoint is the designed surface.

## 1. The Blue Team Proof (Builder Handoff)
When the Developer completes a Stepping Stone and yields control back to the Red Team, it must present a structured proof. It cannot rely on the QA architect to infer its intentions.
- **Physical Output Linkage**: The Developer must specify the absolute paths of the generated physical mock outputs (e.g., `/tmp/test_report.pdf` or output parity logs).
- **Test Command**: The Developer must literally provide the `pytest` command or terminal string it used to claim the Stepping Stone is green. For Wielder work, rewrite internal validation commands into operator command shape: no preceding `cd`, no redundant interpreter path, and no virtualenv activation when the operator zsh/uvenv shell already supplies it.
- **Architectural Defense**: If the Developer actively rejected a Red Team critique due to "Einstein Simplicity" or Scope Creep, it must assert its reasoning formally in the handoff.

## 2. The Red Team Report (Skeptic Handoff)
The QA Architect must process the `git diff` and the Developer's Handoff Proof, and then formally yield a **Red Team Report** back to the Builder. It must be highly structured:
- **🐞 Bugs & Edge Cases**: Identifying logical flaws in the Python loops or missing Null exception handling.
- **🏛️ Architectural Violations**: Highlighting explicitly if PyHocon constraints, partition hierarchies, or dot-notation standards were breached.
- **💅 Style & Naming**: Enforcing accurate domain wording and strict decoupling of OS paths vs Cloud URIs.
- **📉 Verifiability**: Confirming or tearing down the validity of the Blue Team's testing proof.
