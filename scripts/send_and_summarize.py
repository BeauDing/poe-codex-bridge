#!/usr/bin/env python3
"""Build a Poe review prompt, send it, and extract a compact summary."""

from __future__ import annotations

import argparse
import json
import os
import re
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

from build_review_prompt import build_prompt, read_optional
from runtime_env import get_poe_api_base_url, load_runtime_env


SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_CONFIG = SKILL_DIR / "config" / "model_aliases.json"
EXAMPLE_MODEL_CONFIG = SKILL_DIR / "config" / "model_aliases.example.json"


AUTO_ALIAS_BY_MODE = {
    "rebuttal-review": "balanced",
    "paper-claim-review": "balanced",
    "experiment-critique": "balanced",
    "decision-cross-check": "balanced",
}

AUTO_ALIAS_BY_PRESET = {
    "hardline-methodology": "balanced",
    "concept-validity": "balanced",
    "silver-labels": "balanced",
    "runtime-scope": "balanced",
    "claim-tightening": "balanced",
}


def create_text_response(client: OpenAI, *, model: str, prompt: str, max_output_tokens: int) -> str:
    if hasattr(client, "responses"):
        response = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=max_output_tokens,
        )
        text = response.output_text or ""
        if text.strip():
            return text

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_output_tokens,
    )
    return response.choices[0].message.content or ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        default="auto",
        help="Exact Poe model id. Use `auto` to resolve from alias config.",
    )
    parser.add_argument(
        "--model-alias",
        choices=["deep", "balanced", "balanced_alt", "fast"],
        help="Use a configured alias instead of an explicit model id.",
    )
    parser.add_argument(
        "--model-config",
        default=str(DEFAULT_MODEL_CONFIG),
        help="Path to JSON config mapping aliases to exact Poe model ids.",
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=[
            "rebuttal-review",
            "paper-claim-review",
            "experiment-critique",
            "decision-cross-check",
        ],
        help="Review mode.",
    )
    parser.add_argument(
        "--preset",
        choices=[
            "concept-validity",
            "runtime-scope",
            "silver-labels",
            "hardline-methodology",
            "claim-tightening",
        ],
        help="Optional reviewer-style preset.",
    )
    parser.add_argument("--paper-excerpts", help="Markdown file with relevant paper excerpts.")
    parser.add_argument("--reviewer-comments", help="Markdown file with reviewer comments.")
    parser.add_argument("--current-reply", help="Markdown file with current rebuttal or target text.")
    parser.add_argument("--evidence-notes", help="Markdown file with experiment notes or supporting evidence.")
    parser.add_argument("--focus", help="Short reviewer-specific or task-specific focus block.")
    parser.add_argument("--language", default="Chinese", help="Requested output language.")
    parser.add_argument("--prompt-file", help="Optional path to save the constructed prompt.")
    parser.add_argument("--raw-output-file", help="Optional path to save the full Poe response.")
    parser.add_argument("--summary-file", help="Optional path to save the compact summary.")
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    return parser.parse_args()


def extract_section(text: str, heading: str) -> str | None:
    pattern = rf"(?ms)^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text)
    if not match:
        return None
    return match.group(1).strip()


def extract_first_section(text: str, headings: list[str]) -> str | None:
    for heading in headings:
        block = extract_section(text, heading)
        if block is not None:
            return block
    return None


def first_nonempty_line(block: str | None) -> str | None:
    if not block:
        return None
    for line in block.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def load_model_aliases(path: str) -> dict[str, str]:
    config_path = Path(path)
    if not config_path.exists():
        example_note = ""
        if EXAMPLE_MODEL_CONFIG.exists():
            example_note = f" Copy {EXAMPLE_MODEL_CONFIG} to {config_path} and edit as needed."
        raise FileNotFoundError(f"Model alias config not found: {config_path}.{example_note}")
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Model alias config must be a JSON object.")
    return {str(k): str(v) for k, v in data.items()}


def choose_auto_alias(mode: str, preset: str | None) -> str:
    if preset and preset in AUTO_ALIAS_BY_PRESET:
        return AUTO_ALIAS_BY_PRESET[preset]
    return AUTO_ALIAS_BY_MODE[mode]


def resolve_model(model: str, model_alias: str | None, mode: str, preset: str | None, model_config: str) -> tuple[str, str]:
    if model and model != "auto":
        return model, "explicit model"

    aliases = load_model_aliases(model_config)
    alias = model_alias or choose_auto_alias(mode, preset)
    if alias not in aliases:
        raise KeyError(f"Model alias `{alias}` not found in {model_config}")
    return aliases[alias], f"alias `{alias}`"


def summarize_response(text: str, model: str, mode: str, preset: str | None, model_source: str) -> str:
    overall = first_nonempty_line(
        extract_first_section(
            text,
            [
                "1. Overall Judgment",
                "1. Overall Assessment",
            ],
        )
    )
    risks = extract_first_section(
        text,
        [
            "3. Remaining Risks",
            "3. Most Dangerous Remaining Gaps",
            "3. Highest-Priority Remaining Problems",
            "3. Remaining Weak Spots",
            "3. Remaining Vulnerabilities",
            "2. Main Risks",
        ],
    )
    improvements = extract_first_section(
        text,
        [
            "4. Best Minimal Improvements",
            "4. Best Next Move",
            "4. Best Next Moves",
            "4. Best Minimal Rewrites",
            "3. Best Minimal Fix",
        ],
    )
    edits = extract_first_section(
        text,
        [
            "5. Direct Rebuttal Edits",
            "4. Best Minimal Rewrites",
            "4. Direct Rewrite or Recommendation",
        ],
    )
    final_meta = extract_first_section(
        text,
        [
            "6. Final Meta-Judgment",
            "6. Final Reviewer Simulation",
        ],
    )

    parts = [
        f"# Poe Review Summary",
        f"- model: `{model}`",
        f"- model_source: {model_source}",
        f"- mode: `{mode}`",
        f"- preset: `{preset or 'none'}`",
    ]
    if overall:
        parts.extend(["", "## Verdict", overall])
    if risks:
        parts.extend(["", "## Top Risks", risks])
    if improvements:
        parts.extend(["", "## Best Next Moves", improvements])
    if edits:
        parts.extend(["", "## Direct Edits", edits])
    if final_meta:
        parts.extend(["", "## Final Meta-Judgment", final_meta])
    return "\n".join(parts).strip() + "\n"


def main() -> int:
    args = parse_args()
    env_path = load_runtime_env()
    api_key = os.getenv("POE_API_KEY")
    if not api_key:
        print("POE_API_KEY is not set.", file=sys.stderr)
        if env_path is not None:
            print(f"Checked runtime env file: {env_path}", file=sys.stderr)
        return 1

    prompt = build_prompt(
        mode=args.mode,
        language=args.language,
        paper_excerpts=read_optional(args.paper_excerpts),
        reviewer_comments=read_optional(args.reviewer_comments),
        current_reply=read_optional(args.current_reply),
        evidence_notes=read_optional(args.evidence_notes),
        preset=args.preset,
        focus=args.focus,
    )

    try:
        resolved_model, model_source = resolve_model(
            args.model,
            args.model_alias,
            args.mode,
            args.preset,
            args.model_config,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.prompt_file:
        Path(args.prompt_file).write_text(prompt, encoding="utf-8")

    client = OpenAI(api_key=api_key, base_url=get_poe_api_base_url())
    text = create_text_response(
        client,
        model=resolved_model,
        prompt=prompt,
        max_output_tokens=args.max_output_tokens,
    )
    if not text.strip():
        print("Poe returned an empty response.", file=sys.stderr)
        return 1

    if args.raw_output_file:
        Path(args.raw_output_file).write_text(text, encoding="utf-8")

    summary = summarize_response(text, resolved_model, args.mode, args.preset, model_source)
    if args.summary_file:
        Path(args.summary_file).write_text(summary, encoding="utf-8")
    else:
        print(summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
