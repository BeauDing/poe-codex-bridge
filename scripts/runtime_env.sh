#!/usr/bin/env bash

claude_poe_get_runtime_env_path() {
  local preferred=""
  local legacy=""

  if [[ -n "${POE_REVIEW_ENV_FILE:-}" ]]; then
    printf '%s\n' "$POE_REVIEW_ENV_FILE"
    return 0
  fi

  if [[ -n "${CLAUDE_POE_ENV_FILE:-}" ]]; then
    printf '%s\n' "$CLAUDE_POE_ENV_FILE"
    return 0
  fi

  preferred="${HOME}/.config/poe-review.env"
  legacy="${HOME}/.config/claude-poe.env"

  if [[ -f "$preferred" ]]; then
    printf '%s\n' "$preferred"
  elif [[ -f "$legacy" ]]; then
    printf '%s\n' "$legacy"
  else
    printf '%s\n' "$preferred"
  fi
}

claude_poe_trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

claude_poe_load_runtime_env_defaults() {
  local config_file="$1"
  local raw_line=""
  local line=""
  local key=""
  local cleaned=""
  local first_char=""
  local last_char=""

  [[ -f "$config_file" ]] || return 0

  while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    line="$(claude_poe_trim "$raw_line")"
    [[ -z "$line" || "${line:0:1}" == "#" ]] && continue

    if [[ "$line" == export[[:space:]]* ]]; then
      line="${line#export }"
      line="$(claude_poe_trim "$line")"
    fi

    [[ "$line" == *=* ]] || continue

    key="$(claude_poe_trim "${line%%=*}")"
    [[ -n "$key" && "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue

    if [[ -n "${!key+x}" ]]; then
      continue
    fi

    cleaned="$(claude_poe_trim "${line#*=}")"
    if [[ ${#cleaned} -ge 2 ]]; then
      first_char="${cleaned:0:1}"
      last_char="${cleaned: -1}"
      if [[ "$first_char" == "$last_char" && ( "$first_char" == "'" || "$first_char" == '"' ) ]]; then
        cleaned="${cleaned:1:${#cleaned}-2}"
      fi
    fi

    printf -v "$key" '%s' "$cleaned"
    export "$key"
  done < "$config_file"
}
