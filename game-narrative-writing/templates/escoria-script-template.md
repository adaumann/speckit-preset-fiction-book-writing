# Escoria Room Script: [LOCATION_NAME]

<!-- Node ID: [NODE_ID] | Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE] -->
<!-- This template is optimized for Godot + Escoria (.esc) export.
     Prose is wrapped in [MECHANIC:VERB] hooks to map to Escoria interaction blocks. -->

---

## ESC Script Metadata
| Field | Value |
|---|---|
| **Room ID** | [room_id] |
| **Active Actor** | [actor_id] |
| **Default Music** | [bgm_id] |
| **Walkable?** | [yes/no] |

---

## Interaction logic (.esc)

### > [setup]
<!-- Entry logic: what happens as soon as the room loads -->
[MECHANIC:LOCATION_STATE location=[room_id] check=first_visit]
:walk [actor_id] [start_marker]
say [actor_id] "This place... it hasn't changed in years."
[/MECHANIC]

---

### > [item_id]
<!-- Interactions with specific hotspots or objects -->

#### Examine
[MECHANIC:VERB type=examine]
say [actor_id] "[Atmospheric description of the object]"
[/MECHANIC]

#### Interact
[MECHANIC:VERB type=interact]
[MECHANIC:OBJECT_STATE object=[item_id] check=locked]
  say [actor_id] "It's locked tight."
  [MECHANIC:AUDIO trigger=door_rattle action=play]
[/MECHANIC]

[MECHANIC:OBJECT_STATE object=[item_id] check=unlocked]
  [MECHANIC:AUDIO trigger=door_open action=play]
  :walk [actor_id] [exit_marker]
  transition [target_room_id]
[/MECHANIC]
[/MECHANIC]

#### Use [item_variable]
[MECHANIC:INVENTORY check=[item_variable]]
  say [actor_id] "The [item_name] fits the lock perfectly."
  [MECHANIC:OBJECT_STATE object=[item_id] set=unlocked]
[/MECHANIC]

---

## Supporting Dialogue Nodes
<!-- For conversations with NPCs in this room -->

### > talk [npc_id]
[MECHANIC:VERB type=talk]
:walk [actor_id] [npc_id]
[MECHANIC:NPC_STATE npc=[npc_id] check=alive]
  say [actor_id] "Hello?"
  say [npc_id] "[Response based on character/ relationship-template.md]"
[/MECHANIC]
[/MECHANIC]
