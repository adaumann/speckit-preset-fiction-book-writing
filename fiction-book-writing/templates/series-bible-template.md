# Series Bible: [SERIES_TITLE]

<!-- SERIES-LEVEL CANON — governs all books in the series.
     Each individual book has its own constitution.md, spec.md, plan.md, and tasks.md.
     This file is the authority on anything that spans books.
     When a per-book decision contradicts this file, this file wins.
     Path: series/series-bible.md (create a series/ directory at the top of your workspace) -->

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
     Updated after each book is completed (or drafted).
     Cross-reference each character's `characters/[name].md` for full profile. -->

### [Character Name]

| After Book | Relationship status | Physical state | Knowledge state | Arc position | Emotional state | Notes |
|---|---|---|---|---|---|---|
| Book 1 | [e.g., "Estranged from mentor"] | [e.g., "Injured left hand — permanent"] | [e.g., "Knows antagonist's identity"] | [e.g., "Wound cracked open, not yet healed"] | [e.g., "Grieving, functional"] | |
| Book 2 | | | | | | |

### [Character Name]

*(repeat block)*

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
