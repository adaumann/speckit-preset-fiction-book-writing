---
description: Create a story brief from a natural language story idea — logline, character arcs, scene beats, and plot requirements.
handoffs:
  - label: Build Story Structure
    agent: speckit.plan
    prompt: Create a story structure plan for this brief. The plot structure I want to use is...
  - label: Clarify Story Elements
    agent: speckit.clarify
    prompt: Clarify the story elements in this brief
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before story brief creation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_specify` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook with no `condition` field or a null/empty `condition`, output the appropriate hook block (Optional or Mandatory), then wait for mandatory hook results before continuing.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

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
   - **Assumptions & Scope**: What this story IS and is NOT. Series position. Target word count and audience if known.

6. **Report**: Output the path to the created `spec.md`, the short name used, and any items left as `[NEEDS CLARIFICATION]`.
