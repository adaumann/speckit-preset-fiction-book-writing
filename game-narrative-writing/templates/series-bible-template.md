# Series Bible: [SERIES_NAME]

<!-- SERIES-LEVEL CANON — governs all entries in the series.
     Each individual entry has its own spec.md, plan.md, variables.md, and constitution.md.
     This file is the authority on anything that spans entries.
     When a per-entry decision contradicts this file, this file wins.
     Path: series/series-bible.md -->

---

## Workspace Structure

```
<workspace-root>/
+-- series/
¦   +-- series-bible.md              ? this file: series-level canon, shared across all entries
¦
+-- specs/
    +-- entry-1-[title]/              ? Entry 1
    ¦   +-- spec.md
    ¦   +-- plan.md
    ¦   +-- variables.md
    ¦   +-- endings.md
    ¦   +-- constitution.md
    ¦   +-- nodes/
    ¦   +-- outlines/
    ¦   +-- characters/
    ¦
    +-- entry-2-[title]/              ? Entry 2
        +-- ...
```

**Authority hierarchy**:
- `series/series-bible.md` wins over any per-entry decision on canon, world rules, and NPC state.
- Each entry's `constitution.md` mirrors relevant series constraints — do not edit those sections manually; use `speckit.series update` to sync them.
- Each NPC's state table in `characters/` is the per-entry view; the NPC Survival Registry in this file is the series-level authority.

---

## Series Parameters

| Parameter | Value |
|---|---|
| Series Name | [SERIES_NAME] |
| Total planned entries | [N / open series] |
| Current entry | [N] |
| Genre / tone | [NEEDS CLARIFICATION] |
| Target audience | [NEEDS CLARIFICATION] |
| Engine target | [Sugarcube / Ink / other] |
| Carry-over strategy | [save-file / questionnaire / both] |
| Overarching dramatic question | [The series-level spine — one sentence. Must not be fully answered until the final entry.] |
| Overarching theme | [Stated as a question. Each entry explores it from a different angle.] |
| Series ending contract | [What the final entry MUST resolve — not what happens, but what it must feel like.] |

---

## Entries

| # | Title | Status | Canon Ending Used | Key Arc Closed | Key Thread Opened |
|---|---|---|---|---|---|
| 1 | [TITLE] | released / in-progress / planned | END-[ID] | [arc] | [thread] |
| 2 | [TITLE] | | | | |

---

## Series Canon

<!-- Hard facts that are TRUE across all entries and cannot be contradicted by a per-entry decision.
     speckit.series audit flags violations when checking non-standalone entries. -->

### World Rules (Series-Level)

| Rule ID | Rule | Introduced In | Must Hold Through |
|---|---|---|---|
| SWR-001 | [e.g., "Magic has a permanent physical cost — no exceptions"] | Entry 1 | All entries |
| SWR-002 | [NEEDS CLARIFICATION] | | |

### Named Entity Registry

<!-- NPCs, locations, factions, and objects that exist across entries.
     Track canonical state so Entry 2 doesn't contradict Entry 1's endings. -->

| Entity | Type | Canonical status at series start | Last updated in |
|---|---|---|---|
| [NPC_NAME] | NPC | [alive / dead / location / faction] | [Entry N] |
| [LOCATION_NAME] | Location | [exists / destroyed / controlled by faction] | [Entry N] |

### Series Continuity Constraints

<!-- Facts established in earlier entries that later entries must not violate.
     speckit.series audit cross-references these for non-standalone entries. -->

| Constraint ID | Constraint | Established at | Must hold from |
|---|---|---|---|
| STC-001 | [e.g., "Player knows faction leader's true identity from Entry 1, NODE-087 onward"] | Entry 1, NODE-087 | Entry 2 onward |
| STC-002 | | | |

---

## Carry-Over Variable Registry

<!-- Variables that transfer from one entry to the next.
     Import method: save-file = read from previous save; questionnaire = player answers on new game.
     speckit.series validate checks all carry-over variables are declared in variables.md. -->

| Variable | Type | Default (fresh start) | Import Method | Affects Entry |
|---|---|---|---|---|
| npc_[name]_state | npc_state | alive | save-file / questionnaire | 2, 3 |
| flag_[name] | flag | false | save-file / questionnaire | 2 |
| trust_[npc] | trust | 50 | save-file | 2 |
| end_[id]_choice | flag | [DEFAULT_CHOICE] | questionnaire | 2, 3 |

---

## Canonical Import State

<!-- The "default save" — assumed choices when player starts Entry N fresh without importing.
     This is the canon used for marketing material, sequels that don't support import, etc. -->

### Fresh Start Defaults (Entry 2)

```yaml
canonical_import:
  npc_[name]_state: alive          # [RATIONALE]
  flag_[name]: false               # [RATIONALE]
  trust_[npc]: 65                  # [RATIONALE]
  ending_imported: END-A           # [RATIONALE — which ending is "canon"]
```

---

## Ending Canon Table

<!-- Which ending is treated as "true" for sequel purposes.
     All endings may be supported as carry-over, but only one is the narrative default. -->

| Entry | Canon Ending | Supported Carry-Over Endings | Notes |
|---|---|---|---|
| 1 | END-A | END-A, END-B | END-C (secret) not supported — too divergent |
| 2 | [TBD] | | |

---

## World State Delta Per Entry

<!-- How the world changes between entries based on canonical ending. -->

| Element | Entry 1 State | Entry 2 State (canon) | Entry 2 State (alt carry-over) |
|---|---|---|---|
| [LOCATION_NAME] | [STATE] | [STATE] | [STATE — if END-B imported] |
| [NPC_NAME] | alive | dead (END-A) | alive (END-B carry-over) |
| [FACTION_NAME] | neutral | allied | hostile |

---

## NPC State Registry

<!-- CLOSING STATE per NPC per entry. These values are the OPENING STATE for the next entry.
     "conditional" = depends on carry-over import.
     Updated by speckit.series update after each entry ships. -->

### [NPC_NAME]

| After Entry | Alive / Dead | Location | Faction alignment | Trust range | Notes |
|---|---|---|---|---|---|
| Entry 1 | alive | [LOCATION] | [FACTION] | 0–100 | |
| Entry 2 (canon) | | | | | |
| Entry 2 (conditional) | dead | | | | if END-B imported |

*(repeat block per major NPC)*

---

## Series Arc

<!-- The overarching narrative question that spans all entries.
     Each entry answers it partially; the final entry resolves it. -->

**Overarching dramatic question**: [SERIES_DRAMATIC_QUESTION]

**Series ending contract**: [What the final entry MUST resolve — not what happens, but what it must feel like.]

### Per-Entry Arc Contribution

| Entry | Partial question answered | New question opened |
|---|---|---|
| 1 | [e.g., "Can the player survive the inciting conflict?"] | [e.g., "Who engineered it?"] |
| 2 | | |

---

## Unresolved Series Threads

<!-- Story elements seeded across entries that have not yet paid off.
     speckit.series audit checks OPEN threads against drafted nodes.
     Mark RESOLVED when the pay-off entry is shipped. -->

| Thread ID | Description | Introduced In | Planned Pay-Off | Status |
|---|---|---|---|---|
| ST-001 | [e.g., "The locked vault in the faction HQ"] | Entry 1, NODE-042 | Entry 3 | OPEN |
| ST-002 | | | | |

---

## Known Contradictions

<!-- Continuity issues between entries. Log and resolve; do not delete rows.
     speckit.series audit flags OPEN contradictions as CRITICAL. -->

| ID | Description | Entries Affected | Status | Resolution |
|---|---|---|---|---|
| CON-001 | [NEEDS CLARIFICATION] | Entry 1, 2 | OPEN | |
| CON-002 | | | RESOLVED | [RESOLUTION] |
