---
description: Generate editable node outline files from plan.md. Authors review and approve each outline before AI drafting begins, or mark SKIP to write their own prose.
handoffs:
  - label: Start Drafting
    agent: speckit.implement
    prompt: Draft nodes from approved outlines
    send: true
  - label: Check Branch Structure First
    agent: speckit.plan
    prompt: Node targets or branch logic conflict with the flowmap. Please review and fix it.
    send: true
---

# speckit.outline

Generate a node outline (`outlines/NODE-NNN.md`) for one or more nodes. Outlines must be reviewed and approved before `speckit.implement` will draft the node.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- `[NODE_ID]` � generate outline for a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` � generate outlines for a list of nodes
- `--act [N]` � outline all nodes for a given act
- `--force` � regenerate an existing outline (overwrite)
- `--batch` / `--all` — generate outlines for ALL nodes listed in `plan.md` that do not yet have an outline
- *(no argument)* — outline the next unoutlined node from `plan.md`

## Pre-Execution Checks

**Check for extension hooks (before outline generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_outline` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:
1. Confirm `specs/[FEATURE_DIR]/plan.md` and `.specify/memory/constitution.md` exist.
2. For each requested node, verify it appears in `plan.md` — warn if not found.
3. **Skip any node that already has an outline file with `status: APPROVED` or `status: SKIP`** � never overwrite approved or skipped outlines unless `--force` is set.
4. Confirm `specs/[FEATURE_DIR]/variables.md` exists � hooks cannot be declared without it.

## Outline

**Goal**: Generate structured, decision-complete node outlines in `outlines/` that give the author all the information needed to approve the node before drafting begins.
**Language Rule**: All node outlines MUST be generated in English (`en`) by default, regardless of any `[LANGUAGE]` setting in the constitution. This stage remains in English to facilitate author review against project specifications.

### Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Load source documents**:
   - **Required**: `specs/plan.md` (node graph, branch dependencies, act breakdown), `specs/spec.md` (NPC profiles, variable registry, research gaps)
   - **Required**: `.specify/memory/constitution.md` (enabled mechanics list, world rules, tone, target platform, `prose_profile`)
   - **Required**: `specs/mechanics.md` (hook schemas, tier levels, translations, parameter definitions for all declared hooks including newly added ones)
   - **Required**: `specs/endings.md` (ending IDs, variable gates, thematic statements) -- needed to validate all choice targets
   - **Required**: `specs/characters.md` index + `specs/characters/` profiles (NPC trust thresholds, state behaviors, bark lines, dialogue consistency)
   - **Required if style_mode is humanized-ai**: `.specify/memory/craft-rules.md` (to tune beat language and dialogue register per active prose profile)
   - **Optional**: `specs/variables.md` (declared variables with types and value ranges) -- validate Variables Read and Variables Set sections
   - **Optional**: `specs/glossary.md` (terminology registry) -- load if present; check outline for any terminology that should be flagged for consistency checking during drafting
   - **Optional**: `specs/locations.md` (sensory anchors, location rules) -- load if present; populate location context in outline if this node takes place in a key location
   - **Optional**: `specs/themes.md` -- load if present; use to populate the Thematic work field in the outline Beat Summary: match the node's act to the Thematic Arc by Act table, and check whether any registered motif (MO-NNN) or symbol has a planned occurrence in this node
   - **Optional**: `specs/world-building.md` (location sensory anchors, world rules)
   - Note any missing required documents -- abort with clear error if `specs/endings.md` or `specs/characters.md` missing
   - Note any missing optional documents � affected outline sections are marked `[TBD � populate <document>]`

3. **Determine target nodes**:
   - If `$ARGUMENTS` is `--batch` or `--all`: find ALL nodes in `plan.md` that do not yet have an outline file and process them in order.
   - If `$ARGUMENTS` is empty: find the first node in `plan.md` that has no outline file yet.
   - If `$ARGUMENTS` is a node ID or list: use those nodes.
   - If `$ARGUMENTS` is `--act N`: use all nodes in that act without an existing outline file.
   - Skip any node already outlined with `status: APPROVED` or `status: SKIP` (unless `--force`).

4. **For each target node, generate an outline file**:

   **Output path**: `outlines/[NODE_ID].md`

   Use `templates/node-outline-template.md` as the base structure. Populate each section from the source documents:

   **Frontmatter** — pull from `plan.md` node entry:
   - `node_id`, `title`, `act`, `status: DRAFT`, `pov` (from constitution.md default or node override)

   **Beat Summary** � derive from the flowmap node entry:
   - 2�4 sentences: what happens in this node, what the player is doing or deciding
   - Narrative purpose: `decision / consequence / revelation / setup / hub / transition / climax / ending`
   - Tension level: 1�10 with brief rationale

   **Variables Read** � derive from flowmap branch conditions into this node:
   - Each variable used as a gate or prose condition, with expected value and source node
   - Flag any variable not yet declared in `variables.md` with `[UNDECLARED]`

   **Variables Set** � derive from flowmap annotations and constitution.md hook schemas:
   - Each variable changed by this node, with hook type, new value/delta, and trigger condition
   - Flag any variable not yet declared in `variables.md` with `[UNDECLARED]`

   **Choices** — derive all outgoing edges from `plan.md`:
   - Minimum 2 choices for non-terminal nodes; 0 for ending nodes
   - Each choice: label, condition (if conditional), target node ID, narrative consequence
   - Default path if no conditional choices are met

   **Dialogue Tree** — *only if node is flagged `(dialogue-centric)` or `(mixed)` in plan.md*:
   - Structure player dialogue options and NPC responses within the node
   - Each dialogue choice includes: player phrase, NPC responses by character, gating/variable effects
   - Include all NPCs present in this node; each NPC uses their correct dialogue register from `specs/characters/[NPC_ID].md` Section VIII
   - Multi-party reactions: both/all NPCs respond to the player's dialogue choice (shown in sequence)
   - Dialogue sub-branches: indicate if a dialogue choice continues in-node or branches to a different node
   - If no structured dialogue tree is needed, mark as `None`

   **Mechanic Hooks Summary & Checklist** — Identify all mechanics relevant to this node:
   
   1. **First, derive explicit hooks** from `specs/mechanics.md` and flowmap annotations:
      - All hooks already triggered: type, tier (1 or 2), variable, action, timing
      - Include any custom hooks added via `speckit.mechanics declare`

   2. **Then, use the Mechanic Hooks Checklist** (in template) to identify forgotten mechanics:
      
      For each node type, prompt the author through these common patterns:
      - **Dialogue-centric** (dialogue-heavy prose_profile or dialogue-centric flag):
        - ✓ CHOICE_MEMORY (record which dialogue option player chose)
        - ✓ TRUST (dialogue choice should affect NPC trust by ±N)
        - ✓ NPC_STATE (dialogue can change NPC mood or relationship tier)
        - ✓ FLAG (dialogue might reveal secrets or flag new knowledge)
        
      - **Quest/Task hub** (setup or hub narrative purpose):
        - ✓ COUNTER (track active quests, attempts, or rounds)
        - ✓ INVENTORY (check prerequisites, award completion items)
        - ✓ VISITED (mark location explored)
        
      - **Investigative/Mystery** (contains clue discovery or evidence gathering):
        - ✓ CLUE (discover evidence piece)
        - ✓ INVENTORY (collect physical evidence)
        - ✓ COUNTER (track evidence collected, theories tested)
        
      - **Timed challenge** (tension level 7+, obstacle or puzzle):
        - ✓ TIMER (start countdown or ticking timer)
        - ✓ COUNTER (track attempts or rounds remaining)
        - ✓ ENDING_CONDITION (major success/failure consequence)
        
      - **Choice consequence** (decision node with multiple paths):
        - ✓ TRUST (choice affects NPC relationships)
        - ✓ FLAG (choice unlocks/locks paths)
        - ✓ NPC_STATE (NPC reacts to choice)
        - ✓ ENDING_CONDITION (choice pushes toward specific ending)
        
      - **Any node with player resources (items, money, health)**:
        - ✓ INVENTORY (track items acquired/lost)
        - ✓ CURRENCY (track resources spent/gained)

   3. **Populate the template's Mechanic Hooks Checklist**: 
      - Check the boxes for all mechanics that should apply to this node
      - Fill in the summary table at the top with the concrete hooks
      - Reference "Common Hook Combinations" section if uncertain

   **Branch Logic Notes** � pull from flowmap annotations:
   - Any complex gate logic, reachability conditions, or POV overrides
   - If this node is only reachable via specific upstream variable states, document them here

   **Game Bible Compliance Notes** � scan `constitution.md` for:
   - Any mechanic or hook constraints relevant to this node
   - Platform/engine limits on choice count or variable types
   - POV rules or tone requirements that apply

   **Deviations from plan.md** — default to `None`. Only populate if the outline generation process identified an inconsistency (e.g. a variable read in this node that no upstream node sets).

   **Ending Gate Validation** — derive from `specs/endings.md`:
   - For each choice in the Choices table:
     - If the target node ID is a terminal node: verify it maps to a valid `END-NNN` entry in `specs/endings.md`
     - Flag any choice target that is not in `plan.md` as `[MISSING NODE]`
     - Flag any ending node reference that has no corresponding `END-NNN` in `specs/endings.md` as `[UNREGISTERED ENDING]`

   **Location & Sensory Context** — load from `specs/locations.md` if present:
   - If this node's title or POV mentions a location, find that location in `specs/locations.md`
   - Populate a new **Setting Anchors** field in the outline with sensory and rule details from the location profile
     - E.g., "Sanctuary Station: sterile white walls, hum of life support, restricted entry"
   - If location is absent from locations.md, mark as `[LOCATION PROFILE NEEDED]`

   **Terminology Cross-Check** — load from `specs/glossary.md` if present:
   - Scan beat summary and choice labels for any specialized terminology
   - If any term appears in both the outline and `specs/glossary.md`, cross-reference the definition in the Glossary section of the outline
   - Flag any term used that is not in the glossary (for writer awareness during drafting) as `[GLOSSARY NOTE]`

5. **Outline quality rules**:
   - Every beat must be one sentence � no prose
   - If a `[NEEDS CLARIFICATION]` marker is present in the flowmap entry, propagate it into the outline � do not invent a resolution
   - A variable listed in Variables Read must be set by at least one upstream node in `plan.md` — flag otherwise
   - No choice may target a node ID not present in `plan.md`
   - The outline is a brief, not a draft � no narrative prose, no dialogue text

6. **Report**: List all outline files created with their output paths and `status: DRAFT`. Include a per-node summary: `[NODE_ID] [title] — [N] beats, [N] choices, [N] variables set, [ending gates], act [N]`. Flag any:
   - `[UNDECLARED]` variables
   - `[MISSING NODE]` choice targets
   - `[UNREGISTERED ENDING]` terminal nodes
   - `[LOCATION PROFILE NEEDED]` locations not in locations.md
   - `[GLOSSARY NOTE]` terminology not in glossary.md
   - Propagated `[NEEDS CLARIFICATION]` markers
   
   Remind the author to:
   - Review each outline file and edit beats, choices, and variable tables as needed
   - **Complete the Mechanic Hooks Checklist** for each node — check all applicable hook types (dialogue-centric nodes should include CHOICE_MEMORY + TRUST + NPC_STATE; quest hubs should include COUNTER + INVENTORY; timed challenges should include TIMER; etc.)
   - Verify ending gates are correct (choice targets are valid ending IDs or intermediate nodes)
   - Check sensory anchors for location-based nodes
   - Change `status: DRAFT` ? `status: APPROVED` when satisfied, or `status: SKIP` to write the node themselves
   - Run `speckit.implement` once outlines are approved

7. **Check for extension hooks** (after generation): check `hooks.after_outline`.

