---
description: Final line-edit pass — prose rhythm, sentence variety, word repetition, filter words, adverb density, and voice register consistency. Runs after speckit.checklist PASS. Distinct from speckit.revise (structural/checklist failures) and speckit.checklist (craft gates).
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
handoffs:
  - label: Run Checklist
    agent: speckit.checklist
    prompt: Run the scene quality checklist before polishing
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting the next scene in phase order
    send: true
---

## Polish Purpose: "Making Prose Invisible"

**CRITICAL CONCEPT**: Polish is the final pass that removes friction between reader and story. It operates at the sentence and paragraph level — not the scene level. A scene that passes `speckit.checklist` is structurally sound; polish makes it feel effortless.

**NOT for structural problems** — use `speckit.revise`:
- ❌ NOT "This scene doesn't have a triple purpose"
- ❌ NOT "The ending isn't off-balance"
- ❌ NOT "This contradicts the story bible"

**FOR prose surface quality**:
- ✅ Sentence rhythm variation (short/long alternation, end-weight)
- ✅ Word repetition within paragraphs and across adjacent paragraphs
- ✅ Filter word removal (`she noticed`, `he felt`, `she saw`, `he heard`)
- ✅ Adverb density reduction (max 1 adverb per 200 words of prose)
- ✅ Weak verb replacement (`was`, `had`, `got`) with active/precise verbs
- ✅ Voice register drift (POV character's vocabulary register slipping)
- ✅ Em-dash and ellipsis overuse
- ✅ Paragraph opening word variety (no two consecutive paragraphs starting with the same word)

**Metaphor**: If `speckit.checklist` is the unit test suite, polish is the linter and formatter — it catches surface patterns that tests don't see.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).
Expected format: a chapter ID (e.g., `A1.101`) or a range (e.g., `A1.101–A1.103`). If empty, polish the most recently drafted chapter with a PASS checklist verdict.

## Pre-Execution Checks

**Check for extension hooks (before polishing)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_polish` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Operating Constraints

**VOICE AUTHORITY**: `.specify/memory/constitution.md` is the final arbiter of what is correct prose. Polish must not "improve" a sentence into a voice that doesn't belong to the POV character. A low-register character must remain low-register even after polishing.

**CHECKLIST GATE**: Do not polish a chapter whose most recent checklist verdict is FAIL. Emit an error and direct the user to run `speckit.revise` first.

**SCOPE**: Only the chapter prose is touched. YAML frontmatter (other than `version`, `actual_words`, and adding `polished:` field) is not altered.

**PROHIBITION**: Do not change the meaning or structural function of any sentence. If a fix requires changing what a sentence communicates, stop and flag it — do not silently rewrite.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

2. **Identify the target**:
   - Parse `$ARGUMENTS` for chapter ID or range. Resolve to `draft/*.md` file(s).
   - If no argument given: find the most recently modified draft file whose matching checklist has `Verdict: PASS`.
   - For each target file, verify the most recent checklist in `checklists/` has `Verdict: PASS`. If FAIL: abort that file with: `⛔ <CHAPTER_ID>: checklist is FAIL — run speckit.revise before polishing.`

3. **Load context**:
   - Read `.specify/memory/constitution.md`: style mode, vocabulary register, story-specific Anti-AI phrases (`§VII`), em-dash cap rule, **Language** (`§VII Language`), **Tone** (`§VII Tone`), **Target Audience** (`§VII Target Audience`), **Tense** (`§VII Tense`), **Sentence Rhythm** (`§VII Sentence Rhythm`). Tone governs emotional temperature and irony during polish — do not neutralise a scene's intended dark humour, bleakness, or warmth while fixing rhythm. Target Audience governs vocabulary ceiling — do not replace simple diction with elevated synonyms when audience is middle-grade or young-adult. Tense governs the required narrative tense; flag any tense drift found during polish as a separate WARNING rather than silently correcting it. Sentence Rhythm provides the story-specific baseline for the rhythm checks (SR-001, SR-002) — apply the author's stated pattern, not a generic alternation rule.
   - Read `.specify/memory/craft-rules.md`: universal Anti-AI Filter phrases, active prose profile rules, voice register standards
   - Read `characters/[pov-character-name].md`: vocabulary pool, vocabulary register, verbal tics, speech-under-stress patterns

   **Language-aware scope**: If `Language ≠ en` (or Language is not set to `en`), the following checks are **English-only and must be SKIPPED**:
   - WR-001 Filter word list (`she noticed`, `he felt`, etc.) — these patterns are English-specific; do not apply to other languages
   - WR-004 Adverb density (the `-ly` suffix rule is English-specific morphology)
   - DI-001 Said-bookism (dialogue attribution norms vary strongly by language)
   - DI-002 Adverb on attribution (same reason)
   For `Language ≠ en`, the following checks are **language-agnostic and always active**: PR-001–PR-004 (rhythm), WR-002 (word repetition), WR-003 (weak verbs), WR-005 (throat-clearing), VR-001–VR-006, DI-003 (double punctuation).
   Notify the user at the start of the audit: `ℹ️ Language is set to [LANGUAGE] — English-specific checks (WR-001, WR-004, DI-001, DI-002) are disabled.`
   - Read `glossary.md` if present: Section V (Usage Rules) — capitalization rules, spelling preferences, terms that must not appear, and terms with restricted meaning. These supplement the Anti-AI Filter for this specific chapter's context.
   - Read author voice sample (if `STYLE_MODE: author-sample`): use it as the rhythm reference for sentence length calibration

4. **Run the polish audit** — scan the chapter prose for each issue category and record every instance:

   **PR — Prose Rhythm**
   - PR-001: Sentence length monotony — 4+ consecutive sentences within ±20% of the same word count
   - PR-002: End-weight violation — sentence ends on a weak/unstressed syllable cluster in a high-tension passage
   - PR-003: Paragraph opening repetition — two or more consecutive paragraphs opening with the same word or construction
   - PR-004: Paragraph length monotony — 4+ consecutive paragraphs of the same approximate length

   **WR — Word-Level Issues**
   - WR-001: Filter word — `she noticed`, `he saw`, `she heard`, `he felt`, `she realized`, `he thought`, `she wondered`, `he knew`, `she looked`, `he watched` (and variants)
   - WR-002: Same content word repeated within 100 words (excluding POV character name, pronouns, conjunctions)
   - WR-003: Weak verb — `was [adjective]`, `had [noun]`, `got [adjective/past participle]` in a position where a precise verb is available
   - WR-004: Adverb count exceeds 1 per 200 words in any 400-word window
   - WR-005: Throat-clearing opener — sentence or paragraph opening that delays the real content (`It was at this point that...`, `She found herself thinking about...`)

   **VR — Voice Register**
   - VR-001: Vocabulary above the POV character's register (word not in their vocabulary pool and not in narration distance)
   - VR-002: Vocabulary below register in a passage requiring precision or authority
   - VR-003: Verbal tic absent from a scene where the POV character is under stress (tic should be present per `characters/[name].md`)
   - VR-004: Em-dash count exceeds constitution.md limit per page-equivalent (every 250 words)
   - VR-005: Ellipsis used to pad or suggest vagueness rather than trailing thought or interrupted speech
   - VR-006: Glossary violation — a term from `glossary.md` is misspelled, incorrectly capitalised, used in a rejected variant form, or used with a meaning that contradicts its story-specific definition (only checked if `glossary.md` is present)

   **DI — Dialogue Internals** (dialogue-line level only; scene-level dialogue is `speckit.checklist` territory)
   - DI-001: Said-bookism — dialogue attribution using a verb other than `said`/`asked` and their tense forms, where the action is not physically distinct
   - DI-002: Adverb on attribution (`said quietly`, `asked nervously`) — remove or show via action beat instead
   - DI-003: Double punctuation with attribution (`"Oh." she said.` → `"Oh," she said.`)

5. **Present the Polish Audit Report** before making any edits:

   ```
   ## Polish Audit: <CHAPTER_ID>

   | Issue ID | Category | Location | Issue | Proposed fix |
   |---|---|---|---|---|
   | PR-001 | Rhythm | Para 3, sentences 2–6 | 5 sentences averaging 12 words | Vary: split sentence 4; merge 5+6 |
   | WR-001 | Filter word | Para 7, line 2 | "She noticed the door was ajar" | "The door stood ajar." |
   | WR-002 | Repetition | Paras 11–12 | "dark" × 3 in 80 words | Replace 2nd instance; remove 3rd |
   | VR-001 | Register | Para 9, line 4 | "ameliorate" — above Theresa's register | Replace with "fix" or "ease" |

   Total issues: N (PR: N | WR: N | VR: N | DI: N)
   Estimated change surface: N sentences / N words affected
   ```

   **Stop and wait for user confirmation** before applying any edits. Allow the user to:
   - Approve all fixes
   - Skip specific items (`skip WR-002 in para 11 — repetition is intentional`)
   - Provide a direction note for an item
   - Approve by category (`apply all WR fixes, skip PR fixes`)

6. **Apply approved fixes** in top-to-bottom order:
   - Make only the changes in the confirmed scope
   - Do not cascade edits beyond the fix (if shortening a sentence changes a nearby rhythm issue that wasn't in scope, leave it — flag it for the next pass)
   - After each fix, verify: the sentence still communicates the same thing; the voice register is still correct; no new repetition has been introduced in the immediate vicinity

7. **Assemble the polished draft**:
   - Write the full chapter with all approved fixes applied
   - Update YAML frontmatter:
     - Increment `version` (e.g., `version: 2` → `version: 3`)
     - Update `actual_words` with new word count
     - Add `polished: [YYYY-MM-DD]` field (insert after `revised:` if present, else after `drafted:`)
   - Save as `draft/<CHAPTER_ID>_<ChapterName>_v<N>.md`
   - Keep all prior versions unchanged

7b. **Sync audiobook drafts** (skip if `OUTPUT_MODE` is `book` in `constitution.md ## X`):

   Check for matching audiobook draft files in `FEATURE_DIR/audiodraft/`:
   - SSML: `audiodraft/<CHAPTER_ID>_<ChapterName>.ssml`
   - ElevenLabs: `audiodraft/<CHAPTER_ID>_<ChapterName>_el.xml`

   If neither file exists: note `⚠️ No audiobook draft found for <CHAPTER_ID> — run speckit.implement to generate one.` in the report. Do not block.

   If audiobook draft(s) exist: regenerate from the polished prose draft using `speckit.implement step 5b` transformation rules:
   - Re-apply all polish fixes at the audio text level:
     - WR-001 filter word removal → the direct prose replacement is used verbatim; no `<voice>` or break changes needed
     - PR-001 / PR-004 rhythm fixes → sentence splits may change `<break>` placement; update break timing to match new sentence boundaries
     - WR-002 word repetition fixes → update the inline text; re-check that affected words are still in the Pronunciation Lexicon if they were wrapped in `<phoneme>` tags
     - VR-004 em-dash reduction → fewer `<break time="250ms"/>` tags; verify count matches revised prose
     - DI-001 / DI-002 said-bookism / adverb-on-attribution fixes → update attribution text in the segment; these are within `<voice>` or narrator segments, not boundary changes
   - **Do not change segment boundaries or voice assignments** unless the polish fix changed a narration-to-dialogue or dialogue-to-narration boundary (rare; flag if it happens)
   - Increment `version` in the audiobook YAML frontmatter to match the polished prose version
   - Add `polished: [YYYY-MM-DD]` to the audiobook YAML frontmatter
   - Append a `<!-- AUDIOBOOK POLISH NOTES` block immediately after the YAML header:
     ```xml
     <!-- AUDIOBOOK POLISH NOTES v<N>
          Synced from:  draft/<CHAPTER_ID>_<ChapterName>_v<N>.md
          Polished:     [YYYY-MM-DD]
          Audio changes: N (break adjustments: N | phoneme updates: N | text fixes: N)
          Segment boundary changes: none | [describe if any]
     -->
     ```
   - Overwrite the existing audiobook file in place

8. **Append polish notes** to the top of the polished file (after YAML frontmatter, before prose):
   ```
   <!-- POLISH NOTES v<N>
        Polished: [YYYY-MM-DD]
        Issues fixed: N (PR: N | WR: N | VR: N | DI: N)
        Issues skipped: [list with reason]
        Net word delta: [+N / -N words]
   -->
   ```

9. **Report**:
   - Path to polished file
   - Issues fixed vs. skipped
   - Net word delta
   - Any items flagged during fixing that require meaning-change review (user must decide)
   - Audiobook draft sync result (regenerated / not found / skipped)
   - If no issues were found: `✅ <CHAPTER_ID>: prose is clean — no polish changes needed.`

10. **Check for extension hooks** (after polishing): check `hooks.after_polish` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

11. **Update search index** (optional — large projects):
    - If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root.
    - Polished draft files are re-indexed incrementally so continuity and research checks query the final prose.
    - If the command fails or the index does not exist, skip silently.