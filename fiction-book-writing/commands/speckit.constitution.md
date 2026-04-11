---
description: Create or update the story bible — style mode selection, plot structure choice, craft principles, and propagation to all dependent templates.
handoffs:
  - label: Create Story Brief
    agent: speckit.specify
    prompt: Create a story brief for...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before story bible update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

## Outline

**Goal**: Create or update `.specify/memory/constitution.md` (the Story Bible) from user input or inference from existing project files.

### Execution steps

1. **Load existing constitution** (if present): Read `.specify/memory/constitution.md`. Identify all `[NEEDS CLARIFICATION]` and `[PLACEHOLDER]` tokens that still require resolution.

2. **Determine style mode** — ask the user if not already set:

   > "Which style mode do you want for this story?
   > (a) **author-sample** — paste a key chapter/passage and I'll extract your voice markers
   > (b) **humanized-ai** — use the built-in craft ruleset for commercially viable fiction that avoids AI clichés"

   - If `author-sample`: prompt the user to paste 500–2000 words of their own prose. Extract the 8 style markers (POV, tense, rhythm, vocabulary register, sensory density, tone, dialogue style, anti-patterns). Write them into the Extracted Style Markers table. Confirm the extracted values with the user.
   - If `humanized-ai`: confirm the built-in ruleset is active. Then determine the **Prose Profile** — ask if not already set:

     > "Which prose profile fits this story?
     > (a) **commercial** — balanced pace, moderate interiority, alternating rhythm (general fiction, romance, fantasy)
     > (b) **literary** — deep interiority, high sensory texture, reflection-forward (literary fiction, character studies)
     > (c) **thriller** — action-forward, minimal interiority, short-dominant sentences (thrillers, crime, horror)
     > (d) **atmospheric** — maximum sensory density, slow burn, environment as plot engine (gothic, horror, weird fiction)
     > (e) **dark-realist** — clipped declarative prose, cold interiority, consequence-forward (noir, social realism, gritty literary)"

     Set `[PROSE_PROFILE]` to the chosen value. The profile tunes how the universal craft principles (Sections II–VII) are weighted — it does not relax or override any universal rule.

     Ask if there are any additional prohibited phrases to add to the Anti-AI Filter for this specific story/genre (beyond the profile's built-in additions).

3. **Fill the Story Bible fields** — work through each `[NEEDS CLARIFICATION]` token. Gather values from:
   - User input in `$ARGUMENTS`
   - Inference from existing `spec.md` if present
   - Direct questions to the user (ask only what cannot be inferred)

   Fields to resolve in order:
   - `[PLOT_STRUCTURE]` — if not set, present the 7 options with a brief description of each and ask the user to choose
   - `[DRAMATIC_QUESTION]` — one sentence, the story's spine
   - `[THEME]` — stated as a question, not an answer
   - `[POV_STRATEGY]` and `[TENSE]` — from style mode or user input
   - `[WORD_COUNT_TARGET]`, `[GENRE]`, `[TARGET_AUDIENCE]`, `[SERIES_POSITION]`
   - `[DRY_IRONY_CHARACTERS]` — which characters (if any) are permitted situational irony
   - `[STORY_SPECIFIC_PRINCIPLES]` — 3–5 rules unique to this story
   - `[ADDITIONAL_PROHIBITED_PHRASES]` — story/genre-specific additions to the Anti-AI filter

4. **Increment the semantic version**:
   - **MAJOR**: if plot structure, POV strategy, or number of POV strands changed
   - **MINOR**: if new principles, style rules, or Anti-AI phrases added
   - **PATCH**: typos, clarifications, minor refinements
   - Update `[CONSTITUTION_VERSION]`, `[RATIFICATION_DATE]` (on first creation only), `[LAST_AMENDED_DATE]`

5. **Write a Sync Impact Report** as an HTML comment at the top of the file, summarizing what changed and which dependent templates are affected:
   ```html
   <!-- SYNC IMPACT: v1.0.0 → v1.1.0
        Changed: Added 3 prohibited phrases, updated theme statement
        Affected templates: spec-template.md (Reader Experience Goals), tasks-template.md (Polish Pass)
        Action required: Re-run /speckit.continuity if scenes have been drafted -->
   ```

6. **Propagate changes** to dependent templates if applicable:
   - If plot structure changed: update `plan-template.md` to activate the correct structure block
   - If Anti-AI Filter phrases changed: note in the impact report (scenes need re-scan)
   - If POV strategy changed: update `spec-template.md` character arc section header

7. **Validate the final constitution**:
   - No unresolved `[NEEDS CLARIFICATION]` tokens remain
   - `[RATIFICATION_DATE]` and `[LAST_AMENDED_DATE]` are ISO format (`YYYY-MM-DD`)
   - Style mode is explicitly set
   - If `humanized-ai` mode: `[PROSE_PROFILE]` is one of the 5 supported values: `commercial`, `literary`, `thriller`, `atmospheric`, `dark-realist`
   - Plot structure is one of the 7 supported values
   - Theme is stated as a question, not an answer
   - If `author-sample` mode: all 8 Extracted Style Markers have values (not `[NEEDS CLARIFICATION]`)

8. **Report**: Summarize all resolved fields, the new version number, and any remaining items requiring attention.
