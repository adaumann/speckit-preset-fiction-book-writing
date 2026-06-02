---
description: Generate scene-by-scene writing tasks ordered by act and character arc, with research phase, critical checkpoint, polish pass, and optional audiobook/illustration tasks.
handoffs:
  - label: Analyze Structure
    agent: speckit.analyze
    prompt: Run a pre-draft structural alignment check
    send: true
  - label: Generate Scene Outlines
    agent: speckit.outline
    prompt: Generate editable scene outlines for author review before drafting
    send: true
  - label: Start Drafting
    agent: speckit.implement
    prompt: Begin drafting scenes in phase order
    send: true
  - label: Generate Illustrations
    agent: speckit.illustrate
    prompt: Generate illustration briefs for drafted chapters
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before task generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_tasks` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Outline
## Goal

Generate a complete, ordered list of **scene‑by‑scene writing tasks** that drives the drafting process. The tasks include research, character profile creation, world‑building, timeline work, prose drafting, optional audiobook drafting, optional illustration generation, and final polish passes. They are grouped by phases (research, drafting, polish) and respect character‑arc priorities and parallelism constraints.

## Command

When the `speckit.tasks` command is invoked, the LLM should:
1. **Read** any user arguments (`$ARGUMENTS`).
2. **Perform** pre‑execution checks (extension hooks).
3. **Resolve** the feature directory (`FEATURE_DIR`) by locating the first sub‑directory under `specs/` that contains project files (fallback to the project root).
4. **Load** required story documents (`plan.md`, `spec.md`) and optional supporting files (`characters.md`, character profiles, `world-building.md`, `timeline.md`, `research.md`).
5. **Extract** plot structure, character arcs (with priorities P1‑P3), and scene beats from the loaded documents.
6. **Generate** tasks following the detailed workflow:
  - Create Phase 1 research tasks from actual `research.md` R‑items (or a placeholder if missing).
  - Create profile, world‑building, and timeline tasks using real character and setting names.
  - Map each scene beat to a drafting task, marking parallelizable tasks with `[P]` only when scenes are truly independent.
  - Insert a critical checkpoint task after Phase 1 research and before any drafting.
  - Add polish pass tasks based on constitution compliance requirements.
  - If the story bible specifies `OUTPUT_MODE` of `audiobook` or `both`, generate corresponding audiobook setup, audiodraft, and polish tasks as described.
  - If the story bible specifies `Illustrations: yes` in § XI, generate corresponding illustration setup, illustration brief, and polish tasks as described.
7. **Write** the resulting `tasks.md` using `templates/tasks-template.md`, filling in the correct story title, feature directory, scene names, character‑arc labels, file paths, and task statistics (total tasks, arc distribution, parallel vs sequential counts, audiobook task count, illustration task count).
8. **Report** a summary header with task counts and any remaining `[BLOCKED]` or `[NEEDS CLARIFICATION]` markers.
9. **Process** any post‑task extension hooks.

The LLM must follow this sequence exactly and must not modify any files outside the newly generated `tasks.md`.
1. **Setup**: Resolve `FEATURE_DIR` by reading the project structure: the first subdirectory inside `specs/` that contains project files. Fall back to project root if `specs/` does not exist.

2. **Load story documents**: Read from `FEATURE_DIR`:
   - **Required**: `plan.md` (story structure, chosen plot structure, act breakdown), `spec.md` (character arcs with priorities)
   - **Optional**: `characters.md` (index) and `characters/` profiles (voice signatures, micro-obsessions), `world-building.md`, `timeline.md`, `research.md`
   - Note which optional documents are missing — some tasks may be marked `[BLOCKED: needs <document>]`
   - Read `constitution.md ## X. Audiobook Production` and extract `OUTPUT_MODE` (`book`, `audiobook`, or `both`). If absent or `[NEEDS CLARIFICATION]`, treat as `book`.
   - Read `constitution.md ## XI. Illustration Guidelines` and extract `Illustrations` (`yes` or `no`) and `Illustration Automation` (`per-chapter` or `manual`). If absent or `[NEEDS CLARIFICATION]`, treat as `no`.

3. **Execute task generation workflow**:
   - Extract the chosen plot structure from `plan.md`
   - Extract all character arcs from `spec.md` with their priorities (P1, P2, P3)
   - Map each scene beat from `spec.md` Key Scenes to a phase/act slot
   - For each phase: identify which scenes can be drafted in parallel (`[P]`) vs. sequentially (dependency on prior scene's outcome)
   - Identify the critical checkpoint location (after Phase 1 research is complete, before any drafting begins)
   - Generate polish pass tasks from constitution.md compliance requirements
   - For each task, note which supporting documents are needed (for implement to use RAG instead of loading all files)

4. **Generate Phase 1 research tasks from `research.md`** (do NOT use the static T001–T006 from `tasks-template.md`):
   - If `research.md` exists in `FEATURE_DIR`:
     - Read all R-items with `Status: OPEN` or `Status: IN PROGRESS`
     - Generate one task per R-item: `TXXX Research: [R-item topic] → resolve R[NNN] in research.md`
     - Prioritize tasks matching Authenticity Flags first (highest risk items come first)
     - Mark parallelizable research tasks with `[P]` where they cover independent domains
   - If `research.md` does not exist yet:
     - Generate a single task: `T001 Research: Generate research.md from story brief — identify all domain/historical/world knowledge gaps before drafting`
   - Always generate the standard non-research Phase 1 tasks (character profiles, world-building, timeline) but use the actual character names from `spec.md` rather than generic placeholders:
     - `T___ [P] Profile: Write full character profile — [CHARACTER_NAME] (wound, arc, voice signature, micro-obsession, contradiction) (characters/[name].md, register in characters.md)`
     - `T___ World: Document world rules, locations, sensory anchors — [WORLD/SETTING NAME] (world-building.md)`
     - `T___ Timeline: Lock chronological event order including backstory — [ERA/PERIOD] (timeline.md)`

5. **Generate `tasks.md`**: Use `templates/tasks-template.md` as structure, fill with:
   - Correct story title and feature directory from `plan.md`
   - Actual scene names from spec.md mapped to their phases
   - Correct `[CA-n]` labels matching the character arcs (CA-1 = P1 protagonist)
   - Accurate `[P]` markers where chapter drafts are genuinely parallelizable (different POV characters in non-intersecting scenes)
   - Output file paths: `draft/{PREFIX}{phase}.{beat_number}_{ShortName}.md` — using the structure-aware prefix convention from the scene outline in `plan.md` (PREFIX from `constitution.md`: `A` three-act, `JO` heros-journey, `SC` save-the-cat, etc.)
   - Example output paths: `draft/A1.101_Awakening.md`, `draft/JO3.201_SupremeOrdeal.md`
   - Phase checkpoints drawn from story bible compliance requirements

5b. **Generate audiobook tasks** (only when `OUTPUT_MODE` is `audiobook` or `both`):
   - Add a **Phase 1 audiobook setup block** (before the critical checkpoint) with these tasks:
     - `T___ [P] Audiobook: Configure narrator and character voice IDs (SSML name / ElevenLabs voice ID) → update constitution.md ## X`
     - `T___ [P] Audiobook: Populate Pronunciation Lexicon for invented/foreign/unusual words → update constitution.md ## X`
     - If `OUTPUT_MODE` is `both`: add `T___ [P] Audiobook: Configure ElevenLabs voice IDs and upload lexicon.pls → update constitution.md ## X`
   - For **every prose draft task** in every phase, insert a paired audiodraft task immediately after it:
     - Format: `T___ [CA-n] Audiodraft: Generate SSML draft — [SCENE_SHORT_NAME] → audiodraft/{CHAPTER_ID}_{ShortName}.md`
     - The audiodraft task is sequential (no `[P]` marker) and depends on the prose draft task completing first
     - Output path mirrors prose path but uses `audiodraft/` directory: `audiodraft/A1.101_Opening.md`
   - Add an **audiobook polish task** in the Polish Pass phase:
     - `T___ Audiodraft: Review all SSML files for pronunciation, break timing, and delivery hints against constitution.md ## X`
   - Update the task statistics header to include: `Audiodraft Tasks: NN`

5c. **Generate illustration tasks** (only when `Illustrations` is `yes` in constitution.md § XI):
   - Add a **Phase 1 illustration setup block** (before the critical checkpoint) with this task:
     - `T___ [P] Illustration: Configure illustration defaults (style, color range, aspect ratio) → update constitution.md § XI`
   - For **every prose draft task** in every phase, insert a paired illustration task immediately after it:
     - Format: `T___ Illustration: Generate illustration brief — [SCENE_SHORT_NAME] → illustrations/{CHAPTER_ID}-brief.md`
     - The illustration task is sequential (no `[P]` marker) and depends on the prose draft task completing first
     - Output path: `illustrations/{CHAPTER_ID}-brief.md` (e.g., `illustrations/A1.101_Opening-brief.md`)
     - If `Illustration Automation` is `per-chapter`: add `T___ [P] Illustration: Generate PNG placeholder → illustrations/{CHAPTER_ID}.png`
   - Add an **illustration polish task** in the Polish Pass phase:
     - `T___ Illustration: Review all illustration briefs for visual consistency against constitution.md § XI`
   - Update the task statistics header to include: `Illustration Tasks: NN`

6. **Task generation rules**:
   - Every scene beat from spec.md Key Scenes MUST have at least one draft task
   - Research tasks (Phase 1) are generated from `research.md` R-items — never copied from tasks-template.md boilerplate
   - Research tasks precede all drafting tasks
   - No drafting task may be `[P]` with a scene that it causally depends on
   - Polish tasks are always sequential, never parallel
   - Audiodraft tasks are only generated when `OUTPUT_MODE` is `audiobook` or `both` — never when `OUTPUT_MODE` is `book`
   - Each audiodraft task is always paired with its prose draft task and is never `[P]` (it depends on the prose draft being complete)
   - Illustration tasks are only generated when `Illustrations` is `yes` in constitution.md § XI
   - Each illustration task is always paired with its prose draft task and is never `[P]` (it depends on the prose draft being complete)
   - If `Illustration Automation` is `per-chapter`, add a parallel PNG placeholder task after each illustration brief task
   - Total task count, arc distribution, parallel opportunity count, audiodraft task count (if applicable), and illustration task count (if applicable) are reported in the task file header

7. **Report**: Total tasks, tasks per arc (P1/P2/P3), parallel vs. sequential ratio, number of story-specific research tasks generated, number of illustration tasks generated (if applicable), recommended MVP scope (minimum scenes to complete Act I).

