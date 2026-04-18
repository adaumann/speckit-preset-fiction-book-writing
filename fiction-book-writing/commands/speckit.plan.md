---
description: Create the story structure from the brief and story bible — act/phase breakdown, chapter map, and supporting documents.
handoffs:
  - label: Create Writing Tasks
    agent: speckit.tasks
    prompt: Break the story structure into scene-by-scene writing tasks
    send: true
  - label: Create Scene Checklist
    agent: speckit.checklist
    prompt: Create a quality checklist for the following scene or act...
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before story structure planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_plan` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for `FEATURE_SPEC`, `IMPL_PLAN`, `SPECS_DIR`, `BRANCH`. Load the `plan-template.md` already copied to `IMPL_PLAN`.

2. **Load context**: Read `FEATURE_SPEC` (story brief) and `.specify/memory/constitution.md` (story bible).

3. **Execute story structure workflow** — follow the structure in `IMPL_PLAN`:

   **Fill Narrative Parameters**:
   - Extract genre, POV strategy, tense, word count target, audience, series position, tone from spec.md and constitution.md
   - Identify chosen plot structure from constitution.md. If not set, ask the user to choose from: `three-act`, `heros-journey`, `freytag`, `save-the-cat`, `story-circle`, `kishotenketsu`, `five-act`
   - Mark unknowns as `[NEEDS CLARIFICATION]`

   **Story Bible Check**:
   - Evaluate all gates in the Story Bible Check table
   - Mark each ✅ PASS, ⚠️ NEEDS WORK, or ❌ VIOLATION
   - A ❌ VIOLATION blocks Phase 0 unless the user provides explicit justification — document it in the Justified Violations table
   - If style mode is not set in constitution.md, pause and ask: "author-sample or humanized-ai?"

   **Phase 0 — Supporting Documents**:

   > **Pre-fill rule**: Every supporting document MUST be written with actual story-specific content inferred from `spec.md` and `constitution.md`. Do NOT produce bare template copies. Replace every `[placeholder]` marker with real content. Only write `[NEEDS CLARIFICATION: reason]` when a field genuinely cannot be inferred from available information. The output must be immediately editable by the writer — not a blank scaffold.

   - Generate `research.md`: identify all world/domain knowledge gaps that must be resolved before drafting (historical accuracy, world rules, technical domains)
   - Generate character profiles: one file per major character at `characters/[character-name].md` using `characters-template.md` (use the character's name in lowercase-kebab-case as the filename, e.g., `characters/theresa-solis.md`). For each character, populate all nine sections:
     - **I. Core Identity**: dominant trait, strength, flaw, drive, fear, background foundation, internal arc (wound / want / need / transformation)
     - **II. Speech Patterns & Voice**: vocabulary register, recurring word clusters, intensifiers, contractions, example vocabulary pool, dialogue style (directness, power dynamic, deflection strategy, under-pressure behavior), 3 sample dialogue exchanges with tone + subtext
     - **III. Internal Monologue**: cognitive mode, blind spot, self-deception pattern, obsessive loop, 3 voice examples (discovery / conflict / decision)
     - **IV. Physical Expression**: micro-obsession (must recur and escalate), stress tell, comfort behavior, authority posture, touch pattern, signature appearance detail
     - **V. Emotional Landscape**: 4–6 primary emotions ranked by intensity with triggers, visible behaviors, and what each masks; expression mechanism; overflow and recovery patterns; 2+ moments of real doubt
     - **VI. Relationships**: one entry per significant relationship — communication pattern, subtext (what neither says directly), dynamic (the repeating loop), trigger points, arc
     - **VII. Scene Guidance**: scenes this character drives, sensory signature, emotional arc progression table across story phases
     - **VIII. Verbal Tics**: repeated phrases with their signaled states, speech pattern under stress, the sentence they never say aloud
     - **IX. Summary for Writers**: core challenge, default tone, variance points, Voice Homogeneity Test sentence, success indicator
   - Mark any field that cannot be completed without user input as `[NEEDS CLARIFICATION]`; do not invent details that could contradict spec.md
   - Generate `characters.md` as an index using `characters-index-template.md`: register every character file, populate the Voice Homogeneity Test, Arc Progression Summary, and Relationship Map
   - Generate `world-building.md`: world rules, internal logic constraints, faction rules, and system-level details too broad for individual location entries
   - Generate `glossary.md` from `glossary-template.md`: seed with all invented terms and proper nouns already present in `spec.md` and `constitution.md` — character names (with all variant forms), place names, faction names, invented vocabulary, and any story-specific usage rules. Add one entry per term; mark fields that require more draft context as `[NEEDS CLARIFICATION]`. Terms coined during drafting are added by the writer directly.
   - Generate `relationships.md` from `relationships-template.md` if `spec.md` has any named character relationships (any character profile entry has a relationship in Section VI, or `spec.md` defines Key Relationship Arcs): create one `REL-NNN` block per significant pair. Populate the Relationship Brief from `spec.md` Key Relationship Arcs and `characters/` Section VI entries; fill the Arc Beat Sheet with beat IDs from the Phase 1 structure map (rows may have empty Chapter IDs until Phase 3); pre-fill the Phase Tracker rows from the act structure in `plan.md`, leaving evidence columns blank. If no named relationships are defined, skip and note: `relationships.md not generated — no relationship arcs found in spec.md.`
   - Generate `subplots.md` from `subplots-template.md` if `spec.md` has any P2 or P3 arcs: create one `SP-NNN` block per non-P1 arc. Populate the Subplot Brief from `spec.md` character arc entries; fill the Subplot Beat Sheet with beat IDs from the Phase 1 structure map (rows may have empty Chapter IDs until Phase 3); pre-fill the Convergence Map skeleton with all chapter IDs from the Scene Outline, leaving arc presence columns blank. Leave the Arc Absence Log empty — populated by `speckit.analyze`. If all arcs are P1 (no subplots), skip this document and note: `subplots.md not generated — no P2/P3 arcs in spec.md.`
   - Generate `locations.md` from `locations-template.md`: one `LOC-NNN` block per named location that appears in the Scene Outline. For each block, populate: Physical Profile, Sensory Anchors (primary anchor as a direct prose fragment), Dirt Rule details (≥2 options), Atmosphere by Time table rows for the time(s) the location appears, Character Relationships for POV characters who enter it, Scene Guidance (what narrative functions it supports and what it cannot support). Leave State Log empty — rows are added as scenes are drafted. Transitional Spaces section: one paragraph per unnamed pass-through location.
   - Generate `themes.md` from `themes-template.md`: populate Thematic Core (Theme + Dramatic Question) from `constitution.md`; register at least the 2–3 most structurally important motifs identified in `spec.md` Key Scenes and Plot Requirements; skeleton-fill the Thematic Arc by Chapter table from the beat sheet (one row per chapter, "Expected thematic work" column filled with a one-sentence note, status = `planned`). Mark anything that cannot be inferred as `[NEEDS CLARIFICATION]`.
   - Generate `timeline.md`: chronological event map (fabula) including backstory events
   - If non-linear structure: fill the Syuzhet — Narrative Order section in `timeline.md`
   - **Series bible** (non-standalone books only): read `Series Position` from `spec.md`.
     - If the value is anything other than `standalone` (e.g., `book-1`, `book-2`, `series-entry`):
       - Check whether `series/series-bible.md` already exists.
       - If it **does not exist**: create `series/` directory and generate a skeleton `series/series-bible.md` from `series-bible-template.md`. Populate what can be inferred from `spec.md` and `constitution.md` (series title, world rules already established, named entities, the current book's entry in the Books in Series table, and the dramatic question if stated). Leave all fields that require information from future books as `[TBD]`. Emit a notice: `⚠️ series/series-bible.md created — review [TBD] entries before drafting Book 2+.`
       - If it **already exists**: load it and verify the current book has an entry in the Books in Series table. If missing, add the row. Check the Known Contradictions table; if any rows with `status: OPEN` reference this book, emit a warning listing each `SX-NNN` code.
     - If the value is `standalone`: skip this step entirely.

   **Phase 1 — Structure Map**:
   - Fill the act/phase breakdown appropriate to the chosen plot structure (use the correct commented-out block in plan-template.md)
   - Map each scene beat from spec.md to a phase/act slot
   - Identify gaps (phases with no scene beats mapped) and add `[NEEDS SCENE]` notes
   - Fill the Open Narrative Threads table from spec.md Chekhov Items

   **Phase 1 — Agent Context Update**:
   - Run the agent script to update the story context file

   **Re-evaluate Story Bible Check** after Phase 1 is complete.

   **Phase 2 — Plot Beat Sheet**:
   Generate the full beat sheet in the `## Plot Beat Sheet` section of `IMPL_PLAN`.

   **Beat ID prefix table** (read plot structure from `constitution.md`):

   | Plot structure | Prefix | Example IDs |
   |---|---|---|
   | three-act | `A{n}` | `A1.101`, `A2.201`, `A3.301` |
   | heros-journey | `JO{n}` | `JO1.101` … `JO8.801` |
   | save-the-cat | `SC{n}` | `SC1.101` … `SC5.501` |
   | kishotenketsu | `KT{n}` | `KT1.101` … `KT4.401` |
   | freytag | `FT{n}` | `FT1.101` … `FT5.501` |
   | story-circle | `SL{n}` | `SL1.101` … `SL8.801` |
   | five-act | `FA{n}` | `FA1.101` … `FA5.501` |
   | generic | `P{n}` | `P1.101`, `P2.201` |

   Format: `{PREFIX}{phase_digit}.{sequential_3digit}` — prefix is fixed for the whole project.
   Insertion beats use letter suffix: `JO3.201b` between `JO3.201` and `JO3.202`.

   For each beat:
   - Assign a beat ID using the structure-aware prefix from the table above (e.g., `A1.101` for three-act, `JO1.101` for Hero's Journey)
   - Assign a short name (2–4 words, PascalCase, e.g., `Awakening`, `BetrayalRevealed`, `FinalReckoning`)
   - Fill all 14 fields: estimated length, chapters count, act/phase, plot structure stage, timeline focus, world focus, thematic focus, characters focus, key decisions, key elements, scene structure, emotional beats, character movements, critical constraints, activities, trigger, discoveries, closing
   - Estimated length guidance:
     - Opening/closing beats: 1,500–2,500 words
     - Action/confrontation beats: 2,000–4,000 words
     - Interiority/transition beats: 1,000–2,000 words
   - Distribute word count targets across beats so total aligns with `[WORD_COUNT_TARGET]` from Narrative Parameters
   - Every scene beat from `spec.md` Key Scenes must appear in at least one beat
   - Every Plot Requirement (`PR-NNN`) from `spec.md` must be assigned to a beat

   **Phase 3 — Scene Outline**:
   Generate the full scene outline in the `## Scene Outline` section of `IMPL_PLAN`.
   For each chapter within each beat:
   - Assign the chapter ID using the structure-aware prefix: `{PREFIX}{phase}.{beat_number}_{ShortName}` (e.g., `A1.101_Awakening` for three-act, `JO3.201_SupremeOrdeal` for Hero's Journey)
   - Note the draft file path: `draft/{CHAPTER_ID}.md`
   - Fill all fields: POV (character + POV type), setting (location + time + atmosphere anchor), timeline position, estimated length, act/phase, status (= `outline`)
   - Write: opening hook (sensory, not summary), key beats (3–6 micro-events in causal order), character beats (internal POV change + visible secondary changes), dialogue requirements (each critical exchange: participants / subtext / oblique pattern), sensory details (≥1 non-visual, include Dirt Rule imperfection), thematic work (how theme is carried without being stated), closing beat (off-balance, what has irreversibly changed)
   - If a beat spans multiple chapters, give each chapter its own distinct entry with non-overlapping key beats

4. **Stop and report**: Command ends after Phase 3. Report: `IMPL_PLAN` path, total beats generated, total chapters outlined, word count distribution across acts, any remaining `[NEEDS CLARIFICATION]` markers, open threads count.

5. **Check for extension hooks** (after planning): check `hooks.after_plan` and process as standard hook block.
