---
description: Pre-draft structural alignment check — spec↔plan coverage, act proportions, task completeness. Run after speckit.tasks, before speckit.implement. For post-draft prose analysis use speckit.continuity.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Goal

Verify that `spec.md`, `plan.md`, and `tasks.md` are internally consistent and structurally complete **before any drafting begins**. Catch alignment gaps, missing coverage, and proportion errors now — not after 80,000 words have been written.

Run after `speckit.tasks` has produced a complete `tasks.md`. Does not require any drafted scene files to exist. For post-draft prose analysis (story bible compliance in chapters, character arc continuity, timeline coherence across drafts), use `speckit.continuity` instead.

## Operating Constraints

**STRICTLY READ-ONLY**: Do not modify any files. Output a structured analysis report. Offer an optional remediation plan only if the user explicitly asks for one.

**Story Bible Authority**: The project constitution (`.specify/memory/constitution.md`) is non-negotiable. If a structural principle needs to change, that requires a separate `speckit.constitution` update — not reinterpretation or silent ignoring.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` and parse `FEATURE_DIR`. Load all available documents.

2. **Load documents**:
   - Required: `spec.md`, `plan.md`, `tasks.md`, `.specify/memory/constitution.md`
   - Also load: `characters.md` (index) and `characters/` profiles, `timeline.md`, `world-building.md`, `subplots.md` (if present)
   - Abort with a clear error if any required document is missing
   - Do **not** scan `draft/` — this command is pre-draft only. If draft files are present, note their count in the report but do not analyze them.

3. **Run analysis across these dimensions**:

   **A. Spec ↔ Plan Alignment** (severity: CRITICAL if blocking)
   - Does every character arc in `spec.md` appear in the `plan.md` structure map?
   - Does every Key Scene (Given/When/Then) in `spec.md` have a corresponding task in `tasks.md`?
   - Does every Plot Requirement (`PR-NNN`) map to at least one scene task?
   - Does every Reader Experience Goal (`RG-NNN`) map to at least one scene?
   - Do character arc labels in `tasks.md` (`CA-1`, `CA-2`, etc.) correctly match the arcs declared in `spec.md`?

   **B. Chekhov Item Coverage**
   - Does every Chekhov item in `spec.md` Key Entities have an assigned pay-off scene in `tasks.md`?
   - Does any open thread lack a planned resolution before the final act?

   **C. Act Proportions & Task Coverage**
   - Are act word-count targets approximately balanced per the chosen plot structure from `constitution.md`?
   - Is there a CRITICAL checkpoint task between Phase 1 and Phase 2 in `tasks.md`?
   - Are polish tasks present for: continuity, voice homogeneity, Anti-AI filter, opening/closing image resonance?
   - Does `timeline.md` have internal contradictions or gaps (structural/fabula-level — not cross-referencing draft prose)?

   **D. Subplot Integrity** *(skip if `subplots.md` is absent or `spec.md` has no P2/P3 arcs)*
   - For each `SP-NNN` block in `subplots.md`: does the subplot have all five required beats (inciting incident, first obstacle, midpoint reversal, darkest moment, resolution) mapped to chapter IDs in `plan.md`? Missing beat → CRITICAL.
   - Does any subplot's Arc Absence Log show two or more consecutive acts with no scene → WARNING.
   - Does the Subplot Resolution Checklist have any `Resolved: No` rows → CRITICAL.
   - Does the Convergence Map have any chapter flagged `high` load (3+ arcs) without a scene outline entry that explicitly addresses both arcs → WARNING.
   - Does every `SP-NNN` subplot reference a thematic link from `themes.md` (if `themes.md` exists)? Missing link → WARNING.

   **E. Series Constraints** *(skip entirely if `spec.md` Series Position is `standalone`)*
   - Does `series/series-bible.md` exist? If not: CRITICAL — series bible is required before planning a non-standalone book.
   - Does the `spec.md` Series Position field match the book's row in the series bible `## Books in Series` table?
   - For each character, does their opening state in this book's `characters/[name].md` `## Series Arc State` table match the **closing state** from the preceding book's row in that same table (or the series bible Character State Registry)? Flag any mismatch as CRITICAL.
   - Does any plan-level decision (POV strategy, tense, world rule) contradict an entry in `series/series-bible.md ## Series Canon`? Flag as CRITICAL.
   - Are there any `OPEN` entries in `series/series-bible.md ## Known Contradictions` that involve this book? Flag as CRITICAL.

4. **Output structured report**:

   ```
   ## Pre-Draft Analysis Report

   ### CRITICAL Issues (blocking — do not begin drafting)
   - [issue] — [location] — [remediation suggestion]

   ### WARNINGS (quality risks, addressable during or after drafting)
   - [issue] — [location] — [suggestion]

   ### PASS (dimensions with no issues)
   - [dimension]: OK

   ### Summary
   CRITICAL: N | WARNINGS: N | PASS: N | Existing drafts (not analyzed): N | Subplots checked: N | Series checks: [skipped (standalone) / N issues]
   Recommended action: [clear to draft / address criticals first / run speckit.constitution to resolve structural issues / update series-bible.md]
   ```

5. **Check for extension hooks (after analysis)**:
   - Look for `hooks.after_analyze` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

6. **Optional remediation plan**: Only if the user explicitly requests it, list the specific file edits needed to resolve CRITICAL issues. User must approve before any editing commands are invoked.
