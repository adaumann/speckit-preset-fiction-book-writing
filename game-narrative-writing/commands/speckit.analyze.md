---
description: Full structural analysis of all node files — branch integrity, variable coverage, endings reachability, and plan alignment. Run after node drafting phases; for per-node quality checks use speckit.checklist.
handoffs:
  - label: Fix Flagged Nodes
    agent: speckit.revise
    prompt: Fix the structural issues flagged by the analysis report
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Structural issues are fixed. Run a continuity check across all nodes.
    send: true
  - label: Run Per-Node Quality Checks
    agent: speckit.checklist
    prompt: Run per-node quality checks across all drafted nodes
    send: true
---

# speckit.analyze

## Goal

Verify that all drafted node files are structurally sound and internally consistent. Catch dead ends, unreachable nodes, undeclared variables, unreachable endings, and plan mismatches now — not after a full playtest cycle.

Run after node drafting phases. Does not modify any files. For per-node prose and dialogue quality checks, use `speckit.checklist` instead.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- *(no argument)* — analyze all nodes in `nodes/`
- `--act [N]` — scope analysis to a single act
- `--check dead-ends|unreachable|variables|endings|plan|hooks` — run only one class of check
- `--report` — write full analysis output to `analysis-report.md`

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:
1. Confirm `nodes/` directory exists and contains at least one node file.
2. Load `specs/plan.md` — required for reachability and alignment analysis.
3. Load `specs/variables.md` — required for variable declaration check.
4. Load `specs/endings.md` — required for endings reachability check.
5. Load `.specify/memory/constitution.md` — required for hook schema compliance check.

## Operating Constraints

**STRICTLY READ-ONLY**: Do not modify any files. Output a structured analysis report. Offer an optional remediation plan only if the user explicitly asks for one.

**Constitution Authority**: `.specify/memory/constitution.md` is non-negotiable. If a mechanic or structural principle needs to change, that requires a `speckit.constitution` update — not reinterpretation.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Load documents**:
   - **Required**: `nodes/` (all drafted node files), `specs/plan.md`, `specs/variables.md`, `specs/endings.md`, `.specify/memory/constitution.md`
   - **Optional**: `outlines/` (for outline-gate compliance check), `specs/spec.md`, `specs/relationships.md` (for relationship beat coverage check), `specs/timeline.md` (for continuity constraint check)
   - Abort with a clear error if any required document is missing.

3. **Run analysis across these dimensions**:

   **A. Branch Integrity** (dead ends & unreachable nodes) — severity: CRITICAL if blocking
   - Find all non-terminal nodes with 0 outgoing choices
   - Find all nodes where all choice targets are referenced but no corresponding file exists
   - Build the full node?choice?node graph from all node files
   - Identify nodes with no incoming links (orphaned)
   - Cross-reference with `plan.md`: flag plan nodes with no drafted file; flag drafted nodes not in `plan.md`

   **B. Variable Coverage**
   - Scan all `variables_read` and `variables_set` frontmatter fields across all node files
   - Check every variable against `specs/variables.md` — flag undeclared variables as CRITICAL
   - Check for read-before-set: a variable read in a node that has no upstream node setting it on any path to that node — flag as CRITICAL
   - Flag any variable declared in `specs/variables.md` that is never read or set in any node — WARNING

   **C. Endings Reachability**
   - For each ending in `specs/endings.md`, trace whether its required variable conditions can be satisfied on at least one complete path from the opening node to the ending node
   - Flag any ending with no satisfiable path as CRITICAL
   - Flag any ending node referenced in `specs/endings.md` with no drafted node file as CRITICAL

   **D. Flowmap ? Node Alignment**
   - List flowmap nodes that have no drafted file in `nodes/` — WARNING (or CRITICAL if gating an ending)
   - List drafted node files not registered in `plan.md` — WARNING
   - Verify act assignments in node frontmatter match the act assignments in `plan.md` — flag mismatches as WARNING

   **E. Outline Gate Compliance**
   - For each drafted node, check whether a corresponding `outlines/[NODE_ID].md` exists with `status: APPROVED`
   - Flag any node drafted without an APPROVED outline as WARNING (outline gating was bypassed)

   **F. Hook Schema Compliance**
   - For each `variables_set` entry across all nodes, verify the hook type matches the valid hook types defined in `.specify/memory/constitution.md` mechanic schemas
   - Flag invalid or unrecognised hook types as WARNING
   - Flag any NPC trust or state variable that exceeds its declared range in `specs/variables.md` as WARNING

   **G. Relationship Beat Coverage** *(skip if `specs/relationships.md` is absent)*
   - For each REL-NNN in `specs/relationships.md`: verify that all five key beats have a mapped node ID (not `[NEEDS NODE]`) — flag any unmapped beat as WARNING
   - Verify the mapped node exists in `specs/plan.md` — flag missing nodes as CRITICAL if the beat gates an ending

   **H. Timeline Constraint Check** *(skip if `specs/timeline.md` is absent)*
   - For each TC-NNN in `specs/timeline.md`: verify no drafted node with a variable value that satisfies the "before" condition precedes the required fabula event — flag violations as CRITICAL

4. **Output structured report**:

   ```
   ## Structural Analysis Report

   ### CRITICAL Issues (blocking — fix before QA or export)
   - [issue] — [node or file] — [remediation suggestion]

   ### WARNINGS (quality risks, addressable before export)
   - [issue] — [node or file] — [suggestion]

   ### PASS (dimensions with no issues)
   - [dimension]: OK

   ### Summary
   CRITICAL: N | WARNINGS: N | PASS: N
   Nodes analyzed: N | Flowmap nodes: N | Endings checked: N | Variables checked: N | Relationships checked: N | Timeline constraints: [N checked / skipped]
   Recommended action: [clear to QA / fix criticals first / run speckit.revise on flagged nodes]
   ```

   If `--report` is set, write the full details to `analysis-report.md`.

5. **Check for extension hooks (after analysis)**:
   - Look for `hooks.after_analyze` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

6. **Optional remediation plan**: Only if the user explicitly requests it, list the specific file edits needed to resolve CRITICAL issues. The user must approve before any editing commands are invoked.

