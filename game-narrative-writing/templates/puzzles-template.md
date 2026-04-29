# Puzzle Registry: [GAME_TITLE]

<!-- Feature: [FEATURE_DIR] | Spec: specs/[FEATURE_DIR]/spec.md -->
<!-- This document tracks the logical and physical dependencies of Point-and-Click puzzles. 
     Each puzzle must have a clear Solution, required State (Variables), and Outcomes. -->

---

## I. Logic Gating (Knowledge & Dialogue)

| Puzzle ID | Narrative Goal | Required Knowledge | Required NPC State | Outcome |
|---|---|---|---|---|
| PZ-101 | [e.g., Get the safe code] | [know_maid_secret] | [npc_maid_state=trusting] | [set $inv_safe_code] |

---

## II. Physical Gating (Lock & Key & Combat)

| Puzzle ID | Interactable Object | Required Item | Required Location State | Outcome |
|---|---|---|---|---|
| PZ-201 | [e.g., Studio Door] | [inv_silver_key] | [loc_hallway_lights=on] | [set obj_studio_door=unlocked] |

---

## III. Item Combinations (Inventory Puzzles)

| Puzzle ID | Item 1 | Item 2 | Resulting Item | Notes |
|---|---|---|---|---|
| CZ-001 | [e.g., Rusty Key] | [e.g., Oil Can] | [inv_clean_key] | [Requires 'interact' verb] |

---

## IV. Detailed Puzzle Breakdowns

### [PUZZLE_NAME] (PZ-[NNN])

**Summary**: [One sentence describing the player's goal.]

**Interaction Modes (Verbs)**:
*   **Examine**: [Result of 'Look At']
*   **Interact**: [Result of 'Use/Pull/Push']
*   **Talk**: [Target NPC response regarding this puzzle]

**Dependencies (The 'In' conditions)**:
- [ ] **Physical**: [e.g., must have $inv_screwdriver]
- [ ] **Contextual**: [e.g., must be in room $loc_basement]
- [ ] **Knowledge**: [e.g., must have read the 'Manual' — $know_wiring]

**The Interaction (The 'Middle')**:
- **Point-and-Click Action**: [e.g., 'Use Screwdriver on Loose Panel']
- **Dialogue/Feedback**: [e.g., "The screws are rusted, but they turn with a screech."]

**Resolution (The 'Out' conditions)**:
- [ ] **Variable Changes**: [e.g., $obj_panel_open=true]
- [ ] **New Paths**: [e.g., unlocks NODE-204]
- [ ] **Items Consumed**: [e.g., removes $inv_key_card]

---

## V. Deadlock Check

<!-- Use this to ensure puzzles can actually be solved in the current node graph. -->

| Puzzle | Can it be solved later? | Is it missable? | Status |
|---|---|---|---|
| [ID] | [Yes/No - if player leaves area] | [Yes/No] | [Verified/Open] |
