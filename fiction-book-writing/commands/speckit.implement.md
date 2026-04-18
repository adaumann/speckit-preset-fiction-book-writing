---
description: Draft scenes and chapters by executing writing tasks from tasks.md, enforcing story bible compliance and checklist gates.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
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

**Check for extension hooks (before drafting)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_implement` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse `FEATURE_DIR` and available documents list.

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
   - After resolving the target chapter ID (from `$ARGUMENTS` or the first unchecked task), look for a matching outline file at `outlines/<CHAPTER_ID>_<ChapterName>-outline.md`
   - If a matching outline file exists:
     - Read its `status` field from the frontmatter
     - If `status: DRAFT` — stop and display:
       ```
       ⚠️ OUTLINE GATE: outlines/<CHAPTER_ID>-outline.md has status: DRAFT.

       Review the scene outline, edit beats and requirements as needed, then set:
           status: APPROVED

       To write this chapter yourself instead, set:
           status: SKIP

       Then re-run /speckit.implement
       ```
     - If `status: SKIP` — do not generate any prose for this chapter. Instead:
       - Report: `⏭ SKIP: <CHAPTER_ID> <ChapterName> — author will write this chapter. No prose generated.`
       - Mark the corresponding task `[x]` in `tasks.md` with a note: `[author-written — no AI draft]`
       - Update the `## Scene Outline` entry status in `plan.md` from `outline` → `author-draft`
       - Advance to the next unchecked task and repeat the outline gate check
     - If `status: APPROVED` — proceed to drafting using the outline file as the working brief (see step 4)
   - If no outline file exists for this chapter — proceed using `plan.md ## Scene Outline` as the working brief (legacy behaviour, no gate applied)

3. **Load context**:
   - Read `tasks.md` — identify the first group of unchecked tasks (respect `[P]` markers for parallel drafting)
   - Read `plan.md` for the full beat sheet and scene outlines (the `## Plot Beat Sheet` and `## Scene Outline` sections are the primary drafting brief)
   - Read `.specify/memory/constitution.md` for story bible (style mode, stylistic parameters, story-specific Anti-AI phrases, series context, audiobook config)
   - Read `.specify/memory/craft-rules.md` for craft rules (Sections II–VI: Dirt Rule, Physical Feedback, Triple Purpose, Oblique Dialogue, universal Anti-AI Filter, active prose profile definition)
   - Read `characters.md` (index) and the POV character's profile at `characters/[name].md` if present (voice signatures, micro-obsessions)
   - Read the relevant section of `timeline.md` for the chapters being drafted
   - Read the `LOC-NNN` block(s) in `locations.md` matching the chapter's setting — load: Sensory Anchors, Atmosphere by Time/Condition row matching `timeline_position`, Character Relationships for the POV character, Dirt Rule detail options, prohibited uses. If `locations.md` does not exist or the location has no entry, continue without it but flag it in the draft notes block.
   - If user specified a chapter ID or range in `$ARGUMENTS` (e.g., `A1.101` or `A1.101–A1.103` for three-act, `JO3.201–JO3.203` for Hero's Journey), use that range
   - If no argument given, use the first unchecked task that has a `draft/` output path

4. **Resolve the target chapter outline**:
   - **Priority order for the working brief**:
     1. If `outlines/<CHAPTER_ID>_<ChapterName>-outline.md` exists with `status: APPROVED` → use the outline file as the sole working brief. Extract: opening hook, beat sequence, character beats, dialogue requirements, sensory anchors, thematic work from the outline file sections.
     2. Otherwise → fall back to `plan.md ## Scene Outline` entry. Extract: POV, setting, timeline position, estimated length, opening hook, key beats (in order), character beats, dialogue requirements, sensory details, thematic work, closing beat.
   - This resolved content is the **working brief** — follow it, do not improvise structure
   - If the working brief contains `[NEEDS CLARIFICATION]` markers, pause and resolve them with the user before drafting
   - If the outline file and `plan.md` conflict on structural beats, the **outline file wins** (it is the author's last-reviewed version). Note the conflict in the draft's `DRAFT NOTES` block.

5. **Draft the chapter**:

   **`--outline-only` mode**: If `$ARGUMENTS` contains `--outline-only`:
   - Run `speckit.outline` behaviour for the target chapter(s) instead of drafting prose
   - Generate `outlines/<CHAPTER_ID>_<ChapterName>-outline.md` with `status: DRAFT`
   - Do **not** write any prose or create any file in `draft/`
   - Report the outline file path(s) and remind the author to review, then either approve or set `status: SKIP` and re-run `/speckit.implement`
   - Stop after generating outlines

   **Output path**: `draft/<CHAPTER_ID>_<ChapterName>.md`
   **Naming convention**: `{PREFIX}{phase}.{beat_number}_{ShortName}.md` where PREFIX is the plot-structure prefix from `constitution.md` (e.g., `A` = three-act, `JO` = Hero's Journey, `SC` = Save the Cat, `KT` = Kishōtenketsu, `FT` = Freytag, `SL` = Story Circle, `FA` = Five-Act, `P` = generic). Examples: `draft/A1.101_Awakening.md`, `draft/JO3.201_SupremeOrdeal.md`
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
   - Confirm the Triple Purpose: this chapter must advance plot + reveal character + deepen world
   - Note the opening hook — the draft MUST open with it (or a refined version true to its intent)
   - Note the closing beat — the draft MUST end with it (off-balance, no tidy summary)

   **While writing** (enforce story bible):
   - Apply the active style mode from `constitution.md`:
     - `author-sample`: match voice, rhythm, and sensory density from the extracted style markers
     - `humanized-ai`: apply Sections II–VI from `.specify/memory/craft-rules.md` (Dirt Rule, Physical Feedback, Oblique Dialogue, Triple Purpose, etc.) plus story-specific Anti-AI phrases from `constitution.md §VII`
   - Follow the key beats from the scene outline in causal order — each beat produces the next
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
   - Mark the corresponding task `[x]` in `tasks.md`
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
   - Add a corresponding task entry in `tasks.md` immediately after the related task — `plan.md` is updated first, `tasks.md` mirrors it
   - Resume drafting only after both files are updated
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
