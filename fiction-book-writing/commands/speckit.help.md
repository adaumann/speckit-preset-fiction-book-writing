---
description: Workflow advisor — scans all project files to detect the current state of the manuscript and gives prioritized, opinionated recommendations for what to do next and why. Distinct from speckit.status (which reports numbers); this command reasons about the project and acts as a senior editor guiding the session.
handoffs:
  - label: Show Manuscript Status
    agent: speckit.status
    prompt: Show the full manuscript dashboard with chapter table and word counts
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
- `--focus [phase]` — limit advice to one phase: `planning`, `drafting`, `revision`, `polish`, `submission`
- `--chapter [CHAPTER_ID]` — focused guidance for one specific chapter (e.g. `--chapter A2.201`)
- A free-text question — answer it contextually using the project's actual state (e.g. `"Is my spec ready to plan?"`, `"I'm stuck after chapter 3"`)

---

## Purpose

`speckit.help` is the workflow navigator for the fiction writing preset. It reads every project file, maps the state to the workflow lifecycle, and answers the question: **"What should I do next — and why?"**

**How it differs from `speckit.status`**:
- `speckit.status` reports the numbers: word counts, task completion percentages, chapter status table.
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
| `.specify/memory/constitution.md` | Exists? Style mode set? Plot structure set? Version? |
| `FEATURE_DIR/spec.md` | Exists? Contains `[NEEDS CLARIFICATION]`? Character arc count? Series position? |
| `FEATURE_DIR/plan.md` | Exists? Phase 0 docs generated? Story Bible Check results (any ❌ VIOLATION)? Scene outline count? |
| `FEATURE_DIR/tasks.md` | Exists? Total tasks, checked tasks, next unchecked task ID? `[FEEDBACK]` tasks open? |
| `FEATURE_DIR/research.md` | Exists? Count of OPEN items by priority (HIGH/MEDIUM/LOW)? |
| `FEATURE_DIR/glossary.md` | Exists? Open Consistency Log violations (Fixed: No count)? `[NEEDS CLARIFICATION]` count? |
| `FEATURE_DIR/characters.md` | Exists? Any `[NEEDS CLARIFICATION]` entries? |
| `FEATURE_DIR/characters/` | Profile file count vs. character count in characters.md? |
| `FEATURE_DIR/outlines/` | Exists? Count by status: DRAFT / APPROVED / SKIP? |
| `FEATURE_DIR/draft/*.md` | Count by status: draft / revised / checked / polished? Oldest unrevised `drafted` date? Any `constitution_version` mismatches vs. current? |
| `FEATURE_DIR/audiodraft/` | Exists? Count of `.ssml` and `_el.xml` files? Any with `version` lower than corresponding prose draft (`STALE AUDIODRAFT`)? Any drafted chapters with no matching audiodraft (`MISSING AUDIODRAFT`)? Only evaluated when `OUTPUT_MODE` is `audiobook` or `both` in `constitution.md`. |
| `FEATURE_DIR/checklists/` | Exists? Count of failing gates (incomplete items)? |
| `FEATURE_DIR/feedback/` | Exists? Files with `Status: unprocessed` or `Status: triaged`? |
| `FEATURE_DIR/pov-structure.md` | Exists? Any audit flags? |
| `FEATURE_DIR/subplots.md` | Exists? Any `SP-NNN` entries with no draft coverage? |
| `FEATURE_DIR/relationships.md` | Exists? Any `REL-NNN` entries with missing arc beats or no draft coverage? |
| `FEATURE_DIR/series-bible.md` or `series/series-bible.md` | Exists? Current book registered? Open `SX-NNN` contradictions? |
| `FEATURE_DIR/synopsis.md` | Exists? |
| `FEATURE_DIR/pacing-arc.md` | Exists? (output of `speckit.pacing`) |
| `FEATURE_DIR/query-letter.md` | Exists? Submission tracker rows present? |

---

## Step 2 — Determine Workflow Phase

From the inventory, classify the project into one of these phases. Use the **lowest satisfied gate**:

| Phase | Key signals |
|---|---|
| **0 — No project yet** | `constitution.md` missing OR `spec.md` missing |
| **1 — Planning** | `spec.md` exists; `plan.md` missing OR has `[NEEDS CLARIFICATION]` → `tasks.md` missing |
| **2 — Pre-draft** | `tasks.md` exists; no (`draft/`) OR fewer than 3 chapters drafted |
| **3 — Active drafting** | At least one unchecked draft task; not all chapters drafted |
| **4 — Revision / checking** | All chapters drafted; some still `draft` or `revised` (no checklist pass yet) |
| **5 — Polishing** | All chapters `checked`; some not yet `polished` |
| **6 — Post-draft / submission prep** | All chapters `polished`; `synopsis.md` or `query-letter.md` missing or incomplete |
| **7 — Ready** | All chapters `polished`; synopsis and query letter present; no open CRITICAL feedback tasks |

A project may have signals from multiple phases (e.g., revising some chapters while still drafting others) — report the **primary phase** but surface the cross-phase signals as secondary items.

---

## Step 3 — Build the Guidance Report

Emit the report in this structure:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SPECKIT HELP — [STORY_TITLE or "New Project"]
  Phase: [phase name]   |   [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Section A — Project Snapshot (3–5 lines, no tables)

A brief prose paragraph summarising where the project stands. Include:
- What exists and what is still missing
- Key progress indicator (e.g., "7 of 22 chapters drafted; 2 polished")
- Any single most visible problem (e.g., "12 open research items including 3 HIGH-priority flags")

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
- `spec.md` has `[NEEDS CLARIFICATION]` items and `plan.md` already exists → constitution/spec drift risk
- `plan.md` Story Bible Check has ❌ VIOLATION → blocks drafting
- `research.md` has HIGH-priority OPEN items AND any chapters are in `draft` or later → factual debt compounding
- `checklists/` has chapters with failing gates AND those chapters are already `revised` or `polished` → quality regression
- `outlines/` has `status: DRAFT` entries AND `draft/` has chapters with IDs that match → outline gate was skipped
- `tasks.md` has `[FEEDBACK]` CRITICAL tasks open AND new chapters are being drafted → structural debt
- `series-bible.md` has open `SX-NNN` contradictions → series integrity risk before next book
- `constitution_version` mismatch in any `_v3`+ draft files → story bible changed after polishing
- `OUTPUT_MODE` is `audiobook` or `both` AND `audiodraft/` is absent or has fewer files than `draft/` → audiobook drafts not generated yet; compounding debt if prose revisions continue without audiodraft resync
- Any chapter is `polished` but its audiodraft `version` is lower than the prose `version` → audiodraft trail is stale; audio will not match final prose

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

Things that are not on the critical path but would strengthen the manuscript:

```
⚪ OPTIONAL: [description]
   Command : /speckit.[command] [arguments]
   Value   : [one sentence on what this adds]
```

**Common optional improvements to detect and surface:**
- `glossary.md` has 3+ `[NEEDS CLARIFICATION]` → `speckit.glossary add`
- Characters without individual profile files in `characters/` → `speckit.plan` (regenerate Phase 0)
- `pov-structure.md` absent on a multi-POV spec → `speckit.pov draft`
- `subplots.md` exists but has SP entries with no draft coverage past Act I → `speckit.analyze`
- No `feedback/` directory → no beta readers yet; worth noting for the revision phase
- `speckit.versions` never used (no tagged versions) → suggest tagging the first draft send
- `series-bible.md` not yet created for a non-standalone spec → `speckit.series init`
- All chapters polished but `pacing-arc.md` absent → `speckit.pacing` (tension arc audit before submission)
- `OUTPUT_MODE` is `audiobook` or `both` AND stale or missing audiodrafts exist → `speckit.export audio` to review manifest and identify gaps before synthesis
- All chapters polished but no sensitivity review on record (no session note or annotation in `constitution.md`) → `speckit.sensitivity` (recommend before querying, especially for work featuring communities outside author's experience)
- `subplots.md` exists with SP entries marked unresolved and draft is past Act II → `speckit.subplot resolve` to close dramatic questions before synopsis/query

### Section F — Phase-Relevant Command Cheatsheet

Only show commands relevant to the current phase (not the full list):

```
━━ Commands for this phase ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Show 4–8 commands as: /speckit.command — one-line reminder]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use these per-phase command sets:

**Phase 0–1 (Setup / Planning):**
`speckit.constitution`, `speckit.specify`, `speckit.clarify`, `speckit.brainstorm`, `speckit.research add`, `speckit.series init`

**Phase 2 (Pre-draft):**
`speckit.plan`, `speckit.tasks`, `speckit.analyze`, `speckit.outline`, `speckit.pov`, `speckit.research status`

**Phase 3 (Active drafting):**
`speckit.implement`, `speckit.checklist`, `speckit.continuity`, `speckit.status`, `speckit.glossary audit`, `speckit.research check`, `speckit.subplot check`

**Phase 4 (Revision / checking):**
`speckit.revise`, `speckit.checklist`, `speckit.continuity`, `speckit.pacing`, `speckit.versions diff`, `speckit.glossary check`

**Phase 5 (Polishing):**
`speckit.polish`, `speckit.pacing`, `speckit.sensitivity`, `speckit.versions list`, `speckit.glossary check`, `speckit.continuity`

**Phase 6 (Submission prep):**
`speckit.synopsis`, `speckit.export`, `speckit.query`, `speckit.pacing`, `speckit.sensitivity`, `speckit.feedback`, `speckit.series update`, `speckit.versions tag`

---

## Handling a Free-Text Question

If `$ARGUMENTS` contains a question or sentence (not a flag):

1. Read the question.
2. Perform the full inventory scan (Step 1) to ground the answer in the actual project state.
3. Answer the question directly first (2–4 sentences).
4. Follow with the relevant subset of Sections B–D: blockers if any, the single best next action, and one "coming up" item.
5. Skip Sections E and F unless directly relevant to the question.

Examples:
- *"Is my spec ready to plan?"* → Check spec.md for `[NEEDS CLARIFICATION]`, character arc count, series position completeness, and constitution.md gates. Answer directly: "Yes, proceed" or "No, because X".
- *"I'm stuck after chapter 3"* → Check what tasks.md shows as next unchecked task. Check if chapter 3's checklist has failing gates. Check if research.md has HIGH items relevant to the chapters ahead. Give a concrete unblocking recommendation.
- *"Should I run continuity or polish next?"* → Check chapter statuses. If any are `draft` with no checklist pass, continuity first. If all are `checked`, polish. Explain the gate order.

---

## Handling `--chapter [CHAPTER_ID]`

Scope the report to a single chapter:

1. Find all version files for the chapter ID in `draft/`.
2. Find the checklist file in `checklists/` if present.
3. Find any open feedback tasks in `tasks.md` referencing this chapter ID.
4. Find any continuity issues referencing this chapter in `.specify/memory/constitution.md` or `glossary.md` Consistency Log.
5. Report:
   - Current version and status
   - Open blockers specific to this chapter
   - The single next action for this chapter: run checklist / run revise item X / run polish / already done

---

## Post-Execution Hooks

- Look for `hooks.after_help` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.
