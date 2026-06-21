#!/usr/bin/env python3
"""Small stdlib validator for Codex skill folders."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

BANNED_PATTERNS = [
    "Sergey",
    "Сергей",
    "/Users/",
    "pimenov",
    "Pimenov",
    "Bipolyar",
    "Биполяр",
    "WorkOps",
    "Keychain service codex-",
]

NAME_RE = re.compile(r"^[a-z0-9-]+$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
      raise ValueError("missing opening frontmatter fence")
    end = text.find("\n---\n", 4)
    if end == -1:
      raise ValueError("missing closing frontmatter fence")
    block = text[4:end]
    result: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def main() -> int:
    if not SKILLS.is_dir():
        print(f"Missing skills directory: {SKILLS}", file=sys.stderr)
        return 1

    errors: list[str] = []
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("No skill directories found.")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        text = skill_file.read_text(encoding="utf-8")
        try:
            meta = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(f"{skill_dir.name}: {exc}")
            continue

        name = meta.get("name")
        description = meta.get("description")
        if not name:
            errors.append(f"{skill_dir.name}: missing name")
        elif name != skill_dir.name:
            errors.append(f"{skill_dir.name}: frontmatter name is {name!r}")
        elif not NAME_RE.match(name):
            errors.append(f"{skill_dir.name}: invalid skill name")

        if not description:
            errors.append(f"{skill_dir.name}: missing description")
        elif len(description) < 80:
            errors.append(f"{skill_dir.name}: description looks too short")

        for pattern in BANNED_PATTERNS:
            if pattern in text:
                errors.append(f"{skill_dir.name}: banned private pattern {pattern!r}")

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
