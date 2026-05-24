description: Create a detailed story brief from a natural‑language story idea, generating a logline, character arcs, key scene beats, and essential plot requirements.
handoffs:
  - label: Build Story Structure
    agent: speckit.plan
    prompt: Create a story structure plan for this brief. The plot structure I want to use is...
  - label: Clarify Story Elements
    agent: speckit.clarify
    prompt: Clarify the story elements in this brief
    send: true
## User Input
```text
$ARGUMENTS
```
You **MUST** consider the user input before proceeding (if not empty).
## Pre-Execution Checks
**Check for extension hooks (before story brief creation)**:
## Outline
The text the user typed after `/speckit.specify` is the story idea. Assume it is always available in this conversation. Do not ask the user to repeat it unless they provided nothing.
Given that story idea, do this:
1. **Generate a concise short name** (2–4 words) for the story element being specified:
   - Use action-noun or noun-noun format when possible (e.g., "dark-night-arc", "opening-act", "inciting-discovery")
   - Preserve character names and genre terms
   - Keep it short enough to be a directory name
2. **Branch creation** (optional, via hook):
   If a `before_specify` hook ran and output JSON containing `BRANCH_NAME` and `FEATURE_NUM`, note these values. The branch name does not dictate the spec directory name.
3. **Create the spec directory**:
   - Read `.specify/init-options.json` if it exists and check the `numberingScheme` field
   - If `numberingScheme` is `"timestamp"` or `TIMESTAMP`: use `YYYYMMDD-HHMMSS` prefix
   - Otherwise: scan `specs/` directory for existing numbered directories (format `NNN-`) and use the next sequential number (zero-padded to 3+ digits). Also check current git branches for the highest number used. Use the higher of the two values + 1.
   - Create directory: `specs/<prefix>-<short-name>/`
   - **Series naming**: if `series/series-bible.md` already exists and the story is non-standalone, incorporate the book number into the directory name: `specs/<prefix>-book-<N>-<short-name>/` (e.g., `specs/002-book-2-shattered-key/`). Infer N from the next empty row in `## Books in Series`, or ask the user if the table is not yet populated.
4. **Copy the story brief template**:
   - Locate `spec-template.md` using the preset template resolution order
   - Copy it to `specs/<prefix>-<short-name>/spec.md`
5. **Fill the story brief** with the following sections — work through each systematically:
   - **Logline**: One sentence capturing protagonist + goal + obstacle + stakes
   - **Premise**: ~100 words. The dramatic question and central tension. End with: "The central question: [question]?"
   - **Character Arcs**: For each major character, fill: internal wound/false belief, want (external goal), need (thematic truth), transformation arc (from → to), voice/observational register, micro-obsession, key contradiction. Mark P1 (drives main plot), P2, P3. Apply the Independent Arc Test: could this arc be understood in isolation?
   - **Key Scenes**: At least 3 scene beats using Given/When/Then format. Each labeled with arc served and act/phase. These are narrative obligations.
   - **Plot Requirements**: Events that MUST happen for this to be this story. Use MUST language. Mark unknowns as `[NEEDS CLARIFICATION: reason]`.
   - **Key Entities**: Characters table, locations table, Chekhov items table (items introduced that must pay off).
   - **Reader Experience Goals**: What the reader MUST feel, discover, or experience. Measurable.
   - **Assumptions & Scope**: What this story IS and is NOT. Series position. Target word count and audience if known. Additionally:
     - Check whether `series/series-bible.md` exists in the workspace.
     - If it **exists**: read `## Series Parameters` and pre-fill `Series title`. Read `## Books in Series` to determine the next book number and pre-fill `Series position` (e.g., `book 2 of 3`). Set `Series bible path` to `series/series-bible.md`. Emit: `ℹ️ Existing series detected — series title and position pre-filled from series/series-bible.md. Confirm or override.`
     - If it **does not exist** and series position is non-standalone: add a note to the spec — `⚠️ series/series-bible.md does not yet exist — speckit.plan will create it when this book is planned.`
     - If series position is `standalone`: leave Series title and Series bible path fields blank.
6. **Report**: Output the path to the created `spec.md`, the short name used, and any items left as `[NEEDS CLARIFICATION]`.
7. **Update search index** (optional — large projects):
   - If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root.
   - This indexes the new `spec.md` so `speckit.constitution` can query it for genre, tone, and theme inference.
   - If the command fails or the index does not exist, skip silently.

## Goal

Create a complete **story brief** (`spec.md`) that serves as the foundation for all downstream speckit commands. The brief captures the logline, premise, character arcs, key scenes, plot requirements, entities, reader experience goals, and scope assumptions.

## Command

When the `speckit.specify` command is invoked, the LLM should:
1. **Read** the user‑provided story idea (`$ARGUMENTS`).
2. **Perform** pre‑execution checks (extension hooks).
3. **Generate** a concise short name for the spec directory.
4. **Create** the spec directory using the appropriate numbering scheme (timestamp or sequential) and, if applicable, incorporate series information.
5. **Copy** the `spec-template.md` into the new directory as `spec.md`.
6. **Populate** the brief sections listed in the Outline, prompting the user only for information that cannot be inferred (e.g., missing series data, unclear plot requirements).
7. **Report** the location of the created `spec.md` and any remaining `[NEEDS CLARIFICATION]` placeholders.
8. **Optionally update** the search index if it exists.

The LLM must follow this flow exactly and must not modify any files other than the newly created spec directory and its `spec.md`.
