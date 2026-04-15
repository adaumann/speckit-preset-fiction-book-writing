---
description: Research tracking command for fiction. Four modes — add (log a new research item or source finding), resolve (mark an item answered and capture the finding), check (scan drafted chapters for claims not backed by research.md), and status (research dashboard showing open items ranked by story risk). Drives task generation in speckit.tasks. Run any time from first story concept through final polish.
handoffs:
  - label: Generate Writing Tasks
    agent: speckit.tasks
    prompt: Regenerate writing tasks to reflect the latest resolved research findings
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a continuity check to verify research findings are correctly applied in drafted chapters
    send: true
  - label: Brainstorm Research Topic
    agent: speckit.brainstorm
    prompt: Brainstorm open research questions for this story
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting — research phase complete
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* — display the research status dashboard (same as `status`)
- `add [topic]` — open an interactive session to log a new research item (e.g. `add Soviet naval ranks`)
- `add [topic] --source "[source]"` — log a finding directly with a source (skips interactive prompts)
- `resolve [R-ID]` — mark a research item resolved and capture findings (e.g. `resolve R003`)
- `resolve [R-ID] --finding "[text]" --source "[source]"` — resolve inline
- `check` — scan all drafted chapters for factual claims not backed by any research item (read-only)
- `check [CHAPTER_ID]` — scope the check to a specific chapter
- `status` — display the research dashboard
- `status --open` — show only OPEN items
- `status --resolved` — show only RESOLVED items

---

## Purpose

`speckit.research` keeps the factual grounding of a story explicit, traceable, and integrated with the drafting workflow. It manages `research.md` as a living document that:

1. Records every domain knowledge gap before it becomes a prose error
2. Captures source findings and maps them to specific scenes and beats
3. Drives research task generation in `speckit.tasks` (tasks are generated from R-items, not static placeholders)
4. Scans drafts for unsupported factual claims after writing begins

**Scope**:
- This command only reads/writes `research.md` and (in `check` mode) reads draft files.
- It does not revise prose — use `speckit.revise` to fix scenes where findings require changes.
- `check` is strictly read-only.

---

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_research` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Setup and Mode Resolution

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Locate `FEATURE_DIR/research.md`. If the file does not exist:
- For `add` mode: create it from `research-template.md`. Populate `## Research Scope` from `spec.md` and `constitution.md` if present (time period, locations, technical domains, cultural context). Emit: `✓ Created research.md from template. Proceeding to add first item.`
- For `resolve`, `check`, or `status` modes: abort with `✗ research.md not found. Run speckit.research add [topic] to create it.`

Parse `$ARGUMENTS` for mode and any inline flags. Resolve mode:
- `add …` → **Mode: Add**
- `resolve …` → **Mode: Resolve**
- `check …` → **Mode: Check**
- `status …` or *(empty)* → **Mode: Status**

---

## Mode: Add

**Purpose**: Log a new research item — a knowledge gap that needs answering before or during drafting.

### Add Step 1 — Parse topic

If `$ARGUMENTS` contains a topic after `add`: use it as the item title. Otherwise prompt:
> `What topic needs research? (e.g. "Soviet naval officer ranks 1991", "symptoms of arsenic poisoning", "18th-century printing presses")`

### Add Step 2 — Context questions

Ask the following. Accept inline flags if provided (`--source`, `--finding`). Skip any question already answered by `$ARGUMENTS`:

1. **Why does this matter?**
   > `Which scene, beat, or character decision requires this knowledge? (e.g. "A1.103 — Mira must give correct orders in the submarine control room")`

2. **Specific questions to answer** (ask for up to 3):
   > `What specific factual questions need answers? Enter each on a new line:`
   Accept free-form text. Each non-empty line becomes one bullet in the `Questions to answer` list.

3. **Authenticity risk** — is this an expert-visible error?
   > `Would a specialist reader catch it if this is wrong? (y/n)`
   If yes: add it to the `## Authenticity Flags` table with a risk description.

4. **Scene impact** (if a scene/beat was named in question 1):
   > `How will the findings change the prose, dialogue, or plot? (leave blank if unknown)`

5. **Existing source** (if `--source` was passed, skip this):
   > `Do you have a source already? If yes, paste or describe it. (leave blank to skip)`
   If a source is provided with a finding: jump to **Add Step 4** (resolve immediately).

### Add Step 3 — Write the item

Auto-assign the next `R-NNN` ID (highest existing ID + 1, starting at `R001` if none exist).

Append the new item to `FEATURE_DIR/research.md ## Research Items`:

```markdown
### R[NNN] — [Topic Name]
**Why this matters**: [scene/beat reference + explanation]
**Questions to answer**:
- [question 1]
- [question 2]
**Findings**: OPEN
**Sources**: —
**Scene impact**: [text or TBD]
```

If the item is an Authenticity Flag: also append a row to `## Authenticity Flags`:

```markdown
| [FLAG — e.g. "Soviet naval ranks, 1991"] | [scene/beat] | [Risk if Wrong] |
```

Confirm:
```
✓ Added: R[NNN] — [Topic Name]   Status: OPEN
  Authenticity flag: [Yes / No]
  Next step: run `speckit.research resolve R[NNN]` when you have findings.
             Or: add it to tasks.md as a research task via `speckit.tasks`.
```

### Add Step 4 — Immediate resolve (if source was provided)

If a source AND finding were provided in Add Step 2: call **Mode: Resolve** for this item inline. Do not prompt again.

---

## Mode: Resolve

**Purpose**: Mark a research item answered and record the finding.

### Resolve Step 1 — Locate item

Parse `R-ID` from `$ARGUMENTS`. Find the matching `### R[NNN]` block in `research.md`. If not found, abort:
```
✗ R[NNN] not found in research.md.
  Run `speckit.research status` to see all item IDs.
```

If the item already has `Status: RESOLVED`, warn and ask: `R[NNN] is already resolved. Update the finding? (y/n)`

### Resolve Step 2 — Gather findings

If `--finding` and `--source` were passed in `$ARGUMENTS`: use them directly.

Otherwise prompt:

1. > `What did you find? (paste or summarise your research finding)`
2. > `Source? (book title + page, URL, expert interview, etc.)`
3. > `Does this change anything in the current plan.md, spec.md, or drafted chapters?`
   - If yes: prompt for a brief note. Append it to the finding block as `**Plan impact**: [note]` — this is not automatically applied; it is a flag for the author to act on.

### Resolve Step 3 — Update research.md

In the `### R[NNN]` block:
- Replace `**Findings**: OPEN` with `**Findings**: [finding text]`
- Replace `**Sources**: —` with `**Sources**: [source text]`
- Add or update `**Plan impact**: [note]` if applicable

Move the block from `## Research Items` to `## Resolved Research` table:

| R[NNN] | [Topic] | [one-sentence finding summary] | [source] |

If the item was in `## Authenticity Flags`: mark it as resolved by appending ` ✓` to its Flag column value.

Confirm:
```
✓ Resolved: R[NNN] — [Topic Name]
  Finding logged. Source: [source summary]
  [Plan impact: (note) — review plan.md and consider running speckit.continuity if chapters are drafted]
  Remaining OPEN items: [N]
```

---

## Mode: Check

**Purpose**: Scan drafted chapters for specific, verifiable factual claims that are not backed by a resolved R-item in `research.md`. Read-only.

### Check Step 1 — Load assets

Load `research.md`. Build two lists:
- **RESOLVED claims**: collect all findings from the `## Resolved Research` table. For each, extract: topic, scene/beat reference, key factual assertions from the finding text.
- **OPEN items**: collect all `R-NNN` blocks with `Findings: OPEN`. Note their scene/beat references.

Determine the chapter scope:
- If `$ARGUMENTS` contains a chapter ID: load only that draft file.
- Otherwise: scan all `FEATURE_DIR/draft/*.md` files. Prefer the highest `_vN` version of each chapter stem.

If no draft files exist, abort: `✗ No draft files found. Run speckit.implement to generate drafts first.`

### Check Step 2 — Scan for unsupported claims

For each draft chapter in scope, identify **specific factual claims** — statements that assert:
- A historical fact (dates, names, events, institutions, technology)
- A technical or procedural detail (how something works, medical/legal/scientific specifics)
- A cultural, geographic, or social detail that requires domain knowledge
- A world-building rule stated as fact (for non-fantasy: real-world accuracy; for fantasy/sci-fi: internal consistency with `world-building.md`)

For each detected claim:

1. Check whether a RESOLVED R-item covers it (topic match, scene reference match, or finding text directly addresses the claim).
   - **Covered** → no flag
2. Check whether an OPEN R-item references the same scene or topic.
   - **Open research pending** → flag as `PENDING`
3. No R-item covers it → flag as `UNSUPPORTED`

### Check Step 3 — Output report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RESEARCH CHECK REPORT
  Scope   : [chapter ID or "all drafted chapters"]
  Chapters checked : [N]
  Date    : [YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### UNSUPPORTED Claims (no R-item covers this)
| Chapter | Claim | Risk | Suggested R-item |
|---|---|---|---|
| A1.103 | "She recited the correct depths for safe periscope operation" | HIGH — expert-visible | Add: R[next] — submarine periscope depth protocols |

### PENDING Claims (OPEN R-item exists but not yet resolved)
| Chapter | Claim | Linked R-item |
|---|---|---|
| A2.201 | "The 1943 rationing cards used blue tokens for fats" | R004 — WWII rationing system |

### COVERED (mention in brief)
N claims checked against resolved research — no issues found.

### Summary
UNSUPPORTED: [N]  PENDING: [N]  COVERED: [N]
Recommended action: [run speckit.research add for each UNSUPPORTED claim / resolve pending R-items before polishing]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Mode: Status

**Purpose**: Research dashboard — live view of all items, coverage, and risk.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RESEARCH STATUS: [STORY_TITLE]
  OPEN: [N]  RESOLVED: [N]  Total: [N]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Open Research Items  (sorted: Authenticity Flags first, then by scene order)
| ID    | Topic                          | Scene/Beat | Authenticity flag |
|-------|--------------------------------|------------|-------------------|
| R003  | Soviet naval ranking system    | A1.103     | ⚠️ HIGH           |
| R007  | 1943 UK rationing card system  | A2.205     | ⚠️ HIGH           |
| R011  | Symptoms of slow arsenic poison| A3.301     | —                 |

### Authenticity Flags (unresolved)
| Flag                          | Scene/Beat | Risk if wrong |
|-------------------------------|------------|---------------|
| Soviet naval ranks, 1991      | A1.103     | Expert readers will catch immediately |
…

### Resolved Research Items
| ID    | Topic                             | Finding (summary)          | Source |
|-------|-----------------------------------|----------------------------|--------|
| R001  | Traditional Japanese burial rites | [one sentence summary]     | [source] |
…

### Research Scope Coverage
| Dimension          | Items | Open | Resolved |
|--------------------|-------|------|----------|
| Time period / era  | [N]   | [N]  | [N]      |
| Geographic         | [N]   | [N]  | [N]      |
| Technical domains  | [N]   | [N]  | [N]      |
| Cultural/social    | [N]   | [N]  | [N]      |
| Specialist         | [N]   | [N]  | [N]      |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If there are OPEN Authenticity Flag items, append:
```
⚠️  [N] high-risk authenticity flag(s) unresolved. Resolve before polishing.
    Run `speckit.research resolve R[NNN]` for each.
```

If all items are resolved, append:
```
✓ All research items resolved. Safe to proceed with speckit.polish.
```

---

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_research` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.
