---
description: Targeted chapter revision — rewrites specific failing passages identified by speckit.checklist or speckit.continuity without touching passing content. Produces a versioned draft file with a diff summary.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
handoffs:
  - label: Re-run Checklist
    agent: speckit.checklist
    prompt: Re-run the checklist on the revised draft
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting the next scene in phase order
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).
Expected format: a chapter ID (e.g., `A1.101`) optionally followed by a checklist path (e.g., `A1.101 checklists/A1.101_Awakening-checklist.md`) or a quoted failure description (e.g., `A1.101 "CHR-002 STB-004"`).
If only a chapter ID is given and a matching checklist file exists, load the checklist automatically.

## Pre-Execution Checks

**Check for extension hooks (before revision)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_revise` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Goal

Rewrite only the passages in a drafted chapter that are failing checklist items or continuity checks. Do not touch passing content. Produce a versioned output file and a diff summary so the writer can see exactly what changed and why.

## Operating Constraints

**SURGICAL SCOPE**: Only modify prose that directly causes a flagged failure. Do not improve, tighten, or vary surrounding prose just because it could be better. Scope creep in revision corrupts the isolation of what changed and undermines the versioning model.

**STORY BIBLE AUTHORITY**: `.specify/memory/constitution.md` governs all prose decisions. If a revision cannot fix the failure without violating the story bible, STOP and report the conflict — do not silently violate the bible to pass a checklist item.

**SCENE OUTLINE AUTHORITY**: `plan.md ## Scene Outline` is authoritative. Revision must not alter the scene's structural function: opening hook intent, key beats in causal order, and closing beat must remain intact. Only the *execution* of those beats changes.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

2. **Identify the revision target**:
   - Parse `$ARGUMENTS` for chapter ID. Resolve to `draft/<CHAPTER_ID>_<ChapterName>.md` in `FEATURE_DIR`.
   - If no argument given: scan `checklists/` for the most recently modified file with `Verdict: FAIL` — use its linked chapter as the target.
   - Abort with a clear error if the draft file does not exist or has no valid YAML frontmatter header.

3. **Load failure context**:
   - If a checklist file is provided or auto-detected: read all items marked `❌ FAIL` or `⚠️ WARNING` plus the Top Revision Priorities list.
   - If `$ARGUMENTS` contains quoted item IDs (e.g. `"CHR-002 STB-004"`): treat those item codes as the failure scope.
   - If `$ARGUMENTS` contains a quoted description from `speckit.continuity` (CRITICAL issue text): use that as the failure scope.
   - If none of the above: list the FAIL/WARNING items from the most recent checklist for this chapter and ask the user to confirm the revision scope before proceeding.
   - **Failure scope is fixed at this step.** Do not expand it during revision.

4. **Load required context**:
   - Read `draft/<CHAPTER_ID>_<ChapterName>.md` in full (prose + YAML frontmatter)
   - Read `.specify/memory/constitution.md` — style mode, story-specific Anti-AI phrases; note current `version` for `constitution_version` field
   - Read `.specify/memory/craft-rules.md` — craft rules (Sections II–VI), universal Anti-AI Filter phrases, active prose profile definition
   - Read `plan.md ## Scene Outline` entry for this chapter — opening hook, key beats, closing beat
   - Read `characters/[pov-character-name].md` — voice register, vocabulary pool, micro-obsession state, stress tells, self-deception pattern
   - Read `characters.md` (index) for any secondary characters present in the scene

5. **Pre-revision audit** — for each failing item, identify the exact passage(s) responsible:
   - Quote the specific sentence(s) or paragraph(s) that cause the failure
   - State which checklist item / continuity issue each passage violates and why
   - If a passage cannot be found (item failed due to *absence* of something — e.g., no Dirt Rule imperfection present), note what must be *added* and where

   Present this audit to the user as:
   ```
   ## Revision Scope Confirmation

   | Item | Failing passage / what's missing | Root cause |
   |---|---|---|
   | CHR-002 | "She felt the weight of the moment..." | Emotion named directly; no involuntary physical reaction |
   | STB-004 | "It was a testament to her resilience." | Prohibited phrase |
   | SCN-005 | Closing paragraph [quotes it] | Scene ends on resolved emotion, not off-balance |
   | SEN-003 | [End of paragraph 4] | No Dirt Rule imperfection in the environment description |
   ```

   **Stop and wait for user confirmation** before writing any revised prose. Allow the user to:
   - Approve the scope as-is
   - Remove items from scope ("skip STB-004 fix, I'll handle it manually")
   - Add items to scope ("also fix CHR-003")
   - Provide a direction note for a specific item ("for SCN-005: end on the sound of footsteps, not on dialogue")

6. **Revise each failing passage**:
   For each item in the confirmed scope, in the order they appear in the prose (top to bottom):
   - Write the revised version of only the failing passage
   - Apply all applicable story bible rules (POV, tense, Dirt Rule, Triple Purpose, Anti-AI Filter, voice signature, oblique dialogue, em-dash cap, etc.)
   - Preserve the scene outline's structural intent: if the failing passage is the closing beat, the revised version must still close on an off-balance moment — only the specific mechanism changes
   - After each passage revision, note: which checklist item it addresses and how

7. **Assemble the revised draft**:
   - Replace only the revised passages in the original full draft
   - **Do not alter** any prose outside the confirmed revision scope
   - Increment `version` in the YAML frontmatter (e.g., `version: 1` → `version: 2`)
   - Update `actual_words` field with the new word count
   - Update `constitution_version` to the current value from `constitution.md`
   - Add `revised: [YYYY-MM-DD]` field to the YAML frontmatter (insert after `drafted:`)

8. **Write output files**:
   - **Revised draft**: save as `draft/<CHAPTER_ID>_<ChapterName>_v<N>.md` (e.g., `draft/A1.101_Awakening_v2.md`)
   - **Keep the original** `draft/<CHAPTER_ID>_<ChapterName>.md` unchanged — it is the v1 record
   - **Diff summary**: append a `<!-- REVISION NOTES` comment block at the top of the revised file (after YAML frontmatter), before the chapter prose:
     ```
     <!-- REVISION NOTES v2
          Revised: [YYYY-MM-DD]
          Revision scope: [list of item codes fixed]
          Based on: [checklist file path or "speckit.continuity report" or "manual scope"]

          Changes:
          - CHR-002: Replaced "She felt the weight..." paragraph. Emotion now shown via
            [character micro-obsession tell] and forward-leaning posture instead of named feeling.
          - STB-004: Removed "It was a testament to her resilience." Replaced with
            concrete sensory image: [quote first 8 words of replacement].
          - SCN-005: Closing paragraph rewritten. Now ends on [brief description of off-balance
            closing beat — what sensory/action element the reader is left with].
          - SEN-003: Added Dirt Rule imperfection: [brief description] at [location in scene].

          Unchanged from v1: [everything else]
     -->
     ```

8b. **Sync audiobook drafts** (skip if `OUTPUT_MODE` is `book` in `constitution.md ## X`):

   Check for matching audiobook draft files in `FEATURE_DIR/audiodraft/`:
   - SSML: `audiodraft/<CHAPTER_ID>_<ChapterName>.ssml`
   - ElevenLabs: `audiodraft/<CHAPTER_ID>_<ChapterName>_el.xml`

   If neither file exists: append `⚠️ No audiobook draft found — run speckit.implement to generate one.` to the report. Do not block.

   If audiobook draft(s) exist: regenerate each from the revised prose draft (`draft/<CHAPTER_ID>_<ChapterName>_v<N>.md`) using the full transformation rules from `speckit.implement step 5b`:
   - Apply all prose-to-audio rules: break timing, phonemes from Pronunciation Lexicon, SSML voice blocks / EL segment splits
   - Carry forward speaker configuration and style hints from `constitution.md ## X`
   - **Only changed passages need regeneration.** For passages outside the revision scope, copy the existing audiobook text verbatim — do not re-translate unchanged prose
   - Increment `version` in the audiobook file's YAML frontmatter to match the prose draft version
   - Add `revised: [YYYY-MM-DD]` to the audiobook YAML frontmatter
   - Append a `<!-- AUDIOBOOK REVISION NOTES` block immediately after the YAML header:
     ```xml
     <!-- AUDIOBOOK REVISION NOTES v<N>
          Synced from:  draft/<CHAPTER_ID>_<ChapterName>_v<N>.md
          Synced date:  [YYYY-MM-DD]
          Prose changes that affected audio:
          - [item code]: [brief description of the passage that changed and its audio impact]
          Unchanged segments: [N of N] carried forward from prior audiobook version
     -->
     ```
   - Overwrite the existing audiobook file in place (no versioned copy needed — the prose draft versioning is the source of truth)
   - Update `audiodraft/lexicon.pls` if the revised prose introduced any new words that appear in the Pronunciation Lexicon

9. **Report**:
   ```
   ## Revision Report

   | Item | Status | Change summary |
   |---|---|---|
   | CHR-002 | Fixed | Named emotion → involuntary physical reaction |
   | STB-004 | Fixed | Prohibited phrase removed |
   | SCN-005 | Fixed | Closing beat rewritten to off-balance ending |
   | SEN-003 | Fixed | Dirt Rule imperfection added |

   Revised draft: draft/A1.101_Awakening_v2.md
   Word count: v1 [N] → v2 [N] ([+/- delta])
   Recommendation: Re-run speckit.checklist on the revised draft to confirm all items now pass.
   ```

   If any item could **not** be fixed without violating the story bible or scene outline, report it as BLOCKED:
   ```
   | CHR-005 | BLOCKED | Fixing this would require the character to name their motivation aloud
                          (violates constitution.md IV — Oblique Dialogue). 
                          Resolution: revise the scene outline entry for this chapter to 
                          approach the same character beat from a different angle. |
   ```

10. **Check for extension hooks (after revision)**:
    - Look for `hooks.after_revise` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.
