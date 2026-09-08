---
name: tek-wave
description: Execute ONE refactor wave — a net-negative, parity-verified simplification of one module, committed with the two-number contract (LOC budget + parity proof). Use when simplifying/compressing a module, running a simplification campaign round, or before committing any refactor wave.
---

# Tek Wave — one refactor iteration, gated

Every refactor commit carries a two-number contract:

```
refactor(plugins/telegram): split send/inbound god methods into phase helpers,
drop dead code (8817->6578 LOC, 13073-case Bot API payload parity)
```

Number 1 proves **progress** (LOC went down). Number 2 proves **safety** (behavior
parity verified against baseline). Both must be in the message. Neither is optional.

## One wave = this exact sequence

1. **Pick one item** from `TODO.md` (top-down). One item. Never two.
2. **Branch**: `<campaign>/r<R>-<M>` for the round; `-X<k>`/`-W<k>` suffix for a
   racing experiment variant of the same objective (e.g. `simp/r3-36-X2`).
3. **Baseline the parity check FIRST**: run the module's test/parity suite before
   touching anything. If there is none, write the equivalence check before
   refactoring — deleting without a parity net is banned.
4. **Refactor**: delete dead code, dedupe paths, split god methods, compact docs.
   Every motion must be net-negative or parity-preserving.
5. **Gate** (script below): parity passes + net LOC ≤ 0 + conventional subject.
6. **Commit** with the two-number message. Update `TODO.md` (checkbox + evidence log line).

## Commit gate

```bash
./scripts/commit-gate.sh <repo> "<conventional subject>" [parity/test command]
```

Exit 0 = commit allowed. The script:
- runs the parity/test command (if given) — G1
- validates the subject against Conventional Commits — G2
- computes staged +/− and, for `refactor:` subjects, requires net ≤ 0 — G5
- prints the ready-made `(X->Y LOC)` budget string to paste into the message — G4

## Rules

1. **No refactor commit without both numbers.** If parity can't be stated as a
   checkable count ("13073-case payload parity"), build the check first.
2. **Wave ends when the item's numeric criterion is met** — then stop. Surplus
   ambition becomes a new TODO item, not scope creep.
3. **Racing variants** (`-X2`, `-W1`) are cheap: spawn them when one approach
   might not pan out; merge the winner, abandon the rest without ceremony.
4. **LOC budget per wave is a target**, e.g. "module 2653→≤2450". Write it in
   TODO.md before starting, not after counting.
5. **Review findings become `review-fix:` commits** that restore baseline
   semantics — never discussion threads.
