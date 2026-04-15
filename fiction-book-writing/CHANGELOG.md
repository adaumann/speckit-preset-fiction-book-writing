# Changelog

All notable changes to the Fiction Book Writing preset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.4.1] - Current

### Changed
- `speckit.brainstorm` — significant improvements to the interactive loop:
  - **Session length modes**: `quick` (~5 Qs), `standard` (~10 Qs, default), `deep` (unlimited); depth gate surfaces a stopping point when the limit is reached
  - **Resume support**: detects prior `brainstorm-[topic].md` notes and offers to load them as additional context or start fresh
  - **Challenge mode**: `challenge` argument inverts question priority to stress-test existing file decisions rather than fill gaps
  - **Secondary context loading**: each topic silently loads related files (e.g. `characters` brainstorm also loads `spec.md` and `themes.md`) to prevent redundant questions and surface cross-topic conflicts
  - **`!skip` command**: skip any question without answering; skipped questions do not count toward the depth limit
  - **Expanded question banks**: `pov` (5→10 questions), `research` (4→9), `glossary` (3→8)
  - **Wildcard bank**: 8 topic-agnostic generative questions drawn once core gaps are covered
  - **Specific synthesis guidance** in Step 4b: acknowledgements must name a narrative function, a tension, or an affected scene beat — generic filler is explicitly prohibited
  - **Merge output option**: after a multi-topic session (`switch` used), produces a single cross-topic file with a `Cross-Topic Connections` section
  - **Change Candidates Status column**: `PENDING` → `APPLIED` / `SKIPPED` / `EDITED` tracked during Step 6 review
  - **Blank-slate template population**: when creating a topic file from a template, replaces `[NEEDS CLARIFICATION]` tokens with brainstorm insights; leaves all other placeholders intact
  - **New handoffs**: `speckit.clarify` and `speckit.pov` added to frontmatter
  - **Operating Rules**: three new rules — depth is binding, acknowledgements must be specific, prior session data is read-only

---

## [1.4.0]

### Added
- `speckit.outline` command — generates editable per-scene outline files with opening hook, causal beat sequence, character beats, dialogue requirements, sensory anchors, and thematic work
- `scene-outline-template.md` — template for per-scene outlines with status gate (`DRAFT` / `APPROVED` / `SKIP`)
- `--outline-only` flag for `speckit.implement` — generates outline and stops; author writes prose manually
- Outline gate in `speckit.implement` — drafting stops on `status: DRAFT` outlines; skips `status: SKIP` chapters
- `speckit.continuity` command — post-draft story bible compliance, character arc consistency, and timeline coherence analysis
- `subplots-template.md` — subplot beat sheets with main plot intersection map
- `themes-template.md` — thematic contract, motif registry, symbol tracker, and chapter thematic map
- `locations-template.md` — per-location sensory anchors, atmosphere, character tells, and state log
- `series-bible-template.md` — series-level canon, world rules, and character state registry per book
- `glossary-template.md` — invented terms, proper nouns, capitalization rules, and consistency log
- `timeline-template.md` — chapter-by-chapter chronology, elapsed time, and continuity cross-references
- `research-template.md` — open questions, source notes, world-building facts, and resolved findings
- `synopsis-template.md` — one-page and full synopsis in present tense
- `query-letter-template.md` — query letter with submission tracker
- `feedback-template.md` — beta/editorial feedback log with severity tiers
- `agent-file-template.md` — living context file for active characters, world state, and open threads

### Changed
- `speckit.implement` outline gate behaviour: falls back to `plan.md` when no outline file is present (backwards-compatible)
- README expanded with full workflow tutorials, POV modes reference, plot structure table, style modes detail, and export format docs

---

## [1.2.0]

### Added
- `speckit.pov` command with sub-commands: `draft`, `audit`, `schedule`, `asymmetry`, `relay`
- `pov-structure-template.md` — POV configuration, voice differentiation matrix, POV schedule, and information asymmetry map
- Support for 8 POV modes: alternating, dual, braided, ensemble, mosaic, frame+embedded, chorus, first-person-multiple
- `speckit.query` command with sub-commands: `draft`, `update`, `track`, `comp-titles`
- `speckit.export` command (pandoc-based) supporting DOCX, EPUB, and LaTeX output formats
- `export.py` script for chapter assembly with version-aware file selection
- `speckit.feedback` command with sub-commands: `triage`, `tasks`
- `speckit.continuity` command for post-draft multi-POV consistency auditing
- `characters-index-template.md` — character roster with role, affiliations, and first appearance

### Changed
- `speckit.status` now reports per-chapter word counts (actual vs. estimated) and outstanding quality gates
- `speckit.revise` accepts chapter ID, failure codes, and checklist file path as arguments

---

## [1.1.0]

### Added
- `speckit.constitution` command — story bible creation with style mode selector and plot structure choice
- `constitution-template.md` — style mode, voice markers, craft principles, and prohibited phrases list
- `humanized-ai` style mode with five prose profiles: `commercial`, `literary`, `thriller`, `atmospheric`, `dark-realist`
- `author-sample` style mode — extracts 8 voice markers from a provided writing sample
- Universal craft principles applied across all prose profiles (sensory grounding, filter word purge, off-balance ending, triple purpose, dirt rule)
- Profile-specific anti-AI phrase filters
- `speckit.analyze` command — read-only pre-draft structural alignment check
- `speckit.checklist` command — per-scene quality gates (triple purpose, off-balance ending, embodied emotion, dialogue subtext, sensory anchoring, prohibited phrases)
- `speckit.polish` command — line-edit pass (sentence rhythm, filter words, adverb density, weak verbs, voice register drift)
- `checklist-template.md`
- Support for Fichtean Curve and In Medias Res plot structures

### Changed
- `speckit.plan` reads `constitution.md` to align act breakdown with chosen plot structure
- `speckit.implement` reads prohibited phrase list from `constitution.md` during drafting

---

## [1.0.0]

### Added
- Initial release of the Fiction Book Writing preset
- Core commands: `speckit.specify`, `speckit.clarify`, `speckit.plan`, `speckit.tasks`, `speckit.implement`, `speckit.revise`, `speckit.status`
- Base templates: `spec-template.md`, `plan-template.md`, `tasks-template.md`, `characters-template.md`, `world-building-template.md`
- Support for Three-Act Structure, Save the Cat, Hero's Journey, and Story Circle plot frameworks
- Single POV support
- Given/When/Then scene beat format in `spec.md`
