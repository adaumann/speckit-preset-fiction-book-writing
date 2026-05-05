---
description: Ingest playtest feedback — categorize issues by type, map to node IDs, assign severity, generate prioritized revision tasks in tasks.md. Closes the playtest round as a proper workflow step.
handoffs:
  - label: Start Revisions
    agent: speckit.revise
    prompt: Begin targeted revisions for the CRITICAL issues from the playtest feedback log
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check to cross-reference feedback against known continuity issues
    send: true
  - label: Run Node Checklists
    agent: speckit.checklist
    prompt: Run quality checklists for the nodes flagged in the feedback log
    send: true
  - label: Check Project Status
    agent: speckit.status
    prompt: Show current project status and outstanding tasks
    send: true
---

# speckit.feedback

Ingest playtest feedback, categorize issues, assign severity, and generate revision tasks in `tasks.md`. The feedback log becomes the audit trail for the playtest round.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- A file path or quoted block of raw playtest notes to ingest
- A tester name (e.g. `"Alice"`) for labeling the feedback log
- `--session [LABEL]` — label the playtest session
- `--tester [ID]` — tester identifier (use "anonymous" if not specified)
- `--target [sugarcube|ink]` — which export was tested
- `--resolve [FB-NNN]` — mark an issue as resolved
- `--summary` — print summary of open issues without ingesting new ones
- `triage` — re-run triage only on an existing feedback log without regenerating tasks
- `tasks` — generate tasks from an already-triaged feedback log

## Pre-Execution Checks

**Check for extension hooks (before feedback processing)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_feedback` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Steps

### Step 1 — Setup

Run `{SCRIPT}` from repo root. Load `nodes/` file list (required to validate node IDs referenced in feedback).

### Step 2 — Identify the Feedback Source

- If `$ARGUMENTS` contains a file path → read that file as raw notes
- If `$ARGUMENTS` contains quoted text → use it directly
- If a `feedback/` directory exists → list existing feedback log files; ask which to process or process all unprocessed ones
- If `--summary` → skip to Step 7 (display open issues, no ingestion)
- If `--resolve [FB-NNN]` → skip to Step 6
- If nothing provided → ask: "Paste the playtest notes, or provide a file path."

### Step 3 — Create or Locate the Feedback Log File

- Target: `feedback/[tester-slug]-[YYYY-MM-DD].md` (slugify tester name)
- Use `templates/feedback-template.md` structure
- Fill Metadata table from `$ARGUMENTS` values and context
- Paste raw notes verbatim into the **Raw Notes** section

### Step 4 — Triage

Parse raw notes and populate the per-category issue tables.

**Category classification rules**:

| Keyword signals | Category |
|---|---|
| "dead end", "can't get to", "wrong node", "missing option", "branch doesn't appear" | BR — Branch |
| "variable not set", "wrong value", "flag missing", "trust didn't change", "hook didn't fire" | VA — Variable |
| "dragged", "rushed", "too long here", "tension dropped", "pacing off" | PA — Pacing |
| "confused", "lost track", "unclear choice", "didn't understand", "needed more context" | CL — Clarity |
| "obvious choice", "no trade-off", "trivial", "one option dominates", "mechanic felt useless" | BA — Balance |
| "contradicts earlier", "NPC wrong state", "world rule broken", "remembered wrong" | CO — Continuity |
| "crashed", "syntax error", "output broken", "wrong passage name", "unsupported tag" | EX — Export |

**Node ID mapping**: when the tester references a passage name, scene label, or description, map to the closest `NODE-NNN` by cross-referencing node file titles and `specs/plan.md`. When no node is identifiable, mark as `NODE-UNKNOWN`.

**Severity assignment**:
- CRITICAL: blocks progression, crashes export, breaks variable state, or creates unwinnable state
- HIGH: significantly degrades experience (major confusion, obvious dominant choice, NPC state contradiction)
- MEDIUM: noticeable but non-blocking; addressable in polish
- LOW: minor style preference or "nice to have"

**Positive notes**: extract any explicit "this worked well" or "keep this" comments into the POS section. Do not revise these away.

### Step 5 — Resolve Duplicates

If multiple testers flagged the same node for the same category, merge into one issue entry with "N testers" noted in the Description. Increment severity if ≥ 2 testers independently raised the same issue.

### Step 6 — Resolve Flow (if `--resolve`)

- Confirm the issue ID exists in the feedback log
- Mark issue as RESOLVED
- Add resolution description and node version where fix was applied
- Update summary counts

### Step 7 — Generate Revision Tasks (unless `triage` mode)

Scan `tasks.md` for existing `## Playtest Round` sections. Determine the next round number: if none exist, use Round 1; if one or more exist, use highest N + 1 **only if the current tester's feedback file was not already processed** (check whether any `[tester-slug·` task IDs already appear in tasks.md — if so, skip task generation and report: `ℹ️ Tasks for this tester already exist in tasks.md. Use the triage argument to re-triage only.`).

Add a section to `tasks.md` under `## Playtest Round [N]` with sub-header: `### [tester-name] — [YYYY-MM-DD] ([target])`

**Per-issue task generation**:
- One task per CRITICAL and HIGH issue:
  ```
  - [ ] [FEEDBACK] [tester-slug·BR-001] NODE-007 — Dead end reached from NODE-004 via choice B (2 testers)
  - [ ] [FEEDBACK] [tester-slug·VA-002] NODE-012 — trust_mira not set before read at NODE-012
  ```
- MEDIUM issues: one grouped task per category:
  ```
  - [ ] [FEEDBACK] [MEDIUM-CL] Clarity polish pass — 3 medium clarity notes (see feedback/alice-2026-04-27.md)
  ```
- LOW issues: do NOT add to tasks.md. Preserved in feedback log only.
- Fill the **Revision Tasks Generated** table in the feedback log.

### Step 8 — Update Feedback Log Status

Update `Status` field in the log Metadata table to `tasks generated`.

### Step 9 — Report

```
✅ Feedback processed

| Metric          | Value                                              |
|---|---|
| Tester          | [name]                                             |
| Session         | [label]                                            |
| Export target   | [sugarcube / ink]                                  |
| Raw notes       | [N] items                                          |
| Issues found    | [N] (CRITICAL: N, HIGH: N, MEDIUM: N, LOW: N)      |
| Tasks generated | [N] (added to tasks.md Playtest Round [N])         |
| Log saved       | feedback/[tester-slug]-[YYYY-MM-DD].md             |
```

If any CRITICAL issues were found:
```
⚠ CRITICAL issues require immediate attention before next playtest:
  [FB-NNN] NODE-NNN — [brief description]
```

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_feedback` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

