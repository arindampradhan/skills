# Skills

Personal collection of agent skills. Each folder is one skill with a `SKILL.md`;
install by copying the folder into `~/.pi/agent/skills/`, a project's `.pi/skills/`,
or `~/.claude/skills/`.

## Tek workflow (`../tek`)

The four-skill campaign pipeline from the tek technique — spec the work, loop one
item at a time, gate every refactor, and land waves in reviewable batches.

| Skill | What it does |
|---|---|
| `tek-spec` | Turn a goal into a prioritized task list where every item names its files and a numeric done criterion, committed before any agent work starts |
| `tek-loop` | Run exactly one iteration of an autonomous work loop: top item → implement behind gates → commit with evidence → stop |
| `tek-wave` | Execute one refactor wave — net-negative, parity-verified, committed with the two-number contract (LOC budget + parity proof) |
| `tek-integrate` | Forward-port main into the campaign line, batch waves into integration trunks, apply review findings as review-fix commits |

Includes `tek-wave/scripts/commit-gate.sh` — a pre-commit gate (parity, conventional
subject, net-negative LOC). Run `fingerprint`-style audits from the tek repo.

## Code review

| Skill | What it does |
|---|---|
| `ocd-reviewer` | Obsessive line-by-line review of a branch diff: magic strings, casing, naming, style, unused imports, CSS, import order |

## Planning & process

| Skill | What it does |
|---|---|
| `grill-me` | Relentlessly interview the user about a plan or idea until every decision branch is resolved |
| `send-to-opencode` | Send the current plan to opencode in the background and track its output in a log file |
| `command-pr-description` | Generate a short, skimmable, human-sounding PR description from the branch diff vs develop |

## Frontend & scaffolding

| Skill | What it does |
|---|---|
| `frontend-radio` | Answer frontend system-design interview questions with the RADIO framework plus an Excalidraw architecture diagram |
| `0-dollar-stack-project` | Scaffold a production-ready SaaS entirely on free-tier tools |

## Media & automation

| Skill | What it does |
|---|---|
| `narrate-browser-recording` | Add local, offline voice narration to a browser-use recording — dub its captions with a real macOS voice, no cloud TTS |
