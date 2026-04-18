---
description: Prose statistics report — readability score, sentence length variance, passive voice %, adverb density, and dialogue balance (% dialogue vs. action/narration). Read-only. Run after speckit.implement or speckit.polish to get a quantitative picture of your prose at the sentence level.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
handoffs:
  - label: Polish Prose
    agent: speckit.polish
    prompt: Run the final line-edit pass to reduce adverb density, fix passive voice, and improve sentence rhythm
    send: false
  - label: Revise Chapter
    agent: speckit.revise
    prompt: Revise this chapter based on the statistics report findings
    send: false
  - label: Run Pacing Audit
    agent: speckit.pacing
    prompt: Run a pacing audit to check the emotional tension arc across chapters
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* — full statistics report across all drafted chapters
- `[CHAPTER_ID]` — scope to a single chapter (e.g. `A2.201`)
- `[CHAPTER_ID]–[CHAPTER_ID]` — scope to a chapter range (e.g. `A1.101–A1.103`)
- `--act [act label]` — scope to one act (e.g. `--act "Act II"`)
- `dialogue` — output only the dialogue balance report
- `readability` — output only readability and sentence-level metrics

---

## Purpose

`speckit.statistics` produces a quantitative prose health report at the sentence level. It answers: *how is the writing actually constructed?* — not whether the narrative arc is sound (that is `speckit.pacing`) or whether it complies with the story bible (that is `speckit.continuity`), but whether the prose itself reads well according to measurable craft signals.

**What it is NOT**:
- It does not fix anything — use `speckit.polish` or `speckit.revise` for that
- It does not check scene structure — use `speckit.checklist`
- It does not check tension arc — use `speckit.pacing`
- It does not check story bible compliance — use `speckit.continuity`

**Operating constraint**: STRICTLY READ-ONLY. No prose is modified.

---

## Metrics Reference

### Section A — Readability

| Metric | How it is computed | Target range |
|---|---|---|
| Flesch Reading Ease | Standard formula over the full chapter | 60–80 (literary fiction); 50–70 (dense/literary) |
| Flesch-Kincaid Grade Level | Grade level equivalent | 6–10 (general fiction); up to 12 for literary |
| Average sentence length | Total words ÷ total sentences | 12–18 words (vary by genre) |
| Sentence length variance | Standard deviation of sentence lengths | ≥6 = good variety; <4 = flat rhythm |
| Long sentence % | Sentences ≥35 words as % of total | Flag if >20% |
| Short sentence % | Sentences ≤6 words as % of total | Flag if <5% (no punchy rhythm) or >40% (staccato overload) |

**Rhythm health verdict**: GOOD / FLAT / STACCATO / WALL-OF-TEXT based on the combined pattern.

---

### Section B — Voice Signals

| Metric | Definition | Target |
|---|---|---|
| Passive voice % | Passive constructions as % of all sentences | ≤10%; flag if >20% |
| Adverb density | Adverbs ending in `-ly` per 1,000 words | ≤5 per 1k words; flag if >10 |
| Filter word count | Instances of `noticed`, `felt`, `saw`, `heard`, `thought`, `realized`, `wondered`, `seemed`, `appeared` | Flag if >3 per 500 words |
| Weak verb % | `was`, `were`, `had`, `got`, `began to`, `started to` as % of all verbs | ≤15%; flag if >25% |
| Hedge word count | `maybe`, `perhaps`, `somewhat`, `rather`, `quite`, `very`, `really`, `just` per 1,000 words | Flag if >8 per 1k |

**Voice strength verdict**: STRONG / MODERATE / WEAK based on combined passive + adverb + filter + weak verb signals.

---

### Section C — Dialogue Balance

Classify every paragraph as one of:

| Type | Definition |
|---|---|
| **Dialogue** | Any paragraph containing a spoken line (enclosed in quotation marks) including its attribution tag |
| **Action** | Paragraph containing physical beats, movement, or stage direction — no spoken line |
| **Narration** | Paragraph containing reflection, exposition, backstory, or internal monologue |

Report:
- Dialogue % / Action % / Narration % by word count and by paragraph count
- Chapter-level balance vs. genre target band (see below)
- Flag any stretch of 500+ consecutive words with zero dialogue in a scene marked as a confrontation, negotiation, or dialogue-heavy beat in `tasks.md`
- Flag any stretch of 500+ consecutive words with zero action in a scene marked as a chase, fight, or physical sequence in `tasks.md`

**Genre dialogue target bands** (derived from `constitution.md` genre field if present, else defaults):

| Genre | Dialogue target |
|---|---|
| Literary fiction | 20–40% |
| Commercial / thriller / mystery | 35–55% |
| Romance | 40–60% |
| Fantasy / sci-fi (world-heavy) | 20–45% |
| YA | 40–60% |
| Horror | 20–40% |

---

## Execution Steps

### Step 1 — Setup

Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

Load:
- Required: draft files in `FEATURE_DIR/draft/` matching the scope from `$ARGUMENTS`. Abort if none exist.
- Optional: `constitution.md` — read `GENRE`, `POV_MODE`, `STYLE_MODE`, and author rule overrides table (Section: Governance → Author Rule Overrides). Any overrides documented there suppress corresponding flags in this report.
- Optional: `tasks.md` — used to cross-reference scene intent for dialogue/action mismatch detection.

### Step 2 — Compute metrics per chapter

For each chapter in scope, compute all metrics in Sections A, B, and C.

Apply any Author Rule Overrides from `constitution.md` before flagging:
- If an override documents intentional high adverb use for a POV character's voice, suppress adverb density flags for that POV's chapters and add a note: `Adverb density: suppressed by Author Rule Override [character name]`.
- If passive voice is documented as a deliberate stylistic choice (e.g. bureaucratic deadpan register), suppress passive voice flags.

### Step 3 — Aggregate across scope

Compute scope-wide aggregates:
- Average and range for each metric across all chapters in scope
- Identify the highest and lowest performing chapters per metric
- Identify the chapter with the least sentence length variance (flattest rhythm)
- Identify the chapter with the highest passive voice % and highest adverb density

### Step 4 — Verdict per chapter

For each chapter, assign:
- **Readability verdict**: GOOD / FLAT / STACCATO / WALL-OF-TEXT
- **Voice verdict**: STRONG / MODERATE / WEAK
- **Dialogue balance verdict**: BALANCED / DIALOGUE-HEAVY / NARRATION-HEAVY / ACTION-HEAVY

### Step 5 — Report

Emit the full statistics report. Example format:

```
📊 Prose Statistics — [STORY_TITLE]
Scope: [chapter range or "All chapters"]  |  Chapters analyzed: N
Constitution genre: [genre]  |  Style mode: [mode]

═══════════════════════════════════════════════
 SECTION A — READABILITY
═══════════════════════════════════════════════

Chapter       | Flesch | Grade | Avg Sent | Variance | Rhythm
------------- | ------ | ----- | -------- | -------- | ------
A1.101        |  72    |  7.4  |   15.2   |   7.1    | GOOD
A1.102        |  58    |  9.8  |   21.4   |   3.2    | FLAT ⚠️
A2.201        |  81    |  6.1  |   12.0   |   8.9    | GOOD
...

Scope average Flesch:     N    Range: N–N
Scope avg sentence length: N   Range: N–N
Flattest rhythm chapter:   [ID] (variance N)
Most complex chapter:      [ID] (Grade N)

═══════════════════════════════════════════════
 SECTION B — VOICE SIGNALS
═══════════════════════════════════════════════

Chapter       | Passive% | Adverbs/1k | Filters/500 | Weak V% | Verdict
------------- | -------- | ---------- | ----------- | ------- | -------
A1.101        |   8%     |    4.2     |    1        |  12%    | STRONG
A1.102        |   24%    |   11.3     |    6        |  28%    | WEAK ❌
A2.201        |   11%    |    5.9     |    2        |  16%    | MODERATE
...

Highest passive voice:    [Chapter ID] at N%
Highest adverb density:   [Chapter ID] at N per 1k
Most filter words:        [Chapter ID] at N per 500 words

═══════════════════════════════════════════════
 SECTION C — DIALOGUE BALANCE
═══════════════════════════════════════════════

Chapter       | Dialogue% | Action% | Narration% | Balance verdict
------------- | --------- | ------- | ---------- | ---------------
A1.101        |   38%     |  28%    |   34%      | BALANCED
A1.102        |   12%     |  15%    |   73%      | NARRATION-HEAVY ⚠️
A2.201        |   61%     |  22%    |   17%      | DIALOGUE-HEAVY ⚠️
...

Genre target band ([genre]):  [N%–N%] dialogue
Scope average dialogue:       N%

═══════════════════════════════════════════════
 FLAGS
═══════════════════════════════════════════════

CRITICAL
  ❌ [Chapter ID] — [metric]: [one-line description]

WARNING
  ⚠️ [Chapter ID] — [metric]: [one-line description]

INFO
  ℹ️ [Chapter ID] — [note]

═══════════════════════════════════════════════
 RECOMMENDED NEXT STEPS
═══════════════════════════════════════════════
  1. [Highest-priority action — e.g. "A1.102: run speckit.polish — adverb density and passive voice both flagged"]
  2. [Second priority]
  3. [Third priority]
```

If no issues found:
```
✅ Statistics report: all chapters within target bands.
No readability, voice, or dialogue balance flags.
```

---

## Scope Interaction with `speckit.polish`

`speckit.polish` and `speckit.statistics` share some surface signals (adverb density, filter words, weak verbs). The distinction:

- `speckit.statistics` **measures and reports** — it tells you *how much* and *where*
- `speckit.polish` **finds and fixes** — it operates on the same signals but rewrites prose

Run `speckit.statistics` first to understand the scope of the problem, then hand off to `speckit.polish` for the targeted chapter. If a chapter's statistics verdict is STRONG across all metrics, it can skip the polish pass.
