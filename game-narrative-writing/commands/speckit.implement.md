---
description: Draft a full node from an APPROVED outline. Enforces hook declarations, POV rules, and craft rules from constitution.md.
handoffs:
  - label: Generate Outline First
    agent: speckit.outline
    prompt: The outline does not exist or is not yet approved. Generate the node outline first.
    send: true
  - label: Verify Node Output
    agent: speckit.verify
    prompt: Validate and verify the drafted node against the engine compiler and unit tests
    send: true
  - label: Run Quality Checklist
    agent: speckit.checklist
    prompt: Run the quality checklist on the drafted node
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a continuity check across all drafted nodes
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

# speckit.implement

Draft a full node file (`spec/<specname>/draft/[ENGINE]/NODE-NNN.[EXT]`) from an approved node outline.

**Language Rule**: This is the **ONLY** stage where the `[LANGUAGE]` setting from `constitution.md` is applied. All prose and dialogue generated in this step will be written in the target language. All preceding planning and outlining documents (spec, flowmap, outlines, profiles, etc.) are strictly English-only to ensure structural clarity.

**Gate requirement**: The outline (`outlines/NODE-NNN.md`) must have `status: APPROVED`. If status is `DRAFT` or `SKIP`, `speckit.implement` will halt.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- `[NODE_ID]` - draft a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` - draft a list of nodes in sequence
- `--outline-only` - generate the outline only (delegates to `speckit.outline`; does not draft the node)
- `--force` - redraft an existing node (prompts for confirmation)
- *(no argument)* - draft the next APPROVED outline that has no corresponding node file

## Pre-Execution Checks

**Check for extension hooks (before drafting)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_implement` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**Checklist gate** (if `checklists/` exists):
- Scan all checklist files in `checklists/`
- If ANY checklist has incomplete items, output a status table and **stop**:

  ```
  CHECKLIST GATE: Incomplete quality gates detected.

  | Checklist | Total | Complete | Incomplete |
  |---|---|---|---|
  | [name] | N | N | N |

  These checklists must be completed before drafting continues.
  To override: explicitly confirm "proceed despite incomplete checklists"
  ```
- If the user explicitly confirms, proceed with a warning in the draft output.

**Outline gate**:
   - Resolve the target node ID from `$ARGUMENTS` or `tasks.md` (first unchecked task with a `spec/<specname>/draft/[ENGINE]/` output path).
- Look for `outlines/[NODE_ID].md`:
  - If absent - halt: "No outline found. Run `speckit.outline [NODE_ID]` first."
  - If `status: DRAFT` - halt:
    ```
    OUTLINE GATE: outlines/[NODE_ID].md has status: DRAFT.

    Review the node outline, edit beats and variable tables as needed, then set:
        status: APPROVED

    To write this node yourself instead, set:
        status: SKIP

    Then re-run speckit.implement
    ```
  - If `status: SKIP` - do not generate any prose. Instead:
    - Report: `SKIP: [NODE_ID] [title] - author will write this node. No prose generated.`
    - Mark the corresponding task `[x]` in `tasks.md` with note: `[author-written - no AI draft]`
    - Advance to the next unchecked task and repeat the outline gate check.
  - If `status: APPROVED` - proceed.
- If `spec/<specname>/draft/[ENGINE]/NODE-NNN.[EXTENSION]` already exists and `--force` not set: ask user to confirm overwrite.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **`--outline-only` mode**: If `$ARGUMENTS` contains `--outline-only`:
   - Run `speckit.outline` behaviour for the target node(s) instead of drafting prose.
   - Generate `outlines/[NODE_ID].md` with `status: DRAFT`.
   - Do **not** write any prose or create any file in `spec/<specname>/draft/[ENGINE]/` yet.
   - Report the outline file path(s) and remind the author to review, then approve or set `status: SKIP`.
   - Stop after generating outlines.

3. **Load context**:
   - **Required**: `outlines/[NODE_ID].md` (the APPROVED outline is the authoritative drafting brief)
   - **Required**: `.specify/memory/constitution.md` - extract: `export_engines` (list of target engines), `player_perspective` (POV default), enabled mechanics list (Section II), `tone`, `style_mode`, `prose_profile`, Prose Style Mode (Section VII: tense, sentence rhythm, vocabulary register, sensory density)
   - **Required**: `specs/mechanics.md` - hook syntax definitions, tier levels, and translation tables for all hook types (including newly declared or promoted mechanics)
   - **Required**: `specs/endings.md` — validate that any terminal choice target is a valid `END-NNN` entry
   - **Required**: `specs/characters.md` index + `specs/characters/` profiles (NPC trust thresholds, state values, bark line register, dialogue style) — load for each NPC present in this node
   - **Required if style_mode is humanized-ai**: `.specify/memory/craft-rules.md` - read active prose profile section, NPC Voice & Dialogue rules, Description & World rules, anti-AI clichés filter, prohibited phrases
   - **Required**: `specs/variables.md` - validate all `variables_read` and `variables_set` in the outline are registered; warn on any undeclared variable: `Variable $[name] is not in variables.md. Register it before drafting.`
   - **Optional**: `specs/glossary.md` — load if present; check terminology usage during drafting for consistency with registry
   - **Optional**: `specs/locations.md` — load if present; pull sensory anchors and location rules for this node's setting (from outline's Setting Anchors field)
   - **Optional**: `specs/themes.md` — load if present; check thematic work field in outline; ensure prose carries thematic payload (references to motifs/symbols if flagged in outline)
   - **Optional**: `specs/world-building.md` - sensory anchors, atmosphere notes for the node's setting
   - Read `tasks.md` - identify the first group of unchecked tasks (respect `[P]` markers for parallel drafting)
   - If the outline contains `[NEEDS CLARIFICATION]`, `[MISSING NODE]`, `[UNREGISTERED ENDING]`, or `[LOCATION PROFILE NEEDED]` markers, **pause** and resolve them with the user before drafting.

4. **Draft the node**:

   **Output path**: `spec/<specname>/draft/[ENGINE]/[NODE_ID].[EXTENSION]`
   
   **Multi-Engine Generation**: For each engine in `export_engines`, generate a separate file:
   
   Directory structure is organized by target engine:
   - `spec/<specname>/draft/generic/NODE-NNN.[title].md` — for `.md` (annotated Markdown with hook blocks)
   - `spec/<specname>/draft/sugarcube/NODE-NNN-[title].twee` — for `.twee` (Twine/SugarCube)
   - `spec/<specname>/draft/ink/NODE-NNN-[title].ink` — for `.ink` format
   - `spec/<specname>/draft/renpy/NODE-NNN-[title].rpy` — for `.rpy` (Ren'Py)
   - `spec/<specname>/draft/escoria/NODE-NNN-[title].esc` — for `.esc` (Godot Escoria)
   - `spec/<specname>/draft/ags/NODE-NNN-[title].asc` — for `.asc` (Adventure Game Studio)
   - `spec/<specname>/draft/unity/NODE-NNN-[title].cs` or `.yarn` — for Yarn spinner
   
   File naming convention:
   - `generic` -> `NODE-NNN.md`
   - `sugarcube` -> `NODE-NNN-[title].twee`
   - `ink` -> `NODE-NNN-[title].ink`
   - `renpy` -> `NODE-NNN-[title].rpy`
   - `escoria` -> `NODE-NNN-[title].esc`
   - `ags` -> `NODE-NNN-[title].asc`
   - `unity` -> `NODE-NNN-[title].cs` or `.yarn`
   
   Create the `spec/<specname>/draft/[ENGINE]/` directory if it does not exist.

   **Engine-Specific Syntax Rules**:
   - **Generic**: Use YAML header `---` and Markdown choices `- [Label](NODE_ID)`.
   - **Twine/SugarCube**: Use `.twee` format with `:: PassageName` headers and `[[Label->PassageName]]` links.
   - **Ink**: Wrap header in `/* ... */`, use `=== knot_name ===` for title, and `* [Label] -> target_knot` for choices.
   - **Ren'Py**: Wrap header in `#`, use `label [node_id]:` for title, and `menu:` block with quoted string options for choices.
   - **Escoria**: Wrap header in `#`, use `:node_name` state labels, and `?` / `- Label: set_scene target` for choices.
   - **AGS**: Wrap header in `/* ... */`, use C-style function declarations, and `cCharacter.Say()` for dialogue.
   - **Unity/Yarn**: Use `title: [NODE_ID]` header, `===` separator, and `-> Label` options for choices.

   **Every draft file MUST begin with this metadata block** (wrapped in the correct comment syntax for the engine):
   ```
   node_id: [NODE_ID]
   title: [NODE_TITLE]
   act: [ACT_NUMBER]
   status: DRAFT
   pov: [POV_OVERRIDE or blank for constitution.md default]
   variables_read: [list from approved outline]
   variables_set: [list from approved outline]
   drafted: [YYYY-MM-DD]
   outline_ref: outlines/[NODE_ID].md
   ```
   For engines that cannot use YAML front-matter, wrap this block in the appropriate comment marker
   (`/* ... */` for Ink/AGS, `#` for Ren'Py/Escoria, `///` for Yarn).

   **Before writing prose**:
   - Confirm POV from `constitution.md` (`player_perspective`) or outline `pov` override
   - Confirm all NPC profiles needed for this node are loaded (dialogue style, state values)
   - Note the beat summary from the outline - the draft MUST open with an orienting line (where, who, what is at stake) and follow the beats causally
   - Note the Choices table from the outline - the draft MUST include all choices

   **Pre-Draft Validation Checklist**:
   - ✓ Ending gates: All terminal choices point to registered `END-NNN` entries
   - ✓ Characters loaded: All NPCs in this node have character profiles available
   - ✓ Location context: If Setting Anchors field is populated, location profile has been loaded
   - ✓ Terminology registry: If `[GLOSSARY NOTE]` markers present, glossary.md has been loaded
   - ✓ No blocking clarification markers present

   **While writing**:
   - Apply craft rules (NR-NNN and PR-NNN from `.specify/memory/craft-rules.md`)
   - Apply active prose profile from `constitution.md` `prose_profile` field (dialogue-heavy, environmental, action-forward, atmospheric, minimalist)
   - Apply Prose Style Mode from `constitution.md`: match declared tense, sentence rhythm, vocabulary register, and sensory density; apply anti-AI filter from craft-rules.md if style mode is `humanized-ai`; use extracted voice markers from constitution if style mode is `author-sample`
   - Match tone (from `constitution.md` `tone` field) and dialogue register to each NPC's profile
   - Check prohibited phrases from `.specify/memory/craft-rules.md` before finalising prose
   - **Check terminology consistency** (if glossary.md loaded): When introducing specialized terms, cross-check against `specs/glossary.md` to ensure usage matches registered definitions
   - **Apply location anchors** (if locations.md loaded): Use sensory details from Setting Anchors field; ensure descriptions match the location profile from `specs/locations.md`
   - **Weave thematic elements** (if themes.md loaded): If outline flags thematic work for this node, embed motif references or symbol occurrences naturally into prose (from `specs/themes.md` registry)
   - **Match NPC registers** (from characters.md): For each NPC in this node, pull their trust state (from Variables Read), then render dialogue at the correct register from `specs/characters/[NPC_ID].md` section "VIII. Dialogue Register by Trust State"
   - **Generate Dialogue Tree** (if outline has `Dialogue Tree` field): Render each player dialogue option with NPC responses in sequence. Show multi-party reactions naturally with action beats between lines (not as list format). For Twine: structure as passages with inline responses. For Ink: use `*` for dialogue choices and `+` for sub-branches. Track dialogue choices via `CHOICE_MEMORY` hook if needed for later branches.
   - **Engine Synthesis**: If the target engine is not `generic`, translate all structural markers (headings, paragraphs, dialogue) into engine-native code (e.g., `say` commands for Escoria, `label` and `show` for Ren'Py, `=== knot ===` for Ink).

   **Insert mechanic hooks and logic**:
   - If target is `generic`: Insert `[MECHANIC:TYPE]` blocks after prose body, using hook syntax from `specs/mechanics.md`.
   - If target is engine-specific: Translate all logic directly into code using the maps in `specs/mechanics.md` (e.g., `~ flag = true` for Ink, `$ flag = true` for Ren'Py Python block).
   - Tier 1 hooks: insert fully
   - Tier 2 hooks: insert as stubs with engine-specific comment syntax (e.g., `//` or `#`)
   - Verify each hook variable is declared in `specs/variables.md`
   - **CURRENCY**: every `MECHANIC:CURRENCY` block MUST include `variable=[variable_name]`; the variable must be `type: currency` in `variables.md`. If `variable=` is absent, do not guess - warn: `CURRENCY hook missing variable= - add the currency variable name.`
   - **RANDOM**: every `MECHANIC:RANDOM` block MUST include `variable=[name] min=N max=N`; variable must be `type: counter` in `variables.md`. Warn if range is missing.
   - **CHOICE_MEMORY**: `variable=` must be `type: string` in `variables.md`; `value=` must be a quoted choice label. Ink targets: add a comment `// CHOICE_MEMORY: [label] will map to integer constant`.
   - **CLUE**: `clue_id` must follow the `clue_` prefix convention and be declared as `type: flag` in `variables.md`. If a new clue is being added that is not yet in `variables.md`, warn: `Clue [clue_id] not in variables.md - register it.`
   - Warn if a TIMER hook uses seconds: `Timer hook type is seconds - Sugarcube requires a JS widget; Ink does not support real-time timers.`
   - Warn for each Tier 2 hook used: `Tier 2 stub [HOOK_TYPE] - will produce an UNSUPPORTED HOOK comment.`

   **Write choices/branching section**:
   - Minimum 2 choices unless node is terminal (ending node).
   - If target is `generic`: Use a `## Choices` heading followed by `- [Label text](TARGET_NODE_ID)`.
   - If target is engine-specific: Use native menu/choice syntax per the **Engine-Specific Syntax Rules** above.
   - Choice labels: active verb phrase, player-agency framing, no meta-language.
   - Conditional choices: use engine-native `if` logic or gates (e.g., `* {var} [Label] -> target` in Ink).
   - All target node IDs must exist in `specs/plan.md`.

   **After writing**:
   - **Verification Step** - automatically run `speckit.verify [NODE_ID]` for each generated engine file:
     - Runs structural unit tests (`test_nodes.py`) against the drafted file.
     - Runs the engine compiler/linter (`validate_engine.py --target [ENGINE]`) where ENGINE is from `export_engines`.
     - If errors are found, enter the **Self-Correction Loop** (max 3 attempts):
       1. Analyze compiler/test error output.
       2. Apply the minimal targeted fix to the node file.
       3. Re-run validation.
       4. If clean within 3 attempts: add `verified: true` to the YAML header and continue.
       5. If still failing after 3 attempts: report the unresolved errors and prompt the user for guidance. Do not mark as verified.
     - If toolchain is missing, run only structural tests and note the missing binary.
   - Add a `DRAFT NOTES` comment block at the top of the file using engine-specific comment markers:
     ```
     [Comment Marker] DRAFT NOTES
          Outline ref:       outlines/[NODE_ID].md
          Deviation from outline: [None / describe]
          New variable states discovered: [list]
          Unresolved items: [list]
     ```
   - Mark the corresponding task `[x]` in `tasks.md`
   - Note any newly discovered variable states or branch conditions not in the outline - add to `outlines/[NODE_ID].md` Deviations section

   **If a new unplanned node is needed** (discovered during drafting - a missing transition, required setup, etc.):
   - **STOP drafting**. Do not write the node yet.
   - Notify the user: "Drafting [NODE_ID] requires an unplanned node: [description]. Add it to `specs/plan.md` before drafting continues."
   - Add the new node to `specs/plan.md` with a `[NEEDS OUTLINE]` marker
   - Add a corresponding task entry in `tasks.md` immediately after the related task
   - Resume drafting only after both files are updated
   - **`specs/plan.md` is the authoritative node list. `tasks.md` must never contain nodes that are not in `plan.md`**
