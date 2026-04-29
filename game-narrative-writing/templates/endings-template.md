# Endings Registry: [GAME_TITLE]

<!-- All planned endings. Every ending node must be registered here.
     speckit.analyze validates that each ending has at least one reachable path.
     speckit.continuity checks ending_condition variables against this registry. -->

---

## Summary

| Total Endings | Good | Bad | Neutral | Secret |
|---|---|---|---|---|
| [N] | [N] | [N] | [N] | [N] |

---

## Ending Entries

### END-A — [ENDING_NAME]

| Field | Value |
|---|---|
| Ending ID | END-A |
| Name | [ENDING_NAME] |
| Type | good / bad / neutral / secret |
| Ending node | NODE-[N] |
| Thematic statement | [One sentence: what truth this ending makes about the game's theme] |
| Carry-over state | [for series use — see series-bible.md] |

**Description** (what happens, what it means for the player arc):
[ENDING_DESCRIPTION]

**Required conditions**:
| Variable | Operator | Value | Source |
|---|---|---|---|
| $end_A_progress | >= | [N] | Multiple nodes |
| $flag_[name] | = | true | NODE-[N] |
| $trust_[npc] | >= | [N] | NODE-[N] |

**Reachable paths**:
| Path | Key Nodes | Approximate Branch |
|---|---|---|
| Path 1 | NODE-001 → NODE-[N] → NODE-[N] | Choose [A] at NODE-002, [B] at NODE-[N] |
| Path 2 | NODE-001 → NODE-[N] → NODE-[N] | Choose [B] at NODE-002 |

**Variable state snapshot** (for series carry-over):
```yaml
end_A_state:
  npc_[name]_state: alive
  flag_[name]: true
  trust_[npc]: [N]
```

---

### END-B — [ENDING_NAME]

| Field | Value |
|---|---|
| Ending ID | END-B |
| Name | [ENDING_NAME] |
| Type | good / bad / neutral / secret |
| Ending node | NODE-[N] |
| Thematic statement | [One sentence: what truth this ending makes about the game's theme] |
| Carry-over state | [for series use — see series-bible.md] |

**Description**:
[ENDING_DESCRIPTION]

**Required conditions**:
| Variable | Operator | Value | Source |
|---|---|---|---|
| $end_B_progress | >= | [N] | Multiple nodes |

**Reachable paths**:
| Path | Key Nodes |
|---|---|
| Path 1 | NODE-001 → ... → NODE-[N] |

**Variable state snapshot**:
```yaml
end_B_state:
  npc_[name]_state: dead
  flag_[name]: false
```

---

### END-C — [ENDING_NAME] *(Secret)*

| Field | Value |
|---|---|
| Ending ID | END-C |
| Name | [ENDING_NAME] |
| Type | secret |
| Ending node | NODE-[N] |
| Thematic statement | [One sentence: what truth this ending makes about the game's theme] |
| Carry-over state | [for series use — see series-bible.md] |

**Description**:
[ENDING_DESCRIPTION]

**Required conditions** (all must be true):
| Variable | Operator | Value | Source |
|---|---|---|---|
| $flag_[hidden_condition] | = | true | NODE-[N] |
| $trust_[npc] | >= | 90 | Multiple nodes |
| $inv_[item] | present | — | NODE-[N] |

**How to find it**: [DISCOVERY_HINT_FOR_AUTHOR — not player-facing]

**Reachable paths**:
| Path | Key Nodes |
|---|---|
| Path 1 (only path) | NODE-[N] (ally trust + hidden flag + item) |

**Variable state snapshot**:
```yaml
end_C_state:
  npc_[name]_state: [state]
  flag_[hidden_condition]: true
  inv_[item]: present
```

---

## Reachability Audit

<!-- Populated by speckit.analyze. Do not edit manually. -->

| Ending ID | Status | Issue |
|---|---|---|
| END-A | [REACHABLE / UNREACHABLE / UNVERIFIED] | |
| END-B | | |
| END-C | | |
