---
name: spec-driven-development
description: Defines the implementation contract before planning or coding so work is built against explicit goals, users, scope, non-goals, assumptions, acceptance criteria, and verification. Use when creating or changing a feature, product workflow, API, integration, migration, user-facing behavior, cross-team handoff, or any task where Codex could implement the wrong thing correctly; when the user asks for a spec, requirements, PRD, contract, acceptance criteria, or "what exactly are we building".
---

# Spec-Driven Development

## Overview

Use this skill before planning or implementation when the contract is not already explicit. The output should make it clear what is being built, why, for whom, what counts as done, and what is intentionally out of scope.

Spec-driven development is a guard against technically clean work that solves the wrong problem.

## Relationship To Other Skills

- Use `context-engineering` first when the source of truth or current project state is unclear.
- Use `planning-and-task-breakdown` after the spec is accepted or the contract is clear.
- Use `incremental-implementation` after planning to execute the work in verified slices.
- Use `test-driven-development` to turn acceptance criteria into failing checks.
- Use `source-driven-development` when spec choices depend on current external API, SDK, framework, or platform behavior.
- Use `doubt-driven-review` before high-stakes specs involving production, auth, data, billing, security, or irreversible operations.

## Do Not Use

- Tiny implementation tasks with clear requirements and low risk.
- Pure bug reproduction where expected behavior is already obvious; use `debugging-and-error-recovery` and `test-driven-development`.
- Emergency incident stabilization before safe state is restored.
- Pure writing/copy tasks unless the acceptance criteria are unclear.
- Creating a durable spec artifact when a short chat contract is enough.

## Core Loop

```text
INTENT -> CONTRACT -> BOUNDARIES -> ACCEPTANCE -> STORAGE -> HANDOFF
```

### 1. INTENT: Name The Problem And Audience

Before writing tasks or code, answer:

- who is this for;
- what problem or job-to-be-done it addresses;
- what current pain or failure it removes;
- what will be different when it works;
- which source artifacts support this intent.

If the user intent is ambiguous, ask the smallest clarifying question or run read-only discovery. Do not fill product gaps with implementation guesses.

### 2. CONTRACT: Define The Desired Behavior

Write the behavior contract in concrete terms:

- primary scenarios;
- inputs and outputs;
- user/system actions;
- states and transitions;
- data or API contracts;
- permissions and roles;
- error and empty states;
- performance or reliability requirements when relevant;
- compatibility and migration expectations.

Prefer observable behavior over internal implementation details.

### 3. BOUNDARIES: State Scope And Non-Goals

A good spec says what not to do.

Include:

- in scope;
- explicitly out of scope;
- assumptions;
- dependencies;
- constraints;
- stop-lines;
- approval gates;
- risks and open questions.

If a hidden product decision appears, stop and mark it as an open question. Do not bury it inside implementation.

### 4. ACCEPTANCE: Make Done Testable

Acceptance criteria should be observable and verifiable.

Use this shape:

```text
Acceptance criteria:
- Given <state>, when <action>, then <observable result>.
- <System/API/data behavior> is true and verified by <test/check/smoke>.
- <Non-goal or excluded behavior> remains unchanged.
```

Map acceptance to proof:

- unit/integration/component test;
- typecheck/build/lint;
- browser/manual smoke;
- read-only live check;
- screenshots or artifacts;
- human approval when automation cannot verify the outcome.

If acceptance cannot be tested, the spec is not ready for implementation.

### 5. STORAGE: Choose The Right Artifact

Do not default to `SPEC.md`.

Choose the smallest durable layer that will actually be used:

| Situation | Artifact |
|---|---|
| Small clear change | Chat contract or issue comment |
| New product/user workflow | Mini-PRD |
| Implementation-ready project work | Work Packet |
| Execution across chats/people | Linear document or issue |
| Human/client-facing explanation | Notion |
| Technical contract owned by code | Repo docs / ADR / spec file |
| Local sandbox or reusable process | Local `RUNBOOK.md` / `SESSION_NOTES.md` |

For user-facing durable prose, match the user's language. Keep commands, paths, package names, API identifiers, env vars, issue keys, and canonical product names exact.

### 6. HANDOFF: Prepare For Planning Or Implementation

A spec is ready to hand off when:

- intent is clear;
- scenarios are concrete;
- non-goals are explicit;
- acceptance criteria are testable;
- source of truth is named;
- risks and approval gates are visible;
- unresolved questions are separated from ready work.

Then route:

- ready implementation -> `planning-and-task-breakdown`;
- behavior tests -> `test-driven-development`;
- thin execution -> `incremental-implementation`;
- risky decision -> `doubt-driven-review`;
- unclear product intent -> keep in discovery or mini-PRD refinement.

## Mini-PRD Shape

Use when the work is product-new, UX/operationally new, or could be technically right but product-wrong.

```text
Mini-PRD:
- Audience:
- Problem:
- Current state:
- Target state:
- Key scenarios:
- Success criteria:
- Non-goals:
- Risks/dependencies:
- Open questions:
- Next safe step:
```

Mini-PRD answers "what and why", not full implementation detail.

## Technical Spec Shape

Use when behavior and product intent are clear, but the implementation contract needs precision.

```text
Technical spec:
- Goal:
- Existing behavior:
- Desired behavior:
- Contract/API/schema/state changes:
- Edge cases:
- Compatibility/migration:
- Security/data considerations:
- Acceptance criteria:
- Verification plan:
- Rollback/stop-lines:
```

Technical specs should be close to code when they define durable code-owned contracts.

## Work Packet Bridge

After the spec is accepted, a Work Packet can answer "how to execute the next chunk safely".

Do not mix the two:

- Spec: what, why, for whom, success, non-goals.
- Work Packet: scope, tasks, approach, checks, approval gates, Definition of Done.

If both are needed, keep the spec concise and let `planning-and-task-breakdown` create the execution plan.

## Production And External Systems

Specs touching production, live data, auth, billing, DNS, routing, webhooks, migrations, external SaaS, VPS, Cloudflare, Linear, Notion, GitHub, Gmail, Calendar, Drive, or similar systems must include:

- read-only discovery first, unless exact mutation approval already exists;
- explicit no-touch systems;
- data classification and secret-handling assumptions;
- backup/evidence/rollback expectation;
- dry-run or staging path where available;
- live approval gate before mutation.

Do not let a spec imply permission to mutate production.

## Output Shape

For compact specs:

```text
Spec:
- Goal:
- Audience:
- Scenarios:
- Scope:
- Non-goals:
- Acceptance:
- Verification:
- Open questions:
- Next safe step:
```

For specs that should become durable artifacts, use Russian headings by default and state where the artifact belongs.

If the spec is not ready, do not pretend it is:

```text
Spec readiness:
- Ready:
- Not ready:
- Blocking questions:
- Safe next step:
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The feature is obvious." | Obvious features still hide audience, edge cases, and non-goals. |
| "We can clarify while coding." | Coding turns unclear requirements into accidental architecture. |
| "A task list is enough." | A task list without a contract can execute the wrong intent efficiently. |
| "We'll write acceptance later." | Acceptance after implementation often blesses what was built, not what was needed. |
| "It is internal, so no spec needed." | Internal operational work can still touch real systems and needs boundaries. |

## Red Flags

- No named audience or operator.
- No non-goals.
- Acceptance criteria are subjective or untestable.
- Product decisions are hidden in technical tasks.
- API/schema/state changes are vague.
- Production/data/auth behavior is implied but not approved.
- Spec duplicates Linear, Notion, and repo docs without purpose.
- The next step is implementation while open questions still block correctness.

## Verification

Before handing off a spec, confirm:

- [ ] Intent and audience are explicit.
- [ ] Desired behavior is observable.
- [ ] Scope and non-goals are clear.
- [ ] Assumptions, dependencies, risks, and approval gates are named.
- [ ] Acceptance criteria are testable.
- [ ] Verification plan matches the risk.
- [ ] Artifact location is correct, or chat-only contract is enough.
- [ ] Ready work is separated from open questions.
