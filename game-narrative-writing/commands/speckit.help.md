---
description: Workflow advisor — scans all project files to detect the current state of the game and gives prioritized, opinionated recommendations for what to do next and why. Distinct from speckit.status (which reports numbers); this command reasons about the project and acts as a senior narrative designer guiding the session.
handoffs:
  - label: Show Project Status
    agent: speckit.status
    prompt: Show the full project dashboard with node table and task completion
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

Consider user input before proceeding. Accepted arguments:
- *(no argument)* — full guidance report for the current project state
- `--focus [phase]` — limit advice to one phase: `planning`, `pre-draft`, `drafting`, `quality`, `export`
- `--node [NODE_ID]` — focused guidance for one specific node (e.g. `--node NODE-042`)
- A free-text question — answer it contextually using the project's actual state (e.g. `"Is my flowmap ready to outline?"`, `"I'm stuck after node 12"`)

---

## Purpose

`speckit.help` is the workflow navigator for the game-narrative-writing preset. It reads every project file, maps the state to the workflow lifecycle, and answers the question: **"What should I do next — and why?"**

**How it differs from `speckit.status`**:
- `speckit.status` reports the numbers: node counts, task completion percentages, branch coverage table.
- `speckit.help` reasons about the project: what is blocking progress, what is the highest-value next action, what risks will compound if ignored.

Run `speckit.help` at the start of any working session, when you feel stuck, or when you're not sure which command to use next.

---

## Pre-Execution Checks

- Check if `.specify/extensions.yml` exists. Look for `hooks.before_help`. Process as standard hook block. Skip silently if absent.

---

## Step 1 — Detect Project State

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Perform a **non-blocking inventory scan** — read each file if present, note its absence if not. Never abort because a file is missing; missing files are themselves state signals.

**Files to scan and what to extract**:

| File | Signals to extract |
|---|---|
| `specs/constitution.md` | Exists? POV configured? Mechanic hook schema present? Version? `author_name` filled (not `[PLACEHOLDER]`)? |
| `specs/spec.md` | Exists? Contains `[NEEDS CLARIFICATION]` or open `OQ-NNN` items? |
| `specs/plan.md` | Exists? Total node count? Act count? Ending node count? Branch structure complete? |
| `specs/tasks.md` | Exists? Total tasks, checked tasks, next unchecked task ID? `[FEEDBACK]` tasks open? |
| `specs/variables.md` | Exists? Variable count? Any `[NEEDS CLARIFICATION]` entries? Export names for all configured engines? |
| `specs/mechanics.md` | Exists? Tier 1 hook types defined? Tier 2/3 stubs present? |
| `specs/endings.md` | Exists? Ending count? Any endings with no reachability path noted? |
| `specs/world-building.md` | Exists? World rules defined? Locations mapped? |
| `specs/themes.md` | Exists? Motif registry populated? Any CRITICAL drift in drift log? |
| `specs/relationships.md` | Exists? Any REL-NNN beats unmapped (`[NEEDS NODE]`)? |
| `specs/timeline.md` | Exists? Any TC-NNN constraints without a mapped node? |
| `characters/` | Profile file count vs. NPC count in spec.md? Trust states documented? |
| `outlines/` | Exists? Count by status: DRAFT / APPROVED / SKIP? |
| `draft/<ENGINE>/` | Node file count per engine? Count by status in frontmatter? Engine targets configured? |
| `checklists/` | Exists? Count of failing gates (incomplete items)? |
| `research.md` | Exists? OPEN item count? Any HIGH authenticity flags? |
| `analysis-report.md` | Exists? CRITICAL issue count? Date of last run? |
| `output/<ENGINE>/` | Compiled output present for each configured engine? Playable HTML generated? |
| `series/series-bible.md` or `series-bible.md` | Exists? Current game registered? Open contradictions? Series carry-over variables complete? |
| `ENGINE_CONFIGURATION.md` or `preset.yml` | `export_engines` configured? All target engines have required compilation tooling? |

---

## Step 2 — Determine Workflow Phase

From the inventory, classify the project into one of these phases. Use the **lowest satisfied gate**:

| Phase | Key signals |
|---|---|
| **0 — No project yet** | `constitution.md` missing OR `spec.md` missing |
| **1 — Planning** | `spec.md` exists; `plan.md` missing OR `tasks.md` missing |
| **2 — Pre-draft** | `tasks.md` exists; `variables.md` / `mechanics.md` / `endings.md` incomplete or missing; `outlines/` not yet started |
| **3 — Active drafting** | At least one APPROVED outline; fewer than all planned nodes drafted |
| **4 — Quality** | All planned nodes have a draft file; some still have open checklist failures or unresolved `speckit.analyze` CRITICAL issues |
| **5 — Export-ready** | All nodes pass quality gates; compilation pending or complete |

A project may have signals from multiple phases (e.g., drafting some branches while quality-checking others) — report the **primary phase** but surface cross-phase signals as secondary items.

---

## Step 3 — Build the Guidance Report

Emit the report in this structure:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SPECKIT HELP — [GAME_TITLE or "New Project"]
  Phase: [phase name]   |   [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Section A — Project Snapshot (3–5 lines, no tables)

A brief prose paragraph summarising where the project stands. Include:
- What exists and what is still missing
- Key progress indicator (e.g., "14 of 38 nodes drafted; 6 checklist-approved")
- Any single most visible problem (e.g., "3 undeclared variables detected in last analysis run")

### Section B — Blockers (URGENT)

List only true blockers — things that will cause incorrect or wasted work if not resolved first.

For each blocker:
```
🔴 URGENT: [one-line description]
   Why it matters : [1–2 sentences explaining the downstream risk]
   Fix with       : /speckit.[command] [arguments]
```

**Blocker detection rules:**
- `constitution.md` missing → blocks everything
- `constitution.md` has software development markers (`API`, `CLI`, `TDD`, `microservice`, `library`) → was generated from wrong template; blocks everything
- `spec.md` has open `OQ-NNN` items and `plan.md` already exists → spec drift risk
- `plan.md` has nodes with no drafted file AND those nodes gate an ending → blocks reachability testing
- `variables.md` missing AND nodes are being drafted → undeclared variable risk compounding
- `mechanics.md` missing Tier 1 schemas AND any Tier 1 hooks used in drafts → hook translation risk
- `outlines/` has `status: DRAFT` entries AND a matching node file exists in `draft/` → outline gate was skipped
- `analysis-report.md` exists with CRITICAL issues AND new nodes are still being drafted → structural debt compounding
- `research.md` has HIGH authenticity flags OPEN AND any nodes referencing those topics are drafted → factual debt compounding
- `tasks.md` has `[FEEDBACK]` CRITICAL tasks open AND new nodes are being drafted → structural debt
- `export_engines` configured but no compilation tooling found (tweego.exe missing for sugarcube, inklecate.exe missing for ink) → export will fail
- Engine-specific draft files exist but variables.md has no export names for that engine → compilation will fail
- `series-bible.md` has open contradictions → series integrity risk before export

### Section C — Primary Recommendation (NEXT)

The single highest-value action to take right now:

```
✅ NEXT: [one-line description]
   Why now         : [2–3 sentences of reasoning — what is gained, what is avoided]
   Command         : /speckit.[command] [typical arguments]
   Expected output : [what file or state change this produces]
   Watch for       : [1 thing to check or decide during this step]
```

### Section D — Coming Up (SOON)

2–3 actions that follow logically after the primary recommendation. For each:

```
🔵 SOON: [one-line description]
   Command : /speckit.[command]
   Why     : [one sentence]
```

### Section E — Optional Improvements

Things that are not on the critical path but would strengthen the game:

```
⚪ OPTIONAL: [description]
   Command : /speckit.[command] [arguments]
   Value   : [one sentence on what this adds]
```

**Common optional improvements to detect and surface:**
- `spec.md` has 3+ `[NEEDS CLARIFICATION]` items → `speckit.clarify`
- Characters without individual profile files in `characters/` → `speckit.plan` (regenerate Phase 0 docs)
- `plan.md` exists but `plan-diagram.md` is absent → `speckit.flowmap` (Mermaid graph for visual review)
- `feedback.md` has open items and no corresponding `[FEEDBACK]` tasks in `tasks.md` → `speckit.feedback`
- `series-bible.md` not yet created for a non-standalone game → `speckit.series init`
- All nodes drafted but no `analysis-report.md` → `speckit.analyze --report` (run full audit before final review)
- `outlines/` has SKIP entries that cover ending-gating nodes → worth reviewing whether the skip was intentional
- `draft/<ENGINE>/` populated but `output/` missing → `speckit.compile --all-engines` (generate playable builds)
- All nodes drafted but engine targets not yet tested → `speckit.compile --engine <ENGINE>` (test each target engine)
- Puzzles exist but `puzzles.md` not documented → `speckit.brainstorm puzzles` (document puzzle dependencies)
- POV configured as switching but `pov-structure.md` incomplete → `speckit.pov audit` (verify POV consistency)

### Section F — Phase-Relevant Command Cheatsheet

Only show commands relevant to the current phase (not the full list):

```
━━ Commands for this phase ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Show 4–8 commands as: /speckit.command — one-line reminder]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use these per-phase command sets:

**Phase 0–1 (Setup / Planning):**
`speckit.constitution`, `speckit.specify`, `speckit.clarify`, `speckit.brainstorm`, `speckit.series init`, `speckit.research add`

**Phase 2 (Pre-draft setup):**
`speckit.plan`, `speckit.tasks`, `speckit.flowmap`, `speckit.mechanics`, `speckit.analyze`, `speckit.variables check`, `speckit.research status`

**Phase 3 (Active drafting):**
`speckit.outline`, `speckit.implement`, `speckit.checklist`, `speckit.continuity`, `speckit.status`, `speckit.brainstorm`, `speckit.research check`

**Phase 4 (Quality Review):**
`speckit.analyze`, `speckit.continuity`, `speckit.checklist`, `speckit.revise`, `speckit.flowmap`, `speckit.pacing`, `speckit.status`

**Phase 5 (Export / Compilation):**
`speckit.compile`, `speckit.export`, `speckit.series update`, `speckit.analyze --report`

---

## Handling a Free-Text Question

If `$ARGUMENTS` contains a question or sentence (not a flag):

1. Read the question.
2. Perform the full inventory scan (Step 1) to ground the answer in the actual project state.
3. Answer the question directly first (2–4 sentences).
4. Follow with the relevant subset of Sections B–D: blockers if any, the single best next action, and one "coming up" item.
5. Skip Sections E and F unless directly relevant to the question.

Examples:
- *"Is my plan ready to outline?"* → Check plan.md for node count, variables.md completeness, mechanics.md definitions, and tasks.md existence. Answer directly: "Yes, proceed" or "No, because X".
- *"I'm stuck after node 12"* → Check what tasks.md shows as next unchecked task. Check if node 12's checklist has failing gates. Give a concrete unblocking recommendation.
- *"Should I compile or analyze first?"* → Check whether all planned nodes are drafted. If not all drafted, finish drafting. If all drafted, run analyze for full audit before compilation. Explain the gate order.

---

## Handling `--node [NODE_ID]`

Scope the report to a single node:

1. Find the node file in `draft/<ENGINE>/` for the given NODE_ID.
2. Find the checklist file in `checklists/` if present.
3. Find any open feedback or revision tasks in `tasks.md` referencing this NODE_ID.
4. Find any analysis CRITICAL issues referencing this node in `analysis-report.md`.
5. Report:
   - Current status and outgoing branch count
   - Engines targeted by this node
   - Open blockers specific to this node
   - The single next action: run checklist / run revise item X / approve and move on / already done

---

## Post-Execution Hooks

- Look for `hooks.after_help` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.
