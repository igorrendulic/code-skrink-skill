#!/usr/bin/env bash
set -euo pipefail

cleanup_dir=""
src_dir=""

cleanup() {
  if [ -n "$cleanup_dir" ] && [ -d "$cleanup_dir" ]; then
    rm -rf "$cleanup_dir"
  fi
}
trap cleanup EXIT

resolve_local_src_dir() {
  local script_path="${BASH_SOURCE[0]:-}"
  local script_dir

  if [ -z "$script_path" ]; then
    return 1
  fi

  script_dir="$(cd "$(dirname "$script_path")" 2>/dev/null && pwd -P)" || return 1
  if [ -f "$script_dir/SKILL.md" ]; then
    src_dir="$script_dir"
    return 0
  fi

  return 1
}

download_src_dir() {
  local repo="${CODE_SHRINK_REPO:-igorrendulic/code-skrink-skill}"
  local ref="${CODE_SHRINK_REF:-main}"
  local tarball_url="https://codeload.github.com/${repo}/tar.gz/${ref}"
  local entry

  if ! command -v curl >/dev/null 2>&1; then
    echo "Error: curl is required for remote install." >&2
    exit 1
  fi

  cleanup_dir="$(mktemp -d "${TMPDIR:-/tmp}/code-shrink-install.XXXXXX")"
  curl -fsSL "$tarball_url" | tar -xzf - -C "$cleanup_dir"

  for entry in "$cleanup_dir"/*; do
    if [ -d "$entry" ]; then
      src_dir="$entry"
      break
    fi
  done

  if [ -z "$src_dir" ] || [ ! -f "$src_dir/SKILL.md" ]; then
    echo "Error: downloaded archive does not contain a code-shrink skill." >&2
    exit 1
  fi
}

if ! resolve_local_src_dir; then
  download_src_dir
fi

skills_dir="${CODEX_HOME:-"$HOME/.codex"}/skills"
target_dir="$skills_dir/code-shrink"

mkdir -p "$skills_dir"
rm -rf "$target_dir"
mkdir -p "$target_dir"

cp "$src_dir/SKILL.md" "$target_dir/SKILL.md"
cp -R "$src_dir/references" "$target_dir/references"
if [ -d "$src_dir/scripts" ]; then
  cp -R "$src_dir/scripts" "$target_dir/scripts"
fi

echo "Installed code-shrink skill to $target_dir"
