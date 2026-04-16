---
description: Generate scene quality checklists — triple purpose test, dialogue subtext, sensory detail, off-balance ending, and story bible compliance. "Unit tests for prose."
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## Checklist Purpose: "Unit Tests for Prose"

**CRITICAL CONCEPT**: Scene checklists are **quality gates for prose** — they validate whether a drafted scene fulfills its craft obligations.

**NOT for verifying story events**:
- ❌ NOT "Does this scene match the outline?"
- ❌ NOT "Is the plot logical here?"

**FOR prose quality validation**:
- ✅ "Is the Triple Purpose satisfied?" (completeness)
- ✅ "Is the scene ending off-balance?" (craft)
- ✅ "Are emotions shown through physical reaction, not named?" (style compliance)
- ✅ "Does dialogue contain at least one deflection or misunderstanding?" (dialogue craft)
- ✅ "Are prohibited phrases absent?" (Anti-AI filter)

**Metaphor**: If your scene is a chapter written in prose, the checklist is its unit test suite — testing whether the prose works as prose and the scene fulfills its story bible contract.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before checklist generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_checklist` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

2. **Identify the target**: Determine what the checklist is for from `$ARGUMENTS`:
   - A specific scene file (e.g., "create checklist for scenes/act1-opening.md")
   - An act or phase (e.g., "create checklists for all Act I scenes")
   - The current scene being drafted (if no argument, use the most recently modified scene file)

3. **Ask ≤3 targeted clarifying questions** derived from the scene's specific content:
   - Only ask questions not answerable from the scene file and story brief
   - Focus on: intended emotional register, whether dry irony is appropriate for this POV character, specific Anti-AI phrases to check for this genre/voice
   - Skip if the scene provides enough context

4. **Load context**: Read `.specify/memory/constitution.md` for the active style mode and craft rules. Read `spec.md` for the character arc this scene serves.

5. **Generate the checklist**: Use `templates/checklist-template.md` as structure. Customize the items based on:
   - The scene's POV character (which micro-obsession to check, which voice signature applies)
   - The scene's act/phase (Act I opening scenes have different obligations than Act III climax scenes)
   - Whether dry irony applies (only for permitted characters per constitution.md)
   - Any specific Anti-AI phrases flagged for this genre or voice
   - Whether this is a dialogue-heavy scene vs. action vs. interiority (adjust DLG section weight)

6. **Generate the rating**: After filling in all checklist items, calculate the weighted **RTG — Overall Rating** score:
   - Score each of the five sections (SCN, CHR, DLG, SEN, STB) from 1–10 based on how many items pass
   - Apply the section weights to compute a weighted total
   - Mark the gate table: score ≥ 7 is PASS; any single STB failure or SCN-004 failure is FAIL regardless of score
   - If the scene scores < 7, set Verdict to FAIL and list the top 3 revision priorities

7. **Write checklist file**: Save to `FEATURE_DIR/checklists/<scene-short-name>-checklist.md`

8. **Report**: Output the checklist path, the weighted score, the PASS/FAIL verdict, and the highest-risk items. If FAIL, explicitly state the scene must be revised before drafting continues — invoke `speckit.revise` with the chapter ID and the failing item codes.

   **Audiobook sync note** (append to report; skip if `OUTPUT_MODE` is `book` in `constitution.md ## X`):
   - Check for `audiodraft/<CHAPTER_ID>_<ChapterName>.ssml` and/or `_el.xml`
   - If found: compare `version` field in the audiodraft YAML against the prose draft's `version`. If lower: `⚠️ Audiodraft is stale (prose v[N], audio v[M]) — resync by running speckit.revise or speckit.implement for this chapter.`
   - If not found: `ℹ️ No audiodraft found for this chapter — run speckit.implement to generate one.`
   - If in sync: `✓ Audiodraft in sync (v[N]).`
