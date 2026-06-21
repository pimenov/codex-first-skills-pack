# Customizing The Pack

## Recommended Customization

After installing the skills, add a short routing section to your global or
project `AGENTS.md`.

Start from:

```text
templates/AGENTS.skills-routing.md
```

Then adapt:

- your language preference;
- your issue tracker;
- your documentation layer;
- your production approval rules;
- your preferred test commands;
- your deploy process.

## Keep Public Skills Generic

Do not put private company rules directly into a reusable public skill unless
the skill is meant to be private.

Avoid:

- personal names;
- local absolute paths;
- private project names;
- internal service hostnames;
- Notion, Linear, Jira, GitHub, or CRM IDs;
- secrets or credential setup commands;
- production account assumptions.

Prefer:

- "the user" instead of a personal name;
- "project tracker" instead of a specific tracker when the tracker is optional;
- "local runbook" instead of a machine-specific folder;
- "match the user's language" instead of hard-coding a language.

## Private Extensions

If your team needs private workflows, create a separate private skill pack.
That private pack can depend on this public pack conceptually, but it should
not be mixed into the public repository.
