# Series Bible: [SERIES_TITLE]

<!-- SERIES-LEVEL CANON — governs all books in the series.
     Each individual book has its own constitution.md, spec.md, plan.md, and tasks.md.
     This file is the authority on anything that spans books.
     When a per-book decision contradicts this file, this file wins.
     Path: series/series-bible.md (create a series/ directory at the top of your workspace) -->

---

## Workspace Structure
<!-- How a multi-book series workspace is organized.
     Each book is a self-contained spec folder in specs/. The series/ directory is shared.
     speckit.specify names non-standalone book folders with a book-N prefix automatically. -->

```
<workspace-root>/
├── series/
│   └── series-bible.md              ← this file: series-level canon, shared across all books
│
└── specs/
    ├── 001-book-1-[title]/           ← Book 1 (created by speckit.specify)
    │   ├── spec.md                   ← story brief for this book
    │   ├── plan.md                   ← story structure for this book
    │   ├── tasks.md
    │   ├── characters/               ← per-character profiles (each has ## X. Series Arc State)
    │   ├── draft/
    │   ├── outlines/
    │   └── .specify/memory/
    │       └── constitution.md       ← story bible for this book (has ## IX. Series Context)
    │
    └── 002-book-2-[title]/           ← Book 2
        └── ...
```

**Authority hierarchy**:
- `series/series-bible.md` wins over any per-book decision on canon, world rules, and character state.
- Each book's `.specify/memory/constitution.md ## IX. Series Context` mirrors the relevant constraints from this file for that book — it is populated by `speckit.constitution` and should not be edited manually.
- Each character's `## X. Series Arc State` table is the per-character view; the `## Character State Registry` in this file is the series-level authority.

---

## Series Parameters

| Parameter | Value |
|---|---|
| Series title | [SERIES_TITLE] |
| Total book count | [N books / open series] |
| Genre | [NEEDS CLARIFICATION] |
| Target audience | [NEEDS CLARIFICATION] |
| Overarching dramatic question | [The series-level spine — one sentence. Must not be fully answered until the final book.] |
| Overarching theme | [Stated as a question. Each book explores it from a different angle.] |
| Series POV strategy | [Consistent across all books / changes per book — document here] |
| Series tense | [Consistent / changes — document here] |

---

## Series Canon

<!-- Hard facts that are TRUE across all books and cannot be contradicted by a per-book decision.
     Any per-book spec.md, constitution.md, or plan.md that contradicts a canon entry is a conflict.
     speckit.analyze flags these when series position is non-standalone. -->

### World Rules

<!-- Physical, magical, technological, or social rules that apply universe-wide.
     One row per rule. -->

| Canon ID | Rule | Established in |
|---|---|---|
| SC-001 | [e.g., "Magic requires physical cost — no exceptions"] | [Book 1, A1.101] |
| SC-002 | | |

### Named Entity Registry

<!-- Characters, places, factions, and objects that exist across the series.
     Track canonical state so Book 2 doesn't contradict Book 1's ending. -->

| Entity | Type | Canonical status at series start | Last updated in |
|---|---|---|---|
| [Character Name] | Character | [alive / dead / location / relationship status] | [Book N] |
| [Place Name] | Location | [exists / destroyed / renamed] | [Book N] |

### Series Continuity Constraints

<!-- Facts established in earlier books that later books must not violate.
     speckit.analyze cross-references these for non-standalone books. -->

| Constraint ID | Rule | Established at | Must hold from |
|---|---|---|---|
| STC-001 | [e.g., "P1 knows the antagonist's real name from Book 1, Ch.12 onwards"] | Book 1, A3.301 | Book 2 onward |
| STC-002 | | | |

---

## Carry-Over Variable Registry

<!-- Variables and story states that transfer from one book to the next via carry-over mechanisms.
     Import method: save-file = direct import from Book 1 file; questionnaire = player answers on new game.
     speckit.series validate checks all carry-over variables are declared and reachable in Book 1 endings.
     speckit.series questionnaire generates the new-game-plus interview screen. -->

| Variable | Type | Default (fresh start) | Import Method | Affects Book |
|---|---|---|---|---|
| char_[name]_state | character_state | [e.g., "alive"] | save-file / questionnaire | 2, 3 |
| relation_[name] | relationship | [e.g., "estranged"] | save-file / questionnaire | 2 |
| trust_[character] | trust_score | [e.g., "50"] | save-file | 2 |
| ending_[id]_achieved | flag | false | questionnaire | 2 |

---

## Canonical Import State

<!-- The "default save" — assumed choices when reader starts Book N fresh without importing from Book N-1.
     This is the canon used for marketing material, future spin-offs, etc.
     Not all endings need carry-over support; specify which are "canonical" for continuity purposes. -->

### Fresh Start Defaults (Book 2)

```yaml
canonical_import:
  char_[name]_state: alive                    # [RATIONALE]
  relation_[name]: estranged                  # [RATIONALE]
  trust_[character]: 65                       # [RATIONALE]
  ending_imported: END-A                      # [RATIONALE — which Book 1 ending is "canon"]
```

---

## Ending Canon Table

<!-- Which ending(s) are treated as "true" for sequel purposes and carry-over support.
     Not all endings need to be supported as carry-over — mark divergent ones as unsupported.
     This defines what world state Book 2+ readers experience if they start fresh. -->

| Book | Canon Ending | Supported Carry-Over Endings | Unsupported endings | Notes |
|---|---|---|---|---|
| 1 | END-A | END-A, END-B | END-C (secret), END-D | END-C too divergent; END-D requires restricted prior knowledge |
| 2 | [TBD] | | | |

---

## World State Delta Per Book

<!-- How the world changes between books based on reader choices and canonical ending.
     Track both "canon" (fresh start) and "alt carry-over" (imported state) versions.
     Use this to brief the writer on what Book 2 assumes at its start. -->

| Element | Book 1 State | Book 2 State (canon) | Book 2 State (END-B carry-over) |
|---|---|---|---|
| [LOCATION_NAME] | [STATE] | [STATE] | [STATE — if END-B imported] |
| [CHARACTER_NAME] | alive, estranged | dead (END-A) | alive, allied (END-B carry-over) |
| [FACTION_NAME] | neutral | allied | hostile |
| [RELATIONSHIP] | enemies | [STATE] | [STATE] |

---

## Books in Series

<!-- One row per book. Add rows as books are conceived or completed.
     Status: planned / in-progress / drafted / published -->

| # | Working title | Status | Series dramatic question contribution | Key arc closed | Key thread opened |
|---|---|---|---|---|---|
| 1 | [BOOK_1_TITLE] | [status] | [How this book advances the overarching question] | [Arc resolved in this book] | [New thread seeded for later] |
| 2 | [BOOK_2_TITLE] | [status] | | | |

---

## Character State Registry

<!-- CLOSING STATE per character per book.
     These values are the OPENING STATE for the next book.
     "canonical" = opening state when reader starts fresh (no carry-over import)
     "conditional" = opening state when specific ending is imported from prior book
     Updated by speckit.series update after each book draft is finalized.
     Cross-reference each character's `characters/[name].md` for full profile. -->

### [Character Name]

| After Book | Status | Relationship | Physical State | Arc Position | Notes |
|---|---|---|---|---|---|
| Book 1 (canonical) | [e.g., "alive"] | [e.g., "estranged from mentor"] | [e.g., "Injured left hand"] | [e.g., "Wound fresh"] | Default path for fresh start |
| Book 1 (END-B conditional) | [e.g., "alive"] | [e.g., "allied with mentor"] | [e.g., "Fully healed"] | [e.g., "Transformed"] | if END-B imported |
| Book 2 (canonical) | | | | | |
| Book 2 (conditional) | | | | | |

### [Character Name]

*(repeat block per major character)*

---

## Series Arc & Dramatic Question

<!-- The overarching arc is the invisible spine that makes books cohere as a series.
     Each book answers a partial question; the final book answers the full one.
     Fill this progressively — don't force answers you haven't discovered yet. -->

### Overarching Arc
[OVERARCHING_ARC]
<!-- 3–5 sentences. What journey does the series-level protagonist (or the world) take
     across all N books? What starts broken? What does transformation cost? -->

### Per-Book Arc Contribution

| Book | Partial question answered | New question opened |
|---|---|---|
| 1 | [e.g., "Can P1 survive the inciting trauma?"] | [e.g., "Was the inciting event engineered?"] |
| 2 | | |

### Series Ending Contract
<!-- What the reader is promised by the series title, premise, and Book 1. -->
[SERIES_ENDING_CONTRACT]
<!-- Write what the ending MUST deliver — not what happens, but what it must feel like or resolve. -->

---

## Unresolved Series Threads

<!-- Chekhov items and narrative threads seeded across books that have not yet paid off.
     Mark RESOLVED when the pay-off book is drafted. -->

| Thread ID | Description | Introduced in | Planned pay-off | Status |
|---|---|---|---|---|
| ST-001 | [e.g., "The locked room in the antagonist's estate"] | Book 1, A1.103 | Book 3 | OPEN |

---

## Known Contradictions

<!-- Conflicts between the series bible and a per-book decision. Log and resolve.
     Do not delete rows — mark RESOLVED and note the fix. -->

| ID | Conflict | Books affected | Status | Resolution |
|---|---|---|---|---|
| SX-001 | [e.g., "Book 2 plan has P1 in City A; series canon puts them in City B post-Book 1"] | 1, 2 | OPEN | |
