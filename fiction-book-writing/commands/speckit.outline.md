---
description: Generate editable scene-by-scene outline files from plan.md. Authors review and approve each outline before AI drafting begins, or mark SKIP to write their own prose.
handoffs:
  - label: Start Drafting
    agent: speckit.implement
    prompt: Draft scenes from approved outlines
    send: true
  - label: Check Structure First
    agent: speckit.analyze
    prompt: Run a pre-draft structural alignment check
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- `[CHAPTER_ID]` — generate outline for a single scene (e.g. `A1.101`)
- `[CHAPTER_ID]–[CHAPTER_ID]` — generate outlines for a range (e.g. `A1.101–A1.103`)
- `all` — generate outlines for all scenes in `plan.md ## Scene Outline` that do not already have an outline file
- *(no argument)* — generate the outline for the next scene without an outline file

## Pre-Execution Checks

**Check for extension hooks (before outline generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_outline` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse `FEATURE_DIR` and available documents list.

2. **Load source documents**:
   - **Required**: `plan.md` (the `## Scene Outline` section is the authoritative source for scene content), `spec.md` (character arcs, scene beats)
   - **Required**: `.specify/memory/constitution.md` (plot structure prefix, POV rules, thematic contract)
   - **Optional**: `characters.md` and `characters/[name].md` profiles (voice signatures, micro-obsessions, arc progression table)
   - **Optional**: `locations.md` (sensory anchors, Dirt Rule options, atmosphere blocks)
   - **Optional**: `timeline.md` (timeline position, elapsed time)
   - **Optional**: `themes.md` (active motif registry — which motifs are scheduled for each phase)
   - **Optional**: `pov-structure.md` (POV schedule — which character holds this chapter)

3. **Determine target chapters**:
   - If `$ARGUMENTS` is empty: find the first chapter in `plan.md ## Scene Outline` whose `status` is `outline` (not yet started) and for which no file exists at `outlines/<CHAPTER_ID>_<ChapterName>-outline.md`
   - If `$ARGUMENTS` is a chapter ID: use that scene
   - If `$ARGUMENTS` is a range: use all scenes in that range
   - If `$ARGUMENTS` is `all`: use all scenes without an existing outline file
   - **Skip any scene that already has an outline file with `status: APPROVED` or `status: SKIP`** — never overwrite approved or skipped outlines

4. **For each target scene, generate an outline file**:

   **Output path**: `outlines/<CHAPTER_ID>_<ChapterName>-outline.md`
   Create `outlines/` directory in `FEATURE_DIR` if it does not exist.

   Use `templates/scene-outline-template.md` as the base structure. Populate each section from the available source documents:

   **Frontmatter** — pull from `plan.md ## Scene Outline` entry:
   - `chapter_id`, `chapter_name`, `pov_character`, `pov_type`, `act_phase`, `plot_structure_stage`, `timeline_position`, `setting`, `estimated_words`
   - Set `status: DRAFT`

   **Outline language**: Draft all text in the outline (opening hook, beat sequence labels, dialogue requirement notes, sensory anchor descriptions) in the language specified in `constitution.md § VII Language`. If Language is not set or not recognised, default to English.

   **Opening Hook** — derive from the plan entry's opening hook or first key beat. Write as one concrete sentence (character in motion, not in reflection). Must be specific to this scene, not generic.

   **Beat Sequence** — expand each key beat from the plan entry to a single-sentence causal step. Verify:
   - First beat enters the scene in motion (no setup paragraphs)
   - Beats follow causal order (each produces the next)
   - The final beat is off-balance (do not resolve the scene cleanly)
   - Minimum 3 beats; add an explicit pivot beat if the plan entry shows only entry + exit

   **Character Beats** — for each character present in this scene:
   - Load their arc state at this phase from `spec.md` character arc progression
   - State what they want entering the scene and what they actually get
   - For non-POV characters: state their function (obstacle, mirror, catalyst, revelation)

   **Dialogue Requirements** — map each dialogue exchange from the plan entry:
   - Do NOT write dialogue — state what must be communicated and how it must be deflected or unspoken
   - Include the word-failure moment if the plan specifies one
   - If the plan entry has no dialogue requirement: note `No dialogue required — silent scene.`

   **Sensory Anchors** — load from `locations.md` if the setting has a `LOC-NNN` entry:
   - Pull the primary sensory anchor from the Sensory Anchors table
   - Pull one Dirt Rule detail option from the location's Dirt Rule row
   - If no `locations.md` entry: derive from the plan entry's setting description and note `TBD — populate locations.md`

   **Thematic Work** — load from `themes.md` if available:
   - Identify which motif from the Motif Registry is scheduled for this scene's phase
   - Specify the delivery method (action / object / spatial relationship — never dialogue statement)
   - If `themes.md` does not exist: leave as `[TBD — create themes.md to populate]`

   **Story Bible Compliance Notes** — scan `constitution.md` for:
   - Any prohibited phrases or patterns relevant to this POV character's voice
   - POV distance rules that apply (especially for first-person-multiple or close-third)
   - Flag any tension between the plan entry's content and constitution.md principles

   **Deviations from plan.md** — default to `None`. Only populate if the outline generation process identified a discrepancy or impossible beat that requires plan.md to be updated first.

5. **Outline quality rules**:
   - Every beat must be one sentence — no prose, no dialogue fragments
   - "Opening Hook" and "Exit beat" must be the most concrete, specific items in the file
   - If a `[NEEDS CLARIFICATION]` marker is present in the plan entry, propagate it into the outline and do not invent a resolution — the author must resolve it
   - If the plan entry is incomplete (missing key beats, no closing beat), generate what can be derived and mark gaps with `[NEEDS CLARIFICATION: <description>]`
   - The outline is a brief, not a draft — no narrative prose, no atmospheric description, no named emotions

6. **Report**: List all outline files created with their output paths and `status: DRAFT`. Include a summary line per scene: `[CHAPTER_ID] [ChapterName] — [N] beats, POV: [name], [word estimate] words`. Flag any scenes where `[NEEDS CLARIFICATION]` markers were propagated. Remind the author to:
   - Review each outline file
   - Edit beats, sensory anchors, and dialogue requirements as needed
   - Change `status: DRAFT` → `status: APPROVED` when satisfied, or `status: SKIP` to write the chapter themselves
   - Run `/speckit.implement` once outlines are approved

7. **Check for extension hooks** (after generation): check `hooks.after_outline`.
