# Narrative Design Document: [GAME_TITLE]

<!-- Created: [CREATION_DATE] | Spec: specs/[FEATURE_DIR]/narrative-design-doc.md -->

---

## Logline

[LOGLINE]
<!-- One sentence: player character + central goal + primary obstacle + stakes.
     Example: "A disgraced detective must expose a cover-up before the only witness is silenced,
     knowing the truth will destroy the one person who still believes in her." -->

---

## Premise

[PREMISE]
<!-- ~100 words. The game's core dramatic situation, player agency, and central tension.
     What does the player do? What is at stake? What makes the branching matter?
     End with: "The central question: [dramatic question as a sentence]?" -->

---

## Central Dramatic Question

[DRAMATIC_QUESTION]
<!-- The single question the entire narrative is building toward answering.
     Stated as a question, not an answer.
     Example: "Can Mira expose the conspiracy before the city burns, and at what cost?" -->

---

## Player Arc

<!-- What changes for the player character across the game.
     In choice-IF the player IS the arc � their choices define it. -->

### Starting State
[PLAYER_START_STATE]
<!-- Who/what is the player character at the beginning? What do they want? What do they lack? -->

### Transformation Range

| Ending Direction | Player State Change | Key Choices That Drive It |
|---|---|---|
| [ENDING_A] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| [ENDING_B] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| [ENDING_C] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |

---

## Branch Structure Overview

| Parameter | Value |
|---|---|
| Total acts | [N] |
| Estimated node count | [N] |
| Target endings count | [N] |
| Branch model | [linear-with-branches / branching-remerging / fully-branching / hub-and-spoke] |
| Convergence points | [NEEDS CLARIFICATION] |
| Earliest divergence | [ACT / NODE_ID] |

<!-- Branch model definitions:
     linear-with-branches      mostly linear, short branches that rejoin the main path
     branching-remerging        real branches that reunite at key convergence nodes
     fully-branching            branches that never rejoin; parallel story paths
     hub-and-spoke              central hub nodes with radiating optional excursions -->

### Act Map

| Act | Node Range | Narrative Purpose | Major Beat at Act Boundary | Convergence Node |
|---|---|---|---|---|
| Act 1 | NODE-001�NODE-[N] | Setup / inciting incident | [NEEDS CLARIFICATION] | NODE-[N] |
| Act 2 | NODE-[N]�NODE-[N] | Rising action / complications | [NEEDS CLARIFICATION] | NODE-[N] |
| Act 3 | NODE-[N]�NODE-[N] | Climax / endings | [NEEDS CLARIFICATION] | � |

---

## Key NPCs

<!-- NPCs who appear in multiple nodes and affect branch logic.
     Full profiles live in characters/[npc-name].md. -->

| NPC ID | Name | Role | First Node | Wound / False Belief | Want | Need | Relationship Arc | Trust Hook | State Hook |
|---|---|---|---|---|---|---|---|---|---|
| NPC-001 | [NAME] | [ROLE] | NODE-[N] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [start state] -> [range] | $trust_[name] | $npc_[name]_state |
| NPC-002 | [NAME] | [ROLE] | NODE-[N] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | � | $npc_[name]_state |

---

## Endings Map

<!-- All planned endings. Full conditions and thematic statements live in endings.md. -->

| Ending ID | Name | Type | Rough Gate Conditions | Thematic Statement |
|---|---|---|---|---|
| END-A | [NAME] | [good/bad/neutral/secret/true] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| END-B | [NAME] | [good/bad/neutral/secret/true] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| END-C | [NAME] | [good/bad/neutral/secret/true] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |

<!-- Ending types:
     good    positive resolution for player character
     bad     negative resolution; player failure state
     neutral ambiguous outcome; neither clearly won nor lost
     secret  requires specific hidden conditions; not on obvious path
     true    the "intended" ending unlocked by understanding the full picture -->

---

## Key Scenes / Nodes

<!-- Narrative obligations � these beats MUST appear regardless of branch path.
     Use Given/When/Then format. -->

| Node ID | Scene Name | Act | Type | Arc Served | Branch Conditions |
|---|---|---|---|---|---|
| NODE-001 | [OPENING_NODE] | 1 | opening | Player establishment | none |
| NODE-[N] | [INCITING_NODE] | 1 | inciting | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| NODE-[N] | [MIDPOINT_NODE] | 2 | midpoint | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| NODE-[N] | [CRISIS_NODE] | 2 | crisis | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| NODE-[N] | [CLIMAX_NODE] | 3 | climax | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |

<!-- Node types: opening / setup / exploration / decision / consequence / revelation /
                 midpoint / crisis / climax / ending / hub / transition

     Given/When/Then for each key scene:
     Given [world state before this node],
     When  [player arrives / makes a choice],
     Then  [what changes � consequence, information revealed, variable set]. -->

---

## Design Requirements

<!-- Events and conditions that MUST exist for this to be this game.
     Use MUST language. Violations here block plannings and outlining.
     Mark unknowns as [NEEDS CLARIFICATION: reason]. -->

| DR ID | Requirement | Relates To |
|---|---|---|
| DR-001 | The player MUST [NEEDS CLARIFICATION] | [NPC / NODE / MECHANIC] |
| DR-002 | [NEEDS CLARIFICATION] | |

---

## Key Entities

### Characters

| Name | Role | First Node | Notes |
|---|---|---|---|
| [NAME] | [protagonist / antagonist / ally / etc.] | NODE-[N] | [NEEDS CLARIFICATION] |

### Locations

| Name | Atmosphere Note | Acts Present | Notable Nodes |
|---|---|---|---|
| [LOCATION] | [NEEDS CLARIFICATION] | Act [N] | NODE-[N] |

### Key Items

<!-- Items introduced that must pay off narratively or mechanically. -->

| Item | Introduced At | Narrative/Mechanical Payoff | Payoff Node |
|---|---|---|---|
| [ITEM] | NODE-[N] | [NEEDS CLARIFICATION] | NODE-[N] |

---

## Player Experience Goals

<!-- What the player MUST feel, discover, or experience. Measurable and testable.
     These are design contracts � not vibe notes. -->

| Goal | How It Will Be Achieved | Success Signal |
|---|---|---|
| The player MUST feel [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| The player MUST discover [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | |
| The player MUST experience [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | |

---

## World Rules

<!-- Rules that govern the game world and constrain narrative logic.
     Violations are caught by speckit.analyze and speckit.continuity. -->

| Rule ID | Rule | Category |
|---|---|---|
| WR-001 | [NEEDS CLARIFICATION] | [world-physics / social / technical / mechanical] |
| WR-002 | [NEEDS CLARIFICATION] | |

---

## Research Domains

| Domain | Priority | Notes |
|---|---|---|
| [NEEDS CLARIFICATION] | [high / medium / low] | |

---

## Open Questions

<!-- Unresolved design decisions that must be answered before or during drafting.
     Resolved by speckit.clarify. -->

| ID | Question | Owner | Resolution Deadline |
|---|---|---|---|
| OQ-001 | [NEEDS CLARIFICATION] | [AUTHOR] | Before Act [N] drafting |

---

## Assumptions & Scope

| Parameter | Value |
|---|---|
| Genre | [NEEDS CLARIFICATION] |
| Engine preference | [sugarcube / ink / both / undecided] |
| Player perspective | [second-person / third-person / first-person / switching] |
| Target audience | [NEEDS CLARIFICATION] |
| Tone | [NEEDS CLARIFICATION] |
| Estimated play time | [N] minutes |
| Series position | [standalone / series � entry N of M] |
| Series title | [NEEDS CLARIFICATION / N/A if standalone] |
| Series bible path | [specs/series-bible.md / N/A if standalone] |
| Sequel threads left open | [NEEDS CLARIFICATION] |
| What this game IS | [NEEDS CLARIFICATION] |
| What this game IS NOT | [NEEDS CLARIFICATION] |
