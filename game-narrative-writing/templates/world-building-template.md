# World-Building Reference: [GAME_TITLE]

<!-- Living reference document for locations, objects, world rules, and ambient states.
     Updated throughout drafting. speckit.continuity checks node prose against these entries. -->

---

## World Overview

[WORLD_OVERVIEW]
<!-- 100–200 words. The setting's essential nature, tone, and rules.
     What makes this world distinct? What constraints does it place on narrative? -->

---

## World Rules

<!-- Rules that govern the game world and constrain narrative logic.
     Violations are caught by speckit.analyze and speckit.continuity.
     Format: WR-NNN | Rule | Category | First enforced in
     Categories: world-physics / social / technical / magical / mechanical -->

| Rule ID | Rule | Category | First Enforced In | Consequence if violated |
|---|---|---|---|---|
| WR-001 | [NEEDS CLARIFICATION] | world-physics / social / technical / magical / mechanical | NODE-[N] | [what breaks narratively or mechanically] |
| WR-002 | [NEEDS CLARIFICATION] | | | |

### Narrative Boundaries

<!-- What the player cannot do, access, or know in this world. Defines the edge of agency.
     These are not mechanical gates — they are world-level constraints that make choices meaningful. -->

| Boundary | Reason | Nodes where this matters |
|---|---|---|
| [PLAYER_CANNOT_DO_X] | [world-rule rationale] | NODE-[N] |
| [INFORMATION_UNAVAILABLE] | [narrative rationale] | NODE-[N] |

---

## Locations

<!-- One entry per location that appears in nodes. -->

### [LOCATION_NAME] — [LOCATION_ID]

| Field | Value |
|---|---|
| Location ID | LOC-[N] |
| State variable | $location_[name]_state (Tier 2 — stub only) |
| First appears | NODE-[N] |
| Connected to | [LOCATION_IDs] |

**Description** (canonical, second/third person per constitution.md):
[LOCATION_DESCRIPTION]

**Sensory anchors**:
- Sight: [SIGHT] — *"[Direct prose example — one sentence, second/third person per constitution.md]"*
- Sound: [SOUND] — *"[Direct prose example]"*
- Smell: [SMELL] — *"[Direct prose example]"*
- Texture / touch: [TEXTURE] — *"[Direct prose example]"*

**Atmosphere by time/state**:
| State | Atmosphere | Sensory shift |
|---|---|---|
| default | [ATMOSPHERE] | [what changes from baseline] |
| [STATE] | [ATMOSPHERE] | |

**Narrative function**: [What this location does for the story — tension source / sanctuary / decision point / revelation site / environmental pressure]

**Forbidden/off-limits**: [What the player cannot do or access here — creates boundaries and raises stakes]

**Object inventory**:
| Object ID | Object | State | Variable | Interactable |
|---|---|---|---|---|
| OBJ-[N] | [OBJECT_NAME] | [intact/broken/taken] | $object_[name]_state | yes/no |

**Node references**: NODE-[N], NODE-[N]

---

## Objects

<!-- Objects that appear across multiple locations or have mechanical significance. -->

### [OBJECT_NAME] — [OBJECT_ID]

| Field | Value |
|---|---|
| Object ID | OBJ-[N] |
| Location | LOC-[N] |
| Portable | yes / no |
| Inventory item | $inv_[name] (if portable) |
| State variable | $object_[name]_state (Tier 2 — stub only) |

**States**: [intact / broken / repaired / taken / combined]
**Description**: [OBJECT_DESCRIPTION]
**Sensory detail**: *"[Direct prose example — how this object looks, feels, or sounds when interacted with]"*
**Narrative purpose**: [What this object does for the story — Chekhov item / gate / trust signal / world-rule demonstration]
**Story function**: [1–2 sentences on symbolic or thematic role, if any]
**Appears in nodes**: NODE-[N], NODE-[N]

---

## Factions

<!-- Groups with standing in the world. Trust/faction hooks may reference these. -->

| Faction ID | Name | Role | Variable | Default Standing |
|---|---|---|---|---|
| FAC-[N] | [FACTION_NAME] | [FACTION_ROLE] | $faction_[name] (Tier 2) | [neutral/hostile/ally] |

---

## Ambient States

<!-- World-level states that affect multiple locations or narrative conditions.
     Examples: time of day, weather, political state, alert level. -->

| State Variable | Type | Valid Values | Default | Affects |
|---|---|---|---|---|
| [var_name] | flag / counter / enum | [VALUES] | [DEFAULT] | [NODES / LOCATIONS] |

---

## Continuity Log

<!-- Populated by speckit.continuity. Do not edit manually. -->

| Date | Node ID | Issue | Status |
|---|---|---|---|
| | | | |
