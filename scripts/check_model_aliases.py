#!/usr/bin/env python3
"""Check whether configured Poe model aliases still resolve to available models."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ModuleNotFoundError:
    print(
        "Missing dependency: `openai`. Run this script with a Python environment that has the OpenAI SDK installed.",
        file=sys.stderr,
    )
    raise


DEFAULT_BASE_URL = "https://api.poe.com/v1"
SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_CONFIG = SKILL_DIR / "config" / "model_aliases.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model-config",
        default=str(DEFAULT_MODEL_CONFIG),
        help="Path to JSON config mapping aliases to exact Poe model ids.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero if any alias target is missing.",
    )
    return parser.parse_args()


def load_aliases(path: str) -> dict[str, str]:
    config_path = Path(path)
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Model alias config must be a JSON object.")
    return {str(k): str(v) for k, v in data.items()}


def main() -> int:
    args = parse_args()
    api_key = os.getenv("POE_API_KEY")
    if not api_key:
        print("POE_API_KEY is not set.", file=sys.stderr)
        return 1

    aliases = load_aliases(args.model_config)
    client = OpenAI(api_key=api_key, base_url=DEFAULT_BASE_URL)
    models = client.models.list()
    available = {item.id for item in models.data}

    missing: list[tuple[str, str]] = []
    print("# Poe Model Alias Check")
    print(f"- config: `{args.model_config}`")
    print(f"- available_models: {len(available)}")
    print("")

    for alias, model in sorted(aliases.items()):
        if model in available:
            print(f"- OK `{alias}` -> `{model}`")
        else:
            print(f"- MISSING `{alias}` -> `{model}`")
            missing.append((alias, model))

    if missing:
        print("")
        print("## Missing Aliases")
        for alias, model in missing:
            print(f"- `{alias}` -> `{model}`")

    if missing and args.strict:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
