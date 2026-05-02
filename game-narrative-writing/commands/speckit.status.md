---
description: Project dashboard â€” scan all nodes, outlines, tasks, and QA state to produce a progress table, phase breakdown, and next-action recommendation. Run at any time during the project.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
handoffs:
  - label: Continue Outlining
    agent: speckit.outline
    prompt: Generate the next node outline
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting the next approved node
    send: true
  - label: Run Structural Analysis
    agent: speckit.analyze
    prompt: Run a full structural analysis of all node files
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a continuity check across all drafted nodes
    send: true
---

# speckit.status

Print a project status dashboard showing current progress across all phases. Safe to run at any time â€” does not modify any files.

## User Input

```text
$ARGUMENTS
```

Consider user input before proceeding. Accepted arguments:
- *(no argument)* â€” full status dashboard
- `--phase [N]` â€” status for a single phase only
- `--export` â€” export readiness check only
- `--mechanics` â€” mechanic health summary only
- `--brief` â€” two-line summary

## Pre-Execution Checks

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.
2. Locate `tasks.md` â€” if absent, warn: "No tasks file found. Run `speckit.tasks` first." Continue with available data.
3. Locate `specs/plan.md` — required to count total nodes. If absent, note "plan.md not found — node totals unavailable."

## Steps

1. **Collect node data**:
   - Scan `specs/plan.md` for all node IDs, acts, and types (regular / ending)
   - For each node: check `outlines/[NODE_ID].md` status (DRAFT / APPROVED / SKIP / missing) and `nodes/[NODE_ID].md` status (DRAFT / APPROVED / SKIP / missing)
   - Count total nodes, ending nodes separately

2. **Collect task data** from `tasks.md`:
   - Count total tasks vs. completed (`- [x]`) tasks per phase
   - Identify the next unchecked task (node ID + title)
   - Count Phase 0 setup tasks separately

3. **Collect QA data**:
   - Check whether `analysis-report.md` exists â€” extract date and CRITICAL/WARNING counts if present
   - Check whether any continuity report exists â€” extract date and issue counts
   - Check `checklists/` directory (if present): per-checklist pass/fail

4. **Build the node progress table**:

   One row per node, sorted by act then node ID:

   ```
   | Node ID   | Title                    | Act | Outline    | Draft      | Type    |
   |---|---|---|---|---|---|
   | NODE-001  | Arrival at the Station   | 1   | APPROVED   | APPROVED   | regular |
   | NODE-002  | The First Choice         | 1   | APPROVED   | DRAFT      | regular |
   | NODE-003  | Hidden Path              | 1   | DRAFT      | â€”          | regular |
   | END-A     | The Survivor             | 3   | APPROVED   | APPROVED   | ending  |
   ```

   Status values:
   - `APPROVED` â€” reviewed and ready / shipped
   - `DRAFT` â€” generated, not yet reviewed
   - `SKIP` â€” author writes manually
   - `â€”` â€” not yet created

5. **Build the phase summary**:

   ```
   === [GAME_TITLE] STATUS ===

   Nodes: [N] total | [N] outlined (APPROVED) | [N] drafted (APPROVED) | [N] SKIP | [N] not started
   Endings: [N] total | [N] reachable (per endings.md) | [N] drafted

   Phase 0 (Setup):   [complete / N tasks remaining]
     variables.md: âœ“/âœ—  mechanics.md: âœ“/âœ—  endings.md: âœ“/âœ—  world-building: âœ“/âœ—
     NPC profiles: [N/N complete]

   Act 1:   [N/N] outlined (APPROVED) | [N/N] drafted (APPROVED)
   Act 2:   [N/N] outlined (APPROVED) | [N/N] drafted (APPROVED)
   Act 3:   [N/N] outlined (APPROVED) | [N/N] drafted (APPROVED)
   Endings: [N/N] outlined (APPROVED) | [N/N] drafted (APPROVED)

   QA:      analyze last run: [DATE / never] | CRITICAL: [N] | WARNINGS: [N]
            continuity last run: [DATE / never] | issues: [N]
            checklists: [N/N gates passing]

   Export:  Sugarcube: [ready / not ready] | Ink: [ready / not ready]
            dry-run: [passed [DATE] / never run]

   Tasks:   [N/N] complete ([N]%)
   ```

6. **Build the summary block**:

   ```
   ## Project Summary

   | Metric                    | Value                     |
   |---|---|
   | Total nodes (flowmap)     | N                         |
   | Outlines approved         | N  (N%)                   |
   | Nodes drafted (APPROVED)  | N  (N%)                   |
   | Endings drafted           | N / N                     |
   | Tasks complete            | N / N  (N%)               |
   | QA gates passing          | N / N                     |
   | Next action               | [node ID + title]         |
   | Workflow stage            | [see below]               |
   ```

   **Workflow stage** â€” infer from data:
   - `ðŸ“‹ Pre-draft setup` â€” Phase 0 tasks incomplete
   - `âœï¸ Outlining` â€” setup complete; outlines not fully approved
   - `âœï¸ Active drafting` â€” at least one node drafted; not all drafted
   - `ðŸ” QA / revision` â€” all nodes drafted; QA not yet complete
   - `ðŸ“¦ Export ready` â€” all nodes APPROVED, QA passed, no CRITICAL issues

7. **Blockers** (if any):
   - Nodes with `status: DRAFT` (outline not yet approved â€” blocking `speckit.implement`)
   - Open CRITICAL issues from `analysis-report.md`
   - Checklist gates with failing items
   - Variables declared in `specs/variables.md` but not yet used in any node (`[UNDECLARED]` flags from `speckit.analyze`)
   - Phase 0 tasks remaining that gate Act 1 outlining

8. **If `--export` is in `$ARGUMENTS`**:
   - List all nodes with `status != APPROVED` in `nodes/`
   - List any CRITICAL issues from the last `analysis-report.md`
   - State: `Export ready: YES / NO â€” [N] nodes not APPROVED, [N] CRITICAL issues blocking`

9. **If `--brief` is in `$ARGUMENTS`**, collapse to two lines:
   ```
   [GAME_TITLE]: [N/N] nodes drafted ([N]%) Â· [N] endings Â· Stage: [stage]
   Next: [NODE_ID] â€” [title]
   ```

10. **Next recommended action**:
    - If Phase 0 incomplete â†’ `speckit.tasks`
    - If outlines pending approval â†’ `speckit.outline [next node ID]`
    - If nodes pending draft â†’ `speckit.implement [next node ID]`
    - If all drafted, QA not run â†’ `speckit.analyze`
    - If QA passed â†' `speckit.continuity` (cross-branch validation)

11. **If `--mechanics` is in `$ARGUMENTS`**, produce a mechanics health report:
    - Scan all `nodes/NODE-*.md` and `outlines/*.md` for mechanic hook blocks
    - Count usage per hook type (Tier 1 and Tier 2)
    - List all Tier 2 stub hooks in use with their node IDs â€” flag as âš ï¸ STUB
    - List all `MECHANIC:TIMER` check blocks â€” verify each has a `failure_node` downstream in `specs/flowmap.md`; flag missing as âš ï¸ NO FAILURE NODE
    - List all `MECHANIC:ENDING_CONDITION` blocks â€” verify each ending ID exists in `specs/endings.md`; flag unknown IDs as âŒ UNKNOWN ENDING
    - List all `MECHANIC:RANDOM` blocks â€” confirm `variable=` is `type: counter` in `variables.md`
    - Count `hub` tagged nodes in `specs/plan.md` and confirm each has at least one `MECHANIC:VISITED` check
    - Output: `Mechanic health: [N] Tier 1 hooks | [N] Tier 2 stubs | [N] timer gaps | [N] unknown endings | [N] hub nodes`
