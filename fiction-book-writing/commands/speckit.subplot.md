---
description: Subplot management command â€” add (register a new SP-NNN arc mid-draft), check (audit all subplot arcs for beat gaps, absence streaks, and unresolved dramatic questions), status (dashboard of arc health, draft coverage, and convergence load), and intersect (rebuild the Convergence Map from current plan.md and draft state). Works with subplots.md as the subplot authority; speckit.analyze and speckit.continuity both reference it.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
handoffs:
  - label: Fix Story Structure
    agent: speckit.plan
    prompt: Subplot gaps found â€” revisit the plan to add missing beats
    send: false
  - label: Run Analyze
    agent: speckit.analyze
    prompt: Run a full structural alignment check including subplot integrity
    send: true
  - label: Run Continuity
    agent: speckit.continuity
    prompt: Run a full continuity check including subplot arc tracking
    send: true
  - label: Revise Chapter
    agent: speckit.revise
    prompt: Revise the chapter to serve the subplot arc
    send: false
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* â€” display the subplot status dashboard (same as `status`)
- `add [character name]` â€” register a new subplot arc interactively (e.g. `add Mira`)
- `add [character name] --priority [P2/P3]` â€” skip the priority prompt
- `check` â€” audit all subplot arcs for beat gaps, arc absence streaks, and unresolved dramatic questions (read-only)
- `check [SP-NNN]` â€” scope the audit to a single subplot (e.g. `check SP-002`)
- `intersect` â€” rebuild the Convergence Map from current `plan.md` chapter list and subplot beat sheet chapter IDs
- `resolve [SP-NNN]` â€” mark a subplot's dramatic question as resolved and record the resolution beat
- `status` â€” subplot dashboard: arc count, beat coverage, absence flags, convergence load overview

---

## Purpose

`speckit.subplot` manages `subplots.md` as the active authority for all P2+ character arcs. It bridges the subplot template â€” seeded by `speckit.plan` â€” with the ongoing drafting workflow, where new arcs often emerge mid-draft and existing arcs drift from their planned beat positions.

**What each mode covers**:

| Mode | When to use | Writes files? |
|---|---|---|
| `add` | Any time a new P2/P3 arc is established mid-draft | Yes â€” `subplots.md` only |
| `check` | Before `speckit.analyze`; after completing an act | No â€” read-only |
| `intersect` | After adding chapters to `plan.md` or shifting beat positions | Yes â€” `subplots.md` Convergence Map only |
| `resolve` | When a subplot's dramatic question is answered in draft | Yes â€” `subplots.md` only |
| `status` | Any time â€” overview of subplot arc health | No â€” read-only |

**Integration with other commands**:
- `speckit.plan` seeds `subplots.md` from `spec.md` P2/P3 arcs at plan time.
- `speckit.analyze` checks beat completeness and arc absence streaks using this file.
- `speckit.continuity` tracks arc silence across drafted chapters and updates Arc Absence Log rows.
- `speckit.implement` does not read `subplots.md` directly â€” but scene outlines reference subplot beats; use `speckit.subplot check` to confirm beat assignments before drafting an act.

---

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_subplot` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 â€” Setup and Mode Resolution

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Locate `FEATURE_DIR/subplots.md`. If the file does not exist:
- For `add` mode: create it from `subplots-template.md`. Populate the header from `spec.md` (`[STORY_TITLE]`, `[FEATURE_DIR]`, today's date). Seed Subplot Index from any P2/P3 arcs found in `spec.md` character entries. Emit: `âœ“ Created subplots.md from template. Proceeding to add first subplot.`
- For `check`, `intersect`, `resolve`, or `status`: abort with `âœ— subplots.md not found. Run speckit.subplot add [character] to create it, or run speckit.plan to generate it from the story brief.`

Parse `$ARGUMENTS` for mode, optional SP-NNN or character name, and optional flags. Resolve mode:
- `add â€¦` â†’ **Mode: Add**
- `check â€¦` â†’ **Mode: Check**
- `intersect` â†’ **Mode: Intersect**
- `resolve â€¦` â†’ **Mode: Resolve**
- `status` or *(empty)* â†’ **Mode: Status**

---

## Mode: Add

**Purpose**: Register a new P2 or P3 subplot arc in `subplots.md`.

### Add Step 1 â€” Determine arc priority

If `--priority` was provided, use it. Otherwise display:

```
What arc priority is this subplot?

  P2  â€” A major secondary arc: this character's journey occupies significant
         page-time and has thematic weight (minimum 5 beats required)
  P3  â€” A minor supporting arc: this character influences the plot but their
         arc is resolved quickly or off-page (minimum 3 beats required)

Enter P2 or P3:
```

### Add Step 2 â€” Gather arc fields

Ask in sequence (accept inline `--` flags):

1. **Character name** â€” exact spelling matching `characters.md` entry
2. **Dramatic question** â€” one sentence: what this subplot arc asks and must answer
3. **Wound / false belief** â€” what the character believes that blocks their need
4. **Want (external goal)** â€” what they are consciously pursuing
5. **Need (thematic truth)** â€” what they must learn or accept for arc resolution
6. **Transforms from â†’ to** â€” starting state and ending state in one line
7. **Relationship to main plot** â€” select one:
   - `complicates` â€” creates direct obstacles for P1
   - `mirrors` â€” argues the same theme from a different angle
   - `contrasts` â€” argues against the theme, providing a counter-voice
8. **Thematic link** â€” which theme or motif from `themes.md` this arc carries
9. **Resolution type** â€” `resolved` / `tragic` / `open`

### Add Step 3 â€” Assign beat positions

Load `plan.md` chapter list. For each required beat (P2: 5 beats; P3: 3 beats), ask the author to select the chapter ID where that beat falls, or enter `TBD`:

| Beat | P2 required | P3 required |
|---|---|---|
| Inciting incident | âœ“ | âœ“ |
| First obstacle | âœ“ | optional |
| Midpoint reversal | âœ“ | âœ“ |
| Darkest moment | âœ“ | optional |
| Resolution | âœ“ | âœ“ |

### Add Step 4 â€” Write to subplots.md

- Assign the next available `SP-NNN` ID (scan existing blocks for the highest N).
- Insert a new subplot block after the last existing `SP-NNN` block, using the template structure.
- Add a row to the Subplot Index table.
- Add a row to the Subplot Resolution Checklist.
- **Do not rebuild the Convergence Map automatically** â€” prompt: `Run speckit.subplot intersect to update the Convergence Map with the new subplot.`

### Add Step 5 â€” Report

```
âœ“ SP-NNN registered: [Character Name] â€” [Dramatic Question]

| Field         | Value             |
|---|---|
| ID            | SP-NNN            |
| Priority      | P2 / P3           |
| Beats mapped  | N / 5 (or 3)      |
| TBD beats     | [list or "none"]  |
```

---

## Mode: Check

**Purpose**: Audit all subplot arcs (or a single arc) for structural problems.

Load `plan.md` chapter list and `subplots.md`. For each `SP-NNN` block in scope:

### Check A â€” Beat completeness

| Severity | Condition |
|---|---|
| CRITICAL | A required beat (inciting incident, midpoint reversal, or resolution) has no chapter ID assigned |
| WARNING | An optional beat (first obstacle, darkest moment) has no chapter ID for a P2 arc |
| INFO | A beat chapter ID is listed as `TBD` |

### Check B â€” Arc absence streaks

Cross-reference the Subplot Beat Sheet against `plan.md` act structure:
- Count consecutive acts with no subplot beat assigned
- One consecutive act absent â†’ INFO
- Two consecutive acts absent â†’ WARNING
- Three or more â†’ CRITICAL

Update each row in the Arc Absence Log for the subplot being checked.

### Check C â€” Dramatic question resolution

- Is the subplot's Resolution beat assigned to a chapter ID before or at the same act as the main plot climax? If not â†’ WARNING.
- Is the Resolution row in Subplot Resolution Checklist marked `Yes`? If post-draft and no â†’ CRITICAL.

### Check D â€” Convergence load

Load the Convergence Map. Flag any chapter with 3+ arcs active simultaneously â†’ WARNING (high-load scene; review scene outline).

### Check Report

```
ðŸ“‹ Subplot Audit â€” [STORY_TITLE]

[SP-NNN] [Character]: [Dramatic Question]
  âœ“ / âš ï¸ / âŒ Beat completeness
  âœ“ / âš ï¸ / âŒ Arc absence
  âœ“ / âš ï¸ / âŒ Resolution assignment
  âš ï¸ High-load chapters: [list or "none"]

[Repeat for each SP-NNN in scope]

Summary: N CRITICAL Â· N WARNING Â· N INFO
```

---

## Mode: Intersect

**Purpose**: Rebuild the Convergence Map from current `plan.md` chapter list and all subplot beat sheet chapter assignments.

1. Load `plan.md` chapter list (all chapter IDs in order).
2. Load every `SP-NNN` beat sheet â€” for each chapter ID, mark which subplots have a beat assigned.
3. Determine P1 activity: P1 is active in every chapter by default; mark P1 inactive only if plan.md explicitly notes a chapter belongs to a non-P1 act with no P1 presence.
4. Compute load rating per chapter:
   - 1 arc active â†’ `low`
   - 2 arcs active â†’ `medium`
   - 3+ arcs active â†’ `high`
5. Overwrite the `## Convergence Map` section of `subplots.md` with rebuilt table.
6. Report:

```
âœ“ Convergence Map rebuilt

| Stat                | Value |
|---|---|
| Total chapters      | N     |
| High-load chapters  | N     |
| Medium-load         | N     |
| Low-load            | N     |
```

---

## Mode: Resolve

**Purpose**: Mark a subplot's dramatic question as answered and record the resolution beat.

1. Read the SP-NNN block. Confirm the Resolution beat has a chapter ID assigned; if not, prompt for it.
2. Ask: `Resolution type for SP-NNN: resolved / tragic / open`
3. Update the Subplot Resolution Checklist row: set `Resolved?` to `Yes`, fill `Resolution beat` and `Resolution type`.
4. Update the SP-NNN block's Subplot Brief `Resolution type` field.
5. Report: `âœ“ SP-NNN marked resolved. Update speckit.continuity to verify arc closure in drafted chapters.`

---

## Mode: Status

**Purpose**: Subplot health dashboard â€” no file writes.

```
ðŸ“Š Subplot Status â€” [STORY_TITLE]

Subplots: N total (N P2 Â· N P3)

| ID     | Character | Dramatic question (short) | Beats | Draft coverage | Resolved? | Issue |
|---|---|---|---|---|---|---|
| SP-001 |           |                           | 5/5   | Acts Iâ€“III     | Yes       | âœ“     |
| SP-002 |           |                           | 3/5   | Acts Iâ€“II      | No        | âš ï¸ 2  |

High-load chapters (3+ arcs): [list or "none"]
Unresolved subplots past Act II: [list or "none"]
Subplots with TBD beats: [list or "none"]

Run speckit.subplot check for full detail.
```

---

## Post-Execution Index Update

**Update search index** (optional â€” large projects, applies to all write modes: `add`, `update`, `resolve`):
- If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root after any mode that modifies `subplots.md`.
- Updated subplot entries are re-indexed so `speckit.continuity` and `speckit.implement` can query subplot beats by meaning.
- `status` mode makes no file writes â€” skip the index update for that mode.
- If the command fails or the index does not exist, skip silently.
