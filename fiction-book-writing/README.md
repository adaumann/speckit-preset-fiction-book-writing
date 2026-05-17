# Spec Kit Fiction Book Writing Preset

**Version 1.8.0** Â· Part of [Spec Kit](https://github.com/adaumann/speckit-preset-fiction-book-writing)

A Spec-Driven Development preset purpose-built for novel and long-form fiction writing. It applies the discipline of structured software development to creative fiction: story bibles instead of architecture docs, scene tasks instead of tickets, quality gates instead of CI checks.

**Key features at a glance:**

- **Story Bible governance** â€” `constitution.md` is the single source of truth for voice, tense, prose profile, tone, target audience, and language. Every command reads from it; no style drift across sessions.
- **Full story pipeline** â€” 27 AI commands from first idea (`speckit.specify`) through structural planning (`speckit.plan`, `speckit.outline`), drafting (`speckit.implement`), quality loop (`speckit.checklist`, `speckit.revise`, `speckit.polish`), feedback (`speckit.feedback`), and submission (`speckit.synopsis`, `speckit.query`, `speckit.export`).
- **Multi-POV architecture** â€” 9 POV modes including alternating, dual, braided, ensemble, mosaic, frame, chorus, and first-person-multiple. `speckit.pov` designs and audits the POV schedule and information asymmetry map.
- **All major plot structures** â€” Three-Act, Save the Cat, Hero's Journey, Story Circle, Fichtean Curve, KishÅtenketsu, Freytag's Pyramid, Five-Act, and custom. `speckit.plan` adapts the chapter map to your chosen framework.
- **Two style modes** â€” `author-sample` (extract 8 voice markers from your own prose) or `humanized-ai` (built-in craft ruleset: 5 prose profiles, sensory grounding, filter word purge, off-balance endings, Triple Purpose).
- **Multilingual** â€” set `Language` (BCP-47) in the story bible once; prose drafting, SSML output, export metadata, and English-specific prose checks all adapt automatically. 12 languages supported.
- **Submission-ready export** â€” pandoc-based DOCX, EPUB (KDP / IngramSpark / D2D), and LaTeX output. Author name, language, copyright, and "About the Author" back matter all read from the story bible automatically.
- **Audiobook pipeline** â€” SSML / ElevenLabs audiodraft generation, voice assignments, pronunciation lexicon (W3C PLS 1.0), and stale-draft detection.
- **Cover design** â€” `speckit.cover` generates a platform-specific cover brief, 3 AI image prompts, and typography placement notes for KDP, IngramSpark, D2D, and social media. 10 style presets.
- **Author bio management** â€” `speckit.bio` drafts, refines, and generates context-specific bio variants (agent query, reader back matter, platform, social, first-person, press kit). Stored in the story bible; consumed automatically by `speckit.query` and `speckit.export`.
- **Offline semantic search index** - for large fiction projects. Walks all project markdown files, chunks them into ~300-token segments with
metadata (file, section, character IDs, location IDs, date tags), and stores embeddings in a local ChromaDB index (no external services â€” fully offline). Primary backend  : ChromaDB + sentence-transformers (semantic / vector search). Fallback backend : BM25 keyword search (pure Python, zero ML dependencies)

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Commands Reference](#commands-reference)
- [Templates Reference](#templates-reference)
- [Tutorials](#tutorials)
  - [Single POV Novel](#tutorial-single-pov-novel)
  - [Multi-POV Novel](#tutorial-multi-pov-novel)
  - [Series Workflow](#series-workflow)
  - [The Planning Process](#the-planning-process)
  - [Analyze Before You Draft](#analyze-before-you-draft)
  - [Drafting Scenes with Tasks](#drafting-scenes-with-tasks)
  - [Checklist, Polish & Revise](#checklist-polish--revise)
  - [Processing Feedback](#processing-feedback)
  - [Synopsis & Query Letter](#synopsis--query-letter)
  - [Export](#export)
  - [Glossary, Research & Versions](#glossary-research--versions)
- [POV Modes Reference](#pov-modes-reference)
- [Plot Structure Support](#plot-structure-support)
- [Style Modes](#style-modes)
- [Export Formats](#export-formats)
- [Language Support](#language-support)
- [Comparable Products](#comparable-products)
- [Related Resources](#related-resources)

---

## Overview

The Fiction Book Writing preset applies the Spec-Driven Development methodology to creative fiction. It provides:

- **27 AI commands** covering every stage from idea to submission-ready manuscript
- **21 templates** for all supporting story documents
- **1 export script** (pandoc-based) for DOCX, EPUB, and LaTeX output
- Support for **9 POV modes** (single, alternating, dual, braided, ensemble, mosaic, frame, chorus, first-person-multiple)
- Support for all major **plot structure frameworks** (Three-Act, Save the Cat, Hero's Journey, Story Circle, etc.)
- Two **style modes**: author voice sample extraction or humanized AI prose principles

The central philosophy: the **story bible** (`constitution.md`) is the governing authority. Every drafted scene, every revision, every checklist gate derives its rules from it.

Each specification run (/speckit.specify) will generate one book, it is a 1:1 relationship. Make sure to give the most detailed specification and plan before implementation.

---

## Prerequisites

This preset requires the following tools installed on your system:

- **[Spec Kit CLI](https://github.com/adaumann/specify)**: The core engine for running commands.
- **Python 3.10+**: Required for export and search indexing scripts.
- **Pandoc**: Required by `speckit.export` for DOCX, EPUB, and LaTeX generation.
- **(Optional) Node.js**: Required if you use certain MCP servers for extended capabilities.

---

## Installation

1.  **Install the Spec Kit CLI**:
    ```powershell
    # Windows (PowerShell)
    iwr -useb https://raw.githubusercontent.com/adaumann/specify/main/install.ps1 | iex
    ```

2.  **Initialize a new project with this preset**:
    ```powershell
    mkdir my-new-novel
    cd my-new-novel
    specify init --preset fiction-book-writing
    ```
---

## Quick Start

```bash
# 1. Install Spec Kit and apply the preset
# (See Installation section above)

# 2. Create your story bible first
/speckit.constitution

# 3. Write your story idea as a brief
/speckit.specify A reluctant librarian discovers her small town's founding myth is a cover story for her ancestor's crimes â€” and the only witness is still alive.

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
# â†’ review outlines/, edit beats, set status: APPROVED or status: SKIP

# 10. Start drafting (AI prose for APPROVED; skips SKIP chapters)
/speckit.implement
# â†' AI drafts only APPROVED chapters; SKIP chapters are marked as author-written
# Options:
#   --dismiss-outline  : Draft freely without outline gates (discovery mode)
#   --outline-only     : Generate outlines only, no prose (review before drafting)

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
    constitution.md        â† Story Bible (governing authority)
  features/
    <story-slug>/
      spec.md              â† Story brief (logline, arcs, beats)
      plan.md              â† Story structure (acts, chapters)
      tasks.md             â† Scene-by-scene writing tasks
      pov-structure.md     â† POV architecture (multi-POV)
      characters/
        index.md           â† Character roster
        <character>.md     â† Per-character profiles
      world-building.md    â† Setting rules and world systems
      timeline.md          â† Chronology and elapsed time
      research.md          â† Open questions and source notes
      subplots.md          â† Subplot beat sheets
      themes.md            â† Thematic contract and motif registry
      glossary.md          â† Consistency reference (invented terms)
      locations.md         â† Canonical location reference
      series-bible.md      â† Series-level canon (multi-book)
      outlines/
        <CHAPTER_ID>_<Title>-outline.md  â† Scene outline (status: DRAFT/APPROVED/SKIP)
      draft/
        <CHAPTER_ID>_<Title>.md        â† Chapter draft
        <CHAPTER_ID>_<Title>_v2.md     â† Revised version
        <CHAPTER_ID>_<Title>_polished.md
      audiodraft/
        <CHAPTER_ID>_<Title>.md        â† Chapter draft
        <CHAPTER_ID>_<Title>_v2.md     â† Revised version
        <CHAPTER_ID>_<Title>_polished.md
      checklists/
        <CHAPTER_ID>_<Title>-checklist.md
      feedback/
        feedback.md        â† Beta/editorial feedback log
      synopsis.md          â† Query-ready synopsis
      query-letter.md      â† Submission query letter
```

---

## Commands Reference

### Story Development

| Command | Phase | What It Does |
|---|---|---|
| `speckit.brainstorm` | Ideation | Interactive brainstorming session for any story topic â€” spec, characters, themes, world-building, research, or timeline. Produces a notes file or a patch to the topic file |
| `speckit.constitution` | Setup | Create or update the story bible: style mode, plot structure, craft principles |
| `speckit.specify` | Concept | Turn a free-text idea into a structured story brief with logline, character arcs, and scene beats |
| `speckit.clarify` | Concept | Detect and resolve ambiguities in `spec.md` (motivation gaps, timeline issues, POV holes) |
| `speckit.plan` | Structure | Build the act/phase breakdown and chapter map from `spec.md` and `constitution.md` |
| `speckit.pov` | Structure | Design and audit multi-POV architecture, generate POV schedule, validate information asymmetry |
| `speckit.tasks` | Pre-draft | Generate scene-by-scene writing tasks ordered by act and character arc |
| `speckit.outline` | Pre-draft | Generate editable per-scene outline files from `plan.md`; authors approve or skip before AI drafts |
| `speckit.analyze` | Pre-draft | Read-only structural alignment check (specâ†”planâ†”tasks coverage, act proportions) |

### Drafting & Quality

| Command | Phase | What It Does |
|---|---|---|
| `speckit.implement` | Drafting | Draft scenes and chapters by executing tasks in order from `tasks.md` |
| `speckit.checklist` | Quality | Generate per-scene quality checklists (triple purpose, off-balance endings, dialogue subtext, sensory detail) |
| `speckit.continuity` | Quality | Post-draft analysis: story bible compliance, character arc consistency, timeline coherence |
| `speckit.revise` | Revision | Surgically rewrite only the failing passages identified by checklist or continuity |
| `speckit.polish` | Polish | Final line-edit pass: rhythm, filter words, adverb density, voice register, repetition |
| `speckit.roleplay` | Exploration | Interactive multi-role play-through of an outline or draft chapter; AI and author take on scene roles beat by beat; accumulated insights committed back as revision notes |

### Post-Draft

| Command | Phase | What It Does |
|---|---|---|
| `speckit.feedback` | Revision | Ingest beta reader or editor notes, categorize issues, generate prioritized revision tasks |
| `speckit.status` | Monitoring | Read-only project dashboard: word counts, chapter status, outstanding quality gates |
| `speckit.versions` | Monitoring | Version timeline, narrative diff between two chapter versions, revision log, and milestone tagging |
| `speckit.glossary` | Consistency | Add terms, check drafts for glossary violations, audit unregistered terms, view coverage dashboard |
| `speckit.subplot` | Consistency | Add P2/P3 arcs mid-draft, check beat gaps and arc absence streaks, rebuild Convergence Map, resolve dramatic questions |
| `speckit.pacing` | Quality | Tension arc audit per chapter (1â€“10 score), plateau/peak/valley detection, act-band calibration, Mermaid xychart output. Flags sagging middles, undersold climaxes, and premature peaks |
| `speckit.statistics` | Quality | Sentence-level prose statistics: readability score (Flesch/Kincaid), sentence length variance, passive voice %, adverb density, filter word count, weak verb %, and dialogue balance (% dialogue vs. action vs. narration). Read-only. Run after drafting or polishing |
| `speckit.sensitivity` | Quality | Cultural representation, harmful tropes, anachronism review (historical fiction), identity portrayal, trauma depictions. CRITICAL/WARNING/NOTE tiers. Scoped by chapter, category, or full manuscript |
| `speckit.research` | Research | Log knowledge gaps, resolve findings, check factual claims in drafts, view open-item dashboard |
| `speckit.series` | Series | Init/audit/update the series bible and run cross-book continuity checks |
| `speckit.interview` | Character | Interactive one-on-one conversation with a character voiced by AI; export as notes |
| `speckit.help` | Navigation | Workflow advisor: scans project state, identifies blockers, recommends next steps |
| `speckit.synopsis` | Submission | Generate a one-page (250â€“350 words) and full (1,000â€“2,000 words) synopsis; reveals the ending; present tense, third person |
| `speckit.query` | Submission | Generate a 250â€“350 word query letter with hook, body, comp titles, and submission tracker |
| `speckit.export` | Submission | Export manuscript to DOCX (Word), EPUB (KDP/IngramSpark), or LaTeX via pandoc. `--platform` selects KDP, IngramSpark, D2D, Shunn, or Smashwords formatting |
| `speckit.audiobook` | Audiobook | Convert prose chapters to SSML/ElevenLabs audiodraft files, manage voice assignments and pronunciation lexicon, check for stale drafts, export `lexicon.pls` |
| `speckit.cover` | Submission | Generate a cover brief, AI image-generation prompts (3 variants), and platform specs for KDP, IngramSpark, D2D, and social. 10 style presets. Reads spec.md for title/author/genre/series |
| `speckit.bio` | Submission | Draft, refine, and generate author bio variants (agent / reader / platform / social / first-person). Stores canonical short and long bios in constitution.md. Short bio used by `speckit.query`; long bio appended by `speckit.export` as "About the Author" |

---

### Sub-Commands Quick Reference

All sub-commands and arguments for every command.

#### `speckit.brainstorm`
```
/speckit.brainstorm                        â† prompts for topic interactively
/speckit.brainstorm [topic]                â† spec, plan, characters, themes, world-building,
                                              locations, series, glossary, pov, research, timeline
/speckit.brainstorm character [name]       â† pre-fill a specific character
/speckit.brainstorm [topic] challenge      â† Challenge Mode: stress-test existing decisions
/speckit.brainstorm [topic] quick          â† short session (3â€“5 questions)
/speckit.brainstorm [topic] standard       â† standard session (default)
/speckit.brainstorm [topic] deep           â† exhaustive session
```

#### `speckit.specify`
```
/speckit.specify [free-text idea]          â† turn a pitch into a structured story brief
```

#### `speckit.constitution`
```
/speckit.constitution                      â† create or update the story bible (interactive)
```

`speckit.constitution` governs the full story bible at `.specify/memory/constitution.md`. During setup you will be prompted for:

- **Style mode**: `author-sample` (paste prose for voice extraction) or `humanized-ai` (built-in craft ruleset)
- **Plot structure**: Three-Act, Save the Cat, Hero's Journey, Story Circle, Fichtean Curve, Custom
- **Author Name**: your publishing byline â€” used by `speckit.cover`, `speckit.query`, and `speckit.export`
- **Language**: BCP-47 code (`en`, `de`, `fr`, `es`, `it`, `pt`, `nl`, `ja`, `zh`, `fi`, `hu`, `tr`) â€” gates prose checks and sets export `dc:language`
- **Copyright**: selectable format (All rights reserved / CC BY 4.0 / CC BY-NC 4.0 / CC0 / custom) â€” written as `dc:rights` in EPUB metadata
- **Author Bio (Short)** and **Author Bio (Long)**: stored in the bible; consumed by `speckit.query` (short) and `speckit.export` back matter (long). Use `speckit.bio draft` to generate and save these.
- **Tone**, **Target Audience**, **Series Position**, and all craft parameters

#### `speckit.clarify`
```
/speckit.clarify                           â† detect and resolve all ambiguities in spec.md
```

#### `speckit.plan`
```
/speckit.plan                              â† build the full story structure from spec.md
```

#### `speckit.pov`
```
/speckit.pov draft                         â† create pov-structure.md from spec.md
/speckit.pov audit                         â† audit voice differentiation across all POV characters
/speckit.pov schedule                      â† generate or validate the chapter-by-chapter POV schedule
/speckit.pov asymmetry                     â† check no POV character knows what they shouldn't
/speckit.pov relay                         â† review POV handoff transitions between chapters
/speckit.pov [free-text question]          â† contextual POV design question (read-only)
```

#### `speckit.tasks`
```
/speckit.tasks                             â† generate scene-by-scene writing tasks from plan.md
```

#### `speckit.outline`
```
/speckit.outline                           â† generate outline for the next scene without one
/speckit.outline all                       â† generate outlines for all unoutlined scenes
/speckit.outline [CHAPTER_ID]              â† generate outline for one scene (e.g. A1.101)
/speckit.outline [CHAPTER_ID]â€“[CHAPTER_ID] â† generate outlines for a chapter range
```

#### `speckit.analyze`
```
/speckit.analyze                           â† full pre-draft structural alignment check (read-only)
```

#### `speckit.implement`
```
/speckit.implement                         â† draft the next unchecked scene task in order
/speckit.implement [CHAPTER_ID]            â† draft a specific chapter
/speckit.implement --outline-only          â† generate outline only; no prose produced
```

#### `speckit.checklist`
```
/speckit.checklist                         â† checklist for most recently modified draft
/speckit.checklist [CHAPTER_ID]            â† checklist for a specific chapter
/speckit.checklist "Act I"                 â† checklists for all scenes in an act/phase
```

#### `speckit.continuity`
```
/speckit.continuity                        â† full post-draft continuity analysis (read-only)
/speckit.continuity [CHAPTER_ID]           â† scope to a single chapter
/speckit.continuity [CHAPTER_ID]â€“[CHAPTER_ID] â† scope to a chapter range
```

#### `speckit.revise`
```
/speckit.revise [CHAPTER_ID]                             â† revise all failing passages (auto-loads checklist)
/speckit.revise [CHAPTER_ID] "CHR-002 STB-004"           â† revise specific failure codes
/speckit.revise [CHAPTER_ID] checklists/[file].md        â† revise from explicit checklist path
```

#### `speckit.polish`
```
/speckit.polish                            â† polish most recently PASS-checked draft
/speckit.polish [CHAPTER_ID]               â† polish a specific chapter
/speckit.polish [CHAPTER_ID]â€“[CHAPTER_ID]  â† polish a chapter range
```

#### `speckit.roleplay`
```
/speckit.roleplay                          â† play through most recently modified outline or draft
/speckit.roleplay [CHAPTER_ID]             â† play through a specific scene
/speckit.roleplay [CHAPTER_ID] outline     â† force outline mode (even if a draft exists)
/speckit.roleplay [CHAPTER_ID] draft       â† force draft mode (even if only outline exists)
/speckit.roleplay [CHAPTER_ID] dialog      â† Dialog Workshop mode: speaker turns + improvisation
/speckit.roleplay [CHAPTER_ID] tension     â† Tension Curve analysis pass after play-through
/speckit.roleplay [CHAPTER_ID] pick        â† Section Picker: choose which beats to include
/speckit.roleplay [CHAPTER_ID] [N]-[M]     â† play only segments N through M (e.g. 3-7)
/speckit.roleplay [CHAPTER_ID] dialog pick â† mode flags and pick/range are combinable
```

#### `speckit.feedback`
```
/speckit.feedback [file-path] --reader-type [beta|cp|editor]   â† ingest feedback from a file
/speckit.feedback "[quoted notes]" "[reader name]" --reader-type [type]
/speckit.feedback triage                   â† re-categorize an existing feedback log
/speckit.feedback tasks                    â† generate tasks from an already-triaged log
```

#### `speckit.status`
```
/speckit.status                            â† full project dashboard (word counts, chapter status, gates)
```

#### `speckit.versions`
```
/speckit.versions list [CHAPTER_ID]        â† version timeline for one chapter
/speckit.versions list                     â† version timeline for all chapters
/speckit.versions diff [CHAPTER_ID]        â† narrative diff: latest vs. previous version
/speckit.versions diff [CHAPTER_ID] v1 v3  â† diff two specific versions
/speckit.versions log                      â† cross-chapter revision history sorted by date
/speckit.versions tag [CHAPTER_ID] v2 [label]  â† attach a milestone label to a version
```

#### `speckit.glossary`
```
/speckit.glossary                          â† status dashboard (same as status)
/speckit.glossary add [term]               â† register a new term interactively
/speckit.glossary add [term] --type [type] â† skip type prompt: invented, character, place, faction, rule
/speckit.glossary check                    â† scan all drafted chapters for glossary violations
/speckit.glossary check [CHAPTER_ID]       â† scope the check to one chapter
/speckit.glossary audit                    â† find unregistered invented terms in drafts
/speckit.glossary audit [CHAPTER_ID]       â† scope the audit to one chapter
/speckit.glossary status                   â† term counts, open violations, coverage by section
```

#### `speckit.subplot`
```
/speckit.subplot                           â† subplot health dashboard (same as status)
/speckit.subplot add [character name]      â† register a new subplot arc interactively
/speckit.subplot add [name] --priority [P2/P3]  â† skip the priority prompt
/speckit.subplot check                     â† audit all subplot arcs (beat gaps, absence streaks)
/speckit.subplot check [SP-NNN]            â† scope audit to a single subplot
/speckit.subplot intersect                 â† rebuild the Convergence Map
/speckit.subplot resolve [SP-NNN]          â† mark a subplot's dramatic question as resolved
```

#### `speckit.pacing`
```
/speckit.pacing                            â† full tension arc audit of all drafted chapters
/speckit.pacing [CHAPTER_ID]              â† scope to a single chapter
/speckit.pacing [CHAPTER_ID]â€“[CHAPTER_ID] â† scope to a chapter range
/speckit.pacing chart                     â† output only the Mermaid tension arc chart
/speckit.pacing --act "Act II"            â† scope to one act band
```

#### `speckit.statistics`
```
/speckit.statistics                        â† full prose statistics report across all drafted chapters
/speckit.statistics [CHAPTER_ID]           â† scope to a single chapter
/speckit.statistics [CHAPTER_ID]â€“[CHAPTER_ID] â† scope to a chapter range
/speckit.statistics --act "Act II"         â† scope to one act band
/speckit.statistics dialogue               â† output only the dialogue balance report
/speckit.statistics readability            â† output only readability and sentence-level metrics
```

#### `speckit.sensitivity`
```
/speckit.sensitivity                       â† full sensitivity review of all drafted chapters
/speckit.sensitivity [CHAPTER_ID]          â† scope to a single chapter
/speckit.sensitivity [CHAPTER_ID]â€“[CHAPTER_ID] â† scope to a chapter range
/speckit.sensitivity --category [name]     â† representation, tropes, historical, language, trauma
/speckit.sensitivity --genre [genre]       â† override genre detection (e.g. historical-fiction, fantasy)
```

#### `speckit.research`
```
/speckit.research add "[topic]"            â† log a new research item or source finding
/speckit.research resolve R-003 --finding "..." --source "..."
/speckit.research check [CHAPTER_ID]       â† check one chapter for unsupported factual claims
/speckit.research status                   â† open-item dashboard sorted by story risk
```

#### `speckit.series`
```
/speckit.series init                       â† scaffold series/series-bible.md (before Book 1)
/speckit.series audit                      â† cross-book continuity, arc chains, unresolved threads
/speckit.series update [book-number]       â† sync series bible after completing a book
/speckit.series status                     â† series-wide dashboard
```

#### `speckit.interview`
```
/speckit.interview [CHARACTER_NAME]        â† interactive one-on-one session with a character
```

#### `speckit.help`
```
/speckit.help                              â† full guidance report for current project state
/speckit.help --focus [phase]             â† limit advice to one phase: planning, drafting,
                                              revision, polish, submission
/speckit.help --chapter [CHAPTER_ID]      â† focused advice for one chapter
/speckit.help "[free-text question]"       â† contextual answer grounded in project state
```

#### `speckit.synopsis`
```
/speckit.synopsis                          â† generate both one-page and full synopsis
/speckit.synopsis one-page                 â† generate only the 250â€“350 word synopsis
/speckit.synopsis full                     â† generate only the 1,000â€“2,000 word synopsis
/speckit.synopsis update                   â† regenerate from current draft (post-draft accuracy)
/speckit.synopsis check                    â† validate synopsis.md against spec.md and plan.md
```

#### `speckit.query`
```
/speckit.query draft                       â† generate a query letter from spec.md and synopsis.md
/speckit.query update                      â† add a submission log entry
/speckit.query track                       â† view submission tracker table
/speckit.query comp-titles                 â† generate comp title suggestions only
/speckit.query "[Agent Name at Agency]"    â† generate a personalization paragraph
```

#### `speckit.export`
```
/speckit.export                            â† DOCX (default, Shunn submission format)
/speckit.export docx                       â† DOCX (Word, Shunn manuscript format)
/speckit.export docx --platform smashwords â† Smashwords DOCX (minimal styles)
/speckit.export epub                       â† EPUB, KDP platform (default)
/speckit.export epub --platform kdp        â† EPUB for KDP (cover required for listing)
/speckit.export epub --platform ingramspark â† EPUB for IngramSpark + accessibility metadata
/speckit.export epub --platform ingramspark --isbn 978-3-16-148410-0  â† with ISBN
/speckit.export epub --platform d2d        â† EPUB for Draft2Digital (stripped CSS; cover separate)
/speckit.export latex                      â† LaTeX 6Ã—9 KDP print (default)
/speckit.export latex --platform kdp-print-6x9     â† KDP Print trim 6"Ã—9"
/speckit.export latex --platform ingramspark-6x9   â† IngramSpark 6"Ã—9" (PDF/X-1a notes)
/speckit.export audio                      â† assemble audiobook chapter manifest; validate drafts
/speckit.export --polished-only            â† skip chapters without a polished version
/speckit.export --title "My Novel"         â† override title (default: reads from spec.md)
/speckit.export --author "Jane Smith"      â† override author byline (default: reads from constitution.md)
/speckit.export --lang de                  â† override BCP-47 language code (default: reads from constitution.md â†’ en)
/speckit.export --rights "Â© 2026 Jane Smith. All rights reserved."  â† override dc:rights metadata
/speckit.export --author-bio "Jane Smith writesâ€¦"  â† override "About the Author" back matter text
/speckit.export --no-author-bio            â† suppress "About the Author" even if set in constitution.md
/speckit.export --status polished          â† filter by chapter status
```

#### `speckit.audiobook`
```
/speckit.audiobook                         â† audiodraft production dashboard (same as status)
/speckit.audiobook draft [CHAPTER_ID]      â† convert one prose chapter to audiodraft
/speckit.audiobook draft all               â† convert all new/stale chapters to audiodraft
/speckit.audiobook voice add [CHARACTER_NAME]  â† add or update a TTS voice assignment
/speckit.audiobook voice list              â† display all current voice assignments
/speckit.audiobook lexicon add [WORD]      â† register a pronunciation entry (IPA + EL substitute)
/speckit.audiobook lexicon list            â† display the full pronunciation lexicon
/speckit.audiobook lexicon export          â† write audiodraft/lexicon.pls (W3C PLS 1.0)
/speckit.audiobook check                   â† find stale and missing audiodrafts vs. prose drafts
/speckit.audiobook status                  â† full audiodraft dashboard
```

#### `speckit.cover`
```
/speckit.cover                             â† interactive: prompts for platform, style, elements
/speckit.cover --platform kdp-ebook        â† KDP ebook (2560Ã—1600 RGB) [default]
/speckit.cover --platform kdp-print        â† KDP print (300 DPI CMYK, spine calculated)
/speckit.cover --platform ingramspark      â† IngramSpark ebook or print
/speckit.cover --platform d2d              â† Draft2Digital (1600Ã—2400 RGB)
/speckit.cover --platform social           â† social media crops (1:1 and 9:16)
/speckit.cover --platform all              â† all platforms, one brief with variant notes
/speckit.cover --style photorealistic      â† photo composite (thriller, crime, romance)
/speckit.cover --style illustrated         â† digital art (fantasy, YA, sci-fi)
/speckit.cover --style painterly           â† oil/watercolour (literary, historical)
/speckit.cover --style minimalist          â† type-led, near-no imagery (literary)
/speckit.cover --style typographic         â† bold type dominates (thriller, contemporary)
/speckit.cover --style dark-moody          â† atmospheric low-key (horror, dark fantasy)
/speckit.cover --style cinematic           â† epic wide-angle silhouette (epic fantasy, sci-fi)
/speckit.cover --style retro-pulp          â† halftone vintage (noir, genre homage)
/speckit.cover --style hand-drawn          â† ink line art (MG, cozy, humour)
/speckit.cover --style abstract            â† conceptual colour field (literary, poetry)
/speckit.cover --include "series-title,tagline,extra-text"  â† add optional elements
/speckit.cover --tagline "Some doors are meant to stay closed."  â† set tagline text
/speckit.cover --extra "Book One of the Ashfall Chronicles"  â† series number label
/speckit.cover --custom "With a foreword by Jane Smith"  â† custom text element
/speckit.cover --platform kdp-print --style cinematic --include "series-title,tagline"  â† combined
/speckit.cover refresh                     â† regenerate image prompt variants, same brief
/speckit.cover prompt-only                 â† output only the AI image prompt, no file written
/speckit.cover brief-only                  â† write cover-brief.md only, no chat prompt output
```

#### `speckit.bio`

```
/speckit.bio                               â† list existing bios (or draft if none set)
/speckit.bio draft                         â† interactive: answer prompts to build canonical short + long bio
/speckit.bio refine                        â† improve existing bio stored in constitution.md
/speckit.bio variant agent                 â† 3rd person â‰¤50w for query-letter bio paragraph
/speckit.bio variant reader                â† 3rd person 100â€“150w for "About the Author" back matter
/speckit.bio variant platform              â† â‰¤25w for KDP/D2D Author Central profile
/speckit.bio variant social                â† â‰¤160 chars for X/Instagram/Bluesky bio field
/speckit.bio variant first-person          â† 80â€“120w 1st person for website/newsletter
/speckit.bio variant long                  â† 200â€“300w 3rd person for press kit / festival programme
/speckit.bio list                          â† display short and long bios from constitution.md
/speckit.bio set short [text]              â† save short bio to constitution.md Â§ VII
/speckit.bio set long [text]               â† save long bio to constitution.md Â§ VII
```

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
| `synopsis-template.md` | One-page (250â€“350 words) and full (1,000â€“2,000 words) synopsis in present tense |
| `glossary-template.md` | Invented terms, proper nouns, capitalization rules, consistency log |
| `subplots-template.md` | Subplot beat sheets: inciting incident through resolution, main plot intersection map, Convergence Map, Arc Absence Log â€” managed by `speckit.subplot` |
| `research-template.md` | Open questions, source notes, world-building facts, resolved findings |
| `timeline-template.md` | Chapter-by-chapter chronology, elapsed time, scene durations, continuity cross-refs |
| `world-building-template.md` | Setting rules, geography, culture, history, in-world systems |
| `locations-template.md` | Per-location sensory anchors, atmosphere, character behavioral tells, state log |
| `themes-template.md` | Thematic contract: motif registry, symbol tracker, chapter thematic map, drift log |
| `feedback-template.md` | Beta/editorial feedback: raw notes, categorized issues, severity, revision tasks |
| `query-letter-template.md` | Query letter: hook, story body, housekeeping, comp titles, bio, submission tracker |
| `cover-brief-template.md` | Cover design brief: elements, colour palette, typography zones, 3 AI image prompts (hero/environment/symbol), platform specs, print spine calculation |

---

## Tutorials

### Tutorial: Single POV Novel

A single POV novel uses one viewpoint character throughout. This is the simplest architecture and the best starting point for first novels.

#### Step 1 â€” Establish the Story Bible

```
/speckit.constitution
```

Choose your **style mode**:

- **`author-sample`** â€” Paste 500â€“2,000 words from a book or story you've written (or want to emulate). The AI extracts 8 voice markers: POV, tense, rhythm, vocabulary register, sensory density, tone, dialogue style, and anti-patterns.
- **`humanized-ai`** â€” Use the built-in anti-AI craft ruleset: sensory grounding, character-in-body principles, dialogue subtext rules, filter-word purge.

Choose your **plot structure**: Three-Act Structure, Save the Cat, Hero's Journey, Story Circle, Fichtean Curve, or custom.

This creates `.specify/memory/constitution.md` â€” the governing authority for all subsequent commands.

#### Step 2 â€” Write the Story Brief

```
/speckit.specify A 19th-century lighthouse keeper starts receiving telegrams from a ship that sank twenty years ago.
```

The AI produces `spec.md` with:
- A two-sentence **logline**
- **Character arcs** with priorities (P1 = protagonist, P2+ = supporting)
- **Scene beats** in Given/When/Then format
- **Plot requirements** and reader experience goals

#### Step 3 â€” Clarify Before Planning

```
/speckit.clarify
```

Scans `spec.md` for `[NEEDS CLARIFICATION]` markers and ambiguities across:
- Character motivation (why does the keeper not destroy the telegrams?)
- Timeline (when does Act II break happen?)
- POV clarity (how close is the narrative distance?)
- World-building inconsistencies

Writes resolutions directly back into `spec.md`. **Do not skip this step** â€” ambiguities here multiply into structural problems downstream.

#### Step 4 â€” Build the Story Structure

```
/speckit.plan
```

Reads `spec.md` and `constitution.md`, produces `plan.md` with:
- Act/phase breakdown aligned to your chosen plot structure
- Chapter-by-chapter map with estimated word counts
- Story bible compliance check gates
- Supporting document map (which templates to populate)

#### Step 5 â€” Generate Scene Tasks

```
/speckit.tasks
```

Reads `plan.md` and `spec.md`, produces `tasks.md` with:
- Scene-by-scene tasks ordered by act
- A research phase at the top (tasks marked `[BLOCKED]` until research documents exist)
- Critical checkpoint markers between acts
- A polish pass block at the end

#### Step 6 â€” Structural Check (Pre-Draft)

```
/speckit.analyze
```

Read-only verification that `spec.md` â†’ `plan.md` â†’ `tasks.md` coverage is complete. No file modifications. Fix any gaps before drafting.

#### Step 7 â€” Generate and Approve Scene Outlines

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
- Set `status: APPROVED` â†’ AI drafts the chapter from this outline
- Set `status: SKIP` â†’ you write the chapter yourself; AI skips it entirely

#### Step 8 â€” Draft

```
/speckit.implement
```

Executes tasks in order. For each chapter:
- If an outline file exists with `status: APPROVED` â†’ uses it as the working brief (overrides `plan.md`)
- If an outline file exists with `status: DRAFT` â†’ **stops** with an outline gate warning
- If an outline file has `status: SKIP` â†’ marks task done, skips to next chapter
- If no outline file exists â†’ falls back to `plan.md` (no gate)

**Author-written path** â€” generate outline only, no prose:

```
/speckit.implement --outline-only
```

Generates the outline file for the next scene and stops. No `draft/` files are written. You write the chapter in `draft/` manually, then run `speckit.checklist` as normal.

#### Step 9 â€” Quality Loop (per chapter)

```
/speckit.checklist        â† "unit test" the scene
/speckit.revise           â† fix only failing passages (if needed)
/speckit.polish           â† line-edit pass (only after checklist PASS)
```

This loop is identical whether the prose was AI-drafted or author-written.

Repeat for each chapter. Run `speckit.status` at any time for a dashboard view.

---

### Series Workflow

Planning a multi-book series from scratch adds one persistent authority document â€” `series/series-bible.md` â€” that governs canon, character state, and continuity constraints across all books. Every per-book command reads from it automatically.

#### One-Time Series Setup

Run this once before any individual book is planned:

```
/speckit.series init
```

This gathers the series-level parameters interactively:

| Parameter | Purpose |
|---|---|
| Series title | Used to pre-fill every book's spec and constitution |
| Total book count | Can be `open series` if undetermined |
| Genre + Target audience | Pre-filled into each book's constitution â€” confirm or override per book |
| Overarching dramatic question | The series-level spine; must not be fully answered until the final book |
| Overarching theme | Stated as a question |
| Series POV strategy | Consistency rule across all books |
| Series tense | Consistency rule across all books |
| Series ending contract | What the ending must feel like or resolve â€” not what happens |

Creates: `series/series-bible.md`

#### Per-Book Cycle

Repeat these steps for every book. The order is fixed â€” each step feeds the next.

```
Step 1 â€” speckit.constitution
```
Reads `series/series-bible.md` and pre-fills genre, audience, POV strategy, and tense â€” you only confirm or override. Set style mode, prose profile, plot structure, and tone.

```
Step 2 â€” speckit.specify
```
Reads `series/series-bible.md` and pre-fills series title, book position, and opening character states. The story idea is written as a brief shaped by the craft rules from Step 1.

```
Step 3 â€” speckit.plan
```
Reads both `spec.md` and `constitution.md` (both required). Generates all supporting documents in Phase 0, then builds the beat sheet and scene outline in Phases 1â€“3. Verifies `series/series-bible.md` and adds the new book entry automatically.

```
Step 4 â€” speckit.analyze
```
Pre-draft structural alignment check â€” confirms spec â†” plan â†” tasks consistency before any prose is written. Read-only.

Then follow the standard [drafting loop](#drafting-scenes-with-tasks): `outline â†’ implement â†’ checklist â†’ revise â†’ polish`.

#### Between Books

After a book's draft is finalized:

```
/speckit.series update N
```

Syncs `series/series-bible.md` with what actually happened in Book N â€” new world canon, new continuity constraints, resolved threads, and updated character arc closing states that become Book N+1's opening states.

Then, before writing anything for Book N+1:

```
/speckit.series audit
```

Cross-book continuity check across all books. **This is a mandatory gate** â€” CRITICAL issues in the series bible must be fixed before the next brief is written. Validates:
- Character state chain: closing state of Book N must match opening state in Book N+1
- World canon consistency: every `SC-NNN` rule across all drafts
- Continuity constraint chain: `STC-NNN` constraints forward from their establishment book
- Unresolved series threads: open `ST-NNN` items with no pay-off book assigned

Once audit is clean, start the per-book cycle again at Step 1.

#### Full Lifecycle

```
series init
    â”‚
    â–¼
constitution â—„â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
    â”‚                                                                        â”‚
    â–¼                                                                        â”‚
specify                                                                      â”‚
    â”‚                                                               series audit
    â–¼                                                                        â–²
plan â†’ analyze                                                               â”‚
    â”‚                                                               series update
    â–¼                                                                        â–²
outline â†’ implement â†’ checklist â†’ revise â†’ polish                           â”‚
    â”‚                                                                        â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ continuity â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”˜
                           (repeat for each book)
```

#### Workspace Structure

A series project uses this layout:

```
<workspace-root>/
â”œâ”€â”€ series/
â”‚   â””â”€â”€ series-bible.md              â† series-level canon, shared across all books
â”‚
â””â”€â”€ specs/
    â”œâ”€â”€ 001-book-1-[title]/           â† created by speckit.specify
    â”‚   â”œâ”€â”€ spec.md
    â”‚   â”œâ”€â”€ plan.md
    â”‚   â”œâ”€â”€ tasks.md
    â”‚   â”œâ”€â”€ characters/               â† each profile has a Series Arc State table
    â”‚   â”œâ”€â”€ draft/
    â”‚   â”œâ”€â”€ outlines/
    â”‚   â””â”€â”€ .specify/memory/
    â”‚       â””â”€â”€ constitution.md       â† has ## IX. Series Context mirroring series-bible.md
    â”‚
    â””â”€â”€ 002-book-2-[title]/
        â””â”€â”€ ...
```

Book directory names (`NNN-book-N-[title]`) are created automatically by `speckit.specify` for non-standalone books.

#### Switching Between Books

To work on a different book in the series, open its folder as the VS Code workspace root:

```
File â†’ Open Folder â†’ specs/002-book-2-[title]/
```

All commands resolve `.specify/memory/constitution.md`, `spec.md`, `draft/`, `outlines/`, and all other paths relative to the active workspace root â€” so the correct book's files become active automatically. Commands that need `series/series-bible.md` look one level up from the book root to find it.

Each book's constitution is isolated in its own `.specify/memory/constitution.md`. Reopening a previous book's folder restores its full context exactly as you left it.

#### Authority Hierarchy

| Document | Scope | Wins over |
|---|---|---|
| `series/series-bible.md` | All books | Any per-book decision on canon, world rules, character state |
| `.specify/memory/constitution.md` | One book | Any scene, outline, or draft within that book |
| `spec.md` | One book | `plan.md` on story intent |
| `plan.md` | One book | `outlines/*.md` on structural beats |
| `outlines/*.md` | One scene | `draft/*.md` on beat sequence |

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
- **Voice Differentiation Matrix** â€” how each POV character sounds different (vocabulary register, sentence length, sensory focus)
- **POV Schedule** â€” chapter-by-chapter assignment of POV characters
- **Information Asymmetry Map** â€” what each POV character knows and when
- **Convergence Points** â€” scenes where character arcs intersect
- **Relay Rules** â€” how POV handoffs between chapters are handled

#### POV Sub-Commands

```
/speckit.pov audit          â† audit voice differentiation across all POV characters
/speckit.pov schedule       â† generate or validate the chapter-by-chapter POV schedule
/speckit.pov asymmetry      â† check that no POV character knows what they shouldn't
/speckit.pov relay          â† review POV handoff transitions between chapters
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
/speckit.continuity JO3.201â€“JO3.203
```

---

### The Planning Process

The planning phase produces three documents that lock in the story's architecture before a single draft scene is written. The order matters.

```
speckit.constitution  â†’  speckit.specify  â†’  speckit.clarify  â†’  speckit.plan  â†’  speckit.tasks  â†’  speckit.outline
```

**`speckit.constitution`** is a prerequisite for everything else. It encodes:
- Your style mode and extracted/manual voice markers
- Plot structure choice (governs how `plan.md` will be structured)
- Central Dramatic Question
- Prohibited phrases (anti-AI filter applied during `speckit.implement`)

**`speckit.specify`** converts a pitch-length idea into a structured brief. Keep your initial prompt concise â€” one or two sentences. The AI expands it into `spec.md`. You edit `spec.md` directly after.

**`speckit.clarify`** is the most important step to not skip. Gaps in the brief do not disappear when you plan â€” they become structural holes. Run clarify until `spec.md` has no `[NEEDS CLARIFICATION]` markers remaining.

**`speckit.plan`** reads the clarified brief and story bible and produces the full act breakdown. If you're using a non-standard plot structure, specify it during `speckit.constitution` setup.

**`speckit.tasks`** reads `plan.md` and converts every chapter beat into an actionable writing task. Tasks are ordered, prioritized by arc, and blocked where prerequisite documents are missing. Resolve blocked tasks by creating the required supporting documents (characters, world-building, research) before drafting those scenes.

**`speckit.outline`** expands each plan entry into a dedicated, author-editable outline file. This is the bridge between structural planning and prose: plan.md captures *what* happens at the story level; the outline file captures *how* the scene plays out beat by beat, with specific sensory anchors and dialogue requirements. The author's review and approval of each outline is the last checkpoint before AI prose is generated.

---

### Analyze Before You Draft

`speckit.analyze` is a mandatory pre-flight check before `speckit.implement`. It is **strictly read-only** â€” it never modifies files.

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
5. If outline is `SKIP`: marks the task done and moves on â€” no prose generated for that chapter
6. If no outline file: falls back to `plan.md` directly (same behaviour as before `speckit.outline` existed)
7. Drafts the scene into `draft/`

#### Author-Written Mode (`--outline-only`)

```
/speckit.implement --outline-only
```

Generates the outline file for the next unwritten scene and **stops** â€” no prose is produced. The author writes the chapter in `draft/` manually (any tool, any format). The same quality loop (`speckit.checklist` â†’ `speckit.revise` â†’ `speckit.polish`) applies regardless of who wrote the prose.

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
| Triple Purpose | Does every scene serve â‰¥3 narrative functions simultaneously? |
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
/speckit.revise A1.101 "CHR-002 STB-004"     â† specify failure codes
/speckit.revise A1.101 checklists/A1.101_Awakening-checklist.md
```

`speckit.revise` rewrites **only the failing passages**. It does not improve surrounding prose or change passing sections. The result is a versioned file (e.g., `Chapter_v2.md`) with a diff summary.

Do not use `speckit.revise` for structural problems â€” those require changes to `plan.md` and `tasks.md` first.

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

`speckit.polish` is a **linter and formatter**, not a structural tool. Never use it to fix story bible violations, missing triple purpose, or off-balance endings â€” that is `speckit.revise`'s job.

---

### Processing Feedback

Beta-reader, critique-partner, and editorial feedback enters the workflow through `speckit.feedback`.

```
/speckit.feedback feedback-notes.txt --reader-type beta
/speckit.feedback "The pacing in chapters 8â€“12 dragged and I lost interest in Marcus entirely." "Jane Doe" --reader-type cp
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
/speckit.feedback triage          â† re-categorize existing feedback without regenerating tasks
/speckit.feedback tasks           â† generate tasks from an already-triaged log
```

After feedback ingestion:

```
/speckit.revise                   â† address CRITICAL issues first
/speckit.continuity               â† cross-reference feedback against current drafts
/speckit.status                   â† check overall revision progress
```

---

### Glossary, Research & Versions

#### Maintaining the Glossary

`glossary.md` is generated by `speckit.plan` and seeded from `spec.md` and `constitution.md`. Use `speckit.glossary` to keep it current throughout drafting:

```
/speckit.glossary add "the Shatter"          â† register a new invented term
/speckit.glossary audit                       â† find unregistered terms in draft chapters
/speckit.glossary check                       â† scan drafts for spelling/capitalisation violations
/speckit.glossary                             â† status dashboard (coverage, open violations)
```

`speckit.polish` and `speckit.continuity` both enforce the glossary passively. Run `speckit.glossary check` proactively before polishing a chapter to resolve violations before they get flagged.

#### Tracking Research

`research.md` is generated by `speckit.plan` to log all domain knowledge gaps. Use `speckit.research` to close the loop:

```
/speckit.research add "Victorian-era telegraph protocols"
/speckit.research resolve R-003 --finding "..." --source "..."
/speckit.research check A1.101          â† check one chapter for unsupported claims
/speckit.research status                â† dashboard sorted by authenticity risk
```

Unresolved HIGH-priority research items before drafting those chapters are flagged as blockers by `speckit.help`.

---

### Search Index (RAG)

For large projects (50k+ words), maintaining a mental map of every character mention, world detail, and subplot beat becomes difficult. The Fiction Book Writing preset includes a local **Search Index (RAG)** powered by `scripts/python/index.py` to provide offline semantic and keyword search.

#### How it Works

The indexer chunks your project files (specs, plans, drafts, world-building, etc.) into manageable pieces and stores them in a local vector or keyword database (`.specify/index/`).

- **Semantic Search**: Understands meaning (e.g., searching for "sadness" finds "tears on her cheek"). Requires `chromadb` and `sentence-transformers`.
- **Keyword Search**: Uses BM25 or basic TF scoring as a zero-dependency fallback.

#### Commands

NOTE: These CLI commands are included in the SpeckIt commands. Just for reference

The RAG index is managed via terminal commands (using your Python environment):

```powershell
# 1. Build the initial index (run once your core planning is done)
python scripts/python/index.py build

# 2. Incrementally update the index (run after drafting or significant edits)
python scripts/python/index.py update

# 3. Query the index
python scripts/python/index.py query "how does the protagonist react to fire?"
python scripts/python/index.py query "ancient magic rules" --type world
python scripts/python/index.py query "Elowen" --type draft --top 10

# 4. Check status and staleness
python scripts/python/index.py status
```

#### Backends

1.  **ChromaDB** (Recommended): Provides true semantic search. Enabled by installing:
    `pip install chromadb sentence-transformers`
2.  **BM25**: Better than basic keyword search. Enabled by installing:
    `pip install rank-bm25`
3.  **Basic TF**: A built-in, zero-dependency keyword search that works out-of-the-box.

You can configure your backend preference and path in the **Tooling** section of your `constitution.md`.

---

#### Managing Draft Versions

Each `speckit.revise` and `speckit.polish` run produces a versioned file (`_v2.md`, `_v3.md`, â€¦). Use `speckit.versions` to navigate the history:

```
/speckit.versions list A1.101           â† version timeline for one chapter
/speckit.versions diff A1.101           â† narrative diff: latest vs. previous version
/speckit.versions diff A1.101 v1 v3     â† diff two specific versions
/speckit.versions log                   â† cross-chapter revision history by date
/speckit.versions tag A1.101 v2 beta-reader-1   â† milestone tag for the sent version
```

#### Series Management

For multi-book projects, use `speckit.series` to manage the series bible:

```
/speckit.series init                    â† scaffold series/series-bible.md (before Book 1)
/speckit.series audit                   â† cross-book canon, arc chains, unresolved threads
/speckit.series update 1                â† sync bible after completing Book 1
/speckit.series status                  â† series-wide dashboard
```

#### Workflow Navigation

Start every session with `speckit.help` if you are unsure what to do next:

```
/speckit.help                           â† full guidance report for current project state
/speckit.help "Is my spec ready to plan?"
/speckit.help "I'm stuck after chapter 3"
/speckit.help --chapter A2.201         â† focused advice for one chapter
```

---

### Synopsis & Query Letter

#### Writing the Synopsis

Run `speckit.synopsis` after `speckit.plan` to get an outline-based synopsis, or after drafting for post-draft accuracy.

```
/speckit.synopsis
```

Produces `synopsis.md` with two formats:

- **One-page synopsis** (250â€“350 words) â€” the compressed arc, present tense, third person, ending revealed. Required in most query packages.
- **Full synopsis** (1,000â€“2,000 words) â€” beat-by-beat account of every major plot turn and character arc resolution. Required on partial/full manuscript requests.

Both formats explicitly reveal the ending. A synopsis is not a blurb.

```
/speckit.synopsis one-page        â† regenerate only the 250â€“350 word version
/speckit.synopsis full            â† regenerate only the full 1,000â€“2,000 word version
/speckit.synopsis update          â† regenerate from current draft (post-draft accuracy)
/speckit.synopsis check           â† validate existing synopsis.md against spec.md and plan.md
```

#### Writing the Query Letter

Run `speckit.synopsis` first â€” `speckit.query` reads `synopsis.md` as its story body source.

```
/speckit.query draft
```

Produces a `query-letter.md` in 250â€“350 words following the industry-standard four-section format:

1. **Personalization** â€” why this specific agent (left blank, add manually per submission)
2. **Hook** â€” protagonist + inciting incident + stakes (â‰¤50 words)
3. **Body** â€” setup, escalation, central dramatic question (~200 words)
4. **Housekeeping** â€” word count, genre, comp titles, bio, credentials

Log submissions and suggest comparable titles:

```
/speckit.query update             â† add a submission log entry
/speckit.query track              â† view submission tracker table
/speckit.query comp-titles        â† generate comp title suggestions only
/speckit.query "Sarah Jensen at Foundry Literary"  â† generate personalization paragraph
```

### Export

#### Exporting the Manuscript

Requires [pandoc](https://pandoc.org) installed separately.

```
/speckit.export                   â† DOCX (default, submission-ready)
/speckit.export epub              â† EPUB (KDP / Draft2Digital / IngramSpark)
/speckit.export latex             â† LaTeX (typeset)
```

Chapter assembly logic:
- Prefers `<CHAPTER_ID>_<Title>_polished.md` over base drafts
- Sorts chapters by `chapter_id` from frontmatter
- Highest version number wins (e.g., `_v3.md` beats `_v2.md`)

#### Metadata Resolution

All export metadata is read automatically from `constitution.md Â§ VII` â€” no manual flags needed unless you want to override:

| Metadata | Source in constitution.md | CLI override |
|---|---|---|
| Author byline | `Author Name` | `--author "Jane Smith"` |
| Language (`dc:language`) | `Language` (BCP-47 code) | `--lang de` |
| Copyright (`dc:rights`) | `Copyright` | `--rights "Â© 2026 Jane Smith"` |
| "About the Author" | `Author Bio (Long)` | `--author-bio "..."` / `--no-author-bio` |

If `Language` is not set, the export defaults to `en`. Run `speckit.bio draft` to generate the canonical author bio before exporting if you want an "About the Author" section appended.

#### Platform Presets

| Platform flag | Output format | Use case |
|---|---|---|
| *(default)* | DOCX Shunn | Agent/publisher manuscript submission |
| `--platform smashwords` | DOCX | Smashwords aggregator (minimal styles) |
| `--platform kdp` | EPUB | Amazon KDP (cover required for listing) |
| `--platform ingramspark` | EPUB | IngramSpark + accessibility + optional ISBN |
| `--platform d2d` | EPUB | Draft2Digital (no embedded cover) |
| `--platform kdp-print-6x9` | LaTeX | KDP Print 6"Ã—9" |
| `--platform ingramspark-6x9` | LaTeX | IngramSpark 6"Ã—9" (PDF/X-1a notes) |



---

## POV Modes Reference

| Mode | POV Count | Rotation Pattern | When to Use |
|---|---|---|---|
| **Single POV** | 1 | N/A | Best for intimate, psychological narratives |
| **Alternating** | 2â€“4 | Strict rotation between chapters | Parallel storylines converging toward a common climax |
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

Paste 500â€“2,000 words from your own writing or a target author. `speckit.constitution` extracts 8 style markers automatically:

1. **POV & Tense** â€” narrative distance and temporal mode
2. **Rhythm** â€” typical sentence length and cadence patterns
3. **Vocabulary Register** â€” formal vs. colloquial, period-appropriate
4. **Sensory Density** â€” frequency and type of sensory detail
5. **Tone** â€” emotional temperature and irony level
6. **Dialogue Style** â€” attribution patterns, subtext density
7. **Anti-Patterns** â€” specific phrasings to avoid (extracted from sample)
8. **Scene Integrity Rules** â€” structural habits in the sample text

### Humanized AI Prose (`humanized-ai`)

Uses the built-in craft ruleset for AI-generated prose that reads as human-crafted. The following **universal principles** apply in all profiles â€” they cannot be disabled:

| Principle | Rule |
|---|---|
| Sensory grounding | Minimum one non-visual sense per scene |
| Character-in-body | Physical reactions precede named emotions |
| Dialogue subtext | Deflection or misunderstanding in every exchange |
| Filter word purge | No `she noticed`, `he felt`, `she saw`, `he heard` |
| Off-balance ending | Every scene ends in a new instability |
| Triple purpose | Every scene serves â‰¥3 narrative functions simultaneously |
| Dirt Rule | Every environment has at least one flaw or imperfection |
| Anti-AI Filter | Prohibited phrases list (universal + profile-specific) |

#### Prose Profiles

When using `humanized-ai`, choose a **Prose Profile** to set how the universal principles are weighted. All profiles enforce all universal principles â€” they differ in sentence rhythm, sensory density, interiority depth, dialogue subtext intensity, and pacing bias.

| Profile | Best For | Sentence Rhythm | Sensory Density | Interiority | Pace Bias |
|---|---|---|---|---|---|
| **`commercial`** | General fiction, fantasy, romance | Alternating short/long | Medium | Balanced | Scene = Sequel |
| **`literary`** | Literary fiction, character studies | Long-dominant; fragments under rupture | High (texture) | Deep, contradictory | Reflection-forward |
| **`thriller`** | Thrillers, crime, horror | Short-dominant (1â€“2 clauses) | Low-medium, functional | Minimal; act-before-reflect | Action-forward |
| **`atmospheric`** | Gothic, horror, weird fiction | Long, winding, syntactically embedded | Maximum; environment as character | Deep; inner/outer blur permitted | Atmosphere as plot |
| **`dark-realist`** | Noir, social realism, gritty literary | Clipped, declarative, no ornament | Medium; decay and failure bias | Cold, selective; rationalisation visible | Consequence-forward |

Each profile also adds its own genre-specific Anti-AI filter entries. Examples:

- **`commercial`** adds: `"a world turned upside down"` Â· `"everything changes when"`
- **`literary`** adds: `"liminal"` Â· `"ineffable"` Â· `"the weight of"` Â· `"something shifted inside her"`
- **`thriller`** adds: `"heart pounding"` Â· `"adrenaline surged"` Â· `"every instinct screamed"`
- **`atmospheric`** adds: `"an oppressive silence"` Â· `"the darkness seemed alive"` Â· `"she could feel the history"`
- **`dark-realist`** adds: `"broken but not beaten"` Â· `"found her strength"` Â· `"at the end of the day"`

Set the profile using `speckit.constitution` â€” it will prompt for the choice when initialising `humanized-ai` mode.

---

## Export Formats

| Format | Use Case | Requirements |
|---|---|---|
| **DOCX** | Publisher/agent submissions, Word compatibility | pandoc â‰¥ 2.11 |
| **EPUB** | KDP, Draft2Digital, IngramSpark, Kobo | pandoc â‰¥ 2.11 |
| **LaTeX** | Professional typesetting, print-on-demand | pandoc â‰¥ 2.11 + LaTeX distribution |

Install pandoc: [pandoc.org/installing.html](https://pandoc.org/installing.html)

All export metadata (author byline, language, copyright, "About the Author" back matter) is read automatically from `constitution.md Â§ VII`. No manual configuration is required for standard exports. See the [Export tutorial](#export) for the full metadata resolution table and CLI overrides.

**Language support**: Set `Language` in `constitution.md Â§ VII` to a BCP-47 code (`en`, `de`, `fr`, `es`, `it`, `pt`, `nl`, `ja`, `zh`, `fi`, `hu`, `tr`). The code is passed as `dc:language` to EPUB, as `lang` metadata to DOCX/LaTeX, and gates English-only prose checks in `speckit.polish` and `speckit.statistics`. See [Language Support](#language-support) for full details.

---

## Language Support

Set `Language` in `constitution.md Â§ VII` to a [BCP-47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt) language code. This single field propagates through the entire pipeline:

| BCP-47 Code | Language |
|---|---|
| `en` | English (default) |
| `de` | German |
| `fr` | French |
| `es` | Spanish |
| `it` | Italian |
| `pt` | Portuguese |
| `nl` | Dutch |
| `ja` | Japanese |
| `zh` | Chinese |
| `fi` | Finnish |
| `hu` | Hungarian |
| `tr` | Turkish |

### What the Language field controls

| Command / Output | Effect |
|---|---|
| `speckit.implement` | All drafted prose is written in the set language |
| `speckit.outline` | Scene outlines are written in the set language |
| `speckit.polish` | English-only rules (WR-001, WR-004, DI-001, DI-002) are suppressed when Language â‰  `en`; a note explains which checks were skipped |
| `speckit.statistics` | Fleschâ€“Kincaid readability score is suppressed when Language â‰  `en` (not valid for non-English prose) |
| `speckit.audiobook` | `xml:lang` attribute set on `<speak>` and `<lexicon>` SSML elements; warning issued if TTS voice model may not support the language |
| `speckit.cover` | Tagline length target: â‰¤8 words for analytic languages; â‰¤4 compound words for agglutinative languages (de, nl, fi, hu, tr) |
| `speckit.query` | If Language = `de`: generates German ExposÃ© format (Anschreiben + ExposÃ© body + Leseprobe) instead of English query letter |
| `speckit.export` (EPUB) | Passed as `dc:language` metadata; sets pandoc `--metadata lang=<code>` |
| `speckit.export` (DOCX/LaTeX) | Passed as pandoc `lang` metadata |
| `audiobook-draft-template.md` | `xml:lang` placeholder pre-filled from Language |

### Setting the language

Run `speckit.constitution` and set the `Language` field in Section VII, or edit `constitution.md` directly:

```yaml
language: de
```

The CLI `--lang` flag overrides `constitution.md` for a single export run without changing the stored value:

```
/speckit.export epub --lang de
```

## Comparable Products

**General-purpose LLMs (ChatGPT, Claude, Gemini direct)**

Most writers using AI are just chatting with these directly â€” "write chapter 3", "make this better". ChatGPT Projects and Claude Projects now offer persistent memory and context management, which helps with session continuity. What they still lack is a consistency *model*: no quality gates, no structural governance, no constitution-based authority that every command obeys. Chapter 10 can still sound nothing like chapter 1 unless you manually enforce the rules in every prompt. This preset's architecture removes that manual burden and replaces it with automated enforcement.

**Sudowrite â€” the closest real competitor**

Sudowrite is purpose-built for fiction, has a chapter-by-chapter approach, and has the most polish of any dedicated tool. Where this preset wins: structural governance. Sudowrite helps you write scenes but doesn't enforce that the scenes are structurally coherent with the plan, that characters are arc-consistent, or that your invented terminology is spelled the same way throughout. It's a creative accelerator; this is a production system. Sudowrite also has no equivalent to the quality gates â€” it will just write whatever you ask.

**NovelAI**

Primarily a continuous text generator, not a workflow tool. Strong on keeping prose in a specific style (model fine-tuning approach rather than rule approach). No structural planning, no version management, no quality gates. Different use case entirely â€” closer to a co-author than a workflow system.

**Scrivener + AI plugins**

Scrivener is still the best document management tool for long-form writing. This preset has no file browser, no corkboard, no compile system. The two are complementary, not competing â€” speckit.export via pandoc covers the export gap but doesn't replace Scrivener's organizational model. A writer using this preset still needs something to manage raw files.

**ProWritingAid / AutoCrit / Hemingway**

These are manuscript analyzers, not AI writers. They catch passive voice, overused words, pacing issues. speckit.polish and speckit.checklist cover some of the same ground but from a craft principle angle rather than a statistical frequency angle. These tools are better at surface-level prose quality; this system is better at structural and voice-consistency enforcement.

**Plottr / Fictionary / Campfire**

Planning tools, not AI writers. Plottr is excellent for outlining. This preset's speckit.plan + speckit.outline + speckit.analyze covers equivalent structural ground but is AI-generated and directly connected to the drafting pipeline â€” the outline isn't a separate document you maintain manually, it becomes the working brief for prose generation.

**The honest gap vs. Sudowrite specifically**

Sudowrite's "Shrink Ray", "Describe", and "Brainstorm" features are genuinely better at in-the-moment creative assistance â€” the micro-level stuff. If you're stuck on one paragraph, Sudowrite is faster. This preset is better when the problem is the whole book â€” consistency, structure, arc tracking, series management across 80,000â€“300,000 words.

**The positioning in one sentence**

Most AI writing tools are accelerators (write faster). This preset is a production system (write consistently, at publishable quality, with structural integrity). That's a different â€” and currently underserved â€” market. The writers who will get the most value are those who've already discovered that raw AI writing creates a mess at novel scale.

---

## Related Resources

- [Spec Kit Documentation](https://github.com/andreasdarsa/spec-kit)
- [Spec-Driven Development Overview](../../spec-driven.md)
- [Preset Development Guide](../ARCHITECTURE.md)
- [Publishing a Preset](../PUBLISHING.md)
