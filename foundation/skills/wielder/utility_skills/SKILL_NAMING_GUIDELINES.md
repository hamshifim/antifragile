---
description: Choose cohesive names that expose purpose, ownership and consequential state in their local layer.
---

# Naming

Names should help a reader understand what a component does and where its
responsibility ends. Use the vocabulary of the owning domain or Wielder layer.

## Conventions

- Name scientific and business concepts in domain terms.
- Name infrastructure mechanisms accurately: ports, queues, mounts and
  subprocess arguments are meaningful concepts in that layer.
- Expose consequential distinctions such as source versus destination,
  raw versus processed, and local path versus object key.
- Prefer verbs that disclose effects. A function that updates configuration
  should not sound like a passive lookup.
- Keep related APIs consistent. Avoid repeating the package name in every
  symbol when qualification already establishes ownership.
- Use short conventional variables where their meaning is local and obvious.
  Use descriptive names when their meaning must survive across functions or
  boundaries.

A name is not wrong merely because it is short, resembles a type or lacks a
prescribed suffix. Judge it in context. Do not rename established APIs for
cosmetic conformity without considering caller churn and compatibility.

## Review

Ask whether a reader can infer the purpose and safely distinguish inputs,
outputs and side effects. A misleading source/destination name warrants more
attention than a harmless stylistic inconsistency.

For a rename, inspect definitions, imports, aliases, qualified calls, dynamic
references, tests and documentation. Check for collisions with project wrappers.
Verify the affected call paths; a textual replacement alone does not establish
correctness.
