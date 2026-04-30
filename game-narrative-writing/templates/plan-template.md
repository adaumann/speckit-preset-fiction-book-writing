# Flowmap: [GAME_TITLE]

<!-- Branch/Dir: [FEATURE_DIR] | Date: [PLAN_DATE] | Spec: specs/[FEATURE_DIR]/spec.md -->

---

## Summary

**Central conflict**: [PRIMARY_CONFLICT]
**Narrative approach**: [NARRATIVE_APPROACH]
<!-- Brief statement of how this game will be experienced: player perspective, branch model,
     tonal register. Example: "Second-person branching-remerging, past-reflective narration,
     three acts converging at a single climax with five diverging endings." -->

---

## Narrative Parameters

| Parameter | Value |
|---|---|
| Branch Model | [BRANCH_MODEL] |
| Genre | [NEEDS CLARIFICATION] |
| Engine Target | [NEEDS CLARIFICATION] |
| Player Perspective | [NEEDS CLARIFICATION] |
| Estimated Play Time | [NEEDS CLARIFICATION] |
| Total Nodes Planned | [N] |
| Total Endings | [N] |
| Target Audience | [NEEDS CLARIFICATION] |
| Series Position | [standalone / series entry N] |
| Tone | [NEEDS CLARIFICATION] |
| Game Bible Version | [NEEDS CLARIFICATION] |

---

## Game Bible Check

<!-- Gates that MUST pass before node authoring begins.
     Mark each: ? PASS / ?? NEEDS WORK / ? VIOLATION + justification.
     A ? VIOLATION blocks progression unless justified below. -->

<!-- Status values used by speckit.plan:
     ? PASS        � gate satisfied
     ?? NEEDS WORK  � partially satisfied; action required before authoring
     ? VIOLATION   � gate fails; blocks Phase 0 until justified below -->

| Gate | Status | Notes |
|---|---|---|
| Central dramatic question declared in spec.md | [NEEDS CLARIFICATION] | |
| Player arc: starting state and transformation range documented | [NEEDS CLARIFICATION] | |
| All planned endings registered in endings.md | [NEEDS CLARIFICATION] | |
| No unresolved [NEEDS CLARIFICATION] markers in spec.md | [NEEDS CLARIFICATION] | |
| Export target set in constitution.md | [NEEDS CLARIFICATION] | |
| Active mechanics declared in constitution.md Section II | [NEEDS CLARIFICATION] | |
| All Tier 1 hooks registered in variables.md before use | [NEEDS CLARIFICATION] | |
| World Rules (WR-NNN) defined with no unresolved entries | [NEEDS CLARIFICATION] | |
| Open Questions (OQ-NNN) resolved or have a resolution deadline | [NEEDS CLARIFICATION] | |
| All key NPCs have a profile in characters/ | [NEEDS CLARIFICATION] | |
| Game bible version recorded and ratified | [NEEDS CLARIFICATION] | |
| **[Series only]** specs/series-bible.md exists with carry-over variable registry | [N/A if standalone] | |

### Justified Violations

| Gate | Rationale |
|---|---|
| | |

---

## Act Structure

<!-- Node counts and dramatic purpose per act.
     Convergence nodes are where branches must rejoin before the next act. -->

| Act | Node Count | Key Convergence Node | Narrative Goal |
|---|---|---|---|
| Act 1 | [N] | NODE-1[NNN] | Setup, inciting incident, first branching decision |
| Act 2 | [N] | NODE-2[NNN] | Rising action, complication, midpoint revelation |
| Act 3 | [N] | � | Climax, diverge to endings |

---

## Node Graph

<!-- Text representation of the branch graph.
     Use speckit.flowmap to generate the Mermaid diagram.
     Format: NODE-ID: [description] � choice text > NODE-ID | choice text > NODE-ID -->

### Act 1

```
NODE-1001: [OPENING_NODE]
  -> [Choice A] NODE-1002
  -> [Choice B] NODE-1003

NODE-1002: [SETUP_A]
  -> NODE-1004

NODE-1003: [SETUP_B]
  -> NODE-1004

NODE-1004: [CONVERGENCE - ACT 1 END]
  -> NODE-2001
```

### Act 2

```
NODE-2001: [ACT_2_OPEN]
  -> [Choice A] NODE-2002
  -> [Choice B] NODE-2003
  -> [Choice C - requires $inv_key] NODE-2004

NODE-2002: ...
```

### Act 3

```
NODE-3[N]: [CLIMAX]
  -> [Choice A - requires $end_A_progress >= 3] END-A_[Name]
  -> [Choice B] END-B_[Name]
  -> [Choice C] END-C_[Name]
```

---

## Information Asymmetry Map

<!-- Which variables gate what information, and which NPCs know what at which point.
     Prevents branching logic that assumes knowledge the player cannot have. -->

| Node ID | Information Revealed | Variable Set | Player Must Not Know Before |
|---|---|---|---|
| NODE-[N] | [INFO] | $flag_[name] | NODE-[N] |
| NODE-[N] | [INFO] | $trust_[npc] >= 50 | � |

---

## Branch Health Check

<!-- Run speckit.analyze to populate this automatically. Fill manually during planning. -->

| Check | Status | Node IDs |
|---|---|---|
| Dead ends (non-ending nodes with no outgoing choices) | [NEEDS CLARIFICATION] | |
| Unreachable nodes (no path leads to them) | [NEEDS CLARIFICATION] | |
| Variables read before set | [NEEDS CLARIFICATION] | |
| Endings with no reachable path | [NEEDS CLARIFICATION] | |
| Nodes with only 1 choice (non-terminal) | [NEEDS CLARIFICATION] | |

---

## Pacing Overview

<!-- tension_score: 1 (calm) to 10 (climax). -->

| Act | Decision Density | Avg Tension | Mechanic Trigger Nodes | Notes |
|---|---|---|---|---|
| Act 1 | low to rising | 3�5 | [N] | Establish world, introduce hooks |
| Act 2 | high | 5�8 | [N] | Complications, NPC state changes |
| Act 3 | very high to resolution | 7�10 | [N] | Endings diverge |

---

## Supporting Documents

| Document | Purpose | Status |
|---|---|---|
| `specs/variables.md` | All state variables � types, defaults, read/write map, ending gates | [NEEDS CLARIFICATION] |
| `specs/mechanics.md` | Hook schemas per mechanic type; engine-specific syntax | [NEEDS CLARIFICATION] |
| `specs/endings.md` | Endings registry: gate conditions, thematic statements, final node IDs | [NEEDS CLARIFICATION] |
| `characters.md` | Character index: NPC roster, trust variable registry, relationship map | [NEEDS CLARIFICATION] |
| `characters/[name].md` | Full NPC profile: arc, voice, relationship arc with player, scene guidance | [NEEDS CLARIFICATION] |
| `specs/world-building.md` | Locations, world rules, faction logic, sensory anchors | [NEEDS CLARIFICATION] |
| `glossary.md` | Invented terms, proper nouns, variable name register | [NEEDS CLARIFICATION] |
| `specs/series-bible.md` | Carry-over variable registry, series continuity | [exists / N/A if standalone] |

---

## Open Narrative Threads

<!-- Track every promise made to the player that must be paid off.
     Populate from Key Items in spec.md + any discovered during planning. -->

| Thread | Introduced | Must resolve by | Status |
|---|---|---|---|
| [Thread description] | [Node ID] | [Node ID or "any ending"] | open |

---

## Complexity Notes

<!-- Justified deviations from the game bible or branch structure plan. -->

| Decision | Justification |
|---|---|
| | |

---

## Node Outline

<!-- Generated by speckit.plan. One entry per node.
     A "node" is a discrete narrative unit the player reaches via navigation or choice.

     Node ID format: NODE-{act}{sequential_3digit}_{ShortName}
       Act 1 nodes  -> NODE-1001_Awakening, NODE-1002_FirstChoice
       Act 2 nodes  -> NODE-2001_Complication, NODE-2003_BetrayalRevealed
       Act 3 nodes  -> NODE-3001_Climax, NODE-3002_FinalGate
       Endings      -> END-A_TrueReconciliation, END-B_Sacrifice, END-C_Escape
     Insertion nodes use letter suffix: NODE-2003b between NODE-2003 and NODE-2004

     Branch types:
       choice    -- presents 2+ choices to the player
       converge  -- merge node, no choice presented
       gate      -- content gated by variable; may branch or converge
       terminal  -- an ending node (use END- prefix) -->

### Node: [NODE_ID] -- [NODE_NAME]
<!-- Example: Node: NODE-1001 -- Opening -->

| Field | Value |
|---|---|
| **Estimated word count** | [range, e.g., 300�600 words] |
| **Act** | [1 / 2 / 3] |
| **Branch type** | [choice / converge / gate / terminal] |
| **Player perspective** | [2nd-person / 3rd-person / uses $pov � omit if not a switching game] |
| **Location** | [location name from world-building.md] |
| **Variables read** | [$var_name (condition)] |
| **Variables written** | [$var_name = value] |
| **NPC presence** | [NPC name -- emotional state] |
| **Status** | outline |

**Opening hook**: [Sensory detail -- not summary. Drop the player into a moment.]

**Key beats** (3�5 micro-events in causal order):
1. [Beat 1 -- causal event]
2. [Beat 2 -- complication or reveal]
3. [Beat 3 -- NPC reaction or world response]
4. [Beat 4 -- optional]
5. [Beat 5 -- optional]

**Choice architecture**:

| Choice text | Condition | Target node | Effect |
|---|---|---|---|
| [Choice A text] | [none / $var condition] | NODE-[N] | [$var_name = value] |
| [Choice B text] | [none / $var condition] | NODE-[N] | [$var_name = value] |

**Thematic work**: [How theme is carried in this node without being stated explicitly.]

**Closing beat**: [What has irreversibly changed. What the player now knows or suspects.]

<!-- Required beat flag (if applicable): [REQUIRED: fulfills KEY-SCENE-N] -->
