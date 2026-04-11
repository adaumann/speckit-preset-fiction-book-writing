---
description: Detect and resolve narrative ambiguity in the active story brief — character motivation, timeline gaps, POV clarity, world-building inconsistencies, and unresolved plot requirements.
handoffs:
  - label: Build Story Structure
    agent: speckit.plan
    prompt: Create a story structure plan for this brief. The plot structure I want to use is...
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before clarification)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_clarify` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Outline

**Goal**: Detect and reduce ambiguity or missing decision points in the active story brief (`spec.md`), then write the answers directly back into the file.

**Note**: This clarification workflow should run BEFORE `/speckit.plan`. If the user explicitly skips it, warn that downstream rework risk increases — then proceed.

### Execution steps

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC path and SPECS_DIR.

2. **Load `spec.md`**: Read the full story brief. Identify all `[NEEDS CLARIFICATION]` markers.

3. **Run a structured ambiguity scan** across these domains — look for gaps or contradictions, not just explicit markers:

   | Domain | Questions to ask |
   |---|---|
   | **Character motivation** | Is each character's internal wound clearly distinct from their external want? Does the need (thematic truth) conflict meaningfully with the want? Are micro-obsessions defined and distinct per POV character? Are the self-deception patterns and blind spots specified? Are the doubt moments (Section V) identified? |
   | **Voice distinctiveness** | Could a scene from Character A be narrated by Character B without the name tags? Check: vocabulary pools do not overlap, cognitive modes differ, deflection strategies differ, verbal tics are distinct. Run the Voice Homogeneity Test sentence from Section IX. |
   | **Relationship dynamics** | For each significant relationship: is the repeating dynamic loop defined? Is the subtext (what neither person says directly) named? Are trigger points specified? |
   | **Narrative arc logic** | Is the protagonist's transformation arc plausible given their wound? Does each arc's Given/When/Then chain hold together causally? |
   | **Timeline & continuity** | Are there time gaps that create logical contradictions? Does any Chekhov item lack a plausible pay-off scene? |
   | **POV & scope** | Is POV strategy (single/multiple/omniscient) consistent with story scope? Are there scenes that would require POV characters who aren't defined? |
   | **World-building** | Are world rules implied by the story that haven't been documented? Are there location or world-state details that could contradict each other? |
   | **Dramatic question** | Is the central dramatic question stated once, clearly? Does every major scene meaningfully advance its answer? |
   | **Reader experience goals** | Are the RG- goals measurable? Is there anything the story promises the reader that isn't yet covered by a scene beat? |

4. **Select ≤5 questions** — the highest-value targeted clarifications. Prioritize:
   - Questions that block planning (structural ambiguity)
   - Questions about character wound / need (thematic engine)
   - Chekhov items with no pay-off assigned
   - Voice distinctiveness gaps
   
   Do NOT ask about things resolvable from context. Do NOT ask generic questions.

5. **Present questions to the user** — one at a time or as a numbered list if the user prefers batch mode. Wait for answers.

6. **Write answers back into `spec.md`**:
   - Replace `[NEEDS CLARIFICATION: ...]` markers with the clarified content
   - Add answers to the relevant character arc, scene beat, or plot requirement section
   - If a new Chekhov item is discovered, add it to the Key Entities table
   - If a new scene beat is implied, add it to Key Scenes with a `[NEEDS SCENE DRAFT]` note

7. **Report**: Summarize what was clarified, what was added, and whether any `[NEEDS CLARIFICATION]` markers remain.
