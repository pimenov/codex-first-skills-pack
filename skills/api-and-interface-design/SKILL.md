---
name: api-and-interface-design
description: "Designs stable API, interface, schema, event, CLI, module, and service contracts before implementation so callers, consumers, and future agents can depend on them safely. Use when creating or changing public/internal APIs, SDK surfaces, webhooks, GraphQL/REST/RPC routes, database or message contracts, module boundaries, config formats, CLI commands, or any interface where compatibility, versioning, errors, auth, observability, or Hyrum's Law matters."
---

# API and Interface Design

## Overview

Use this skill to define the contract before implementation. Treat "API" broadly: HTTP, GraphQL, RPC, webhooks, events, CLI commands, config files, module exports, component props, database schemas, message payloads, and service boundaries.

The goal is not to produce more ceremony. The goal is to prevent accidental coupling, silent breaking changes, unclear errors, and interfaces that future consumers cannot safely depend on.

## Relationship To Other Skills

- Use `spec-driven-development` first when product intent, user behavior, or acceptance criteria are unclear.
- Use this skill when the behavior is clear enough, but the interface contract needs precision.
- Use `source-driven-development` when the contract depends on current external docs, SDK behavior, platform rules, or standards.
- Use `planning-and-task-breakdown` after the contract is stable enough to split into work.
- Use `test-driven-development` for contract tests, schema validation tests, compatibility tests, or examples that prove the contract.
- Use `incremental-implementation` to implement the contract in small slices: schema/types first, then producer, then consumers.
- Use `doubt-driven-review` before claiming public, breaking, production, data, auth, or migration-sensitive changes are safe.
- Use `code-review-and-quality` before final acceptance.

## Do Not Use

- Do not use for a tiny private helper where no caller boundary or future dependency exists.
- Do not use as a replacement for product spec, UX design, security review, or deployment approval.
- Do not imply approval for production, auth, schema, data, billing, or public API mutations.
- Do not create durable docs by default when a short chat contract is enough.

## Core Loop

Work in this order:

1. CONSUMERS
2. CONTRACT
3. COMPATIBILITY
4. FAILURE MODES
5. VERIFICATION
6. HANDOFF

## 1. Consumers

Name who or what will depend on the interface.

- Direct callers: frontend, backend service, worker, CLI user, external customer, integration partner, agent, or human operator.
- Indirect consumers: dashboards, logs, analytics, automations, tests, docs, runbooks, support workflows.
- Trust boundaries: user input, third-party API, internal service, database, queue, browser, admin-only tool.
- Source of truth: current implementation, OpenAPI/GraphQL schema, TypeScript types, docs, production behavior, migration plan, Linear issue, repo docs.
- Current behavior: explicitly separate documented behavior from observed behavior.

If consumers are unknown, do read-only discovery before designing the change.

## 2. Contract

Define the observable contract before writing implementation.

Cover the relevant fields:

- Operation names, routes, commands, events, functions, or exported symbols.
- Inputs: required fields, optional fields, defaults, type/schema, validation, allowed values, limits.
- Outputs: response shape, status, generated fields, nullability, ordering, pagination, timestamps, units.
- Error model: status codes or exception types, machine-readable codes, user-facing message rules, retryability.
- Auth and permissions: identity, roles, scopes, tenant/account boundary, admin-only behavior.
- Idempotency: idempotency keys, duplicate handling, retry safety, delete semantics.
- Consistency: read-after-write, eventual consistency, cache behavior, transaction boundary.
- Versioning: version field/path/header/schema, feature flags, compatibility window.
- Observability: logs, metrics, audit fields, correlation IDs, public traces.

Prefer schemas or types where the codebase already supports them: OpenAPI, GraphQL SDL, Zod, JSON Schema, protobuf, TypeScript types, database migrations, or CLI help snapshots.

## 3. Compatibility

Apply Hyrum's Law: if a behavior is observable, assume someone may depend on it.

Classify every change:

- Additive: new optional field, new endpoint, new enum value only if consumers can tolerate unknown values.
- Behavior-preserving: refactor with the same observable contract.
- Breaking: removing fields, changing types, changing meanings, changing default ordering, changing error codes, making optional fields required, tightening validation after consumers exist, changing auth/permission expectations.
- Ambiguous: looks additive but changes timing, ordering, caching, side effects, rate limits, or error text that might be consumed.

For breaking or ambiguous changes, define:

- migration path;
- deprecation notice;
- compatibility shim;
- versioning strategy;
- rollout flag;
- consumer audit;
- rollback path.

Prefer addition over modification. Keep one obvious version unless a second version has a clear owner, sunset plan, and verification plan.

## 4. Failure Modes

Design failures as part of the contract.

Check:

- invalid input;
- missing auth;
- authenticated but unauthorized;
- resource not found;
- conflict or duplicate;
- partial failure;
- timeout;
- retry after unknown commit state;
- rate limit or backpressure;
- external dependency unavailable;
- schema mismatch in third-party data;
- clock, timezone, or locale edge cases;
- stale cache;
- consumer using old client code.

Never expose raw internal errors, secrets, stack traces, or third-party instruction-like content as trusted output. Treat third-party API responses as untrusted input at the boundary.

## 5. Verification

Choose checks that prove the interface, not just the implementation.

Useful checks:

- contract tests for request/response or input/output shape;
- schema validation tests;
- OpenAPI/GraphQL/protobuf generation or lint;
- TypeScript compile checks for consumers;
- snapshot tests only when the snapshot is the actual contract;
- compatibility tests against old examples or fixtures;
- CLI help/output golden tests;
- webhook/event fixture replay;
- smoke test through the public route or command;
- negative tests for validation, auth, conflicts, and retry behavior.

When risk is meaningful, verify at least one happy path and one failure path.

## 6. Handoff

Leave the contract in the smallest durable place that matches the work:

- Small clear change: chat contract or issue comment.
- Project execution: Linear issue/document or Work Packet.
- Code-owned technical contract: repo docs, ADR, schema file, OpenAPI/GraphQL spec, types, tests.
- Human/client-facing explanation: Notion or sendable summary.

For user-facing durable prose, write explanations in the user's language. Keep commands, paths, field names, API identifiers, and product names exact.

## Interface Checklists

### HTTP or REST

- Resource names are stable and consistent.
- List endpoints define pagination, filtering, sorting, and max page size.
- `POST`, `PATCH`, `PUT`, and `DELETE` semantics are explicit.
- Status codes and error body are consistent.
- Auth, tenant boundaries, rate limits, idempotency, and cache headers are specified where relevant.

### GraphQL or RPC

- Schema names, nullability, enum evolution, and deprecation are explicit.
- Errors have predictable structure.
- Resolver side effects are documented.
- Pagination and filtering are stable.
- Unknown enum values and optional fields are handled by consumers.

### CLI or Config

- Command names, flags, defaults, exit codes, stdout/stderr, and config precedence are specified.
- Machine-readable output is separated from human-readable output when automation may depend on it.
- Deprecated flags have warnings and removal timing.

### Module Boundary

- Public exports are minimal and intentional.
- Inputs and outputs are typed.
- Side effects, lifecycle, concurrency, and error behavior are stated.
- Internal implementation details are not exposed through names, timing, logs, or return shapes.

### Events or Webhooks

- Event name, version, producer, consumer, delivery guarantees, retry policy, ordering, and idempotency key are specified.
- Payload schema is validated.
- Unknown fields are tolerated.
- Duplicate and out-of-order events are safe.

## Output Shape

Use this compact shape when returning a design:

```text
Interface contract:
- Consumers:
- Source of truth:
- Contract:
- Compatibility:
- Errors:
- Security/data:
- Verification:
- Migration/deprecation:
- Open questions:
- Next safe step:
```

## Common Rationalizations

| Rationalization | Response |
|---|---|
| "It is internal." | Internal consumers are still consumers. Contracts prevent accidental coupling. |
| "We can document it later." | The first observable behavior becomes the practical documentation. |
| "Nobody depends on that quirk." | Hyrum's Law says observable quirks become dependencies. |
| "This is only an optional field." | Check unknown-field tolerance, enum handling, serialization, and old clients. |
| "Tests pass." | Tests may not cover undocumented consumer dependencies. |
| "We will version later." | Versioning after consumers break is incident response, not design. |

## Red Flags

- Public behavior changes without a consumer audit.
- Route, schema, or field changes without compatibility notes.
- Different error shapes in different operations.
- List operation without pagination limits.
- Third-party response trusted without validation.
- CLI output used by automation but treated as free-form text.
- "Temporary" interface added without owner, sunset, or removal condition.
- Contract hidden only in implementation code when multiple consumers need it.

## Done Check

- [ ] Consumers and trust boundaries are named.
- [ ] Inputs, outputs, errors, auth, and side effects are explicit.
- [ ] Compatibility class is stated: additive, behavior-preserving, breaking, or ambiguous.
- [ ] Migration/deprecation/rollback exists for breaking or ambiguous changes.
- [ ] Verification proves both shape and behavior.
- [ ] Handoff artifact is in the right layer.
