from __future__ import annotations

import pytest
from pyhocon import ConfigFactory

from wielder_antifragile.core.utils import validate_execution_identity


def _conf_with_identity(identity: dict[str, str]):
    return ConfigFactory.from_dict({"wielder_antifragile": {"execution_identity": identity}})


def test_validate_execution_identity_passes_for_valid_payload() -> None:
    conf = _conf_with_identity(
        {
            "user_name": "operator",
            "provider": "openai",
            "agent_type": "codex-cli",
            "agent_instance_id": "1",
            "agent_name": "openai_codex-cli_1",
            "agent_version": "gpt-5.4",
            "session_id": "session_1",
            "run_id": "run_1",
            "invoked_at_utc": "2026-03-25T00:00:00Z",
        }
    )
    validate_execution_identity(conf)


def test_validate_execution_identity_fails_when_name_mismatch() -> None:
    conf = _conf_with_identity(
        {
            "user_name": "operator",
            "provider": "openai",
            "agent_type": "codex-cli",
            "agent_instance_id": "1",
            "agent_name": "wrong_name",
            "agent_version": "gpt-5.4",
            "session_id": "session_1",
            "run_id": "run_1",
            "invoked_at_utc": "2026-03-25T00:00:00Z",
        }
    )
    with pytest.raises(ValueError, match="agent_name must be"):
        validate_execution_identity(conf)


def test_validate_execution_identity_fails_for_unsupported_chars() -> None:
    conf = _conf_with_identity(
        {
            "user_name": "operator",
            "provider": "open ai",
            "agent_type": "codex-cli",
            "agent_instance_id": "1",
            "agent_name": "open ai_codex-cli_1",
            "agent_version": "gpt-5.4",
            "session_id": "session_1",
            "run_id": "run_1",
            "invoked_at_utc": "2026-03-25T00:00:00Z",
        }
    )
    with pytest.raises(ValueError, match="provider contains unsupported characters"):
        validate_execution_identity(conf)


def test_validate_execution_identity_fails_for_missing_field() -> None:
    conf = _conf_with_identity(
        {
            "user_name": "operator",
            "provider": "openai",
            "agent_type": "codex-cli",
            "agent_instance_id": "1",
            "agent_name": "openai_codex-cli_1",
            "agent_version": "",
            "session_id": "session_1",
            "run_id": "run_1",
            "invoked_at_utc": "2026-03-25T00:00:00Z",
        }
    )
    with pytest.raises(ValueError, match="Missing required execution_identity fields"):
        validate_execution_identity(conf)
