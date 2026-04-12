# Spec Kit Fiction Book Writing Preset

**Version 1.3.0** 


Spec Kit Version: >= 0.5.0 : (https://github.com/github/spec-kit)

A Spec-Driven Development preset purpose-built for novel and long-form fiction writing with single POV or multi POV. It replaces software engineering terminology with storytelling craft: features become story elements, specs become story briefs, plans become story structures, and tasks become scene-by-scene writing tasks.

Can write full prose or stays with book story outlines in order to write your own prose against the structure.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Commands Reference](#commands-reference)
- [Templates Reference](#templates-reference)
- [Tutorials](#tutorials)
  - [Single POV Novel](#tutorial-single-pov-novel)
  - [Multi-POV Novel](#tutorial-multi-pov-novel)
  - [The Planning Process](#the-planning-process)
  - [Analyze Before You Draft](#analyze-before-you-draft)
  - [Drafting Scenes with Tasks](#drafting-scenes-with-tasks)
  - [Checklist, Polish & Revise](#checklist-polish--revise)
  - [Processing Feedback](#processing-feedback)
  - [Query Letter & Export](#query-letter--export)
- [Workflow Sequence Diagram](#workflow-sequence-diagram)
- [POV Modes Reference](#pov-modes-reference)
- [Plot Structure Support](#plot-structure-support)
- [Style Modes](#style-modes)
- [Export Formats](#export-formats)

---

## Overview

The Fiction Book Writing preset applies the Spec-Driven Development methodology to creative fiction. It provides:

- **17 AI commands** covering every stage from idea to submission-ready manuscript
- **21 templates** for all supporting story documents
- **1 export script** (pandoc-based) for DOCX, EPUB, and LaTeX output
- Support for **8 POV modes** (single, alternating, dual, braided, ensemble, mosaic, frame, chorus, first-person-multiple)
- Support for all major **plot structure frameworks** (Three-Act, Save the Cat, Hero's Journey, Story Circle, etc.)
- Two **style modes**: author voice sample extraction or humanized AI prose principles

The central philosophy: the **story bible** (`constitution.md`) is the governing authority. Every drafted scene, every revision, every checklist gate derives its rules from it.

---

## Prerequisites

Before using this preset, ensure you have the following installed and configured:

| Requirement | Version | Notes |
|---|---|---|
| [Spec Kit](https://github.com/github/spec-kit) | >= 0.5.0 | Core tooling — install via `uv tool install specify-cli` |
| A supported AI coding agent | — | GitHub Copilot, Claude Code, Cursor, Gemini CLI, or [any other supported agent](https://github.com/github/spec-kit#-supported-ai-agents) |
| [Python](https://www.python.org/downloads/) | 3.11+ | Required by the Specify CLI |
| [uv](https://docs.astral.sh/uv/) | latest | Package manager used to install Specify CLI |
| [Git](https://git-scm.com/downloads) | any | Required by Spec Kit for branch and feature management |
| [pandoc](https://pandoc.org/installing.html) | >= 2.11 | Required only for `speckit.export` (DOCX, EPUB, LaTeX output) |

See the [Spec Kit Prerequisites](https://github.com/github/spec-kit#-prerequisites) for full details on installing and configuring the core toolkit.

---

## Quick Start

```bash
# 1. Install Spec Kit and apply the preset
specify init --preset fiction-book-writing

NOTE: The preset is in development and not officially in catalog of SpecKit. You need to clone it via git or from archive:

specify preset add --dev /path/to/your-preset
specify preset add --from https://github.com/adaumann/speckit-preset-fiction-book-writing/archive/refs/tags/v1.3.0.zip

# 2. Create your story bible first
/speckit.constitution

# 3. Write your story idea as a brief
/speckit.specify A reluctant librarian discovers her small town's founding myth is a cover story for her ancestor's crimes — and the only witness is still alive.

# 4. Clarify ambiguities before planning
/speckit.clarify

# 5. Build the story structure
/speckit.plan

# 6. Design POV architecture (skip for single POV)
/speckit.pov draft

# 7. Generate scene tasks
/speckit.tasks

# 8. Run pre-draft structural check
/speckit.analyze

# 9. Generate editable scene outlines (optional but recommended)
/speckit.outline all
# → review outlines/, edit beats, set status: APPROVED or status: SKIP

# 10. Start drafting (AI prose for APPROVED; skips SKIP chapters)
/speckit.implement

# 11. Check prose quality chapter by chapter
/speckit.checklist
/speckit.polish
```

---

## Project Structure

After initialization, your project will have this layout:

```
.specify/
  memory/
    constitution.md        ← Story Bible (governing authority)
  features/
    <story-slug>/
      spec.md              ← Story brief (logline, arcs, beats)
      plan.md              ← Story structure (acts, chapters)
      tasks.md             ← Scene-by-scene writing tasks
      pov-structure.md     ← POV architecture (multi-POV)
      characters/
        index.md           ← Character roster
        <character>.md     ← Per-character profiles
      world-building.md    ← Setting rules and world systems
      timeline.md          ← Chronology and elapsed time
      research.md          ← Open questions and source notes
      subplots.md          ← Subplot beat sheets
      themes.md            ← Thematic contract and motif registry
      glossary.md          ← Consistency reference (invented terms)
      locations.md         ← Canonical location reference
      series-bible.md      ← Series-level canon (multi-book)
      outlines/
        <CHAPTER_ID>_<Title>-outline.md  ← Scene outline (status: DRAFT/APPROVED/SKIP)
      draft/
        <CHAPTER_ID>_<Title>.md        ← Chapter draft
        <CHAPTER_ID>_<Title>_v2.md     ← Revised version
        <CHAPTER_ID>_<Title>_polished.md
      checklists/
        <CHAPTER_ID>_<Title>-checklist.md
      feedback/
        feedback.md        ← Beta/editorial feedback log
      synopsis.md          ← Query-ready synopsis
      query-letter.md      ← Submission query letter
```

---

## Commands Reference

### Story Development

| Command | Phase | What It Does |
|---|---|---|
| `speckit.constitution` | Setup | Create or update the story bible: style mode, plot structure, craft principles |
| `speckit.specify` | Concept | Turn a free-text idea into a structured story brief with logline, character arcs, and scene beats |
| `speckit.clarify` | Concept | Detect and resolve ambiguities in `spec.md` (motivation gaps, timeline issues, POV holes) |
| `speckit.plan` | Structure | Build the act/phase breakdown and chapter map from `spec.md` and `constitution.md` |
| `speckit.pov` | Structure | Design and audit multi-POV architecture, generate POV schedule, validate information asymmetry |
| `speckit.tasks` | Pre-draft | Generate scene-by-scene writing tasks ordered by act and character arc |
| `speckit.outline` | Pre-draft | Generate editable per-scene outline files from `plan.md`; authors approve or skip before AI drafts |
| `speckit.analyze` | Pre-draft | Read-only structural alignment check (spec↔plan↔tasks coverage, act proportions) |

### Drafting & Quality

| Command | Phase | What It Does |
|---|---|---|
| `speckit.implement` | Drafting | Draft scenes and chapters by executing tasks in order from `tasks.md` |
| `speckit.checklist` | Quality | Generate per-scene quality checklists (triple purpose, off-balance endings, dialogue subtext, sensory detail) |
| `speckit.continuity` | Quality | Post-draft analysis: story bible compliance, character arc consistency, timeline coherence |
| `speckit.revise` | Revision | Surgically rewrite only the failing passages identified by checklist or continuity |
| `speckit.polish` | Polish | Final line-edit pass: rhythm, filter words, adverb density, voice register, repetition |

### Post-Draft

| Command | Phase | What It Does |
|---|---|---|
| `speckit.feedback` | Revision | Ingest beta reader or editor notes, categorize issues, generate prioritized revision tasks |
| `speckit.status` | Monitoring | Read-only project dashboard: word counts, chapter status, outstanding quality gates |
| `speckit.query` | Submission | Generate a 250–350 word query letter with hook, body, comp titles, and submission tracker |
| `speckit.export` | Submission | Export manuscript to DOCX (Word), EPUB (KDP/IngramSpark), or LaTeX via pandoc |

---

## Templates Reference

| Template | Purpose |
|---|---|
| `scene-outline-template.md` | Per-scene outline: opening hook, causal beat sequence, character beats, dialogue requirements, sensory anchors, thematic work, status gate |
| `spec-template.md` | Story brief: logline, character arcs, Given/When/Then scene beats, plot requirements |
| `plan-template.md` | Story structure: story bible check gates, act/phase breakdown, chapter map |
| `tasks-template.md` | Scene tasks: organized by act and arc, with research phase and polish pass |
| `checklist-template.md` | Scene quality: triple purpose, off-balance ending, character presence, dialogue subtext |
| `constitution-template.md` | Story Bible: style mode selector, voice markers, craft principles |
| `characters-template.md` | Character profile: psychology, speech patterns, vocabulary, sample dialogue, body language |
| `characters-index-template.md` | Character roster: all characters with role, affiliations, first appearance |
| `pov-structure-template.md` | POV architecture: mode, schedule, voice differentiation, information asymmetry map |
| `agent-file-template.md` | Living context: active characters, world state, open threads, recent chapters |
| `series-bible-template.md` | Series canon: world rules, character state registry per book, series arc |
| `synopsis-template.md` | One-page (250–350 words) and full (1,000–2,000 words) synopsis in present tense |
| `glossary-template.md` | Invented terms, proper nouns, capitalization rules, consistency log |
| `subplots-template.md` | Subplot beat sheets: inciting incident through resolution, main plot intersection map |
| `research-template.md` | Open questions, source notes, world-building facts, resolved findings |
| `timeline-template.md` | Chapter-by-chapter chronology, elapsed time, scene durations, continuity cross-refs |
| `world-building-template.md` | Setting rules, geography, culture, history, in-world systems |
| `locations-template.md` | Per-location sensory anchors, atmosphere, character behavioral tells, state log |
| `themes-template.md` | Thematic contract: motif registry, symbol tracker, chapter thematic map, drift log |
| `feedback-template.md` | Beta/editorial feedback: raw notes, categorized issues, severity, revision tasks |
| `query-letter-template.md` | Query letter: hook, story body, housekeeping, comp titles, bio, submission tracker |

---

## Tutorials

### Tutorial: Single POV Novel

A single POV novel uses one viewpoint character throughout. This is the simplest architecture and the best starting point for first novels.

#### Step 1 — Establish the Story Bible

```
/speckit.constitution
```

Choose your **style mode**:

- **`author-sample`** — Paste 500–2,000 words from a book or story you've written (or want to emulate). The AI extracts 8 voice markers: POV, tense, rhythm, vocabulary register, sensory density, tone, dialogue style, and anti-patterns.
- **`humanized-ai`** — Use the built-in anti-AI craft ruleset: sensory grounding, character-in-body principles, dialogue subtext rules, filter-word purge.

Choose your **plot structure**: Three-Act Structure, Save the Cat, Hero's Journey, Story Circle, Fichtean Curve, or custom.

This creates `.specify/memory/constitution.md` — the governing authority for all subsequent commands.

#### Step 2 — Write the Story Brief

```
/speckit.specify A 19th-century lighthouse keeper starts receiving telegrams from a ship that sank twenty years ago.
```

The AI produces `spec.md` with:
- A two-sentence **logline**
- **Character arcs** with priorities (P1 = protagonist, P2+ = supporting)
- **Scene beats** in Given/When/Then format
- **Plot requirements** and reader experience goals

#### Step 3 — Clarify Before Planning

```
/speckit.clarify
```

Scans `spec.md` for `[NEEDS CLARIFICATION]` markers and ambiguities across:
- Character motivation (why does the keeper not destroy the telegrams?)
- Timeline (when does Act II break happen?)
- POV clarity (how close is the narrative distance?)
- World-building inconsistencies

Writes resolutions directly back into `spec.md`. **Do not skip this step** — ambiguities here multiply into structural problems downstream.

#### Step 4 — Build the Story Structure

```
/speckit.plan
```

Reads `spec.md` and `constitution.md`, produces `plan.md` with:
- Act/phase breakdown aligned to your chosen plot structure
- Chapter-by-chapter map with estimated word counts
- Story bible compliance check gates
- Supporting document map (which templates to populate)

#### Step 5 — Generate Scene Tasks

```
/speckit.tasks
```

Reads `plan.md` and `spec.md`, produces `tasks.md` with:
- Scene-by-scene tasks ordered by act
- A research phase at the top (tasks marked `[BLOCKED]` until research documents exist)
- Critical checkpoint markers between acts
- A polish pass block at the end

#### Step 6 — Structural Check (Pre-Draft)

```
/speckit.analyze
```

Read-only verification that `spec.md` → `plan.md` → `tasks.md` coverage is complete. No file modifications. Fix any gaps before drafting.

#### Step 7 — Generate and Approve Scene Outlines

```
/speckit.outline all
```

Generates one `outlines/<CHAPTER_ID>-outline.md` file per scene. Each file contains:
- Opening hook (one concrete sentence)
- Causal beat sequence (ordered, one sentence per beat)
- Character beats (want vs. get for each character present)
- Dialogue requirements (what must be deflected or left unspoken)
- Sensory anchors (drawn from `locations.md`)
- Thematic work (active motif + delivery method)

All files are created with `status: DRAFT`. Review each one, edit freely, then:
- Set `status: APPROVED` → AI drafts the chapter from this outline
- Set `status: SKIP` → you write the chapter yourself; AI skips it entirely

#### Step 8 — Draft

```
/speckit.implement
```

Executes tasks in order. For each chapter:
- If an outline file exists with `status: APPROVED` → uses it as the working brief (overrides `plan.md`)
- If an outline file exists with `status: DRAFT` → **stops** with an outline gate warning
- If an outline file has `status: SKIP` → marks task done, skips to next chapter
- If no outline file exists → falls back to `plan.md` (no gate)

**Author-written path** — generate outline only, no prose:

```
/speckit.implement --outline-only
```

Generates the outline file for the next scene and stops. No `draft/` files are written. You write the chapter in `draft/` manually, then run `speckit.checklist` as normal.

#### Step 9 — Quality Loop (per chapter)

```
/speckit.checklist        ← "unit test" the scene
/speckit.revise           ← fix only failing passages (if needed)
/speckit.polish           ← line-edit pass (only after checklist PASS)
```

This loop is identical whether the prose was AI-drafted or author-written.

Repeat for each chapter. Run `speckit.status` at any time for a dashboard view.

---

### Tutorial: Multi-POV Novel

Multi-POV adds an architecture layer on top of the single-POV workflow. You still follow the same planning and drafting steps, but you insert a POV design pass after planning and before tasking.

#### Supported POV Modes

| Mode | Description | Classic Examples |
|---|---|---|
| **Alternating** | Two or more POVs in strict rotation | *The Girl with the Dragon Tattoo* |
| **Dual** | Exactly two POVs, equal weight | *Gone Girl* |
| **Braided** | Three or more POVs, interdependent arcs | *A Song of Ice and Fire* |
| **Ensemble** | Four or more POVs, roughly equal weight | *Donna Tartt's The Secret History* |
| **Mosaic** | Many POVs, loosely connected, fragmented | *Cloud Atlas* |
| **Frame + Embedded** | Outer narrator frames inner story | *Frankenstein* |
| **Chorus** | Collective "we" narrator | *The Virgin Suicides* |
| **First-Person Multiple** | Each POV chapter written in first person | *As I Lay Dying* |

#### Additional Step: POV Architecture

After `speckit.plan`, before `speckit.outline`:

```
/speckit.pov draft
```

This creates `pov-structure.md` with:
- **POV Configuration** table (mode, character count, tense, narrative distance, chapter demarcation)
- **Voice Differentiation Matrix** — how each POV character sounds different (vocabulary register, sentence length, sensory focus)
- **POV Schedule** — chapter-by-chapter assignment of POV characters
- **Information Asymmetry Map** — what each POV character knows and when
- **Convergence Points** — scenes where character arcs intersect
- **Relay Rules** — how POV handoffs between chapters are handled

#### POV Sub-Commands

```
/speckit.pov audit          ← audit voice differentiation across all POV characters
/speckit.pov schedule       ← generate or validate the chapter-by-chapter POV schedule
/speckit.pov asymmetry      ← check that no POV character knows what they shouldn't
/speckit.pov relay          ← review POV handoff transitions between chapters
```

Ask any free-text POV design question and `speckit.pov` will answer without modifying files:

```
/speckit.pov Should Elena's POV come before or after Marcus's in chapter 12?
```

#### Post-Draft: Continuity for Multi-POV

After drafting, `speckit.continuity` is especially important in multi-POV narratives to verify:
- No character acts on information their POV hasn't encountered yet
- Voice register doesn't drift between chapters
- Timeline coherence across interleaved timelines

```
/speckit.continuity
```

Optionally scope to specific chapters:

```
/speckit.continuity JO3.201–JO3.203
```

---

### The Planning Process

The planning phase produces three documents that lock in the story's architecture before a single draft scene is written. The order matters.

```
speckit.constitution  →  speckit.specify  →  speckit.clarify  →  speckit.plan  →  speckit.tasks  →  speckit.outline
```

**`speckit.constitution`** is a prerequisite for everything else. It encodes:
- Your style mode and extracted/manual voice markers
- Plot structure choice (governs how `plan.md` will be structured)
- Central Dramatic Question
- Prohibited phrases (anti-AI filter applied during `speckit.implement`)

**`speckit.specify`** converts a pitch-length idea into a structured brief. Keep your initial prompt concise — one or two sentences. The AI expands it into `spec.md`. You edit `spec.md` directly after.

**`speckit.clarify`** is the most important step to not skip. Gaps in the brief do not disappear when you plan — they become structural holes. Run clarify until `spec.md` has no `[NEEDS CLARIFICATION]` markers remaining.

**`speckit.plan`** reads the clarified brief and story bible and produces the full act breakdown. If you're using a non-standard plot structure, specify it during `speckit.constitution` setup.

**`speckit.tasks`** reads `plan.md` and converts every chapter beat into an actionable writing task. Tasks are ordered, prioritized by arc, and blocked where prerequisite documents are missing. Resolve blocked tasks by creating the required supporting documents (characters, world-building, research) before drafting those scenes.

**`speckit.outline`** expands each plan entry into a dedicated, author-editable outline file. This is the bridge between structural planning and prose: plan.md captures *what* happens at the story level; the outline file captures *how* the scene plays out beat by beat, with specific sensory anchors and dialogue requirements. The author's review and approval of each outline is the last checkpoint before AI prose is generated.

---

### Analyze Before You Draft

`speckit.analyze` is a mandatory pre-flight check before `speckit.implement`. It is **strictly read-only** — it never modifies files.

```
/speckit.analyze
```

It checks:
- Every spec requirement maps to at least one plan chapter
- Every plan chapter maps to at least one task
- Act proportions are within acceptable range for your plot structure
- No orphan tasks (tasks referencing non-existent plan chapters)
- Story bible principles are not contradicted in `plan.md`

If `speckit.analyze` flags gaps, resolve them in `spec.md`, `plan.md`, or `tasks.md` before proceeding. Drafting over structural holes costs far more revision time than fixing them pre-draft.

---

### Drafting Scenes with Tasks

`speckit.implement` executes one task at a time, in order. It operates in two modes:

#### AI-Drafted Mode (default)

```
/speckit.implement
```

For each chapter:

1. Reads the task from `tasks.md`
2. Checks the checklist gate (previous chapter must pass before continuing)
3. Checks the **outline gate**: if `outlines/<CHAPTER_ID>-outline.md` exists with `status: DRAFT`, stops and asks the author to approve it first
4. If outline is `APPROVED`: uses the outline file as the working brief
5. If outline is `SKIP`: marks the task done and moves on — no prose generated for that chapter
6. If no outline file: falls back to `plan.md` directly (same behaviour as before `speckit.outline` existed)
7. Drafts the scene into `draft/`

#### Author-Written Mode (`--outline-only`)

```
/speckit.implement --outline-only
```

Generates the outline file for the next unwritten scene and **stops** — no prose is produced. The author writes the chapter in `draft/` manually (any tool, any format). The same quality loop (`speckit.checklist` → `speckit.revise` → `speckit.polish`) applies regardless of who wrote the prose.

You can also mix modes per scene by setting `status: SKIP` in any individual outline file.

**Check project status at any time:**

```
/speckit.status
```

Produces a dashboard showing word counts (actual vs. estimated), chapter completion status (drafted / revising / polishing / done), and outstanding gates.

---

### Checklist, Polish & Revise

These three commands form the per-chapter quality loop. Run them in this order.

#### 1. Checklist (Unit Test for Prose)

```
/speckit.checklist
```

Validates the *craft layer* of the scene (not plot logic):

| Gate | Description |
|---|---|
| Triple Purpose | Does every scene serve ≥3 narrative functions simultaneously? |
| Off-Balance Ending | Does the scene end in a new instability, not resolution? |
| Embodied Emotion | Are emotions shown through physical reactions, not named? |
| Dialogue Subtext | Does every dialogue exchange carry at least one deflection or misunderstanding? |
| Sensory Anchoring | Is at least one non-visual sense grounded per scene? |
| Prohibited Phrases | Are all AI-sounding phrases (from the story bible list) absent? |

The checklist result is saved to `checklists/<CHAPTER_ID>-checklist.md`.

#### 2. Revise (Surgical Rewrite)

If any gate fails:

```
/speckit.revise A1.101
/speckit.revise A1.101 "CHR-002 STB-004"     ← specify failure codes
/speckit.revise A1.101 checklists/A1.101_Awakening-checklist.md
```

`speckit.revise` rewrites **only the failing passages**. It does not improve surrounding prose or change passing sections. The result is a versioned file (e.g., `Chapter_v2.md`) with a diff summary.

Do not use `speckit.revise` for structural problems — those require changes to `plan.md` and `tasks.md` first.

#### 3. Polish (Line-Edit Pass)

Only run after checklist PASS:

```
/speckit.polish
```

Applies surface-level refinements:

| Fix | Rule |
|---|---|
| Sentence rhythm | Alternates short and long sentences; moves weight to line endings |
| Word repetition | Eliminates same-word echoes within and across adjacent paragraphs |
| Filter words | Removes `she noticed`, `he felt`, `she saw`, `he heard` |
| Adverb density | Caps at 1 adverb per 200 words |
| Weak verbs | Replaces `was`, `had`, `got` with active alternatives |
| Voice register drift | Corrects vocabulary that drifts away from character register |
| Punctuation overuse | Reduces em-dash and ellipsis clusters |
| Paragraph openings | Ensures variety in how paragraphs begin |

`speckit.polish` is a **linter and formatter**, not a structural tool. Never use it to fix story bible violations, missing triple purpose, or off-balance endings — that is `speckit.revise`'s job.

---

### Processing Feedback

Beta-reader, critique-partner, and editorial feedback enters the workflow through `speckit.feedback`.

```
/speckit.feedback feedback-notes.txt --reader-type beta
/speckit.feedback "The pacing in chapters 8–12 dragged and I lost interest in Marcus entirely." "Jane Doe" --reader-type cp
```

The command:
1. Ingests raw notes (file path or quoted block)
2. Categorizes each issue: **Structural / Character / Pacing / Clarity / Factual**
3. Assigns severity: **CRITICAL / MAJOR / MINOR**
4. Maps issues to specific chapter IDs
5. Generates prioritized revision tasks appended to `tasks.md`
6. Logs everything to `feedback/feedback.md`

Sub-commands for managing the feedback log:

```
/speckit.feedback triage          ← re-categorize existing feedback without regenerating tasks
/speckit.feedback tasks           ← generate tasks from an already-triaged log
```

After feedback ingestion:

```
/speckit.revise                   ← address CRITICAL issues first
/speckit.continuity               ← cross-reference feedback against current drafts
/speckit.status                   ← check overall revision progress
```

---

### Query Letter & Export

#### Writing the Query Letter

Before writing the query letter, ensure `synopsis.md` exists (generate with `speckit.specify` or manually from `synopsis-template.md`).

```
/speckit.query draft
```

Produces a `query-letter.md` in 250–350 words following the industry-standard four-section format:

1. **Personalization** — why this specific agent (left blank, add manually per submission)
2. **Hook** — protagonist + inciting incident + stakes (≤50 words)
3. **Body** — setup, escalation, central dramatic question (~200 words)
4. **Housekeeping** — word count, genre, comp titles, bio, credentials

Log submissions and suggest comparable titles:

```
/speckit.query update             ← add a submission log entry
/speckit.query track              ← view submission tracker table
/speckit.query comp-titles        ← generate comp title suggestions only
/speckit.query "Sarah Jensen at Foundry Literary"  ← generate personalization paragraph
```

#### Exporting the Manuscript

Requires [pandoc](https://pandoc.org) installed separately.

```
/speckit.export                   ← DOCX (default, submission-ready)
/speckit.export epub              ← EPUB (KDP / Draft2Digital / IngramSpark)
/speckit.export latex             ← LaTeX (typeset)
```

Chapter assembly logic:
- Prefers `<CHAPTER_ID>_<Title>_polished.md` over base drafts
- Sorts chapters by `chapter_id` from frontmatter
- Highest version number wins (e.g., `_v3.md` beats `_v2.md`)

---

## POV Modes Reference

| Mode | POV Count | Rotation Pattern | When to Use |
|---|---|---|---|
| **Single POV** | 1 | N/A | Best for intimate, psychological narratives |
| **Alternating** | 2–4 | Strict rotation between chapters | Parallel storylines converging toward a common climax |
| **Dual** | 2 | Equal weight, chapter by chapter | Dual protagonists with equal narrative importance |
| **Braided** | 3+ | Interdependent, convergence-driven | Complex ensemble with significant plot intersection |
| **Ensemble** | 4+ | Roughly equal weight | Community or group narratives |
| **Mosaic** | Many | Fragmented, loosely connected | Non-linear, thematic over plot-driven |
| **Frame + Embedded** | 2 (outer + inner) | Outer frames inner | Unreliable narrators, stories-within-stories |
| **Chorus** | Collective | "We" narrator | Communities as protagonist |
| **First-Person Multiple** | 2+ | Each chapter in first person | Maximum intimacy, high voice differentiation required |

---

## Plot Structure Support

The preset supports any plot structure. Configure in `speckit.constitution`. The `plan.md` act breakdown adapts to the chosen framework.

| Framework | Act Structure | Best For |
|---|---|---|
| **Three-Act Structure** | Setup / Confrontation / Resolution | Universal; commercial fiction |
| **Save the Cat** | 15 beats mapped to pages | Genre fiction; screenwriter-influenced |
| **Hero's Journey** | 12 stages (Campbell/Vogler) | Mythic, quest, and coming-of-age |
| **Story Circle** | 8 stages (Dan Harmon) | Character transformation arcs |
| **Fichtean Curve** | Rising crises to climax | Short, crisis-dense narratives |
| **In Medias Res** | Custom entry point | Literary fiction; non-linear structure |
| **Custom** | Author-defined phases | Experimental or hybrid structures |

---

## Style Modes

### Author Voice Sample (`author-sample`)

Paste 500–2,000 words from your own writing or a target author. `speckit.constitution` extracts 8 style markers automatically:

1. **POV & Tense** — narrative distance and temporal mode
2. **Rhythm** — typical sentence length and cadence patterns
3. **Vocabulary Register** — formal vs. colloquial, period-appropriate
4. **Sensory Density** — frequency and type of sensory detail
5. **Tone** — emotional temperature and irony level
6. **Dialogue Style** — attribution patterns, subtext density
7. **Anti-Patterns** — specific phrasings to avoid (extracted from sample)
8. **Scene Integrity Rules** — structural habits in the sample text

### Humanized AI Prose (`humanized-ai`)

Uses the built-in craft ruleset for AI-generated prose that reads as human-crafted. The following **universal principles** apply in all profiles — they cannot be disabled:

| Principle | Rule |
|---|---|
| Sensory grounding | Minimum one non-visual sense per scene |
| Character-in-body | Physical reactions precede named emotions |
| Dialogue subtext | Deflection or misunderstanding in every exchange |
| Filter word purge | No `she noticed`, `he felt`, `she saw`, `he heard` |
| Off-balance ending | Every scene ends in a new instability |
| Triple purpose | Every scene serves ≥3 narrative functions simultaneously |
| Dirt Rule | Every environment has at least one flaw or imperfection |
| Anti-AI Filter | Prohibited phrases list (universal + profile-specific) |

#### Prose Profiles

When using `humanized-ai`, choose a **Prose Profile** to set how the universal principles are weighted. All profiles enforce all universal principles — they differ in sentence rhythm, sensory density, interiority depth, dialogue subtext intensity, and pacing bias.

| Profile | Best For | Sentence Rhythm | Sensory Density | Interiority | Pace Bias |
|---|---|---|---|---|---|
| **`commercial`** | General fiction, fantasy, romance | Alternating short/long | Medium | Balanced | Scene = Sequel |
| **`literary`** | Literary fiction, character studies | Long-dominant; fragments under rupture | High (texture) | Deep, contradictory | Reflection-forward |
| **`thriller`** | Thrillers, crime, horror | Short-dominant (1–2 clauses) | Low-medium, functional | Minimal; act-before-reflect | Action-forward |
| **`atmospheric`** | Gothic, horror, weird fiction | Long, winding, syntactically embedded | Maximum; environment as character | Deep; inner/outer blur permitted | Atmosphere as plot |
| **`dark-realist`** | Noir, social realism, gritty literary | Clipped, declarative, no ornament | Medium; decay and failure bias | Cold, selective; rationalisation visible | Consequence-forward |

Each profile also adds its own genre-specific Anti-AI filter entries. Examples:

- **`commercial`** adds: `"a world turned upside down"` · `"everything changes when"`
- **`literary`** adds: `"liminal"` · `"ineffable"` · `"the weight of"` · `"something shifted inside her"`
- **`thriller`** adds: `"heart pounding"` · `"adrenaline surged"` · `"every instinct screamed"`
- **`atmospheric`** adds: `"an oppressive silence"` · `"the darkness seemed alive"` · `"she could feel the history"`
- **`dark-realist`** adds: `"broken but not beaten"` · `"found her strength"` · `"at the end of the day"`

Set the profile using `speckit.constitution` — it will prompt for the choice when initialising `humanized-ai` mode.

---

## Export Formats

| Format | Use Case | Requirements |
|---|---|---|
| **DOCX** | Publisher/agent submissions, Word compatibility | pandoc ≥ 2.11 |
| **EPUB** | KDP, Draft2Digital, IngramSpark, Kobo | pandoc ≥ 2.11 |
| **LaTeX** | Professional typesetting, print-on-demand | pandoc ≥ 2.11 + LaTeX distribution |

Install pandoc: [pandoc.org/installing.html](https://pandoc.org/installing.html)

---

## Workflow Sequence Diagram

![Spec Kit Fiction Book Writing workflow sequence diagram](SPEC%20KIT%20Fictional%20Book%20Writing.svg)

---

## Related Resources

- [Spec Kit Documentation](https://github.com/andreasdarsa/spec-kit)
- [Spec-Driven Development Overview](../../spec-driven.md)
- [Preset Development Guide](../ARCHITECTURE.md)
- [Publishing a Preset](../PUBLISHING.md)
