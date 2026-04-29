---
title: [GAME_TITLE]
author_name: [AUTHOR_NAME]
studio_name: [STUDIO_NAME]
language: [LANGUAGE]
tone: [TONE]
copyright: [COPYRIGHT]
dramatic_question: [DRAMATIC_QUESTION]
genre: [GENRE]
narrative_mode: [NARRATIVE_MODE]
# NARRATIVE_MODE: linear | branching | point-and-click | emergent
export_target: [EXPORT_TARGET]
# EXPORT_TARGET: generic | sugarcube | ink
# Use 'generic' to keep prose engine-agnostic until export.
player_perspective: [PLAYER_PERSPECTIVE]
pov_variable: [POV_VARIABLE]
target_audience: [TARGET_AUDIENCE]
series_position: [standalone]
game_bible_version: [GAME_BIBLE_VERSION]
---

<!-- SYNC IMPACT: (populated by speckit.constitution on each update)
     Format: v[OLD] → v[NEW] | Changed: [summary] | Affected: [files] | Action required: [action] -->

# [GAME_TITLE] Game Bible
<!-- Your game's governing document. This overrides all writing prompts and templates. -->

---

## I. Export Configuration

| Parameter | Value |
|---|---|
| Export Target | [EXPORT_TARGET] |
| Export Format | [EXPORT_FORMAT] |
| Narrative Mode | [NARRATIVE_MODE] |
| Player Perspective | [PLAYER_PERSPECTIVE] |
| POV Variable | [POV_VARIABLE] |
| Language | [LANGUAGE] |
| Tone | [TONE] |
| Studio / Author | [STUDIO_NAME] / [AUTHOR_NAME] |

<!-- EXPORT_TARGET: generic | sugarcube | ink
     EXPORT_FORMAT: markdown (for generic) | twee3 (for sugarcube) | ink (for ink)
     PLAYER_PERSPECTIVE: second-person | third-person | first-person | switching
     POV_VARIABLE: name of the variable used when switching (e.g. $pov) — leave blank if not switching -->

---

## II. Active Mechanics

<!-- List all mechanic hooks used in this project.
     Hooks not declared here will trigger a validation error in speckit.checklist.
     Tier 1 hooks are fully exported. Tier 2 hooks export with a warning comment. -->

### Tier 1 Hooks (v1.0 — fully exported)

| Hook | Enabled | Notes |
|---|---|---|
| `flag` | [yes/no] | |
| `counter` | [yes/no] | |
| `visited` | [yes/no] | |
| `inventory` | [yes/no] | |
| `timer` | [yes/no] | |
| `trust` | [yes/no] | |
| `currency` | [yes/no] | |
| `npc_state` | [yes/no] | |
| `ending_condition` | [yes/no] | |

### Tier 2 Hooks (v1.x — stubs, export with warning)

| Hook | Enabled | Notes |
|---|---|---|
| `knowledge` | [yes/no] | |
| `faction` | [yes/no] | |
| `location_state` | [yes/no] | |
| `object_state` | [yes/no] | |
| `choice_memory` | [yes/no] | |
| `clue` | [yes/no] | |

### Tier 3 Hooks (v2.x — point-and-click / high-fidelity)

| Hook | Enabled | Notes |
|---|---|---|
| `verb` | [yes/no] | Examine/Interact/Talk modes |
| `move` | [yes/no] | Character navigation/walking |
| `hotspot` | [yes/no] | UI visibility tracking |
| `audio` | [yes/no] | Scripted SFX triggers |
| `inventory_combine` | [yes/no] | Item crafting/merging |
| `gated_choice` | [yes/no] | Timed decisions |

---

## III. Inventory Configuration
<!-- Only fill when Hook: inventory is enabled -->

```yaml
inventory:
  type: array          # array | slots
  capacity: [N]        # max items; 0 = unlimited
  persistence: save    # save | session (session = resets on load)
  weight_system: false # true = items have weight values in glossary.md
```

---

## IV. Timer Configuration
<!-- Only fill when Hook: timer is enabled -->

```yaml
timer:
  type: turns          # turns | countdown
  unit: turns          # turns | seconds (seconds: Sugarcube JS only)
  failure_node: [NODE_ID]   # node reached when timer expires
  warning_threshold: [N]    # turns remaining when warning fires
```

---

## V. Attribute Configuration
<!-- Fill for RPG-style numeric attributes tracked as counters or trust hooks -->

| Attribute | Variable Name | Range | Default | Hook Type |
|---|---|---|---|---|
| [NAME] | [VAR_NAME] | [MIN–MAX] | [DEFAULT] | counter / trust |
| [NAME] | [VAR_NAME] | [MIN–MAX] | [DEFAULT] | counter / trust |

---

## VI. Currency Configuration
<!-- Only fill when Hook: currency is enabled -->

```yaml
currency:
  name: [CURRENCY_NAME]   # e.g. gold, credits, favors
  variable: [VAR_NAME]    # e.g. $gold
  starting_amount: [N]
  minimum: 0              # can go negative? set to -999 if yes
```

---

## VII. Prose Style Mode

<!-- Configured by speckit.constitution. Referenced by speckit.implement and speckit.checklist
     for voice consistency validation. Do not edit manually after ratification without
     running speckit.constitution --update. -->

| Field | Value |
|---|---|
| Style mode | [author-sample / humanized-ai] |
| Tense | [past / present] |
| Sentence rhythm | [short-punchy / varied / long-flowing] |
| Vocabulary register | [plain / literary / technical / colloquial] |
| Sensory density | [low / medium / high] |
| Dialogue style | [direct / oblique / subtext-heavy] |
| Anti-AI filter active | [yes / no] |

**Extracted voice markers** *(author-sample mode only — leave blank for humanized-ai)*:
- Signature constructions: [e.g. sentence fragments for tension, em-dash for interruption]
- Recurring imagery patterns: [e.g. light/dark, industrial, organic]
- Words/phrases to avoid: [extracted from sample]
- Sample sentence rhythm: [e.g. "Short declarative. Then longer clause that opens out into something uncertain."]

---

## VIII. Craft Rules

### Universal Node Rules

These rules apply to every node regardless of engine target.

| Rule ID | Rule | Scope |
|---|---|---|
| NR-001 | Every non-terminal node must offer at least 2 meaningful choices | per node |
| NR-002 | Choices must differ in consequence, not just phrasing | per node |
| NR-003 | No choice may be obviously dominant — all options must have narrative cost | per node |
| NR-004 | Dead ends (no outgoing choices, not an ending node) are a validation error | per node |
| NR-005 | Every mechanic hook must be declared in variables.md before use | per project |
| NR-006 | Variables must be set before they are read (no read-before-set) | per branch |
| NR-007 | Ending nodes must be registered in endings.md | per project |
| NR-008 | Prose must cohere without hook blocks (hooks are annotations, not load-bearing) | per node |

### Prose Style Rules

| Rule ID | Rule | Scope |
|---|---|---|
| PR-001 | Player perspective declared in Section I must be consistent across all nodes | per project |
| PR-002 | No on-the-nose emotional labelling ("you feel sad") — show through action/sensation | per node |
| PR-003 | Opening line of each node must orient player: where, who, what is at stake | per node |
| PR-004 | Choice labels must be written in the same person as the node prose | per node |
| PR-005 | Prohibited phrases list (Section VIII) applies to all prose and choice labels | per node |

### Project-Specific Craft Rules

<!-- 3–5 rules unique to this game's voice and design, generated by speckit.constitution.
     Examples: dialogue line length cap, bark line format, cutscene tense convention. -->

| Rule ID | Rule | Scope |
|---|---|---|
| PSR-001 | [STORY_SPECIFIC_PRINCIPLES_1] | [per node / per project] |
| PSR-002 | [STORY_SPECIFIC_PRINCIPLES_2] | [per node / per project] |
| PSR-003 | [STORY_SPECIFIC_PRINCIPLES_3] | [per node / per project] |

### Author Rule Overrides

<!-- Document deliberate overrides here with rationale -->

| Rule ID | Override Rationale | Scope |
|---|---|---|
| | | |

---

## IX. Prohibited Phrases

<!-- Phrases that break the voice, betray AI origin, or violate craft rules.
     speckit.checklist and speckit.implement will flag these. -->

| Phrase / Pattern | Reason |
|---|---|
| "Suddenly" | Weak intensifier — let the action speak |
| "You can't help but feel" | Filter phrase — direct address only |
| "As if on cue" | Contrivance marker |
| [ADD PROJECT-SPECIFIC PHRASES] | |

---

## X. Content & Sensitivity Policy

| Category | Level | Notes |
|---|---|---|
| Target audience | [TARGET_AUDIENCE] | adult / new-adult / young-adult / teen / all-ages |
| Violence | [none / mild / moderate / graphic] | |
| Player character death | [permanent / checkpoint / impossible] | |
| Horror content | [none / mild / moderate / extreme] | |
| Sexual content | [none / fade-to-black / explicit] | |
| Reader advisory flags | [NEEDS CLARIFICATION] | |

---

## XI. Tooling

### Search Index (RAG)
<!-- Optional: configure offline semantic search for large projects -->

```yaml
search_index:
  enabled: false
  backend: tf       # tf (zero-dep) | bm25 (pip install rank-bm25) | chromadb (pip install chromadb sentence-transformers)
  index_dir: .specify/index/
```

### Bible Version

| Field | Value |
|---|---|
| Version | 1.0 |
| Ratified | [DATE] |
| Last Updated | [DATE] |
| Updated By | [AUTHOR] |

---

## XII. Series Context
<!-- Populated by speckit.constitution when series_position is not standalone.
     Leave all fields as [TBD] if series-bible.md has not been created yet.
     Validated by speckit.series. -->

| Field | Value |
|---|---|
| Series Title | [SERIES_TITLE] |
| Series Position | [standalone / entry-N] |
| Series Arc Summary | [SERIES_ARC_SUMMARY] |
| Series Tone | [SERIES_TONE] |
| Series Genre | [SERIES_GENRE] |

### Carry-Over Variables
<!-- Variables imported from the previous entry's save state.
     Validated against specs/series-bible.md ## Carry-Over Variable Registry. -->

| Variable | Source Entry | Default (new game+) | Notes |
|---|---|---|---|
| [VAR_NAME] | entry-[N] | [DEFAULT] | |

### Series Variance Log
<!-- Intentional deviations from series-wide defaults (tone, genre, POV, tense).
     Populated by speckit.constitution when a mismatch is detected. -->

| Field | Series Default | This Entry | Reason |
|---|---|---|---|
| | | | |
