---
description: Detect and resolve ambiguity and open design questions in the narrative design doc or game bible — branch logic gaps, mechanic coherence, variable states, and unresolved OQ-NNN items.
handoffs:
  - label: Rewrite Narrative Design Doc
    agent: speckit.specify
    prompt: Major concept changes emerged during clarification. Please rewrite the narrative design doc.
  - label: Generate Game Bible
    agent: speckit.constitution
    prompt: All open questions are resolved. Generate the game bible.
---

# speckit.clarify

Detect and reduce ambiguity or missing decision points in the narrative design document or game bible, then write resolved answers directly back into the relevant files.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted input:
- A specific open question reference (e.g. "resolve OQ-003")
- A topic area (e.g. "clarify branch structure" or "clarify engine target")
- No input — runs a full structured ambiguity scan across all scoped files

Optional flags:
- `--scope narrative` — scan `specs/spec.md` only
- `--scope constitution` — scan `.specify/memory/constitution.md` only
- `--all` — resolve all open questions in sequence (interactive mode)

## Pre-Execution Checks

**Check for extension hooks (before clarification)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_clarify` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:
1. Locate `specs/spec.md` — if absent, suggest running `speckit.specify` first.
2. Count all `[NEEDS CLARIFICATION]` and `OQ-NNN` markers in scoped files.
3. Report: "Found [N] open questions. Proceeding to resolution."

## Outline

**Goal**: Detect and reduce ambiguity or missing decision points in the active spec files, then write the answers directly back into the relevant file.

**Note**: This clarification workflow should run BEFORE `speckit.plan`. If the user explicitly skips it, warn that downstream rework risk increases — then proceed.

### Execution Steps

1. **Setup**: Run `{SCRIPT}` from repo root if available and parse JSON for spec file paths.

2. **Load spec files**: Read `spec.md` (and `constitution.md` if in scope). Identify all `[NEEDS CLARIFICATION]` and `OQ-NNN` markers.

3. **Run a structured ambiguity scan** across these domains — look for gaps or contradictions, not just explicit markers:

   | Domain | Questions to ask |
   |---|---|
   | **Branch logic** | Are all branch conditions fully specified? Do any branches lead to dead ends or unreachable nodes? Are merge points and convergence conditions documented? |
   | **Player agency** | Is the player's decision scope clearly bounded? Do choices have distinct, meaningful consequences? Are illusion-of-choice moments deliberately marked? |
   | **Variable states** | Are all tracked variables (flags, counters, relationship scores) defined with their valid ranges? Are there state combinations that produce contradictions or unreachable content? |
   | **Character consistency** | Do NPC motivation anchors hold across all branches? Are self-deception patterns or behavioral blind spots defined per major NPC? Could an NPC behave differently in two branches in ways that break characterisation? |
   | **World rules** | Are world-building rules implied by the narrative but not yet documented as WR-NNN? Are there location or faction details that could contradict each other across scenes? |
   | **Mechanic coherence** | Are narrative mechanics aligned with the gameplay systems described in the spec? Are pacing requirements compatible with engine or platform constraints? |
   | **Endings & arcs** | Is each ending's prerequisite path clearly traceable from the branch map? Are thematic arcs resolved consistently across all major ending variants? |
   | **Continuity** | Are there timeline gaps or scene-order contradictions? Do introduced story elements (Chekhov items) have documented pay-off scenes? |
   | **Export / platform** | Are there engine, platform, or toolchain constraints that affect narrative structure but aren't yet captured in the spec? |

4. **Select =5 questions** — the highest-value targeted clarifications. Prioritize:
   - Questions that block planning or branch-map work (structural ambiguity)
   - Variable state contradictions (breaks implementation)
   - Character consistency gaps across branches
   - Missing world rules implied by existing content
   - Endings with untraceable prerequisite paths

   Do NOT ask about things resolvable from context. Do NOT ask generic questions.

5. **Present questions to the user** — one at a time, or as a numbered list if the user prefers batch mode. Wait for answers.

6. **Write answers back into the relevant file**:
   - Replace `[NEEDS CLARIFICATION: ...]` markers with clarified content
   - Remove resolved `OQ-NNN` markers and record the resolution inline
   - If a resolution creates new constraints, add a world rule (`WR-NNN`) entry
   - If a new branch condition is implied, add a `[NEEDS BRANCH SPEC]` note to the plan section
   - Group remaining unresolved items by category: design, world-building, mechanic, export, research

7. **Report**: "Resolved [N] of [N] questions. [N] remain."
   - If all resolved: "All open questions resolved. Run `speckit.constitution` to generate the game bible."

