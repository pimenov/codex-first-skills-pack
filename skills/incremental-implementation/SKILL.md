---
name: incremental-implementation
description: Breaks large or multi-file implementation work into small verified slices that keep the project working after each step. Use when building a feature, bugfix, refactor, migration, integration, UI flow, or operational change that could become a large diff; when more than one file/module is touched; when scope is fuzzy; when review or rollback would be hard; when Codex is tempted to code for a long time before testing; or when the user asks to work in small verified steps, slices, маленькими проверяемыми шагами, по шагам с проверкой, or после каждого шага проверяй.
---

# Incremental Implementation

## Overview

Build in small complete slices. Each slice should have a clear purpose, a bounded file set, a focused verification step, and a checkpoint before moving on.

This skill turns "do the whole thing" into "make one safe step true, prove it, then continue."

When the user asks to work in small verified steps, explicitly name this skill before planning or editing. The behavior is not enough; the user should be able to see that the slice gate is active.

## Relationship To Other Skills

- Use `context-engineering` first when the right slice boundary depends on project structure or source of truth.
- Use `test-driven-development` for behavior-sensitive slices where a failing check should come first.
- Use `debugging-and-error-recovery` when a slice fails unexpectedly.
- Use `code-review-and-quality` before calling a multi-slice change done.
- Use `doubt-driven-review` before risky production, auth, data, migration, or irreversible steps.
- Use `source-driven-development` when a slice depends on current framework, SDK, API, CLI, or platform behavior.

## Do Not Use

- Tiny one-file changes where the scope is already smaller than a slice.
- Pure documentation or copy edits with no implementation risk.
- Mechanical formatting changes that should be one bounded operation.
- Emergency rollback or incident stabilization where the first priority is restore-safe-state.
- Cases where slicing would hide a required atomic change, such as a schema and code deploy that must ship together.

## Core Loop

```text
PLAN SLICE -> IMPLEMENT -> VERIFY -> CHECKPOINT -> NEXT SLICE
```

### 1. PLAN SLICE: Choose The Smallest Useful Step

Before editing, define:

- current target outcome;
- what is in this slice;
- what is explicitly out of scope;
- files or modules likely touched;
- proof for this slice;
- rollback or stop-line if it fails.

Good slice shapes:

- one end-to-end vertical path;
- one contract/type/interface before consumers;
- one risky unknown proven with a spike or focused check;
- one bug reproduction plus fix;
- one mechanical move before behavior changes;
- one UI state or route before the whole flow.

Bad slice shapes:

- "update backend, frontend, tests, copy, config, and cleanup";
- "refactor while adding the feature";
- "touch every nearby file while I am here";
- "implement everything, then see if it builds."

### 2. IMPLEMENT: Keep The Change Narrow

Within a slice:

- edit only files needed for that slice;
- prefer the simplest implementation that satisfies the slice;
- avoid speculative abstractions;
- do not modernize or clean adjacent code unless it is required;
- keep behavior changes separate from mechanical refactors;
- keep incomplete user-visible work hidden behind a safe default or feature flag when needed.

If the slice expands while coding, stop and split it instead of silently widening scope.

### 3. VERIFY: Prove The Slice

Run the smallest useful check first:

- focused unit/integration/component test;
- typecheck or build for touched stack;
- lint only when relevant to touched files;
- browser/manual smoke for UI behavior;
- dry-run or read-only smoke for operational work.

Then widen checks only when the blast radius justifies it.

Do not rerun the same expensive command repeatedly on unchanged code. Rerun after meaningful edits.

### 4. CHECKPOINT: Preserve A Safe Boundary

After a verified slice, leave a clear recovery point.

In git repositories:

- inspect `git status --short`;
- review the diff for only this slice;
- stage explicit files only when committing;
- commit only when the user asked for commits or the repo workflow makes it clearly appropriate;
- never auto-commit secrets, generated noise, unrelated user changes, or dirty-tree leftovers.

Outside git or when not committing:

- summarize the slice in chat or `SESSION_NOTES.md` when durable tracking matters;
- name files changed and checks run;
- record remaining slices and stop-lines;
- leave temporary/debug artifacts cleaned up unless intentionally saved as evidence.

Checkpoint does not always mean commit. It means the next step starts from a known state.

### 5. NEXT SLICE: Continue Or Stop Deliberately

Continue only if:

- the last slice is verified or its gap is explicitly accepted;
- the next slice has a clear scope;
- no new approval gate appeared;
- the workspace is still clean enough to proceed safely.

Stop and report when:

- tests/build fail and the root cause is not understood;
- production/data/auth/routing/secrets changes become necessary;
- the next slice would be a different feature;
- local untracked or user changes make scope unsafe;
- the remaining work needs a Work Packet, Linear issue, or explicit approval.

## Slicing Strategies

### Vertical Slice

Use when the user-visible path matters.

```text
Slice 1: minimal create path through model/API/UI
Slice 2: list/display path
Slice 3: edit path
Slice 4: delete or edge states
```

Each slice should work end-to-end, even if the UI is plain or the behavior is hidden behind a flag.

### Contract-First Slice

Use when backend/frontend, service/client, or worker/API boundaries matter.

```text
Slice 0: define types/schema/API contract
Slice 1: backend/provider implementation with tests
Slice 2: consumer implementation against the contract
Slice 3: integration smoke
```

Do not let both sides drift by implementing from two different assumptions.

### Risk-First Slice

Use when one unknown could invalidate the plan.

```text
Slice 1: prove auth/token/API/websocket/filesystem behavior
Slice 2: build the normal path on the proven boundary
Slice 3: add retries, edge cases, and cleanup
```

If the risky slice fails, switch to discovery or `debugging-and-error-recovery`.

### Mechanical-Then-Behavior Slice

Use for refactors.

```text
Slice 1: move/rename/extract with no behavior change
Slice 2: verify behavior is unchanged
Slice 3: add the actual behavior change
```

Do not mix rename noise with business logic changes.

### Guard-Then-Fix Slice

Use for bugs.

```text
Slice 1: reproduce failing behavior
Slice 2: minimal fix
Slice 3: regression guard and nearby checks
```

This usually pairs with `test-driven-development`.

## Scope Discipline

Say what you noticed but did not touch:

```text
Not touching in this slice:
- unrelated formatting in <file>
- old comment near changed code
- broader refactor of <module>
```

Do not bundle "while I am here" improvements into a slice. If they matter, create a later slice or task.

## Production And External Systems

For production, live data, auth, billing, routing, DNS, webhooks, migrations, external SaaS, VPS, Cloudflare, Linear, Notion, or GitHub mutations:

- first slice is read-only discovery unless approval already covers the exact mutation;
- dry-run before live writes where possible;
- keep backup/evidence and rollback boundaries explicit;
- do not combine deploy or schema changes with cleanup/refactor;
- after each approved mutation slice, run the agreed smoke and record evidence.

Incremental work reduces risk; it does not grant permission to mutate production.

## Output Shape

For substantial implementation, keep a compact slice report:

```text
Incremental plan:
- Target: <desired outcome>
- Slice 1: <scope, proof, stop-line>
- Slice 2: <scope, proof, stop-line>
- Not doing: <explicit non-goals>

Slice report:
- Slice: <what changed>
- Files: <paths>
- Verification: <commands/checks and results>
- Checkpoint: <commit / notes / known state>
- Next slice: <next safe step>
```

For tiny tasks, do not over-report. Use the slice report only when it helps orientation.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It is faster to do it all at once." | It feels faster until debugging a large mixed diff consumes the time. |
| "I will test at the end." | Early bugs contaminate later slices. Test the slice while the cause is still small. |
| "This refactor is small enough to include." | Refactor plus feature makes review and rollback worse. Separate it. |
| "I will add the feature flag later." | Incomplete user-visible work needs a safe default now. |
| "One big commit is fine." | Big commits hide unrelated changes and make rollback expensive. |
| "The project is not git, so checkpoints do not matter." | Non-git work still needs session notes, evidence, and clean handoff points. |

## Red Flags

- More than roughly 100 lines of behavior code written without a check.
- A slice touches many unrelated modules.
- Build or tests are broken between slices.
- A large unreviewed diff accumulates.
- A feature and refactor are mixed.
- Scope grows because adjacent code looked messy.
- New dependency added inside a slice without dependency review.
- Production/data/auth mutation appears without approval.
- The final answer says "done" but cannot name each slice and proof.

## Verification

Before finishing the overall task, confirm:

- [ ] Work was split into logical slices or the no-slice reason is clear.
- [ ] Each slice had explicit scope and non-scope.
- [ ] Each slice left the project in a known state.
- [ ] Focused checks were run after meaningful changes.
- [ ] Broader checks matched the blast radius.
- [ ] Checkpoints were recorded without capturing unrelated user changes.
- [ ] Remaining slices, risks, and approval gates are stated plainly.
