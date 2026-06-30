# Resolved Wielder Config

Resolved config is the contract an entrypoint actually executes. When behavior
looks surprising, inspect the resolved app or service config before changing
Python code.

## Resolution Rule

Treat the canonical accessor as the only source of truth for a contract:

- Project or app entrypoints use the project-local `get_app_conf(...)`.
- Service entrypoints use the project-local service accessor when one exists.
- Cross-repo callers load a foreign app through that foreign repo's canonical
  accessor, then read only the specific owned fields they need.

Do not recreate resolution by hand from `project.conf`, ecosystem manifests,
mode files, and context packs. That creates a side loader and a second config
truth.

## Investigation Order

1. Run the nearest endpoint in `-w plan` mode.
2. Inspect the resolved app/service contract emitted by that endpoint or its
   staged plan artifacts.
3. Compare the same field across the smallest useful chain: project config,
   ecosystem family, thin phenotype ecosystem, app config, test overlay, context
   pack, and CLI.
4. Fix the first ownership layer where the value diverges.

Python fallback branches, string normalizers, and defensive defaults are not
config fixes. They only hide the wrong owner.

## Neutral Contexts

`default_conf` is not an implicit CLI. Keep mode values and live dates out of
neutral developer contexts. Put deliberate local intent in a named context pack
or an ignored generated ephemeral config file.

## Runtime Polymorphism

Some apps have one domain contract with several valid runtime expressions. A
service may run from workstation source, in Kubernetes, as a CPU or accelerator
profile, against an inner or outer broker endpoint, or through different mounted
bucket roots. Those are runtime phenotypes, not different domain contracts.

The app may branch on resolved typed leaves, but the branch selector must still
come from config. If the selector becomes useful to another app, move it toward
the shared ecosystem or service contract instead of copying it.
