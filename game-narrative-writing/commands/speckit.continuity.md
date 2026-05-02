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
- A specific check: `--check variables|pov|npc|dialogue|glossary|locations|relationships|series|timeline|thematic`
- A scope: `--act [N]` to scope to one act

Optional flags:
- `--check [types]` — run only specific checks (comma-separated: variables, pov, npc, dialogue, glossary, locations, relationships, series, timeline, thematic)
- `--act [N]` — scope to a single act
- `--report` — write output to `continuity-report.md`
- `--strict` — require all nodes to have `polished: [date]` before continuity check (default: optional)

## Pre-Execution Checks

1. Confirm `draft/` contains node files to analyze.
2. Load `variables.md` — authoritative variable registry.
3. Load `.specify/memory/constitution.md` — POV, craft rules, and prose profile.
4. Load `characters/` — NPC state machines, trust thresholds, dialogue registers.
5. Load `.specify/memory/craft-rules.md` — dialogue style rules per prose profile.
6. If `--strict`: verify all node files have `polished: [date]` in frontmatter; warn if not found and continue.
7. If `specs/glossary.md` exists: load for terminology consistency checks.
8. If `specs/locations.md` exists: load for location state consistency checks.
9. If `--check series` or `series-bible.md` exists: load `series-bible.md`.
10. If `specs/themes.md` exists: load it for thematic drift and motif checks.
11. If `specs/relationships.md` exists: load it for NPC dynamic consistency checks.
12. If `specs/timeline.md` exists: load it for continuity constraint checks.

## Outline

1. **Variable state consistency**
   - Simulate all reachable paths from NODE-001 through each ending
   - For each path: track variable state at each node
   - Detect: variable read before any set on that path; variable set to value outside declared range; counter exceeding declared max; flag set twice without being cleared
   - Report per-path, per-variable: "PATH [A?C?E]: $trust_mira = 130 at NODE-012 (exceeds max 100)"

2. **POV drift check**
   - Load `player_perspective` from constitution.md
   - Scan all node prose for POV violations:
     - Second-person project: flag any `he/she/they` referring to the player
     - Third-person project: flag any `you` addressing the player
     - Switching project: verify `$pov` variable is set before each POV-dependent passage
   - Report: "POV drift in NODE-[N] line [N]: '[QUOTE]'"

3. **NPC state transition validation**
   - Load `.specify/memory/craft-rules.md` for dialogue style rules per prose profile (NPC Voice & Dialogue section)
   - For each NPC: verify trust score changes are applied at the correct nodes
   - Verify that NPC dialogue register matches the trust score range at each node where the NPC speaks, and matches the dialogue style rules for the active prose profile
   - Verify that NPC state (alive/dead/hostile) is consistent — NPC dead in NODE-A cannot speak in NODE-B unless NODE-B precedes NODE-A on all paths
   - Report: "[NPC] speaks in NODE-[N] but is dead on PATH [A–B–N]"

4. **Series carry-over validation** (if `series-bible.md` exists or `--check series`)
   - Verify all carry-over variables in `series-bible.md` are declared in `variables.md`
   - Verify each ending's variable state snapshot is achievable on at least one path
   - Report any carry-over variable that is never set before the ending node

5. **Update continuity logs**
   - Append issues to `world-building.md` continuity log and `glossary.md` consistency log
   - Mark resolved issues from previous runs

6. **Thematic drift check** *(skip if `specs/themes.md` is absent)*
   - For each registered motif (MO-NNN): verify it appears in at least 3 drafted nodes; flag < 3 occurrences as WARNING
   - For each act: verify at least one node carries thematic work (node outline "Thematic work" field or prose evidence); two consecutive acts with no thematic work ? CRITICAL
   - For each symbol in the Symbol & Object Registry: verify physical state is consistent across nodes (object cannot be in two locations simultaneously); flag inconsistency as CRITICAL
   - Append issues to `specs/themes.md` Thematic Drift Log

7. **NPC relationship consistency check** *(skip if `specs/relationships.md` is absent)*
   - For each REL-NNN: verify the NPC states implied by each key beat are consistent with the variable values set in the corresponding node
   - Verify no node references an NPC as friendly/ally when the active dynamic at that branch point should make them hostile
   - Append issues to `specs/relationships.md` Relationship Drift Log

8. **Timeline constraint check** *(skip if `specs/timeline.md` is absent)*
   - For each TC-NNN constraint: verify no drafted node violates the stated before/after rule
   - Flag any NPC dialogue that reveals information before the fabula event that creates it — CRITICAL

9. **Dialogue continuity check** *(skip if no `Dialogue Tree` fields found in outlines)*
   - For each node with a `Dialogue Tree` (from `outlines/[NODE_ID].md`):
     - Verify each NPC's dialogue response uses the correct register from `specs/characters/[NPC_ID].md` Section VIII (Dialogue Register by Trust State)
     - Pull the NPC's current trust state from `variables_read` in the outline; verify the dialogue prose in the drafted node matches that register
     - Verify all NPCs present in the dialogue tree are actually present in the node (no dangling NPC responses)
     - For multi-party dialogues: verify NPC-A and NPC-B responses are consistent with their relationship state (from `specs/relationships.md` if present)
   - Report: "[NPC] dialogue in NODE-[N] uses high-register prose but trust state is 'hostile' (expected low-register)"
   - Report: "[NPC-A] and [NPC-B] dialogue in NODE-[N] contradicts their relationship arc"

10. **Glossary validation check** *(skip if `specs/glossary.md` is absent)*
   - Scan all drafted node prose for terminology that appears in `specs/glossary.md` Section I (Term Registry)
   - For each found term: verify it is spelled correctly and used with a meaning consistent with the glossary definition
   - Flag capitalization errors: term registered as `Sanctuary` but used as `sanctuary` in node
   - Flag usage variance: term has a "Rejected variant" in glossary (e.g., "Temporal Flux" vs. rejected "Time Flux") — flag if rejected variant used
   - Flag contradictory definitions: same term used with two different meanings across different nodes
   - Append issues to `specs/glossary.md` Consistency Log

11. **Location state consistency check** *(skip if `specs/locations.md` is absent)*
   - For each location appearing in multiple nodes: extract sensory details and location state from the node prose
   - Verify sensory descriptions are consistent across nodes (e.g., "sterile white walls" in NODE-005 should not become "organic vine-covered walls" in NODE-010 unless explicitly changed)
   - Track location state changes (e.g., if NODE-005 describes the door as "sealed", verify NODE-010 shows the door still sealed unless a node between them opened it)
   - Flag contradictions: "Sanctuary Station described as 'sterile white' in NODE-005 but 'overgrown with moss' in NODE-012 — timeline unclear"
   - Append issues to `specs/locations.md` State Change Log

12. **Multi-party dialogue consistency check** *(skip if fewer than 2 NPCs in project)*
   - For each pair of NPCs (NPC-A, NPC-B) that interact in multiple nodes:
     - Verify their dialogue and interaction patterns are consistent with their relationship arc (from `specs/relationships.md` if present or inferred from trust state delta)
     - If NPC-A's trust toward player is increasing but NPC-B's is decreasing, verify their dialogue reflects this (NPC-A increasingly friendly, NPC-B increasingly distant)
     - Verify neither NPC contradicts information the other has stated in earlier nodes
   - Report: "NODE-005: Corvus trusts you enough to reveal the vault key. NODE-012: Corvus claims he never knew about it. Contradiction." (if trust path supports first statement)

13. **Polish stage gate** (if `--strict` flag set)
   - For each node file in `draft/`: verify the frontmatter includes `polished: [YYYY-MM-DD]`
   - Emit a report: "Nodes awaiting polish: [count] (required for --strict mode)"
   - If all nodes have been polished: proceed with full continuity check
   - If some nodes not polished: halt and report which nodes need polish before continuity can be validated in strict mode

6. **Output**
   - Report summary: "Variable errors: [N] | POV drift: [N] | NPC errors: [N] | Dialogue continuity: [N] | Glossary errors: [N] | Location state errors: [N] | Multi-party dialogue: [N] | Series errors: [N] | Thematic drift: [N] | Relationship errors: [N] | Timeline violations: [N]"
   - If `--report`: write full details to `continuity-report.md` with sections per check type
   - Suggest: "Run `speckit.revise NODE-NNN` to fix flagged nodes. Run `speckit.polish NODE-NNN` to complete polish stage gate."
   - If `--strict` and polish gate failed: "Cannot complete continuity check in strict mode. Run `speckit.polish [UNPOLISHED_NODES]` first."
