from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import build_review_prompt as review_prompt  # noqa: E402


fake_openai = types.ModuleType("openai")


class _FakeOpenAI:  # pragma: no cover - helper for import only
    pass


fake_openai.OpenAI = _FakeOpenAI
sys.modules.setdefault("openai", fake_openai)

spec = importlib.util.spec_from_file_location(
    "send_and_summarize",
    SCRIPTS_DIR / "send_and_summarize.py",
)
assert spec is not None and spec.loader is not None
send_and_summarize = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_and_summarize)


class BuildReviewPromptTests(unittest.TestCase):
    def test_each_mode_includes_required_headings(self) -> None:
        for mode, mode_info in review_prompt.MODE_INSTRUCTIONS.items():
            prompt = review_prompt.build_prompt(
                mode=mode,
                language="Chinese",
                paper_excerpts="Paper block",
                reviewer_comments="Review block",
                current_reply="Reply block",
                evidence_notes="Evidence block",
                preset="claim-tightening" if mode == "paper-claim-review" else None,
                focus="Extra focus",
            )

            self.assertIn("## Important Rules", prompt)
            self.assertIn("## Required Output Format", prompt)
            self.assertIn("## Focus", prompt)
            self.assertIn("## Paper Excerpts", prompt)
            self.assertIn("## Reviewer Comments", prompt)
            self.assertIn("## Current Reply or Target Text", prompt)
            self.assertIn("## Evidence Notes", prompt)
            for line in mode_info["structure"]:
                if line.startswith("## "):
                    self.assertIn(line, prompt)


class ResolveModelTests(unittest.TestCase):
    def test_resolve_model_returns_explicit_model_without_alias_lookup(self) -> None:
        model, source = send_and_summarize.resolve_model(
            "gemini-3.1-pro",
            None,
            "decision-cross-check",
            None,
            "unused.json",
        )

        self.assertEqual(model, "gemini-3.1-pro")
        self.assertEqual(source, "explicit model")

    def test_resolve_model_uses_auto_alias_for_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "model_aliases.json"
            config_path.write_text(
                json.dumps(
                    {
                        "balanced": "gemini-3.1-pro",
                        "balanced_alt": "gemini-3-flash",
                    }
                ),
                encoding="utf-8",
            )

            model, source = send_and_summarize.resolve_model(
                "auto",
                None,
                "experiment-critique",
                None,
                str(config_path),
            )

        self.assertEqual(model, "gemini-3.1-pro")
        self.assertEqual(source, "alias `balanced`")

    def test_resolve_model_errors_when_alias_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "model_aliases.json"
            config_path.write_text(json.dumps({"fast": "gemini-3-flash"}), encoding="utf-8")

            with self.assertRaises(KeyError):
                send_and_summarize.resolve_model(
                    "auto",
                    None,
                    "rebuttal-review",
                    None,
                    str(config_path),
                )


class SummarizeResponseTests(unittest.TestCase):
    def test_summarize_response_extracts_expected_sections(self) -> None:
        response_text = """\
## 1. Overall Assessment
证据基本够用

## 3. Remaining Vulnerabilities
- Reviewer may still question the baseline choice.

## 4. Best Next Move
- 更清楚引用已有结果。

## 6. Final Reviewer Simulation
大体可以接受，但需要更明确地收紧表述。
"""

        summary = send_and_summarize.summarize_response(
            response_text,
            "gemini-3.1-pro",
            "experiment-critique",
            None,
            "explicit model",
        )

        self.assertIn("# Poe Review Summary", summary)
        self.assertIn("- model: `gemini-3.1-pro`", summary)
        self.assertIn("## Verdict", summary)
        self.assertIn("证据基本够用", summary)
        self.assertIn("## Top Risks", summary)
        self.assertIn("baseline choice", summary)
        self.assertIn("## Best Next Moves", summary)
        self.assertIn("更清楚引用已有结果", summary)
        self.assertIn("## Final Meta-Judgment", summary)


class CreateTextResponseTests(unittest.TestCase):
    def test_create_text_response_falls_back_when_responses_output_text_is_blank(self) -> None:
        class _FakeResponses:
            def create(self, **_: object) -> object:
                return types.SimpleNamespace(output_text="")

        class _FakeChatCompletions:
            def create(self, **_: object) -> object:
                return types.SimpleNamespace(
                    choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="pong"))]
                )

        fake_client = types.SimpleNamespace(
            responses=_FakeResponses(),
            chat=types.SimpleNamespace(completions=_FakeChatCompletions()),
        )

        text = send_and_summarize.create_text_response(
            fake_client,
            model="gemini-3-flash",
            prompt="Reply with exactly: pong",
            max_output_tokens=50,
        )

        self.assertEqual(text, "pong")


if __name__ == "__main__":
    unittest.main()
