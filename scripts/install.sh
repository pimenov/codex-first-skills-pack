#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${CODEX_HOME:-$HOME/.codex}/skills"
dry_run=0
skill_filter=""

usage() {
  cat <<'USAGE'
Usage: scripts/install.sh [--dry-run] [--target DIR] [--skill NAME]

Copies skills from this repository into ${CODEX_HOME:-$HOME/.codex}/skills.

Options:
  --dry-run      Show what would be copied.
  --target DIR   Install into a custom skills directory.
  --skill NAME   Install only one skill.
  -h, --help     Show this help.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --target)
      target="${2:?Missing target directory}"
      shift 2
      ;;
    --skill)
      skill_filter="${2:?Missing skill name}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ ! -d "$repo_root/skills" ]; then
  echo "Missing skills directory: $repo_root/skills" >&2
  exit 1
fi

mkdir -p "$target"

for skill_dir in "$repo_root"/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"

  if [ -n "$skill_filter" ] && [ "$skill_name" != "$skill_filter" ]; then
    continue
  fi

  if [ ! -f "$skill_dir/SKILL.md" ]; then
    echo "Skipping $skill_name: missing SKILL.md" >&2
    continue
  fi

  dest="$target/$skill_name"
  if [ "$dry_run" -eq 1 ]; then
    echo "Would install $skill_name -> $dest"
    continue
  fi

  if [ -e "$dest" ]; then
    backup="$dest.backup-$(date +%Y%m%dT%H%M%S)"
    mv "$dest" "$backup"
    echo "Backed up existing $skill_name to $backup"
  fi

  mkdir -p "$dest"
  cp -R "$skill_dir/." "$dest/"
  echo "Installed $skill_name -> $dest"
done

if [ -n "$skill_filter" ] && [ ! -d "$repo_root/skills/$skill_filter" ]; then
  echo "Skill not found: $skill_filter" >&2
  exit 1
fi
