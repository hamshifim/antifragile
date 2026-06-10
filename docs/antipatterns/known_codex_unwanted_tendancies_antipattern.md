# Known Codex Unwanted Tendencies Antipattern

This note names recurring Codex failure modes observed while wielding Wielder
projects. Treat these as review smells, not personality traits. If one appears,
repair the ownership boundary rather than normalizing the workaround.

The filename preserves the operator phrase `known_codex_unwanted_tendancies` so
future searches find it even with that spelling.

## Gnostic CLI

**Smell:** A script gains a new private CLI flag because one run needs a branch,
dataset, cluster, timeout, approval choice, or routing fact.

**Why it is harmful:** The flag becomes a second operator control plane beside
resolved HOCON. Future runs cannot tell whether intent lives in config, chat, or
shell history.

**Preferred move:** Put durable or replayable intent in the owning app,
ecosystem, or `context_conf/<name>/developer.conf`. If the config leaf is
missing, fail closed with a message naming the required key and expected owner.
Keep Wielder CLI arguments for broad framework modulation such as ecosystem,
stage tier, security, context pack, test overlay, and action.

## Environment Variable Side Channel

**Smell:** A human-facing workflow depends on an exported environment variable
for a choice that should be reproducible, reviewable, or versioned.

**Why it is harmful:** Environment variables are invisible to plan output and
easy to forget across terminals, workstations, containers, or handoffs.

**Preferred move:** Use resolved config or secrets as the control plane. Mirror
values into environment variables only at the platform boundary where a
container, SDK, CLI, or provider requires process input.

## CLI Override Wrapping

**Smell:** One Wielder entrypoint manually reconstructs or forwards a bundle of
CLI overrides to another entrypoint, especially by copying lifecycle fields such
as `stage_tier`, `security`, `destroy`, `canary`, `context_conf`, `test`, and
`action`.

**Why it is harmful:** The wrapper reimplements the resolver and can silently
diverge from native Wielder precedence. It turns config resolution into a
hand-carried object graph.

**Preferred move:** Let the downstream canonical accessor resolve its own
config. If a topology switch is genuinely required, override only that narrow
dimension and document why. If the downstream entrypoint needs a durable choice,
add it to the owning config rather than smuggling it through a wrapper.

## Corrective Review Questions

- Where does the operator intent live in resolved HOCON?
- Does `-w plan` expose the same value that `-w apply` will use?
- Is this value durable enough to belong in config rather than a shell?
- Is this script invoking another Wielder surface because ownership demands it,
  or because we are patching around a missing app/ecosystem contract?
- Could the downstream app resolve this natively if the ecosystem contract were
  complete?
