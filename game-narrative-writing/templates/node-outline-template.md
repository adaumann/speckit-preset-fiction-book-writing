---
node_id: [NODE_ID]
title: [NODE_TITLE]
act: [ACT_NUMBER]
status: DRAFT
# status: DRAFT | APPROVED | SKIP
# DRAFT    ? speckit.implement gates — will not draft until changed to APPROVED
# APPROVED ? speckit.implement will draft prose for this node
# SKIP     ? speckit.implement skips this node entirely
---

# Node Outline: [NODE_TITLE]

<!-- Node ID: [NODE_ID] | Act: [ACT_NUMBER] -->

---

## Beat Summary

[BEAT_SUMMARY]
<!-- 1–3 sentences. What happens in this node? What is the player doing/deciding?
     What narrative or mechanical purpose does this node serve? -->

**Narrative purpose**: [decision / consequence / revelation / setup / hub / transition / climax / ending]
**Tension level**: [1–10]
**POV override**: [blank = use constitution.md default / or: second-person | third-person | first-person | character_name]
**Thematic work**: [blank = none / or: motif MO-NNN appears | symbol [name] state changes | counter-theme voice present | theme-question advanced]

---

## Variables Read (Inputs)

<!-- Variables this node checks. Must all be declared in variables.md. -->

| Variable | Type | Condition | Effect |
|---|---|---|---|
| [VAR_NAME] | flag / inventory / trust / counter | [= true / >= N / contains X] | [gates choice / changes prose] |
| [VAR_NAME] | | | |

---

## Variables Set (Outputs)

<!-- Variables this node sets. Must all be declared in variables.md. -->

| Variable | Hook Type | Value / Delta | When |
|---|---|---|---|
| [VAR_NAME] | visited | true | on entry |
| [VAR_NAME] | inventory | add / remove [ITEM] | on choice [A/B/C] |
| [VAR_NAME] | trust | +N / -N | on entry / on choice |
| [VAR_NAME] | flag | true / false | on entry / on choice |
| [VAR_NAME] | ending_condition | +1 | on entry |

---

## Choices

<!-- Minimum 2 choices for non-terminal nodes. 0 choices for ending nodes.
     Include all conditional choices with their requirements.
     
     IMPORTANT: The "Narrative Consequence" column is CRITICAL for speckit.implement.
     It describes what the player experiences as a result of this choice.
     These consequences will be transferred to the drafted node as comments in the Choices section.
     
     speckit.implement uses this table to generate the ## Choices section in the node file.
     export.py requires: ## Choices heading + - [Label](NODE-ID) <!-- condition; Effect: consequence --> format. -->

| # | Label | Condition | Target Node | Narrative Consequence |
|---|---|---|---|---|
| A | [CHOICE_LABEL] | none | NODE-[N] | [What changes or what the player experiences] |
| B | [CHOICE_LABEL] | none | NODE-[N] | [What changes or what the player experiences] |
| C | [CHOICE_LABEL] | requires [VAR CONDITION] | NODE-[N] | [What changes or what the player experiences] |

**Narrative Consequence examples:**
- "Mira gains trust in you" (relationship change)
- "You escape the chamber" (plot progression)
- "The door locks behind you" (environmental change)
- "You gain the artifact" (inventory change)
- "The timer starts counting down" (mechanic activation)
- "The guard becomes suspicious" (NPC state change)

**Default path** (if no conditional choices are met): [NODE_ID or END_ID]

---

## Mechanic Hooks Summary

<!-- Quick reference of all hooks triggered in this node.
     Review the Mechanic Hooks Checklist below and select which ones apply. -->

| Hook Type | Variable | Action | Timing |
|---|---|---|---|
| VISITED | [VAR_NAME] | set=true | on entry |
| INVENTORY | [ITEM_VAR] | add / check | on entry / choice [A] |
| TRUST | $trust_[npc] | +N | choice [A] |
| NPC_STATE | $npc_[name]_state | set=[value] | choice [B] |

---

## Mechanic Hooks Checklist

<!-- Consider each available hook type for this node. Check which ones apply. -->

**Tier 1 Hooks (Fully Supported)**:

- [ ] **VISITED** — Mark this node as visited for later tracking
  - Example: `visited=player_visited_sanctuary`
  - Use when: Player should remember reaching this location

- [ ] **FLAG** — Set or check boolean state flags
  - Example: `flag=door_unlocked` or check `flag=knows_combination`
  - Use when: Binary state needs to persist (learned fact, completed task)

- [ ] **COUNTER** — Track numeric state (quest progress, attempts, rounds)
  - Example: `counter=escape_attempts +1` or check `counter=riddle_attempts >= 3`
  - Use when: Node needs to count occurrences (failed attempts, items collected, round number)

- [ ] **INVENTORY** — Add/remove/check items
  - Example: `add=key_rusty` or check `contains=lockpick`
  - Use when: Player gains/loses equipment or tools

- [ ] **TIMER** — Start/stop/check elapsed time
  - Example: `start=bomb_timer 30s` or check `timer=ticking expired`
  - Use when: Time pressure or delayed consequence is important

- [ ] **TRUST** — Adjust NPC relationship score (+/- N)
  - Example: `npc=mira delta=+5` (gain 5 trust)
  - Use when: Player dialogue or action affects NPC loyalty/attitude

- [ ] **NPC_STATE** — Change NPC state (suspicious → convinced, etc.)
  - Example: `npc=mira state=convinced`
  - Use when: NPC mood/relationship state progresses beyond simple trust value

- [ ] **CURRENCY** — Add/remove/check money or resources
  - Example: `variable=gold delta=-50` or check `currency=gold >= 100`
  - Use when: Purchasing power or economic consequence matters

- [ ] **ENDING_CONDITION** — Increment progress toward an ending
  - Example: `ending=escape delta=+1` (one step closer to escape ending)
  - Use when: Multiple nodes contribute to reaching a specific ending

- [ ] **RANDOM** — Generate random outcome
  - Example: `variable=random_outcome min=1 max=3`
  - Use when: Node has probabilistic results

- [ ] **CHOICE_MEMORY** — Record player dialogue choice for later reference
  - Example: `variable=player_response value="agreed_to_help"`
  - Use when: Previous dialogue choice should influence later dialogue or prose

- [ ] **CLUE** — Mark a clue as discovered (for detective/puzzle mechanics)
  - Example: `clue_id=clue_suspect_alibi`
  - Use when: Node contains investigative discoveries

**Common Hook Combinations**:

- **Dialogue-centric node**: CHOICE_MEMORY (record dialogue choice) + TRUST (adjust per choice) + NPC_STATE (change mood)
- **Quest hub node**: COUNTER (track active quests) + VISITED (mark as explored) + INVENTORY (check prerequisites)
- **Timed challenge**: TIMER (start countdown) + COUNTER (track attempts) + FLAG (mark as succeeded/failed)
- **Investigation scene**: CLUE (discover evidence) + INVENTORY (collect items) + NPC_STATE (witness becomes suspicious)
- **Relationship branch**: TRUST (major change) + NPC_STATE (reflect new relationship tier) + FLAG (unlock new options)

---

## Branch Logic Notes

[BRANCH_LOGIC_NOTES]
<!-- Any complex conditional logic that needs to be remembered during drafting.
     Example: "This node is only reachable if $trust_mira >= 50 AND $flag_backdoor is false.
     If both conditions are met, choice C unlocks the hidden path to NODE-087." -->

---

## Game Bible Compliance Notes

<!-- Optional. Note any constitution.md constraints relevant to this node:
     mechanic or hook limits, platform/engine restrictions, POV rules, tone requirements.
     Leave blank if no special constraints apply. -->

- [Note or leave blank]

---

## Deviations from plan.md

<!-- If this outline reveals an inconsistency with plan.md (e.g. a variable read here
     that no upstream node sets, or a missing branch edge), record it here before APPROVING.
     Update plan.md first, then set status to APPROVED. -->

- [None / describe any structural deviation]

---

## Quality Check (pre-draft)

<!-- Author fills before changing status to APPROVED -->

- [ ] All variables in "Variables Read" are declared in `variables.md`
- [ ] All variables in "Variables Read" are set by at least one upstream node in `plan.md`
- [ ] All variables in "Variables Set" are declared in `variables.md`
- [ ] At least 2 choices (or 0 for ending/terminal node)
- [ ] No choice is obviously dominant — all have meaningful narrative cost or trade-off
- [ ] All target node IDs exist in `plan.md`
- [ ] Ending nodes registered in `endings.md`
- [ ] Beat summary is specific enough to draft from without ambiguity
- [ ] No `[NEEDS CLARIFICATION]` markers remain unresolved
- [ ] "Deviations from plan.md" is either `None` or has been reconciled in `plan.md`
