from __future__ import annotations

from pathlib import Path

import pytest

from wielder_antifragile.personas.object import PersonaObject


def _write_bundle(
    personas_root: Path,
    subpath: str,
    persona_hocon: str,
    body_markdown: str = "## Body\ncontent",
) -> Path:
    bundle = personas_root / subpath
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "persona.hocon").write_text(persona_hocon.strip() + "\n", encoding="utf-8")
    (bundle / "body.md").write_text(body_markdown.strip() + "\n", encoding="utf-8")
    return bundle


def test_extends_is_rejected(tmp_path: Path) -> None:
    personas_root = tmp_path / "personas"
    _write_bundle(
        personas_root,
        "core",
        """
        id = "core"
        kind = "persona"
        prompt_body_file = "body.md"
        extends = []
        """,
    )
    child_bundle = _write_bundle(
        personas_root,
        "child",
        """
        id = "child"
        kind = "persona"
        base = "core"
        extends = ["mixin_a"]
        prompt_body_file = "body.md"
        """,
    )

    with pytest.raises(ValueError, match="Mixin inheritance is disabled"):
        PersonaObject._resolve_bundle(child_bundle, personas_root)


def test_disallowed_override_field_fails(tmp_path: Path) -> None:
    personas_root = tmp_path / "personas"
    _write_bundle(
        personas_root,
        "core",
        """
        id = "core"
        kind = "persona"
        prompt_body_file = "body.md"
        extends = []
        mission = "stable"
        """,
    )
    child_bundle = _write_bundle(
        personas_root,
        "child",
        """
        id = "child"
        kind = "persona"
        base = "core"
        extends = []
        prompt_body_file = "body.md"
        mission = "mutated"
        """,
    )

    with pytest.raises(ValueError, match="Disallowed overrides"):
        PersonaObject._resolve_bundle(child_bundle, personas_root)


def test_inherited_final_field_cannot_be_overridden(tmp_path: Path) -> None:
    personas_root = tmp_path / "personas"
    _write_bundle(
        personas_root,
        "core",
        """
        id = "core"
        kind = "persona"
        prompt_body_file = "body.md"
        extends = []
        safety = { no_destructive_git = true }
        final = ["safety.no_destructive_git"]
        """,
    )
    child_bundle = _write_bundle(
        personas_root,
        "child",
        """
        id = "child"
        kind = "persona"
        base = "core"
        extends = []
        prompt_body_file = "body.md"
        safety = { no_destructive_git = false }
        """,
    )

    with pytest.raises(ValueError, match="override inherited `final` fields"):
        PersonaObject._resolve_bundle(child_bundle, personas_root)


def test_single_base_inheritance_resolves_cleanly(tmp_path: Path) -> None:
    personas_root = tmp_path / "personas"
    _write_bundle(
        personas_root,
        "core",
        """
        id = "core"
        kind = "persona"
        prompt_body_file = "body.md"
        extends = []
        tools = []
        final = ["safety.no_destructive_git"]
        """,
        body_markdown="## Core Body\ncore",
    )
    child_bundle = _write_bundle(
        personas_root,
        "child",
        """
        id = "child"
        kind = "persona"
        base = "core"
        extends = []
        prompt_body_file = "body.md"
        tools = ["git"]
        outputs = { change_summary = true }
        """,
        body_markdown="## Child Body\nchild",
    )

    resolved_conf, resolved_body, chain = PersonaObject._resolve_bundle(child_bundle, personas_root)
    assert chain == ["core", "child"]
    assert resolved_conf["tools"] == ["git"]
    assert resolved_conf["outputs"]["change_summary"] is True
    assert "## Core Body" in resolved_body
    assert "## Child Body" in resolved_body
