from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from runtime_env import (  # noqa: E402
    DEFAULT_POE_API_BASE_URL,
    get_poe_api_base_url,
    load_runtime_env,
    parse_env_file,
)


class RuntimeEnvTests(unittest.TestCase):
    def test_parse_env_file_supports_basic_and_quoted_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / "test.env"
            env_file.write_text(
                "\n".join(
                    [
                        "# comment",
                        "POE_API_KEY=test-key",
                        'POE_API_BASE_URL="https://proxy.example/v1"',
                        "export CLAUDE_POE_DEFAULT_MODEL=claude-haiku-4-5",
                    ]
                ),
                encoding="utf-8",
            )

            values = parse_env_file(env_file)

        self.assertEqual(values["POE_API_KEY"], "test-key")
        self.assertEqual(values["POE_API_BASE_URL"], "https://proxy.example/v1")
        self.assertEqual(values["CLAUDE_POE_DEFAULT_MODEL"], "claude-haiku-4-5")

    def test_load_runtime_env_preserves_existing_environment_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / "test.env"
            env_file.write_text(
                "\n".join(
                    [
                        "POE_API_KEY=file-key",
                        "POE_API_BASE_URL=https://file.example/v1",
                    ]
                ),
                encoding="utf-8",
            )

            with mock.patch.dict(
                os.environ,
                {
                    "CLAUDE_POE_ENV_FILE": str(env_file),
                    "POE_API_KEY": "shell-key",
                },
                clear=False,
            ):
                load_runtime_env()
                self.assertEqual(os.environ["POE_API_KEY"], "shell-key")
                self.assertEqual(os.environ["POE_API_BASE_URL"], "https://file.example/v1")

    def test_get_poe_api_base_url_uses_env_override(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_poe_api_base_url(), DEFAULT_POE_API_BASE_URL)

        with mock.patch.dict(os.environ, {"POE_API_BASE_URL": "https://override.example/v1"}, clear=True):
            self.assertEqual(get_poe_api_base_url(), "https://override.example/v1")


if __name__ == "__main__":
    unittest.main()

