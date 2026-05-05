---
node_id: [NODE_ID]
title: [NODE_TITLE]
act: [ACT_NUMBER]
status: DRAFT
# status: DRAFT | APPROVED | SKIP
# DRAFT    ? speckit.implement will stop and request approval
# APPROVED ? speckit.implement will draft prose for this node
# SKIP     ? speckit.implement will skip this node entirely
pov: [PLAYER_PERSPECTIVE_OVERRIDE]
# Leave blank to use the default from constitution.md
# Set to: second-person | third-person | first-person | [character_name] (when switching)
variables_read: []
# List all variables this node reads/checks. Must be declared in variables.md.
# Example: [inv_lockpick, trust_mira, visited_NODE-041]
variables_set: []
# List all variables this node sets. Must be declared in variables.md.
# Example: [inv_gear_oil, visited_NODE-042, npc_mira_state]
drafted: [YYYY-MM-DD]
outline_ref: outlines/[NODE_ID].md
---

<!-- DRAFT NOTES
     Outline ref:       outlines/[NODE_ID].md
     Deviation from outline: [None / describe any structural change]
     New variable states discovered: [None / list any]
     Unresolved items: [None / list any]
-->

# [NODE_TITLE]

<!-- Node ID: [NODE_ID] | Act: [ACT_NUMBER] | Status: DRAFT -->

---

[NODE_PROSE]
<!-- Write the narrative prose here. Second/third/first person per constitution.md.
     Keep prose coherent without the hook blocks — hooks are annotations only.
     Opening line MUST orient the player: where, who, what is at stake. -->

---

<!-- -------------------------------------------------------
     MECHANIC HOOKS
     Each hook block is self-contained. Remove unused blocks.
     Prose must read coherently if all hook blocks are removed.
     ------------------------------------------------------- -->

[MECHANIC:VISITED set=[VARIABLE_NAME]]
<!-- Marks this node as visited. Variable must be declared in variables.md as type: visited -->

[MECHANIC:FLAG check=[VARIABLE_NAME]]
<!-- Conditional content shown only when flag is true -->
[OPTIONAL PROSE SHOWN WHEN FLAG IS TRUE]
[/MECHANIC]

[MECHANIC:INVENTORY check=[ITEM_VARIABLE]]
<!-- Conditional content shown only when item is in inventory -->
[OPTIONAL PROSE SHOWN WHEN ITEM IS PRESENT]
[/MECHANIC]

[MECHANIC:INVENTORY add=[ITEM_VARIABLE]]
<!-- Adds item to inventory when player reaches this point -->
[OPTIONAL PROSE DESCRIBING ITEM ACQUISITION]
[/MECHANIC]

[MECHANIC:TRUST npc=[NPC_ID] delta=[+N or -N]]
<!-- Adjusts trust score for an NPC. Positive = gain, negative = loss -->

[MECHANIC:CURRENCY variable=[CURRENCY_VARIABLE] delta=[+N or -N]]
<!-- Adjusts a named currency. variable= must match a type: currency entry in variables.md -->

[MECHANIC:NPC_STATE npc=[NPC_ID] set=[STATE_VALUE]]
<!-- Sets NPC state. Valid values defined in characters/NPC-NNN.md -->

[MECHANIC:ENDING_CONDITION ending=[ENDING_ID] delta=[+1]]
<!-- Increments progress toward an ending. Ending must be declared in endings.md -->

[MECHANIC:TIMER action=[start|stop|check] variable=[TIMER_VARIABLE]]
<!-- Timer hook. action=check branches to failure_node when expired -->

---

## Choices

<!-- Minimum 2 choices for non-terminal nodes; omit section entirely for ending nodes.
     Format: - [Label text](TARGET_NODE_ID) <!-- condition if gated; consequence of choice -->
     Each choice must include:
       1. Label text in brackets [...]
       2. Target node in parentheses (NODE_ID or END_ID)
       3. Optional condition comment: <!-- condition_expression -->
       4. Optional consequence comment: <!-- Effect: narrative consequence from outline -->
     export.py parse_choices() requires this exact heading and link format. -->

- [CHOICE_LABEL_A](NODE_ID_A) <!-- Effect: [Narrative consequence from outline] -->
- [CHOICE_LABEL_B](NODE_ID_B) <!-- Effect: [Narrative consequence from outline] -->
- [CHOICE_LABEL_C](NODE_ID_C) <!-- requires: $VARIABLE_NAME == value; Effect: [Narrative consequence] -->

<!-- Terminal node (ending): use a single entry pointing to the ending node:
- [ENDING_LABEL](END-A) <!-- Effect: [How this ending concludes the story] -->
-->
