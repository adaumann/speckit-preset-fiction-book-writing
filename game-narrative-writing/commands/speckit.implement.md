---
description: Draft a full node from an APPROVED outline. Enforces hook declarations, POV rules, and craft rules from constitution.md.
handoffs:
  - label: Generate Outline First
    agent: speckit.outline
    prompt: The outline does not exist or is not yet approved. Generate the node outline first.
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

Draft a full node file (`nodes/NODE-NNN.md`) from an approved node outline.

**Language Rule**: This is the **ONLY** stage where the `[LANGUAGE]` setting from `constitution.md` is applied. All prose and dialogue generated in this step will be written in the target language. All preceding planning and outlining documents (spec, flowmap, outlines, profiles, etc.) are strictly English-only to ensure structural clarity.

**Gate requirement**: The outline (`outlines/NODE-NNN.md`) must have `status: APPROVED`. If status is `DRAFT` or `SKIP`, `speckit.implement` will halt.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- `[NODE_ID]` — draft a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` — draft a list of nodes in sequence
- `--outline-only` — generate the outline only (delegates to `speckit.outline`; does not draft the node)
- `--force` — redraft an existing node (prompts for confirmation)
- *(no argument)* — draft the next APPROVED outline that has no corresponding node file

## Pre-Execution Checks

**Check for extension hooks (before drafting)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_implement` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**Checklist gate** (if `checklists/` exists):
- Scan all checklist files in `checklists/`
- If ANY checklist has incomplete items, output a status table and **stop**:
  ```
  ⚠️ CHECKLIST GATE: Incomplete quality gates detected.

  | Checklist | Total | Complete | Incomplete |
  |---|---|---|---|
  | [name] | N | N | N |

  These checklists must be completed before drafting continues.
  To override: explicitly confirm "proceed despite incomplete checklists"
  ```
- If the user explicitly confirms, proceed with a warning in the draft output.

**Outline gate**:
- Resolve the target node ID from `$ARGUMENTS` or `tasks.md` (first unchecked task with a `nodes/` output path).
- Look for `outlines/[NODE_ID].md`:
  - If absent → halt: "No outline found. Run `speckit.outline [NODE_ID]` first."
  - If `status: DRAFT` → halt:
    ```
    ⚠️ OUTLINE GATE: outlines/[NODE_ID].md has status: DRAFT.

    Review the node outline, edit beats and variable tables as needed, then set:
        status: APPROVED

    To write this node yourself instead, set:
        status: SKIP

    Then re-run speckit.implement
    ```
  - If `status: SKIP` → do not generate any prose. Instead:
    - Report: `⏭ SKIP: [NODE_ID] [title] — author will write this node. No prose generated.`
    - Mark the corresponding task `[x]` in `tasks.md` with note: `[author-written — no AI draft]`
    - Advance to the next unchecked task and repeat the outline gate check.
  - If `status: APPROVED` → proceed.
- If `nodes/NODE-NNN.md` already exists and `--force` not set: ask user to confirm overwrite.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **`--outline-only` mode**: If `$ARGUMENTS` contains `--outline-only`:
   - Run `speckit.outline` behaviour for the target node(s) instead of drafting prose.
   - Generate `outlines/[NODE_ID].md` with `status: DRAFT`.
   - Do **not** write any prose or create any file in `nodes/`.
   - Report the outline file path(s) and remind the author to review, then approve or set `status: SKIP`.
   - Stop after generating outlines.

3. **Load context**:
   - **Required**: `outlines/[NODE_ID].md` (the APPROVED outline is the authoritative drafting brief)
   - **Required**: `.speckit/memory/constitution.md` — extract: `player_perspective` (POV default), `tone`, active mechanic schemas, craft rules (NR-NNN, PR-NNN), prohibited phrases, Prose Style Mode (Section VII: tense, sentence rhythm, vocabulary register, sensory density, anti-AI filter active)
   - **Required**: `specs/variables.md` — validate all `variables_read` and `variables_set` in the outline are registered; warn on any undeclared variable: `Variable $[name] is not in variables.md. Register it before drafting.`
   - **Required**: `specs/mechanics.md` — hook syntax definitions for each hook type
   - **Optional**: `specs/characters/[NPC_ID].md` — NPC trust thresholds, state values, bark line register, dialogue style (load for each NPC present in this node)
   - **Optional**: `specs/world-building.md` — sensory anchors, atmosphere notes for the node's setting
   - Read `tasks.md` — identify the first group of unchecked tasks (respect `[P]` markers for parallel drafting)
   - If the outline contains `[NEEDS CLARIFICATION]` markers, **pause** and resolve them with the user before drafting.

4. **Draft the node**:

   **Output path**: `nodes/[NODE_ID].md`
   Use `templates/implement-template.md` as the base structure.

   **Every draft file MUST begin with this header block** (machine-readable; do not omit or reorder fields):
   ```
   ---
   node_id: [NODE_ID]
   title: [NODE_TITLE]
   act: [ACT_NUMBER]
   status: DRAFT
   pov: [POV_OVERRIDE or blank for constitution.md default]
   variables_read: [list from approved outline]
   variables_set: [list from approved outline]
   drafted: [YYYY-MM-DD]
   outline_ref: outlines/[NODE_ID].md
   ---
   ```

   **Before writing prose**:
   - Confirm POV from `constitution.md` (`player_perspective`) or outline `pov` override
   - Confirm all NPC profiles needed for this node are loaded (dialogue style, state values)
   - Note the beat summary from the outline — the draft MUST open with an orienting line (where, who, what is at stake) and follow the beats causally
   - Note the Choices table from the outline — the draft MUST include all choices

   **While writing**:
   - Apply craft rules (NR-NNN and PR-NNN from `constitution.md`)
   - Apply Prose Style Mode (Section VII of `constitution.md`): match declared tense, sentence rhythm, vocabulary register, and sensory density; apply anti-AI filter if active; use extracted voice markers if style mode is `author-sample`
   - Match tone (from `constitution.md` `tone` field) and dialogue register to each NPC's profile
   - Check prohibited phrases before finalising prose
   - Prose must read coherently if all mechanic hook blocks are removed

   **Insert mechanic hook blocks** after prose body, using hook syntax from `specs/mechanics.md`:
   - Tier 1 hooks: insert fully
   - Tier 2 hooks: insert as stubs with `// TIER 2 STUB` comment
   - Verify each hook variable is declared in `specs/variables.md`
   - **CURRENCY**: every `MECHANIC:CURRENCY` block MUST include `variable=[variable_name]`; the variable must be `type: currency` in `variables.md`. If `variable=` is absent, do not guess — warn: `⚠️ CURRENCY hook missing variable= — add the currency variable name before exporting.`
   - **RANDOM**: every `MECHANIC:RANDOM` block MUST include `variable=[name] min=N max=N`; variable must be `type: counter` in `variables.md`. Warn if range is missing.
   - **CHOICE_MEMORY**: `variable=` must be `type: string` in `variables.md`; `value=` must be a quoted choice label. Ink targets: add a comment `// CHOICE_MEMORY: [label] will map to integer constant at export`.
   - **CLUE**: `clue_id` must follow the `clue_` prefix convention and be declared as `type: flag` in `variables.md`. If a new clue is being added that is not yet in `variables.md`, warn: `⚠️ Clue [clue_id] not in variables.md — register it before export.`
   - Warn: `⚠️ Timer hook type is seconds — Sugarcube requires a JS widget for this; Ink does not support real-time timers.` if a TIMER hook uses seconds
   - Warn: `⚠️ Tier 2 stub [HOOK_TYPE] — will produce an UNSUPPORTED HOOK comment in export output.` for each Tier 2 hook used

   **Write choices section**:
   - Minimum 2 choices unless node is terminal (ending node)
   - Use a `## Choices` heading followed by one entry per choice — `export.py` requires this exact format:
     ```
     ## Choices

     - [Label text](TARGET_NODE_ID)
     - [Conditional label](TARGET_NODE_ID) <!-- requires: $var_name == value -->
     ```
   - Choice labels: active verb phrase, player-agency framing, no meta-language
   - Conditional choices carry the gate expression as an HTML comment after the link
   - All target node IDs must exist in `specs/flowmap.md`

   **After writing**:
   - Add a `DRAFT NOTES` comment block at the top of the file (after frontmatter):
     ```
     <!-- DRAFT NOTES
          Outline ref:       outlines/[NODE_ID].md
          Deviation from outline: [None / describe any structural change]
          New variable states discovered: [list any]
          Unresolved items: [list any]
     -->
     ```
   - Mark the corresponding task `[x]` in `tasks.md`
   - Note any newly discovered variable states or branch conditions not in the outline — add to `outlines/[NODE_ID].md` Deviations section

   **If a new unplanned node is needed** (discovered during drafting — a missing transition, required setup, etc.):
   - **STOP drafting**. Do not write the node yet.
   - Notify the user: "Drafting [NODE_ID] requires an unplanned node: [description]. Add it to `specs/flowmap.md` before drafting continues."
   - Add the new node to `specs/flowmap.md` with a `[NEEDS OUTLINE]` marker
   - Add a corresponding task entry in `tasks.md` immediately after the related task
   - Resume drafting only after both files are updated
   - **`specs/flowmap.md` is the authoritative node list. `tasks.md` must never contain nodes that are not in `flowmap.md`.**

5. **Report**: After completing the requested node(s), report:
   - Nodes drafted and their output paths in `nodes/`
   - Prose word count for each node
   - Hook blocks inserted (by type) and any Tier 2 stubs
   - Any constitution violations caught and corrected
   - Any deviations from the approved outline
   - Any `[NEEDS CLARIFICATION]` items encountered
   - Next recommended node ID
   - Suggest: "Run `speckit.checklist [NODE_ID]` to validate the drafted node."

6. **Check for extension hooks (after drafting)**: check `hooks.after_implement`.
