#!/usr/bin/env bash
# commit-gate.sh — the Tek wave gate (G1 verify, G2 conventional, G4 budget, G5 net-negative)
# usage: commit-gate.sh <repo> "<conventional subject>" [parity-or-test-command]
set -euo pipefail

REPO="${1:?usage: commit-gate.sh <repo> \"<subject>\" [parity-command]}"
SUBJECT="${2:?usage: commit-gate.sh <repo> \"<subject>\" [parity-command]}"
VERIFY="${3:-}"

cd "$REPO"

# G2: conventional subject
if ! echo "$SUBJECT" | grep -qE '^(feat|fix|test|refactor|docs|chore|perf)(\([a-z0-9_/-]+\))?: .+'; then
  echo "GATE FAIL G2: subject not conventional: '$SUBJECT'" >&2
  exit 2
fi

# G1: verify (tests/parity) — the parity command must pass before anything else
if [ -n "$VERIFY" ]; then
  echo "G1: running: $VERIFY" >&2
  bash -c "$VERIFY" || { echo "GATE FAIL G1: verify command failed" >&2; exit 1; }
fi

# Staged diff accounting (G4/G5)
read -r add del <<< "$(git diff --cached --numstat \
  | awk -F'\t' '$1 ~ /^[0-9]+$/ {a+=$1; d+=$2} END {print a+0, d+0}')"
net=$((add - del))
staged=$(git diff --cached --name-only | grep -c . || true)
[ "$staged" -gt 0 ] || { echo "GATE FAIL: nothing staged" >&2; exit 3; }

echo "staged: +$add/-$del (net $net) across $staged files"

# G5: net-negative for refactors
case "$SUBJECT" in
  refactor:|refactor\(*)
    if [ "$net" -gt 0 ]; then
      echo "GATE FAIL G5: refactor is net-positive (+$net). Delete more or reclassify." >&2
      exit 5
    fi
    ;;
esac

# G4: emit the budget-string template for the commit message.
# NOTE: Tek's budgets are MODULE sizes (2653->2437), not diff stats.
if echo "$SUBJECT" | grep -q '^refactor'; then
  echo "G4: measure module LOC before/after, then use this template:"
  echo "    (<before-module-LOC>-><after-module-LOC> LOC, <parity proof: N-case parity passed>)"
  echo "G4 measure: git show <baseline-sha>:<module-files> | wc -l   vs   wc -l <module-files>"
fi

echo "GATE: PASS"
