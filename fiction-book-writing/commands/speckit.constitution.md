---
description: Create or update the story bible — style mode selection, plot structure choice, craft principles, and propagation to all dependent templates.
handoffs:
  - label: Create Story Brief
    agent: speckit.specify
    prompt: Create a story brief for...
---

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
  python scripts/python/index.py query "genre tone protagonist arc" --top 8
  python scripts/python/index.py query "world rules setting premise" --type spec --top 5
  python scripts/python/index.py query "theme dramatic question" --type spec --top 5
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
     > (c) **thriller** — action-forward, minimal interiority, short-dominant sentences (thrillers, crime, horror)
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
   - `[PLOT_STRUCTURE]` — if not set, present the 7 options with a brief description of each and ask the user to choose
   - `[DRAMATIC_QUESTION]` — one sentence, the story's spine
   - `[THEME]` — stated as a question, not an answer
   - `[POV_STRATEGY]` and `[TENSE]` — from style mode or user input
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
   - `[WORD_COUNT_TARGET]`, `[GENRE]`, `[SERIES_POSITION]`
   - `[AUTHOR_BIO_SHORT]` and `[AUTHOR_BIO_LONG]` — both optional at this stage. Inform the user:
     > "Author bios are optional now. Run `/speckit.bio draft` at any time to generate and save them. They are consumed automatically by `speckit.query` (short bio) and `speckit.export` (long bio as 'About the Author' back matter)."
     
     If the user wants to set them now: accept free-text for each. Otherwise write `[PLACEHOLDER]` as the value.
   - If `[SERIES_POSITION]` is anything other than `standalone`: check whether `series/series-bible.md` exists.
     - If it **exists**: load it, populate `## IX. Series Context` — copy the active SC-NNN and STC-NNN rows relevant to this book, confirm `Series title` and `Series POV strategy`/`Series tense`, and compare against this constitution's `[POV_STRATEGY]`/`[TENSE]`. Any mismatch → log in the Series Variance Log with a `[reason]` placeholder for the author to fill.
     - If it **does not exist yet**: emit `⚠️ series/series-bible.md not found — it will be created by speckit.plan. Populate ## IX. Series Context with [TBD] placeholder values for now.`
   - `[DRY_IRONY_CHARACTERS]` — which characters (if any) are permitted situational irony
   - `[STORY_SPECIFIC_PRINCIPLES]` — 3–5 rules unique to this story
   - `[ADDITIONAL_PROHIBITED_PHRASES]` — story/genre-specific additions to the Anti-AI filter

3b. **RAG Index System** — ask after `[WORD_COUNT_TARGET]` is known:

   Determine the target word count from the resolved `[WORD_COUNT_TARGET]` field (or from `$ARGUMENTS` if not yet set). Compare against 80,000 words to form the recommendation label.

   Ask the user:

   > "Do you want to enable the RAG semantic search index for this project?
   > It allows `speckit.implement`, `speckit.continuity`, `speckit.research`, and other commands to retrieve relevant passages from your entire project without loading all files into context.
   > *(Your target is [WORD_COUNT_TARGET] words — **recommended** for projects over 80,000 words / optional for smaller projects)*
   > (a) **Yes** — initialize the index now
   > (b) **No** — skip (can be enabled later with `python scripts/python/index.py build`)"

   If the user chooses **(b)**: skip silently and continue.

   If the user chooses **(a)**:

   1. **Check if already initialized**: inspect whether `.specify/index/chroma/` exists in the project root.
      - If it exists → emit `ℹ️ ChromaDB index already initialized at .specify/index/ — skipping build.` and continue without re-running build.

   2. **Check if dependencies are installed** (only if not already initialized):
      Run:
      ```
      python -m pip show chromadb sentence-transformers
      ```
      - If both packages are found → proceed to build.
      - If either is missing → ask if a virtual environment is preferred:
        > "ChromaDB and sentence-transformers are not installed.
        > (a) **Install to global/user site** — `python -m pip install chromadb sentence-transformers`
        > (b) **Create and use .venv** (Recommended) — creates a `.venv/` folder and installs there"
      
      - If the user chooses **(b)**:
        1. Run `python -m venv .venv`
        2. Activate (Windows: `.venv\Scripts\Activate.ps1`, Unix: `source .venv/bin/activate`)
        3. Run `python -m pip install chromadb sentence-transformers`
      - Else if **(a)** or fallback:
        Run:
        ```
        python -m pip install chromadb sentence-transformers
        ```
        - On success → proceed to build.
        - On failure → emit: `⚠️ Installation failed. Ensure Python is on the PATH and try running manually: python -m pip install chromadb sentence-transformers` and stop.

   3. **Build the index**:
      Run from the project root:
      ```
      python scripts/python/index.py build
      ```
      - On success → emit: `✓ RAG index initialized at .specify/index/ — semantic search is now active for all project files.`
      - On failure → emit: `⚠️ Index build failed. Check that Python is available and dependencies are installed. You can retry later with: python scripts/python/index.py build`

3c. **Resolve Audiobook Production section** (Section X of constitution.md):

   If `[OUTPUT_MODE]` is `[NEEDS CLARIFICATION]` or absent, ask:

   > "What output do you want for this story?
   > (a) **book** — prose drafts only, no audiobook files
   > (b) **audiobook** — audiobook TTS drafts generated alongside prose drafts
   > (c) **both** — prose drafts AND audiobook TTS drafts"

   If Output Mode is `book`: mark the section as inactive and stop here.

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
   - Plot structure is one of the 7 supported values
   - Theme is stated as a question, not an answer
   - If `author-sample` mode: all 8 Extracted Style Markers have values (not `[NEEDS CLARIFICATION]`)
   - If Series Position is non-standalone: `## IX. Series Context` is present and has at least one populated SC-NNN or STC-NNN row, or is explicitly marked `[TBD pending series-bible.md creation]`. Any Series Variance Log row that is present but has an empty Justification column → WARNING.
   - `[OUTPUT_MODE]` is one of: `book`, `audiobook`, `both`
   - If Output Mode is `audiobook` or `both`:
     - `[TTS_ENGINE]` is one of: `ssml-cloud`, `elevenlabs`, `both`
     - `[SPEAKER_MODE]` is one of: `single`, `multi`
     - Narrator row in Speaker Configuration is populated (not `[NEEDS CLARIFICATION]`) — warn if not
     - If `multi` speaker mode: at least one character row present in Speaker Configuration — warn if none

8. **Report**: Summarize all resolved fields, the new version number, and any remaining items requiring attention.

9. **Update search index** (optional — large projects):
   - If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root.
   - This re-indexes the updated `.specify/memory/constitution.md` so that subsequent `speckit.implement`, `speckit.continuity`, and `speckit.research` queries reflect the latest story bible rules.
   - If the command fails or the index does not exist, skip silently.
