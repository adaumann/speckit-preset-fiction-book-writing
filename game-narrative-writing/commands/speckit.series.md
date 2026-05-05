---
description: Series management command — init the series bible before Entry 1, audit cross-entry continuity, sync the series bible after an entry ships, and display a series-wide status dashboard. Operates on series/series-bible.md as the single authority for cross-entry canon.
handoffs:
  - label: Specify Next Entry
    agent: speckit.specify
    prompt: Create a narrative design doc for the next entry in the series
    send: true
  - label: Run Entry Continuity
    agent: speckit.continuity
    prompt: Run a full continuity check on the current entry's nodes
    send: true
  - label: Validate Carry-Over Variables
    agent: speckit.series
    prompt: validate
    send: true
---

# speckit.series

Manage series-level continuity for multi-entry game narratives. Operates on `series/series-bible.md` as the single authority for cross-entry canon.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* — display the series status dashboard (same as `status`)
- `init` — scaffold `series/series-bible.md` as a new series founding document
- `audit` — run a full cross-entry continuity check (read-only)
- `audit [N-M]` — audit only entries N through M
- `update [N]` — sync `series/series-bible.md` after entry N is completed
- `status` — display the series-level dashboard
- `draft` — (legacy) generate or update series-bible.md from current entry's endings and variables
- `validate` — check that all carry-over variables are declared and reachable in ending states
- `questionnaire` — generate the new-game questionnaire for importing state from a previous entry
- `delta` — compute the world state delta between two entries given a carry-over import

Optional flags:
- `--entry [N]` — scope to a specific entry number
- `--ending [END-ID]` — assume a specific ending as the import state for `questionnaire` or `delta`
- `--canonical` — use the canonical ending (from `series-bible.md`) for `delta`

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_series` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Scope Boundaries

- `speckit.series` does **not** check within-entry node quality, hook correctness, or variable continuity within a single entry — that is `speckit.continuity` and `speckit.analyze`.
- `audit` and `status` are strictly **read-only**. No files are modified.
- `update` writes only to `series/series-bible.md` and NPC state tables. Nothing else.

## Mode Resolution

| Argument | Mode |
|---|---|
| `init` | Init — create the series bible |
| `audit` / `audit N-M` | Audit — cross-entry read-only check |
| `update N` | Update — sync after entry N ships |
| `status` / *(empty)* | Status — dashboard |
| `draft` | Draft — populate from current entry's endings/variables |
| `validate` | Validate — check carry-over variable coverage |
| `questionnaire` | Questionnaire — generate player import screen |
| `delta` | Delta — compute world-state change between entries |

In all modes except `init`: locate `series/series-bible.md`. If not found, abort with:
```
? series/series-bible.md not found.
  Run `speckit.series init` to create it.
```

---

## Mode: Init

**Purpose**: Create `series/series-bible.md` as the founding document before Entry 1 is planned.

If `series/series-bible.md` already exists, abort:
```
? series/series-bible.md already exists. Edit it directly, or use: speckit.series update [N]
```

Ask the following (accept from `$ARGUMENTS` if present, otherwise ask interactively):

1. **Series title**
2. **Total entry count** — number of planned entries, or "open series"
3. **Genre / tone** — (e.g. "Dark fantasy interactive fiction")
4. **Target audience**
5. **Overarching dramatic question** — one sentence; the series-level spine not fully answered until the final entry
6. **Overarching theme** — stated as a question
7. **Engine target** — Sugarcube / Ink / other (consistent across entries or varies)
8. **Carry-over strategy** — save-file import / questionnaire / both
9. **Series ending contract** — what the final entry must deliver (not what happens — what it must resolve)

Generate `series/series-bible.md` from `series-bible-template.md`. Create `series/` directory if absent.

Confirm:
```
? Created: series/series-bible.md
  Series  : [SERIES_TITLE]
  Entries : [count or open]
  Next step: Run `speckit.specify` to create the narrative design doc for Entry 1.
```

---

## Mode: Audit

**Purpose**: Cross-entry continuity check. Strictly read-only.

Resolve scope from `$ARGUMENTS`: range (`audit N-M`) or all entries.

For each entry in scope, load: `specs/spec.md`, `specs/plan.md`, `specs/variables.md`, `specs/endings.md`, `specs/characters/` profiles, `.specify/memory/constitution.md`. Note missing files as INCOMPLETE.

**Run these checks**:

**A. NPC State Chain Validation**
- For each NPC in the carry-over variable registry: the closing state after Entry N must match the opening state in Entry N+1's character profile. Mismatch ? **CRITICAL**.
- Any NPC whose state table is missing a row for an entry where they appear ? **WARNING**.

**B. Carry-Over Variable Coverage**
- For each carry-over variable: confirm it is set on at least one path to each ending that exports it. Not set on any path ? **CRITICAL**.
- Confirm the variable is declared in Entry N+1's `variables.md` with a valid default. Missing ? **CRITICAL**.

**C. Series World Rules**
- For each `SWR-NNN` row: check that no drafted node in any scoped entry contradicts it. Violation ? **CRITICAL**.

**D. Unresolved Series Threads**
- For each `ST-NNN` row with `Status: OPEN` whose planned pay-off entry is within scope and has drafted nodes: check whether any node delivers the resolution. Not found ? **WARNING**.
- Thread with no planned pay-off assigned ? **WARNING**.

**E. Known Contradictions**
- Any `CON-NNN` row with `Status: OPEN` whose entries fall in scope ? **CRITICAL**.

**F. Ending Canon Coverage**
- Any ending in `series-bible.md` Ending Canon Table with `Status: OPEN` carry-over support but no drafted node delivering it ? **WARNING**.

**G. Series Arc Pacing**
- Any entry with `Status: in-progress` or later that has no declared arc contribution in the Per-Entry Arc table ? **WARNING**.
- Final planned entry with no series dramatic question contribution ? **WARNING**.

Output:
```
???????????????????????????????????????????????????????
  SERIES AUDIT REPORT
  Series  : [SERIES_TITLE]
  Scope   : Entries [N]–[M]
  Date    : [YYYY-MM-DD]
???????????????????????????????????????????????????????

### CRITICAL Issues
- [Code]: [description] — [suggested action]

### WARNINGS
- [Code]: [description] — [suggested action]

### PASS
- [dimension]: OK

### Summary
CRITICAL: N | WARNINGS: N | PASS: N
Recommended action: [proceed / resolve contradictions / update series-bible.md]
???????????????????????????????????????????????????????
```

---

## Mode: Update

**Purpose**: Sync `series/series-bible.md` after entry N ships. Writes to series-bible.md and NPC state tables only.

1. **NPC State Registry sync**: for each NPC with a state row in `characters/`: read closing state after Entry N. If incomplete, prompt for each field. Copy into series-bible.md NPC Survival Registry.

2. **New world rules**: prompt — "What world rules were definitively established in Entry N?" Add each as `SWR-NNN` (auto-increment).

3. **New carry-over variables**: prompt — "Were any new variables added to carry-over in Entry N?" Add to Carry-Over Variable Registry.

4. **New series threads**: load open narrative threads from Entry N. For each new series-level thread, add `ST-NNN` row. For threads planned to pay off in Entry N, ask and mark RESOLVED or update pay-off entry.

5. **Known contradictions**: prompt — "Any new continuity issues to log?" Add as `CON-NNN`.

6. **Update Entries table**: set Entry N status to `released` (or as specified). Prompt for `Key arc closed` and `Key thread opened` if empty.

7. Confirm:
```
???????????????????????????????????????????????????????
  SERIES BIBLE UPDATED — Entry [N]: [ENTRY_TITLE]
???????????????????????????????????????????????????????
  NPC state rows updated  : N
  New world rules (SWR)   : N
  New series threads (ST) : N
  Resolved threads        : N
  Entry status            : ? released / in-progress

  Next: speckit.series audit ? speckit.specify (Entry [N+1])
???????????????????????????????????????????????????????
```

---

## Mode: Status

**Purpose**: Series-wide dashboard. Read-only.

```
???????????????????????????????????????????????????????
  SERIES STATUS: [SERIES_TITLE]
  [Total entries planned / open series]
  Dramatic question: [first 80 chars]
???????????????????????????????????????????????????????

### Entries
| # | Title | Status | Nodes | Endings | Carry-over vars |
|---|---|---|---|---|---|
| 1 | [TITLE] | released | N | N | N vars |
| 2 | [TITLE] | in-progress | N | — | — |

### Open Series Threads
| ID | Description | Introduced | Pay-off |
|---|---|---|---|
| ST-001 | [description] | Entry 1 | Entry 3 |
(N threads open / M total)

### Known Contradictions
| ID | Conflict | Entries | Status |
|---|---|---|---|
| CON-001 | [description] | 1, 2 | OPEN |
(N open / M total)

### Series Arc
| Entry | Q answered | Q opened |
|---|---|---|
| 1 | [partial answer] | [new question] |
| 2 | — | — |

Series ending contract: [SET / NOT YET WRITTEN]
???????????????????????????????????????????????????????
```

If any `CON-NNN` contradictions are OPEN, append:
```
??  Action recommended: Run `speckit.series audit` to check cross-entry continuity.
```

---

## Mode: Draft (Legacy)

1. Load `endings.md` — extract all variable state snapshots per ending.
2. Load `variables.md` — identify variables flagged as carry-over (scope: series).
3. Generate or update `series/series-bible.md` using `series-bible-template.md`.

---

## Mode: Validate

1. For each carry-over variable in `series-bible.md`: confirm declared in `variables.md`; confirm set on at least one path to each ending that carries it; confirm default value is valid per type.
2. Report: "Carry-over validation: [N] passed, [N] failed."
3. Flag: variables in series-bible.md missing from `variables.md`; endings with no achievable carry-over state.

---

## Mode: Questionnaire

1. Load the carry-over variable registry from `series-bible.md`.
2. For each variable with `import_method: questionnaire`: generate a player-facing question mapping answers to variable values.
3. Output the questionnaire as a structured list suitable for an in-game new-game-plus setup screen.

---

## Mode: Delta

1. Load the specified ending's variable state snapshot (or canonical ending if `--canonical`).
2. Compare against Entry N+1's starting variable defaults.
3. Report all differences: variables that change, NPCs whose state differs from default, world rules that need overriding.
4. Output a delta block for inclusion in the series bible's world state delta table.

---

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_series` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

