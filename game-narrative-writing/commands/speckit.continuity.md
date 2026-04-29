---
description: Validate variable state consistency across all branches, check POV drift, and validate series carry-over variables.
handoffs:
  - speckit.revise: Fix nodes with continuity failures
  - speckit.series: For series carry-over validation specifically
---

# speckit.continuity

Run a full continuity analysis across all node files. Validates variable state consistency on all paths, POV drift, series carry-over variables, and NPC state transitions.

## User Input

Provide one of:
- Nothing — full continuity check across all nodes
- A specific check: `--check variables|pov|npc|series`
- A scope: `--act [N]` to scope to one act

Optional flags:
- `--check variables|pov|npc|series` — run only one class of check
- `--act [N]` — scope to a single act
- `--report` — write output to `continuity-report.md`

## Pre-Execution Checks

1. Confirm `nodes/` contains files to analyze.
2. Load `variables.md` — authoritative variable registry.
3. Load `.speckit/memory/constitution.md` — POV and craft rules.
4. Load `characters/` — NPC state machines and trust thresholds.
5. If `--check series` or `series-bible.md` exists: load `series-bible.md`.
6. If `specs/themes.md` exists: load it for thematic drift and motif checks.
7. If `specs/relationships.md` exists: load it for NPC dynamic consistency checks.
8. If `specs/timeline.md` exists: load it for continuity constraint checks.

## Outline

1. **Variable state consistency**
   - Simulate all reachable paths from NODE-001 through each ending
   - For each path: track variable state at each node
   - Detect: variable read before any set on that path; variable set to value outside declared range; counter exceeding declared max; flag set twice without being cleared
   - Report per-path, per-variable: "PATH [A→C→E]: $trust_mira = 130 at NODE-012 (exceeds max 100)"

2. **POV drift check**
   - Load `player_perspective` from constitution.md
   - Scan all node prose for POV violations:
     - Second-person project: flag any `he/she/they` referring to the player
     - Third-person project: flag any `you` addressing the player
     - Switching project: verify `$pov` variable is set before each POV-dependent passage
   - Report: "POV drift in NODE-[N] line [N]: '[QUOTE]'"

3. **NPC state transition validation**
   - For each NPC: verify trust score changes are applied at the correct nodes
   - Verify that NPC dialogue register matches the trust score range at each node where the NPC speaks
   - Verify that NPC state (alive/dead/hostile) is consistent — NPC dead in NODE-A cannot speak in NODE-B unless NODE-B precedes NODE-A on all paths
   - Report: "[NPC] speaks in NODE-[N] but is dead on PATH [A→B→N]"

4. **Series carry-over validation** (if `series-bible.md` exists or `--check series`)
   - Verify all carry-over variables in `series-bible.md` are declared in `variables.md`
   - Verify each ending's variable state snapshot is achievable on at least one path
   - Report any carry-over variable that is never set before the ending node

5. **Update continuity logs**
   - Append issues to `world-building.md` continuity log and `glossary.md` consistency log
   - Mark resolved issues from previous runs

6. **Thematic drift check** *(skip if `specs/themes.md` is absent)*
   - For each registered motif (MO-NNN): verify it appears in at least 3 drafted nodes; flag < 3 occurrences as WARNING
   - For each act: verify at least one node carries thematic work (node outline "Thematic work" field or prose evidence); two consecutive acts with no thematic work → CRITICAL
   - For each symbol in the Symbol & Object Registry: verify physical state is consistent across nodes (object cannot be in two locations simultaneously); flag inconsistency as CRITICAL
   - Append issues to `specs/themes.md` Thematic Drift Log

7. **NPC relationship consistency check** *(skip if `specs/relationships.md` is absent)*
   - For each REL-NNN: verify the NPC states implied by each key beat are consistent with the variable values set in the corresponding node
   - Verify no node references an NPC as friendly/ally when the active dynamic at that branch point should make them hostile
   - Append issues to `specs/relationships.md` Relationship Drift Log

8. **Timeline constraint check** *(skip if `specs/timeline.md` is absent)*
   - For each TC-NNN constraint: verify no drafted node violates the stated before/after rule
   - Flag any NPC dialogue that reveals information before the fabula event that creates it — CRITICAL

6. **Output**
   - Report summary: "Variable errors: [N] | POV drift: [N] | NPC errors: [N] | Series errors: [N] | Thematic drift: [N] | Relationship errors: [N] | Timeline violations: [N]"
   - If `--report`: write full details to `continuity-report.md`
   - Suggest: "Run `speckit.revise NODE-NNN` to fix flagged nodes."
