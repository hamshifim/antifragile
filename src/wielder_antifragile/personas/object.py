"""Persona bundle resolution and audit rendering."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pyhocon import ConfigFactory

from wielder_antifragile.core.utils import ensure_audit_root, get_global_conf_hash, get_project_conf, write_json

TypedConfig = Any

# Phase 0 simplified inheritance model:
# - single-parent inheritance through `base`
# - mixin inheritance through `extends` is currently disabled
# - only a narrow, explicit set of fields may be overridden from base personas
ALLOWED_PERSONA_OVERRIDE_FIELDS = {
    "domain_vocabulary",
    "escalation_behavior",
    "final",
    "outputs",
    "priorities",
    "prompt_body_file",
    "scope_notes",
    "tools",
    "version",
}

_RESERVED_FIELDS = {"id", "kind", "base", "extends"}


def _parse_hocon(path: Path) -> TypedConfig:
    if not path.exists():
        raise FileNotFoundError(f"HOCON file not found at {path}")
    return ConfigFactory.parse_file(path.as_posix(), resolve=True)


def _config_to_dict(conf: TypedConfig) -> dict[str, Any]:
    if hasattr(conf, "as_plain_ordered_dict"):
        return conf.as_plain_ordered_dict()
    return dict(conf)


def _merge_dicts(base_dict: dict[str, Any], overlay_dict: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base_dict)
    for key, value in overlay_dict.items():
        if key in {"final", "tools"}:
            merged[key] = list(dict.fromkeys([*merged.get(key, []), *value]))
        elif isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged


def _find_persona_bundle(personas_root: Path, persona_id: str) -> Path:
    for candidate in personas_root.rglob("persona.hocon"):
        candidate_conf = _parse_hocon(candidate)
        if candidate_conf.id == persona_id:
            return candidate.parent
    raise FileNotFoundError(f"Persona bundle with id '{persona_id}' not found under {personas_root}")


def _flatten_paths(payload: dict[str, Any], prefix: str = "") -> set[str]:
    paths: set[str] = set()
    for key, value in payload.items():
        current = f"{prefix}.{key}" if prefix else key
        paths.add(current)
        if isinstance(value, dict):
            paths.update(_flatten_paths(value, current))
    return paths


def _is_path_overlap(candidate_path: str, final_path: str) -> bool:
    if candidate_path == final_path:
        return True
    if candidate_path.startswith(f"{final_path}."):
        return True
    if final_path.startswith(f"{candidate_path}."):
        return True
    return False


def _validate_disallowed_mixins(persona_dict: dict[str, Any]) -> None:
    mixins = persona_dict.get("extends", [])
    if mixins:
        raise ValueError(
            "Mixin inheritance is disabled for personas. Use single-parent `base` inheritance only. "
            f"Found extends={mixins} in persona id='{persona_dict['id']}'."
        )


def _validate_override_allowlist(base_conf: dict[str, Any], child_conf: dict[str, Any]) -> None:
    disallowed_fields: list[str] = []
    for key, value in child_conf.items():
        if key in _RESERVED_FIELDS:
            continue
        if key in base_conf and base_conf[key] != value and key not in ALLOWED_PERSONA_OVERRIDE_FIELDS:
            disallowed_fields.append(key)

    if disallowed_fields:
        raise ValueError(
            "Persona overrides are restricted to an explicit allowlist. "
            f"Disallowed overrides for id='{child_conf['id']}': {sorted(disallowed_fields)}. "
            f"Allowed fields: {sorted(ALLOWED_PERSONA_OVERRIDE_FIELDS)}"
        )


def _validate_final_constraints(base_conf: dict[str, Any], child_conf: dict[str, Any]) -> None:
    final_fields = base_conf.get("final", [])
    if not final_fields:
        return

    child_paths = _flatten_paths({key: value for key, value in child_conf.items() if key not in _RESERVED_FIELDS})
    violating_paths: list[str] = []

    for candidate_path in child_paths:
        for final_path in final_fields:
            if _is_path_overlap(candidate_path, final_path):
                violating_paths.append(candidate_path)

    if violating_paths:
        raise ValueError(
            "Persona attempted to override inherited `final` fields. "
            f"id='{child_conf['id']}', violating_paths={sorted(set(violating_paths))}, "
            f"final_fields={final_fields}"
        )


@dataclass
class PersonaObject:
    persona_id: str
    bundle_root: Path
    resolved_conf: dict[str, Any]
    resolved_body: str
    inheritance_chain: list[str]
    project_conf_hash: str
    audit_git: dict[str, Any]
    execution_identity: dict[str, Any]

    @classmethod
    def from_id(cls, persona_id: str, conf: TypedConfig | None = None) -> "PersonaObject":
        if conf is None:
            conf = get_project_conf()

        personas_root = Path(conf.wielder_antifragile.roots.personas_root)
        bundle_root = _find_persona_bundle(personas_root, persona_id)
        resolved_conf, resolved_body, inheritance_chain = cls._resolve_bundle(bundle_root, personas_root, set())
        return cls(
            persona_id=persona_id,
            bundle_root=bundle_root,
            resolved_conf=resolved_conf,
            resolved_body=resolved_body,
            inheritance_chain=inheritance_chain,
            project_conf_hash=get_global_conf_hash(conf),
            audit_git=_config_to_dict(conf.audit.git),
            execution_identity=_config_to_dict(conf.wielder_antifragile.execution_identity),
        )

    @classmethod
    def _resolve_bundle(
        cls,
        bundle_root: Path,
        personas_root: Path,
        visited_ids: set[str] | None = None,
    ) -> tuple[dict[str, Any], str, list[str]]:
        if visited_ids is None:
            visited_ids = set()

        persona_conf = _parse_hocon(bundle_root / "persona.hocon")
        persona_dict = _config_to_dict(persona_conf)
        persona_id = persona_dict["id"]

        if persona_id in visited_ids:
            raise ValueError(f"Circular persona base inheritance detected for id='{persona_id}'")

        _validate_disallowed_mixins(persona_dict)

        inheritance_chain: list[str] = []
        resolved_conf: dict[str, Any] = {}
        body_parts: list[str] = []

        base_id = persona_dict.get("base")
        if base_id:
            base_root = _find_persona_bundle(personas_root, base_id)
            next_visited = set(visited_ids)
            next_visited.add(persona_id)
            base_conf, base_body, base_chain = cls._resolve_bundle(base_root, personas_root, next_visited)
            _validate_final_constraints(base_conf, persona_dict)
            _validate_override_allowlist(base_conf, persona_dict)
            resolved_conf = _merge_dicts(resolved_conf, base_conf)
            body_parts.append(base_body)
            inheritance_chain.extend(base_chain)

        resolved_conf = _merge_dicts(resolved_conf, persona_dict)

        body_path = bundle_root / persona_dict["prompt_body_file"]
        if not body_path.exists():
            raise FileNotFoundError(f"Persona body not found at {body_path}")
        body_parts.append(body_path.read_text(encoding="utf-8").strip())

        inheritance_chain.append(persona_id)
        resolved_body = "\n\n".join(part for part in body_parts if part)
        return resolved_conf, resolved_body, inheritance_chain

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.persona_id,
            "kind": self.resolved_conf["kind"],
            "bundle_root": self.bundle_root.as_posix(),
            "inheritance_chain": self.inheritance_chain,
            "resolved_conf": self.resolved_conf,
            "resolved_body": self.resolved_body,
            "project_conf_hash": self.project_conf_hash,
            "audit_git": self.audit_git,
            "execution_identity": self.execution_identity,
        }

    def to_string(self) -> str:
        return f"PersonaObject(id={self.persona_id}, chain={self.inheritance_chain})"

    def to_markdown(self) -> str:
        rendered_at = datetime.now(UTC).isoformat()
        override_fields = sorted(
            key for key in self.resolved_conf.keys() if key not in {"base", "extends", "prompt_body_file"}
        )
        final_fields = self.resolved_conf.get("final", [])
        lines = [
            f"# Persona Audit: {self.persona_id}",
            "",
            "## Provenance",
            f"- object_id: `{self.persona_id}`",
            f"- kind: `{self.resolved_conf['kind']}`",
            f"- source_bundle: `{self.bundle_root.as_posix()}`",
            f"- inheritance_chain: `{self.inheritance_chain}`",
            f"- overridden_fields: `{override_fields}`",
            f"- final_fields: `{final_fields}`",
            f"- project_conf_hash: `{self.project_conf_hash}`",
            f"- render_timestamp: `{rendered_at}`",
            f"- repo_commit: `{self.audit_git.get('commit', 'unknown')}`",
            f"- execution_identity.agent_name: `{self.execution_identity['agent_name']}`",
            f"- execution_identity.provider: `{self.execution_identity['provider']}`",
            f"- execution_identity.agent_type: `{self.execution_identity['agent_type']}`",
            f"- execution_identity.agent_version: `{self.execution_identity['agent_version']}`",
            f"- execution_identity.run_id: `{self.execution_identity['run_id']}`",
            "",
            "## Resolved Body",
            self.resolved_body,
            "",
        ]
        return "\n".join(lines)

    def write_audit_bundle(self, conf: TypedConfig | None = None) -> dict[str, Path]:
        if conf is None:
            conf = get_project_conf()

        audit_root = ensure_audit_root(conf)
        rendered_path = audit_root / "rendered_markdown" / "personas" / f"{self.persona_id}_RESOLVED.md"
        resolved_path = audit_root / "resolved" / "personas" / f"{self.persona_id}_RESOLVED.json"
        chain_path = audit_root / "inheritance_chains" / "personas" / f"{self.persona_id}_CHAIN.json"

        rendered_path.parent.mkdir(parents=True, exist_ok=True)
        rendered_path.write_text(self.to_markdown(), encoding="utf-8")
        write_json(resolved_path, self.to_dict())
        write_json(chain_path, {"id": self.persona_id, "inheritance_chain": self.inheritance_chain})

        return {
            "rendered_markdown": rendered_path,
            "resolved_snapshot": resolved_path,
            "inheritance_chain": chain_path,
        }
