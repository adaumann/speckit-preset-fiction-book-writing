---
description: Emotional rhythm and pacing audit — scores each drafted chapter for tension level, identifies plateaus, sagging middles, premature peaks, and act-boundary misalignments. Outputs a tension arc chart (Mermaid xychart), a pacing plateau report, and a remediation task list. Read-only except when writing the chart file. Run after speckit.implement, before speckit.polish or speckit.export.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
handoffs:
  - label: Revise Low-Tension Chapter
    agent: speckit.revise
    prompt: Revise this chapter to raise tension — apply the remediation suggestions from the pacing report
    send: false
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check after pacing revisions
    send: true
  - label: Fix Story Structure
    agent: speckit.plan
    prompt: The pacing audit exposed structural problems — revisit the plan
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* — full pacing audit of all drafted chapters + tension arc chart
- `[CHAPTER_ID]` — scope audit to a single chapter (e.g. `A2.201`)
- `[CHAPTER_ID]–[CHAPTER_ID]` — scope to a chapter range
- `chart` — output only the tension arc chart (no remediation report)
- `--act [act label]` — scope to one act (e.g. `--act "Act II"`)

---

## Purpose

`speckit.pacing` audits the emotional rhythm of drafted chapters: is tension rising where it should, plateauing where it must not, and releasing at structurally correct moments? It is the post-draft complement to `speckit.analyze` (which checks structural coverage pre-draft) — pacing works on prose reality, not plan intent.

**What it checks**:

| Check | What it catches |
|---|---|
| Tension score per chapter | Chapters with no tension movement (plateau) |
| Act-boundary alignment | Tension must peak at Act II close and climax, not before |
| Sagging middle | Three or more consecutive chapters below the story's baseline tension |
| Premature peak | Tension higher in Act I close than Act II midpoint |
| False plateau | Tension flat across two or more chapters without a deliberate breather beat |
| Recovery after valley | After a low-tension breather, does tension recover within one chapter? |
| Scene-ending hooks | Does each chapter end on a tension value ≥ the chapter's opening value? (off-balance ending rule) |

**Operating constraints**: STRICTLY READ-ONLY for source files. Only writes the chart output file. No prose modifications.

---

## Execution Steps

### Step 1 — Setup

Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

Load:
- Required: `plan.md` (act structure, chapter list), `tasks.md` (scene intent)
- Required: all `draft/*.md` files in scope — abort if no draft files exist
- Optional: `spec.md` (central dramatic question, emotional arc intent), `constitution.md` (style mode — affects expected tension baseline)

### Step 2 — Score each chapter

For each drafted chapter in scope, derive a **tension score (1–10)** by evaluating:

| Signal | Tension indicator |
|---|---|
| Conflict type | Physical > social > internal > reflective (descending tension) |
| Stakes at scene end | New threat or revelation raised → +2; stakes resolved → −2 |
| Scene ending hook | Off-balance ending (unresolved want) → +1; closed ending → −1 |
| Dialogue subtext | High-conflict subtext → +1; expository dialogue → −1 |
| Pacing signals | Short sentences dominating → +1; long reflective passages → −1 |
| Emotional state of POV character | Highest-stress state in the scene → +1 per escalation |

Floor: 1 (zero-tension breather scene). Ceiling: 10 (climax/darkest moment).

**Calibration against act structure** (from `plan.md`):

| Act position | Expected tension band |
|---|---|
| Act I (setup) | 3–5 rising to 6 at Act I close |
| Act II-A (rising stakes) | 5–7, midpoint at 7–8 |
| Act II-B (darkest) | 7–9, closing at 9–10 |
| Act III (climax + resolution) | 10 at climax, falling to 3–4 at resolution |

Flag any chapter whose score is outside its expected band by ≥2 points.

### Step 3 — Detect problems

Apply these rules to the scored sequence:

**CRITICAL**:
- Three or more consecutive chapters scored ≤4 outside Act I setup or post-climax resolution → **sagging middle**
- Tension at Act I close (last chapter of Act I) scored lower than Act I chapter 3 → **structure inversion**
- Climax chapter scored below 8 → **undersold climax**
- Final chapter before Act II midpoint scored higher than midpoint chapter → **premature peak**

**WARNING**:
- Two consecutive chapters with identical score → **false plateau**
- Any chapter ending on a lower tension score than it opened → **closing hook failure**
- After a chapter scored ≤3 (breather), next chapter still ≤3 → **failed recovery**
- Any chapter whose score is outside its expected act band by 2+ points → **act misalignment**

**INFO**:
- One chapter with score ≤3 at a structurally appropriate moment (post-climax, mid-act breather) → breather (acceptable)
- Scene-ending hooks present but weak (closed ending, low subtext) → note for polish pass

### Step 4 — Generate tension arc chart

Output a Mermaid `xychart-beta` block mapping chapter sequence number → tension score. Mark act boundaries with a comment line. Write to `FEATURE_DIR/pacing-arc.md`:

````markdown
# Tension Arc: [STORY_TITLE]

<!-- Generated by speckit.pacing — [DATE] -->
<!-- Edit scores manually if AI scoring diverges from your intent, then add a note. -->

```xychart-beta
title "Tension Arc — [STORY_TITLE]"
x-axis ["Ch1", "Ch2", "Ch3", ...]
y-axis "Tension (1–10)" 1 --> 10
line [score1, score2, score3, ...]
```

| Chapter ID | Title | Score | Act | Flag |
|---|---|---|---|---|
| A1.101 | ... | N | Act I | ✓ / ⚠️ / ❌ |
````

If a chapter range was scoped in `$ARGUMENTS`, output only that range in the chart. Add a note: `Partial view — full arc requires all chapters.`

### Step 5 — Build remediation list

For each CRITICAL and WARNING item, generate a concrete remediation suggestion:

| Problem | Suggested fix |
|---|---|
| Sagging middle | Introduce a subplot complication or revelation in the flattest chapter |
| Premature peak | Move the high-tension scene later, or reduce its stakes to a WARNING level |
| Closing hook failure | Add an unanswered question or new threat in the chapter's final paragraph |
| False plateau | Insert a micro-tension beat (a character discovery, a ticking clock) between the two flat chapters |
| Act misalignment | Flag for `speckit.plan` review — the chapter may be in the wrong act position |
| Undersold climax | Flag for `speckit.revise` — the climax scene needs higher stakes language and shorter sentence rhythm |

### Step 6 — Report

```
📈 Pacing Audit — [STORY_TITLE]
Chapters analyzed: N  |  Act coverage: [Acts listed]
Chart: FEATURE_DIR/pacing-arc.md

Tension arc summary:
  Baseline (Act I avg):       N.N
  Peak (highest score):       N — [Chapter ID]
  Valley (lowest score):      N — [Chapter ID]
  Climax chapter score:       N

Issues found: N CRITICAL · N WARNING · N INFO

CRITICAL
  ❌ [Chapter range] — [problem name]: [one-line description]

WARNING
  ⚠️ [Chapter ID] — [problem name]: [one-line description]

INFO
  ℹ️ [Chapter ID] — [note]

Recommended next steps:
  1. [Highest priority remediation]
  2. [Second priority]
```

If no issues found:
```
✅ Pacing audit passed — tension arc is structurally sound.
Chart saved to FEATURE_DIR/pacing-arc.md
```
