---
name: tek-integrate
description: Batch a finished wave into an integration trunk, forward-port main into the campaign line, and apply reviewer findings as review-fix commits. Use when a campaign round (simp/rN, refactor/rN, feature campaign) is ready to land, or when the campaign line has drifted from main.
---

# Tek Integrate — waves in, noise out, drift zero

Main sees *waves*, not commits: batch leaf work, land it in few reviewable
merges, and keep the campaign line current with main. Three practices,
in landing order.

## 1. Forwardport (run FIRST, every integration)

The campaign line must absorb main before main absorbs the campaign:

```bash
git checkout <campaign-trunk>            # e.g. simp/forwardport
git merge origin/main -m "Merge origin/main into <campaign-trunk>: forward-port N main commits"
# resolve, re-run the campaign's parity suites, then continue
```

Do this continuously — the standing branch exists so drift never accumulates.
Evidence: *"forward-port 220 main commits into the simplified tree"*.

## 2. Batch into an integration trunk

Per campaign, keep numbered trunks (`<campaign>/integration`, `-2`, `-3`…).
Merge the round's branches in one landing:

```bash
git checkout <campaign>/integration3
git merge --no-ff simp/r3-36 simp/r3-37 ... -m "integrate r3 waves 36-37 (N leaf commits, parity suites green)"
```

Rules:
- **All racing variants resolve here**: winner merges, losers are deleted
  (`git branch -D`), never half-merged.
- **One landing = one reviewable unit.** If a batch exceeds review budget,
  split into more trunks — don't trickle leaf commits to main.
- Parity suites re-run on the *integrated* tree, not just per-branch.

## 3. Human merge authority

The integrator (human or human-delegated) decides what touches main. Target
ratio: merges ≤ 15% of total commits. An agent may prepare the integration
commit; only the authority runs the merge to main.

## 4. Review-fix loop

Reviewer (human or bot) findings on a landing become commits, not threads:

```
review-fix(<scope>): restore BASE <behavior> in <files> — <finding reference>
```

Semantics: review-fix **restores baseline behavior** the sweep deviated from,
or applies an accepted suggestion. Every finding resolves to exactly one commit
or one TODO.md item — nothing stays open in chat.

## End-of-integration checklist

- [ ] forwardport merge done, campaign line current with main
- [ ] integrated tree passes all parity suites
- [ ] loser branches deleted; TODO.md evidence log updated
- [ ] main merge done by the authority, with the wave summary in the message
- [ ] review findings (if any) committed as review-fix or filed in TODO.md
