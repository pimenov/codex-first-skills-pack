# How The Pack Works

## Skill Anatomy

Each skill lives in:

```text
skills/<skill-name>/SKILL.md
```

Each `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: source-driven-development
description: Grounds framework, library, SDK, API, CLI, and cloud-service implementation decisions in current official sources...
---
```

Codex uses the frontmatter to decide whether a skill is relevant. The full body
is loaded only after the skill triggers.

## Operating Model

The pack is intentionally small. It does not try to automate every part of
software delivery. Instead, it gives Codex reusable gates:

1. Establish context.
2. Define the work.
3. Plan the execution.
4. Implement in small slices.
5. Verify behavior.
6. Debug from evidence.
7. Review quality.
8. Challenge risky claims.
9. Migrate or remove old behavior carefully.

## Natural Language Triggers

Users should not need to invoke exact skill names. Good routing phrases are:

| User Says | Likely Skill |
|---|---|
| "What are we actually building?" | `spec-driven-development` |
| "Break this down." | `planning-and-task-breakdown` |
| "Check the current docs." | `source-driven-development` |
| "Do it in small safe steps." | `incremental-implementation` |
| "This command fails." | `debugging-and-error-recovery` |
| "Prove the bug is fixed." | `test-driven-development` |
| "Review this PR." | `code-review-and-quality` |
| "Design this API." | `api-and-interface-design` |
| "Can we delete the old thing?" | `deprecation-and-migration` |
| "Are we fooling ourselves?" | `doubt-driven-review` |

## What This Pack Does Not Do

This pack does not:

- grant permission to mutate production;
- replace project-specific `AGENTS.md` rules;
- replace tests, code review, or deployment process;
- provide secrets, connectors, or service credentials;
- assume Notion, Linear, GitHub, or any other external system is available.

Project-specific rules still win when they are more specific.
