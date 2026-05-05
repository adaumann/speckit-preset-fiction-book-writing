# Spec Kit Game Narrative Writing Preset

**Version 1.0.0** · Part of [Spec Kit](https://github.com/adaumann/speckit-preset-fiction-book-writing)

A Spec-Driven Development preset purpose-built for branching narrative game design, this is a pre-production topic in game design. It applies structured software development discipline to interactive fiction, quest design, dialogue trees, and player agency: narrative bibles instead of design docs, node tasks instead of tickets, dialogue branching validation instead of manual testing.

**Key features at a glance:**

- **Constitution governance** — `constitution.md` is the single source of truth for engine targets (SugarCube, Ink, Ren'py), POV architecture, player character voice, narrative mode (linear/branching/emergent), mechanics hooks, and craft rules. Every command reads from it; no inconsistencies across sessions.
- **Full narrative pipeline** — 36 AI commands from first idea (`speckit.specify`) through planning (`speckit.plan`, `speckit.outline`), drafting (`speckit.implement`), quality validation (13 narrative analysis tools), and compilation (`speckit.compile`) to playable output.
- **Dialogue branching system** — Plan dialogue trees with trust states, NPC responses, player choices, and branch targets. Outline dialogue beats with multi-party reactions. Implement prose with mechanic hooks. Validate consequences and choice clarity.
- **13 Narrative Quality Validators** — Player agency (no illusory choices), ending quality, subplot resolution, emotional pacing, foreshadowing/payoff, information asymmetry, state mapping, branch complexity, replayability metrics, choice consequences, accessibility (reading level + content warnings), and secret content discovery.
- **Multi-POV support** — Single protagonist, dual parallel, switching POV, ensemble casts, or rotating perspectives. Trust state tracking per POV. Information asymmetry mapping (what each character knows when).
- **Mechanic hooks (Tier 1)** — Flag, counter, visited, inventory, timer, trust, currency, npc_state, ending_condition, choice_memory, clue. SugarCube and Ink translations included. Extensible Tier 2 schema.
- **Multi-engine compilation** — SugarCube 2.x (Twine), Ink (usable in Unreal, Unity, Godot), with Ren'py, Esconia, AGS support coming. Compiled output in `output/[ENGINE]/`. Automatic theme application (dark/light/minimal CSS for SugarCube; HTML wrappers for Ink).
- **Series Bible support** — Carry-over variable registry, ending canon table, NPC survival tracking, world state deltas per game entry, series arc continuity.
- **Playable themes** — 3 base SugarCube CSS themes (dark, light, minimal) with all values as CSS custom properties for easy tweaking. 3 Ink HTML theme wrappers. All themes exposed via `speckit.theme`.

- **TBI** - For next version Point-And-Click adventure engines and RenPy are planning as export format.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Commands Reference](#commands-reference)
  - [Setup & Planning](#setup--planning)
  - [Outlining & Drafting](#outlining--drafting)
  - [Quality Validation](#quality-validation)
  - [Compilation & Export](#compilation--export)
  - [Series & Reference](#series--reference)
  - [Utilities](#utilities)
- [Templates Reference](#templates-reference)
- [Tutorials](#tutorials)
  - [Single-Protagonist Game](#tutorial-single-protagonist-game)
  - [Multi-POV with Trust States](#tutorial-multi-pov-with-trust-states)
  - [Dialogue Branching Workflow](#tutorial-dialogue-branching-workflow)
  - [Series Management](#tutorial-series-management)
  - [Using All Validation Tools](#tutorial-using-all-validation-tools)
- [Mechanic Hooks Reference](#mechanic-hooks-reference)
- [Engine Compilation](#engine-compilation)
- [Validation Workflow Guide](#validation-workflow-guide)
- [Comparable Products](#comparable-products)
- [Related Resources](#related-resources)

---

## Overview

The Game Narrative Writing preset applies Spec-Driven Development to interactive fiction, quest design, and branching narratives. It provides:

- **36 AI commands** covering every stage from idea to compiled, playable game
- **22 templates** for all supporting game documents
- **1 compilation script** (Python-based) for SugarCube, Ink, and Ren'py output
- Support for **multiple POV architectures** (single, dual, rotating, ensemble)
- Support for **all major game narrative modes** (linear, branching, emergent)
- **13 narrative quality validators** covering player agency, endings, pacing, accessibility, and more
- Two **theme modes**: pre-built (dark/light/minimal) or custom via `speckit.theme`

The central philosophy: the **constitution** (`constitution.md`) is the governing authority. Every drafted node, every choice consequence, every mechanic hook derives its rules from it.

Each specification run (`/speckit.specify`) generates one game narrative project—a 1:1 relationship. Provide detailed specification and plan before implementation.

---

## Prerequisites

This preset requires the following tools installed on your system:

- **[Spec Kit CLI](https://github.com/adaumann/specify)**: The core engine for running commands.
- **Python 3.10+**: Required for compilation and validation scripts.
- **(Optional) Tweego**: Required for SugarCube compilation (`.twee` → `.html`). Download from [Tweego releases](https://www.motoslave.net/tweego/).
- **(Optional) Inklecate**: Required for Ink compilation (`.ink` → `.json`). Install via `npm install -g inkcleate`.

---

## Installation

1. **Install the Spec Kit CLI**:
   ```powershell
   # Windows (PowerShell)
   iwr -useb https://raw.githubusercontent.com/adaumann/specify/main/install.ps1 | iex
   ```

2. **Initialize a new game narrative project with this preset**:
   ```powershell
   mkdir my-interactive-game
   cd my-interactive-game
   specify init --preset game-narrative-writing
   ```

3. **(Optional) Install optional compilers**:
   ```powershell
   # For SugarCube: Download Tweego from https://www.motoslave.net/tweego/
   # Place tweego.exe in PATH or project root
   
   # For Ink: Install inklecate globally
   npm install -g inkcleate
   ```

---

## Quick Start

```bash
# 1. Initialize project with preset (see Installation above)

# 2. Create your game's constitution (engine targets, POV, mechanics, tone)
/speckit.constitution

# 3. Define your game idea as a pitch
/speckit.specify A player discovers their trusted ally was a spy all along. Can they rebuild their agency?

# 4. Clarify ambiguities in the pitch
/speckit.clarify

# 5. Build the story structure (nodes, branches, endings)
/speckit.plan

# 6. Design POV architecture if multi-POV
/speckit.pov draft

# 7. Declare all variables that branches will use
/speckit.variables init

# 8. Define mechanic hooks (trust, flags, inventory, etc.)
/speckit.mechanics init

# 9. Generate node outline files (editable beat sheets)
/speckit.outline all

# 10. Run pre-draft structural audit
/speckit.analyze

# 11. Start drafting nodes (prose + mechanic hooks)
/speckit.implement

# 12. Check prose quality per node
/speckit.checklist

# 13. Run comprehensive validation suite
/speckit.agency                # Player agency validator
/speckit.endings              # Ending quality check
/speckit.consequences         # Choice outcome validator
/speckit.continuity           # Cross-branch consistency
/speckit.pacing               # Word count and beat pacing
/speckit.accessibility        # Reading level + content warnings

# 14. Polish prose
/speckit.polish

# 15. Compile to playable output
/speckit.compile --all-engines

# 16. Done! Play in output/<ENGINE>/story.html
```

---

## Project Structure

After initialization, your project will have this layout:

```
specs/
  constitution.md            † Game Bible (engine targets, POV, mechanics)
  spec.md                    † Pitch and game brief (logline, arcs, endings)
  plan.md                    † Full node graph, branch structure, endings
  variables.md               † Variable registry (state tracking per engine)
  mechanics.md               † Mechanic hook schemas (Tier 1 + Tier 2 stubs)
  endings.md                 † Ending definitions and reachability paths
  world-building.md          † World rules, factions, ambient states
  themes.md                  † Thematic contract, motif registry
  glossary.md                † Consistency reference (terms, capitalization)
  characters/
    index.md                 † NPC roster
    <character>.md           † NPC profile (trust states, dialogue, knowledge)
  relationships.md           † NPC relationship arcs (trust dynamics)
  timeline.md                † In-world chronology (fabula vs syuzhet)
  research.md                † Knowledge gaps and authenticity flags
  subplots.md                † Quest/subplot arc tracking
  series-bible.md            † Series-level canon (carry-over variables)
  foreshadow.md              † Mystery clue registry and payoff tracking
  accessibility-audit.md     † Reading level + content warnings
  consequences-audit.md      † Choice outcome analysis
  secrets-audit.md           † Hidden content and easter egg registry

outlines/
  NODE-001_Opening-outline.md          † Node outline (status: DRAFT/APPROVED/SKIP)
  NODE-010_TrustBreak-outline.md
  NODE-020_Confrontation-outline.md

draft/
  sugarcube/                           † SugarCube-specific drafts
    NODE-001_Opening.twee
    NODE-010_TrustBreak.twee
  ink/                                 † Ink-specific drafts
    NODE-001_Opening.ink
    NODE-010_TrustBreak.ink
  generic/
    NODE-001_Opening.md                † Prose for human reviewers

checklists/
  NODE-001_Opening-checklist.md        † Quality checklist (choice test, hook check, etc.)

tasks/
  NODE-001_Opening-tasks.md
  NODE-010_TrustBreak-tasks.md

themes/
  story.css                            † SugarCube theme (dark/light/minimal)
  ink-theme.html                       † Ink wrapper template

output/
  sugarcube/
    story.html                         † Compiled + playable
  ink/
    story.html                         † Compiled + playable
```

---

## Commands Reference

### Common Arguments

Most commands accept these optional arguments:

| Argument | Commands | Meaning |
|---|---|---|
| `[ITEM_ID]` | Most commands | Target a single item (node, chapter, character). Example: `NODE-001`, `A1.105` |
| `[ITEM_ID] [ITEM_ID]` | Most commands | Target multiple items. Example: `NODE-001 NODE-002 NODE-003` |
| `--all` / `--batch` | Many commands | Process all items of the type (all nodes, all outlines, etc.) |
| `--act [N]` | Outline, Implement, Plan | Process all items in a specific act. Example: `--act 2` |
| `--force` | Implement, Outline, Others | Overwrite existing output (normally skipped) |
| `--pick` | Roleplay | Show picker menu before starting (select which segments to process) |
| `--draft` | Roleplay | Force draft mode (ignore outline if present) |
| `--outline` | Roleplay | Force outline mode (ignore draft if present) |

### Setup & Planning

| Command | Phase | What It Does | Arguments |
|---|---|---|---|
| `speckit.specify` | Concept | Turn a free-text game idea into a structured spec: logline, player goal, NPC arcs, key branches, ending count | Free-text pitch or *(none)* for interactive |
| `speckit.constitution` | Setup | Create or update the game bible: engine targets, POV modes, mechanic hooks, tone, player character voice, craft rules | *(none)* |
| `speckit.clarify` | Concept | Detect and resolve ambiguities in `spec.md` (branch logic gaps, variable contradictions, unreachable endings) | *(none)* |
| `speckit.plan` | Structure | Build the full node graph from `spec.md`: acts, node structure, branch topology, information asymmetry map, endings | *(none)* |
| `speckit.pov` | Structure | Design multi-POV architecture: POV schedule, trust states per character, information asymmetry validation | `draft` \| `review` \| `export` |
| `speckit.variables` | Pre-draft | Initialize `variables.md`: declare all state variables with type, scope, default, export names per engine | `init` \| `audit` |
| `speckit.mechanics` | Pre-draft | Initialize `mechanics.md`: Tier 1 hook schemas (flag, counter, trust, etc.) with engine translations | `init` \| `declare [HOOK_NAME]` \| `promote [HOOK_NAME]` |
| `speckit.tasks` | Pre-draft | Generate node authoring tasks ordered by branch and act: research, outline, draft, quality gate, export phases | `[NODE_ID]` \| `--all` \| `--act [N]` |
| `speckit.outline` | Pre-draft | Generate editable node outline files (beat summary, choices, hooks, variables). Author approves or skips before drafting | `[NODE_ID]` \| `--all` \| `--act [N]` \| `--force` \| `--batch` |
| `speckit.analyze` | Pre-draft | Read-only structural audit: branch coverage, dead ends, unreachable nodes, undeclared variables, ending reachability | *(none)* |

### Outlining & Drafting

| Command | Phase | What It Does | Arguments |
|---|---|---|---|
| `speckit.brainstorm` | Exploration | Interactive brainstorming for any narrative topic: spec, characters, mechanics, endings, world, variables, series | Topic or *(none)* for menu |
| `speckit.implement` | Drafting | Draft node prose from approved outlines, inserting mechanic hook blocks. Gates on APPROVED outline status | `[NODE_ID]` \| `--all` \| `--act [N]` \| `--force` |
| `speckit.research` | Support | Log knowledge gaps, record findings, scan drafts for unsupported claims, view open items ranked by risk | `add` \| `view` \| `scan` |
| `speckit.interview` | Character | Interactive one-on-one conversation with an NPC; export insights as revision notes | `[CHARACTER_ID]` or interactive |

### Quality Validation (13 Tools)

#### Narrative Quality

| Command | Validates | How to Use |
|---|---|---|
| `speckit.agency` | Player agency | Run after all branches drafted: detects illusory choices, forced branches, dead choices. **Workflow**: identifies branches where all paths reconverge → revise to add consequence branching |
| `speckit.endings` | Ending quality | All endings resolve central question, arc closure, character fates clear. **Workflow**: run before export → fix any hollow or unresolved endings |
| `speckit.subplots` | Subplot resolution | Subplots start, develop, resolve. Not abandoned mid-branch. **Workflow**: detects dangling threads → revise or mark as intentional |
| `speckit.tone` | Emotional trajectory | Tone consistency and earned payoff. No tonal whiplash. **Workflow**: flags hollow moments or manipulative tone → adjust beats |
| `speckit.foreshadow` | Clue/payoff balance | Clues placed before revelations. Mysteries feel fair. **Workflow**: detects premature payoffs or orphaned clues → reorder or remove |

#### Player Experience

| Command | Validates | How to Use |
|---|---|---|
| `speckit.consequences` | Choice outcomes | Each choice branches into distinct outcome. No identical consequences. **Workflow**: clarifies which choices matter → strengthens consequence clarity |
| `speckit.pacing` | Beat spacing & reading time | Word count per node, beat pacing, reading time. No info dumps or dead zones. **Workflow**: identifies draggy sections → tighten prose or split into multiple nodes |
| `speckit.replayability` | Unique content per playthrough | Measures content reuse ratio, hidden content tracking. **Workflow**: ensures multiple playthroughs feel fresh |
| `speckit.complexity` | Branch explosion | Warns if exponential growth makes maintenance unsustainable. **Workflow**: recommends convergence points or content reuse |

#### Consistency & Accessibility

| Command | Validates | How to Use |
|---|---|---|
| `speckit.asymmetry` | Information gaps | What player knows vs NPCs know. Player agency via informed decisions. **Workflow**: detects unrealistic NPC knowledge → adjust scene order or add clue nodes |
| `speckit.statemap` | Variable state consistency | Variable state transitions per branch, no dead-end combos, convergence conflicts. **Workflow**: visualizes branch state space → detects unreachable or broken states |
| `speckit.accessibility` | Readability + content warnings | Flesch-Kincaid grade level, sentence length, content warnings, UI contrast (WCAG), ableist language. **Workflow**: ensures game is playable by broad audience → simplify prose or add warnings |
| `speckit.secrets` | Hidden content | Achievements, easter eggs, secret scenes reachable and discoverable. **Workflow**: ensures hidden content is fair challenge, not frustrating |

### Revision & Polish

| Command | Phase | What It Does | Arguments |
|---|---|---|---|
| `speckit.checklist` | Quality | Per-node quality gates: choice meaningfulness test, hook declaration check, dead-end detection, POV drift check | `[NODE_ID]` \\| `--all` \\| `--act [N]` |
| `speckit.revise` | Revision | Surgically rewrite failing passages identified by checklist or continuity. Produces versioned node file | `[NODE_ID]` \\| `--all` |
| `speckit.polish` | Polish | Final line-edit: prose rhythm, sentence variety, word repetition, filter words, adverb density, voice consistency | `[NODE_ID]` \\| `--all` \\| `--aggressive` |
| `speckit.continuity` | Post-draft | Cross-branch audit: variable consistency, POV drift, NPC knowledge state, series bible validation | *(none)* |
| `speckit.feedback` | Revision | Ingest playtest notes, categorize by issue type (Branch/Variable/Pacing), generate prioritized revision tasks | `upload [FILE]` \\| `view` |

### Compilation & Export

| Command | Phase | What It Does | Arguments |
|---|---|---|---|
| `speckit.compile` | Build | Compile all nodes to engine-specific output (SugarCube, Ink, Ren'py). Includes theme, variables, and hook translation. Output in `output/[ENGINE]/` | `--all-engines` \| `[ENGINE]` (sugarcube/ink/renpy/generic) |
| `speckit.verify` | QA | Optional: Run comprehensive unit test suite on all nodes (structural tests, hook validation, self-correction). Use for deep audits | `--all-engines` \| `[ENGINE]` \| `--unit-tests` \| `--structural-only` |
| `speckit.theme` | Styling | Generate or adjust story.css (SugarCube) or ink-theme.html wrapper. Dark/light/minimal base themes or custom via flags | `dark` \| `light` \| `minimal` \| `custom [FILE]` |
| `speckit.export` | Distribution | Export final game to platform-specific formats (coming: web deployment, itch.io packaging) | `web` \| `itch` (coming soon) |

### Series & Reference

| Command | Phase | What It Does | Arguments |
|---|---|---|---|
| `speckit.series` | Multi-game | Manage series bible: carry-over variables, ending canon, NPC survival tracking, world state deltas, cross-game continuity | `init` \| `add [GAME_ID]` \| `view` \| `validate` |
| `speckit.glossary` | Consistency | Add invented terms, check drafts for glossary violations, audit unregistered terms | `add [TERM]` \| `check` \| `audit` \| `view` |
| `speckit.help` | Navigation | Workflow advisor: scans project state, identifies blockers, recommends next action based on phase | *(none)* |
| `speckit.status` | Monitoring | Project dashboard: node count by status, branch coverage %, variable completeness, endings reachable vs declared | *(none)* |
| `speckit.flowmap` | Visualization | Generate Mermaid flowchart of full node graph with ending markers, act boundaries, mechanic annotations | `[format]` (mermaid/svg/ascii) |

### Utilities

| Command | What It Does | Arguments |
|---|---|---|
| `speckit.mechanics` | Manage mechanic hook schemas: define Tier 2 stubs, promote to Tier 1 with translations, audit hook usage | `declare [HOOK_NAME]` \| `promote [HOOK_NAME]` \| `audit` |
| `speckit.research` | Research tracking: log gaps, record findings, scan drafts, view open items ranked by risk | `add [TOPIC]` \| `view` \| `scan` |
| `speckit.statistics` | Optional: Prose statistics (sentence length, passive voice %, adverb density, dialogue balance) | `[NODE_ID]` \| `--all` |

---

## Direct Python Script Usage

The preset includes Python scripts for compilation and validation. Call them directly if not using the Spec Kit CLI:

### Compilation

**`scripts/python/compile.py`** — Compile drafted nodes to engine-specific output (HTML for SugarCube, JSON+HTML for Ink, etc.)

```bash
# Compile a single engine
python scripts/python/compile.py --spec <spec-name> --engine sugarcube
python scripts/python/compile.py --spec <spec-name> --engine ink
python scripts/python/compile.py --spec <spec-name> --engine renpy

# Compile all configured engines (reads export_engines from constitution.md or spec.yml)
python scripts/python/compile.py --spec <spec-name> --all-engines

# Optional: specify custom output directory
python scripts/python/compile.py --spec <spec-name> --engine sugarcube --output custom/output/path

# Optional: force full rebuild (don't skip if output exists)
python scripts/python/compile.py --spec <spec-name> --engine sugarcube --force-rebuild

# Optional: validate without writing files (dry-run mode)
python scripts/python/compile.py --spec <spec-name> --engine sugarcube --dry-run
```

**Arguments:**
- `--spec` (**required**) — Spec name or path. Accepts both `test-tier-mechanics` and `specs/test-tier-mechanics`
- `--engine` (**required unless `--all-engines`**) — Target engine: `sugarcube`, `ink`, `renpy`, or `generic`
- `--all-engines` (**alternative to `--engine`**) — Compile all engines configured in `constitution.md`
- `--output` — Custom output directory (default: `specs/<spec>/output/<engine>/`)
- `--force-rebuild` — Regenerate output even if it already exists
- `--dry-run` — Validate structure without writing files

**Output:** Playable HTML file in `specs/<spec>/output/<ENGINE>/story.html`

---

### Verification & Validation

**`scripts/python/verify.py`** — Run comprehensive unit tests on drafted nodes (optional; `compile.py` includes basic validation automatically)

```bash
# Verify a single engine with all tests
python scripts/python/verify.py --spec <spec-name> --engine sugarcube

# Verify all configured engines
python scripts/python/verify.py --spec <spec-name> --all-engines

# Run only structural tests (skip engine compilation)
python scripts/python/verify.py --spec <spec-name> --engine sugarcube --structural-only

# Run optional unit test suite (in addition to structural tests)
python scripts/python/verify.py --spec <spec-name> --engine sugarcube --unit-tests

# Set max retry attempts for auto-correction
python scripts/python/verify.py --spec <spec-name> --engine sugarcube --max-attempts 5
```

**Arguments:**
- `--spec` (**required**) — Spec name or path
- `--engine` (**required unless `--all-engines`**) — Target engine: `sugarcube`, `ink`, `renpy`
- `--all-engines` (**alternative to `--engine`**) — Verify all configured engines
- `--all` — Verify all nodes in all engines
- `--structural-only` — Run only YAML and syntax validation (skip engine compilation)
- `--unit-tests` — Include optional advanced unit test suite
- `--max-attempts` — Max retry attempts for auto-fix logic (default: 3)

**Output:** Validation report with issues, warnings, and auto-fix attempts. Exit code 0 = all pass, 1 = failures.

---

### Direct Structural Testing

**`scripts/python/validation/test_nodes.py`** — Low-level structural validation of node files

```bash
# Test nodes in a specific directory
python scripts/python/validation/test_nodes.py --nodes-dir specs/<spec-name>/draft/sugarcube

# Test nodes and validate against variables.md
python scripts/python/validation/test_nodes.py --nodes-dir specs/<spec-name>/draft/sugarcube --specs-dir specs/<spec-name>

# Target a specific engine for variable export name checking
python scripts/python/validation/test_nodes.py --nodes-dir specs/<spec-name>/draft/sugarcube --target sugarcube
```

**Arguments:**
- `--nodes-dir` — Directory containing drafted node files (`.twee`, `.ink`, `.rpy`, `.md`)
- `--specs-dir` — Directory containing supporting documents like `variables.md`
- `--target` — Engine name for export variable validation

**Checks:**
- YAML frontmatter structure (node_id, title, status, etc.)
- Variable declarations in `variables.md`
- Choice syntax and node references
- Mechanic hook syntax
- Dead-end detection

---

## Templates Reference

### Game Documents

| Template | Purpose |
|---|---|
| `constitution-template.md` | Game Bible: engine targets, POV, mechanics, craft rules, player voice |
| `spec-template.md` | Game Brief: logline, pitch, player arc, NPC arcs, key relationships, endings map |
| `plan-template.md` | Story Plan: node graph in text form, act structure, information asymmetry map, pacing overview |
| `variables-template.md` | Variable Registry: all declared variables with type, scope, default, export names per engine |
| `mechanics-template.md` | Hook Schemas: Tier 1 definitions (flag, counter, trust, etc.) with SugarCube/Ink translations |
| `endings-template.md` | Endings Registry: ending ID, name, condition, paths to reach, narrative closure check |

### Narrative Documents

| Template | Purpose |
|---|---|
| `spec-template.md` | Story Brief: logline, premise, player arc, NPC arcs, key scenes, opening/climax/ending, design requirements |
| `characters-template.md` | NPC Profile: trust states, dialogue register per state, branch behavior, knowledge state, first/last appearance |
| `world-building-template.md` | World Reference: locations with object inventory, state log, world rules, factions |
| `relationships-template.md` | NPC Relationship Arcs: trust state dynamics, repeating loop, 5 key beats with node references |
| `timeline-template.md` | Chronology: fabula (event order), syuzhet (player discovery), branching consequences, timer events |
| `research-template.md` | Research Log: knowledge gaps, findings, open items ranked by authenticity risk |
| `glossary-template.md` | Consistency Log: invented terms, proper nouns, capitalization rules, variable name register |
| `themes-template.md` | Thematic Contract: central theme, dramatic question, motif registry, ending thematic divergence |
| `subplots-template.md` | Quest/Subplot Registry: subplot ID, start node, 5 beat nodes, resolution node, status |
| `foreshadow-template.md` | Mystery Registry: mystery ID, clue placement nodes, payoff node, accessibility check |
| `checklist-template.md` | Node Quality Checklist: choice meaningfulness, hook declaration, dead-end check, POV consistency |

### Output & Compilation

| Template | Purpose |
|---|---|
| `implement-template.md` | Node Draft: prose body, mechanic hook blocks (MECHANIC:TYPE), choices with targets, variables read/set |
| `node-outline-template.md` | Node Outline: beat summary, choice list with targets, hooks, variables. Status gate (DRAFT/APPROVED/SKIP) |
| `sugarcube-theme-dark.css` | SugarCube Dark Theme: charcoal bg, purple accent, serif prose, CSS custom properties |
| `sugarcube-theme-light.css` | SugarCube Light Theme: warm off-white bg, blue links, serif prose, CSS custom properties |
| `sugarcube-theme-minimal.css` | SugarCube Minimal Theme: white page, invisible UI, pure prose focus |
| `ink-theme-dark.html` | Ink Dark Wrapper: HTML template for {title} and {story_json} placeholder injection |
| `ink-theme-light.html` | Ink Light Wrapper: HTML template for clean, readable Ink output |
| `ink-theme-minimal.html` | Ink Minimal Wrapper: HTML template with minimal UI for literary IF |

---

## Tutorials

### Tutorial: Single-Protagonist Game

**Scenario**: A hacker must break into a corporate vault. Single POV. Linear with 2 branch points (stealth vs. aggressive), converging at finale.

#### Step 1: Constitution

```bash
/speckit.constitution
```

When prompted:
- **Engine targets**: SugarCube (primary), Ink (secondary)
- **POV Mode**: Single protagonist (hacker)
- **Tone**: Cyberpunk noir, tense, morally ambiguous
- **Narrative Mode**: Branching (2 paths, reconverge at ending)

Result: `specs/constitution.md` contains engine config, craft rules, POV rules.

#### Step 2: Pitch & Plan

```bash
/speckit.specify A corporate hacker breaks into a vault to expose corporate crime. Can they escape without getting caught? Or do they sacrifice themselves?

/speckit.clarify

/speckit.plan
```

Results:
- `specs/spec.md`: Logline, 2 main branches (stealth/aggressive), 1 shared ending
- `specs/plan.md`: NODE-001 (Start) → NODE-010 (Stealth choice) / NODE-011 (Aggressive choice) → NODE-020 (Finale, shared)
- `specs/variables.md`: `heat_level` (0–100), `evidence_secured` (boolean), `npc_alerted` (boolean)

#### Step 3: Declare Variables

`specs/variables.md` auto-generated by `speckit.plan`, but review:

```yaml
Variables:
  heat_level:
    type: integer
    default: 0
    scope: global
    export_sugarcube: heat
    export_ink: heat
    notes: "Increases with aggressive actions. >75 = guard alert"
  
  evidence_secured:
    type: boolean
    default: false
    scope: global
    export_sugarcube: evidence
    export_ink: evidence
    notes: "Set to true when NODE-015 (Find safe) executed"
  
  npc_alerted:
    type: boolean
    default: false
    scope: global
    export_sugarcube: npc_alerted
    export_ink: npc_alerted
    notes: "Set to true if heat_level > 50 at NODE-012"
```

#### Step 4: Define Mechanics

```bash
/speckit.mechanics
```

When prompted, define Tier 1 hooks used in your game:

```yaml
Tier 1 Hooks:
  flag:
    Description: "Boolean state (true/false)"
    Sugarcube: "<<set $flag_name to true>>"
    Ink: "~ flag_name = true"
  
  counter:
    Description: "Numeric state (increment/decrement)"
    Sugarcube: "<<set $heat_level += 15>>"
    Ink: "~ heat_level += 15"
  
  trust:
    Description: "NPC relationship value (0–100)"
    Sugarcube: "<<set $npc_trust to 50>>"
    Ink: "~ npc_trust = 50"
```

#### Step 5: Generate Outlines

```bash
/speckit.outline all
```

Results: `outlines/NODE-001_Start-outline.md`, `NODE-010_Stealth-outline.md`, etc.

Author reviews and approves. If outline needs work, set `status: DRAFT`. If ready, set `status: APPROVED`.

Example outline:

```markdown
---
node_id: NODE-010
title: "Stealth Approach"
status: APPROVED
choices:
  - label: "Disable alarm panel"
    target: NODE-015
    consequence: "evidence_secured = true; heat_level += 10"
---

# NODE-010: Stealth Approach

## Beat Summary
Hacker bypasses guards silently, finds vault room. Guards patrol in predictable pattern. If alarm triggers, heat_level spikes.

## Choices
1. Disable alarm panel (NODE-015) — silent but risky
2. Wait for guard shift change (NODE-014) — safe but time-consuming

## Mechanic Hooks
- MECHANIC:trust — guard_alerted = false
- MECHANIC:counter — heat_level (currently 25)

## Variables Read
- heat_level
- evidence_secured

## Variables Set
- heat_level (may increment)
- npc_alerted (if heat > 50)
```

#### Step 6: Draft Nodes

```bash
/speckit.implement
```

This drafts all APPROVED outlines in order. AI generates prose for:
- NODE-001 (Start)
- NODE-010 (Stealth choice)
- NODE-011 (Aggressive choice)
- NODE-020 (Finale)

Example generated NODE-010 prose:

```markdown
---
node_id: NODE-010
engine: sugarcube
status: DRAFT
choices:
  - label: "Disable alarm panel"
    target: NODE-015
    consequence: "heat_level += 10"
---

# NODE-010: Stealth Approach

The ventilation shaft opens into a narrow corridor. Red security cameras sweep the hallway every 3 seconds. You count the pattern: sweep, pause, sweep. Your heart hammers.

MECHANIC:counter:heat_level = 25
MECHANIC:flag:guard_alerted = false

The alarm panel is 20 meters ahead, mounted on the wall beside the vault room door. Two guards patrol this sector. They're checking their phones—distracted, sloppy, predictable.

You have a window.

[[Disable the alarm (silent, risky)|NODE-015]]
[[Wait for the guard shift change (safe, slow)|NODE-014]]
```

#### Step 7: Quality Check

```bash
/speckit.checklist
/speckit.continuity
/speckit.agency
/speckit.consequences
```

**speckit.checklist** per node:
- ✅ Choice meaningfulness: Both paths have distinct consequences? Yes (stealth += 10 heat vs wait costs 5 turns)
- ✅ Hook declaration: All `MECHANIC:` blocks declared? Yes
- ✅ Dead-end check: Both branches reconverge? Yes (NODE-020)

**speckit.continuity**:
- ✅ Variable consistency: heat_level only modified in branching paths? Yes
- ✅ NPC state: guard_alerted consistent across branches? Yes

**speckit.agency**:
- ✅ Forced branches: Both paths reach the ending? Yes
- ✅ Cosmetic choices: Do choices have real consequences? Yes (heat_level += 10 vs wait = different npc_alerted state at finale)

**speckit.consequences**:
- ✅ Choice outcomes distinct? Yes (stealth = quick but dangerous; wait = slow but safe)

#### Step 8: Polish

```bash
/speckit.polish
```

Adjusts prose rhythm, removes filter words, ensures hacker voice consistent throughout.

#### Step 9: Compile

```bash
/speckit.compile --all-engines
```

Results:
- `output/sugarcube/story.html` — Playable in browser via SugarCube
- `output/ink/story.html` — Playable in browser via Ink

**Play the game!** Test both branches. Verify endings make sense.

---

### Tutorial: Multi-POV with Trust States

**Scenario**: 2 protagonists (Hacker + Insider). Their trust in each other affects dialogue and available choices. Game tracks `hacker_trusts_insider` (0–100) and `insider_trusts_hacker` (0–100).

#### Step 1: Constitution

```bash
/speckit.constitution
```

When prompted:
- **POV Mode**: Dual (alternating between Hacker and Insider)
- **Variables**: Add `hacker_trusts_insider` and `insider_trusts_hacker`
- **NPC States**: Track trust levels in dialogue

#### Step 2: Multi-POV Outline

```bash
/speckit.pov draft
```

This generates `specs/pov-structure.md`:

```yaml
POV Schedule:
  ACT I:
    NODE-001: Hacker POV (Decide whether to call Insider)
    NODE-002: Insider POV (Receive mysterious call, decide to help)
  
  ACT II:
    NODE-010: Hacker POV (Stealth phase, doubts Insider's loyalty)
    NODE-011: Insider POV (Watches security feeds, notices heat rising)
  
  ACT III:
    NODE-020: Shared POV (Confrontation: "Did you betray me?")

Trust State Thresholds:
  insider_trusts_hacker:
    0–30: Suspicious, withholding info
    31–70: Cooperative, helpful
    71–100: Loyal, self-sacrificing

  hacker_trusts_insider:
    0–30: Paranoid, questions motives
    31–70: Trusting, shares plans
    71–100: Dependent, vulnerable
```

#### Step 3: Dialogue Trees with Trust

When drafting NODE-002 (Insider receives call):

```markdown
---
node_id: NODE-002
pov: insider
dialogue_tree:
  - speaker: Hacker
    text: "I need your help breaking into the vault."
  
  - speaker: Insider
    text: |
      [if insider_trusts_hacker < 30]
        "Why should I risk my job for you?"
      [if insider_trusts_hacker 31-70]
        "Okay. What do you need?"
      [if insider_trusts_hacker > 70]
        "I'd do anything for you. I'm in."
    
    reactions:
      - npc: Hacker
        trust_change: -5 if chosen first, +10 if chosen last
  
  - player_choices:
    - label: "I'll pay you 50,000."
      target: NODE-005
      consequence: "insider_trusts_hacker += 15; hacker_trusts_insider -= 10"
    
    - label: "This is about exposing their crimes."
      target: NODE-005
      consequence: "insider_trusts_hacker += 30; hacker_trusts_insider += 10"
    
    - label: "I can't tell you why."
      target: NODE-005
      consequence: "insider_trusts_hacker -= 20; hacker_trusts_insider -= 15"
---

# NODE-002: Insider's Call

Your phone buzzes at 2 AM. Unknown number. You almost don't answer.

"It's me," the voice says. Your old friend from college. The hacker. You haven't heard from them in 5 years.

"I need your help breaking into the vault."

Your stomach tightens. This is insane. This is also the moment you've been waiting for.

MECHANIC:trust:insider_trusts_hacker (current: 50)
MECHANIC:trust:hacker_trusts_insider (current: 50)

What do you say?

[[offer money|NODE-005]] (-10 hacker_trust, +15 insider_trust)
[[appeal to justice|NODE-005]] (+10 hacker_trust, +30 insider_trust)
[[stay mysterious|NODE-005]] (-15 hacker_trust, -20 insider_trust)
```

#### Step 4: Validate Multi-POV Consistency

```bash
/speckit.asymmetry
```

Checks:
- Does Hacker POV reveal info Insider shouldn't know at that point? ❌ Flag if yes
- Does Insider's dialogue match their trust state? ✅ Yes
- Is information asymmetry realistic? ✅ Yes (Insider on cameras, Hacker on ground)

#### Step 5: Validate Trust Arc

```bash
/speckit.continuity --validate-trust-states
```

Checks:
- Do both trust values stay in 0–100 range? ✅ Yes
- Is there a path where trust plummets to 0 and they never reconcile? ⚠️ Flag if ending becomes unreachable
- Is final trust state narratively satisfying? Check manually in ending node

#### Step 6: Compile & Test

```bash
/speckit.compile --all-engines
```

Play through once trusting Insider (all +trust choices) and once distrusting them (all -trust choices). Verify dialogue and ending branch correctly.

---

### Tutorial: Dialogue Branching Workflow

**This tutorial demonstrates the complete dialogue branching workflow: Planning → Outlining → Implementation → Validation**

#### Phase 1: Plan Dialogue Tree

In `specs/plan.md`, sketch the dialogue structure:

```yaml
NODE-015: Confrontation with Guard

Dialogue Tree:
  - Guard: "What are you doing here?"
    
    Player choices:
      1. Lie ("I'm authorized maintenance")
         - If lie_success: NODE-020 (sneak past)
         - If lie_fails: NODE-025 (combat)
      
      2. Intimidate ("Back off")
         - If courage > 50: NODE-020 (guard retreats)
         - If courage <= 50: NODE-025 (combat)
      
      3. Charm ("Can we talk about this?")
         - If charisma > 70: NODE-030 (guard becomes ally)
         - If charisma 40-70: NODE-025 (combat)
         - If charisma < 40: NODE-022 (guard calls reinforcements)
```

#### Phase 2: Outline with Dialogue Tree

```bash
/speckit.outline NODE-015
```

Edit `outlines/NODE-015_Confrontation-outline.md`:

```markdown
---
node_id: NODE-015
title: "Confrontation with Guard"
status: APPROVED
dialogue_tree:
  npc: Guard
  trust_states:
    suspicious:
      dialogue: "What are you doing here? Identify yourself."
    neutral:
      dialogue: "I haven't seen you here before. Where's your badge?"
    cooperative:
      dialogue: "You shouldn't be here. But I can look the other way for 500 credits."

player_choices:
  - label: "Lie: I'm authorized maintenance"
    condition: "courage > 40 OR deception_skill > 50"
    success_target: NODE-020
    failure_target: NODE-025
    consequence: "if success: reputation -= 5; if fail: combat initiated"
  
  - label: "Intimidate the guard"
    condition: "courage > 60 OR strength > 70"
    success_target: NODE-020
    failure_target: NODE-025
    consequence: "if success: reputation -= 10; alarm system triggered"
  
  - label: "Charm: Let's talk about this"
    condition: "charisma > 50"
    success_target: NODE-030
    failure_target: NODE-022
    consequence: "if success: guard becomes ally; if fail: reinforcements called"
---

# NODE-015: Confrontation with Guard

## Beat Summary
Player encounters guard on patrol. Must convince them to allow passage. 3 dialogue paths with variable-gated success conditions.

## NPC: Guard
- Trust Level: [neutral] (default: 50)
- Dialogue Register: Professional, suspicious, bribeable
- Motivation: Protect vault, don't lose job

## Dialogue Options
1. Lie about authorization (DC: Deception 50)
2. Intimidate (DC: Courage 60)
3. Charm/Negotiate (DC: Charisma 50)

## Mechanic Hooks
- MECHANIC:trust guard_trust (0–100)
- MECHANIC:flag alarm_triggered
- MECHANIC:counter reputation

## Variables Read
- courage, deception_skill, charisma
- guard_trust
- reputation

## Variables Set
- guard_trust (modified by choice)
- alarm_triggered (if intimidate fails)
- reputation (modified by success/fail)
```

#### Phase 3: Implement Dialogue

```bash
/speckit.implement NODE-015
```

AI generates prose + dialogue:

```markdown
---
node_id: NODE-015
engine: sugarcube
status: DRAFT
variables_read:
  - courage
  - deception_skill
  - charisma
  - guard_trust
  - reputation
variables_set:
  - guard_trust
  - alarm_triggered
  - reputation
mechanic_hooks:
  - MECHANIC:trust:guard_trust = 50
  - MECHANIC:flag:alarm_triggered = false
---

# NODE-015: Confrontation with Guard

You turn the corner and freeze. A guard stands 10 meters ahead, hand resting on a plasma rifle. Their eyes snap to you.

"Hey. You. What are you doing in this sector?"

Your heart hammers. The guard's expression shifts: suspicious, calculating. They haven't drawn yet. That's something.

MECHANIC:trust:guard_trust (current: 50)

**What do you do?**

[if deception_skill > 50 OR courage > 40]
[[Lie: "I'm authorized maintenance. Forgot my badge."|NODE-020-lie]] (Deception check)

[if courage > 60 OR strength > 70]
[[Intimidate: "Back off or you're making a mistake."|NODE-020-intimidate]] (Courage check)

[if charisma > 50]
[[Charm: "Look, we both know why I'm here. What would it take to let me through?"|NODE-030-charm]] (Charisma check)

[if deception_skill <= 40 AND courage <= 40 AND charisma <= 50]
[[Surrender and comply|NODE-025-arrested]] (No good options)
```

#### Phase 4: Validate Dialogue Consequences

```bash
/speckit.consequences NODE-015
```

Output:

```
NODE-015 Choice Consequence Map:

Choice 1: Lie (DC: Deception 50)
  ✅ Success path: NODE-020-lie (guard lets you pass)
  ✅ Failure path: NODE-025 (combat initiated)
  ✅ Outcome distinct from others? YES (non-violent)

Choice 2: Intimidate (DC: Courage 60)
  ✅ Success path: NODE-020-intimidate (guard retreats)
  ✅ Failure path: NODE-025 (combat initiated)
  ⚠️ Outcome identical to lie failure — might be redundant
  → SUGGESTION: Add alarm_triggered flag to differentiate

Choice 3: Charm (DC: Charisma 50)
  ✅ Success path: NODE-030-charm (guard becomes ally)
  ✅ Failure path: NODE-022 (reinforcements called)
  ✅ Outcome distinct? YES (ally status)

Overall Agency: 7/10
  - 3 meaningful choices
  - Variable-gated (skill checks)
  - Distinct outcomes
  - Consider: Add 4th option (sneak past) for less social players
```

#### Phase 5: Validate Player Agency

```bash
/speckit.agency
```

Checks:
- Are all choices available to all players? (No — gated by skills) ✅
- Do choices lead to different outcomes? (Yes) ✅
- Can player fail/succeed? (Yes — DC checks) ✅
- Is there a path for low-skill players? (Sneak past as fallback) ✅

---

### Tutorial: Series Management

**Scenario**: 3-game series. Game 1 ending affects Game 2 NPCs and world state. Game 2 ending carries over to Game 3.

#### Step 1: Create Series Bible

```bash
/speckit.series init
```

Generates `specs/series-bible.md`:

```yaml
Series: "Corporate Heist Trilogy"
Entries:
  1: "Game 1: The Vault"
  2: "Game 2: The Network"
  3: "Game 3: The Reckoning"

Carry-Over Variables:
  evidence_secured:
    Type: boolean
    Usage: "If true in Game 1 → Game 2 starts with media exposure"
  
  npc_alive:
    Type: list (NPC names)
    Usage: "Which NPCs survived Game 1 → alive/dead status in Game 2"
  
  corporate_heat:
    Type: counter (0–100)
    Usage: "Carries from Game 1 → Game 2 starting heat level"

Ending Canon:
  Ending A (Corporate Exposure):
    evidence_secured: true
    npc_alive: [Insider, Hacker]
    corporate_heat: 80
    Game 2 starting state: Public scandal, corporation in chaos
  
  Ending B (Silent Success):
    evidence_secured: false
    npc_alive: [Hacker]
    corporate_heat: 30
    Game 2 starting state: Insider disappeared, corporation suspicious but confident
  
  Ending C (Everyone Dies):
    evidence_secured: false
    npc_alive: []
    corporate_heat: 100
    Game 2 starting state: Hacker & Insider dead, corporation triumphant
    → Game 2 cannot be played (canon incompatible)
```

#### Step 2: Define Carry-Over in Game 1

In Game 1 `specs/variables.md`, mark variables as carry-over:

```yaml
evidence_secured:
  type: boolean
  scope: global
  carry_over: true
  series_use: "Game 2: determines media scandal intensity"

npc_alive:
  type: list
  scope: global
  carry_over: true
  series_use: "Game 2: determines NPC availability"
```

#### Step 3: Import Game 1 Save into Game 2

In Game 2 `specs/constitution.md`:

```yaml
Series:
  entry: 2
  import_from: game1
  
  import_state:
    evidence_secured: [from game 1 ending]
    npc_alive: [from game 1 ending]
    corporate_heat: [from game 1 ending]

Series Variables:
  # Game 2 branches based on Game 1 state
  starting_heat:
    [if evidence_secured == true]: 80
    [if evidence_secured == false]: 30
  
  insider_available:
    [if "Insider" in npc_alive]: true
    [else]: false
```

#### Step 4: Validate Series Continuity

```bash
/speckit.series update
/speckit.continuity --series
```

Checks:
- Game 1 carry-over variables exported correctly? ✅
- Game 2 import state matches Game 1 ending? ✅
- Game 2 nodes reference only available NPCs? (Warn if Insider referenced but not in npc_alive) ✅
- Game 3 can be played from all Game 2 endings? (Warn if Game 2 Ending X leaves Game 3 unreachable) ⚠️

#### Step 5: Test Series Playthrough

1. Play Game 1 → Ending A (evidence_secured: true)
2. Export Game 1 save state
3. Import into Game 2
4. Play Game 2 with scandal twist → Ending B
5. Import into Game 3
6. Play Game 3 with Game 2 setup

Verify narrative continuity at each handoff.

---

### Tutorial: Using All Validation Tools

**This walks through using all 13 narrative quality validators in sequence**

After drafting all nodes, run validation suite in order:

#### 1. Structural Validation (Pre-Quality)

```bash
/speckit.analyze
```

Checks:
- ✅ All planned nodes drafted?
- ✅ All endings reachable?
- ✅ No undeclared variables?
- ✅ No orphaned branches?

**If failures**: Fix and re-draft before continuing.

#### 2. Player Agency Validation

```bash
/speckit.agency
```

Checks:
- ✅ Are choices real or illusory?
- ✅ Do both branches in a fork lead to different outcomes?
- ✅ Can player fail a challenge?

**Output**: `specs/agency-audit.md`
**If issues**: Revise choices to add consequence branching.

```bash
/speckit.revise --fix-agency
```

#### 3. Ending Quality Validation

```bash
/speckit.endings
```

Checks:
- ✅ Each ending resolves central dramatic question?
- ✅ Character arcs closed?
- ✅ Stakeholder fates clear?

**If issues**: Revise ending nodes for closure.

#### 4. Subplot Resolution

```bash
/speckit.subplots
```

Checks:
- ✅ Subplots started, developed, resolved?
- ✅ No dangling threads?
- ✅ Resolution satisfying?

**If issues**: Add resolution nodes or mark as intentional cliffhanger.

#### 5. Emotional Trajectory

```bash
/speckit.tone
```

Checks:
- ✅ Tone shifts earned (not whiplash)?
- ✅ No hollow emotional moments?
- ✅ Alignment with theme?

**If issues**: Adjust beats to build emotional context.

#### 6. Foreshadowing & Payoff

```bash
/speckit.foreshadow
```

Checks:
- ✅ Clues placed before revelations?
- ✅ Mysteries feel fair (not random)?
- ✅ Premature payoffs avoided?

**If issues**: Reorder clue placement or add subtle hints.

#### 7. Choice Consequences

```bash
/speckit.consequences
```

Checks:
- ✅ Each choice leads to distinct outcome?
- ✅ Consequences clear and immediate?
- ✅ No identical branches?

**If issues**: Differentiate branch outcomes via variables or prose.

#### 8. Pacing & Reading Time

```bash
/speckit.pacing
```

Checks:
- ✅ No node >1000 words (info dump)?
- ✅ Beat spacing consistent?
- ✅ Reading time reasonable per branch?

**Output**: `specs/pacing-audit.md` with word count per node
**If issues**: Split long nodes or tighten prose.

#### 9. Information Asymmetry

```bash
/speckit.asymmetry
```

Checks:
- ✅ Does player know what's needed to make informed choice?
- ✅ Do NPCs know things they shouldn't?
- ✅ Is information gap realistic?

**If issues**: Adjust scene order or add exposition nodes.

#### 10. State Mapping

```bash
/speckit.statemap
```

Checks:
- ✅ No unreachable variable combinations?
- ✅ No dead-end states?
- ✅ Branch convergence conflicts?

**Output**: State space graph
**If issues**: Adjust variable transitions to avoid dead-ends.

#### 11. Complexity Analysis

```bash
/speckit.complexity
```

Checks:
- ✅ Branch explosion warning?
- ✅ Exponential growth manageable?
- ✅ Maintenance effort sustainable?

**If issues**: Add convergence points or reuse content.

#### 12. Replayability

```bash
/speckit.replayability
```

Checks:
- ✅ How much unique content per playthrough?
- ✅ Content reuse ratio?
- ✅ Hidden content tracking?

**If issues**: Add more branch-unique content or secret scenes.

#### 13. Accessibility

```bash
/speckit.accessibility
```

Checks:
- ✅ Reading level appropriate (grade 8–10)?
- ✅ Content warnings needed?
- ✅ UI contrast WCAG compliant?
- ✅ No ableist language?

**Output**: `specs/accessibility-audit.md`
**If issues**: Simplify prose, add warnings, fix contrast.

#### Post-Validation

After all validators pass:

```bash
/speckit.secrets                    # Map hidden content
/speckit.continuity                 # Final cross-branch check
/speckit.polish                     # Line-edit
/speckit.compile --all-engines      # Build
```

---

## Mechanic Hooks Reference

### Tier 1 Hooks (Built-In)

| Hook | Purpose | Example |
|---|---|---|
| `MECHANIC:flag` | Boolean state (true/false) | `MECHANIC:flag:evidence_secured = true` |
| `MECHANIC:counter` | Numeric state (increment/decrement) | `MECHANIC:counter:heat_level += 15` |
| `MECHANIC:visited` | Tracks if node was visited | `MECHANIC:visited:safe_house = true` |
| `MECHANIC:inventory` | Track player items | `MECHANIC:inventory:add keycard` / `MECHANIC:inventory:remove keycard` |
| `MECHANIC:timer` | Countdown/timer state | `MECHANIC:timer:escape_window (60 seconds)` |
| `MECHANIC:trust` | NPC relationship (0–100) | `MECHANIC:trust:insider_trusts_hacker += 20` |
| `MECHANIC:currency` | Resource tracking | `MECHANIC:currency:credits -= 5000` |
| `MECHANIC:npc_state` | NPC mood/status | `MECHANIC:npc_state:insider_mood = "panicked"` |
| `MECHANIC:ending_condition` | Check if ending unlocked | `MECHANIC:ending_condition:evidence_secured AND insider_alive` |
| `MECHANIC:choice_memory` | Remember player choice | `MECHANIC:choice_memory:player_chose_stealth = true` |
| `MECHANIC:clue` | Track discovered clues | `MECHANIC:clue:vault_location_discovered = true` |

### Syntax

**In node prose:**

```markdown
---
node_id: NODE-010
mechanic_hooks:
  - MECHANIC:counter:heat_level += 15
  - MECHANIC:flag:alarm_triggered = true
  - MECHANIC:trust:insider_trusts_hacker -= 10
---

Your aggressive approach triggers the alarm system.

MECHANIC:counter:heat_level = 50 (was 35)
MECHANIC:flag:alarm_triggered = true
MECHANIC:trust:insider_trusts_hacker = 40 (was 50, -10 for recklessness)

The guards converge from all sides...

[[Run for the exit|NODE-020]]
[[Fight your way through|NODE-025]]
```

### SugarCube Translation

```javascript
// speckit.compile auto-translates MECHANIC: blocks to SugarCube

MECHANIC:counter:heat_level += 15
  ↓
<<set $heat_level += 15>>

MECHANIC:trust:insider_trusts_hacker -= 10
  ↓
<<set $insider_trusts_hacker -= 10>>

MECHANIC:flag:alarm_triggered = true
  ↓
<<set $alarm_triggered = true>>

MECHANIC:inventory:add keycard
  ↓
<<run $inventory.push('keycard')>>
```

### Ink Translation

```ink
// speckit.compile auto-translates MECHANIC: blocks to Ink

MECHANIC:counter:heat_level += 15
  ↓
~ heat_level += 15

MECHANIC:trust:insider_trusts_hacker -= 10
  ↓
~ insider_trusts_hacker -= 10

MECHANIC:flag:alarm_triggered = true
  ↓
~ alarm_triggered = true

MECHANIC:inventory:add keycard
  ↓
~ inventory.push('keycard')
```

---

## Engine Compilation

### SugarCube (Twine)

**Prerequisites**: Tweego installed and in PATH, or in project root.

```bash
/speckit.compile --engine sugarcube
```

Output: `output/sugarcube/story.html`

**What happens**:
1. Finds all `draft/squ/*.twee` files
2. Combines with `themes/story.css`
3. Translates `MECHANIC:` hooks to `<<set>>` syntax
4. Runs Tweego to compile `.twee` → `.html`
5. Outputs playable story.html

**Customization**:

```bash
/speckit.theme --engine sugarcube --base dark --accent #ff00ff
```

Generates custom `themes/story.css` with purple accent on dark background.

### Ink

**Prerequisites**: Inklecate installed globally.

```bash
/speckit.compile --engine ink
```

Output: `output/ink/story.html`

**What happens**:
1. Finds all `draft/ink/*.ink` files
2. Translates `MECHANIC:` hooks to Ink variable syntax
3. Runs inklecate to compile `.ink` → `.json`
4. Wraps story.json in `themes/ink-theme.html`
5. Outputs playable story.html

**Theme customization**:

```bash
/speckit.theme --engine ink --base light
```

Generates `themes/ink-theme.html` with light HTML wrapper.

### Multi-Engine

```bash
/speckit.compile --all-engines
```

Compiles to both SugarCube and Ink simultaneously.

**Output**:
- `output/sugarcube/story.html` ✅
- `output/ink/story.html` ✅

Both read from same `draft/shared/` prose, just different syntax in `draft/squ/` and `draft/ink/`.

---

## Validation Workflow Guide

### Validation Order (Critical)

The validators build on each other. Run in this order:

1. **speckit.analyze** — Structural gates (pre-requisite for all others)
2. **speckit.agency** — Player agency (affects choice design)
3. **speckit.consequences** — Choice outcomes (affects agency)
4. **speckit.continuity** — Cross-branch consistency (affects state logic)
5. **speckit.pacing** — Beat spacing (affects narrative flow)
6. **speckit.accessibility** — Reading level (affects prose revision)
7. **All others** — Can run in any order

### Interpretation Guide

Each validator outputs an audit file in `specs/`. Read the report, interpret severity (🔴 URGENT vs 🟡 WARNING vs 🟢 INFO), and decide:

**🔴 URGENT (Must Fix)**:
- Unreachable endings
- Illusory choices (no consequences)
- Dead-end variable states
- Broken mechanic hooks

**🟡 WARNING (Should Fix)**:
- Hollow emotional beats
- Reading level too high
- Missing content warnings
- Slow pacing

**🟢 INFO (Consider)**:
- Opportunity for more unique content
- Replayability could improve
- Optional refinement

### Fix Workflow

After each validator identifies issues:

```bash
# Option 1: Surgical revision of specific passage
/speckit.revise --fix-[validator]

# Option 2: Re-draft specific node
/speckit.implement NODE-010

# Option 3: Manual edit in draft/[engine]/NODE-XXX.md, then re-validate
$EDITOR draft/squ/NODE-010.twee

# Re-run validator to confirm fix
/speckit.[validator] NODE-010
```

### When to Stop Validating

- All 🔴 URGENT issues resolved? ✅
- 80%+ of 🟡 WARNINGs addressed? ✅
- Game is playable end-to-end? ✅

**You're ready to compile and release.**

---

## Comparable Products

| Product | Strength | vs. Spec Kit |
|---|---|---|
| Twine 2 | Visual flowchart editor | Spec Kit adds: AI prose drafting, validation suite, variable tracking |
| Ink | Narrative scripting language | Spec Kit adds: Visual planning, quality validation, multi-engine support |
| ChoiceScript | Quest design framework | Spec Kit adds: Dialogue tree support, trust states, series management |
| UnityNarrative | Game engine integration | Spec Kit adds: AI drafting, offline operation, language-agnostic |

---

## Related Resources

- **[Spec Kit Documentation](https://github.com/adaumann/specify)** — Core CLI reference
- **[Twine 2 Documentation](https://twine2.neocities.org/)** — SugarCube target
- **[Ink Documentation](https://github.com/inkle/ink/blob/master/Documentation/Writing%20with%20Ink.md)** — Ink target
- **[Interactive Narrative Design Patterns](https://game.dev)** — Branching best practices
- **[Trust State Mechanics](https://research.google.com/pubs)** — NPC relationship frameworks
- **[WCAG Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)** — Contrast and readability standards

---

**Ready to start?** Run `/speckit.constitution` to set up your first game!
