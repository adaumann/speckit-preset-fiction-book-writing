---
description: Series management command — init the series bible before Book 1, audit cross-book continuity across all drafted books, sync the series bible after a book is completed, and display a series-wide status dashboard. Operates on series/series-bible.md as the single authority for cross-book canon.
handoffs:
  - label: Specify Next Book
    agent: speckit.specify
    prompt: Create a story brief for the next book in the series
    send: true
  - label: Plan Next Book
    agent: speckit.plan
    prompt: Plan the next book in the series using the series bible as context
    send: true
  - label: Update Story Bible
    agent: speckit.constitution
    prompt: Update the story bible for the next book incorporating series context
    send: true
  - label: Run Book Continuity
    agent: speckit.continuity
    prompt: Run a full continuity check on the current book's drafts
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
- *(no argument)* — display the series status dashboard (same as `status`)
- `init` — scaffold `series/series-bible.md` as a new series founding document
- `audit` — run a full cross-book continuity check across all books (read-only)
- `audit [N-M]` — audit only books N through M (e.g. `audit 1-3`)
- `update [N]` — sync `series/series-bible.md` after book N is completed or drafted (e.g. `update 2`)
- `status` — display the series-level dashboard

---

## Purpose

`speckit.series` is the lifetime management command for a multi-book series. It operates exclusively on `series/series-bible.md` as the series-level authority document.

**What each mode covers**:

| Mode | When to use | Writes files? |
|---|---|---|
| `init` | Before planning Book 1 — found the series | Yes (creates `series/series-bible.md`) |
| `audit` | Before planning a new book, or at any time | No — strictly read-only |
| `update [N]` | After a book's draft is finalized | Yes (series-bible.md + character Arc State tables) |
| `status` | Any time — live series-wide overview | No — strictly read-only |

**Scope boundaries**:
- `speckit.series` does **not** check prose quality, character voice, or scene-level continuity within a single book — that is `speckit.continuity`.
- `speckit.series` does **not** check pre-draft spec/plan alignment within a single book — that is `speckit.analyze`.
- `audit` and `status` are strictly read-only. No files are modified.
- `update` writes only to `series/series-bible.md` and to character `## X. Series Arc State` tables in `characters/[name].md` files of the target book. Nothing else.

---

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_series` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Setup and Mode Resolution

Run `{SCRIPT}` from repo root. Parse the workspace root path.

Resolve the **run mode** from `$ARGUMENTS`:
- `init` → go to **Mode: Init**
- `audit` or `audit N-M` → go to **Mode: Audit**
- `update N` → go to **Mode: Update**
- `status` or *(empty)* → go to **Mode: Status**

In all modes except `init`: locate `series/series-bible.md`. If not found, abort with:
```
✗ series/series-bible.md not found.
  Run `speckit.series init` to create it, or run `speckit.plan` on the first
  non-standalone book — it will create the skeleton automatically.
```

Locate all book directories by scanning `specs/` for subdirectories matching the pattern `NNN-book-N-*/`. Parse the book number N from the directory name. Build the **Book Directory Map**: `{ book_number → directory_path }`.

If no `specs/` directories match the book pattern, note: `No book directories found matching the specs/NNN-book-N-* convention.`

---

## Mode: Init

**Purpose**: Create `series/series-bible.md` as a creative founding document before any individual book is planned.

### Init Step 1 — Pre-flight check

If `series/series-bible.md` already exists, abort with:
```
✗ series/series-bible.md already exists. To update series parameters, edit it directly.
  To sync after completing a book, use: speckit.series update [N]
```

### Init Step 2 — Gather series parameters

Ask the following questions. For each, accept a value from `$ARGUMENTS` if present; otherwise ask interactively:

1. **Series title** — the published series name (e.g. "The Shattered Key Chronicles")
2. **Total book count** — number of planned books, or "open series" if undetermined
3. **Genre** — primary genre (e.g. "Epic Fantasy", "Literary Fiction")
4. **Target audience** — age group and reader type (e.g. "Adult readers of character-driven fantasy")
5. **Overarching dramatic question** — one sentence; the series-level spine that must not be fully answered until the final book
6. **Overarching theme** — stated as a question (e.g. "Is the cost of justice ever too high to pay?")
7. **Series POV strategy** — how POV is handled across all books (e.g. "Consistent single-POV protagonist throughout" / "POV shifts between books as declared per constitution.md")
8. **Series tense** — consistent tense across all books, or notes on variances
9. **Series ending contract** — what the ending MUST deliver (not what happens — what it must feel like or resolve)

### Init Step 3 — Scaffold the series bible

Generate `series/series-bible.md` from `series-bible-template.md`. Populate all nine answers into their corresponding fields. Leave per-book fields (Books in Series table rows beyond Book 1, Character State Registry, Unresolved Series Threads) as template placeholders — they will be populated by `speckit.plan` and `speckit.series update`.

Create the `series/` directory if it does not exist.

Confirm:
```
✓ Created: series/series-bible.md
  Series     : [SERIES_TITLE]
  Books      : [count or open]
  Next step  : Run `speckit.specify` to create the story brief for Book 1.
               The book directory will be named specs/001-book-1-[title]/ automatically.
```

**Handoff — init mode only**: Display the full Book 1 sequence:
```
Next steps for Book 1 (in order):

  Step 1: speckit.constitution
    Set the story bible — style mode, prose profile, plot structure, POV strategy, tone.
    series/series-bible.md is now present: genre, audience, POV strategy, and tense
    will be pre-filled from it. You will only be asked to confirm or override.
    speckit.plan reads constitution.md as a required input; run this before plan.

  Step 2: speckit.specify
    Create the story brief for Book 1.
    Series title and Book 1 position will be pre-filled from series/series-bible.md.
    The story brief is shaped by the craft rules established in Step 1.

  Step 3: speckit.plan
    Build the structure plan (beat sheet, scene outline, supporting docs).
    Verifies series/series-bible.md and adds Book 1 to the Books in Series table.
```

Do not display the audit, update, or status handoffs at this stage — they are not relevant until a book exists.

---

## Mode: Audit

**Purpose**: Cross-book continuity check across all books in the series (or a scoped range).

**This mode is strictly read-only. No files are modified.**

### Audit Step 1 — Scope resolution

If `$ARGUMENTS` contains a range (`audit N-M`): restrict analysis to books N through M only. Confirm scope before proceeding:
```
Auditing series: [SERIES_TITLE]
Scope          : Books [N]–[M] ([count] books)
```

If no range: audit all books present in the Book Directory Map.

### Audit Step 2 — Load all book assets

For each book in scope, load the following if they exist (skip silently if absent, note in report):

- `spec.md` — story brief, series position, character arcs
- `plan.md` — structure, open threads
- `.specify/memory/constitution.md` — story bible, `## IX. Series Context`
- `characters/` — all character profiles; specifically `## X. Series Arc State` tables
- `tasks.md` — for thread pay-off verification

Flag any book in scope that is missing `spec.md` as `INCOMPLETE` in the report — analysis for that book will be partial.

### Audit Step 3 — Run cross-book checks

**A. Character State Chain Validation**

For every character that appears in two or more books in scope:

1. Read each book's `## X. Series Arc State` row for that character (from `characters/[name].md` in each book directory).
2. Walking chronologically: the `After Book N` row's values must match the opening state implied by Book N+1's character profile and spec arcs.
3. Any mismatch between closing state of Book N and what Book N+1's character profile declares → **CRITICAL**: `CHN-NNN: [CharacterName] state mismatch between Book N close and Book N+1 open — [field]: expected "[value]", found "[value]"`.
4. Any character whose `## X. Series Arc State` table is missing a row for a book where that character appears as a major arc → **WARNING**: `CHN-NNN: [CharacterName] Series Arc State not logged for Book N`.

**B. World Canon Consistency**

For every `SC-NNN` row in `## Series Canon`:

1. For each book in scope that has drafts: check whether any drafted chapter contradicts the canon rule.
   - If the book has no drafts: check whether `spec.md` or `plan.md` implies a violation.
2. Any contradiction → **CRITICAL**: `SCC-NNN: SC-[ID] violated in Book N, [chapter_id] — [detail]`.
3. Any `SC-NNN` row that has no `Established in` value → **WARNING**: `SCC-NNN: SC-[ID] has no source — cannot verify establishment`.

**C. Continuity Constraint Chain**

For every `STC-NNN` row in `## Series Continuity Constraints` whose `Must hold from` value falls within the audit scope:

1. For each book in scope at or after `Must hold from`: check drafted chapters, spec arcs, and plan decisions for violations.
2. Any violation → **CRITICAL**: `STC-NNN: constraint violated in Book N — [detail]`.

**D. Unresolved Series Threads**

For every `ST-NNN` row in `## Unresolved Series Threads` with `Status: OPEN`:

1. Check whether the `Planned pay-off` book is within the audit scope AND has drafts.
2. If the pay-off book is drafted but contains no scene that delivers the thread's resolution:
   → **WARNING**: `STR-NNN: ST-[ID] pay-off planned for Book N but not found in any drafted chapter — verify or update Planned pay-off`.
3. If the `Planned pay-off` column is empty → **WARNING**: `STR-NNN: ST-[ID] has no planned pay-off assigned`.
4. If the `Introduced in` book has been drafted but the thread introduction scene cannot be located → **WARNING**: `STR-NNN: ST-[ID] introduction scene not found in Book N drafts`.

**E. Known Contradictions**

For every `SX-NNN` row in `## Known Contradictions` with `Status: OPEN` whose `Books affected` includes any book in scope:
→ **CRITICAL**: `SXC-NNN: Known contradiction SX-[ID] is OPEN — [conflict description] — resolve before drafting affected books`.

**F. Series Arc Pacing**

Load `## Per-Book Arc Contribution`. For each book row:

1. If both `Partial question answered` and `New question opened` are empty for any book with `Status: in-progress` or later → **WARNING**: `ARC-NNN: Book N has no declared arc contribution — update series-bible.md ## Per-Book Arc Contribution`.
2. If any book except the final planned book has `New question opened` empty → **WARNING**: `ARC-NNN: Book N closes questions but opens none — risk of series arc deflating prematurely`.
3. If the final planned book's `Partial question answered` is empty → **WARNING**: `ARC-NNN: Final book arc contribution not declared`.
4. If the `## Series Ending Contract` field is `[SERIES_ENDING_CONTRACT]` or empty → **WARNING**: `ARC-NNN: Series ending contract not written — reader promise is undefined`.

**G. Named Entity Registry Staleness**

For every row in `## Named Entity Registry`:

1. Determine the most recently drafted book for that entity's active range.
2. If `Last updated in` is earlier than the most recently drafted book where that entity appears → **WARNING**: `NER-NNN: [EntityName] last updated in Book N but appears in later drafted books — verify canonical status is current`.

### Audit Step 4 — Output report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SERIES AUDIT REPORT
  Series  : [SERIES_TITLE]
  Scope   : Books [N]–[M] ([count] books audited)
  Date    : [YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Book Coverage
| Book | Dir | spec.md | drafts | constitution | Series Arc State tables |
|---|---|---|---|---|---|
| 1 | specs/001-book-1-…/ | ✓ | N chapters | ✓ | 2 characters logged |
…

### CRITICAL Issues
- [Code]: [description] — [suggested action]
…

### WARNINGS
- [Code]: [description] — [suggested action]
…

### PASS
- [dimension]: no issues

### Summary
CRITICAL: N | WARNINGS: N | PASS: N
Recommended action: [proceed to plan next book / resolve SX-NNN contradictions / update series-bible.md]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Mode: Update

**Purpose**: Sync `series/series-bible.md` after a book's draft is finalized. Captures closing states, new canon, new threads.

**Writes to**: `series/series-bible.md` and `characters/[name].md ## X. Series Arc State` tables in the target book only.

### Update Step 1 — Identify target book

Parse the book number N from `$ARGUMENTS`. Locate the book directory from the Book Directory Map. If not found, abort with:
```
✗ No directory found for Book [N] in specs/. Expected pattern: specs/NNN-book-N-*/
```

Load the book's `spec.md`, `plan.md`, `characters/` profiles, and `## Unresolved Series Threads` from `series/series-bible.md`.

Confirm:
```
Syncing series bible after Book [N]: [BOOK_TITLE]
Directory: [path]
```

### Update Step 2 — Character State Registry sync

For each character with a `## X. Series Arc State` table in `characters/[name].md`:

1. Read the `After Book [N]` row. If it does not exist or contains only `[NEEDS CLARIFICATION]` values, prompt:
   > "[CharacterName] — Book [N] closing state is incomplete. Please provide:
   > - Relationship status:
   > - Physical state:
   > - Knowledge state:
   > - Arc position:
   > - Emotional state:
   > - Notes:"
   Accept values and write them back to the `After Book [N]` row in `characters/[name].md`.

2. Copy the completed `After Book [N]` row into the corresponding character block in `series/series-bible.md ## Character State Registry`. If the character block does not exist in the registry, create it.

### Update Step 3 — Capture new world canon

Prompt:
> "What world rules were definitively established in Book [N] that all future books must honor?
> Enter each as a rule statement, one per line. Press Enter twice to finish.
> (Leave blank to skip)"

For each rule provided: add a new `SC-NNN` row to `## Series Canon` (auto-increment the ID from the highest existing SC number + 1). Set `Established in` to `Book [N]`.

### Update Step 4 — Capture new continuity constraints

Prompt:
> "What character knowledge disclosures, relationship changes, or world-state facts were established in Book [N]
> that future books must not contradict?
> Describe each constraint — who knows what, what relationship has changed, what fact is now canon.
> One per line. Press Enter twice to finish.
> (Leave blank to skip)"

For each constraint: add a new `STC-NNN` row (auto-increment from highest existing STC + 1). Set `Established at` to `Book [N]` and `Must hold from` to `Book [N+1] onward`.

### Update Step 5 — New series threads

Load `plan.md ## Open Narrative Threads` from the target book. For each thread:

1. Check whether it already exists in `## Unresolved Series Threads` (match by description or thread ID).
2. If new: prompt — "Is '[thread description]' a series-level thread that future books must pay off? (y/n)".
   - If yes: add as a new `ST-NNN` row (auto-increment). Set `Introduced in` to `Book [N]`. Set `Planned pay-off` to the author's stated book, or `[TBD]` if unknown.
3. If already listed: verify `Status` is still `OPEN`; if the pay-off appeared in this book, ask the author to confirm and mark it `RESOLVED`.

### Update Step 6 — Close resolved threads

List all `OPEN` `ST-NNN` rows whose `Planned pay-off` is `Book [N]`. For each, ask:
> "Thread ST-[ID]: '[description]' was planned to pay off in Book [N]. Was it resolved? (y / n / partial)"

- `y` → set Status to `RESOLVED`
- `partial` → keep `OPEN`, update Notes
- `n` → keep `OPEN`, prompt to update `Planned pay-off` to a later book

### Update Step 7 — Update Books in Series table

Update the target book's row in `## Books in Series`:
- Set `Status` to `drafted` (unless the author specifies `published`)
- Prompt for `Key arc closed` and `Key thread opened` if empty

### Update Step 8 — Update Per-Book Arc Contribution

If `## Per-Book Arc Contribution` is missing the Book [N] row or has it empty, prompt:
> "Book [N] arc contribution:
> - Partial question answered:
> - New question opened:"

Fill the values.

### Update Step 9 — Confirm and report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SERIES BIBLE UPDATED — Book [N]: [BOOK_TITLE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Character State Registry   : [N] characters updated
  New world canon (SC-NNN)   : [N] rules added
  New constraints (STC-NNN)  : [N] constraints added
  New series threads (ST-NNN): [N] threads added
  Resolved threads            : [N] marked RESOLVED
  Books in Series             : Book [N] status → [drafted/published]

  ⚠️  Review new SC / STC rows in series/series-bible.md before planning Book [N+1].
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Handoff — update mode only**: Display the following next-steps in order. The audit step is mandatory before briefing the next book:

```
Recommended next steps for Book [N+1]:

  Step 1 (mandatory): speckit.series audit
    Run a full cross-book continuity audit before writing the next brief.
    This ensures character states, world canon, and unresolved threads from
    Book [N] are correct before they become constraints on Book [N+1].
    Fix any CRITICAL issues in series/series-bible.md first.

  Step 2: speckit.constitution
    Set the story bible for Book [N+1], incorporating series context.
    Genre, audience, POV strategy, and tense will be pre-filled from
    series/series-bible.md — confirm or override per-book as needed.
    speckit.plan reads constitution.md as a required input; run this before plan.

  Step 3: speckit.specify
    Create the story brief for Book [N+1].
    Series title, position, and opening character states will be
    pre-filled automatically from series/series-bible.md.
    The brief is shaped by the craft rules established in Step 2.

  Step 4: speckit.plan
    Build the structure plan. speckit.plan will verify the series bible
    and add Book [N+1] to the Books in Series table automatically.
```

Do not display the status or init handoffs at this stage.

---

## Mode: Status

**Purpose**: Series-wide dashboard. Read-only.

Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SERIES STATUS: [SERIES_TITLE]
  [Total books planned / open series]
  Overarching question: [first 80 chars]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Books
| # | Title          | Status      | Word count | Arc closed | Threads opened |
|---|----------------|-------------|------------|------------|----------------|
| 1 | [TITLE]        | drafted     | 94,200     | [arc]      | [N] threads    |
| 2 | [TITLE]        | in-progress | 31,000     | —          | —              |
| 3 | [TITLE]        | planned     | —          | —          | —              |
```

Word count for each book: sum `actual_words` from all draft chapters in that book's `draft/` directory. If no drafts exist, show `—`.

```
### Open Series Threads
| ID     | Description                               | Introduced | Pay-off   |
|--------|-------------------------------------------|------------|-----------|
| ST-001 | [description]                             | Book 1     | Book 3    |
…
(N threads open / M total)

### Known Contradictions
| ID     | Conflict                                  | Books | Status |
|--------|-------------------------------------------|-------|--------|
| SX-001 | [description]                             | 1, 2  | OPEN   |
…
(N open / M total)

### Series Arc Completeness
| Book | Q answered                      | Q opened                        |
|------|---------------------------------|---------------------------------|
| 1    | [partial answer]                | [partial question]              |
| 2    | —                               | —                               |
…

Series ending contract: [SET / NOT YET WRITTEN]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If there are any `OPEN` `SX-NNN` contradictions or more than 0 `CRITICAL` issues detectable from the status scan, append:

```
⚠️  Action recommended: Run `speckit.series audit` to check cross-book continuity.
```

---

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_series` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

**Update search index** (optional — large projects):
- If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root.
- Updated `series/series-bible.md` and all `series/*.md` files are re-indexed so `speckit.continuity` and `speckit.constitution` queries reflect the latest series canon.
- If the command fails or the index does not exist, skip silently.
