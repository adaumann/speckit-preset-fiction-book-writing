---
description: Create or update the story bible (constitution) by selecting a style mode, choosing a plot structure, defining craft principles, and automatically propagating these settings to all dependent templates. This command prepares the core metadata that drives subsequent speckit commands.
handoffs:
  - label: Create Story Brief
    agent: speckit.specify
    prompt: Create a story brief for...
scripts:
  sh: scripts/bash/setup-plan.sh
  ps: scripts/powershell/setup-plan.ps1

## Goal

Create or update the central **Story Bible** (`.specify/memory/constitution.md`). The command:
1. Determines the story's **style mode** (author‑sample or humanized‑AI).
2. Selects a **plot structure** and defines core **craft principles**.
3. Populates or amends the constitution file with these values.
4. Propagates any changes to dependent templates (e.g., `craft‑rules.md`, export settings).

All subsequent `speckit.*` commands rely on the data produced here.

## Command

When the `speckit.constitution` command is run, the LLM should:
1. **Read** any user‑provided arguments (`$ARGUMENTS`).
2. **Perform** the pre‑execution checks (extension hooks, optional search‑index queries).
3. **Interact** with the user only for information that cannot be inferred (style mode, prose profile, author name, copyright, language, plot structure, dramatic question, theme, tone, target audience, etc.).
4. **Create or update** the file `.specify/memory/constitution.md` with the collected values, replacing all `[NEEDS CLARIFICATION]` and `[PLACEHOLDER]` tokens.
5. **Generate** the impact report and propagate changes to dependent templates as described in the Outline.
6. **Exit** without modifying any other files.

The LLM must follow this flow exactly and avoid performing any actions outside the scope of the command.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before story bible update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**Query search index for existing project context** (optional — large projects):
- If `.specify/index/` exists, query the index before loading documents to identify which files contain relevant context for constitution fields:
  ```
  python .specify/presets/fiction-book-writing/scripts/python/index.py query "genre tone protagonist arc" --top 8
  python .specify/presets/fiction-book-writing/scripts/python/index.py query "world rules setting premise" --type spec --top 5
  python .specify/presets/fiction-book-writing/scripts/python/index.py query "theme dramatic question" --type spec --top 5
  ```
- Use returned passages as supplementary context when inferring `[GENRE]`, `[TONE]`, `[THEME]`, `[DRAMATIC_QUESTION]`, and `[STORY_SPECIFIC_PRINCIPLES]` from existing project files.
- This is especially useful when `spec.md` is large or when characters/world-building files already contain implicit constitutional constraints.
- If the index does not exist, skip silently and proceed with direct file loading.

## Outline

**Goal**: Create or update `.specify/memory/constitution.md` (the Story Bible) from user input or inference from existing project files.

### Execution steps

1. **Load existing constitution** (if present): Read `.specify/memory/constitution.md`. Identify all `[NEEDS CLARIFICATION]` and `[PLACEHOLDER]` tokens that still require resolution.

2. **Determine style mode** — ask the user if not already set:

   > "Which style mode do you want for this story?
   > (a) **author-sample** — paste a key chapter/passage and I'll extract your voice markers
   > (b) **humanized-ai** — use the built-in craft ruleset for commercially viable fiction that avoids AI clichés"

   - If `author-sample`: prompt the user to paste 500–2000 words of their own prose. Extract the 8 style markers (POV, tense, rhythm, vocabulary register, sensory density, tone, dialogue style, anti-patterns). Write them into the Extracted Style Markers table. Confirm the extracted values with the user.
   - If `humanized-ai`: confirm the built-in ruleset is active. Then determine the **Prose Profile** — ask if not already set:

     > "Which prose profile fits this story?
     > (a) **commercial** — balanced pace, moderate interiority, alternating rhythm (general fiction, romance, fantasy)
     > (b) **literary** — deep interiority, high sensory texture, reflection-forward (literary fiction, character studies)
     > (c) **thriller** — variable sentence rhythm (short for action, longer for reflection), interiority through physical sensation and systems-thinking (thrillers, crime, horror)
     > (d) **atmospheric** — maximum sensory density, slow burn, environment as plot engine (gothic, horror, weird fiction)
     > (e) **dark-realist** — clipped declarative prose, cold interiority, consequence-forward (noir, social realism, gritty literary)"

     Set `[PROSE_PROFILE]` to the chosen value. The profile tunes how the universal craft principles (Sections II–VI in craft-rules.md) are weighted — it does not relax or override any universal rule.

     Ask if there are any additional prohibited phrases to add to the Anti-AI Filter for this specific story/genre (beyond the profile's built-in additions).

3. **Fill the Story Bible fields** — work through each `[NEEDS CLARIFICATION]` token. Gather values from:
   - User input in `$ARGUMENTS`
   - Inference from existing `spec.md` if present
   - Direct questions to the user (ask only what cannot be inferred)

   Fields to resolve in order:
   - **Series pre-fill** (before asking any field): if `series/series-bible.md` exists, read its `## Series Parameters` table and silently pre-fill the following fields as defaults — do not ask the user for these from scratch; instead confirm or offer to override:
     - `[GENRE]` ← Series Parameters `Genre`
     - `[TARGET_AUDIENCE]` ← Series Parameters `Target audience`
     - `[POV_STRATEGY]` ← Series Parameters `Series POV strategy`
     - `[TENSE]` ← Series Parameters `Series tense`
     Emit: `ℹ️ Series bible detected — genre, audience, POV strategy, and tense pre-filled from series/series-bible.md. Confirm or override below.`
     Per-book overrides are valid; any variance will be logged in the Series Variance Log.
   - `[AUTHOR_NAME]` — the publishing byline (used by `speckit.cover`, `speckit.query`, and `speckit.export`). Ask if not already set.
   - `[COPYRIGHT]` — ask the user to choose a format or enter custom text:
     > "Which copyright notice?
     > (a) © [YEAR] [AUTHOR_NAME]. All rights reserved.
     > (b) © [YEAR] [AUTHOR_NAME]. Licensed under CC BY 4.0.
     > (c) © [YEAR] [AUTHOR_NAME]. Licensed under CC BY-NC 4.0.
     > (d) CC0 — public domain dedication
     > (e) Custom — enter your own text
     > (f) Skip — omit from export metadata"
     
     Written into `dc:rights` in EPUB/DOCX/LaTeX exports. If skipped, the field is omitted from the exported file.
   - `[LANGUAGE]` — BCP-47 code. Ask if not already set:
     > "What language is this story written in? (e.g. en, de, fr, es, it, pt, nl, ja, zh, fi, hu, tr)"
     
     Controls prose drafting language, SSML `xml:lang`, export `dc:language`, and gates English-only prose checks.
   - `[PLOT_STRUCTURE]` — if not set, present the 8 options with a brief description of each and ask the user to choose
   - `[DRAMATIC_QUESTION]` — one sentence, the story's spine
   - `[THEME]` — stated as a question, not an answer
   - `[POV_STRATEGY]` — ask if not already set:
     > "What is the POV strategy?
     > (a) **single** — one POV character throughout
     > (b) **alternating** — two or more POV characters, alternating chapters/sections
     > (c) **multiple** — three or more POV characters
     > (d) **first-person-multiple** — each POV uses 'I' with distinct voice"
   - `[TENSE]` — ask if not already set:
     > "What tense?
     > (a) **past** — standard past tense
     > (b) **present** — present tense for immediacy
     > (c) **dual** — past for story, present for flashbacks"
   - `[TONE]` — ask if `STYLE_MODE` is `humanized-ai` and not already set:
     > "What is the emotional register of this story?
     > (a) **warm-dark** — emotional intimacy with genuine threat and consequence
     > (b) **dry-ironic** — deadpan distance, situational irony, understatement
     > (c) **bleak-unflinching** — no comfort, no rescue, consequences are final
     > (d) **elevated-lyrical** — prose beauty is foregrounded; emotional intensity through image
     > (e) **neutral-controlled** — flat affect, reader infers; Flesch target 60–70"
     
     If `STYLE_MODE` is `author-sample`, Tone is derived from the extracted markers — confirm the inferred value rather than asking from scratch.
   - `[TARGET_AUDIENCE]` — ask if not already set:
     > "Who is the primary audience?
     > (a) **adult** — no content ceiling; vocabulary unrestricted
     > (b) **new-adult** — 18–25; mature themes permitted; extreme graphic content discouraged
     > (c) **young-adult** — 13–18; sexual content limited to non-explicit; violence permitted with consequence
     > (d) **middle-grade** — 8–12; no sexual content; violence must be consequence-free or off-page
     > (e) **literary** — adult literary fiction readership; elevated register, ambiguity permitted"
   - `[SERIES_POSITION]` — ask if not already set:
     > "What is the series position?
     > (a) **standalone** — a complete story with no series context needed
     > (b) **book-1** — first book in a series (series-bible.md will be created by speckit.plan)
     > (c) **book-2** — second book in a series
     > (d) **book-3** — third book in a series
     > (e) **book-N** — specify the book number"
   - `[WORD_COUNT_TARGET]`, `[GENRE]`
   - `[AUTHOR_BIO_SHORT]` and `[AUTHOR_BIO_LONG]` — both optional at this stage. Inform the user:
     > "Author bios are optional now. Run `/speckit.bio draft` at any time to generate and save them. They are consumed automatically by `speckit.query` (short bio) and `speckit.export` (long bio as 'About the Author' back matter)."
     
     If the user wants to set them now: accept free-text for each. Otherwise write `[PLACEHOLDER]` as the value.
   - If `[SERIES_POSITION]` is anything other than `standalone`: check whether `series/series-bible.md` exists.
     - If it **exists**: load it, populate `## IX. Series Context` — copy the active SC-NNN and STC-NNN rows relevant to this book, confirm `Series title` and `Series POV strategy`/`Series tense`, and compare against this constitution's `[POV_STRATEGY]`/`[TENSE]`. Any mismatch → log in the Series Variance Log with a `[reason]` placeholder for the author to fill.
     - If it **does not exist yet**: emit `⚠️ series/series-bible.md not found — it will be created by speckit.plan. Populate ## IX. Series Context with [TBD] placeholder values for now.`
   - `[DRY_IRONY_CHARACTERS]` — which characters (if any) are permitted situational irony
   - `[STORY_SPECIFIC_PRINCIPLES]` — 3–5 rules unique to this story
   - `[ADDITIONAL_PROHIBITED_PHRASES]` — story/genre-specific additions to the Anti-AI filter

3b. **RAG Search Index** — ask if not already set:

   > "Do you want to enable the offline search index for this project?
   >
   > It indexes all supporting documents (characters, locations, timeline, world-building, plan, etc.)
   > so that speckit.implement, speckit.continuity, and speckit.research can retrieve relevant
   > passages without loading all files into context.
   >
   > (a) **yes** — enable the index (requires pip install chromadb sentence-transformers rank-bm25)
   > (b) **no** — skip for now (can be enabled later with `python .specify/presets/fiction-book-writing/scripts/python/index.py build`)"

   If **yes**:
   - Set `[SEARCH_INDEX_ENABLED]` to `yes`
   - **Execute** `scripts/bash/setup-plan.sh` (Unix/macOS) or `scripts/powershell/setup-plan.ps1` (Windows) from the project root. This installs chromadb, sentence-transformers, and rank-bm25. Both scripts auto-create a `.venv` virtual environment if one doesn't exist.
   - Verify the Python ChromaDB package is installed by checking that `.venv` exists and contains the packages. If the script fails, inform the user: "⚠️ Failed to install search index packages. You can run the script manually later with `bash scripts/bash/setup-plan.sh` or `.\scripts\powershell\setup-plan.ps1`."
   - A configuration file `.specify/index/config.json` will be created on first run. Edit this file to adjust:
    - `backend_preference` (auto, chroma, bm25, keyword)
    - `embedding_model` (e.g., `all-MiniLM-L6-v2`)
    - `chunk_size_tokens` (target tokens per chunk)
    - `top_k` (default number of results per query)
    
    ```json
    {
      "backend_preference": "auto",
      "embedding_model": "all-MiniLM-L6-v2",
      "chunk_size_tokens": 300,
      "top_k": 5
    }
    ```
   - Ask for backend preference:
     > "Which backend?
     > (a) **auto** — use best available (chromadb if installed, else bm25, else built-in)
     > (b) **chroma** — force ChromaDB vector search (requires chromadb + sentence-transformers)
     > (c) **bm25** — force rank-bm25 keyword search
     > (d) **keyword** — use built-in TF scorer (no install needed)"
   - Ask for embedding model (default: `all-MiniLM-L6-v2`):
     > "Embedding model (press Enter for default `all-MiniLM-L6-v2`):"
   - Ask for chunk size (default: 300):
     > "Chunk size in tokens (200–600 recommended, press Enter for default 300):"
   - Ask for top-k (default: 5):
     > "Results per query (press Enter for default 5):"

   If **no**:
   - Set `[SEARCH_INDEX_ENABLED]` to `no`
   - Leave other RAG fields as defaults

3c. **Resolve Illustration Guidelines section** (Section XI of constitution.md):

   If `[ILLUSTRATIONS_ENABLED]` is `[NEEDS CLARIFICATION]` or absent, ask:

   > "Will this book include illustrations?
   > (a) **yes** — configure illustration defaults for speckit.illustrate
   > (b) **no** — skip illustration configuration"

   If Illustrations is `no`: mark the section as inactive and proceed to audiobook configuration.

   If Illustrations is `yes`:

   **Illustration Automation** — ask if not set:
   > "How should illustrations be handled?
   > (a) **per-chapter** — automatically create illustration placeholders and add references to draft files
   > (b) **manual** — only generate illustration briefs; you manually add image links"

   **Default Style** — ask if not set:
   > "Which illustration style?
   > (a) **penandink** — Pen and Ink (literary fiction, classics, MG)
   > (b) **2color** — Two-Color Print (chapter openers, section dividers)
   > (c) **greyscale** — Greyscale (interior illustrations, budget printing)
   > (d) **woodcut** — Woodcut Print (historical, literary, horror)
   > (e) **lineart** — Line Art (MG, chapter headers)
   > (f) **engraving** — Copperplate Engraving (period pieces)
   > (g) **artnouveau** — Art Nouveau (fantasy, historical romance)
   > (h) **artdeco** — Art Deco (1920s-1930s settings)
   > (i) **vintage** — Vintage Book Style (period pieces, nostalgia)
   > (j) **minimalist** — Minimalist (contemporary, literary)"

   **Default Color Range** — ask if not set:
   > "Which color range?
   > (a) **full** — Full color (CMYK/RGB) for premium editions
   > (b) **2color** — Two-color printing (black + 1 spot color)
   > (c) **greyscale** — Greyscale only for interior illustrations"

   **Default Aspect Ratio** — ask if not set:
   > "Which aspect ratio?
   > (a) **portrait** — 2:3 ratio (standard book)
   > (b) **landscape** — 3:2 ratio (wide format)
   > (c) **square** — 1:1 ratio"

   **Base Design Guideline** — ask if not set:
   > "Any overall visual direction for illustrations? (e.g., 'Minimalist line art with single accent color', 'Cross-hatched engraving style', or press Enter to skip)"

   Validate: if Illustrations is `yes` but Default Style, Default Color Range, or Default Aspect Ratio are not set → emit `⚠️ Illustration defaults incomplete. These fields are required when Illustrations: yes.`

3d. **Resolve Audiobook Production section** (Section X of constitution.md):

   If `[OUTPUT_MODE]` is `[NEEDS CLARIFICATION]` or absent, ask:

   > "What output do you want for this story?
   > (a) **book** — prose drafts only, no audiobook files
   > (b) **both** — prose drafts AND audiobook TTS drafts"

   If Output Mode is `book`: skip the audiobook configuration.

   If Output Mode is `audiobook` or `both`:

   If `[ILLUSTRATIONS_ENABLED]` is `[NEEDS CLARIFICATION]` or absent, ask:

   > "Will this book include illustrations?
   > (a) **yes** — configure illustration defaults for speckit.illustrate
   > (b) **no** — skip illustration configuration"

   If Illustrations is `no`: mark the section as inactive and stop here.

   If Illustrations is `yes`:

   **Illustration Automation** — ask if not set:
   > "How should illustrations be handled?
   > (a) **per-chapter** — automatically create illustration placeholders and add references to draft files
   > (b) **manual** — only generate illustration briefs; you manually add image links"

   **Default Style** — ask if not set:
   > "Which illustration style?
   > (a) **penandink** — Pen and Ink (literary fiction, classics, MG)
   > (b) **2color** — Two-Color Print (chapter openers, section dividers)
   > (c) **greyscale** — Greyscale (interior illustrations, budget printing)
   > (d) **woodcut** — Woodcut Print (historical, literary, horror)
   > (e) **lineart** — Line Art (MG, chapter headers)
   > (f) **engraving** — Copperplate Engraving (period pieces)
   > (g) **artnouveau** — Art Nouveau (fantasy, historical romance)
   > (h) **artdeco** — Art Deco (1920s-1930s settings)
   > (i) **vintage** — Vintage Book Style (period pieces, nostalgia)
   > (j) **minimalist** — Minimalist (contemporary, literary)"

   **Default Color Range** — ask if not set:
   > "Which color range?
   > (a) **full** — Full color (CMYK/RGB) for premium editions
   > (b) **2color** — Two-color printing (black + 1 spot color)
   > (c) **greyscale** — Greyscale only for interior illustrations"

   **Default Aspect Ratio** — ask if not set:
   > "Which aspect ratio?
   > (a) **portrait** — 2:3 ratio (standard book)
   > (b) **landscape** — 3:2 ratio (wide format)
   > (c) **square** — 1:1 ratio"

   **Base Design Guideline** — ask if not set:
   > "Any overall visual direction for illustrations? (e.g., 'Minimalist line art with single accent color', 'Cross-hatched engraving style', or press Enter to skip)"

   Validate: if Illustrations is `yes` but Default Style, Default Color Range, or Default Aspect Ratio are not set → emit `⚠️ Illustration defaults incomplete. These fields are required when Illustrations: yes.`

3d. **Resolve Audiobook Production section** (Section X of constitution.md):

   If `[OUTPUT_MODE]` is `[NEEDS CLARIFICATION]` or absent, ask:

   > "What output do you want for this story?
   > (a) **book** — prose drafts only, no audiobook files
   > (b) **both** — prose drafts AND audiobook TTS drafts"

   If Output Mode is `book`: skip the audiobook configuration.

   If Output Mode is `audiobook` or `both`:

   **TTS engine** — ask if not set:
   > "Which TTS engine?
   > (a) **ssml-cloud** — SSML XML output for Azure TTS, Google Cloud TTS, or Amazon Polly
   > (b) **elevenlabs** — ElevenLabs voice IDs, break tags, and .pls lexicon sidecar
   > (c) **both** — generate both variants per chapter"

   **Speaker mode** — ask if not set:
   > "Speaker mode?
   > (a) **single** — one narrator voice reads everything (narration + all dialogue)
   > (b) **multi** — narrator reads prose; each named character's dialogue is routed to a distinct voice"

   **Speaker Configuration table**:
   - Always populate the narrator row with the user's chosen voice name/ID
   - For `multi` mode: add one row per named speaking character. Ask the user to provide voice names/IDs now, or stub with `[NEEDS CLARIFICATION]` to fill later
   - For `single` mode: only the narrator row is required; remove or keep the comment placeholder

   **Pronunciation Lexicon**:
   - Scan `spec.md` and `characters.md` (if present) for unusual names, invented words, or foreign terms
   - Pre-populate the lexicon table with any found. Mark IPA and hints as `[NEEDS CLARIFICATION]` for entries that need phonetic review
   - Ask the user: "Any words or names you know TTS commonly mispronounces for this story?"

   **Audiobook Style Hints**:
   - Ask: "Any delivery notes for the narrator or specific characters? (e.g., speaking pace, emotional register, pausing style)"
   - Populate the table if provided; leave the placeholder if none given

   Validate: if `multi` speaker mode but no character voice rows populated → emit `⚠️ Speaker Configuration incomplete. Add voice IDs for each character or switch to single speaker mode.`

4. **Increment the semantic version**:
   - **MAJOR**: if plot structure, POV strategy, or number of POV strands changed
   - **MINOR**: if new principles, style rules, or Anti-AI phrases added
   - **PATCH**: typos, clarifications, minor refinements
   - Update `[CONSTITUTION_VERSION]`, `[RATIFICATION_DATE]` (on first creation only), `[LAST_AMENDED_DATE]`

5. **Write a Sync Impact Report** as an HTML comment at the top of the file, summarizing what changed and which dependent templates are affected:
   ```html
   <!-- SYNC IMPACT: v1.0.0 → v1.1.0
        Changed: Added 3 prohibited phrases, updated theme statement
        Affected templates: spec-template.md (Reader Experience Goals), tasks-template.md (Polish Pass)
        Action required: Re-run /speckit.continuity if scenes have been drafted -->
   ```

6. **Propagate changes** to dependent templates if applicable:
   - If plot structure changed: update `plan-template.md` to activate the correct structure block
   - If Anti-AI Filter phrases changed: note in the impact report (scenes need re-scan)
   - If POV strategy changed: update `spec-template.md` character arc section header

7. **Generate `.specify/memory/craft-rules.md`**:
   - Copy `templates/craft-rules-template.md`
   - Set `[PROSE_PROFILE]` to the chosen prose profile value
   - If `STYLE_MODE` is `humanized-ai`: keep only the chosen profile's definition block under `## Profile Specifications`; remove the other four profile blocks entirely
   - If `STYLE_MODE` is `author-sample`: remove the entire `## Profile Specifications` section (profiles are irrelevant; craft rules II–VI and the Universal Anti-AI Filter still apply)
   - Write the result to `.specify/memory/craft-rules.md`
   - Emit: `✓ craft-rules.md written — loaded automatically by speckit.implement, speckit.checklist, speckit.polish, speckit.revise.`

8. **Validate the final constitution**:
   - No unresolved `[NEEDS CLARIFICATION]` tokens remain
   - `[AUTHOR_NAME]` is set (not `[PLACEHOLDER]`) — warn if absent: `⚠️ Author Name not set — required by speckit.cover, speckit.query, and speckit.export`
   - `[LANGUAGE]` is a valid BCP-47 code from the supported list — warn if absent, default will be `en`
   - `[COPYRIGHT]` is set or explicitly skipped — info note if absent: `ℹ️ Copyright not set — dc:rights will be omitted from exports`
   - `[TONE]` is one of the 5 supported values when `STYLE_MODE` is `humanized-ai`
   - `[TARGET_AUDIENCE]` is one of the 5 supported values
   - `[RATIFICATION_DATE]` and `[LAST_AMENDED_DATE]` are ISO format (`YYYY-MM-DD`)
   - Style mode is explicitly set
   - If `humanized-ai` mode: `[PROSE_PROFILE]` is one of the 5 supported values: `commercial`, `literary`, `thriller`, `atmospheric`, `dark-realist`
   - Plot structure is one of the 8 supported values: `three-act`, `heros-journey`, `save-the-cat`, `kishotenketsu`, `freytag`, `story-circle`, `five-act`, `given-by-spec`
   - Theme is stated as a question, not an answer
   - If `author-sample` mode: all 8 Extracted Style Markers have values (not `[NEEDS CLARIFICATION]`)
   - If Series Position is non-standalone: `## IX. Series Context` is present and has at least one populated SC-NNN or STC-NNN row, or is explicitly marked `[TBD pending series-bible.md creation]`. Any Series Variance Log row that is present but has an empty Justification column → WARNING.
   - `[OUTPUT_MODE]` is one of: `book`, `both`
   - If Output Mode is `audiobook` or `both`:
     - `[TTS_ENGINE]` is one of: `ssml-cloud`, `elevenlabs`, `both`
     - `[SPEAKER_MODE]` is one of: `single`, `multi`
     - Narrator row in Speaker Configuration is populated (not `[NEEDS CLARIFICATION]`) — warn if not
     - If `multi` speaker mode: at least one character row present in Speaker Configuration — warn if none
   - `[SEARCH_INDEX_ENABLED]` is one of: `yes`, `no`
   - If `yes`:
     - `[BACKEND_PREFERENCE]` is one of: `auto`, `chroma`, `bm25`, `keyword`
     - `[EMBEDDING_MODEL]` is a valid model name (default: `all-MiniLM-L6-v2`)
     - `[CHUNK_SIZE_TOKENS]` is an integer 200–600
     - `[TOP_K_DEFAULT]` is a positive integer
   - `[ILLUSTRATIONS_ENABLED]` is one of: `yes`, `no`
   - If Illustrations is `yes`:
     - `[ILLUSTRATION_AUTOMATION]` is one of: `per-chapter`, `manual`
     - `[DEFAULT_ILLUSTRATION_STYLE]` is one of: `penandink`, `2color`, `greyscale`, `woodcut`, `lineart`, `engraving`, `artnouveau`, `artdeco`, `vintage`, `minimalist`
     - `[DEFAULT_ILLUSTRATION_COLOR]` is one of: `full`, `2color`, `greyscale`
     - `[DEFAULT_ILLUSTRATION_ASPECT]` is one of: `portrait`, `landscape`, `square`

8. **Report**: Summarize all resolved fields, the new version number, and any remaining items requiring attention.

9. **Update search index** (optional — large projects):
   - If `.specify/index/` exists, run: `python .specify/presets/fiction-book-writing/scripts/python/index.py update` from the project root.
   - This re-indexes the updated `.specify/memory/constitution.md` so that subsequent `speckit.implement`, `speckit.continuity`, and `speckit.research` queries reflect the latest story bible rules.
   - If the command fails or the index does not exist, skip silently.
