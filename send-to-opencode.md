---
name: send-to-opencode
description: Send the current plan to opencode in the background and track output in a log file. Saves contextual plans to a file if needed, then runs `opencode run -f <file> &` redirecting output to ~/.claude/plans/opencode-run-<ts>.log so Claude is not blocked.
---

# Send Plan to Opencode

When the user invokes `/send-to-opencode`:

## Step 1: Resolve the plan file

Run:
```bash
ls -t ~/.claude/plans/*.md 2>/dev/null | head -1
```

- **File found**: use it as the plan file. Proceed to Step 2.
- **No file found**: extract the agreed plan from the current conversation context — include the approach, all steps, files to modify, and verification method — and write it to `~/.claude/plans/send-to-opencode-$(date +%s).md` using the Write tool. Proceed to Step 2.

## Step 2: Preview

Read the resolved plan file. Show the user:
- The absolute file path
- The first 15 lines of content

Proceed immediately without waiting for confirmation.

## Step 3: Launch opencode in the background

Read the plan file content first, then embed it directly in the message (avoids `-f` flag parsing issues). Pipe output through `sed` to strip ANSI escape codes so the log file is clean plain text:

```bash
PLAN_FILE="<absolute-plan-file-path>"
LOG="$HOME/.claude/plans/opencode-run-$(date +%s).log"
# Export avoids quoting issues when the plan content contains quotes or special chars
export OPENCODE_PROMPT="Implement the following plan exactly as described:

$(cat "$PLAN_FILE")"
nohup bash -c 'opencode run "$OPENCODE_PROMPT" 2>&1 | sed '"'"'s/\x1b\[[0-9;]*[mGKHFABCDJsu]//g; s/\x1b(B//g'"'"'' > "$LOG" &
OPENCODE_PID=$!
echo "PID: $OPENCODE_PID"
echo "Log: $LOG"
```

## Step 4: Report back

Tell the user:
- The background PID
- The log file path
- The exact `tail -f <log>` command they can paste into a terminal to watch progress live
- That Claude is unblocked and they can keep working
