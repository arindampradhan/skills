---
name: tek-spec
description: Turn a goal into a prioritized task list where every item names its files and a numeric or test-defined done criterion, then commit it before any agent work starts. Use when starting a new campaign or before delegating work to agents.
---

# Tek Spec — write the plan before looping

Write the spec so an agent can execute it without asking questions: every item
names its files, its priority, and its machine-checkable done criterion.

## Output

A `TODO.md` in the project root with exactly this shape:

```markdown
# TODO — <campaign name>

## Goal
One sentence. Falsifiable. Prefer a number: "reduce X from A to B".

## Invariants (checked every iteration, never trade away)
- [ ] <test suite / build / behavior that must keep passing>

## Open items (work top-down; HIGH PRIORITY first)
- [ ] 1. HIGH: <task> **Files to modify:** <path1>, <path2> **Done when:** <machine-checkable criterion, ideally a number>
- [ ] 2. MED: <task> ... 

## Evidence log (append-only, one line per iteration)
| iter | item | finding/result | evidence (command / sha) |
```

## Rules

1. **Every item names the files to modify.** Vague items get sharpened first or split.
2. **Every item has a numeric or test-defined done criterion** ("8817→6578 LOC",
   "all tests pass", "p95 latency ≤ 200ms"). Prose done-criteria are banned —
   agents can't self-gate against prose.
3. **Priorities are explicit** (HIGH/MED/LOW); the loop works top-down.
4. **The spec fits in one file.** If it doesn't, it's a program, not a spec — split into campaigns.
5. Commit it immediately: `docs(plan): spec <campaign> — N items, numeric done criteria`.
