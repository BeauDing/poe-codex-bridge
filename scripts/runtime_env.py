#!/usr/bin/env python3
"""Shared runtime environment loading for Poe Codex Bridge helpers."""

from __future__ import annotations

import os
from pathlib import Path


DEFAULT_POE_API_BASE_URL = "https://api.poe.com/v1"


def get_runtime_env_path() -> Path:
    override = os.environ.get("CLAUDE_POE_ENV_FILE")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".config" / "claude-poe.env"


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        cleaned = value.strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
            cleaned = cleaned[1:-1]
        values[key] = cleaned
    return values


def load_runtime_env() -> Path | None:
    env_path = get_runtime_env_path()
    if not env_path.exists():
        return None

    for key, value in parse_env_file(env_path).items():
        os.environ.setdefault(key, value)
    return env_path


def get_poe_api_base_url() -> str:
    return os.environ.get("POE_API_BASE_URL", DEFAULT_POE_API_BASE_URL)
