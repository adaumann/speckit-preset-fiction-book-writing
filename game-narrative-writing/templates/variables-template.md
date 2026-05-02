# Variable Registry: [GAME_TITLE]

<!-- All state variables used in this project.
     Every variable referenced in a node [MECHANIC:*] hook MUST be declared here.
     speckit.checklist and speckit.continuity validate against this registry. -->

---

## Registry Format

Each entry:
- **Variable name**: exact name used in hook blocks and export output
- **Type**: hook type category
- **Scope**: `global` (persists across saves) | `session` (resets on load) | `branch` (reset when branch rejoins)
- **Default**: initial value at game start
- **Export name**: name used in engine output (Sugarcube: `$name`, Ink: `~ name`)
- **Set in**: node IDs where this variable is first/primarily set
- **Read in**: node IDs where this variable gates content or choices

---

## Visited Flags

<!-- Auto-set when a node is entered. Used to prevent repeated intro text,
     unlock lore options, or track exploration. -->

| Variable | Type | Scope | Default | Export (SC) | Export (Ink) | Set in | Read in |
|---|---|---|---|---|---|---|---|
| visited_NODE-001 | visited | global | false | `$visited_NODE_001` | `~ visited_node_001` | NODE-001 | [NODE_IDs] |
| visited_NODE-[N] | visited | global | false | | | | |

---

## Boolean Flags

<!-- Simple true/false state. Use for events that happen once. -->

| Variable | Type | Scope | Default | Description | Export (SC) | Export (Ink) | Set in | Read in |
|---|---|---|---|---|---|---|---|---|
| flag_[name] | flag | global | false | [DESCRIPTION] | `$flag_[name]` | `~ flag_[name]` | NODE-[N] | NODE-[N] |

---

## Counters

<!-- Integer values. Use for progress tracking, aggregate choice scoring, turn counts. -->

| Variable | Type | Scope | Default | Range | Description | Export (SC) | Export (Ink) | Set in | Read in |
|---|---|---|---|---|---|---|---|---|---|
| counter_[name] | counter | global | 0 | 0–[MAX] | [DESCRIPTION] | `$counter_[name]` | `~ counter_[name]` | NODE-[N] | NODE-[N] |

---

## Inventory

<!-- Item tracking. type=array: unlimited list. type=slots: fixed capacity from constitution.md. -->

| Item Variable | Type | Scope | Default | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| inv_[item_name] | inventory | global | false | [ITEM_DESCRIPTION] | `$inv_[item_name]` (boolean flag) | `~ inv_[item_name]` |

<!-- Export pattern: individual boolean flags per item — `$inv_item = true/false`.
     Sugarcube array alternative (manual): `<<set $inv.push("item")>>` / `<<if $inv.includes("item")>>`
     Use the array alternative only if you need to iterate or count items; write it as raw prose markup. -->

---

## Trust Scores (per NPC)

<!-- Integer. Thresholds defined in characters/NPC-NNN.md. -->

| Variable | NPC ID | Scope | Default | Range | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| trust_[npc_name] | NPC-[N] | global | 50 | 0–100 | `$trust_[npc_name]` | `~ trust_[npc_name]` |

---

## Currency

<!-- Declared once per currency type. Multiple currencies allowed. -->

| Variable | Name | Scope | Default | Min | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| [var_name] | [CURRENCY_NAME] | global | [N] | 0 | `$[var_name]` | `~ [var_name]` |

---

## NPC State

<!-- Enumerated states per NPC. Valid values defined in characters/NPC-NNN.md. -->

| Variable | NPC ID | Scope | Default | Valid States | Export (SC) | Export (Ink — integer enum) |
|---|---|---|---|---|---|---|
| npc_[name]_state | NPC-[N] | global | alive | alive / dead / hostile / absent | `$npc_[name]_state` | `~ npc_[name]_state` (0=alive,1=dead,2=hostile,3=absent) |

---

## Ending Conditions

<!-- Progress counters toward specific endings. Checked at climax nodes. -->

| Variable | Ending ID | Scope | Default | Threshold to Unlock | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| end_[ending_id]_progress | END-[ID] | global | 0 | >= [N] | `$end_[id]_progress` | `~ end_[id]_progress` |

---

## Timer Variables

<!-- Only when Hook: timer is enabled in constitution.md. -->

| Variable | Type | Scope | Default | Failure Node | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| timer_[name] | timer | session | [N] | NODE-[N] | `$timer_[name]` | `~ timer_[name]` |

---

## Random Result Variables

<!-- Variables used with MECHANIC:RANDOM. Declare as type: counter.
     Roll results are integers in the declared min–max range. -->

| Variable | Type | Scope | Default | Range | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|---|
| random_[name] | counter | session | 0 | [min]–[max] | [DESCRIPTION — e.g. "Luck roll result"] | `$random_[name]` | `~ random_[name]` |

> **Note**: Use `scope: session` unless the roll result needs to persist across saves. Random variables are re-rolled each time the hook executes.

---

## Choice Memory Variables

<!-- Variables used with MECHANIC:CHOICE_MEMORY. Declare as type: string.
     Follow the naming convention choice_[node_id_context].
     Ink targets: string values are mapped to integer CONST at export. -->

| Variable | Type | Scope | Default | Possible Values | Description | Export (SC) | Export (Ink — CONST int) |
|---|---|---|---|---|---|---|---|
| choice_[name] | string | global | "" | "[label_a]" / "[label_b]" / ... | [DESCRIPTION] | `$choice_[name]` | `~ choice_[name]` (CONST) |

---

## Clue Variables

<!-- Variables used with MECHANIC:CLUE. Declare as type: flag.
     Always use the clue_ prefix. One variable per distinct clue. -->

| Variable | Type | Scope | Default | Description | Export (SC) | Export (Ink) |
|---|---|---|---|---|---|---|
| clue_[name] | flag | global | false | [WHAT THIS CLUE REVEALS] | `$clue_[name]` | `~ clue_[name]` |

---

## POV Variable

<!-- Only when player_perspective: switching is set in constitution.md. -->

| Variable | Valid Values | Default | Export (SC) | Export (Ink) |
|---|---|---|---|---|
| pov | [character_names] | [DEFAULT_CHARACTER] | `$pov` | `~ pov` |

---

## Tier 2 Variables (stubs — no export translation in v1.0)

<!-- Variables used with Tier 2 hooks. Exported with // UNSUPPORTED HOOK warning. -->

| Variable | Hook Type | Description |
|---|---|---|
| knowledge_[name] | knowledge | [DESCRIPTION] |
| faction_[name] | faction | [DESCRIPTION] |
| location_[name]_state | location_state | [DESCRIPTION] |
| object_[name]_state | object_state | [DESCRIPTION] |
