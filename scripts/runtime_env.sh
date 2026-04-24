#!/usr/bin/env bash

poe_review_get_runtime_env_path() {
  if [[ -n "${POE_REVIEW_ENV_FILE:-}" ]]; then
    printf '%s\n' "$POE_REVIEW_ENV_FILE"
    return 0
  fi

  printf '%s\n' "${HOME}/.config/poe-review.env"
}

poe_review_trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

poe_review_load_runtime_env_defaults() {
  local config_file="$1"
  local raw_line=""
  local line=""
  local key=""
  local cleaned=""
  local first_char=""
  local last_char=""

  [[ -f "$config_file" ]] || return 0

  while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    line="$(poe_review_trim "$raw_line")"
    [[ -z "$line" || "${line:0:1}" == "#" ]] && continue

    if [[ "$line" == export[[:space:]]* ]]; then
      line="${line#export }"
      line="$(poe_review_trim "$line")"
    fi

    [[ "$line" == *=* ]] || continue

    key="$(poe_review_trim "${line%%=*}")"
    [[ -n "$key" && "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue

    if [[ -n "${!key+x}" ]]; then
      continue
    fi

    cleaned="$(poe_review_trim "${line#*=}")"
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
