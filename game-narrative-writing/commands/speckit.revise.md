---
description: Targeted node revision — rewrites only the failing passages identified by speckit.checklist, speckit.analyze, or speckit.continuity without touching passing content. Produces a versioned node file with a diff summary.
handoffs:
  - label: Re-run Checklist
    agent: speckit.checklist
    prompt: Re-run the checklist on the revised node
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Re-run continuity check after variable changes
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Continue drafting the next approved node
    send: true
---

# speckit.revise

Revise a node file to address quality failures, structural issues, or authorial feedback. Rewrites only failing passages — does not touch passing content.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted formats:
- `NODE-003` — revise the node; auto-load its most recent checklist failures
- `NODE-003 NR-001 PR-004` — revise specific failure codes only
- `NODE-003 FB-007` — revise a specific feedback issue from `feedback.md`
- `NODE-003 "dead-end branch after choice B"` — revise from a quoted description
- *(no argument)* — revise the node with the most recent open checklist failure

Optional flags:
- `--checklist` — auto-load all open checklist failures for the node
- `--feedback [ID]` — load a specific feedback issue from `feedback.md`
- `--full` — full redraft (not targeted revision); requires confirmation

## Pre-Execution Checks

**Check for extension hooks (before revision)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_revise` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Operating Constraints

**SURGICAL SCOPE**: Only modify prose, hooks, or choices that directly cause a flagged failure. Do not improve or tighten surrounding content. Scope creep corrupts the isolation of what changed and undermines the versioning model.

**CONSTITUTION AUTHORITY**: `.specify/memory/constitution.md` governs all prose and mechanic decisions. If a revision cannot fix the failure without violating the constitution, STOP and report the conflict — do not silently violate the constitution to pass a checklist item.

**OUTLINE AUTHORITY**: `outlines/[NODE_ID].md` is authoritative for the node's structural intent: beat sequence, choice set, and variable contract must remain intact. Only the *execution* changes.

**PLAN AUTHORITY**: `specs/plan.md` is authoritative for target node IDs. A revision must not add or remove choices that change the branch graph without a corresponding `plan.md` update.

## Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

2. **Identify the revision target**:
   - Parse `$ARGUMENTS` for node ID. Resolve to `draft/[ENGINE]/[NODE_ID].[EXT]` (auto-detect engine from the first existing file).
   - If no argument: scan `checklists/` for the most recently modified file with open failures — use its linked node as the target.
   - Abort with a clear error if the node file does not exist or has no valid YAML frontmatter header.

3. **Load failure context**:
   - If a checklist file is auto-detected or specified: read all items marked FAIL or WARNING plus any Top Revision Priorities list.
   - If `$ARGUMENTS` contains failure codes (e.g. `NR-001 PR-004`): treat those as the failure scope.
   - If `$ARGUMENTS` contains a quoted description from `speckit.continuity` or `speckit.analyze` (CRITICAL issue text): use that as the failure scope.
   - If `--feedback [ID]` is set: load the specified issue from `feedback.md`.
   - If none of the above: list FAIL/WARNING items from the most recent checklist for this node and ask the user to confirm scope before proceeding.
   - **Failure scope is fixed at this step.** Do not expand it during revision.

4. **Load required context**:
   - Read `draft/[ENGINE]/[NODE_ID].[EXT]` in full (prose + YAML frontmatter)
   - Read `.specify/memory/constitution.md` — POV rules, prohibited phrases, tone, Prose Style Mode (Section VII), `style_mode`, `prose_profile`
   - Read `.specify/memory/craft-rules.md` — craft rules (NR-NNN, PR-NNN per active prose profile), anti-AI clichés filter, prohibited phrases
   - Read `outlines/[NODE_ID].md` — beat sequence, choices table, variable contract, Dialogue Tree field (if present)
   - Read `specs/variables.md` — declared variables with types and value ranges
   - Read `specs/characters/[NPC_ID].md` for each NPC present — dialogue style (profile-tuned), trust thresholds, state values, Section VIII Dialogue Register by Trust State
   - **Optional (if dialogue revisions needed)**: Read `specs/relationships.md` for multi-party dialogue consistency
   - **Optional (if glossary revisions needed)**: Read `specs/glossary.md` Section V (Usage Rules) for term definitions and rejected variants
   - **Optional (if location revisions needed)**: Read `specs/locations.md` for sensory anchors and location rules

5. **Scope confirmation** — for each item in the failure scope, identify the exact passage or element responsible:
   - Quote the specific sentence(s), hook block, or choice line that causes the failure
   - State which item / issue each one violates and why
   - If failure is due to *absence* (e.g. no VISITED hook declared), note what must be *added* and where

   Present to the user:
   ```
   ## Revision Scope Confirmation

   | Item | Failing element / what's missing | Root cause | Revision type |
   |---|---|---|---|
   | PR-002 | "She felt the weight of the moment..." | Emotion named directly | Prose |
   | PR-010 | "The room felt cold and sterile" | Sensory inconsistent with Sanctuary location profile | Sensory detail |
   | DI-001 | "asked nervously" | Said-bookism with adverb on attribution | Dialogue prose |
   | DIAL-002 | Corvus dialogue uses high register | Trust state is hostile (expects low register) | Dialogue register |
   | GLOSS-001 | "Temporal Flux" used 3 times, "Time Flux" once | Glossary has "Time Flux" as rejected variant | Glossary consistency |
   | LOC-001 | Door described as "sealed" in NODE-005, "open" in NODE-012 | Timeline gap, state change not explained | Location state |
   | NR-001 | Choice B targets NODE-099 | NODE-099 does not exist in plan.md | Structural |
   | MH-003 | Missing [MECHANIC:VISITED set=...] | Variable visited_NODE-003 never set | Hook |
   | FB-007 | Trust delta in TRUST hook: +30 | Exceeds max single-node trust delta per constitution.md | Mechanic |
   ```

   **Stop and wait for user confirmation** before writing any revisions. Allow the user to:
   - Approve the scope as-is
   - Remove items ("skip FB-007, I'll fix it manually")
   - Add items ("also fix PR-004")
   - Provide a direction note ("for NR-001: retarget choice B to NODE-047 instead")

6. **Revise each failing element**:
   For each item in the confirmed scope, in the order they appear in the node file (top to bottom):
   - **Prose failures (PR-001—PR-008)**: rewrite only the failing passage; apply craft rules, POV, prohibited phrase check
   - **Sensory detail failures (PR-009, PR-010, PR-011)**: add/revise sensory descriptions to match location profile and NPC context; ensure emotional subtext is shown through environment/action not explicitly named
   - **Dialogue register failures (DIAL-NNN, DI-NNN)**: rewrite NPC dialogue to use correct register from `specs/characters/[NPC_ID].md` Section VIII per current trust state; fix said-bookism and adverb-on-attribution issues
   - **Dialogue tree consistency failures (DIAL-MULTI)**: if multi-party dialogue contradicts relationship arc or NPC information, revise one NPC's response to align with established dynamic
   - **Glossary failures (GLOSS-NNN)**: correct spelling/capitalization per `specs/glossary.md`; replace rejected variants with canonical terms; align meaning with glossary definition
   - **Location state failures (LOC-NNN)**: update sensory descriptions to match location profile; note timeline if state has changed; add brief explanation if location state differs from previous node
   - **Structural failures**: fix target node IDs, correct choice count, update branch logic
   - **Hook failures**: correct hook syntax, fix variable names or deltas, add missing hook declarations
   - **Feedback items**: implement the suggested change or propose an alternative with rationale
   - **Polish-stage failures (from speckit.polish audit)**: apply line-edit fixes (sentence rhythm, word repetition, filter words, weak verbs, voice register, em-dash count, dialogue attribution)
   - After each revision, note: which item it addresses and how

7. **Assemble the revised node**:
   - Replace only the revised elements in the original full node
   - **Do not alter** any content outside the confirmed revision scope
   - Reset `status` to `DRAFT` in YAML frontmatter if it was `APPROVED` (revision requires re-approval)
   - If `polished: [date]` exists: remove it (revision of prose means polish is invalidated)
   - Update `variables_read` / `variables_set` in frontmatter if changed
   - Increment `version` field (e.g. `version: 1` ? `version: 2`); add if absent
   - Add `revised: [YYYY-MM-DD]` field to the YAML frontmatter

8. **Write output**:
   - **Revised node**: save as `draft/[ENGINE]/[NODE_ID]_v[N].[EXT]` (e.g. `draft/ink/NODE-003_v2.ink`)
   - **Keep the original** `draft/[ENGINE]/[NODE_ID].[EXT]` unchanged — it is the v1 record
   - **Revision notes**: append a `<!-- REVISION NOTES` comment block at the top of the revised file (after YAML frontmatter):
     ```
     <!-- REVISION NOTES v[N]
          Revised: [YYYY-MM-DD]
          Revision scope: [list of item codes fixed]
          Based on: [checklist file / speckit.analyze report / speckit.continuity report / speckit.polish audit / manual scope]
          Revision types: [Prose|Sensory detail|Dialogue register|Dialogue consistency|Glossary|Location state|Structural|Hook|Mechanic|Polish]

          Changes:
          - [ITEM] ([TYPE]): [brief description of what changed and why]
          - [ITEM] ([TYPE]): [brief description]

          Prose validity: [unchanged from v[N-1] outside revision scope]
          Polish status: [invalidated - requires re-polish]
     -->
     ```

9. **Report**:
   ```
   ## Revision Report

   | Item | Type | Status | Change summary |
   |---|---|---|---|
   | PR-002 | Prose | Fixed | Named emotion ? involuntary physical reaction |
   | PR-010 | Sensory detail | Fixed | Updated sensory descriptions to match Sanctuary profile (sterile, cold) |
   | DIAL-001 | Dialogue register | Fixed | Corvus dialogue shifted to low-register; trust state is hostile |
   | GLOSS-001 | Glossary | Fixed | Replaced "Time Flux" with canonical "Temporal Flux" (3 instances) |
   | LOC-001 | Location state | Fixed | Clarified door state: "sealed in NODE-005, remains sealed via backdoor route, opened via main atrium" |
   | NR-001 | Structural | Fixed | Choice B retargeted: NODE-099 ? NODE-047 |
   | MH-003 | Hook | Fixed | Added [MECHANIC:VISITED set=visited_NODE-003] after prose |
   | FB-007 | Fixed | TRUST delta reduced: +30 ? +10 |

   Revised node: draft/ink/NODE-003_v2.ink
   Status reset to DRAFT — polish invalidated (revise removes polished: field); re-review and set status: APPROVED before next drafting run.
   Recommendations: (1) Run `speckit.checklist NODE-003` on the revised node to confirm all items pass. (2) Run `speckit.polish NODE-003` to re-polish after structural revisions complete. (3) Run `speckit.continuity --check dialogue,glossary,locations` if any dialogue/glossary/location changes made.
   ```

   If any item could **not** be fixed without violating the game bible or outline, report as BLOCKED:
   ```
   | NR-002 | BLOCKED | Fixing this requires adding a third choice, which changes the branch
                         graph. Update specs/plan.md for NODE-003 first, then re-run revision. |
   ```

   If `specs/plan.md` was affected (target node IDs changed or dialogue tree modified): note:
   ```
   ?? plan.md may need updating — choice targets or dialogue options changed. Run speckit.analyze to verify branch integrity.
   ```

   If glossary, location, or dialogue tree changes made: note:
   ```
   ?? Glossary/Location/Dialogue changes made. Run speckit.continuity --check glossary,locations,dialogue to validate cross-node consistency.
   ```

10. **Check for extension hooks (after revision)**: check `hooks.after_revise`.

