description: Emotional rhythm and pacing audit — scores each drafted chapter for tension level, identifies plateaus, sagging middles, premature peaks, and act-boundary misalignments. Outputs a tension arc chart (Mermaid xychart), a pacing plateau report, and a remediation task list. Read-only except when writing the chart file. Run after speckit.implement, before speckit.polish or speckit.export.
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

## Purpose

The **`speckit.pacing`** command audits the *emotional rhythm* of a draft manuscript. It scores each chapter on a 1‑10 tension scale, detects plateaus, sagging middles, premature peaks, and act‑boundary mis‑alignments, then produces a Mermaid tension‑arc chart and a remediation task list. The command is **read‑only** for source files; it only writes the chart output file.

## When to Use

- After `speckit.implement` has generated draft chapters and before you move on to polishing or exporting.
- When you need a quantitative view of tension flow across the whole story or a specific act/chapter range.
- To identify structural pacing problems that may require revising chapters (`speckit.revise`) or adjusting the story plan (`speckit.plan`).

## Usage

```bash
speckit.pacing [options]
```

*No arguments* – full pacing audit of all drafted chapters and generate the full tension‑arc chart.
`[CHAPTER_ID]` – audit a single chapter.
`[CHAPTER_ID]–[CHAPTER_ID]` – audit a contiguous range of chapters.
`chart` – output **only** the Mermaid chart (no remediation report).
`--act "Act label"` – limit the audit to a specific act (e.g. `--act "Act II"`).

## High‑Level Execution Flow (LLM Friendly)

1. **Pre‑checks** – run any `hooks.before_pacing` and verify required files exist.
2. **Resolve feature directory** – locate `FEATURE_DIR` (first sub‑folder under `specs/` or project root).
3. **Load core documents** – `plan.md`, `tasks.md`, all relevant `draft/*.md` files (or a scoped subset based on arguments). If the project is large and an index exists, query the index for tension‑bearing passages instead of loading every file.
4. **Score each chapter** – compute a tension score (1‑10) from conflict type, stakes, scene‑ending hook, dialogue subtext, pacing signals, and POV character emotional state. Calibrate scores against the act‑level expectations defined in `plan.md`.
5. **Detect problems** – apply the critical, warning, and info rules (sagging middle, premature peak, false plateau, closing‑hook failures, act mis‑alignment, etc.).
6. **Generate Mermaid chart** – write `FEATURE_DIR/pacing-arc.md` containing an `xychart-beta` block with chapter sequence vs. tension score, marking act boundaries.
7. **Build remediation list** – for each identified issue, create a concrete suggestion (e.g., add a subplot complication, move a high‑tension scene, insert a micro‑tension beat).
8. **Report** – output a concise summary including total chapters analyzed, issue counts, and next‑step recommendations.
9. **Post‑checks** – run any `hooks.after_pacing`.

The detailed steps below remain unchanged but are now preceded by this concise overview to guide the LLM.

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

Resolve `FEATURE_DIR` by reading the project structure: the first subdirectory inside `specs/` that contains project files. Fall back to project root if `specs/` does not exist.

Load:
- Required: `plan.md` (act structure, chapter list), `tasks.md` (scene intent)
- Required: all `draft/*.md` files in scope — abort if no draft files exist
- **Large project optimization** (if `.specify/index/` exists and project has >50 drafted chapters): instead of loading all `draft/*.md` simultaneously, query the index to retrieve tension-bearing passages per chapter. The index stores `chapter_id` and `act_phase` metadata on each chunk, which is sufficient to compute the tension arc without loading full chapter prose:
  ```
  python .specify/presets/fiction-book-writing/scripts/python/index.py query "conflict stakes tension threat revelation" --type draft --top 100
  ```
  Group returned chunks by `chapter_id`, derive a tension score from each group, then plot the arc. Fall back to full file loading for any chapter where the index returns fewer than 2 chunks.
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

