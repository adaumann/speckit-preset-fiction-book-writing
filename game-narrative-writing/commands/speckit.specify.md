---
description: Generate a game story brief from a game concept or high-level brief.
handoffs:
  - label: Clarify Design Elements
    agent: speckit.clarify
    prompt: Clarify the open questions in this game story brief
    send: true
  - label: Build Game Bible
    agent: speckit.constitution
    prompt: Generate the game bible from the approved game story brief
---

# speckit.specify

Turn a game concept brief into a structured game story brief (`spec.md`).

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Optional flags:
- `--update` — revise an existing `spec.md` in the `specs/` directory rather than generating from scratch

## Pre-Execution Checks

**Check for extension hooks (before narrative design doc creation)**:
- Check if `.speckit/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_specify` key.
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook with no `condition` field or a null/empty `condition`, output the appropriate hook block (Optional or Mandatory), then wait for mandatory hook results before continuing.
- If no hooks are registered or `.speckit/extensions.yml` does not exist, skip silently.

**Document checks**:
1. Does a `.specify/memory/constitution.md` already exist?
   - If yes: warn — "A game bible exists. Run `speckit.specify --update` to revise the story brief; avoid contradicting approved world rules."
2. Does a `specs/` directory already contain a `spec.md` in any subdirectory?
   - If yes and `--update` not set: ask user to confirm overwrite or use `--update`.

## Outline

1. **Generate a concise short name** (2–4 words) for the game being specified:
   - Use action-noun or noun-noun format when possible (e.g., `hollow-crown`, `last-signal`, `iron-veil`)
   - Preserve setting terms and genre keywords
   - Keep it short enough to serve as a directory reference

2. **Create the spec directory**:
   - Create directory `specs/` if it does not already exist
   - Read `.speckit/init-options.json` if it exists and check the `numberingScheme` field
   - **Default Naming**: Scan `specs/` for existing numbered directories (format `NNN-`) and use the next sequential number (zero-padded to 3 digits). Also check current git branches for the highest number used. Use the higher of the two + 1.
   - **Timestamp Override**: Only use `YYYYMMDD-HHMMSS` as a prefix if `numberingScheme` is explicitly `"timestamp"` or `TIMESTAMP`.
   - **Series naming**: if `specs/series-bible.md` already exists and this game is non-standalone, incorporate the entry number into the directory name: `specs/<prefix>-game-<N>-<short-name>/` (e.g., `specs/002-game-2-iron-veil/`). Infer N from the next empty row in `## Games in Series`, or ask the user if the table is not yet populated.
   - Otherwise: create directory `specs/<prefix>-<short-name>/` (e.g., `specs/001-hollow-crown/`)

3. **Copy the game story brief template**:
   - Locate `spec-template.md` using the preset template resolution order
   - Copy it to `specs/<prefix>-<short-name>/spec.md`
   - **Language Rule**: The game story brief MUST be generated in English (`en`) by default, regardless of any `[LANGUAGE]` setting in the constitution.

4. **Parse the concept brief** from `$ARGUMENTS` or user input:
   - Extract: premise, tone, genre, setting, player arc shape, approximate node count, target endings, known NPCs
   - Flag any missing mandatory fields as `[NEEDS CLARIFICATION: reason]`

5. **Fill spec.md** working through each section systematically:

   - **Logline**: One sentence capturing player character + central goal + primary obstacle + stakes.

   - **Premise**: ~100 words. The dramatic situation and central tension. End with: "The central question: [question]?"

   - **Opening Node Hook**: What the player MUST know, feel, and suspect by the end of Node 1. Plus what is deliberately withheld.

   - **Player Arc (P1)**: Internal wound / false belief, want, need, transformation range (from ? to per ending direction), player agency expression, key contradiction.

   - **NPC Arcs (P2/P3)**: For each load-bearing NPC:
     - Internal wound / false belief, want, need, transformation arc (from ? to range)
     - Trust hook name (variable that tracks relationship)
     - Independent arc test

   - **Key Relationship Arcs**: Load-bearing player–NPC or NPC–NPC relationships. For each: opens as, stress point, closes as, function (what wound does it force to the surface?).

   - **Branch Structure Overview**: Choose from enum:
     - `linear-with-branches` — single path with local divergence, converges at acts
     - `branching-remerging` — meaningful choice diverges and re-merges at key nodes
     - `fully-branching` — each major choice opens a distinct path to end
     - `hub-and-spoke` — central hub with explorable spokes, returns to hub
     Include: act map (act count, rough node distribution per act, major beat at each act boundary).

   - **Endings Map**: 3–6 planned endings with:
     - Type: `good` / `bad` / `neutral` / `secret` / `true`
     - Rough condition notes (variables / flags that gate this ending)
     - Thematic statement this ending makes

   - **Key Scenes / Nodes**: 5–10 pivotal moments using Given/When/Then format. Each labeled with:
     - Arc served, act placement, branch conditions (if any), variable set
     - These are narrative obligations — they MUST appear in the final game.

   - **Design Requirements**: Events that MUST exist for this to be this game. Use MUST language. Mark unknowns as `[NEEDS CLARIFICATION: reason]`.

   - **Act Boundaries & Structural Beats**: Map design requirements to act beats. Include pacing intent.

   - **Key Entities**:
     - Characters table (name, role, first node, arc priority)
     - Locations table (name, atmosphere note, acts present, notable nodes)
     - Key items table (introduced at, narrative/mechanical payoff, payoff node)
     - World rules table (inviolable facts — physics, social, technical, mechanical, geography)
     - Research domains table (accuracy requirement per domain)

   - **Player Experience Goals**: What the player MUST feel, discover, or experience. Measurable and testable. Use MUST language.

   - **Assumptions & Scope**: What this game IS and is NOT. Additionally:
     - Check whether `specs/series-bible.md` exists in the workspace.
     - If it **exists**: read `## Series Parameters` and pre-fill Series title. Read `## Games in Series` to determine the next entry number and pre-fill Series position (e.g., `game 2 of 3`). Set Series bible path to `specs/series-bible.md`. Emit: `?? Existing series detected — series title and position pre-filled from specs/series-bible.md. Confirm or override.`
     - If it **does not exist** and this is non-standalone: add a note — `?? specs/series-bible.md does not yet exist — speckit.series will create it when this game is planned.`
     - If series position is `standalone`: leave Series title and Series bible path fields blank.
     - Target node count, target endings count, target audience, engine preference (if known).

   - **Open Questions (OQ-NNN)**: Unresolved design decisions that block proceeding. Numbered sequentially.

6. **Output**
   - List all OQ-NNN items as a summary block at the end of `specs/<prefix>-<short-name>/spec.md`
   - Report the full path created and any items left as `[NEEDS CLARIFICATION]`
   - Suggest: "Run `speckit.clarify` to resolve open questions, or `speckit.constitution` to generate the game bible."

7. **Update search index** (optional — large projects):
   - If `.speckit/index/` exists, run: `python scripts/python/index.py update` from the project root.
   - This indexes the new `specs/<prefix>-<short-name>/spec.md` so `speckit.constitution` can query it for genre, tone, and mechanics inference.
   - If the command fails or the index does not exist, skip silently.
