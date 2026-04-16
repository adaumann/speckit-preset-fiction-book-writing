---
description: Generate scene-by-scene writing tasks ordered by act and character arc, with research phase, critical checkpoint, and polish pass.
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
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
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

1. **Setup**: Run `{SCRIPT}` from repo root and parse `FEATURE_DIR` and available documents list.

2. **Load story documents**: Read from `FEATURE_DIR`:
   - **Required**: `plan.md` (story structure, chosen plot structure, act breakdown), `spec.md` (character arcs with priorities)
   - **Optional**: `characters.md` (index) and `characters/` profiles (voice signatures, micro-obsessions), `world-building.md`, `timeline.md`, `research.md`
   - Note which optional documents are missing — some tasks may be marked `[BLOCKED: needs <document>]`
   - Read `constitution.md ## X. Audiobook Production` and extract `OUTPUT_MODE` (`book`, `audiobook`, or `both`). If absent or `[NEEDS CLARIFICATION]`, treat as `book`.

3. **Execute task generation workflow**:
   - Extract the chosen plot structure from `plan.md`
   - Extract all character arcs from `spec.md` with their priorities (P1, P2, P3)
   - Map each scene beat from `spec.md` Key Scenes to a phase/act slot
   - For each phase: identify which scenes can be drafted in parallel (`[P]`) vs. sequentially (dependency on prior scene's outcome)
   - Identify the critical checkpoint location (after Phase 1 research is complete, before any drafting begins)
   - Generate polish pass tasks from constitution.md compliance requirements

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

6. **Task generation rules**:
   - Every scene beat from spec.md Key Scenes MUST have at least one draft task
   - Research tasks (Phase 1) are generated from `research.md` R-items — never copied from tasks-template.md boilerplate
   - Research tasks precede all drafting tasks
   - No drafting task may be `[P]` with a scene that it causally depends on
   - Polish tasks are always sequential, never parallel
   - Audiodraft tasks are only generated when `OUTPUT_MODE` is `audiobook` or `both` — never when `OUTPUT_MODE` is `book`
   - Each audiodraft task is always paired with its prose draft task and is never `[P]` (it depends on the prose draft being complete)
   - Total task count, arc distribution, parallel opportunity count, and audiodraft task count (if applicable) are reported in the task file header

7. **Report**: Total tasks, tasks per arc (P1/P2/P3), parallel vs. sequential ratio, number of story-specific research tasks generated, recommended MVP scope (minimum scenes to complete Act I).
