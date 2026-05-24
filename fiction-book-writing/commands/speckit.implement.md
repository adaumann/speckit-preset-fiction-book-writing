description: Draft scenes and chapters — supports discovery mode (--discovery), outline dismissal (--dismiss-outline), and voice sample calibration (--voice <file>).
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
## Purpose

The **`/speckit.implement`** command generates a prose draft for a specified chapter (or chapters) based on the project's planning files. It:
* Loads the appropriate scene outline or plan entry.
* Enforces checklist and outline gates unless overridden.
  * Supports optional modes (flags):
    * `--discovery` – Draft the scene in discovery mode, letting the POV character explore the moment.
    * `--dismiss-outline` – Bypass outline gates and draft without a predefined beat map.
    * `--outline-only` – Produce only an outline file for the chapter; no prose is written.
    * `--voice <file>` – Use the provided writing‑sample file to calibrate prose style (rhythm, register, sensory density).
* Updates draft files, task status, and story‑bible metadata, then reports the results.

## Flags

| Flag | Description |
|------|-------------|
| `--discovery` | Write the chapter in a discovery style, using the POV character’s senses as the primary guide.
| `--dismiss-outline` | Skip outline validation and draft freely; the outline is treated only as a loose guide.
| `--outline-only` | Generate an outline file (`outlines/<CHAPTER_ID>_<ChapterName>-outline.md`) with status `DRAFT` and stop; no prose draft is created.
| `--voice <file>` | Provide a path to a writing‑sample file; the command will read a few paragraphs to align its prose style with the author's voice.

These flags can be combined as needed (e.g., `/speckit.implement --dismiss-outline --discovery`).

## Execution Flow

1. **Validate input** – Ensure `$ARGUMENTS` are present; abort if required arguments are missing.
2. **Run pre‑hooks** – Execute any `hooks.before_implement` defined in `.specify/extensions.yml`.
3. **Update search index** – If the project has a Python index script, run it before and after drafting.
4. **Resolve `FEATURE_DIR`** – Determine the feature directory (first sub‑folder in `specs/` or project root).
5. **Checklist gate** – Scan `checklists/`; if any are incomplete, stop and report unless the user explicitly overrides.
6. **Outline gate** – Locate the target outline file; apply `--dismiss-outline` or `--outline-only` behavior as requested.
7. **Load context** – Pull required files (constitution, outline, character profiles) respecting the token budget.
8. **Prepare working brief** – Assemble the brief from the outline or plan entry according to the selected mode.
9. **Draft prose** – Write the chapter following the brief, applying discovery mode, voice calibration, and style rules.
10. **Post‑draft actions** – Save the draft, update `tasks.md`, modify the scene‑outline status, log any new Chekhov items, and adjust location state logs.
11. **Generate reports** – Summarize drafted chapters, word counts, deviations, and any `[NEEDS CLARIFICATION]` markers.
12. **Run post‑hooks** – Execute any `hooks.after_implement` defined in `.specify/extensions.yml`.

The command exits after step 12, leaving the workspace updated and ready for the next task.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before drafting)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_implement` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

**Update search index** (large projects):
- Check whether `scripts/python/index.py` exists (check `.specify/presets/fiction-book-writing/scripts/python/index.py` first, then `scripts/python/index.py` as fallback) and `.specify/index/` exists (index has been built).
- If both exist, run: `python .specify/presets/fiction-book-writing/scripts/python/index.py update` from the project root before drafting begins.
- This ensures semantic search reflects the latest draft files and supporting documents.
   - After drafting is complete, run: `python .specify/presets/fiction-book-writing/scripts/python/index.py update` again to index the newly written chapter.
1. **Setup**: Resolve `FEATURE_DIR` by reading the project structure: the first subdirectory inside `specs/` that contains project files. Fall back to project root if `specs/` does not exist.

2. **Check checklist gates** (if `FEATURE_DIR/checklists/` exists):
   - Scan all checklist files in `checklists/`
   - For each checklist, count total items vs. completed items (`- [x]` or `- [X]`)
   - If ANY checklist has incomplete items, output a status table and **stop**:
     ```
     ⚠️ CHECKLIST GATE: Incomplete quality gates detected.

     | Checklist | Total | Complete | Incomplete |
     |---|---|---|---|
     | [name] | N | N | N |

     These checklists must be completed before drafting continues.
     To override: explicitly confirm "proceed despite incomplete checklists"
     ```
   - If the user explicitly confirms, proceed with a warning in the draft output

2b. **Check outline gate** (if `FEATURE_DIR/outlines/` exists):
   - **Resolve target chapter ID**:
     - If `$ARGUMENTS` contains a chapter ID (e.g., `A1.101`), use that
     - Else if `tasks.md` exists in `FEATURE_DIR`, use the first unchecked task
     - Else if `tasks.md` does not exist, use the first unchecked scene in `plan.md ## Scene Outline` (status not `done` or `skip`)
   - After resolving the target chapter ID, look for a matching outline file at `outlines/<CHAPTER_ID>_<ChapterName>-outline.md`
   - **`--dismiss-outline` mode**: If `$ARGUMENTS` contains `--dismiss-outline`:
     - Skip the outline gate entirely for this chapter
     - Use `plan.md ## Scene Outline` entry as a direction-of-travel guide, not a beat map
     - Proceed directly to drafting with discovery mode enabled (see step 5)
     - Note in DRAFT NOTES: `Outline dismissed — discovery draft`
   - If a matching outline file exists:
     - Read its `status` field from the frontmatter
     - If `status: DRAFT` — stop and display:
       ```
       ⚠️ OUTLINE GATE: outlines/<CHAPTER_ID>-outline.md has status: DRAFT.

       Review the scene outline, edit beats and requirements as needed, then set:
           status: APPROVED

       To write this chapter yourself instead, set:
           status: SKIP

       To dismiss the outline and draft freely, re-run with:
           /speckit.implement --dismiss-outline <CHAPTER_ID>

       Then re-run /speckit.implement
       ```
     - If `status: SKIP` — do not generate any prose for this chapter. Instead:
       - Report: `⏭ SKIP: <CHAPTER_ID> <ChapterName> — author will write this chapter. No prose generated.`
       - If `tasks.md` exists: Mark the corresponding task `[x]` in `tasks.md` with a note: `[author-written — no AI draft]`
       - If `tasks.md` does not exist: Update the `## Scene Outline` entry status in `plan.md` from `outline` → `author-draft`
       - Advance to the next unchecked task (from tasks.md or plan.md) and repeat the outline gate check
     - If `status: APPROVED` — proceed to drafting using the outline file as the working brief (see step 4)
   - If no outline file exists for this chapter — proceed using `plan.md ## Scene Outline` as a direction-of-travel guide (discovery mode, no gate applied)

3. **Load context (Context Budget: 4k-8k tokens)**:
   - **Mandatory**: `constitution.md`, the current scene outline, and the POV character profile.
   - **Targeted**: Only load specific files listed in the outline's `Documents Needed`. 
   - **RAG-First**: For world-building or secondary characters, use RAG queries instead of loading the full files. 
   - **Context Retrieval (Drafts & Outlines)**: For checking past/future scene beats or specific draft details (to ensure setup/payoff), query the index instead of loading multiple full files.
   - **Summaries**: If a file is >5000 words, read only its `# Summary` or `## Recent Events` section.
   - **Skip**: `spec.md` and `plan.md` unless the outline explicitly points to them for unresolved questions.

     Use returned chunks to supplement or replace loading full files when combined file size approaches context limits.

- **Outline-required context** (if outline file exists with `status: APPROVED`): read the `## Required Context` section from the outline file and use it to determine which documents to load. For documents listed, use RAG queries instead of loading full files:
     ```
     python .specify/presets/fiction-book-writing/scripts/python/index.py query "[from outline Required Context]" --type [character|world|theme|outline] --top 3
     ```
     Only load full files for: constitution.md, plan.md ## Scene Outline (this chapter), and the outline file itself.

4. **Resolve the target chapter outline**:
   - **Priority order for the working brief**:
     1. If `$ARGUMENTS` contains `--dismiss-outline` → use `plan.md ## Scene Outline` entry as a **direction-of-travel guide**. Extract only: POV, setting, timeline position, estimated length, opening hook intent, closing beat intent. Do not extract or enforce intermediate beats, dialogue requirements, or sensory anchors. The model discovers these.
     2. If `outlines/<CHAPTER_ID>_<ChapterName>-outline.md` exists with `status: APPROVED` → use the outline file as the sole working brief. Extract: opening hook, beat sequence, character beats, dialogue requirements, sensory anchors, thematic work from the outline file sections.
     3. Otherwise → fall back to `plan.md ## Scene Outline` entry as a direction-of-travel guide (discovery mode). Extract: POV, setting, timeline position, estimated length, opening hook, key beats (in order), character beats, dialogue requirements, sensory details, thematic work, closing beat. Use these as reference, not mandate.
   - This resolved content is the **working brief** — follow it, do not improvise structure. In `--dismiss-outline` or discovery mode, follow it as a compass, not a map.
   - If the working brief contains `[NEEDS CLARIFICATION]` markers, pause and resolve them with the user before drafting
   - If the outline file and `plan.md` conflict on structural beats, the **outline file wins** (it is the author's last-reviewed version). Note the conflict in the draft's `DRAFT NOTES` block.

5. **Draft the chapter**:

   **`--outline-only` mode**: If `$ARGUMENTS` contains `--outline-only`:
   - Run `speckit.outline` behaviour for the target chapter(s) instead of drafting prose
   - Generate `outlines/<CHAPTER_ID>_<ChapterName>-outline.md` with `status: DRAFT`
   - Do **not** write any prose or create any file in `draft/`
   - Report the outline file path(s) and remind the author to review, then either approve or set `status: SKIP` and re-run `/speckit.implement`
   - Stop after generating outlines

   **Voice sample** (optional — if available): Check whether `writing-sample.md` exists at the project root, or whether `$ARGUMENTS` contains `--voice <filepath>`. If a voice sample is available:
   - **Do NOT analyze it** or extract formal markers
   - **Do read 2-3–5 paragraphs aloud in your head** (simulate the reading experience) to absorb the rhythm, register, and sensory density
   - Keep the sample open as a **stylistic compass** — when unsure about sentence length, vocabulary choice, or how much interiority, or what rhythm to land on, glance at the sample and match its register
   - The goal is not to copy the sample but to **calibrate your prose ear** to the author's frequency

   **`--discovery` mode**: If `$ARGUMENTS` contains `--discovery`:
   - After loading the working brief (outline or plan.md), set it aside as a **reference only** — do not write to it
   - Write the scene as if discovering it for the first time through the POV character's senses
   - Hit the beats but don't let the beats drive the prose — let the character's moment-to-moment experience drive the prose
   - Trust that the causal progression is internalised; check against the outline only at scene-end to confirm coverage
   - This mode is the default when no outline file exists (discovery replaces rigid beat-following)

   **Prose language**: Draft all prose written *into the chapter draft file* in the language specified in `constitution.md § VII Language`. If Language is not set or not recognised, default to English. **All command output, status messages, confirmations, and conversational responses remain in English regardless of the Language setting.**

   **Output path**: `draft/<CHAPTER_ID>_<ChapterName>.md`
   **Naming convention**: `{PREFIX}{phase}.{beat_number}_{ShortName}.md` where PREFIX is the plot-structure prefix from `constitution.md` (e.g., `A` = three-act, `JO` = Hero's Journey, `SC` = Save the Cat, `KT` = Kishōtenketsu, `FT` = Freytag, `SL` = Story Circle, `FA` = Five-Act, `SP` = given-by-spec, `P` = generic). Examples: `draft/A1.101_Awakening.md`, `draft/JO3.201_SupremeOrdeal.md`
   Create `draft/` directory in `FEATURE_DIR` if it does not exist.

   **Every draft file MUST begin with this header block** (machine-readable; do not omit or reorder fields):
   ```
   ---
   chapter_id: A1.101   # e.g. A1.101 (three-act) or JO3.201 (heros-journey)
   chapter_name: Awakening
   beat_id: A1.101      # same as chapter_id
   pov_character: [Character Name]
   pov_type: [3rd person limited / 1st person / 3rd person omniscient]
   act_phase: [Act I / Act II-A / Act II-B / Act III]
   plot_structure_stage: [e.g., Inciting Incident / Midpoint / All Is Lost]
   timeline_position: [e.g., Day 3, late afternoon]
   estimated_words: [number from scene outline]
   actual_words: [fill after writing]
   status: draft
   version: 1
   outline_ref: plan.md#scene-outline
   drafted: [YYYY-MM-DD]
   constitution_version: [hash or date of constitution.md used]
   ---
   ```
   Fields are used by `speckit.continuity` and `speckit.revise` for machine-readable chapter identification and continuity checking. `actual_words` and `status` must be filled after writing.

   **Before writing**:
   - Confirm POV character's full profile from `characters/[name].md` is loaded — specifically: voice register, vocabulary pool, micro-obsession state for this phase, current emotional state per the arc progression table, active self-deception pattern, and stress tells
   - Absorb the opening hook and closing beat — the draft must open with the hook's intent and end at the closing beat's instability
   - If in `--discovery` mode: take a moment to imagine yourself in the POV character's body at this moment. What do they notice first? What do they avoid? Let that guide the opening, not the outline's first beat.
   - Confirm the Triple Purpose: this chapter must advance plot + reveal character + deepen world

   **While writing** — write as a storyteller, not a task-executor:

   **Mode**: You are discovering the scene alongside the POV character. The outline beats are a safety net, not a leash. If a character does something unexpected that serves the story, follow it. You can reconcile with the outline after.

   - Apply the active style mode from `constitution.md`:
     - `author-sample`: let the voice sample's rhythm and register be your compass — match its frequency, not its content
     - `humanized-ai`: apply the craft principles from `.specify/memory/craft-rules.md` (Dirt Rule, Physical Feedback, Oblique Dialogue, Triple Purpose, Anti-AI Filter) as instincts, not a checklist
   - Follow the key beats from the scene outline in causal order — each beat produces the next. In `--discovery` mode, check against the outline only at natural breaks to confirm coverage.
   - Deliver the dialogue requirements: each critical exchange uses oblique dialogue (deflection before honest answer), includes the misunderstanding/word-failure moment if specified
   - Include the required sensory details; at minimum, the primary anchor from `locations.md` (or the scene outline if no location entry exists) and one Dirt Rule imperfection from the location's options
   - Carry the thematic work through action and image — never state the theme in dialogue
   - Show emotions through involuntary physical reactions — do not name feelings
   - Each character present gets ≥1 physical action per scene, not tagged with emotion
   - Em-dash cap: ≤3 per 1,000 words across the whole chapter
   - Self-check before finalizing: scan for prohibited phrases from the Anti-AI Filter

   **After writing the chapter**:
   - Write draft to `draft/<CHAPTER_ID>_<ChapterName>.md`
   - Update `status` field in the matching `## Scene Outline` entry from `outline` → `in-draft`
   - If `tasks.md` exists in `FEATURE_DIR`: Mark the corresponding task `[x]` in `tasks.md`
   - If `tasks.md` does not exist: Update the `status` field in `plan.md ## Scene Outline` entry to `done`
   - Note any new Chekhov items discovered during drafting — add to the Open Threads table in `plan.md`
   - If the scene changes the physical state of any `LOC-NNN` location (damage, new fixture, change of ownership, destruction), add a row to that location's **State Log** in `locations.md`
   - Note any deviations from the scene outline (additions, cuts, structural changes) as a comment block at the top of the draft file:
     ```
     <!-- DRAFT NOTES

5b. **Generate audiobook draft** (if `OUTPUT_MODE` is `audiobook` or `both` in `constitution.md ## X`):

   Read from `constitution.md ## X. Audiobook Production`:
   - `TTS_ENGINE` (`ssml-cloud`, `elevenlabs`, or `both`)
   - `SPEAKER_MODE` (`single` or `multi`)
   - Speaker Configuration table (narrator + per-character voice IDs)
   - Pronunciation Lexicon table
   - Audiobook Style Hints table

   Source: the prose draft just written in step 5.
   Template: `templates/audiobook-draft-template.md` — use this as the structural model for generated files.

   **Output paths** (create `audiodraft/` in `FEATURE_DIR` if it does not exist):
   - SSML-cloud: `audiodraft/<CHAPTER_ID>_<ChapterName>.ssml`
   - ElevenLabs: `audiodraft/<CHAPTER_ID>_<ChapterName>_el.xml`
   - Lexicon sidecar (ElevenLabs, shared across all chapters): `audiodraft/lexicon.pls`

   **File header** (top of every audiobook draft file, both formats):
   ```yaml
   ---
   chapter_id: [CHAPTER_ID]
   chapter_name: [CHAPTER_NAME]
   audiobook_format: ssml-cloud | elevenlabs | both
   speaker_mode: single | multi
   source_draft: draft/[CHAPTER_ID]_[CHAPTER_NAME].md
   status: audiodraft
   generated: [YYYY-MM-DD]
   ---
   ```

   **Prose-to-audio transformation rules (apply to both formats)**:
   - Strip all markdown formatting: `**bold**` → plain text, `_italic_` marks for `<emphasis>`, `# headings` → chapter title spoken aloud as opening line
   - Em-dash (—) mid-sentence → `<break time="250ms"/>`
   - Ellipsis (…) trailing off → `<break time="400ms"/>`
   - Paragraph break → `<break time="600ms"/>`
   - Scene break (`---` or `* * *`) → `<break time="1500ms"/>`
   - Italics (`_text_`) → `<emphasis level="moderate">text</emphasis>`
   - ALL CAPS → `<emphasis level="strong">text</emphasis>`
   - Every word in the Pronunciation Lexicon → wrap with `<phoneme alphabet="ipa" ph="[IPA]">[WORD]</phoneme>` (SSML) or substitute the ElevenLabs Substitute value inline (EL)
   - Audiobook Style Hints → applied as `<!-- DELIVERY: [hint] -->` comments before the relevant passage, and as `<prosody>` attributes where applicable

   **SSML-cloud output rules** (`ssml-cloud` or `both`):
   - Root element: `<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">`
   - Wrap full chapter narration in `<voice name="[NARRATOR_VOICE_SSML]">`
   - In `multi` speaker mode: each character's dialogue is wrapped:
     ```xml
     </voice>
     <voice name="[CHARACTER_VOICE_SSML]">
       [dialogue text with phonemes and breaks]
     </voice>
     <voice name="[NARRATOR_VOICE_SSML]">
     ```
   - In `single` speaker mode: all text stays inside the narrator `<voice>` block; dialogue gets `<prosody rate="95%" pitch="-2st">` unless a Style Hint overrides it
   - Close with `</voice></speak>`

   **ElevenLabs output rules** (`elevenlabs` or `both`):
   - ElevenLabs v2 API accepts: `<break>`, `<phoneme alphabet="ipa">`, `<emphasis>` — use only these tags
   - In `multi` speaker mode: split the chapter into contiguous per-voice **segments**. Each segment is a self-contained `<speak>` block preceded by a routing comment:
     ```xml
     <!-- VOICE: [EL_VOICE_ID] | role: narrator -->
     <speak>[narration text]<break time="600ms"/></speak>

     <!-- VOICE: [EL_VOICE_ID] | role: [CHARACTER_NAME] -->
     <speak>[dialogue text]</speak>
     ```
   - In `single` speaker mode: one `<speak>` block with `<!-- VOICE: [NARRATOR_EL_VOICE_ID] | role: narrator -->` header
   - ElevenLabs Substitute values from the Pronunciation Lexicon replace the source word directly in the text (the `.pls` file handles phonetic mapping on the EL platform side)
   - Emit an info comment at the top of the file:
     ```xml
     <!-- ELEVENLABS AUDIOBOOK DRAFT
          Chapter:      [CHAPTER_ID] [CHAPTER_NAME]
          Speaker mode: single | multi
          Segments:     N
          Lexicon:      audiodraft/lexicon.pls
          Generated:    [DATE]
          API hint:     POST /v1/text-to-speech/{voice_id}
                        model_id: eleven_multilingual_v2 or eleven_turbo_v2_5
                        Pass each segment's <speak> content as the `text` field. -->
     ```

   **Lexicon sidecar `audiodraft/lexicon.pls`** (ElevenLabs or both — create once, append on each chapter run):
   - If file does not exist, create it with the PLS header and all current Pronunciation Lexicon entries
   - If it exists, append only new entries not already present:
     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <lexicon version="1.0"
              xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
              alphabet="ipa" xml:lang="en">
       <lexeme>
         <grapheme>Caoimhe</grapheme>
         <phoneme>ˈkiːvə</phoneme>
       </lexeme>
     </lexicon>
     ```

   **Report** (append to step 6 output):
   ```
   | Audiobook | audiodraft/[CHAPTER_ID]_[CHAPTER_NAME].ssml  | SSML segments: N |
   | Audiobook | audiodraft/[CHAPTER_ID]_[CHAPTER_NAME]_el.xml | EL segments: N  |
   | Lexicon   | audiodraft/lexicon.pls                        | Entries: N      |
   ```
   If any Pronunciation Lexicon entries still have `[NEEDS CLARIFICATION]` for IPA or Substitute: emit `⚠️ Lexicon incomplete — review audiodraft/lexicon.pls before synthesis.`
          Deviation from outline: [describe any deviation]
          New Chekhov items: [list any]
          Unresolved items: [list any]
     -->
     ```

   **If a new unplanned beat is needed** (discovered during drafting — a missing transition, a required setup scene, etc.):
   - **STOP drafting**. Do not write the chapter yet.
   - Notify the user: "Drafting [CHAPTER_ID] requires an unplanned beat: [description]. This must be added to plan.md before drafting continues."
   - Add a full Scene Outline entry for the new chapter in `plan.md ## Scene Outline` (all required fields: POV, setting, opening hook, key beats, closing beat, etc.)
   - Assign the new chapter a beat ID that fits sequentially (insert fractional if needed, e.g., `A1.103b` for three-act or `JO3.201b` for Hero's Journey)
   - If `tasks.md` exists: Add a corresponding task entry in `tasks.md` immediately after the related task — `plan.md` is updated first, `tasks.md` mirrors it
   - If `tasks.md` does not exist: No task entry needed; the new chapter will be tracked via `plan.md` status updates
   - Resume drafting only after `plan.md` is updated (and `tasks.md` if it exists)
   - **`plan.md` is the authoritative chapter list. `tasks.md` must never contain chapters that are not in `plan.md ## Scene Outline`.**

6. **Stop and report**: After completing the requested chapter(s) (or one beat, if no range specified), report:
   - Chapters drafted and their output paths in `draft/`
   - Word count of each chapter vs. estimated length from scene outline
   - Any story bible violations caught and corrected
   - Any deviations from the scene outline
   - Any `[NEEDS CLARIFICATION]` items encountered
   - Next recommended chapter ID
   - Recommended next task range

7. **Agent context update**: Run the agent script to refresh the story context file with the newly drafted chapters.

8. **Check for extension hooks** (after drafting): check `hooks.after_implement`.

9. **Token Usage Optimization**
   - **Batch RAG Queries**: When multiple documents are listed in `## Required Context`, combine them into a single RAG query where possible (e.g., "character alara and location market details") to reduce the number of separate calls.
   - **Cache Summaries**: Store a `*_summary.md` for any file >5k words (world-building, timeline). Subsequent drafts should load the summary instead of the full file unless a specific detail is missing.
   - **Lazy Loading**: Defer loading of optional sections (e.g., `appendices/`, `research/`) until a `[NEEDS CLARIFICATION]` marker explicitly references them.
   - **Trim Hook Payloads**: Extension hooks should return only essential key/value pairs; avoid returning large blobs of text.
   - **Monitor Token Budget**: Before each major step, estimate the token count of loaded context (approx. 0.75 tokens per word). If projected usage exceeds 8k, drop the lowest‑priority document from the list and note it in the draft notes.
   - **Reuse Draft Notes**: When a draft is re‑run, reuse the previous `<!-- DRAFT NOTES -->` block to avoid re‑loading the same large context.
   - **Avoid Redundant `plan.md` Loads**: Only load the `## Plot Beat Sheet` section when the outline is missing; otherwise rely solely on the outline file.
   - **Compress Inline Tables**: When including tables in the draft output, keep them minimal; use concise markdown or reference an external `tables/` file.
   - **Log Token Consumption**: Append a small comment at the end of each draft file:
     ```
     <!-- Tokens used: [estimated] – context budget: 8k max -->
     ```
     This helps future runs stay within limits.

