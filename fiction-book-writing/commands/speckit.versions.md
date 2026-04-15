---
description: Draft version management — list (version timeline for a chapter or all chapters), diff (narrative comparison between two versions of a chapter), log (cross-chapter revision history sorted by date), and tag (attach a label to a specific version for milestone tracking). Read-only except for tag mode.
handoffs:
  - label: Revise Chapter
    agent: speckit.revise
    prompt: Revise the chapter to fix checklist or continuity failures
    send: true
  - label: Polish Chapter
    agent: speckit.polish
    prompt: Run a final line-edit pass on the latest version
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* — list version timelines for all chapters (same as `list`)
- `list` — version timeline for all chapters
- `list [CHAPTER_ID]` — version timeline for a single chapter (e.g. `list A1.101`)
- `diff [CHAPTER_ID]` — narrative diff between the two most recent versions of a chapter
- `diff [CHAPTER_ID] [vA] [vB]` — narrative diff between two specific versions (e.g. `diff A1.101 v1 v3`)
- `log` — chronological revision history across all chapters
- `log [CHAPTER_ID]` — revision history for a single chapter
- `tag [CHAPTER_ID] [vN] [label]` — attach a milestone label to a version (e.g. `tag A1.101 v2 beta-reader-1`)

---

## Purpose

`speckit.versions` is the companion to `speckit.revise` and `speckit.polish`. Those commands produce versioned draft files; this command surfaces the history, compares what changed, and lets you mark milestones.

**Version model** (used by this command):

| File | Interpreted as | YAML `version` |
|---|---|---|
| `draft/A1.101_Awakening.md` | v1 — initial AI draft | `version: 1` |
| `draft/A1.101_Awakening_v2.md` | v2 — first revision | `version: 2` |
| `draft/A1.101_Awakening_v3.md` | v3 — polish pass | `version: 3` |

The YAML frontmatter in each file is the authority for metadata:
- `version` — integer version number
- `drafted` — date first drafted (present in all versions)
- `revised` — date last revised (added by speckit.revise)
- `polished` — date polished (added by speckit.polish)
- `constitution_version` — which constitution version governed this draft
- `actual_words` — word count of the prose in this version
- `tags` — milestone labels (written by this command's `tag` mode)

**Revision notes** (`<!-- REVISION NOTES vN -->` comment blocks) record the scope and rationale for each revision. This command reads them when available.

**Modes at a glance**:

| Mode | Purpose | Writes files? |
|---|---|---|
| `list` | Timeline of all versions per chapter — dates, word counts, what changed | No |
| `diff` | AI-narrated comparison of prose between two versions | No |
| `log` | Cross-chapter revision history sorted by date | No |
| `tag` | Attach a named milestone label to a specific version | Yes — YAML frontmatter only |

---

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_versions` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Setup and Mode Resolution

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Scan `FEATURE_DIR/draft/` for all `.md` files. If the directory does not exist or is empty: abort with `✗ No draft files found in FEATURE_DIR/draft/. Nothing to version.`

**Build the version registry**: group draft files by chapter stem. For each group:
- Identify the chapter ID and name from the filename (format: `{CHAPTER_ID}_{ChapterName}[_vN].md`)
- Sort versions: the file with no `_vN` suffix is v1; files with `_v2`, `_v3`, etc. follow numerically
- For each file: read the YAML frontmatter (`version`, `drafted`, `revised`, `polished`, `constitution_version`, `actual_words`, `tags`)
- For each file: scan for a `<!-- REVISION NOTES v[N]` comment block — extract the `Revision scope` and `Changes` lines if present

Parse `$ARGUMENTS` for mode and optional chapter ID / version specifiers:
- `list …` or *(empty)* → **Mode: List**
- `diff …` → **Mode: Diff**
- `log …` → **Mode: Log**
- `tag …` → **Mode: Tag**

---

## Mode: List

**Purpose**: Show the full version timeline per chapter. Read-only.

For each chapter (or the specified chapter if a chapter ID was given), output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  A1.101  Awakening                          Act I
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  v1   2026-03-10   3,200w   Initial draft              draft/A1.101_Awakening.md
  v2   2026-03-14   3,310w   +110w  Revised (CHR-002, STB-004, SCN-005, SEN-003)
                                                         draft/A1.101_Awakening_v2.md
  v3 ★  2026-03-18   3,295w   -15w  Polished             draft/A1.101_Awakening_v3.md
       [tags: beta-reader-1]
```

**Format rules:**
- Mark the current (highest) version with `★`
- If `polished:` is present in frontmatter: append `Polished` label
- If `revised:` is present: append `Revised (…)` with the revision scope codes from the REVISION NOTES block (e.g. `CHR-002, STB-004`)
- Show word count delta from the previous version (`+N w` or `-N w`)
- If `tags:` is present: show as `[tags: …]` on a second line
- If a version has `constitution_version` older than the current `constitution.md` version: flag with `⚠️ constitution mismatch` so the author knows a story bible update may affect this version

After all chapters:
```
Chapters: [N]  |  Total versions: [N]  |  Chapters with 2+ revisions: [N]  |  Chapters never revised (v1 only): [N]
```

---

## Mode: Diff

**Purpose**: Narrative comparison of prose between two versions of a chapter. Read-only.

### Diff Step 1 — Resolve version files

Identify the chapter from `$ARGUMENTS`. If no versions are specified, compare vN-1 (second-highest) to vN (highest). If only one version exists: output `ℹ️ Only one version exists for [CHAPTER_ID]. Nothing to diff.` and stop.

If specific versions were given (e.g., `v1 v3`): resolve to the corresponding files. If either file doesn't exist: abort with the expected filename.

### Diff Step 2 — Read REVISION NOTES block

Check whether the newer version file has a `<!-- REVISION NOTES v[N] -->` block. If so, extract and display it:

```
── Recorded revision notes (v[A] → v[B]) ─────────────────────────
[REVISION NOTES block content]
───────────────────────────────────────────────────────────────────
```

### Diff Step 3 — Narrative prose comparison

Read the full prose of both versions. Compare at the passage level — not a line diff, but a scene-aware analysis of what is meaningfully different:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DIFF: [CHAPTER_ID]  [ChapterName]
  Comparing: v[A] ([YYYY-MM-DD], [N]w)  →  v[B] ([YYYY-MM-DD], [N]w)
  Net word change: [+/- N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Structural changes
[What changed in scene structure, beats, or POV — "None" if unchanged.]

### Prose-level changes

  PASSAGE [N]:
    Location : [approximate position — e.g. "opening paragraph", "mid-scene at the market stall"]
    v[A] had : [1–3 sentence summary or direct quote of the older version]
    v[B] has  : [1–3 sentence summary or direct quote of the newer version]
    Effect    : [what the change accomplishes narratively or stylistically]

### Unchanged
[Brief confirmation — "Core scene structure, all dialogue, closing beat unchanged."]

### Assessment
[1–2 sentences: did the revision improve the flagged issues? Any new concerns introduced?]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Mode: Log

**Purpose**: Chronological revision history across all chapters (or a single chapter). Read-only.

From the version registry, collect all revision events — each versioned file with a `revised:` or `polished:` date in its frontmatter. Sort by date ascending.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  REVISION LOG  [STORY_TITLE]
  [If scoped: Chapter CHAPTER_ID only]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[YYYY-MM-DD]  A1.101  Awakening         v1 → v2   Revised  (CHR-002, STB-004, SCN-005, SEN-003)   +110w
[YYYY-MM-DD]  A1.102  The Crossing      v1 → v2   Revised  (CHR-003, SCN-002)                      -20w
[YYYY-MM-DD]  A1.101  Awakening         v2 → v3   Polished                                          -15w
[YYYY-MM-DD]  A2.201  The Market        v1 → v2   Revised  (SEN-001, STB-002)                      +45w

Total revision events: [N]
Chapters touched: [N] of [M] total
Average revisions per chapter: [X]
Most-revised chapter: [CHAPTER_ID] [Name] ([N] revision cycles)
```

If a versioned file has no REVISION NOTES block: note `[no revision notes — manual edit]`.

---

## Mode: Tag

**Purpose**: Attach a named milestone label to a specific version. This is the only mode that writes to a file.

**Use cases**: mark the version sent to a beta reader, submitted for critique, or representing a structural milestone — so you know exactly what state the chapter was in at that point.

### Tag Step 1 — Validate

Parse `$ARGUMENTS`: chapter ID, version specifier (`v1`, `v2`, etc.), and label string.
- If any of the three are missing: prompt for the missing value.
- Resolve the file: `draft/<CHAPTER_ID>_<ChapterName>[_vN].md` (v1 has no suffix)
- If the file does not exist: abort with the expected filename.
- Validate label: non-empty, no spaces (replace spaces with hyphens silently), max 40 characters.

### Tag Step 2 — Write tag

Read the file's YAML frontmatter. Look for an existing `tags:` field:
- If absent: add `tags: [label]` after the `version:` line
- If present as a list: append the new label
- If present as a scalar: convert to a list and append

Write back only the YAML frontmatter — do not touch the prose content.

### Tag Step 3 — Confirm

```
✓ Tagged: draft/A1.101_Awakening_v2.md
  Label added: beta-reader-1
  All tags on this version: [beta-reader-1]
```

---

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_versions` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.
