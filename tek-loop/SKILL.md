---
name: tek-loop
description: Run exactly one iteration of an autonomous work loop — pick the top open item, implement it behind verification gates, commit the outcome with evidence, then stop. Use as the per-iteration prompt for cron or while-true drivers, or when asked to "run one loop iteration".
---

# Tek Loop — one iteration, then stop

You are the loop body. The driver (cron, `while true`, scheduler) re-invokes you.
`TODO.md`, git history, and the evidence log are your only memory. **One item per
invocation — this is the entire contract.**

## The iteration

1. Read `TODO.md`. Pick the highest-priority open item. If the top item is vague,
   spend this iteration sharpening it into implementable shape (files-to-modify +
   numeric done criterion), commit as `docs(plan): spec Q<n>`, and STOP.
2. If it's a refactor item → load `tek-wave`; if it needs landing → `tek-integrate`.
3. Branch: `<campaign>/r<R>-<M>`. Implement behind the gates (verify, conventional,
   budget, net-negative).
4. Commit with a subject that states the **outcome/finding**, not the activity.
   Even a failed iteration commits: `fix: blocked on item <n> — <one-line reason>`.
5. Update `TODO.md`: flip the checkbox only if the item's numeric criterion was
   met THIS iteration with evidence; append one evidence-log line.
6. STOP. Do not take a second item.

## Hard rules

1. At least one NEW result, deeper finding, or disconfirmed assumption per
   iteration — restating what's known is a wasted iteration.
2. Every claimed number carries the command that produced it, run this iteration.
3. New discoveries become new TODO items, never scope creep.
4. If 3 consecutive iterations restated known findings, move one abstraction up:
   behavior → mechanism → counterfactual → generalization.
5. If hard-blocked (credentials, missing data, human decision), log
   `BLOCKED: <reason>` in TODO.md, commit, stop.

## Driver

```bash
while true; do pi -p "$(cat LOOP.md)"; sleep 30; done   # or cron every N minutes
```

The loop's speed comes from the driver; its quality comes from the gates; its
direction comes from you only at merge time.
