# NPC Relationships: [GAME_TITLE]

<!-- Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE] -->
<!-- Tracks the dynamic between key NPCs — how their states and relationships affect
     each other across branches. Player↔NPC relationships live in characters/[name].md
     Section VI. This file covers NPC↔NPC dynamics that create branch consequences.
     speckit.analyze checks REL-NNN beat coverage in plan.md.
     speckit.continuity checks that NPC state changes are consistent with active dynamics. -->

---

## Relationship Index

| ID | NPC A | NPC B | Type | Dynamic summary | Affects | Status |
|---|---|---|---|---|---|---|
| REL-001 | [NAME] | [NAME] | [see types below] | [One sentence on the repeating loop] | [variable(s) or ending(s)] | `planned` |
| REL-002 | [NAME] | [NAME] | | | | `planned` |

<!-- Relationship types:
     - rivals         In opposition over the same goal or NPC resource (trust, information, territory)
     - allies         Cooperative but with divergent methods or costs — can fracture
     - antagonist     Fundamental opposition — one NPC's arc requires the other's defeat or change
     - mentor/ward    Power-asymmetric — knowledge or protection flows one direction
     - betrayal arc   Starts as ally or neutral; collapses at a defined node
     - history        A past relationship that shapes present behaviour without an active arc
     A relationship can carry more than one type. -->

---

## REL-001 — [NPC A] & [NPC B]: [Relationship Label]

### Relationship Brief

| Field | Value |
|---|---|
| Type(s) | [rivals / allies / antagonist / mentor-ward / betrayal arc / history] |
| Power balance (game open) | [Who holds power at game start — A / B / equal — and why] |
| Power balance (at climax) | [Who holds power at climax — and what shifted it] |
| Founding event | [The backstory event that established this dynamic before the game begins] |
| Central dramatic question | [One sentence — what does this dynamic force to resolution?] |
| What A wants from B | [A's conscious want — stated as A would state it] |
| What B wants from A | [B's conscious want] |
| Shared subtext | [The thing neither NPC says aloud that every scene between them is really about] |
| Thematic link | [Which theme from themes.md this dynamic embodies or tests] |
| Variable(s) affected | [`$npc_[a]_state`, `$trust_[b]`, etc.] |
| Resolution | [resolved / fractured / ongoing at game close — and in which ending(s)] |

---

### Repeating Loop

<!-- The pattern that drives scenes where both NPCs are present.
     This is not a single scene — it is the machine beneath all scenes.
     If the loop can't be described, the dynamic isn't generating branch content yet. -->

**The loop**:
> [What A does in scenes with B] → [How B responds] → [How that response changes variables or unlocks/locks choices]

**What breaks the loop** (the node or condition that forces the dynamic to change):
NODE-[N] or [variable condition]

---

### Branch Coverage

<!-- Which nodes involve both NPCs simultaneously or reference one NPC's state
     when the player is interacting with the other. -->

| Node ID | Act | Both present? | Which NPC's state matters | Branch consequence |
|---|---|---|---|---|
| NODE-[N] | [1/2/3] | [yes/no] | [A / B / both] | [What changes in the branch if dynamic is hostile vs. ally] |

---

### Key Beats

<!-- Five structural beats for this relationship arc.
     Not all need a dedicated node — some can be off-screen, referenced in NPC dialogue.
     Flag any beat without a node reference as [NEEDS NODE]. -->

| Beat | Description | Node ID | Act |
|---|---|---|---|
| Establishing | [How the dynamic is introduced to the player] | NODE-[N] | 1 |
| First rupture | [First moment the dynamic is tested or destabilised] | NODE-[N] | 2 |
| Midpoint shift | [Something irreversible changes — power balance tips or trust breaks] | NODE-[N] | 2 |
| Crisis | [The dynamic reaches its breaking point — player must choose a side or lose both] | NODE-[N] | 3 |
| Resolution | [How the dynamic ends — differs per ending branch] | END-[X] / NODE-[N] | 3 |

---

### Variable Impact Table

<!-- How this relationship's state changes specific variables.
     Used by speckit.analyze to validate that REL beats are reachable. -->

| Beat | Variable changed | New value / delta | Condition |
|---|---|---|---|
| First rupture | `$npc_[b]_state` | `wary` | NODE-[N] reached |
| Crisis | `$trust_[b]` | -20 | Player sides with A |

---

## REL-002 — [NPC A] & [NPC B]: [Relationship Label]

*(repeat block)*

---

## Relationship Drift Log

<!-- Detected inconsistencies from speckit.continuity runs.
     Auto-populated. Do not edit manually. -->

| Date | Node ID | NPC A | NPC B | Issue | Severity | Resolved |
|---|---|---|---|---|---|---|
| | | | | | CRITICAL / WARNING | No |
