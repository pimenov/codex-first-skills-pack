---
name: planning-and-task-breakdown
description: Turns ambiguous, large, multi-step, or handoff-prone work into sequenced tasks with outcomes, dependencies, stop-lines, acceptance criteria, and the right durable layer. Use when planning a feature, bugfix campaign, refactor, migration, deploy prep, client/internal work packet, Linear issue set, or when the user asks to break down, plan, scope, make tasks, prepare execution, or decide the next safe steps before implementation.
---

# Planning And Task Breakdown

## Overview

Use this skill to turn "we should do X" into work that can actually be executed. The output should make order, dependencies, readiness, and stop-lines obvious.

This skill plans execution. It does not replace product thinking, code review, or implementation.

## Relationship To Other Skills

- Use `context-engineering` first when source of truth, project state, or constraints are unclear.
- Use `incremental-implementation` after a plan is ready and work should be executed in slices.
- Use `test-driven-development` for behavior-sensitive implementation tasks.
- Use `debugging-and-error-recovery` when the work starts from a failing system or bug.
- Use `doubt-driven-review` for high-stakes plans before production/data/auth/security mutations.
- Use `code-review-and-quality` when a produced implementation or task packet needs review.
- Use `source-driven-development` when task design depends on current framework, API, SDK, CLI, or platform behavior.

## Do Not Use

- Tiny tasks where the next action is obvious and safe.
- Pure brainstorming before the user wants executable work.
- Full product discovery when the core problem, audience, or success criteria are unknown; start with mini-PRD/discovery.
- Emergency incident recovery where stabilization must happen first.
- Creating Linear/Notion artifacts for raw thoughts that do not need durable execution memory.

## Core Loop

```text
INTENT -> MODE -> BREAKDOWN -> SEQUENCE -> READINESS -> HANDOFF
```

### 1. INTENT: State The Outcome

Before tasking, write one sentence:

```text
Target outcome: <what should be true when this work is done>
```

Then capture:

- who benefits or operates the result;
- current state;
- target state;
- non-goals;
- known constraints;
- risks or approval gates;
- source artifacts: issue, doc, repo, bug report, transcript, live state, or user request.

If the outcome is not clear, ask or run discovery before creating tasks.

### 2. MODE: Choose The Planning Layer

Pick the smallest layer that keeps the work safe.

| Situation | Use |
|---|---|
| Quick safe work, one person, clear next action | Chat plan or checklist |
| Implementation spans multiple files/slices | Work Packet plus task list |
| New product/user workflow or fuzzy feature | Mini-PRD before Work Packet |
| Needs execution across chats or people | Linear issue/document |
| Human/client-facing overview | Notion |
| Technical decision that should live with code | Repo docs / ADR |
| Local sandbox or reusable process | Local `RUNBOOK.md` / `SESSION_NOTES.md` |

Do not duplicate the same plan into every layer by default. Put it where it will be used.

### 3. BREAKDOWN: Create Executable Tasks

Each task should have:

- outcome, not just activity;
- scope and non-scope;
- owner or execution mode when relevant;
- dependencies;
- acceptance criteria;
- verification/checks;
- stop-lines;
- links/source artifacts;
- expected output artifact.

Use this shape:

```text
Task: <verb + outcome>
Why: <reason>
Scope: <included>
Not doing: <excluded>
Depends on: <dependency or none>
Acceptance: <observable done criteria>
Verification: <checks/smoke/review>
Stop-lines: <when to pause>
Output: <code/doc/issue/comment/runbook/etc.>
```

Avoid tasks like "implement backend" or "fix UI". They hide too much. Split by outcome.

### 4. SEQUENCE: Order By Risk And Dependencies

Prefer this ordering:

1. Clarify contracts and source of truth.
2. Prove the riskiest unknown.
3. Build the smallest vertical slice.
4. Add edge cases and hardening.
5. Verify, review, and document.
6. Deploy or hand off only after readiness gates.

Name blockers explicitly:

```text
Blocked until:
- <fact/access/approval/test/data needed>
```

If tasks can run in parallel, say why they are independent. Do not parallelize tasks that edit the same files or mutate the same external system.

### 5. READINESS: Mark What Is Ready For Codex

A task is ready when:

- source of truth is identified;
- scope is bounded;
- acceptance criteria are testable;
- needed access is available or not needed;
- stop-lines are clear;
- no unresolved product decision is hidden inside implementation.

Use statuses:

- `Needs clarification`: missing decision or source.
- `Ready for discovery`: read-only investigation can start.
- `Ready for Codex`: bounded execution can start.
- `Needs approval`: next step mutates production/data/auth/external systems or changes scope.
- `Ready for smoke`: implementation done, user/live verification remains.
- `Done`: criteria met and evidence recorded.

Do not mark `Ready for Codex` just because the task exists in Linear.

### 6. HANDOFF: Preserve The Plan

When the plan needs to survive beyond chat:

- local sandbox -> `RUNBOOK.md` and `SESSION_NOTES.md`;
- project execution -> Linear issue/document/comment;
- human/client overview -> Notion;
- code-owned technical decision -> repo docs/ADR;
- implementation sequence -> link tasks to source docs/issues.

If external sync fails, leave a local pending-sync block and do not claim sync happened.

## Mini-PRD Gate

Raise `PRD-needed` when the work:

- creates a new product capability or user workflow;
- affects UX, onboarding, operations, client-facing behavior, or multiple roles;
- could be technically correct but product-wrong;
- needs prioritization across several issues;
- will be handed to another person or future chat;
- depends on unclear audience, problem, or success criteria.

Mini-PRD should answer:

```text
Audience:
Problem:
Key scenarios:
Success criteria:
Non-goals:
Risks/dependencies:
Open questions:
Next safe step:
```

If the user explicitly chooses to skip PRD, record the assumption and move to Work Packet or task breakdown.

## Work Packet Gate

Use a Work Packet when implementation is non-trivial but product intent is clear.

Work Packet should include:

```text
Goal:
Context:
Current state:
Target state:
Scope:
Not doing:
Approach:
Tasks:
Risks:
Approval gates:
Definition of Done:
Verification:
Rollback/stop-lines:
Links:
```

For user-facing durable planning artifacts, match the user's language. Keep commands, paths, env vars, package names, issue keys, API identifiers, and external product names exact.

## Task Granularity

Good tasks are small enough to verify and large enough to matter.

Split when:

- one task has multiple owners or systems;
- acceptance criteria are vague;
- different tasks require different approvals;
- code and production mutation are mixed;
- refactor and behavior change are mixed;
- frontend, backend, schema, deploy, and docs are all bundled.

Merge when:

- tasks cannot be completed independently;
- verification would be identical and trivial;
- splitting creates ceremony without reducing risk;
- the whole change is a tiny one-file operation.

## Dependency Map

For larger work, include a lightweight graph:

```text
1. Discovery -> 2. Contract -> 3. Slice A -> 4. Slice B -> 5. Review -> 6. Smoke
```

Or:

```text
Parallel:
- A: docs/source audit
- B: local code scan

Serial:
- C depends on A+B
- D depends on C and approval
```

Dependency maps are for decisions, not decoration.

## Production And External Systems

For production, live data, auth, billing, DNS, routing, webhooks, migrations, VPS, Cloudflare, Linear, Notion, GitHub, Gmail, Calendar, Drive, or other live systems:

- first task should usually be read-only discovery;
- separate access request from implementation;
- separate dry-run from live mutation;
- separate deploy from cleanup/refactor;
- add backup/evidence/rollback tasks when relevant;
- mark exact approval gates.

Do not hide a production mutation inside a general implementation task.

## Output Shape

For quick planning:

```text
Plan:
1. <task> - <why / proof>
2. <task> - <why / proof>
Stop-lines: <pause conditions>
Ready now: <first task>
```

For substantial work:

```text
Planning report:
- Target outcome:
- Mode: <chat checklist / mini-PRD / Work Packet / Linear / Notion / repo docs>
- Assumptions:
- Tasks:
- Dependencies:
- Ready for Codex:
- Needs clarification:
- Approval gates:
- Definition of Done:
- Next safe step:
```

For Linear/Notion/repo docs, use Russian headings by default.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The task is obvious." | If acceptance cannot be tested, it is not ready. |
| "We can plan after coding starts." | Coding turns hidden product decisions into accidental architecture. |
| "Just create a Linear issue." | A task without outcome, scope, and stop-lines is a parking lot, not execution memory. |
| "Everything depends on everything." | Then the first task is to clarify contracts and dependencies. |
| "This is only internal." | Internal operational work still needs source, evidence, and rollback when it touches real systems. |

## Red Flags

- Task titles are vague verbs: "do", "improve", "fix", "implement" without outcome.
- No acceptance criteria.
- No stop-lines for production/data/auth/external systems.
- A plan creates many issues but no first executable step.
- A technical task hides a product decision.
- Work Packet duplicates Notion and Linear without purpose.
- "Ready for Codex" is used when access, source, or approval is missing.
- Deploy, migration, cleanup, and refactor are bundled together.

## Verification

Before finishing a plan, confirm:

- [ ] Target outcome is clear.
- [ ] Correct planning layer was chosen.
- [ ] Tasks have outcomes, scope, acceptance, verification, and stop-lines.
- [ ] Dependencies and blockers are explicit.
- [ ] Ready vs not-ready tasks are separated.
- [ ] Approval gates are named.
- [ ] Durable artifact location is correct, or chat-only plan is enough.
