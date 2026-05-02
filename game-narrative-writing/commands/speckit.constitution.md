---
description: Generate the constitution (.specify/memory/constitution.md) from an approved game story brief. Configures engine target, mechanics, POV, craft rules, and content policy.
handoffs:
  - speckit.clarify: If any OQ-NNN items remain unresolved in spec.md
  - speckit.plan: When .specify/memory/constitution.md is approved, generate the plan
---

# speckit.constitution

Generate or update `.specify/memory/constitution.md` � the governing document for the entire project. Derives configuration from `spec.md`.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Optional flags:
- `--engine generic|sugarcube|ink` � override engine target (default: generic)
- `--update` � revise existing `.specify/memory/constitution.md` (preserve approved sections)

## Pre-Execution Checks

**Check for extension hooks (before constitution update)**:
- Check if `.speckit/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**Query search index for existing project context** (optional � large projects):
- If `.speckit/index/` exists, query the index before loading documents to identify which files contain relevant context:
  ```
  python scripts/python/index.py query "genre tone protagonist premise" --top 8
  python scripts/python/index.py query "world rules setting mechanics" --type spec --top 5
  python scripts/python/index.py query "theme player agency dramatic tension" --type spec --top 5
  ```
- Use returned passages as supplementary context when inferring `[GENRE]`, `[TONE]`, `[THEME]`, and `[STORY_SPECIFIC_PRINCIPLES]` from existing project files.
- If the index does not exist, skip silently and proceed with direct file loading.

**Document checks**:
1. Check if `specs/spec.md` exists. Notify if absent but proceed:
   - "No spec.md found�starting project from scratch. I'll prompt you for the core pillars (Engine, POV, Tone) manually."
2. If `specs/spec.md` exists, check for unresolved `OQ-NNN` items � if any remain, warn:
   - "Unresolved open questions exist. Run `speckit.clarify` first, or proceed with `[NEEDS CLARIFICATION]` stubs."
3. If `.specify/memory/constitution.md` exists:
   - **Stale content check**: scan it for software-development markers: `Library-First`, `TDD`, `test coverage`, `API design`, `CLI`, `dependency injection`, `microservice`. If any are found, warn the user immediately:
     > ?? **Wrong constitution detected.** This file was generated from the generic software-dev template, not the game-narrative-writing template. The existing content will produce incorrect export output and should be replaced.
     > Run with `--update` to overwrite it, or confirm below.
   - If no stale markers found and `--update` not set: ask user to confirm overwrite.

## Outline

1. **Load existing constitution** (if present): Read `.specify/memory/constitution.md`. Identify all `[NEEDS CLARIFICATION]` and `[PLACEHOLDER]` tokens that still require resolution.

2. **Derive constitution configuration from context**:

   - **Spec pre-fill**: if `specs/spec.md` exists, read its logline, premise, and world rules.
   - **Series pre-fill**: if `specs/series-bible.md` exists, read its `## Series Parameters` table and silently pre-fill the following fields as defaults � do not ask the user for these from scratch; instead confirm or offer to override:
     - `[GENRE]` ? Series Parameters `Genre`
     - `[TARGET_AUDIENCE]` ? Series Parameters `Target audience`
     - `[TONE]` ? Series Parameters `Series tone`
     Emit: `?? Series bible detected � genre, audience, and tone pre-filled from specs/series-bible.md. Confirm or override below.`

   **Interactive mode** (if `spec.md` is absent or incomplete):
   Work through each field in order, gathering values from user input or direct questions:

   - **Engine target**: twine/sugarcube, ink, renpy, ags, escoria, unity, generic — infer from narrative design doc, ask if absent:
     > "Which engine target?
     > (a) **twine/sugarcube** — Twee 3 / Sugarcube 2 macros
     > (b) **ink** — Inkle's scripting language
     > (c) **renpy** — Python-based visual novel engine (work in progress)
     > (d) **ags** — Adventure Game Studio script (work in progress)
     > (e) **escoria** — Godot-based point-and-click (.esc) (work in progress)
     > (f) **unity** — C# stubs / Yarn Spinner format
     (work in progress)
     > (g) **generic** — Annotated Markdown (engine-agnostic prose with hook blocks)"

   - **Player perspective**: derive from narrative design doc; ask if absent:
     > "What is the player character's perspective?
     > (a) **second-person** � classic IF 'You enter the room...'
     > (b) **third-person** � named protagonist 'Alex steps forward...'
     > (c) **first-person** � immersive 'I reach for the door...'
     > (d) **switching** � perspective changes by scene or choice"
     - If **switching**: declare `pov_variable` name (to be registered in `variables.md`)

   - **Tone**: derive from narrative design doc; ask if not set:
     > "What is the emotional register of this game?
     > (a) **warm-dark** � emotional intimacy with genuine threat and consequence
     > (b) **dry-ironic** � deadpan distance, situational irony, understatement
     > (c) **bleak-unflinching** � no comfort; consequences are final
     > (d) **elevated-lyrical** � prose beauty foregrounded; intensity through image
     > (e) **neutral-controlled** � flat affect, reader infers; Flesch target 60�70"

   - **Prose style** � ask the user:
     > "Which prose style fits this game?
     > (a) **author-sample** – paste a key scene and I'll extract your voice markers
     > (b) **humanized-ai** – use the built-in craft ruleset for engaging interactive fiction"
     - If `author-sample`: prompt for 300–1500 words of representative game text (NPC dialogue, narration, or scene description). Extract style markers (POV, tense, rhythm, vocabulary register, description density, tone, dialogue style, anti-patterns). Confirm extracted values with the user.
     - If `humanized-ai`: confirm built-in ruleset is active. Then determine the **Prose Profile** — ask if not already set:

       > "Which prose profile fits this game?
       > (a) **dialogue-heavy** — NPC banter dominates; minimal description
       > (b) **environmental** — world-building balances with dialogue
       > (c) **action-forward** — choices drive pace; description is functional
       > (d) **atmospheric** — setting and mood establish tone; dialogue is sparse
       > (e) **minimalist** — bare-bones prose; every word earns its place"

       Set `[PROSE_PROFILE]` to the chosen value. The profile tunes how the universal craft principles (Sections II–V in craft-rules.md) are weighted — it does not relax or override any universal rule.

   - **Target audience / rating**: ask if not set:
     > "Who is the primary audience?
     > (a) **adult** � no content ceiling; violence, mature themes unrestricted
     > (b) **new-adult** � 18�25; mature themes permitted; extreme graphic content discouraged
     > (c) **young-adult** � 13�18; limited sexual content; violence permitted with consequence
     > (d) **teen** � 13+; equivalent to PEGI 12 / ESRB T; no sexual content
     > (e) **all-ages** � family-friendly; equivalent to PEGI 7 / ESRB E10+"

   - **Approximate node count and act structure**: infer from narrative design doc; confirm with user.

   - **Active mechanics**: survey narrative design doc for all referenced mechanic types ? identify Tier 1 (core loop) and Tier 2 (optional/conditional) mechanics.

   - **`[LANGUAGE]`** � BCP-47 code. Ask if not already set:
     > "What language is this game written in? (e.g. en, de, fr, es, it, pt, nl, ja, zh, fi, hu, tr)"

   - **`[STUDIO_NAME]`** / **`[AUTHOR_NAME]`** � publishing credit. Ask if not set.

   - **`[COPYRIGHT]`** � ask the user to choose a format or enter custom text:
     > "Which copyright notice?
     > (a) � [YEAR] [STUDIO_NAME]. All rights reserved.
     > (b) � [YEAR] [STUDIO_NAME]. Licensed under CC BY 4.0.
     > (c) CC0 � public domain dedication
     > (d) Custom � enter your own text
     > (e) Skip � omit from export metadata"

   - **Project-specific craft rules** (`[STORY_SPECIFIC_PRINCIPLES]`): 3�5 rules unique to this game's voice and design.

   - **Prohibited phrases**: project-specific clich�s or banned constructions to add to the Anti-AI filter.

3. **Configure constitution.md**:

   **MANDATORY � read the template first**:
   - Read the file `.specify/presets/game-narrative-writing/templates/constitution-template.md` in full before writing anything.
   - The output MUST reproduce every section heading, table, and placeholder from that file � populated with the values gathered above.
   - Do **NOT** use `.specify/templates/constitution-template.md` � that is the generic software-development template and is wrong for this project.
   - Do **NOT** invent a structure from memory or training data. Use only the structure from the file you just read.

   Populate all engine target, POV, language, and version fields
   - Active Mechanics Table: list every hook type the project uses, with Tier (1/2) and config notes
     - Use `templates/mechanics-template.md` as the base for `specs/mechanics.md` � copy the relevant Tier 1 hook sections for the hooks listed in the Active Mechanics Table; leave Tier 2 stubs for any hooks declared but not Tier 1
   - Inventory config: capacity limit, item list, weight system
   - Timer config: type (turns/seconds), precision, failure condition
   - Attribute/currency config: names, ranges, starting values
   - Craft rules: confirm universal node rules (NR-001�NR-009) apply; add project-specific rules
     - NR-009: Choices must use export format `- [Label](NODE_ID) <!-- condition -->` under `## Choices` heading (required by `export.py` parse_choices())
   - Prose style rules: derive from narrative design doc tone + style mode selection
   - NPC voice guidelines: project-specific notes on dialogue consistency
   - Prohibited phrases: project-specific clichés or banned constructions
   - Content policy: based on target audience / rating

3b. **Generate `.specify/memory/craft-rules.md`**:
   - Copy `templates/craft-rules-template.md`
   - Set `[PROSE_PROFILE]` to the chosen prose profile value
   - If `STYLE_MODE` is `humanized-ai`: keep only the chosen profile's definition block under `## Profile Specifications`; remove the other four profile blocks entirely
   - If `STYLE_MODE` is `author-sample`: remove the entire `## Profile Specifications` section (profiles are irrelevant; craft rules I–V and the Universal Anti-AI Filter still apply)
   - Write the result to `.specify/memory/craft-rules.md`
   - Emit: `✓ craft-rules.md written — loaded automatically by speckit.implement, speckit.checklist, speckit.continuity.`

3c. **RAG Index System** – ask after node count is known:

   Determine approximate node count. Compare against 150 nodes to form the recommendation label.

   Ask the user:

   > "Do you want to enable the RAG semantic search index for this project?
   > It allows `speckit.implement`, `speckit.continuity`, and other commands to retrieve relevant passages from your entire project without loading all files into context.
   > *(Your target is ~[NODE_COUNT] nodes � **recommended** for projects over 150 nodes / optional for smaller projects)*
   > (a) **Yes** � initialize the index now
   > (b) **No** � skip (can be enabled later with `python scripts/python/index.py build`)"

   If the user chooses **(b)**: skip silently and continue.

   If the user chooses **(a)**:

   1. **Check if already initialized**: inspect whether `.speckit/index/chroma/` exists in the project root.
      - If it exists ? emit `?? ChromaDB index already initialized at .speckit/index/ � skipping build.` and continue.

   2. **Check if dependencies are installed** (only if not already initialized):
      Run:
      ```
      python -m pip show chromadb sentence-transformers
      ```
      - If both packages are found ? proceed to build.
      - If either is missing ? ask:
        > "ChromaDB and sentence-transformers are not installed.
        > (a) **Install to global/user site** � `python -m pip install chromadb sentence-transformers`
        > (b) **Create and use .venv** (Recommended) � creates a `.venv/` folder and installs there"
      - If the user chooses **(b)**:
        1. Run `python -m venv .venv`
        2. Activate (Windows: `.venv\Scripts\Activate.ps1`, Unix: `source .venv/bin/activate`)
        3. Run `python -m pip install chromadb sentence-transformers`
      - Else run: `python -m pip install chromadb sentence-transformers`
        - On failure ? emit: `?? Installation failed. Ensure Python is on the PATH and try running manually: python -m pip install chromadb sentence-transformers` and stop.

   3. **Build the index**:
      Run from the project root:
      ```
      python scripts/python/index.py build
      ```
      - On success ? emit: `? RAG index initialized at .speckit/index/ � semantic search is now active for all project files.`
      - On failure ? emit: `?? Index build failed. Check that Python is available and dependencies are installed. You can retry later with: python scripts/python/index.py build`

4. **Increment the semantic version**:
   - **MAJOR**: if engine target, player perspective, or narrative mode changed
   - **MINOR**: if new mechanics, craft rules, or prohibited phrases added
   - **PATCH**: typos, clarifications, minor refinements
   - Update `[GAME_BIBLE_VERSION]`, `[RATIFICATION_DATE]` (on first creation only), `[LAST_AMENDED_DATE]`

5. **Write a Sync Impact Report** as an HTML comment at the top of the file, summarizing what changed and which dependent documents are affected:
   ```html
   <!-- SYNC IMPACT: v1.0.0 ? v1.1.0
        Changed: Added 2 prohibited phrases, updated active mechanics table
        Affected templates: plan-template.md, variables-template.md
        Action required: Re-run speckit.continuity if nodes have been drafted -->
   ```

6. **Propagate changes** to dependent documents if applicable:
   - If engine target changed: note in the impact report (all export commands affected)
   - If act structure changed: flag that `specs/plan.md` should be regenerated via `speckit.plan`
   - If prohibited phrases changed: note in the impact report (drafted nodes need re-scan)
   - If player perspective changed: flag `variables.md` for `pov_variable` registration

7. **Output**
   - Create `.specify/memory/` directory if it does not already exist.
   - Create or update `.specify/memory/constitution.md`
   - Warn if Active Mechanics Table contains Tier 2 hooks: "Tier 2 hooks will export as stubs. Confirm this is acceptable."

8. **Validate the final constitution**:
   - No unresolved `[NEEDS CLARIFICATION]` tokens remain
   - `[STUDIO_NAME]` or `[AUTHOR_NAME]` is set � warn if absent
   - `[LANGUAGE]` is a valid BCP-47 code � warn if absent, default will be `en`
   - `[COPYRIGHT]` is set or explicitly skipped � info note if absent: `?? Copyright not set � dc:rights will be omitted from exports`
   - `[TONE]` is one of the 5 supported values
   - `[TARGET_AUDIENCE]` is one of the 5 supported values
   - `[ENGINE_TARGET]` is one or more of: `generic`, `sugarcube`, `ink`, `renpy`, `ags`, `escoria`, `unity`
   - If `humanized-ai` mode: `[PROSE_PROFILE]` is one of: `dialogue-heavy`, `environmental`, `action-forward`, `atmospheric`, `minimalist`
   - If `author-sample` mode: all 8 Extracted Style Markers have values
   - `[PLAYER_PERSPECTIVE]` is one of: `second-person`, `third-person`, `first-person`, `switching`
   - If `switching` perspective: `pov_variable` is declared and registered in `variables.md`
   - `[RATIFICATION_DATE]` and `[LAST_AMENDED_DATE]` are ISO format (`YYYY-MM-DD`)
   - Active Mechanics Table has at least one Tier 1 entry
   - Node rules NR-001–NR-009 are confirmed active
   - `[NARRATIVE_MODE]` is one of: `linear`, `branching`, `point-and-click`, `emergent`
   - If Series Position is non-standalone: `## Series Context` section is present and populated

9. **Report**: Summarize all resolved fields, the new version number, any remaining items requiring attention, and next steps including craft-rules.md generation.

10. **Update search index** (optional):
    - If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root.
    - This re-indexes the updated `.specify/memory/constitution.md` and `.specify/memory/craft-rules.md` so subsequent queries reflect the latest rules.
    - If the command fails or the index does not exist, skip silently.

11. **Suggest next step**: "Run `speckit.spec` to define the game idea"
