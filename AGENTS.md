# AGENTS.md

## Scope

This repository is a public reusable Codex skills pack.

## Rules

- Keep all committed content safe for public sharing.
- Do not add secrets, tokens, private keys, full env files, cookies, auth state,
  or private service credentials.
- Do not add personal local paths, private project names, private customer data,
  tracker IDs, private Notion/Linear/GitHub links, or machine-specific access
  assumptions.
- Keep skills generic. Use "the user" instead of a named person.
- Match the user's language in examples when useful, but do not hard-code a
  single person's language preference into reusable skills.
- Prefer one self-contained `SKILL.md` per skill unless a script or reference
  materially improves repeatability.
- Update README or docs when adding, removing, or renaming a skill.
- Run validation before finishing:

```bash
python3 scripts/validate_skills.py
scripts/install.sh --dry-run
```

## Style

- Skills should be concise, procedural, and evidence-oriented.
- Frontmatter `description` must explain both what the skill does and when it
  should trigger.
- Avoid motivational filler. Write workflows, gates, red flags, and verification
  requirements.
