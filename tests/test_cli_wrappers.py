from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class CliWrapperTests(unittest.TestCase):
    def test_poe_review_delegates_to_poe_external_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fake_repo = tmp / "repo"
            fake_repo.mkdir()
            fake_bin_dir = fake_repo / "bin"
            fake_bin_dir.mkdir()
            captured_args = tmp / "captured-args.txt"

            (fake_bin_dir / "poe-external-review").write_text(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env bash
                    printf '%s\n' "$@" > "{captured_args}"
                    exit 0
                    """
                ),
                encoding="utf-8",
            )
            (fake_bin_dir / "poe-review").write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env bash
                    set -euo pipefail

                    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
                    delegate="$script_dir/poe-external-review"

                    if [[ ! -x "$delegate" ]]; then
                      echo "poe-review: poe-external-review is not installed or not executable." >&2
                      exit 127
                    fi

                    exec "$delegate" "$@"
                    """
                ),
                encoding="utf-8",
            )
            os.chmod(fake_bin_dir / "poe-external-review", 0o755)
            os.chmod(fake_bin_dir / "poe-review", 0o755)

            result = subprocess.run(
                [str(fake_bin_dir / "poe-review"), "--mode", "decision-cross-check", "--help"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(
                captured_args.read_text(encoding="utf-8").splitlines(),
                ["--mode", "decision-cross-check", "--help"],
            )

    def test_claude_poe_uses_new_default_env_filename_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fake_bin = tmp / "bin"
            fake_bin.mkdir()
            output_file = tmp / "poe-code-args.txt"

            (fake_bin / "claude").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            (fake_bin / "poe-code").write_text(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env bash
                    printf '%s\n' "$@" > "{output_file}"
                    exit 0
                    """
                ),
                encoding="utf-8",
            )
            os.chmod(fake_bin / "claude", 0o755)
            os.chmod(fake_bin / "poe-code", 0o755)

            config_dir = tmp / ".config"
            config_dir.mkdir()
            env_file = config_dir / "poe-review.env"
            env_file.write_text(
                "\n".join(
                    [
                        "POE_API_KEY=test-key",
                        "CLAUDE_POE_DEFAULT_MODEL=claude-haiku-4-5",
                    ]
                ),
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["HOME"] = str(tmp)
            env["PATH"] = f"{fake_bin}:{env['PATH']}"

            result = subprocess.run(
                [str(REPO_ROOT / "bin" / "claude-poe"), "-p", "hello"],
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            captured_args = output_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(captured_args[:4], ["wrap", "claude", "--", "--model"])
            self.assertEqual(captured_args[4], "claude-haiku-4-5")

    def test_claude_poe_uses_default_model_from_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fake_bin = tmp / "bin"
            fake_bin.mkdir()
            output_file = tmp / "poe-code-args.txt"

            (fake_bin / "claude").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            (fake_bin / "poe-code").write_text(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env bash
                    printf '%s\n' "$@" > "{output_file}"
                    exit 0
                    """
                ),
                encoding="utf-8",
            )
            os.chmod(fake_bin / "claude", 0o755)
            os.chmod(fake_bin / "poe-code", 0o755)

            config_dir = tmp / ".config"
            config_dir.mkdir()
            env_file = config_dir / "claude-poe.env"
            env_file.write_text(
                "\n".join(
                    [
                        "POE_API_KEY=test-key",
                        "CLAUDE_POE_DEFAULT_MODEL=claude-haiku-4-5",
                    ]
                ),
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["HOME"] = str(tmp)
            env["PATH"] = f"{fake_bin}:{env['PATH']}"

            result = subprocess.run(
                [str(REPO_ROOT / "bin" / "claude-poe"), "-p", "hello"],
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            captured_args = output_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(captured_args[:4], ["wrap", "claude", "--", "--model"])
            self.assertEqual(captured_args[4], "claude-haiku-4-5")

    def test_claude_poe_preserves_exported_env_over_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fake_bin = tmp / "bin"
            fake_bin.mkdir()
            output_file = tmp / "poe-code-args.txt"

            (fake_bin / "claude").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            (fake_bin / "poe-code").write_text(
                textwrap.dedent(
                    f"""\
                    #!/usr/bin/env bash
                    {{
                      printf 'POE_API_KEY=%s\\n' "${{POE_API_KEY:-}}"
                      printf 'POE_API_BASE_URL=%s\\n' "${{POE_API_BASE_URL:-}}"
                      printf '%s\\n' "$@"
                    }} > "{output_file}"
                    exit 0
                    """
                ),
                encoding="utf-8",
            )
            os.chmod(fake_bin / "claude", 0o755)
            os.chmod(fake_bin / "poe-code", 0o755)

            config_dir = tmp / ".config"
            config_dir.mkdir()
            env_file = config_dir / "claude-poe.env"
            env_file.write_text(
                "\n".join(
                    [
                        "POE_API_KEY=file-key",
                        "POE_API_BASE_URL=https://file.example/v1",
                        "CLAUDE_POE_DEFAULT_MODEL=file-model",
                    ]
                ),
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["HOME"] = str(tmp)
            env["PATH"] = f"{fake_bin}:{env['PATH']}"
            env["POE_API_KEY"] = "shell-key"
            env["POE_API_BASE_URL"] = "https://shell.example/v1"
            env["CLAUDE_POE_DEFAULT_MODEL"] = "shell-model"

            result = subprocess.run(
                [str(REPO_ROOT / "bin" / "claude-poe"), "-p", "hello"],
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            captured_lines = output_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(captured_lines[0], "POE_API_KEY=shell-key")
            self.assertEqual(captured_lines[1], "POE_API_BASE_URL=https://shell.example/v1")
            self.assertEqual(captured_lines[2:6], ["wrap", "claude", "--", "--model"])
            self.assertEqual(captured_lines[6], "shell-model")

    def test_claude_poe_models_does_not_require_credentials(self) -> None:
        result = subprocess.run(
            [str(REPO_ROOT / "bin" / "claude-poe"), "models"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("claude-sonnet-4-6", result.stdout)

    def test_claude_poe_wrapper_help_uses_safe_default_resolution(self) -> None:
        result = subprocess.run(
            [str(REPO_ROOT / "bin" / "claude-poe"), "--wrapper-help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Known-good model names for this wrapper", result.stdout)
        self.assertIn("known-good names, not Poe's live catalog", result.stdout)


if __name__ == "__main__":
    unittest.main()
