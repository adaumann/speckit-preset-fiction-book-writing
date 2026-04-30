# Mechanic Hook Schemas: [GAME_TITLE]

<!-- Reference document for all mechanic hooks used in this project.
     Cross-referenced by speckit.implement, speckit.checklist, speckit.continuity, and export.py.
     Only hooks declared as enabled in constitution.md Section II are active. -->

---

## Tier 1 Hooks — Fully Exported (v1.0)

### `flag` — Boolean State

```
[MECHANIC:FLAG set=[variable_name] value=true|false]
[MECHANIC:FLAG check=[variable_name]]
[conditional prose]
[/MECHANIC]
```

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| set=true | `<<set $[var] to true>>` | `~ [var] = true` |
| set=false | `<<set $[var] to false>>` | `~ [var] = false` |
| check (true) | `<<if $[var]>>...<</if>>` | `{[var]: ...}` |
| check (false) | `<<if not $[var]>>...<</if>>` | `{not [var]: ...}` |

---

### `counter` — Integer Increment/Decrement

```
[MECHANIC:COUNTER set=[variable_name] delta=+1|-1|N]
[MECHANIC:COUNTER check=[variable_name] op=gte|lte|eq value=N]
[conditional prose]
[/MECHANIC]
```

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| delta=+1 | `<<set $[var] += 1>>` | `~ [var]++` |
| delta=-1 | `<<set $[var] -= 1>>` | `~ [var]--` |
| delta=N | `<<set $[var] += N>>` | `~ [var] += N` |
| check gte N | `<<if $[var] gte N>>...<</if>>` | `{[var] >= N: ...}` |
| check lte N | `<<if $[var] lte N>>...<</if>>` | `{[var] <= N: ...}` |
| check eq N | `<<if $[var] is N>>...<</if>>` | `{[var] == N: ...}` |

---

### `visited` — Node Seen Tracking

```
[MECHANIC:VISITED set=[variable_name]]
[MECHANIC:VISITED check=[variable_name]]
[prose shown only on first visit]
[/MECHANIC]
```

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| set | `<<run memorize("[var]", true)>>` or `<<set $[var] to true>>` | `~ [var] = true` |
| check (first visit) | `<<if not $[var]>>...<</if>>` | `{not [var]: ...}` |
| check (revisit) | `<<if $[var]>>...<</if>>` | `{[var]: ...}` |

> **Note**: Sugarcube `visited()` function checks passage visit count natively. The flag pattern above is for cross-passage use when the node ID is not the passage name.

---

### `inventory` — Item Management

```
[MECHANIC:INVENTORY add=[item_variable]]
[prose describing item acquisition]
[/MECHANIC]

[MECHANIC:INVENTORY remove=[item_variable]]

[MECHANIC:INVENTORY check=[item_variable]]
[prose shown when item is present]
[/MECHANIC]
```

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| add | `<<set $inv_[item] to true>>` | `~ inv_[item] = true` |
| remove | `<<set $inv_[item] to false>>` | `~ inv_[item] = false` |
| check present | `<<if $inv_[item]>>...<</if>>` | `{inv_[item]: ...}` |
| check absent | `<<if not $inv_[item]>>...<</if>>` | `{not inv_[item]: ...}` |

> **Export pattern**: each item is modelled as an individual boolean flag (`$inv_[item]` / `~ inv_[item]`). This is the default export.py output for both Sugarcube and Ink.
> **Sugarcube array alternative**: if you want `$inv` as an array (to iterate or count items), write the Sugarcube array calls manually in prose — `<<set $inv.push("item")>>` / `<<if $inv.includes("item")>>`. The boolean-flag pattern exported by export.py is simpler and covers the common case of checking whether a specific item is held.
> **Ink**: no native array type. Individual boolean flags are the correct idiomatic pattern.

---

### `timer` — Turn/Countdown

```
[MECHANIC:TIMER action=start variable=[timer_variable]]
[MECHANIC:TIMER action=stop variable=[timer_variable]]
[MECHANIC:TIMER action=check variable=[timer_variable]]
```

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| start | `<<set $[var] to [N]>>` | `~ [var] = N` |
| decrement (per turn) | `<<set $[var] -= 1>>` | `~ [var]--` |
| check expired | `<<if $[var] lte 0>><<goto "[failure_node]">><</if>>` | `{[var] <= 0: -> failure_node}` |

> **Note**: Seconds-based timers require JavaScript in Sugarcube (`window.setTimeout`). Ink has no real-time timer — turn-based only. Export emits a comment warning when `type: seconds`.

---

### `trust` — Per-NPC Trust Score

```
[MECHANIC:TRUST npc=[npc_id] delta=+N|-N]
[MECHANIC:TRUST npc=[npc_id] check=gte|lte|eq value=N]
[prose shown when condition met]
[/MECHANIC]
```

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| delta +N | `<<set $trust_[npc] += N>>` | `~ trust_[npc] += N` |
| delta -N | `<<set $trust_[npc] -= N>>` | `~ trust_[npc] -= N` |
| check gte N | `<<if $trust_[npc] gte N>>...<</if>>` | `{trust_[npc] >= N: ...}` |

---

### `currency` — Cost-Gated Choices

```
[MECHANIC:CURRENCY variable=[variable_name] delta=+N|-N]
[MECHANIC:CURRENCY variable=[variable_name] check=gte|lte value=N]
[prose shown when condition met — e.g. "You can afford the bribe"]
[/MECHANIC]
```

> **`variable=` is required.** Name must match a `type: currency` entry in `variables.md`. Use separate hooks for separate currencies (e.g. `variable=gold`, `variable=influence`).

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| delta +N | `<<set $[var] += N>>` | `~ [var] += N` |
| delta -N | `<<set $[var] -= N>>` | `~ [var] -= N` |
| check gte N | `<<if $[var] gte N>>...<</if>>` | `{[var] >= N: ...}` |
| check lte N | `<<if $[var] lte N>>...<</if>>` | `{[var] <= N: ...}` |

---

### `npc_state` — NPC Alive/Dead/Hostile/Custom

```
[MECHANIC:NPC_STATE npc=[npc_id] set=[state_value]]
[MECHANIC:NPC_STATE npc=[npc_id] check=[state_value]]
[prose shown when NPC is in this state]
[/MECHANIC]
```

| Parameter | Sugarcube Export | Ink Export (integer enum) |
|---|---|---|
| set=alive | `<<set $npc_[id]_state to "alive">>` | `~ npc_[id]_state = 0` |
| set=dead | `<<set $npc_[id]_state to "dead">>` | `~ npc_[id]_state = 1` |
| set=hostile | `<<set $npc_[id]_state to "hostile">>` | `~ npc_[id]_state = 2` |
| set=absent | `<<set $npc_[id]_state to "absent">>` | `~ npc_[id]_state = 3` |
| check alive | `<<if $npc_[id]_state is "alive">>...<</if>>` | `{npc_[id]_state == 0: ...}` |

> State values and integer mappings are defined per NPC in `characters/NPC-NNN.md`.

---

### `random` — Chance-Based Branch

```
[MECHANIC:RANDOM variable=[result_variable] min=N max=N]
[MECHANIC:RANDOM check=[result_variable] op=gte|lte|eq value=N]
[prose shown when condition met]
[/MECHANIC]
```

> `variable=` must be declared as `type: counter` in `variables.md`. The roll is assigned at the point the hook executes — once per node visit unless re-rolled manually. Use a downstream check hook to branch on the result.

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| roll `min` to `max` | `<<set $[var] to random([min], [max])>>` | `~ [var] = RANDOM([min], [max])` |
| check gte N | `<<if $[var] gte N>>...<</if>>` | `{[var] >= N: ...}` |
| check lte N | `<<if $[var] lte N>>...<</if>>` | `{[var] <= N: ...}` |
| check eq N | `<<if $[var] is N>>...<</if>>` | `{[var] == N: ...}` |

> **Note**: `RANDOM()` in Ink is a built-in function (Ink 1.1+). In Sugarcube, `random(min, max)` is a built-in macro. Both are inclusive on both ends.

---

### `choice_memory` — Recalled Past Choice

```
[MECHANIC:CHOICE_MEMORY set=[variable_name] value=[choice_label]]
[MECHANIC:CHOICE_MEMORY check=[variable_name] value=[choice_label]]
[prose shown when the remembered choice matches]
[/MECHANIC]
```

> Variable must be declared in `variables.md` as `type: string`. The `value` attribute stores the choice label verbatim. Ink maps all string values to integer constants (see Ink note below).

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| set | `<<set $[var] to "[label]">>` | `~ [var] = [LABEL_CONST]` |
| check | `<<if $[var] is "[label]">>...<</if>>` | `{[var] == [LABEL_CONST]: ...}` |

> **Ink note**: Ink has no string variables. Declare integer constants at the top of the knot (e.g. `CONST HELPED_MIRA = 1`) and the exporter will map string labels to them. Export emits a `// CHOICE_MEMORY mapping:` comment block listing all used constants.

---

### `clue` — Information Collection

```
[MECHANIC:CLUE add=[clue_id]]
[MECHANIC:CLUE check=[clue_id]]
[prose shown when clue is held]
[/MECHANIC]
```

> `clue_id` must be declared as a `type: flag` variable in `variables.md` (e.g. `clue_broken_key`). Structurally equivalent to FLAG — a boolean per clue. Use `clue_id` naming convention to distinguish from general flags.

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| add | `<<set $clue_[id] to true>>` | `~ clue_[id] = true` |
| check (held) | `<<if $clue_[id]>>...<</if>>` | `{clue_[id]: ...}` |
| check (missing) | `<<if not $clue_[id]>>...<</if>>` | `{not clue_[id]: ...}` |

---

### `ending_condition` — Multi-Ending Progress Tracker

```
[MECHANIC:ENDING_CONDITION ending=[ending_id] delta=+1]
[MECHANIC:ENDING_CONDITION ending=[ending_id] check=gte value=N]
[prose shown when ending threshold is met]
[/MECHANIC]
```

| Parameter | Sugarcube Export | Ink Export |
|---|---|---|
| delta +1 | `<<set $end_[id]_progress += 1>>` | `~ end_[id]_progress++` |
| check gte N | `<<if $end_[id]_progress gte N>>...<</if>>` | `{end_[id]_progress >= N: ...}` |

---

## Tier 2 Hooks — Stubs (v1.x, export with warning)

The following hooks are defined for authoring use but produce `// UNSUPPORTED HOOK — [hook_type] not yet translated for [target]` in export output. No export failure.

### `knowledge` — Information State

```
[MECHANIC:KNOWLEDGE set=[variable_name]]
[MECHANIC:KNOWLEDGE check=[variable_name]]
[prose shown when player character knows this information]
[/MECHANIC]
```

### `faction` — Group Standing

```
[MECHANIC:FACTION name=[faction_id] delta=+N|-N]
[MECHANIC:FACTION name=[faction_id] check=gte|lte value=N]
[/MECHANIC]
```

### `location_state` — Room/Area Condition

```
[MECHANIC:LOCATION_STATE location=[location_id] set=[state_value]]
[MECHANIC:LOCATION_STATE location=[location_id] check=[state_value]]
[/MECHANIC]
```

### `object_state` — Object Condition

```
[MECHANIC:OBJECT_STATE object=[object_id] set=[state_value]]
[MECHANIC:OBJECT_STATE object=[object_id] check=[state_value]]
[/MECHANIC]
```

---

## Tier 3 Hooks — Experimental / Engine-Specific (v2.x)

The following hooks are specialized for **Point-and-Click** adventures and high-fidelity interactive fiction.

### `verb` — Mode-Specific Interaction

```
[MECHANIC:VERB type=examine|interact|talk]
[prose specific to this verb mode]
[/MECHANIC]
```

### `inventory_combine` — Item Crafting

```
[MECHANIC:INVENTORY_COMBINE item1=[id] item2=[id] result=[new_id]]
[prose describing the successful combination]
[/MECHANIC]
```

### `hotspot` — UI Visibility

```
[MECHANIC:HOTSPOT id=[id] visibility=hidden|revealed|dimmed]
[/MECHANIC]
```

### `audio` — Sound & Atmosphere

```
[MECHANIC:AUDIO trigger=[sfx_id] action=play|stop|fade loop=true|false]
[/MECHANIC]
```

### `gated_choice` — Timed Decisions

```
[MECHANIC:GATED_CHOICE time=[seconds] failure_node=[node_id]]
[choice list that will expire]
[/MECHANIC]
```

---

## Compatibility Warning Rules

| Situation | Sugarcube | Ink | Action |
|---|---|---|---|
| Tier 2 hook used | ?? export comment | ?? export comment | `// UNSUPPORTED HOOK` inserted; console warning logged |
| `timer type=seconds` | ?? JS required | ? not supported | Comment inserted; export continues |
| `inventory type=slots` with capacity check | ? with counter | ?? manual counter needed | Ink: comment inserted |
| `npc_state` with custom values beyond 4 | ? string match | ?? add integer mapping | Ink: comment with mapping instructions |
| `currency` missing `variable=` | ? parse error | ? parse error | Export aborts with error; add `variable=[name]` |
| `choice_memory` in Ink | ? integer const | ?? CONST mapping emitted | Ink: mapping comment block auto-inserted |
| `random` in Ink < 1.1 | ? | ?? requires Ink 1.1+ | Comment warning inserted |
| `condition=` compound expression | ? raw emit | ? raw emit | Emitted verbatim — author responsible for syntax |
| Ren'Py target | ? not yet supported | ? not yet supported | Use `--target renpy` when `renpy` is declared as target in constitution.md; emits `.rpy` (v1.x roadmap) |
| Escoria target | ?? Script logic | ?? Script logic | Mapping provided in Tier 3 section; uses Escoria `.esc` syntax |

---

## Tier 3 Escoria Export Mapping (Godot)

When `export_target: escoria` is set in `constitution.md`, the following mappings are used for Tier 3 hooks.

| Hook | Escoria Script (`.esc`) |
|---|---|
| `[MECHANIC:MOVE actor=A target=B]` | `:walk A B` |
| `[MECHANIC:VERB type=examine]` | `> [examine]` (inside item block) |
| `[MECHANIC:AUDIO trigger=sn] play` | `snd_play sn` |
| `[MECHANIC:HOTSPOT id=H] hi/re` | `set_active H true` / `false` |
| `[MECHANIC:INVENTORY] result=R` | `inventory_add R` |

---

## Compound Conditions

Single-variable checks cover most cases. When a branch requires multiple conditions (e.g. "IF has lockpick AND trust_mira >= 3"), use a `condition=` attribute on the **choice line** rather than nesting hooks:

```markdown
- [Try the lock](NODE-017) <!-- condition: $inv_lockpick and $trust_mira >= 3 -->
```

The `condition=` comment is passed verbatim to the export target. Author is responsible for using valid engine syntax:

| Target | Syntax |
|---|---|
| Sugarcube | `$var1 and $var2 gte N` (or `&&` in JS-mode macros) |
| Ink | `{var1 and var2 >= N: ...}` inside a conditional stitch |

> **Authoring rule**: declare all variables used in a `condition=` expression in the node's `variables_read` frontmatter field. `speckit.checklist` NR-006 will catch any that are not set on all upstream paths.

---

## Dialogue Hub Pattern

A **dialogue hub** is a repeated-visit node where the player selects from a shrinking menu of conversation topics. Each topic is a sub-node that loops back to the hub. The hub ends when all topics are exhausted or the player selects "Leave."

**Topology:**
```
HUB-NODE --? TOPIC-A --+
           --? TOPIC-B --¦? back to HUB-NODE
           --? TOPIC-C --+
           --? EXIT-NODE (always available)
```

**Implementation pattern using `visited` + `flag`:**
- Hub node: use `[MECHANIC:VISITED check=[topic_X_visited]]` to hide each topic choice once seen
- Topic sub-node: set `[MECHANIC:VISITED set=[topic_X_visited]]` on entry; last choice points back to hub node ID
- Hub node final exit: show "Leave" choice unconditionally; all other choices gated on `not visited`

**`variables.md` declarations needed:** one `type: visited` variable per topic (e.g. `visited_topic_locksmith`, `visited_topic_rumors`).

**When to use:** interrogation scenes, shopkeeper dialogue, mentor exposition, any NPC with more information than fits one node's pacing. Mark hub node with tag `hub` in `specs/flowmap.md` for branch health check awareness.

---
