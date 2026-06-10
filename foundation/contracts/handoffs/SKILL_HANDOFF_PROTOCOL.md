---
description: Inter-Persona Communication and Context Handoffs
---
# Handoff Protocol & Diagnostic Reporting

To survive the context wipe when switching from the Blue Team Builder to the Red Team QA Architect, the AI must communicate using formalized **Handoff Reports**. Merely saying "I fixed it" is an architectural violation.

## 1. The Blue Team Proof (Builder Handoff)
When the Developer completes a Stepping Stone and yields control back to the Red Team, it must present a structured proof. It cannot rely on the QA architect to infer its intentions.
- **Physical Output Linkage**: The Developer must specify the absolute paths of the generated physical mock outputs (e.g., `/tmp/test_report.pdf` or output parity logs).
- **Test Command**: The Developer must literally provide the `pytest` command or terminal string it used to claim the Stepping Stone is green.
- **Architectural Defense**: If the Developer actively rejected a Red Team critique due to "Einstein Simplicity" or Scope Creep, it must assert its reasoning formally in the handoff.

## 2. The Red Team Report (Skeptic Handoff)
The QA Architect must process the `git diff` and the Developer's Handoff Proof, and then formally yield a **Red Team Report** back to the Builder. It must be highly structured:
- **🐞 Bugs & Edge Cases**: Identifying logical flaws in the Python loops or missing Null exception handling.
- **🏛️ Architectural Violations**: Highlighting explicitly if PyHocon constraints, partition hierarchies, or dot-notation standards were breached.
- **💅 Style & Naming**: Enforcing accurate domain wording and strict decoupling of OS paths vs Cloud URIs.
- **📉 Verifiability**: Confirming or tearing down the validity of the Blue Team's testing proof.
