# Locations: [STORY_TITLE]

<!-- Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE] -->
<!-- Canonical location reference. speckit.implement loads the relevant entry before
     drafting any scene set in that location. Each location block is self-contained:
     load only the block(s) needed for the scene being drafted. -->

---

## How to Use This File

Before drafting a scene, find the entry for the scene's setting. Load:
- **Sensory Anchors** — the 2–3 details that make this place real on the page
- **Atmosphere by Time/Condition** — the variant that matches the scene's moment
- **What Changes** — what is different after this scene (state continuity)
- **Prohibited Uses** — what the writer must not do with this location

---

## Location Index

| Location ID | Name | Type | First appearance | Status |
|---|---|---|---|---|
| LOC-001 | [Location Name] | [interior / exterior / transitional] | [Beat ID] | [active / abandoned / destroyed] |
| LOC-002 | | | | |

---

<!-- ════════════════════════════════════════════════════════════════
     LOCATION BLOCK TEMPLATE — copy and fill for each named location
     ════════════════════════════════════════════════════════════════ -->

## LOC-001 — [Location Name]

**Type**: [interior / exterior / transitional]
**Scale**: [intimate / domestic / civic / vast]
**Access**: [who can enter, under what conditions]
**First appearance**: [Beat ID]
**Last appearance**: [Beat ID or "open"]

---

### Physical Profile

<!-- Permanent features — things that are always true about this place.
     Do not list things that change; those belong in State Log below. -->

**Layout**:
- [Key spatial fact — size, shape, dominant feature]
- [Entry/exit points and what they mean (e.g., "single door — no escape route")]
- [Vertical dimension if relevant (ceiling height, levels, underground)]

**Permanent fixtures**:
- [Object 1 — always present, always in this position]
- [Object 2]
- [Object 3]

**Materials & surfaces** (for tactile and acoustic grounding):
- [Floor: material, sound, temperature]
- [Walls: material, texture, what they absorb or reflect]
- [Dominant material smell when undisturbed]

---

### Sensory Anchors

<!-- The 2–3 details that identify this location in prose. Use at least one per scene.
     Each anchor must be non-visual or multi-sensory — visual-only anchors are insufficient.
     These are direct prose fragments, not descriptions. -->

**Primary anchor** (must appear in every scene set here):
> "[Exact prose fragment — sensory, specific, 1–2 sentences]"

**Secondary anchor** (use at least once per act this location appears in):
> "[Exact prose fragment]"

**Optional anchor** (use when the scene needs to re-establish the space):
> "[Exact prose fragment]"

**The Dirt Rule detail** (mandatory imperfection — one of these per scene set here):
- [Imperfection option A — physical: crack, stain, broken thing]
- [Imperfection option B — sensory: smell, sound, temperature anomaly]
- [Imperfection option C — human trace: something left behind, worn surface]

---

### Atmosphere by Time / Condition

<!-- How the location changes by time of day, weather, occupancy, or story phase.
     speckit.implement uses the row that matches the scene's `timeline_position`. -->

| Condition | Light | Sound | Smell | Temperature | Mood note |
|---|---|---|---|---|---|
| Dawn / early morning | | | | | |
| Day / working hours | | | | | |
| Dusk / evening | | | | | |
| Night / after hours | | | | | |
| [Weather/season variant] | | | | | |
| [Dramatic condition — e.g., "during confrontation"] | | | | | |

---

### Character Relationships

<!-- How each significant character relates to this location.
     Affects body language, attention focus, and comfort level while in the scene. -->

| Character | Relationship | Behavioral tell in this space |
|---|---|---|
| [Character Name] | [e.g., "childhood home — phantom familiarity"] | [e.g., "touches the door frame before entering"] |
| | | |

---

### Scene Guidance

**Scenes this location drives** (what narrative functions it naturally supports):
- [Function 1 — e.g., "Interrogation / power-asymmetric conversation: single exit focuses pressure"]
- [Function 2]
- [Function 3]

**What this location cannot support** (prohibited uses):
- [e.g., "Do not use for intimate revelation — scale and acoustics work against it"]
- [e.g., "Do not use for comedy — register of the space is wrong"]

**Symbolic register**: [One sentence on what this place means beyond its function]

**Thematic link**: [Which theme or motif from `themes.md` this location reinforces, if any]

---

### State Log

<!-- Track what changes about this location across the story.
     speckit.continuity checks state continuity across scene drafts.
     Add a row each time a scene changes the physical state of this location. -->

| After Beat ID | Chapter ID | What changed | New state |
|---|---|---|---|
| [Beat ID] | [Chapter ID] | [e.g., "Window broken in fight scene"] | [e.g., "Boarded up from Act II-B onward"] |
| | | | |

---
<!-- End LOC-001 -->

## LOC-002 — [Location Name]

*(repeat block)*

---

## Transitional Spaces

<!-- Brief entries for locations that appear in only one or two scenes:
     corridor, vehicle, threshold, unnamed exterior.
     Use paragraph form — no full block needed. -->

### [Transitional Space Name]

**Appears in**: [Beat ID(s)]
**Function**: [What narrative work it does — bridge, compression, contrast]
**Key sensory anchor**: "[prose fragment]"
**Dirt Rule detail**: [one imperfection]