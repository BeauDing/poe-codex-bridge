from __future__ import annotations

import os
import subprocess
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
    get_runtime_env_path,
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

    def test_get_runtime_env_path_prefers_new_override_then_legacy_override(self) -> None:
        with mock.patch.dict(os.environ, {"POE_REVIEW_ENV_FILE": "/tmp/poe-review.env"}, clear=True):
            self.assertEqual(get_runtime_env_path(), Path("/tmp/poe-review.env"))

        with mock.patch.dict(os.environ, {"CLAUDE_POE_ENV_FILE": "/tmp/claude-poe.env"}, clear=True):
            self.assertEqual(get_runtime_env_path(), Path("/tmp/claude-poe.env"))

    def test_get_runtime_env_path_prefers_new_default_file_and_falls_back_to_legacy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir)
            config_dir = home / ".config"
            config_dir.mkdir()
            preferred = config_dir / "poe-review.env"
            legacy = config_dir / "claude-poe.env"

            with mock.patch.dict(os.environ, {}, clear=True):
                with mock.patch("pathlib.Path.home", return_value=home):
                    self.assertEqual(get_runtime_env_path(), preferred)

    def test_shell_runtime_env_path_matches_python_logic(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir)
            config_dir = home / ".config"
            config_dir.mkdir()
            legacy = config_dir / "claude-poe.env"
            legacy.write_text("POE_API_KEY=legacy\n", encoding="utf-8")

            command = f'''
source "{SCRIPTS_DIR / "runtime_env.sh"}"
claude_poe_get_runtime_env_path
'''
            result = subprocess.run(
                ["bash", "-lc", command],
                check=False,
                capture_output=True,
                text=True,
                env={"HOME": str(home)},
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(result.stdout.strip(), str(legacy))

    def test_shell_runtime_env_defaults_match_python_parser(self) -> None:
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

            command = f'''
source "{SCRIPTS_DIR / "runtime_env.sh"}"
claude_poe_load_runtime_env_defaults "{env_file}"
printf 'POE_API_KEY=%s\\n' "${{POE_API_KEY:-}}"
printf 'POE_API_BASE_URL=%s\\n' "${{POE_API_BASE_URL:-}}"
printf 'CLAUDE_POE_DEFAULT_MODEL=%s\\n' "${{CLAUDE_POE_DEFAULT_MODEL:-}}"
'''
            result = subprocess.run(
                ["bash", "-lc", command],
                check=False,
                capture_output=True,
                text=True,
                env={"HOME": tmpdir},
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(
                result.stdout.splitlines(),
                [
                    "POE_API_KEY=test-key",
                    "POE_API_BASE_URL=https://proxy.example/v1",
                    "CLAUDE_POE_DEFAULT_MODEL=claude-haiku-4-5",
                ],
            )


if __name__ == "__main__":
    unittest.main()
