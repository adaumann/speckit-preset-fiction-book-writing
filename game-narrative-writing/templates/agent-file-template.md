# Agent Context: [GAME_TITLE]

<!-- Living context file. Updated by speckit.implement and speckit.continuity.
     Load this file at the start of each authoring session for full project state. -->

---

## Current Position

| Field | Value |
|---|---|
| Active node | NODE-[N] — [NODE_TITLE] |
| Act | [ACT_NUMBER] |
| Last drafted | NODE-[N] — [DATE] |
| Next node | NODE-[N] — [NODE_TITLE] |
| Workflow stage | outlining / drafting / revising / QA / export |

---

## Variable State Snapshot

<!-- Current values of all active variables. Updated after each drafting session.
     This is the "current playthrough state" at the active node. -->

### Flags
| Variable | Current Value |
|---|---|
| $flag_[name] | true / false |

### Counters
| Variable | Current Value |
|---|---|
| $counter_[name] | [N] |

### Inventory
| Item | Held |
|---|---|
| $inv_[item] | yes / no |

### Trust Scores
| NPC | Score | State Label |
|---|---|---|
| $trust_[name] | [N] | hostile / cautious / neutral / friendly / ally |

### NPC States
| NPC | State |
|---|---|
| $npc_[name]_state | alive / dead / hostile / absent |

### Ending Conditions
| Ending | Progress | Threshold | Status |
|---|---|---|---|
| END-A | [N] | >= [N] | on-track / locked / achieved |

### POV
| Variable | Value |
|---|---|
| $pov | [character_name / blank if fixed] |

---

## Open Branch Targets

<!-- Nodes that have been referenced as choice targets but not yet drafted. -->

| Node ID | Referenced In | Choice Label | Priority |
|---|---|---|---|
| NODE-[N] | NODE-[N] | "[CHOICE_LABEL]" | high / medium / low |

---

## Recent NPC State Changes

<!-- Last 5 NPC state changes for continuity awareness. -->

| NPC | Previous State | New State | Changed In | Cause |
|---|---|---|---|---|
| [NPC_NAME] | alive | hostile | NODE-[N] | trust fell below 25 |

---

## Open Threads

<!-- Narrative promises that must be paid off before the ending. -->

| Thread | Introduced In | Required Pay-off | Status |
|---|---|---|---|
| [THREAD_DESCRIPTION] | NODE-[N] | NODE-[N] (planned) | open / paid-off |

---

## Recent Quality Gate Failures

<!-- Outstanding checklist or continuity failures requiring revision. -->

| Node ID | Failure Code | Description | Status |
|---|---|---|---|
| NODE-[N] | NR-001 | Only 1 choice in non-terminal node | OPEN |
| NODE-[N] | PR-001 | POV drift — second-person in third-person section | OPEN |

---

## Session Notes

[SESSION_NOTES]
<!-- Freeform notes from the current drafting session.
     Design decisions, deferred questions, things to check in continuity pass. -->
