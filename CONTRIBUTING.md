# Contributing

Contributions should keep the pack small, public-safe, and useful in real
engineering work.

## Adding A Skill

1. Create `skills/<skill-name>/SKILL.md`.
2. Use lowercase hyphen-case for the folder and frontmatter `name`.
3. Write a frontmatter `description` that clearly says when Codex should use
   the skill.
4. Keep the body procedural:
   - overview;
   - workflow;
   - stop-lines;
   - common rationalizations or anti-patterns;
   - verification.
5. Add the skill to the table in `README.md`.
6. Add a routing line to `templates/AGENTS.skills-routing.md`.
7. Run:

```bash
python3 scripts/validate_skills.py
scripts/install.sh --dry-run
```

## Public-Safety Checklist

Before opening a pull request or publishing a release, check that the change
does not include:

- personal names as behavioral rules;
- absolute local paths;
- private project names;
- private tracker or document URLs;
- customer, client, or lead details;
- secrets, tokens, passwords, keys, cookies, or env dumps;
- machine-specific Keychain, SSH, browser profile, or MCP assumptions.

## Attribution

Keep `NOTICE.md` intact. This pack is inspired by
`addyosmani/agent-skills`, and that upstream attribution should remain visible.
