# Timeline: [GAME_TITLE]

<!-- Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE] -->
<!-- OPTIONAL document — create this when the game has a defined in-world chronology
     that the player uncovers, references, or navigates across branches.
     Most relevant for: mystery games, historical settings, timer-heavy mechanics,
     or games where player choices create diverging timelines.

     Two layers:
       Fabula  — the chronological order events actually happened (the world's truth)
       Syuzhet — the order the player encounters events across nodes (branch-dependent)

     speckit.analyze checks that fabula entries referenced by node variables are
     consistent with their declared states. speckit.continuity checks that NPC states
     do not contradict fabula constraints. -->

---

## Temporal Parameters

| Parameter | Value |
|---|---|
| Story span (in-world time covered by gameplay) | [NEEDS CLARIFICATION] |
| Backstory span (pre-game events that drive plot) | [NEEDS CLARIFICATION] |
| Narrative non-linearity | [linear / player-uncovered-past / dual-timeline / fragmented-memory] |
| Calendar system | [real-world Gregorian / fictional / relative ("Day 1") / implied only] |
| Time-of-day sensitivity | [yes — nodes depend on time-of-day state / no] |
| Timer mechanic active | [yes — links to timer hook in specs/variables.md / no] |

---

## Fabula — Chronological Event Order

<!-- Every event in the order it actually happened, including backstory.
     Events the player never witnesses directly still belong here if they cause plot.
     This is the world's truth — independent of which branch the player takes.
     Format: [DATE_OR_OFFSET] | [EVENT] | [Arc or variable affected] -->

### Backstory (before game opens)

| Date / Offset | Event | Arc / Variable Impact |
|---|---|---|
| [e.g., "–10 years"] | [e.g., "The founding agreement was broken by NPC-A"] | [`$npc_a_state` backstory] |
| | | |

### Game Period

| Date / Offset | Event | Node ID | Variable / Arc |
|---|---|---|---|
| [Day 1 / equivalent] | [Status quo opening event] | NODE-001 | — |
| | | | |

---

## Syuzhet — Player Discovery Order

<!-- Only complete this section if the player encounters past events out of order
     across different nodes or branches.
     Maps when the player learns what vs. when it actually happened.
     If linear/chronological, write: "N/A — player encounters events in fabula order." -->

| Discovery order | Event revealed | Fabula date | Revealed in node | Branch condition |
|---|---|---|---|---|
| [1st thing player learns] | | [when it happened] | NODE-[N] | [any / only if $flag = true] |
| | | | | |

---

## Branching Timeline Consequences

<!-- Some player choices create diverging in-world outcomes that change what is true
     from that branch forward. Document these here to prevent continuity errors.
     These are NOT the same as variable states — they are world-state changes. -->

| Decision point | Node ID | Branch A outcome | Branch B outcome | Variable that tracks it |
|---|---|---|---|---|
| [e.g., "Player exposes the cover-up"] | NODE-[N] | [NPC-A arrested by Act 3] | [NPC-A still active] | `$flag_coverup_exposed` |
| | | | | |

---

## Continuity Constraints

<!-- Hard rules derived from the timeline that node drafting must not violate.
     speckit.continuity checks these. One row per constraint. -->

| Constraint ID | Rule | Affected nodes | Enforced by variable |
|---|---|---|---|
| TC-001 | [NPC-A cannot know about X before NODE-[N]] | NODE-[N]–NODE-[N] | `$flag_[name]` |
| TC-002 | | | |

---

## Timer Event Schedule

<!-- Only fill if timer hooks are active (Hook: timer in constitution.md).
     Maps each timer to the fabula event it models and its failure node. -->

| Timer ID | Models (fabula event) | Duration | Warning threshold | Failure node | Variable |
|---|---|---|---|---|---|
| TM-001 | [e.g., "Time before building collapses"] | [N turns] | [N turns remaining] | NODE-[N] | `$timer_[name]` |
| TM-002 | | | | | |
