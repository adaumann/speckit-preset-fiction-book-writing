---
description: Project dashboard — scan all draft chapters, tasks, and checklists to produce a word-count table, status breakdown, and completion estimate. Run at any time during the draft.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
handoffs:
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting the next scene in phase order
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check on all drafted chapters
    send: true
  - label: Run Polish Pass
    agent: speckit.polish
    prompt: Run a final line-edit polish pass on a chapter
    send: true
---

## User Input

```text
$ARGUMENTS
```

Consider user input before proceeding (e.g. a specific act, chapter range, or `--brief` for a one-line summary).

## Purpose

`speckit.status` gives a live snapshot of the manuscript without modifying any files. It is safe to run at any time. It reads frontmatter from draft files and cross-references tasks.md and checklists/ to surface:

- What has been drafted, what is still missing
- Where the manuscript sits in the workflow (drafting / revising / polishing / done)
- Word count actuals vs. estimates
- Outstanding quality gates

---

## Steps

1. **Setup**: Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

2. **Collect chapter data** from `FEATURE_DIR/draft/*.md`:
   - For each `.md` file, parse the YAML frontmatter block
   - Prefer the highest-numbered `_vN.md` version when multiple exist (same stem)
   - Extract per chapter: `chapter_id`, `chapter_name`, `act_phase`, `status`, `estimated_words`, `actual_words`, `drafted` date
   - Count actual body words for any chapter missing `actual_words` in frontmatter
   - If `draft/` is empty or absent: read `OUTPUT_MODE` from `constitution.md ## X. Audiobook Production`.
     - If `OUTPUT_MODE` is `audiobook`: note `No prose drafts (audiobook-only mode)` and proceed directly to the Audiodraft Inventory step below instead of the chapter progress table.
     - Otherwise: note `No chapters drafted yet` and skip the chapter progress table.

   **Audiodraft Inventory** (include when `OUTPUT_MODE` is `audiobook` or `both`, or when `draft/` is absent in audiobook-only mode):
   - Scan `FEATURE_DIR/audiodraft/` for `.ssml` and `_el.xml` files. For each, read `chapter_id`, `chapter_name`, `version`, `status`, `generated` from YAML frontmatter.
   - Cross-reference against `plan.md ## Scene Outline` to identify chapters with no audiodraft (`MISSING`).
   - Print one row per chapter:
     ```
     | Chapter ID | Name | SSML | EL | Audio version | Status |
     |---|---|---|---|---|---|
     | A1.101 | Awakening | ✓ | ✓ | v2 | audiodraft |
     | A1.102 | The Letter | ✗ | ✗ | — | MISSING |
     ```

3. **Collect task data** from `FEATURE_DIR/tasks.md`:
   - Count total tasks vs. completed (`- [x]`) tasks
   - Identify the next unchecked task (chapter ID + name)

4. **Collect checklist data** from `FEATURE_DIR/checklists/` (if it exists):
   - For each checklist file: count total items, completed items, pass/fail status

5. **Build the status report**:

   ### Chapter Progress Table

   Print one row per chapter, sorted by `chapter_id`:

   ```
   | Chapter ID   | Name                          | Act/Phase    | Status    | Est.  | Actual | Polished |
   |---|---|---|---|---|---|---|
   | A1.101       | Awakening                     | Act I        | polished  | 3,200 | 3,440  | _v2      |
   | A1.102       | The Letter                    | Act I        | draft     | 2,800 | 2,650  | —        |
   | A2.201       | Crossing the Threshold        | Act II-A     | outline   | 3,500 | —      | —        |
   ```

   Status values and their meaning:
   - `outline` — scene outlined in plan.md, not yet drafted
   - `in-draft` — actively being written
   - `draft` — written, not yet checked
   - `revised` — passed speckit.revise
   - `checked` — passed speckit.checklist
   - `polished` — passed speckit.polish

   **Status emoji legend** (use in summary only):
   - 🟡 outline / in-draft
   - 🔵 draft / revised
   - 🟢 checked / polished

6. **Build the summary block**:

   ```
   ## Manuscript Summary

   | Metric                  | Value                      |
   |---|---|
   | Total chapters (plan)   | N                          |
   | Drafted                 | N  (N%)                    |
   | Polished                | N  (N%)                    |
   | Total words (actual)    | ~N,NNN                     |
   | Total words (estimated) | ~N,NNN                     |
   | Tasks complete          | N / N  (N%)                |
   | Checklist gates PASS    | N / N                      |
   | Next action             | [chapter ID + name]        |
   | Workflow stage          | [see below]                |
   ```

   **Workflow stage** — infer from the data:
   - `📝 Pre-draft planning` — no chapters drafted yet
   - `✍️ Active drafting` — at least one chapter in `draft` or `in-draft`; not all drafted
   - `🔁 Revision / checking` — all chapters drafted; some still in `draft` or `revised`
   - `✨ Polishing` — all chapters `checked` or `polished`; some not yet `polished`
   - `📦 Ready to export` — all chapters `polished`

7. **Outstanding issues** (if any):
   - Chapters with status `draft` that have been in that state the longest (oldest `drafted` date)
   - Checklist files with failing gates — list chapter name + count of incomplete items
   - Tasks marked `[P]` (parallel) that are unchecked — may be blocking

8. **Word count projection** (if at least 3 chapters are drafted):
   - Calculate average actual/estimated ratio
   - Apply to remaining estimated chapters to project final word count
   - Format: `Projected final: ~N,NNN words (based on N drafted chapters averaging N% of estimate)`

9. **Audiobook draft coverage** (skip entirely if `OUTPUT_MODE` is `book` in `constitution.md ## X`, or if `audiodraft/` does not exist):

   Scan `FEATURE_DIR/audiodraft/` for `.ssml` and `_el.xml` files. For each drafted chapter, check whether a matching audiobook draft exists and whether its `version` frontmatter field matches the prose draft's `version`.

   Append to the summary block:
   ```
   | Audiobook drafts (SSML)   | N / N chapters (N%)  |
   | Audiobook drafts (EL)     | N / N chapters (N%)  |
   | Stale audiodrafts         | N chapters out of sync |
   | Lexicon entries           | N  (audiodraft/lexicon.pls) |
   ```
   If any chapters have a stale or missing audiodraft, list them as:
   `⚠️ MISSING AUDIODRAFT: A1.102, A2.201 — run speckit.implement to generate`
   `⚠️ STALE AUDIODRAFT: A1.101 (prose v3, audio v2) — run speckit.revise or speckit.polish to resync`

10. **If `--brief` is in `$ARGUMENTS`**, collapse everything to two lines:
   ```
   Manuscript: N/N chapters drafted (N%) · ~N,NNN words · Stage: [stage]
   Next: [chapter ID] — [chapter name]
   ```
