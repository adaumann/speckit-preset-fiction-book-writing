---
description: Generate the full node authoring task list (tasks.md) from the flowmap and narrative spec files. Covers all phases from spec setup through export (Phases 0–9).
handoffs:
  - label: Fix Story Structure
    agent: speckit.plan
    prompt: The flowmap is incomplete or the act structure is unclear. Please review and fix it.
    send: true
  - label: Generate Node Outlines
    agent: speckit.outline
    prompt: Begin outlining Phase 1 nodes
    send: true
  - label: Start Drafting
    agent: speckit.implement
    prompt: Begin drafting nodes in phase order
    send: true
  - label: Polish Nodes
    agent: speckit.polish
    prompt: Polish all drafted nodes to completion
    send: true
  - label: Verify Continuity
    agent: speckit.continuity
    prompt: Run continuity checks on all nodes
    send: true
  - label: Compile Story
    agent: speckit.compile
    prompt: Compile nodes to story files for each target engine
    send: true
---

# speckit.tasks

Generate or update `tasks.md` — the complete phased task list for node authoring, QA, and export.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted input:
- Nothing — generate from `specs/plan.md` and `specs/spec.md`
- `--update` — add new tasks or update status of existing tasks
- `--phase [N]` — regenerate a specific phase only

Optional flags:
- `--update` — revise existing `tasks.md` without regenerating completed tasks
- `--phase [0–9]` — scope regeneration to a single phase

## Pre-Execution Checks

**Check for extension hooks (before task generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_tasks` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:
1. Confirm `specs/plan.md` exists — tasks cannot be generated without a node graph.
2. Confirm `.specify/memory/constitution.md` exists.
3. If `tasks.md` exists and neither `--update` nor `--phase` is set: ask user to confirm overwrite.

## Outline

**Goal**: Generate `tasks.md` — a fully scoped, phased task list driven by actual flowmap and spec content, not generic placeholders.

### Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Load spec documents**: Read from `specs/`:
   - **Required**: `plan.md` (node graph, branch structure, act breakdown), `spec.md` (NPCs, variables, research gaps)
   - **Required if generating Phase 0**: `constitution.md` (mechanic schemas, world rules, ending conditions)
   - **Optional**: `characters/` profiles, `world-building.md`, `variables.md`
   - Note which optional documents are missing — affected tasks may be marked `[BLOCKED: needs <document>]`

3. **Generate Phase 0 setup tasks** from actual spec content (do NOT copy static placeholders from `tasks-template.md`):
   - Read all research gaps and `OQ-NNN` items from `spec.md`
   - Generate one research task per domain gap or open question that blocks Act 1 drafting
   - Mark parallelizable setup tasks with `[P]` where they cover independent domains
   - Use actual NPC names from the Key NPCs table for profile tasks

4. **Generate node tasks per act** from `plan.md`:
   - Count all nodes per act
   - Identify nodes that can be outlined/drafted in parallel (`[P]`) — independent branches with no causal dependency on each other
   - Identify sequentially dependent nodes — mark without `[P]`
    - **Step-Phasing**: Generate outline tasks for all nodes in the act first, followed by draft tasks for that act. This ensures the structural logic of the act is approved before prose is generated.

5. **Generate `tasks.md`**: Use `templates/tasks-template.md` as structure, fill with:
   - Correct game title and spec paths from `spec.md`
   - Actual node IDs, titles, and act groupings from `plan.md`
   - Accurate `[P]` markers where node drafts are genuinely parallelizable
   - Specific Phase 0 checkpoint items matching the actual variables, mechanics, and endings in the spec
   - Phase 7 QA tasks scoped to the node count

6. **Task generation rules**:
   - Every node in `plan.md` MUST have at least one outline task and one draft task
   - Phase 0 setup tasks are generated from actual spec content — never copied from template placeholders
   - No draft task may be `[P]` with a node it causally depends on (check branch dependencies in `plan.md`)
   - Phase 6b Polish tasks: one task per node marked `status: APPROVED` in draft/[ENGINE]/. Can be `[P]` if nodes are independent.
   - Phase 7 Continuity Verify tasks: sequential checks for dialogue, glossary, locations, NPC state, variables, series, timeline, thematic. Re-polish tasks for failures.
   - Phase 8 Compilation tasks: sequential compile for each target engine (SugarCube, Ink, Ren'Py, etc.) from themes to story files
   - Phase 9 Export tasks: sequential validation of compiled output, version tagging, release preparation
   - QA and export tasks (Phases 7–9) are always sequential, never parallel
   - If `--update` is set, only add tasks for nodes not already present — never remove completed tasks
   - Blocked tasks must carry a `[BLOCKED: reason]` note

7. **Report**: Total tasks, tasks per act, parallel vs. sequential ratio, number of unresolved OQ-NNN items gating Phase 0 checkpoint, recommended MVP scope (minimum nodes to complete Act 1).

## Phase Definitions

**Phase 0: Research & Setup**
- Research gaps and open questions (OQ-NNN) from spec.md
- Character profile completion for all Key NPCs
- World-building documentation (glossary, locations, timeline if applicable)
- Mechanic schema verification from constitution.md
- Checkpoint: All OQ-NNN items resolved or explicitly deferred; profiles, glossary, locations complete

**Phases 1–5: Narrative Structure** (per act)
- Phase 1: Outline all nodes in Act 1
- Phase 2: Draft all nodes in Act 1 (after outlines approved)
- Phase 3: Outline all nodes in Act 2
- Phase 4: Draft all nodes in Act 2 (after outlines approved)
- Phase 5: Outline and draft remaining acts (Acts 3+)
- Each phase pairs outline ? draft to ensure structural approval before prose generation
- Checkpoint per act: All node drafts reach `status: APPROVED` per checklist

**Phase 6b: Polish**
- One task per node in draft/[ENGINE]/ with `status: APPROVED`
- Tasks can be `[P]` if nodes are independent of each other
- Each node must be polished to completion: `polished: [YYYY-MM-DD]` field added
- Checkpoint: All nodes have `polished: [date]` in frontmatter; no FAIL status on polish audit

**Phase 7: Continuity Verify**
- Run `speckit.continuity --check dialogue,glossary,locations,npc,variables,series,timeline,thematic` (sequential)
- For each failed check, create revision task(s) via `speckit.revise`
- After revisions pass checklist, run `speckit.polish` again to re-polish
- Checkpoint: All continuity checks pass; nodes re-polished after any revisions

**Phase 8: Compilation**
- Generate or verify theme files (story.css for SugarCube, ink-theme-*.html for Ink)
- Compile for each target engine via `speckit.compile --engine [ENGINE]` (sequential per engine)
- Validate output structure in draft/[ENGINE]/ and story/ directories
- Checkpoint: All target engines compile without errors; draft/[ENGINE]/story.* and story/ files present

**Phase 9: Export & Release**
- Test compiled output in each engine environment (Twine player for SugarCube, Ink web player for Ink, etc.)
- Version tagging and changelog updates
- Package final distribution (playable files, theme assets, README)
- Checkpoint: All compiled versions tested playable; version tags and metadata complete

