# Git Specialist Bundle

This directory is the first exemplar of the object bundle convention.

- [persona.hocon](persona.hocon)
  Structural metadata, inheritance, tools, outputs, and final fields.
- [body.md](body.md)
  Human-authored markdown body for the persona.

The intended wrapper behavior is:

1. load `persona.hocon`
2. resolve inheritance
3. load `body.md`
4. render a resolved audit artifact into `.foundation_audit/`
