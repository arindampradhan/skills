---
name: narrate-browser-recording
description: "Add local, offline voice narration to a browser-use recording (record an action, compile it into a captioned video, then dub the captions with a real macOS voice)."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["browser-use", "ffmpeg", "ffprobe", "say"] },
        "install":
          [
            { "id": "ffmpeg", "kind": "brew", "package": "ffmpeg", "bins": ["ffmpeg", "ffprobe"], "label": "Install ffmpeg (Homebrew)" },
          ],
      },
  }
---

# Narrate Browser Recording

Turns a `browser-use` action recording into a video with a spoken voiceover, entirely
local — no cloud TTS, no API key. Uses macOS's `say` for speech synthesis and `ffmpeg`
to mux the audio into the compiled video, timed to match each caption/card.

## When to Use

The user asks to record a browser-use action (or already has one) and wants narration,
a voiceover, or "someone talking over it" added to the resulting video.

## Flow

1. **Record the action** with `browser-use` as normal (enable recording first if needed):

   ```bash
   browser-use recordings enable   # once, if not already on
   browser-use <<'PY'
   new_tab("https://example.com")
   # ...steps...
   PY
   ```

2. **Find the recording** and **write an edit brief** (`edit-brief.json` in the
   recording directory). See `browser-use video review --help` and the schema errors
   it raises for the exact fields — at minimum:

   ```json
   {
     "task": "One-line description of the task",
     "plan": ["Chapter 1", "Chapter 2"],
     "outcomes": ["What the recording demonstrates"],
     "privacy": { "reviewedFrames": ["0001.jpg", "0002.jpg", "..."] },
     "actions": [
       { "event": 1, "chapter": 0, "route": "Semantic label, not a URL", "narration": "Short caption" }
     ],
     "outcomeTitle": "Done"
   }
   ```

   - `event` is the 1-based index into `recording-summary.json`'s `events` list.
   - `narration` on an action must be ≤7 words and only set when the thought
     changes (the compiler rejects narration on 3+ consecutive actions, or on
     more than half the actions in one unbroken run).
   - List every reviewed frame under `privacy.reviewedFrames` (all `NNNN.jpg`
     files in the recording dir) — the compiler requires this as an explicit
     "a human looked at these" step.

3. **Compile and export**:

   ```bash
   browser-use video review "$RECORDING_DIR"
   browser-use video export "$RECORDING_DIR" --reviewed
   ```

   This produces `video.mp4` and `composition.js` in the recording directory.
   `composition.js` holds each beat's duration (`dur`) and its caption
   (`narration`, or `title`/`sub` for intro/outcome cards) — that's the timing
   source of truth for narration.

4. **Add narration** with this skill's script — it reads `composition.js`, walks
   the beats to compute each caption's start time, synthesizes each line locally
   with `say`, and muxes them into `video.mp4` at the right offsets:

   ```bash
   python3 ./scripts/narrate.py \
     --recording "$RECORDING_DIR" \
     --voice "Serena (Premium)"
   ```

   (path relative to this skill's own directory — adjust for wherever it's
   installed, e.g. `~/.claude/skills/narrate-browser-recording/scripts/narrate.py`)

   - Omit `--recording` to use the most recent recording
     (`browser-use recordings --latest`).
   - Output defaults to `<recording>/video-narrated.mp4`; override with `--output`.

5. **Send the result** to the user with `SendUserFile` (`display: "render"`).

## Voice Quality

The default macOS compact voices (Samantha, Alex, etc.) sound robotic. Before
narrating, check whether a **Premium** voice is installed:

```bash
say -v '?' | grep -i premium
```

If none is installed, macOS gates the download behind a GUI (no CLI hook to
trigger it):

```bash
open "x-apple.systempreferences:com.apple.preference.universalaccess?SpeechSynthesis"
```

Have the user go to **Accessibility → Vision → Read & Speak → System Voice →
Manage Voices...**, download a voice tagged **Premium** (e.g. Ava, Nathan, Zoe,
Serena), then re-run `say -v '?' | grep -i premium` to confirm before narrating.
Pass the exact installed name via `--voice`.

## Pitfalls

- `say -o file.aiff` — do **not** pass `--file-format`; it errors on this macOS
  version's `say`. Let it default to AIFF.
- In the ffmpeg `amix` filter, use `duration=longest`, not `duration=first`.
  `duration=first` truncates the whole mix to the length of the *first* listed
  audio input — since narration clips are added in the same order as their
  on-screen appearance, that silently cuts off every line after the first one.
- `apad=whole_dur=<seconds>` should match the video's total duration
  (`ffprobe -show_entries format=duration`), not any individual clip's length,
  so the audio track doesn't end early.
