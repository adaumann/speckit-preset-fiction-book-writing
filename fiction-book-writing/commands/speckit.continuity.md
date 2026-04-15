---
description: Post-draft prose analysis — story bible compliance, character arc consistency, timeline coherence, and open narrative thread coverage across drafted chapters. Run after speckit.implement. For pre-draft structural alignment use speckit.analyze.
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
If a chapter ID or range is given (e.g., `A1.101` or `JO3.201–JO3.203`), scope all prose-level analysis to only those drafts. Structural dimensions (spec↔plan, act proportions) always run across the full project.

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_continuity` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Goal

Identify story bible violations, continuity errors, and untracked narrative threads in drafted chapters. Run after `speckit.implement` has produced at least one draft file. For pre-draft structural alignment (spec↔plan coverage, task completeness), use `speckit.analyze` instead.

## Operating Constraints

**STRICTLY READ-ONLY**: Do not modify any files. Output a structured analysis report. Offer an optional remediation plan only if the user explicitly asks for one.

**Story Bible Authority**: The project constitution (`.specify/memory/constitution.md`) is non-negotiable. Story bible violations in prose are automatically CRITICAL. If a principle itself needs to change, that requires a separate `speckit.constitution` update followed by the retroactive change protocol.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` and parse `FEATURE_DIR`. Load all available documents.

2. **Load documents**:
   - Required: `spec.md`, `plan.md`, `tasks.md`, `.specify/memory/constitution.md`
   - Required: draft files in `FEATURE_DIR/draft/` — identified via their YAML frontmatter header (`chapter_id`, `beat_id`, `pov_character`, `status`, `constitution_version`). Abort with a clear error if no draft files exist.
   - Also load: `characters.md` (index) and `characters/` profiles, `timeline.md`, `world-building.md`, `locations.md` (if present), `glossary.md` (if present), `subplots.md` (if present)

3. **Draft file inventory**:
   - Scan all `draft/*.md` files (or the scoped range from `$ARGUMENTS`)
   - For each file: confirm YAML frontmatter is present and all required fields are populated
   - Flag as `MALFORMED` any draft missing the header or with empty required fields — these cannot be reliably analyzed
   - Cross-reference each draft's `chapter_id` against `plan.md ## Scene Outline` — report any draft whose `chapter_id` has no matching outline entry (`ORPHAN`)
   - Report any outline entry with `status: in-draft` that has no corresponding draft file (`MISSING DRAFT`)
   - Report any draft whose `constitution_version` does not match the current `constitution.md` version (`STALE CONSTITUTION`)
   - For every `STALE CONSTITUTION` draft: read the `## Change Log` in `constitution.md` and identify all change entries newer than the draft's `constitution_version`. Match the specific principles changed against the draft content to identify likely violations. Output as the `Constitution Change Impact` table in the report.

4. **Run analysis across these dimensions**:

   **A. Story Bible Compliance** (severity: CRITICAL if violated)
   - Does every POV scene honor the POV and tense parameters from `constitution.md`?
   - Do any scene drafts contain prohibited phrases from the Anti-AI Filter?
   - Do scene endings comply with the off-balance ending rule?
   - Is the Triple Purpose (plot + character + world) satisfied in each drafted scene?
   - Is the Dirt Rule satisfied (at least one imperfection per environment)?
   - Does any character name their own worst motivation aloud? (must not)

   **B. Character Arc Consistency in Prose**
   - Are POV character voice signatures distinct from each other across drafts? (Voice Homogeneity test: could a scene from CA-1 be mistaken for CA-2?)
   - Are micro-obsessions present in each POV character's scenes — not just one?
   - Do emotional state progressions in draft YAML headers (`act_phase`, `plot_structure_stage`) match the arc in `characters/[name].md`?
   - Is every P1/P2/P3 arc from `spec.md` reflected in the drafted beats — no arc has gone dark for more than one full act?
   - If `subplots.md` is present: for each `SP-NNN` subplot, compare drafted chapter list against the Subplot Beat Sheet. If a subplot's midpoint reversal or darkest moment beat has been reached in the main plot (per chapter IDs) but has no drafted scene → CRITICAL. Update the Arc Absence Log rows in `subplots.md` for any act where the subplot is absent.

   **C. Timeline & World-State Continuity**
   - Are world-state details (locations, resources, relationship states, object positions) consistent across scene drafts?
   - Do `timeline.md` Continuity Constraints (`TC-NNN`) hold in the drafted chapters — no character knows something before its assigned reveal beat?
   - For non-linear structures: does the syuzhet sequence in drafted chapters correctly map to the fabula without contradictions?
   - Does any draft introduce a new place, object, or factual claim that contradicts `world-building.md`?
   - If `glossary.md` is present: does any drafted chapter use an invented term or proper noun in a spelling, capitalisation, or meaning that contradicts `glossary.md`? Mismatch → WARNING. Append to the Consistency Log in `glossary.md` (date, chapter ID, error, correct form).
   - For each `LOC-NNN` location in `locations.md`: do the drafted scenes that use it apply the primary sensory anchor at least once? If a location appears in 2+ scenes and the primary anchor is absent from all of them → WARNING.
   - Do location State Log entries in `locations.md` match the prose? If a State Log row says a location changed state at beat X, do all drafted scenes set there after beat X reflect that change? Mismatch → CRITICAL.

   **D. Open Narrative Threads**
   - Are there Chekhov items introduced in drafted chapters that are not tracked in `plan.md` Open Threads or `spec.md` Key Entities?
   - Does any open thread in `plan.md` already have its introduction drafted but lack a planned pay-off scene in `tasks.md`?
   - Does any open thread lack a planned resolution before the final act?

   **E. Thematic Consistency** (requires `themes.md`; skip silently with one NOTE if absent)
   - Load `themes.md`. If not present, emit: `NOTE: themes.md not found — thematic drift analysis skipped.` and skip this dimension entirely.
   - For each chapter in the draft scope, compare actual prose content against the "Expected thematic work" column in the Thematic Arc by Chapter table.
     - A chapter with no discernible thematic work → WARNING.
     - Two or more consecutive chapters with no thematic work → CRITICAL.
   - For each `MO-NNN` motif in the Motif Registry:
     - Count actual occurrences across all drafted chapters in scope.
     - If a motif has 0 occurrences in any full drafted act → CRITICAL.
     - If a motif recurs identically with no transformation across 2+ consecutive appearances → WARNING ("motif repetition without escalation").
     - If the chapter mapped to a motif's 3rd or later planned occurrence has been drafted but the motif is absent → CRITICAL.
   - For each `SY-NNN` symbol: verify the object's physical state and ownership are consistent across all draft files where it appears.
   - Append any detected issues to the **Thematic Drift Log** table in `themes.md` (date, chapter ID, issue, severity). This is the only write this command performs on `themes.md`.

   **F. Series Canon Compliance** *(skip entirely if `spec.md` Series Position is `standalone`)*
   - Load `series/series-bible.md`. If not found: CRITICAL — a non-standalone book must have an active series bible at `series/series-bible.md`.
   - For each `SC-NNN` world rule in `## Series Canon`: does any drafted chapter explicitly contradict it? → CRITICAL.
   - For each `STC-NNN` constraint in `## Series Continuity Constraints` whose `Must hold from` value ≤ this book's position: does any drafted chapter portray a character knowledge state, relationship status, or world fact that violates the constraint? → CRITICAL.
   - For each named entity in `## Named Entity Registry`: does any drafted chapter portray that entity in a state that contradicts the registry's canonical value at the opening of this book? → CRITICAL.
   - Does any drafted chapter reference a named entity from a prior book but portray it with properties that contradict its series-canonical state or world rule? → WARNING.
   - Does any `OPEN` row in `## Known Contradictions` reference this book? → CRITICAL — cite the `SX-NNN` code; must be resolved before continuing to draft.
   - After analysis: for each character in scope, update or confirm the latest row in their `## X. Series Arc State` table in `characters/[name].md` to reflect the furthest drafted scene's closing state. This is the only write this dimension performs on character profile files.

5. **Output structured report**:

   ```
   ## Continuity Analysis Report

   ### Draft File Inventory
   | File | chapter_id | Status | Issues |
   |---|---|---|---|
   | draft/A1.101_Awakening.md | A1.101 | OK / MALFORMED / ORPHAN / STALE CONSTITUTION | [detail] |

   ### Constitution Change Impact
   <!-- Present only when one or more drafts are STALE CONSTITUTION. Omit if none. -->
   | Draft | Draft version | Changes since | Likely violations | Action |
   |---|---|---|---|---|
   | draft/A1.101_Awakening.md | v1.0 | v1.1: Added prohibited phrase "hollow ache" | Check prose for "hollow ache" | Revise or clear |

   ### CRITICAL Issues (story bible violations or blocking continuity errors)
   - [issue] — [location] — [remediation suggestion]

   ### WARNINGS (quality risks, addressable in revision)
   - [issue] — [location] — [suggestion]

   ### PASS (dimensions with no issues)
   - [dimension]: OK

   ### Summary
   CRITICAL: N | WARNINGS: N | PASS: N | Malformed drafts: N | Orphan drafts: N | Missing drafts: N | Stale constitution: N | Thematic drift: N | Series violations: N
   Recommended action: [continue drafting / revise flagged chapters (`speckit.revise <chapter_id>`) / run retroactive change protocol / update series-bible.md]
   ```

6. **Agent context update**: Run the agent script to refresh the story context file with the current continuity state.

7. **Check for extension hooks (after analysis)**:
   - Look for `hooks.after_continuity` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

8. **Optional remediation plan**: Only if the user explicitly requests it, list the specific file edits needed to resolve CRITICAL issues. User must approve before any editing commands are invoked.
