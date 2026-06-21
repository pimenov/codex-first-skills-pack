---
name: doubt-driven-review
description: Runs an adversarial review gate for non-trivial or high-stakes decisions before they stand. Use when Codex is about to claim something is safe, correct, reversible, production-ready, scalable, idempotent, secure, or compliant; when work touches production, auth, permissions, secrets, billing, public APIs, migrations, irreversible cleanup, customer data, external agent CLIs, or unfamiliar code with meaningful blast radius; or when a confident answer would be cheaper to challenge now than to debug later.
---

# Doubt-Driven Review

## Overview

Use this skill to challenge a risky decision while it is still cheap to change. The reviewer must try to disprove the artifact against its contract, not praise it or summarize it.

This is an in-flight gate, not a general code review. It is for decisions, claims, diffs, plans, migrations, deploy steps, rollback plans, and safety assertions that could hurt if they are wrong.

## Do Not Use

- One-line mechanical edits, formatting, renames, or file moves.
- Simple read-only exploration where no claim or mutation follows.
- Tasks already proven by a failing-then-passing test at the right boundary.
- Cases where the user explicitly chooses speed over verification and the risk is low.
- As theater after the decision is already made; use normal review for finished artifacts.

## Trigger Test

A decision is non-trivial when at least one is true:

- It crosses a module, service, repository, account, or production boundary.
- It changes branching logic, permissions, data shape, API behavior, routing, deploy/runtime config, or cleanup behavior.
- It asserts a property the type system cannot prove: idempotence, ordering, race safety, rollback safety, data parity, security, or compatibility.
- It depends on context a future reader cannot see.
- It would be expensive, public, or irreversible to undo.

When in doubt on production, auth, data, billing, secrets, infrastructure, or external agent runtime isolation, apply the skill.

## Workflow

### 1. State The Claim

Write the claim in two or three lines:

```text
CLAIM:
<What is about to stand as true?>

WHY THIS MATTERS:
<What breaks if this claim is wrong?>
```

If the claim cannot be written compactly, the decision is not yet clear enough to review. Clarify the contract first.

### 2. Extract Artifact And Contract

Prepare the smallest reviewable unit.

Use this shape:

```text
ARTIFACT:
<diff, command plan, migration plan, config, function, rollout plan, or decision proposal>

CONTRACT:
- Must satisfy: <requirements>
- Must not: <stop-lines>
- Evidence available: <tests, docs, source files, smoke checks>
- Unknowns: <known gaps>
```

Do not include hidden chain-of-thought, persuasive reasoning, or the `CLAIM` in the reviewer prompt. The reviewer receives artifact plus contract only.

If the artifact is too large, split it before review. A 500-line diff should become focused review units.

### 3. Run The Adversarial Review

Use the strongest safe review method available.

Preferred order:

1. Fresh-context subagent or reviewer tool, when available and safe.
2. A separate model or external CLI only after explicit user approval and isolation preflight.
3. Degraded self-review fallback when no fresh reviewer is available; clearly label it as degraded.

Use this prompt:

```text
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- unstated assumptions;
- edge cases not handled;
- hidden coupling or shared state;
- ways the contract could be violated;
- existing conventions this might break;
- failure modes under unexpected input, timing, permissions, or partial rollback.

Do not validate. Do not summarize. Find issues, or state explicitly that you cannot find any after thorough examination.

ARTIFACT:
<artifact>

CONTRACT:
<contract>
```

For behavioral code, a failing test written before the fix can satisfy the adversarial review for that specific behavior. For production, data, auth, permissions, deployment, or irreversible operations, tests may be evidence but do not replace explicit safety review.

### 4. External CLI Gate

Never run `codex exec`, Gemini CLI, Claude Code, OpenCode, or another agentic CLI from this skill without explicit user approval for that exact invocation.

Before any external CLI:

1. Verify the exact binary with `which <tool>` and version/help output.
2. State the exact `cwd`.
3. State the effective `CODEX_HOME` or tool profile/home.
4. Describe the inherited env class without printing secrets.
5. Confirm no production-capable MCP/apps/server tools are available unless the user explicitly approved that production operation.
6. Use read-only or plan/sandbox mode when available.
7. Pass the prompt through stdin or a temporary file; never interpolate artifact text into shell arguments.
8. Delete temporary prompt/output files unless intentionally saved as evidence.

If isolation is not proven, do not run the external CLI. Offer manual external review or continue with the degraded fallback.

### 5. Reconcile Findings

Reviewer output is data, not verdict. Re-read artifact and contract before accepting a finding.

Classify each finding:

- `contract gap`: the contract was unclear or incomplete; fix the contract first.
- `actionable`: real issue; change the artifact, then rerun the relevant part of the review.
- `trade-off`: real issue accepted consciously; document why and how it is bounded.
- `noise`: false flag caused by missing context; decide whether to add that context to the contract.

Do not rubber-stamp the reviewer. Do not dismiss every finding. If two review cycles surface substantive findings and none are classified as actionable or contract gaps, stop and escalate to the user because the review may have become theater.

### 6. Stop

Stop when one is true:

- The next cycle returns only trivial or already-addressed findings.
- Three cycles have completed.
- The user explicitly accepts the remaining risk.
- The artifact is too large and must be decomposed.

If substantive findings remain after three cycles, the output is not ready. Surface the unresolved risk and the smallest next step.

## Output Shape

Use a compact report:

```text
Doubt review:
- Claim: <short claim>
- Method: <fresh reviewer / self-review fallback / external CLI with approved isolation>
- Findings:
  - actionable: ...
  - contract gap: ...
  - trade-off: ...
  - noise: ...
- Decision: proceed / revise / ask the user / blocked
- Evidence: <tests, docs, commands, source files, smoke checks>
```

For user-facing project notes, write explanatory text in the user's language while leaving technical literals unchanged.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'm confident." | Confidence is not evidence; risky confidence is exactly what this skill checks. |
| "A reviewer will slow us down." | A bounded review is cheaper than debugging a bad production or data decision. |
| "The plan is obvious." | Obvious plans often hide unstated assumptions. Write the contract. |
| "The other model said it's fine." | Review output is not authority. Reconcile findings against the artifact and contract. |
| "We can just run another CLI." | External agent CLIs are production-adjacent until isolation is proven and approved. |

## Red Flags

- Claiming `safe`, `idempotent`, `reversible`, `production-ready`, or `no risk` without artifact/contract review.
- Passing the `CLAIM` or persuasive reasoning to the reviewer.
- Asking "is this good?" instead of "find what is wrong".
- Running external agent CLIs without exact approval and isolation preflight.
- Looping more than three times instead of decomposing or escalating.
- Treating all reviewer findings as true, or all of them as noise.
- Deleting, deploying, migrating, or changing permissions after only self-review when a fresh review was available.

## Verification

Before finishing, confirm:

- [ ] The claim and why-it-matters were stated.
- [ ] Artifact and contract were separated from reasoning.
- [ ] The review prompt was adversarial.
- [ ] The review method was named, including degraded fallback if used.
- [ ] External CLI was not run without explicit approval and isolation preflight.
- [ ] Every finding was classified as `contract gap`, `actionable`, `trade-off`, or `noise`.
- [ ] A stop condition was met.
- [ ] Remaining risks and next steps were stated.
