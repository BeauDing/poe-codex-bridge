#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config_dir="${HOME}/.config"
config_file="${config_dir}/poe-review.env"
legacy_config_file="${config_dir}/claude-poe.env"
install_advanced_bridge=0
skip_python_deps=0

usage() {
  cat <<'EOF'
install.sh: lightweight setup helper for poe-codex-bridge.

Usage:
  ./scripts/install.sh
  ./scripts/install.sh --advanced-claude-bridge
  ./scripts/install.sh --skip-python-deps
  ./scripts/install.sh --help

Behavior:
  - marks the default packaged-review entrypoints executable
  - optionally marks the advanced Claude bridge wrappers executable
  - installs Python dependencies unless --skip-python-deps is used
  - creates ~/.config/poe-review.env from the example if neither the new nor legacy config exists
  - prints the PATH line to add manually
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --advanced-claude-bridge)
      install_advanced_bridge=1
      shift
      ;;
    --skip-python-deps)
      skip_python_deps=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "install.sh: unknown option '$1'." >&2
      usage >&2
      exit 2
      ;;
  esac
done

chmod +x "$repo_root/bin/poe-review" "$repo_root/bin/poe-external-review"

if [[ $install_advanced_bridge -eq 1 ]]; then
  chmod +x "$repo_root/bin/claude-poe" "$repo_root/bin/claude-poe-review"
fi

if [[ $skip_python_deps -eq 0 ]]; then
  if ! command -v python3 >/dev/null 2>&1; then
    echo "install.sh: python3 is required to install packaged-review dependencies." >&2
    exit 127
  fi
  if ! python3 -m pip --version >/dev/null 2>&1; then
    echo "install.sh: python3 is available, but pip is not working in that environment." >&2
    exit 127
  fi
  python3 -m pip install -r "$repo_root/requirements.txt"
fi

mkdir -p "$config_dir"
if [[ ! -f "$config_file" && ! -f "$legacy_config_file" ]]; then
  cp "$repo_root/config/poe-review.env.example" "$config_file"
fi

cat <<EOF
Setup complete.

Preferred config file:
  $config_file

You can run the packaged-review entrypoint immediately with:
  $repo_root/bin/poe-review --help

Add this to your shell profile if needed:
  export PATH="$repo_root/bin:\$PATH"
EOF
