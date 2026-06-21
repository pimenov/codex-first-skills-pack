---
name: deprecation-and-migration
description: "Plans safe deprecation, migration, sunset, replacement, and removal of old systems, APIs, features, schemas, flags, cron jobs, integrations, configs, libraries, UI flows, and operational processes. Use when retiring legacy code, replacing an implementation, removing a public/internal interface, migrating consumers, consolidating duplicate systems, deciding maintain-vs-sunset, writing deprecation notices, proving zero usage before deletion, or when Hyrum's Law, compatibility, rollback, data safety, production risk, or consumer communication matters."
---

# Deprecation and Migration

## Overview

Deprecation is not deletion. It is the managed transfer of consumers from old behavior to a safer replacement, followed by evidence-backed removal.

Use this skill to avoid two common failures: keeping legacy systems forever because nobody owns the migration, or deleting "unused" behavior that still has hidden consumers.

## Relationship To Other Skills

- Use `context-engineering` first when the source of truth, owner, live state, or relevant docs are unclear.
- Use `source-driven-development` when migration depends on current vendor docs, SDK changes, platform deprecations, version support, or external API behavior.
- Use `api-and-interface-design` when the deprecated surface is an API, schema, event, CLI, config format, or module boundary.
- Use `spec-driven-development` when the desired replacement behavior or success criteria are unclear.
- Use `planning-and-task-breakdown` to turn the migration into waves, issues, owners, gates, and Definition of Done.
- Use `incremental-implementation` to migrate one consumer or slice at a time.
- Use `test-driven-development` for compatibility tests, migration fixtures, adapter checks, and regression guards.
- Use `doubt-driven-review` before irreversible removal, public deprecation deadlines, production cleanup, data migrations, auth changes, or claims that rollback is safe.
- Use `code-review-and-quality` before accepting removal diffs.

## Do Not Use

- Do not use to justify cleanup without consumer evidence.
- Do not remove production, data, secrets, auth, DNS, billing, cron, routing, webhooks, integrations, or public interfaces without explicit approval.
- Do not assume code is unused because local search found no references.
- Do not create a migration plan if there is no replacement, owner, or rollback path. Return a no-go instead.
- Do not turn every tiny private refactor into a formal migration plan.

## Core Loop

Work in this order:

1. INVENTORY
2. DECISION
3. REPLACEMENT
4. MIGRATION PLAN
5. ROLLOUT
6. REMOVAL READINESS
7. HANDOFF

## 1. Inventory

Identify what is being deprecated and who depends on it.

Capture:

- Artifact: code path, route, API, schema, feature flag, workflow, cron, integration, library, config, UI, document, or operational process.
- Owner: team, person, repo, service, project, or "unknown".
- Current state: active, deprecated, zombie, duplicate, broken, experimental, replaced, or unknown.
- Consumers: direct callers, imports, database references, events, dashboards, docs, automations, tests, operators, external customers, partners, agents.
- Evidence sources: `rg`, dependency graph, logs, metrics, tracing, analytics, GitHub search, Linear/Notion docs, production config, support history, runbooks, live smoke.
- Risk surfaces: data loss, auth/permission changes, billing, public API, partner integration, SEO, notifications, scheduled jobs, backups, audit trail.

If the owner or consumers are unknown, start read-only discovery and do not propose removal yet.

## 2. Decision

Choose the correct posture.

Use these outcomes:

- Maintain: the old system still has unique value or migration cost exceeds maintenance risk.
- Freeze: stop adding new features while measuring usage and preparing replacement.
- Advisory deprecation: migration is recommended, no hard removal date yet.
- Compulsory deprecation: removal has a deadline because risk or cost is high enough.
- Emergency disablement: immediate safety issue; use incident handling and explicit approval.
- Remove now: only when zero usage and rollback/evidence are clear.

For each decision, state:

- why now;
- who owns the migration;
- what happens if nothing changes;
- what evidence would change the decision;
- what must not be touched.

## 3. Replacement

Never deprecate critical behavior without a usable target.

Check replacement readiness:

- covers critical old use cases;
- preserves required compatibility or explicitly changes behavior;
- has docs or examples for consumers;
- has tests or smoke checks;
- has operational ownership;
- has observability for migration progress;
- has rollback or compatibility shim;
- has known gaps documented.

If the replacement is not ready, output "No-go: replacement not ready" and list the smallest safe next step.

## 4. Migration Plan

Plan migration around consumers, not around files.

Define:

- consumer list and priority;
- migration waves: canary, low-risk, main, stragglers, final removal;
- compatibility strategy: adapter, dual-write, read-through, feature flag, redirect, alias, shim, versioned API, or manual process;
- communication: who needs notice, where it lives, what date or condition matters;
- verification: tests, logs, metrics, search, dashboards, smoke, old-client fixtures;
- rollback: how to restore old behavior or pause the wave;
- stop-lines: metrics, errors, consumer objections, missing owner, data mismatch.

Prefer moving one consumer at a time. If the old and new systems run in parallel, define how divergence is detected.

## 5. Rollout

Migrate incrementally and keep evidence.

During rollout:

- migrate a small safe consumer first;
- verify old and new behavior against the contract;
- watch errors, latency, volume, data parity, and support signals;
- update docs and notices as reality changes;
- keep old path available until removal readiness is proven;
- record what changed and what stayed untouched.

For production-adjacent systems, separate read-only discovery from mutation. A deprecation plan is not approval to execute the removal.

## 6. Removal Readiness

Removal requires positive evidence, not just lack of local references.

Before deleting:

- verify zero active usage through appropriate live evidence;
- search code, configs, docs, tests, dashboards, runbooks, jobs, queues, and deployment settings;
- check imports and dependency graphs where possible;
- check logs/metrics over a relevant time window;
- confirm no external consumer still has access or contractual expectation;
- confirm backups, rollback, or restore path;
- define exact files/services/data/config to remove;
- define exact checks after removal.

If evidence is incomplete, downgrade to advisory deprecation, add instrumentation, or create a follow-up task.

## 7. Handoff

Store the plan in the smallest durable layer that matches risk:

- Chat-only: tiny internal cleanup with no consumers and no live risk.
- Linear issue/document or Work Packet: project execution, waves, approvals, and owners.
- Repo docs, ADR, migration guide, or runbook: code-owned technical migration.
- Notion: human/client-facing explanation, operating procedure, or reusable knowledge.
- local notes: internal sandbox evidence and repeatable checklist.

For user-facing durable prose, write explanations in the user's language. Keep commands, paths, field names, API identifiers, dates, versions, and product names exact.

## Deprecation Notice Shape

Use this compact shape when drafting a notice:

```text
Deprecation notice:
- Deprecated surface:
- Replacement:
- Status:
- Reason:
- Affected consumers:
- Migration steps:
- Verification:
- Deadline or removal condition:
- Support/owner:
- Rollback/exception path:
```

## Migration Plan Shape

Use this shape when returning a plan:

```text
Migration plan:
- Goal:
- Current surface:
- Replacement:
- Consumers:
- Evidence:
- Decision:
- Waves:
- Compatibility strategy:
- Stop-lines:
- Verification:
- Approval gates:
- Removal readiness:
- Next safe step:
```

## Patterns

### Adapter

Keep the old interface while routing it to the new implementation. Use when consumers are hard to change quickly.

### Feature Flag

Move consumers by cohort or tenant. Use when rollback needs to be fast and behavior can coexist.

### Strangler

Route traffic from old to new gradually. Use for services, routes, and workflows where parallel operation is possible.

### Dual-Write Or Shadow Read

Compare old and new outputs before switching authority. Use carefully for data systems; define reconciliation and rollback first.

### Alias Or Redirect

Preserve old names while pointing to new names. Use for CLI commands, config keys, URLs, or package exports when compatibility matters.

## Zombie Code

Zombie code has active consumers but no owner. Do not delete it casually.

Classify it as one of:

- assign owner and maintain;
- instrument and measure;
- wrap with compatibility boundary;
- migrate consumers;
- remove after proven zero usage.

If nobody can own the migration, surface that as the blocker.

## Common Rationalizations

| Rationalization | Response |
|---|---|
| "Search found no references." | Local search is one evidence source, not proof of zero usage. Check runtime/config/docs where relevant. |
| "It still works." | Working unowned code can still create security, upgrade, and onboarding risk. Compare maintenance cost to migration cost. |
| "Users will migrate themselves." | Consumers need tooling, docs, incentives, deadlines, or owned migration work. |
| "We can keep both forever." | Two systems double testing, docs, incident surface, and cognitive load. |
| "The replacement is better." | Better is not enough. It must cover critical use cases or have explicit behavior changes. |
| "We can rollback if needed." | Name the exact rollback step and prove it before removal. |

## Red Flags

- Deprecation without owner.
- Replacement not production-proven for critical use cases.
- Deadline without migration tooling or support path.
- Removing public behavior without consumer audit.
- Active warnings for months with no migration progress.
- No metric or log that can prove migration completion.
- Cleanup bundled with unrelated refactor or deploy.
- Data deletion hidden inside migration.
- Deprecated system still receiving new features.

## Done Check

- [ ] Deprecated surface, owner, and consumers are named.
- [ ] Evidence sources and gaps are explicit.
- [ ] Decision posture is stated: maintain, freeze, advisory, compulsory, emergency, or remove now.
- [ ] Replacement readiness is proven or the plan is marked no-go.
- [ ] Migration waves, stop-lines, and rollback are defined.
- [ ] Removal readiness uses positive evidence over a relevant window.
- [ ] Approval gates are explicit for production, data, auth, public API, or external systems.
- [ ] Final state is recorded in the correct durable layer.
