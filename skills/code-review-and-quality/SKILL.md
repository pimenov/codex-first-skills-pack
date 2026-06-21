---
name: code-review-and-quality
description: Reviews code changes across correctness, tests, readability, architecture, security, and performance before they are merged, shipped, or called done. Use when the user asks for a code review, when reviewing a PR/diff/commit/agent-produced code, after implementation or bugfix before final confidence, when deciding whether a change is ready, or when large/unclear changes need findings with severity and verification gaps.
---

# Code Review And Quality

## Overview

Use this skill as the normal code quality gate for finished or nearly finished code changes. The review should find real bugs, regressions, missing tests, unsafe assumptions, confusing structure, and verification gaps.

This is not praise, style commentary, or a rewrite plan by default. Lead with actionable findings.

## Relationship To Other Skills

- Use `context-engineering` first when the change intent, source of truth, or local conventions are unclear.
- Use `doubt-driven-review` for high-stakes claims or risky production/auth/data decisions, especially before mutation.
- Use `codex-security:*` for deep or scoped security review when security is the primary task.
- Use `impeccable` for frontend visual/UX/design review.
- Use `test-driven-development` when review finds a behavior gap that needs a regression guard.
- Use `source-driven-development` when review depends on current framework, SDK, API, CLI, or platform behavior.

## Do Not Use

- Pure prose, documentation, or strategy review with no code artifact.
- Design critique of UI aesthetics; route to `impeccable`.
- Deep security audit; route to `codex-security:*`.
- High-stakes operational approval where the artifact is a deploy/migration/rollback decision; route to `doubt-driven-review`.
- Reviewing without a concrete diff, files, commit, PR, patch, or generated code to inspect.

## Review Contract

Before reviewing, establish:

- what the change is trying to accomplish;
- the expected behavior or acceptance criteria;
- the diff, files, commit, PR, or generated code under review;
- relevant tests or verification evidence;
- local conventions and nearest `AGENTS.md`;
- whether production, data, auth, secrets, billing, or public APIs are touched.

If the contract is missing and affects correctness, ask or run read-only discovery before reviewing.

## Review Order

### 1. Read Intent Before Diff

Find the task, issue, spec, commit message, user request, or nearby notes. If no intent exists, infer cautiously and label the inference.

Do not judge code only by taste. Review against the contract and the codebase's existing patterns.

### 2. Inspect Tests First

Tests show what the author thinks matters.

Check:

- tests exist for behavior changes and bug fixes;
- tests assert behavior, not incidental implementation details;
- edge cases are covered: null/empty/boundary/error paths;
- test names describe expected behavior;
- a bugfix has a regression guard;
- test updates did not simply bless broken behavior.

Missing or weak tests are findings when they reduce confidence in changed behavior.

### 3. Review Implementation Across Six Axes

Use these axes for every changed area.

**Correctness**

- matches the spec, issue, or user-visible requirement;
- handles edge cases, race conditions, concurrency, time zones, idempotency, retries, and partial failure where relevant;
- preserves existing behavior outside scope;
- avoids off-by-one, stale state, cache invalidation, and ordering bugs;
- does not silently swallow errors.

**Tests And Verification**

- focused tests/checks cover the changed behavior;
- broader checks are appropriate for the blast radius;
- manual verification is described when automation is unrealistic;
- build/typecheck/lint results are relevant and current;
- screenshots or browser checks exist for UI behavior when needed.

**Readability And Simplicity**

- names are clear and consistent with local conventions;
- control flow is direct;
- abstractions earn their complexity;
- comments explain non-obvious intent, not obvious syntax;
- no cleverness, dead branches, temporary scaffolding, or debug leftovers.

**Architecture**

- fits existing module boundaries and ownership;
- dependencies flow in the expected direction;
- no unjustified new framework, dependency, global state, or cross-layer shortcut;
- shared code is extracted only when reuse is real;
- public contracts and schemas remain compatible unless the breaking change is explicit.

**Security And Data Safety**

- no raw secrets, tokens, private keys, or full env files;
- input is validated at trust boundaries;
- authorization/authentication remains enforced;
- queries and shell calls avoid injection;
- external data, logs, tickets, and fixtures are treated as untrusted data;
- sensitive data is not exposed in logs, errors, telemetry, or UI.

**Performance And Operations**

- no obvious N+1 queries, unbounded loops, unpaginated lists, or excessive data fetches;
- no hot-path allocations or synchronous blocking work where it matters;
- no avoidable frontend re-render churn for UI changes;
- observability, rollback, migrations, and operational behavior match the change risk;
- deployment/config changes have a clear verification path.

## Severity Labels

Classify every finding so the author knows what is required.

| Label | Meaning | Action |
|---|---|---|
| `Critical` | Security issue, data loss, broken core behavior, production-breaking regression. | Must fix before merge/ship. |
| `High` | Likely bug, missing guard for important behavior, risky architecture break. | Should fix before merge/ship. |
| `Medium` | Real maintainability, test, edge-case, or performance issue with bounded impact. | Fix or explicitly defer. |
| `Low` | Minor issue, local cleanup, small readability concern. | Optional unless easy and in scope. |
| `Nit` | Pure preference or tiny style detail. | Optional; do not block. |

Avoid dumping many low-value comments. A review that hides one `Critical` issue among twenty nits is a bad review.

## Output Shape

When the user asks for a review, follow the Codex review stance:

1. Findings first, ordered by severity.
2. File and line references for each finding when available.
3. Open questions or assumptions.
4. Brief verification summary and residual risk.
5. Short change summary only as secondary context.

Use this compact shape:

```text
Findings:
- [High] path/to/file.ts:123 - <specific issue, why it matters, what would fail>

Open questions:
- <question if any>

Verification:
- Reviewed: <diff/files/tests/docs>
- Not run / not available: <gaps>

Summary:
- <brief, optional>
```

If there are no issues, say that clearly and still name test gaps or residual risk.

## Reviewing Your Own Work

Before saying "done":

- inspect the actual diff or edited files;
- run focused checks proportional to the risk;
- look specifically for changes outside the requested scope;
- verify no debug artifacts, placeholders, broad refactors, or unrelated formatting slipped in;
- confirm final answer does not overclaim unrun tests or deploy/smoke status.

Self-review is weaker than fresh review. For high-stakes work, use `doubt-driven-review` or another reviewer when available.

## Large Changes

If the change is too large to review properly:

- identify the logical slices;
- review the riskiest slice first;
- ask to split before merge when review quality would be fake;
- distinguish generated/mechanical changes from hand-written logic;
- verify the generator or transformation, not every repeated output line.

Size guidance:

- around 100 changed lines: usually reviewable;
- around 300 changed lines: reviewable if one logical change;
- around 1000 changed lines: usually split unless mechanical or deletion-heavy.

## Dependency Review

When the change adds or upgrades a dependency, check:

- existing stack or standard library cannot reasonably solve it;
- package is maintained and appropriately licensed;
- bundle/runtime impact is acceptable;
- known vulnerabilities are checked with the repo's normal tools;
- supply-chain risk is appropriate for the project;
- dependency is pinned or ranged according to local convention.

Do not approve new dependencies just because they make implementation shorter.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Tests pass, so the code is good." | Tests are evidence, not a full review. Architecture, security, and readability still matter. |
| "I wrote it, so I know the intent." | Authors are blind to assumptions. Review the diff as if someone else wrote it. |
| "It is AI-generated, so it probably followed the prompt." | AI-generated code needs more scrutiny because it can be plausible and wrong. |
| "We will clean it up later." | Deferred cleanup usually becomes permanent. Require cleanup unless there is a real emergency. |
| "This is just a small change." | Small changes can still break auth, data, routing, or edge cases. |

## Red Flags

- "LGTM" without evidence of review.
- No regression test after a bug fix.
- Tests changed to match implementation without explaining the requirement change.
- Review ignores auth, data, secrets, or external input boundaries.
- Large diff with no clear logical slices.
- New dependency without dependency review.
- Public contract or schema change without compatibility analysis.
- Manual verification claimed but not described.
- Findings lack severity or concrete failure mode.

## Verification

Before finishing a review, confirm:

- [ ] Intent and review artifact were identified.
- [ ] Tests and verification evidence were inspected.
- [ ] Correctness, tests, readability, architecture, security, and performance were considered.
- [ ] Findings are severity-labeled and grounded in file/line references when possible.
- [ ] Optional opinions are separated from required fixes.
- [ ] Remaining risk and unrun checks are stated plainly.
