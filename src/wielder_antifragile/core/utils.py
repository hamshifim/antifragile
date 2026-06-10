"""Strict configuration and audit helpers for wielder-antifragile."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from pyhocon import ConfigFactory

from wielder.util.wgit import WGit, is_repo
from wielder.wield.wield_conf import get_wield_project_conf

TypedConfig = Any


def _resolve_conf_root() -> Path:
    """Resolve the configuration root relative to this package or cwd."""
    try:
        lib_root = Path(__file__).resolve().parents[3]
        conf_root = lib_root / "conf"
        if conf_root.exists():
            return conf_root
    except IndexError:
        pass

    cwd_conf = Path.cwd() / "conf"
    if cwd_conf.exists():
        return cwd_conf

    raise FileNotFoundError("Configuration root 'wielder-antifragile/conf' not found.")


def _resolve_repo_root(project_root: Path) -> Path:
    """Resolve the nearest enclosing git repository for audit-only WGit telemetry."""
    current = project_root.resolve()
    for candidate in [current, *current.parents]:
        if is_repo(candidate.as_posix()):
            return candidate
    raise FileNotFoundError(f"No enclosing git repository found for {project_root}")


def _get_repo_audit(project_root: Path) -> dict[str, Any]:
    """Collect read-only repository telemetry using WGit."""
    repo_root = _resolve_repo_root(project_root)
    wg = WGit(repo_root.as_posix())
    return {
        "repo_root": repo_root.as_posix(),
        "git": wg.as_dict_injection()["git"],
    }


def validate_execution_identity(conf: TypedConfig) -> None:
    identity = conf.wielder_antifragile.execution_identity

    required_fields = [
        "user_name",
        "provider",
        "agent_type",
        "agent_instance_id",
        "agent_name",
        "agent_version",
        "session_id",
        "run_id",
        "invoked_at_utc",
    ]
    missing_or_empty: list[str] = []
    for field in required_fields:
        value = identity[field]
        if not str(value).strip():
            missing_or_empty.append(field)

    if missing_or_empty:
        raise ValueError(f"Missing required execution_identity fields: {missing_or_empty}")

    expected_agent_name = (
        f"{identity.provider}_{identity.agent_type}_{identity.agent_instance_id}"
    )
    if identity.agent_name != expected_agent_name:
        raise ValueError(
            "execution_identity.agent_name must be <provider>_<agent_type>_<agent_instance_id>. "
            f"Expected '{expected_agent_name}', got '{identity.agent_name}'."
        )

    if not re.match(r"^[A-Za-z0-9_.-]+$", str(identity.provider)):
        raise ValueError("execution_identity.provider contains unsupported characters.")
    if not re.match(r"^[A-Za-z0-9_.-]+$", str(identity.agent_type)):
        raise ValueError("execution_identity.agent_type contains unsupported characters.")
    if not re.match(r"^[A-Za-z0-9_.-]+$", str(identity.agent_instance_id)):
        raise ValueError("execution_identity.agent_instance_id contains unsupported characters.")


def get_project_conf(conf_root: Path | None = None) -> TypedConfig:
    """Load the wielder-antifragile project config through Wielder's strict loader."""
    if conf_root is None:
        conf_root = _resolve_conf_root()

    project_root = conf_root.parent
    project_conf = get_wield_project_conf(
        project_root=project_root.as_posix(),
        conf_root=conf_root.as_posix(),
        project_name="wielder-antifragile",
    )
    project_conf.put("audit", ConfigFactory.from_dict(_get_repo_audit(project_root)))
    validate_execution_identity(project_conf)
    return project_conf


# Backward-compatible alias for older call sites.
_validate_execution_identity = validate_execution_identity


def get_global_conf_hash(conf: TypedConfig) -> str:
    """Calculate a stable short hash for the resolved configuration tree."""
    conf_string = str(conf)
    return hashlib.sha256(conf_string.encode("utf-8")).hexdigest()[:12]


def ensure_audit_root(conf: TypedConfig) -> Path:
    """Ensure the audit root exists and return it as a Path."""
    audit_root = Path(conf.wielder_antifragile.roots.audit_root)
    audit_root.mkdir(parents=True, exist_ok=True)
    return audit_root


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write a deterministic JSON artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
