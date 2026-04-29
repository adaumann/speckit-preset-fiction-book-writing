---
node_id: [NODE_ID]
title: [NODE_TITLE]
act: [ACT_NUMBER]
status: DRAFT
# status: DRAFT | APPROVED | SKIP
# DRAFT    → speckit.implement gates — will not draft until changed to APPROVED
# APPROVED → speckit.implement will draft prose for this node
# SKIP     → speckit.implement skips this node entirely
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
     speckit.implement uses this table to generate the ## Choices section in the node file.
     export.py requires: ## Choices heading + - [Label](NODE-ID) <!-- condition --> format. -->

| # | Label | Condition | Target Node | Narrative Consequence |
|---|---|---|---|---|
| A | [CHOICE_LABEL] | none | NODE-[N] | [What changes / where this leads] |
| B | [CHOICE_LABEL] | none | NODE-[N] | [What changes / where this leads] |
| C | [CHOICE_LABEL] | requires [VAR CONDITION] | NODE-[N] | [What changes / where this leads] |

**Default path** (if no conditional choices are met): [NODE_ID or END_ID]

---

## Mechanic Hooks Summary

<!-- Quick reference of all hooks triggered in this node. -->

| Hook Type | Variable | Action | Timing |
|---|---|---|---|
| VISITED | [VAR_NAME] | set=true | on entry |
| INVENTORY | [ITEM_VAR] | add / check | on entry / choice [A] |
| TRUST | $trust_[npc] | +N | choice [A] |
| NPC_STATE | $npc_[name]_state | set=[value] | choice [B] |

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

## Deviations from flowmap.md

<!-- If this outline reveals an inconsistency with flowmap.md (e.g. a variable read here
     that no upstream node sets, or a missing branch edge), record it here before APPROVING.
     Update flowmap.md first, then set status to APPROVED. -->

- [None / describe any structural deviation]

---

## Quality Check (pre-draft)

<!-- Author fills before changing status to APPROVED -->

- [ ] All variables in "Variables Read" are declared in `variables.md`
- [ ] All variables in "Variables Read" are set by at least one upstream node in `flowmap.md`
- [ ] All variables in "Variables Set" are declared in `variables.md`
- [ ] At least 2 choices (or 0 for ending/terminal node)
- [ ] No choice is obviously dominant — all have meaningful narrative cost or trade-off
- [ ] All target node IDs exist in `flowmap.md`
- [ ] Ending nodes registered in `endings.md`
- [ ] Beat summary is specific enough to draft from without ambiguity
- [ ] No `[NEEDS CLARIFICATION]` markers remain unresolved
- [ ] "Deviations from flowmap.md" is either `None` or has been reconciled in `flowmap.md`
