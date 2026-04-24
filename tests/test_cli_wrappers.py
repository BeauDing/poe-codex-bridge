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


if __name__ == "__main__":
    unittest.main()
