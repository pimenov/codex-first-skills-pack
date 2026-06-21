# Skills Routing Appendix

Use installed skills when the user's request matches a skill's purpose. The
user does not need to name the skill exactly.

Recommended routing:

- "check the current docs", "how does this API work now", "latest SDK behavior"
  -> `source-driven-development`
- "what are we building", "write the spec", "define acceptance criteria"
  -> `spec-driven-development`
- "break this down", "make a plan", "prepare tasks", "next safe steps"
  -> `planning-and-task-breakdown`
- "work in small steps", "verify after each step", "avoid a big diff"
  -> `incremental-implementation`
- "this command fails", "debug this", "CI is red", "the app broke"
  -> `debugging-and-error-recovery`
- "prove it with a test", "guard this behavior", "bugfix with regression test"
  -> `test-driven-development`
- "review this diff", "is this ready", "check the PR"
  -> `code-review-and-quality`
- "design this API", "schema contract", "webhook/event/config/interface"
  -> `api-and-interface-design`
- "remove the old system", "migration", "deprecate", "sunset"
  -> `deprecation-and-migration`
- "challenge this", "are we fooling ourselves", "is this safe"
  -> `doubt-driven-review`

Before substantial edits, read the relevant `SKILL.md` fully and follow its
workflow. If multiple skills apply, use the smallest set that covers the task
and state the order.

Production, data, auth, billing, credentials, customer data, deploys, and
irreversible cleanup require explicit bounded approval before mutation.
