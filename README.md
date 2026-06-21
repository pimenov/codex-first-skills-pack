# Codex First Skills Pack

Opinionated engineering skills for Codex and other Markdown-based coding agents.

This pack is a compact Codex-oriented adaptation inspired by
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). It keeps
the most useful engineering workflow gates for everyday software work:
clarify, plan, implement in slices, verify, debug, review, and challenge risky
decisions before they become expensive.

## What This Is

Skills are small instruction folders. Each folder contains a `SKILL.md` file
with frontmatter that tells Codex when to load the skill, and a body that gives
the workflow Codex should follow.

This repository is designed for people who want Codex to work less like a
one-shot code generator and more like a disciplined engineering partner:

- define the work before coding;
- keep context bounded;
- use official sources for version-sensitive APIs;
- break large changes into verified slices;
- debug from evidence instead of guessing;
- write tests or focused checks before claiming success;
- review changes before calling them done;
- use adversarial review for high-risk decisions.

## Included Skills

| Skill | Use When |
|---|---|
| `context-engineering` | Starting/resuming work, switching repos, or when source-of-truth is unclear. |
| `spec-driven-development` | Defining what should be built before planning or coding. |
| `planning-and-task-breakdown` | Turning fuzzy work into tasks, scope, dependencies, and stop-lines. |
| `incremental-implementation` | Building multi-file changes in small verified slices. |
| `source-driven-development` | Checking current official docs for SDKs, APIs, CLIs, frameworks, or cloud services. |
| `api-and-interface-design` | Designing stable APIs, schemas, events, configs, CLIs, or module boundaries. |
| `test-driven-development` | Fixing bugs or changing behavior with tests or focused checks. |
| `debugging-and-error-recovery` | Investigating failures, logs, broken builds, CI, runtime bugs, or tool errors. |
| `code-review-and-quality` | Reviewing diffs, PRs, commits, or agent-written code before merge/ship. |
| `deprecation-and-migration` | Removing or replacing old APIs, jobs, integrations, configs, schemas, or flows. |
| `doubt-driven-review` | Challenging high-stakes claims before production, data, auth, billing, or irreversible work. |

## Quick Install For Codex

Clone the repository:

```bash
git clone <repo-url>
cd codex-first-skills-pack
```

Validate the pack:

```bash
python3 scripts/validate_skills.py
```

Install into Codex:

```bash
scripts/install.sh
```

By default the installer copies skills into:

```bash
${CODEX_HOME:-$HOME/.codex}/skills
```

Dry-run first if you want to see what would happen:

```bash
scripts/install.sh --dry-run
```

Install only one skill:

```bash
scripts/install.sh --skill source-driven-development
```

## Install Through Codex

If your Codex has the built-in `skill-installer`, you can ask Codex in plain
English:

```text
Install the `source-driven-development` skill from GitHub repo <owner>/<repo>,
path `skills/source-driven-development`.
```

For multiple skills, give multiple paths:

```text
Install skills from GitHub repo <owner>/<repo>:
- skills/context-engineering
- skills/source-driven-development
- skills/debugging-and-error-recovery
- skills/test-driven-development
```

After installing new skills, restart Codex so the skills list refreshes.

## Make Codex Route To These Skills

Skills work best when your `AGENTS.md` tells Codex when to use them. You can
copy the relevant block from:

```text
templates/AGENTS.skills-routing.md
```

The important idea is simple: users do not need to remember exact skill names.
They can say natural phrases like:

- "check the current docs";
- "break this into tasks";
- "debug this failure";
- "prove it with a test";
- "review this diff";
- "challenge this plan before we ship it".

Codex should map those phrases to the right skill.

## How Skills Activate

In Codex, skills are discoverable when they are installed under the active
Codex home, usually:

```text
~/.codex/skills/<skill-name>/SKILL.md
```

Codex sees each skill's `name` and `description`. When the user's request
matches a description, Codex reads the full `SKILL.md` and follows that
workflow.

## Attribution

This repository is an independent Codex-oriented adaptation inspired by
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), which is
licensed under MIT. See [NOTICE.md](NOTICE.md) for details.

## License

MIT. See [LICENSE](LICENSE).
