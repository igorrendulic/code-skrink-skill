#!/usr/bin/env bash
set -euo pipefail

src_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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
