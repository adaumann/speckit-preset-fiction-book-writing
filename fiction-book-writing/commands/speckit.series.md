---
description: Series management command  init the series bible before Book 1, audit cross-book continuity across all drafted books, sync the series bible after a book is completed, and display a series-wide status dashboard. Operates on series/series-bible.md as the single authority for cross-book canon. Supports carry-over mechanics: validate, questionnaire, and delta modes for multi-book imports.
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
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* Ã¢â‚¬â€ display the series status dashboard (same as `status`)
- `init` Ã¢â‚¬â€ scaffold `series/series-bible.md` as a new series founding document
- `audit` Ã¢â‚¬â€ run a full cross-book continuity check across all books (read-only)
- `audit [N-M]` Ã¢â‚¬â€ audit only books N through M (e.g. `audit 1-3`)
- `update [N]` Ã¢â‚¬â€ sync `series/series-bible.md` after book N is completed or drafted (e.g. `update 2`)
- `status` Ã¢â‚¬â€ display the series-level dashboard- `validate`  check that all carry-over variables are declared and reachable in all ending states (read-only)
- `questionnaire`  generate a player-facing new-game-plus import interview based on carry-over variables
- `delta [N]`  compute the world state delta (changes) between Book N and Book N+1 based on canonical vs carry-over imports

Optional flags:
- `--ending [END-ID]`  for `questionnaire` or `delta`, assume a specific book ending (default: canonical ending)
- `--target [N]`  for `delta`, compute delta into Book N (default: N+1)
---

## Purpose

`speckit.series` is the lifetime management command for a multi-book series. It operates exclusively on `series/series-bible.md` as the series-level authority document.

**What each mode covers**:

| Mode | When to use | Writes files? |
|---|---|---|
| `init` | Before planning Book 1 Ã¢â‚¬â€ found the series | Yes (creates `series/series-bible.md`) |
| `audit` | Before planning a new book, or at any time | No Ã¢â‚¬â€ strictly read-only |
| `update [N]` | After a book's draft is finalized | Yes (series-bible.md + character Arc State tables) |
| `status` | Any time Ã¢â‚¬â€ live series-wide overview | No Ã¢â‚¬â€ strictly read-only || `validate` | After updating carry-over variables in series-bible.md | No  strictly read-only |
| `questionnaire` | Generate player import UI for new-game-plus | No  generates UI spec (not a file write) |
| `delta [N]` | Generate import state briefing for next book | No  strictly read-only |
**Scope boundaries**:
- `speckit.series` does **not** check prose quality, character voice, or scene-level continuity within a single book Ã¢â‚¬â€ that is `speckit.continuity`.
- `speckit.series` does **not** check pre-draft spec/plan alignment within a single book Ã¢â‚¬â€ that is `speckit.analyze`.
- `audit` and `status` are strictly read-only. No files are modified.
- `update` writes only to `series/series-bible.md` and to character `## X. Series Arc State` tables in `characters/[name].md` files of the target book. Nothing else.

---

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_series` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 Ã¢â‚¬â€ Setup and Mode Resolution

Resolve the workspace root path by reading the project structure.

Resolve the **run mode** from `$ARGUMENTS`:
- `init` Ã¢â€ â€™ go to **Mode: Init**
- `audit` or `audit N-M` Ã¢â€ â€™ go to **Mode: Audit**
- `update N` Ã¢â€ â€™ go to **Mode: Update**- `validate` ? go to **Mode: Validate**
- `questionnaire` ? go to **Mode: Questionnaire**
- `delta [N]` ? go to **Mode: Delta**- `status` or *(empty)* Ã¢â€ â€™ go to **Mode: Status**

In all modes except `init`: locate `series/series-bible.md`. If not found, abort with:
```
Ã¢Å“ series/series-bible.md not found.
  Run `speckit.series init` to create it, or run `speckit.plan` on the first
  non-standalone book Ã¢â‚¬â€ it will create the skeleton automatically.
```

Locate all book directories by scanning `specs/` for subdirectories matching the pattern `NNN-book-N-*/`. Parse the book number N from the directory name. Build the **Book Directory Map**: `{ book_number Ã¢â€ â€™ directory_path }`.

If no `specs/` directories match the book pattern, note: `No book directories found matching the specs/NNN-book-N-* convention.`

---

## Mode: Init

**Purpose**: Create `series/series-bible.md` as a creative founding document before any individual book is planned.

### Init Step 1 Ã¢â‚¬â€ Pre-flight check

If `series/series-bible.md` already exists, abort with:
```
Ã¢Å“ series/series-bible.md already exists. To update series parameters, edit it directly.
  To sync after completing a book, use: speckit.series update [N]
```

### Init Step 2 Ã¢â‚¬â€ Gather series parameters

Ask the following questions. For each, accept a value from `$ARGUMENTS` if present; otherwise ask interactively:

1. **Series title** Ã¢â‚¬â€ the published series name (e.g. "The Shattered Key Chronicles")
2. **Total book count** Ã¢â‚¬â€ number of planned books, or "open series" if undetermined
3. **Genre** Ã¢â‚¬â€ primary genre (e.g. "Epic Fantasy", "Literary Fiction")
4. **Target audience** Ã¢â‚¬â€ age group and reader type (e.g. "Adult readers of character-driven fantasy")
5. **Overarching dramatic question** Ã¢â‚¬â€ one sentence; the series-level spine that must not be fully answered until the final book
6. **Overarching theme** Ã¢â‚¬â€ stated as a question (e.g. "Is the cost of justice ever too high to pay?")
7. **Series POV strategy** Ã¢â‚¬â€ how POV is handled across all books (e.g. "Consistent single-POV protagonist throughout" / "POV shifts between books as declared per constitution.md")
8. **Series tense** Ã¢â‚¬â€ consistent tense across all books, or notes on variances
9. **Series ending contract** Ã¢â‚¬â€ what the ending MUST deliver (not what happens Ã¢â‚¬â€ what it must feel like or resolve)

### Init Step 3 Ã¢â‚¬â€ Scaffold the series bible

Generate `series/series-bible.md` from `series-bible-template.md`. Populate all nine answers into their corresponding fields. Leave per-book fields (Books in Series table rows beyond Book 1, Character State Registry, Unresolved Series Threads) as template placeholders Ã¢â‚¬â€ they will be populated by `speckit.plan` and `speckit.series update`.

Create the `series/` directory if it does not exist.

Confirm:
```
Ã¢Å“â€œ Created: series/series-bible.md
  Series     : [SERIES_TITLE]
  Books      : [count or open]
  Next step  : Run `speckit.specify` to create the story brief for Book 1.
               The book directory will be named specs/001-book-1-[title]/ automatically.
```

**Handoff Ã¢â‚¬â€ init mode only**: Display the full Book 1 sequence:
```
Next steps for Book 1 (in order):

  Step 1: speckit.constitution
    Set the story bible Ã¢â‚¬â€ style mode, prose profile, plot structure, POV strategy, tone.
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

Do not display the audit, update, or status handoffs at this stage Ã¢â‚¬â€ they are not relevant until a book exists.

---

## Mode: Audit

**Purpose**: Cross-book continuity check across all books in the series (or a scoped range).

**This mode is strictly read-only. No files are modified.**

### Audit Step 1 Ã¢â‚¬â€ Scope resolution

If `$ARGUMENTS` contains a range (`audit N-M`): restrict analysis to books N through M only. Confirm scope before proceeding:
```
Auditing series: [SERIES_TITLE]
Scope          : Books [N]Ã¢â‚¬â€œ[M] ([count] books)
```

If no range: audit all books present in the Book Directory Map.

### Audit Step 2 Ã¢â‚¬â€ Load all book assets

For each book in scope, load the following if they exist (skip silently if absent, note in report):

- `spec.md` Ã¢â‚¬â€ story brief, series position, character arcs
- `plan.md` Ã¢â‚¬â€ structure, open threads
- `.specify/memory/constitution.md` Ã¢â‚¬â€ story bible, `## IX. Series Context`
- `characters/` Ã¢â‚¬â€ all character profiles; specifically `## X. Series Arc State` tables
- `tasks.md` Ã¢â‚¬â€ for thread pay-off verification

Flag any book in scope that is missing `spec.md` as `INCOMPLETE` in the report Ã¢â‚¬â€ analysis for that book will be partial.

### Audit Step 3 Ã¢â‚¬â€ Run cross-book checks

**A. Character State Chain Validation**

For every character that appears in two or more books in scope:

1. Read each book's `## X. Series Arc State` row for that character (from `characters/[name].md` in each book directory).
2. Walking chronologically: the `After Book N` row's values must match the opening state implied by Book N+1's character profile and spec arcs.
3. Any mismatch between closing state of Book N and what Book N+1's character profile declares Ã¢â€ â€™ **CRITICAL**: `CHN-NNN: [CharacterName] state mismatch between Book N close and Book N+1 open Ã¢â‚¬â€ [field]: expected "[value]", found "[value]"`.
4. Any character whose `## X. Series Arc State` table is missing a row for a book where that character appears as a major arc Ã¢â€ â€™ **WARNING**: `CHN-NNN: [CharacterName] Series Arc State not logged for Book N`.

**B. World Canon Consistency**

For every `SC-NNN` row in `## Series Canon`:

1. For each book in scope that has drafts: check whether any drafted chapter contradicts the canon rule.
   - If the book has no drafts: check whether `spec.md` or `plan.md` implies a violation.
2. Any contradiction Ã¢â€ â€™ **CRITICAL**: `SCC-NNN: SC-[ID] violated in Book N, [chapter_id] Ã¢â‚¬â€ [detail]`.
3. Any `SC-NNN` row that has no `Established in` value Ã¢â€ â€™ **WARNING**: `SCC-NNN: SC-[ID] has no source Ã¢â‚¬â€ cannot verify establishment`.

**C. Continuity Constraint Chain**

For every `STC-NNN` row in `## Series Continuity Constraints` whose `Must hold from` value falls within the audit scope:

1. For each book in scope at or after `Must hold from`: check drafted chapters, spec arcs, and plan decisions for violations.
2. Any violation Ã¢â€ â€™ **CRITICAL**: `STC-NNN: constraint violated in Book N Ã¢â‚¬â€ [detail]`.

**D. Unresolved Series Threads**

For every `ST-NNN` row in `## Unresolved Series Threads` with `Status: OPEN`:

1. Check whether the `Planned pay-off` book is within the audit scope AND has drafts.
2. If the pay-off book is drafted but contains no scene that delivers the thread's resolution:
   Ã¢â€ â€™ **WARNING**: `STR-NNN: ST-[ID] pay-off planned for Book N but not found in any drafted chapter Ã¢â‚¬â€ verify or update Planned pay-off`.
3. If the `Planned pay-off` column is empty Ã¢â€ â€™ **WARNING**: `STR-NNN: ST-[ID] has no planned pay-off assigned`.
4. If the `Introduced in` book has been drafted but the thread introduction scene cannot be located Ã¢â€ â€™ **WARNING**: `STR-NNN: ST-[ID] introduction scene not found in Book N drafts`.

**E. Known Contradictions**

For every `SX-NNN` row in `## Known Contradictions` with `Status: OPEN` whose `Books affected` includes any book in scope:
Ã¢â€ â€™ **CRITICAL**: `SXC-NNN: Known contradiction SX-[ID] is OPEN Ã¢â‚¬â€ [conflict description] Ã¢â‚¬â€ resolve before drafting affected books`.

**F. Series Arc Pacing**

Load `## Per-Book Arc Contribution`. For each book row:

1. If both `Partial question answered` and `New question opened` are empty for any book with `Status: in-progress` or later Ã¢â€ â€™ **WARNING**: `ARC-NNN: Book N has no declared arc contribution Ã¢â‚¬â€ update series-bible.md ## Per-Book Arc Contribution`.
2. If any book except the final planned book has `New question opened` empty Ã¢â€ â€™ **WARNING**: `ARC-NNN: Book N closes questions but opens none Ã¢â‚¬â€ risk of series arc deflating prematurely`.
3. If the final planned book's `Partial question answered` is empty Ã¢â€ â€™ **WARNING**: `ARC-NNN: Final book arc contribution not declared`.
4. If the `## Series Ending Contract` field is `[SERIES_ENDING_CONTRACT]` or empty Ã¢â€ â€™ **WARNING**: `ARC-NNN: Series ending contract not written Ã¢â‚¬â€ reader promise is undefined`.

**G. Named Entity Registry Staleness**

For every row in `## Named Entity Registry`:

1. Determine the most recently drafted book for that entity's active range.
2. If `Last updated in` is earlier than the most recently drafted book where that entity appears Ã¢â€ â€™ **WARNING**: `NER-NNN: [EntityName] last updated in Book N but appears in later drafted books Ã¢â‚¬â€ verify canonical status is current`.

### Audit Step 4 Ã¢â‚¬â€ Output report

```
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â
  SERIES AUDIT REPORT
  Series  : [SERIES_TITLE]
  Scope   : Books [N]Ã¢â‚¬â€œ[M] ([count] books audited)
  Date    : [YYYY-MM-DD]
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â

### Book Coverage
| Book | Dir | spec.md | drafts | constitution | Series Arc State tables |
|---|---|---|---|---|---|
| 1 | specs/001-book-1-Ã¢â‚¬Â¦/ | Ã¢Å“â€œ | N chapters | Ã¢Å“â€œ | 2 characters logged |
Ã¢â‚¬Â¦

### CRITICAL Issues
- [Code]: [description] Ã¢â‚¬â€ [suggested action]
Ã¢â‚¬Â¦

### WARNINGS
- [Code]: [description] Ã¢â‚¬â€ [suggested action]
Ã¢â‚¬Â¦

### PASS
- [dimension]: no issues

### Summary
CRITICAL: N | WARNINGS: N | PASS: N
Recommended action: [proceed to plan next book / resolve SX-NNN contradictions / update series-bible.md]
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â
```

---

## Mode: Update

**Purpose**: Sync `series/series-bible.md` after a book's draft is finalized. Captures closing states, new canon, new threads.

**Writes to**: `series/series-bible.md` and `characters/[name].md ## X. Series Arc State` tables in the target book only.

### Update Step 1 Ã¢â‚¬â€ Identify target book

Parse the book number N from `$ARGUMENTS`. Locate the book directory from the Book Directory Map. If not found, abort with:
```
Ã¢Å“ No directory found for Book [N] in specs/. Expected pattern: specs/NNN-book-N-*/
```

Load the book's `spec.md`, `plan.md`, `characters/` profiles, and `## Unresolved Series Threads` from `series/series-bible.md`.

Confirm:
```
Syncing series bible after Book [N]: [BOOK_TITLE]
Directory: [path]
```

### Update Step 2 Ã¢â‚¬â€ Character State Registry sync

For each character with a `## X. Series Arc State` table in `characters/[name].md`:

1. Read the `After Book [N]` row. If it does not exist or contains only `[NEEDS CLARIFICATION]` values, prompt:
   > "[CharacterName] Ã¢â‚¬â€ Book [N] closing state is incomplete. Please provide:
   > - Relationship status:
   > - Physical state:
   > - Knowledge state:
   > - Arc position:
   > - Emotional state:
   > - Notes:"
   Accept values and write them back to the `After Book [N]` row in `characters/[name].md`.

2. Copy the completed `After Book [N]` row into the corresponding character block in `series/series-bible.md ## Character State Registry`. If the character block does not exist in the registry, create it.

### Update Step 3 Ã¢â‚¬â€ Capture new world canon

Prompt:
> "What world rules were definitively established in Book [N] that all future books must honor?
> Enter each as a rule statement, one per line. Press Enter twice to finish.
> (Leave blank to skip)"

For each rule provided: add a new `SC-NNN` row to `## Series Canon` (auto-increment the ID from the highest existing SC number + 1). Set `Established in` to `Book [N]`.

### Update Step 4 Ã¢â‚¬â€ Capture new continuity constraints

Prompt:
> "What character knowledge disclosures, relationship changes, or world-state facts were established in Book [N]
> that future books must not contradict?
> Describe each constraint Ã¢â‚¬â€ who knows what, what relationship has changed, what fact is now canon.
> One per line. Press Enter twice to finish.
> (Leave blank to skip)"

For each constraint: add a new `STC-NNN` row (auto-increment from highest existing STC + 1). Set `Established at` to `Book [N]` and `Must hold from` to `Book [N+1] onward`.

### Update Step 5 Ã¢â‚¬â€ New series threads

Load `plan.md ## Open Narrative Threads` from the target book. For each thread:

1. Check whether it already exists in `## Unresolved Series Threads` (match by description or thread ID).
2. If new: prompt Ã¢â‚¬â€ "Is '[thread description]' a series-level thread that future books must pay off? (y/n)".
   - If yes: add as a new `ST-NNN` row (auto-increment). Set `Introduced in` to `Book [N]`. Set `Planned pay-off` to the author's stated book, or `[TBD]` if unknown.
3. If already listed: verify `Status` is still `OPEN`; if the pay-off appeared in this book, ask the author to confirm and mark it `RESOLVED`.

### Update Step 6 Ã¢â‚¬â€ Close resolved threads

List all `OPEN` `ST-NNN` rows whose `Planned pay-off` is `Book [N]`. For each, ask:
> "Thread ST-[ID]: '[description]' was planned to pay off in Book [N]. Was it resolved? (y / n / partial)"

- `y` Ã¢â€ â€™ set Status to `RESOLVED`
- `partial` Ã¢â€ â€™ keep `OPEN`, update Notes
- `n` Ã¢â€ â€™ keep `OPEN`, prompt to update `Planned pay-off` to a later book

### Update Step 7 Ã¢â‚¬â€ Update Books in Series table

Update the target book's row in `## Books in Series`:
- Set `Status` to `drafted` (unless the author specifies `published`)
- Prompt for `Key arc closed` and `Key thread opened` if empty

### Update Step 8 Ã¢â‚¬â€ Update Per-Book Arc Contribution

If `## Per-Book Arc Contribution` is missing the Book [N] row or has it empty, prompt:
> "Book [N] arc contribution:
> - Partial question answered:
> - New question opened:"

Fill the values.

### Update Step 9 Ã¢â‚¬â€ Confirm and report

```
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â
  SERIES BIBLE UPDATED Ã¢â‚¬â€ Book [N]: [BOOK_TITLE]
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â

  Character State Registry   : [N] characters updated
  New world canon (SC-NNN)   : [N] rules added
  New constraints (STC-NNN)  : [N] constraints added
  New series threads (ST-NNN): [N] threads added
  Resolved threads            : [N] marked RESOLVED
  Books in Series             : Book [N] status Ã¢â€ â€™ [drafted/published]

  Ã¢Å¡Â Ã¯Â¸Â  Review new SC / STC rows in series/series-bible.md before planning Book [N+1].
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â
```

**Handoff Ã¢â‚¬â€ update mode only**: Display the following next-steps in order. The audit step is mandatory before briefing the next book:

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
    series/series-bible.md Ã¢â‚¬â€ confirm or override per-book as needed.
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
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â
  SERIES STATUS: [SERIES_TITLE]
  [Total books planned / open series]
  Overarching question: [first 80 chars]
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â

### Books
| # | Title          | Status      | Word count | Arc closed | Threads opened |
|---|----------------|-------------|------------|------------|----------------|
| 1 | [TITLE]        | drafted     | 94,200     | [arc]      | [N] threads    |
| 2 | [TITLE]        | in-progress | 31,000     | Ã¢â‚¬â€          | Ã¢â‚¬â€              |
| 3 | [TITLE]        | planned     | Ã¢â‚¬â€          | Ã¢â‚¬â€          | Ã¢â‚¬â€              |
```

Word count for each book: sum `actual_words` from all draft chapters in that book's `draft/` directory. If no drafts exist, show `Ã¢â‚¬â€`.

```
### Open Series Threads
| ID     | Description                               | Introduced | Pay-off   |
|--------|-------------------------------------------|------------|-----------|
| ST-001 | [description]                             | Book 1     | Book 3    |
Ã¢â‚¬Â¦
(N threads open / M total)

### Known Contradictions
| ID     | Conflict                                  | Books | Status |
|--------|-------------------------------------------|-------|--------|
| SX-001 | [description]                             | 1, 2  | OPEN   |
Ã¢â‚¬Â¦
(N open / M total)

### Series Arc Completeness
| Book | Q answered                      | Q opened                        |
|------|---------------------------------|---------------------------------|
| 1    | [partial answer]                | [partial question]              |
| 2    | Ã¢â‚¬â€                               | Ã¢â‚¬â€                               |
Ã¢â‚¬Â¦

Series ending contract: [SET / NOT YET WRITTEN]
Ã¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€ÂÃ¢â€Â
```

If there are any `OPEN` `SX-NNN` contradictions or more than 0 `CRITICAL` issues detectable from the status scan, append:

```
Ã¢Å¡Â Ã¯Â¸Â  Action recommended: Run `speckit.series audit` to check cross-book continuity.
```

---
## Mode: Validate

**Purpose**: Check that all carry-over variables are properly declared and achievable across all book endings.

**This mode is strictly read-only. No files are modified.**

### Validate Step 1  Load carry-over registry

Load `## Carry-Over Variable Registry` from `series/series-bible.md`. For each variable row:

1. Verify that the variable is declared in `specs/001-book-1-*/variables.md` with:
   - Type matching the registry (character_state, relationship, trust_score, flag, etc.)
   - Default value present and valid per type
   - If import_method includes "questionnaire": the variable must have a questionnaire_label or similar metadata

2. If missing or misconfigured ? **CRITICAL**: `CVR-NNN: [Variable] is in Carry-Over Registry but not properly declared in variables.md`

### Validate Step 2  Check reachability in endings

For each variable with `import_method: save-file` or `import_method: questionnaire`:

1. Load `specs/001-book-1-*/endings.md`. For each ending in the `## Endings` table:
2. Determine the variable's state at that ending by tracing the plot: is it set on at least one path to this ending?
3. If not set on any path ? **WARNING**: `CVR-NNN: [Variable] cannot reach ending [END-ID]  no path sets it`

### Validate Step 3  Canonical import state

Load `## Canonical Import State` from `series/series-bible.md`. For each line in the `canonical_import:` block:

1. Verify the variable is listed in the Carry-Over Registry
2. Verify the value is a valid option for that variable's type
3. If the canonical ending specified (e.g., `ending_imported: END-A`) exists in Book 1 endings ? OK
4. If canonical ending does not exist ? **CRITICAL**: `CVR-NNN: Canonical import state references non-existent ending [END-ID]`

### Validate Step 4  Output report

```
---------------------------------------------------------------------------------------
  CARRY-OVER VALIDATION REPORT
  Series  : [SERIES_TITLE]
  Date    : [YYYY-MM-DD]
---------------------------------------------------------------------------------------

### Carry-Over Variables
| Variable | Type | Declared | Default valid | Reachable in all endings | Import method |
|---|---|---|---|---|---|
| [name] | [type] | ? | ? | ? | save-file |
â€¦

### CRITICAL Issues
- [Code]: [description]  [suggested action]

### WARNINGS
- [Code]: [description]  [suggested action]

### Summary
CRITICAL: N | WARNINGS: N | PASS
Carry-Over validation: [N] passed, [N] failed
---------------------------------------------------------------------------------------
```

If all checks pass: "All carry-over variables are valid and reachable. Book 2 can safely be planned with multi-book imports enabled."

---

## Mode: Questionnaire

**Purpose**: Generate a player-facing new-game-plus interview based on carry-over variables marked for questionnaire import.

**This mode is strictly read-only.**

### Questionnaire Step 1  Load carry-over registry

Load `## Carry-Over Variable Registry` from `series/series-bible.md`. Filter for rows where `Import Method` includes `questionnaire`.

### Questionnaire Step 2  Resolve ending context

If `--ending [END-ID]` is provided on command line: use that ending.
Otherwise: load `## Canonical Import State` and use the ending specified in `ending_imported: [END-ID]` field.

### Questionnaire Step 3  Generate questionnaire structure

For each questionnaire-enabled variable in order:

1. **Load ending state**: If the variable was set in the chosen ending of Book 1, load its value
2. **Generate question**: Create a player-facing multiple-choice or freeform question that maps answers to variable values
   - Examples:
     - Character state: "Where did you leave [Character]?" ? answers map to character_state values
     - Relationship: "How did your relationship with [Character] end?" ? answers map to relationship values
     - Trust score: "How much did [Character] trust you?" ? 5-point slider, maps to trust_score range
3. **Generate responses**: Create readable answer options (e.g., "They parted as allies" instead of "relation_[name]: allied")

### Questionnaire Step 4  Output questionnaire spec

```
---------------------------------------------------------------------------------------
  NEW-GAME-PLUS INTERVIEW  [SERIES_TITLE]
  Importing from: Book 1, ending [END-ID]
  Book 2 opening: [BOOK_2_TITLE]
---------------------------------------------------------------------------------------

## Q1: [Character Name]  Status
**[Question text]**

A) [Response 1] ? char_[name]_state: [value]
B) [Response 2] ? char_[name]_state: [value]
C) [Response 3] ? char_[name]_state: [value]

(Canonical for this ending: Option [X])

---

## Q2: [Relationship Name]
**[Question text]**

A) [Response 1] ? relation_[name]: [value]
B) [Response 2] ? relation_[name]: [value]

(Canonical: Option [X])

---

[Continue per variableâ€¦]

---------------------------------------------------------------------------------------

**Implementation notes for your game engine**:
- Save player responses as variable values in the Book 2 game state
- Missing answers should default to canonical values
- Store all responses in a "import_metadata" table for debugging
---------------------------------------------------------------------------------------
```

---

## Mode: Delta

**Purpose**: Compute and display the world state delta (differences) between Book N ending and Book N+1 opening, showing both canonical and alternate carry-over import scenarios.

**This mode is strictly read-only.**

### Delta Step 1  Parse arguments

From `$ARGUMENTS`:
- Extract source book N (e.g., `delta 1` means delta from Book 1 to Book 2)
- Target book defaults to N+1 (override with `--target M`)
- If `--ending [END-ID]` is provided: use that specific ending as the source state
- Otherwise: load the `## Canonical Import State` to determine canonical ending

### Delta Step 2  Load source and target state models

**Source state** (Book N closing):
- Load `## Ending Canon Table` to determine which Book N ending is the source
- Load `specs/NNN-book-N-*/endings.md` to get variable snapshots at that ending
- Load `## World State Delta Per Book` to see manually documented state changes

**Target state** (Book N+1 opening):
- Load `specs/NNN-book-N+1-*/characters/` and extract opening states for each character
- Load `## Character State Registry` from series-bible.md to determine canonical vs conditional opening states

### Delta Step 3  Compute deltas

For each element in `## World State Delta Per Book` (characters, relationships, locations, factions):

1. **Canonical path**: What world state does Book N+1 expect if the player starts fresh (no import)?
   - Source: Canonical ending of Book N
   - Target: "Book N+1 (canonical)" row in Delta Per Book table

2. **Alt carry-over paths**: What world state results if the player imports a specific alternate ending?
   - For each `Supported Carry-Over Endings` in `## Ending Canon Table`:
     - Source: That alternate ending of Book N
     - Target: "Book N+1 (conditional)" row or conditional state from Character State Registry
   - Compute differences from canonical

### Delta Step 4  Output delta report

```
---------------------------------------------------------------------------------------
  WORLD STATE DELTA: Book [N] ? Book [N+1]
  Canonical ending: [END-ID] (default for fresh start readers)
  Date: [YYYY-MM-DD]
---------------------------------------------------------------------------------------

## Canonical Path (Fresh Start)
### Book [N] closing state (canonical ending [END-ID]):
- [Character] alive, allied
- [Location] under faction control
- [Relationship] resolved

? Book [N+1] opens with:
- [Character] alive, allied (no change expected)
- [Location] under faction control (no change)
- [Relationship] resolved (no change)

---

## Alternate Carry-Over Paths

### If player imported ending [END-B]:
- [Character] dead (DELTA: was alive in END-A)
- [Location] destroyed (DELTA: was under faction control in END-A)
- [Relationship] broken (DELTA: was resolved in END-A)

? Book [N+1] *must* handle:
  - [Character] is dead ? adjust all scenes featuring them
  - [Location] is destroyed ? alternative meeting locations needed
  - [Relationship] is broken ? dialogue branches differ

---

### If player imported ending [END-C]:
- [Character] alive, hostile (DELTA)
- [Relationship] unknown (DELTA)

? Book [N+1] *must* handle:
  - [Character] is now antagonistic ? tone of interactions changes
  - [Relationship] is uncertain ? branching dialogue paths needed

---

## Summary of Required Book [N+1] Handling

| Element | Canonical | END-B import | END-C import |
|---|---|---|---|
| [Character] | alive, allied | dead | alive, hostile |
| [Location] | faction HQ | destroyed | faction HQ |
| [Relationship] | resolved | broken | unknown |

**Writer brief for Book [N+1] drafting**:
- If planning scenes involving [Character] with branching per-import state, prepare:
  - Scene A (canonical): character is alive and allied
  - Scene B (END-B import): character is dead  need replacement NPC or alternate scene
  - Scene C (END-C import): character is hostile  dialogue and choices differ
- Minimum three scenes with conditional player-state gating required for import depth

---------------------------------------------------------------------------------------
```

---
## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_series` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

**Update search index** (optional Ã¢â‚¬â€ large projects):
- If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root.
- Updated `series/series-bible.md` and all `series/*.md` files are re-indexed so `speckit.continuity` and `speckit.constitution` queries reflect the latest series canon.
- If the command fails or the index does not exist, skip silently.

