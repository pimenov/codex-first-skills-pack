---
name: test-driven-development
description: Drives behavior changes through tests or explicit focused checks before implementation. Use when implementing new logic, fixing a bug, changing behavior, adding edge-case handling, modifying validation, refactoring behavior-sensitive code, or after debugging identifies a root cause that needs a regression guard. Also use when Codex is about to say a bug is fixed or behavior works but no proof exists yet.
---

# Test-Driven Development

## Overview

Use tests as executable proof of expected behavior. For bugs, first reproduce the bug with a failing test or focused check. For new behavior, define the expected behavior before writing implementation code.

This skill is not ceremony. It is a guard against "looks fixed" answers that cannot catch regressions.

## Do Not Use

- Pure documentation, copy, or static content changes with no behavior.
- Mechanical formatting, renames, or file moves.
- Configuration-only changes where the right proof is a config validation/build/smoke check rather than a unit test.
- One-off exploration before a behavior claim is made.
- Cases where the repo has no realistic test harness and the user explicitly chooses a manual smoke check.

## Core Loop

Use the smallest proof that matches the risk.

```text
RED -> GREEN -> REFACTOR -> VERIFY
```

### 1. RED: Define The Failing Behavior

Before implementation, create or identify a check that should fail before the fix.

Good RED targets:

- unit test for pure logic;
- integration test for service/API/database boundaries;
- component/browser test for UI behavior;
- CLI command or smoke script for operational behavior;
- minimal reproduction when no test harness exists.

For bugs, use the prove-it pattern:

```text
Bug report -> failing reproduction -> minimal fix -> passing reproduction -> broader check
```

If no failing test can be added, state why and name the substitute proof:

```text
No automated test added because <reason>.
Focused check: <command/manual smoke/repro script>.
Regression risk: <remaining gap>.
```

### 2. GREEN: Make The Smallest Fix

Write the minimum code that makes the RED check pass.

Do not mix in:

- broad refactors;
- unrelated cleanup;
- dependency upgrades;
- UI polish;
- new features not covered by the behavior check.

If the minimum fix needs a design decision, stop and surface the decision before coding through it.

### 3. REFACTOR: Improve Safely

Refactor only after the behavior check is green.

Keep refactors behavior-preserving. Run the focused check after meaningful refactor steps. If a refactor changes behavior, it needs its own RED check or a scope note.

### 4. VERIFY: Expand Confidence

Run checks in widening circles:

1. the focused failing test/check;
2. nearby tests for the touched module;
3. typecheck/lint/build if the stack uses them;
4. broader suite or browser/manual smoke when the touched surface warrants it.

Do not rerun expensive broad checks repeatedly on unchanged code. Say what was run and what remains unverified.

## Choosing Test Size

Prefer the smallest test that proves the behavior:

- `unit`: pure functions, validation rules, data transforms;
- `integration`: API handlers, database queries, service boundaries, auth checks;
- `component/browser`: user-visible UI behavior, routing, forms, rendering;
- `smoke`: deploy/runtime/CLI/config behavior where automated unit tests are not the right proof.

Avoid brittle tests that only assert implementation details unless the implementation detail is the contract.

## Working In Existing Repos

Before adding tests:

1. Read the existing test style and commands.
2. Find the closest similar test.
3. Use the repo's current runner and helpers.
4. Avoid adding a new test framework unless the user explicitly approves.
5. Keep test data small and deterministic.

If test commands or framework behavior are version-sensitive, use `source-driven-development` before inventing syntax.

## Working With Bugs

When `debugging-and-error-recovery` has identified a root cause, use this skill to add the guard.

Bugfix checklist:

- observed behavior is captured;
- expected behavior is explicit;
- failing reproduction exists or the no-test reason is stated;
- fix makes the reproduction pass;
- nearby regressions are checked.

Do not close a bug only because the code changed. Close it when the proof passes or the user explicitly accepts the remaining gap.

## Working With Production And External Systems

For production, data, auth, billing, routing, webhooks, email, CRM, Notion, Linear, GitHub, Directus, Cloudflare, VPS, or other live systems:

- keep the first pass read-only unless a bounded mutation is approved;
- prefer dry-runs, local fixtures, staging, or smoke checks over live writes;
- do not create synthetic production data without approval;
- record the exact check and rollback/evidence path when relevant.

Tests and smoke checks are evidence, not approval to deploy or mutate production.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is obvious." | Obvious behavior still regresses. A small check protects it. |
| "I'll add tests after." | After-the-fact tests often mirror the implementation instead of proving the requirement. |
| "There are no tests here." | Then state that and create the smallest focused check instead of pretending it is proven. |
| "The bug is fixed because I changed the code." | The bug is fixed when the failing scenario passes. |
| "A snapshot is enough." | Snapshots rarely prove behavior unless the rendered output is the contract. |

## Red Flags

- Claiming a bug is fixed without reproducing it first.
- Adding implementation code before defining expected behavior.
- Updating tests to match new behavior without explaining why the expectation changed.
- Removing a failing test instead of understanding it.
- Adding broad mocks that hide the real boundary being tested.
- Treating manual "looks good" as enough for risky behavior changes.
- Skipping verification because the change is small but user-visible.

## Output Shape

Use this compact report:

```text
TDD report:
- Behavior: <what should be true>
- RED: <test/check that failed or no-test reason>
- GREEN: <minimal fix>
- Guard: <test/check now protecting behavior>
- Verification: <commands/checks and results>
- Remaining risk: <if any>
```

For user-facing durable notes, write explanatory prose in the user's language and keep commands, paths, env vars, test names, and package names in their exact form.

## Verification

Before finishing, confirm:

- [ ] Expected behavior was stated before or alongside implementation.
- [ ] A failing test/check existed, or a no-test reason was stated.
- [ ] The implementation was the smallest reasonable fix for that behavior.
- [ ] The focused test/check passed after the fix.
- [ ] Broader checks were run when the touched surface warranted them.
- [ ] Remaining unverified risk was stated plainly.
