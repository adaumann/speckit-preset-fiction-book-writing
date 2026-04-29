# Game Story Brief: [GAME_TITLE]

<!-- Created: [CREATION_DATE] | Brief: specs/[FEATURE_DIR]/spec.md -->

---

## Logline

[LOGLINE]
<!-- One sentence. Formula: [Player character] must [goal] before/or [stakes/antagonist force].
     Example: "A disgraced detective must expose a cover-up before the only witness is silenced,
     knowing the truth will destroy the one person who still believes in her." -->

---

## Premise

[PREMISE]
<!-- ~100 words. The game's core dramatic situation, player agency, and central tension.
     What does the player do? What is at stake? What makes the branching matter?
     No engine choices. No mechanic implementation details.
     End with: "The central question: [dramatic question as a sentence]?" -->

---

## Opening Node Hook

<!-- What must the player know, feel, or suspect by the end of Node 1.
     Be explicit — vague intent produces generic openings. -->

- **Player must know**: [NEEDS CLARIFICATION]
  <!-- The one fact or situation that orients the player immediately -->
- **Player must feel**: [NEEDS CLARIFICATION]
  <!-- The emotional register established in the opening node -->
- **Player must suspect**: [NEEDS CLARIFICATION]
  <!-- The question or dread that pulls the player forward -->
- **Deliberately withheld**: [NEEDS CLARIFICATION]
  <!-- What the player does NOT yet know — name the gap that creates forward momentum -->

---

## Player Arc

<!-- What changes for the player character across the game.
     In choice-IF the player IS the arc — their choices define it.
     P1 = drives the main plot. -->

### Arc: [PLAYER_CHARACTER] — Priority: P1
- **Internal wound / false belief**: [NEEDS CLARIFICATION]
- **Want** (external goal the player character pursues): [NEEDS CLARIFICATION]
- **Need** (thematic truth they must confront): [NEEDS CLARIFICATION]
- **Transforms from → to**: [NEEDS CLARIFICATION]
  <!-- In a choice game, state the range: what does the character become at each major ending direction? -->
- **Player agency expression**: [NEEDS CLARIFICATION]
  <!-- How do the player's choices manifest this arc — what kinds of decisions force the wound to the surface? -->
- **Key contradiction**: [NEEDS CLARIFICATION]

### Transformation Range

| Ending Direction | Player State Change | Key Choices That Drive It |
|---|---|---|
| [ENDING_A] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| [ENDING_B] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |
| [ENDING_C] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] |

---

## NPC Arcs

<!-- One entry per NPC whose arc is load-bearing for the narrative.
     These are the characters the player's choices force into transformation.
     Independent Arc Test: could the NPC's transformation be understood in isolation? -->

### Arc: [NPC_NAME] — Priority: P2
- **Internal wound / false belief**: [NEEDS CLARIFICATION]
- **Want** (surface goal): [NEEDS CLARIFICATION]
- **Need** (thematic truth): [NEEDS CLARIFICATION]
- **Transforms from → to**: [NEEDS CLARIFICATION]
- **Trust hook**: [NEEDS CLARIFICATION]
  <!-- Variable name tracking the player–NPC relationship state, e.g. $trust_mira -->
- **Independent arc test**: [Can this arc be understood without the player arc? yes/no + rationale]

### Arc: [NPC_NAME] — Priority: P3
- **Internal wound / false belief**: [NEEDS CLARIFICATION]
- **Want**: [NEEDS CLARIFICATION]
- **Need**: [NEEDS CLARIFICATION]
- **Transforms from → to**: [NEEDS CLARIFICATION]
- **Independent arc test**: [yes/no + rationale]

---

## Key Relationship Arcs

<!-- Load-bearing player–NPC or NPC–NPC relationships that carry and test the player arc's central wound.
     These are the mechanism through which the player's choices are forced to mean something.
     RA = Relationship Arc. -->

### RA-001: [PLAYER_CHARACTER] ↔ [NPC_NAME] — Role: [mentor / rival / ally / antagonist / foil]
- **Opens as**: [State of the relationship at game start]
- **Stress point**: [The node or event where the relationship breaks, shifts, or reveals its true nature]
- **Closes as**: [State at the end — may differ per ending branch]
- **Function**: [What wound or arc does this relationship force to the surface?]

### RA-002: [CHARACTER_A] ↔ [CHARACTER_B] — Role: [NEEDS CLARIFICATION]
- **Opens as**: [NEEDS CLARIFICATION]
- **Stress point**: [NEEDS CLARIFICATION]
- **Closes as**: [NEEDS CLARIFICATION]
- **Function**: [NEEDS CLARIFICATION]

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
| Act 1 | NODE-001–NODE-[N] | Setup / inciting incident | [NEEDS CLARIFICATION] | NODE-[N] |
| Act 2 | NODE-[N]–NODE-[N] | Rising action / complications | [NEEDS CLARIFICATION] | NODE-[N] |
| Act 3 | NODE-[N]–NODE-[N] | Climax / endings | [NEEDS CLARIFICATION] | — |

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

<!-- Narrative obligations — these beats MUST appear regardless of branch path.
     Map each as a Given/When/Then contract.
     These are the scenes that cannot be cut; if one doesn't deliver its Then, revise it. -->

### Node: [OPENING_NODE] — Act 1 / opening
- **Given**: [World state and player character state at this node's opening]
- **When**: [The inciting action, decision, or revelation]
- **Then**: [Changed world state, character state, or player understanding]
- **Arc served**: P1
- **Branch conditions**: none
- **Variable set**: [VAR_NAME = VALUE]

### Node: [INCITING_NODE] — Act 1 / inciting incident
- **Given**: [NEEDS CLARIFICATION]
- **When**: [NEEDS CLARIFICATION]
- **Then**: [NEEDS CLARIFICATION]
- **Arc served**: [NEEDS CLARIFICATION]
- **Branch conditions**: [NEEDS CLARIFICATION]

### Node: [MIDPOINT_NODE] — Act 2 / midpoint
- **Given**: [NEEDS CLARIFICATION]
- **When**: [NEEDS CLARIFICATION]
- **Then**: [NEEDS CLARIFICATION]
- **Arc served**: [NEEDS CLARIFICATION]
- **Branch conditions**: [NEEDS CLARIFICATION]

### Node: [CRISIS_NODE] — Act 2 / crisis
- **Given**: [NEEDS CLARIFICATION]
- **When**: [NEEDS CLARIFICATION]
- **Then**: [NEEDS CLARIFICATION]
- **Arc served**: [NEEDS CLARIFICATION]
- **Branch conditions**: [NEEDS CLARIFICATION]

### Node: [CLIMAX_NODE] — Act 3 / climax
- **Given**: [NEEDS CLARIFICATION]
- **When**: [NEEDS CLARIFICATION]
- **Then**: [NEEDS CLARIFICATION]
- **Arc served**: [NEEDS CLARIFICATION]
- **Branch conditions**: [NEEDS CLARIFICATION]

<!-- Node types: opening / setup / exploration / decision / consequence / revelation /
                 midpoint / crisis / climax / ending / hub / transition -->

---

## Design Requirements

<!-- Things that MUST happen in the game for it to be this game.
     Use MUST language. Mark unknowns as [NEEDS CLARIFICATION: reason].
     DR = Design Requirement. These are narrative obligations — violations block planning. -->

- **DR-001** MUST: [Core narrative event that must occur]
- **DR-002** MUST: [Another mandatory story beat]
- **DR-003** MUST: [NEEDS CLARIFICATION: describe what's uncertain]

---

## Act Boundaries & Structural Beats

<!-- Maps WHEN the Design Requirements happen within the chosen structure.
     Populate with your act structure; adjust rows as needed. -->

| Beat | Description | Approx. Node Range | DR IDs anchored here |
|---|---|---|---|
| Act 1 Opening | Setup — world and player character established | NODE-001–[N] | |
| Inciting Incident | The event that makes the status quo impossible | NODE-[N] | |
| Act 1 Convergence | Player commits to the game's central goal; earliest divergence begins | NODE-[N] | |
| Midpoint | False victory or false defeat; stakes escalate | NODE-[N] | |
| Act 2 Convergence | Lowest point; wound fully exposed | NODE-[N] | |
| Climax | Player confronts central conflict across branch paths | NODE-[N]–[N] | |
| Endings | Consequences established per branch | NODE-[N]–END | |

**Pacing intent**: [NEEDS CLARIFICATION]
<!-- Describe the intended emotional energy curve: e.g., slow-burn build with a compressed Act 3;
     or relentless escalation with deliberate breathing nodes after each act convergence. -->

---

## Key Entities

### Characters

| Name | Role | First Node | Arc |
|---|---|---|---|
| [CHARACTER] | [protagonist / antagonist / ally / foil / etc.] | NODE-[N] | [P1/P2/P3] |

### Locations

| Name | Atmosphere Note | Acts Present | Notable Nodes |
|---|---|---|---|
| [LOCATION] | [Sensory anchors, mood, significance] | Act [N] | NODE-[N] |

### Key Items

<!-- Objects or facts introduced that MUST pay off narratively or mechanically.
     The spec will enforce these are not forgotten. -->

| Item | Introduced At | Narrative / Mechanical Payoff | Payoff Node |
|---|---|---|---|
| [ITEM] | NODE-[N] | [NEEDS CLARIFICATION] | NODE-[N] |

### World Rules

<!-- Inviolable facts of this game's world. Violations are caught by speckit.analyze and speckit.continuity. -->

| ID | Rule | Category | Source / established in |
|---|---|---|---|
| WR-001 | [NEEDS CLARIFICATION] | [world-physics / social / technical / mechanical / geography] | [spec / node name] |
| WR-002 | [NEEDS CLARIFICATION] | | |
<!-- Categories:
     world-physics  → what the laws of nature allow or forbid
     social         → power structures, factions, norms that cannot be handwaved
     technical      → technology that exists / does not exist / is prototype-only
     mechanical     → hard rules of a magic or game system
     geography      → fixed locations, distances, travel times
     other          → any inviolable fact not covered above -->

### Research Domains

<!-- Topics that require investigation before drafting begins.
     Feeds speckit.research scope. -->

| Domain | Accuracy requirement | Notes |
|---|---|---|
| [DOMAIN] | [accurate / fictionalized / accurate-with-exceptions] | [NEEDS CLARIFICATION] |
<!-- Examples:
     | 1940s police procedure | accurate | Interrogation and evidence rules must be realistic |
     | Psychic ability mechanics | fictionalized | Internal consistency only |
     | 19th-century maritime trade | accurate | Research before drafting Acts 1–2 | -->

---

## Player Experience Goals

<!-- Measurable player outcomes. Use MUST language.
     These are design contracts — not vibe notes. Success criteria for the game.
     PG = Player Goal. -->

- **PG-001** The player MUST feel [emotion] at [story moment / node]
- **PG-002** The player MUST be surprised by [revelation] — the surprise must feel earned in retrospect
- **PG-003** The player MUST not be able to stop playing at [act convergence / node]
- **PG-004** [NEEDS CLARIFICATION]

---

## Assumptions & Scope

### This game IS
- [What this game promises to be / deliver]
- [Genre, tone, what kind of endings are on offer]

**Tone**: [TONE]
<!-- The emotional register the prose sustains across the whole game.
     Examples: sardonic-but-warm · bleak-with-earned-hope · clinical-detachment · tense-and-urgent
     This feeds the constitution's Tone field. -->

### This game is NOT
- [What this game deliberately excludes]
- [What will not be resolved within this game entry]

**Target node count**: [N]
**Target endings count**: [N]
**Target audience**: [adult / new-adult / young-adult / teen / all-ages]
**Engine preference**: [sugarcube / ink / undecided]

**Series / sequel threads left open**:
<!-- Name unresolved threads deliberately held for a future entry.
     These are OUT OF SCOPE for this game's resolution. The AI must not close them.
     Set to "none" if standalone. -->
- [THREAD_NAME]: [Brief description of what is left open and why]

**Series position**: [standalone / game N of N / open series]

### Open Questions & Deferred Decisions

<!-- Unresolved design decisions that must be settled before or during planning.
     OQ = Open Question. -->

| ID | Question | Owner | Must resolve before |
|---|---|---|---|
| OQ-001 | [NEEDS CLARIFICATION — e.g., "Does the antagonist survive any branch?"] | [author / speckit.clarify] | [planning / Act 2 outline / Act 3 outline] |
| OQ-002 | [NEEDS CLARIFICATION] | | |
