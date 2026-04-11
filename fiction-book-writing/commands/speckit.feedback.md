---
description: Ingest beta reader, critique partner, or editor notes — categorize by issue type, map to chapter IDs, generate prioritized revision tasks in tasks.md. Closes the editorial round as a proper workflow step.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -IncludeTasks
handoffs:
  - label: Start Revisions
    agent: speckit.revise
    prompt: Begin targeted revisions for the CRITICAL issues from the feedback log
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check to cross-reference feedback against known continuity issues
    send: true
  - label: Check Project Status
    agent: speckit.status
    prompt: Show current manuscript status and outstanding tasks
    send: true
---

## User Input

```text
$ARGUMENTS
```

Consider user input before proceeding. Accepted arguments:
- A file path or quoted block of raw feedback text to ingest
- A reader name (e.g. `"Jane Doe"`) for labeling the feedback log
- `--reader-type` value: `beta`, `cp` (critique partner), `editor`, `sensitivity`
- `triage` — re-run triage only on an existing feedback log without regenerating tasks
- `tasks` — generate tasks from an already-triaged feedback log

---

## Purpose

`speckit.feedback` turns unstructured reader notes into actionable revision tasks. It:

1. Creates a structured feedback log from raw notes
2. Categorizes issues into five types (Structural / Character / Pacing / Clarity / Factual)
3. Maps issues to specific chapter IDs
4. Assigns severity (CRITICAL / MAJOR / MINOR / NOTE)
5. Appends prioritized revision tasks to `tasks.md`

The feedback log becomes the audit trail for the editorial round — you can see which issues were addressed and which were declined.

---

## Steps

1. **Setup**: Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

2. **Identify the feedback source**:
   - If `$ARGUMENTS` contains a file path → read that file as raw notes
   - If `$ARGUMENTS` contains quoted text → use it directly
   - If a `feedback/` directory exists in `FEATURE_DIR` → list existing feedback log files and ask which to process (or process all unprocessed ones)
   - If nothing provided → ask: "Paste the feedback notes, or provide a file path."

3. **Create or locate the feedback log file**:
   - Target: `FEATURE_DIR/feedback/<reader-name>-<YYYY-MM-DD>.md` (slugify reader name)
   - Use `feedback-template.md` structure
   - Fill Metadata table from `$ARGUMENTS` values and context
   - Paste raw notes verbatim into the **Raw Notes** section

4. **Triage** — parse the raw notes and populate the Categorized Issues tables:

   **Category classification rules**:
   | Keyword signals | Category |
   |---|---|
   | "scene doesn't work", "act feels off", "subplot disappears", "pacing too fast/slow in the act" | S — Structural |
   | "motivation unclear", "character wouldn't do this", "arc inconsistent", "voice shifts" | C — Character |
   | "dragged here", "rushed", "too much internal monologue", "skipped over", "breathless" | P — Pacing |
   | "confused", "lost track of who", "unclear whose POV", "needed more context" | CL — Clarity |
   | "couldn't have known this", "contradicts chapter N", "wrong geography", "world rule broken" | F — Factual/World |

   **Chapter mapping**:
   - When the reader references a chapter number, scene name, or page range, map it to the closest `chapter_id` by cross-referencing `plan.md ## Scene Outline`
   - When no chapter is referenced, mark as `[global]`

   **Severity assignment**:
   - CRITICAL: involves the central arc, POV character's core motivation, or a story-logic break
   - MAJOR: degrades reader experience noticeably, would likely appear in a rejection letter
   - MINOR: surface-level, addressable in polish
   - NOTE: personal preference, stylistic opinion, or "I wonder if…" suggestions

   **Positive notes**: extract any explicit praise or "keep this" comments into the POS table

5. **Resolve duplicates**:
   - If multiple readers flagged the same chapter for the same category, merge into one issue with "N readers" noted in the Description
   - Increment severity if ≥2 readers independently raised the same issue

6. **Generate revision tasks** (unless `triage` mode):
   - Add a section to `tasks.md` under `## Beta / Editorial Round [N]`
   - One task per CRITICAL and MAJOR issue
   - Task format (mirrors existing tasks.md convention):
     ```
     - [ ] [FEEDBACK] [S-001] A2.201 — Restructure the midpoint scene: reader lost the stakes (2 readers)
     - [ ] [FEEDBACK] [C-003] A1.102 — Clarify Elena's motivation for refusing the letter
     ```
   - MINOR issues: add as a single grouped task per category:
     ```
     - [ ] [FEEDBACK] [MINOR-CL] Clarity polish pass — 4 minor clarity notes (see feedback/jane-2026-04-10.md)
     ```
   - NOTE items: do NOT add to tasks.md; they are preserved in the feedback log only
   - Fill the **Revision Tasks Generated** table in the feedback log

7. **Update feedback log status** to `tasks generated`

8. **Report**:
   ```
   ✅ Feedback processed

   | Metric              | Value                                     |
   |---|---|
   | Reader              | [name] ([type])                           |
   | Raw notes           | [N] paragraphs / [N] comments             |
   | Issues found        | [N] (CRITICAL: N, MAJOR: N, MINOR: N, NOTE: N) |
   | Tasks added         | [N] tasks in tasks.md                     |
   | Feedback log        | FEATURE_DIR/feedback/<filename>.md        |
   | Chapters affected   | [list of chapter IDs]                     |
   ```

   If CRITICAL issues found, display them prominently:
   ```
   🔴 CRITICAL issues requiring immediate attention:
   - [S-001] A2.201 — [description]
   - [C-003] A1.102 — [description]
   ```
