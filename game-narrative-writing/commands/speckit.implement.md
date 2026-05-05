---
description: Draft narrative prose for nodes from approved outlines. Prose is generated engine-agnostic (markdown), then exported to engine-specific formats (Twee for SugarCube, Ink, etc.) via speckit.export.
handoffs:
  - label: Export to engines
    agent: speckit.export
    prompt: Export drafted markdown nodes to engine-specific formats (SugarCube, Ink, etc.)
    send: true
  - label: Compile to playable output
    agent: speckit.compile
    prompt: Compile exported engine files to playable HTML/JSON
    send: true
  - label: Review outlines again
    agent: speckit.outline
    prompt: I want to review or regenerate the outlines before drafting
    send: false
---

# speckit.implement

Draft narrative prose for nodes from approved outlines. Generates engine-agnostic markdown node files, preserving all outline information (variables, choices, mechanical consequences) in structured format.

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `[NODE_ID]` – draft a single node (e.g. `NODE-001`)
- `[NODE_ID] [NODE_ID] ...` – draft a list of nodes
- `--act [N]` – draft all nodes for a given act
- `--all` – draft all approved nodes that don't yet have draft files
- `--force` – regenerate an existing draft (overwrite)
- *(no argument)* – draft the next unoutlined node with status APPROVED

## Pre-Execution Checks

**Check for extension hooks (before drafting)**:
- Check if `.specify/extensions.yml` exists in the project root
- If it exists, read it and look for entries under the `hooks.before_implement` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

Then:
1. Confirm `specs/[FEATURE_DIR]/outline/` and `specs/[FEATURE_DIR]/constitution.md` exist
2. For each requested node, verify an outline file exists at `outlines/[NODE_ID].md` 
3. Verify outline status is `APPROVED` (skip nodes marked `DRAFT` or `SKIP`) — unless `--force` is set
4. Confirm `specs/[FEATURE_DIR]/variables.md` exists — hooks declared in outlines must resolve
5. Confirm `specs/[FEATURE_DIR]/characters.md` exists — dialogue and NPC references must resolve
6. Confirm `specs/[FEATURE_DIR]/constitution.md` exists — prose_profile and engine settings needed

## Execution Steps

### 1. Load Required Documents

For each target node, load:
- **Required**: Outline file `outlines/[NODE_ID].md` (Beat Summary, Variables, Choices, Mechanic Hooks)
- **Required**: `constitution.md` (prose_profile, default POV, tone, style_mode)
- **Required**: `spec.md` (research notes, world rules, context)
- **Required**: `variables.md` (variable declarations for type checking)
- **Required**: `characters.md` (NPC profiles, dialogue registers, relationship states)
- **Required**: `mechanics.md` (hook schemas for translating mechanics to engine syntax)
- **Optional**: `craft-rules.md` (if style_mode is humanized-ai — guides beat language register)
- **Optional**: `glossary.md` (for consistent terminology in prose)
- **Optional**: `locations.md` (for sensory anchors and location-specific rules)
- **Optional**: `themes.md` (for thematic resonance and motif placement)

### 2. Parse Outline Choices & Consequences

**This is the critical step for preserving consequences:**

From the outline's **Choices table**, extract:
- Column 1: Choice letter (A, B, C...)
- Column 2: **Label** (player-visible choice text)
- Column 3: **Condition** (optional gate like `$trust_mira >= 50`)
- Column 4: **Target Node** (NODE_ID or END_ID)
- Column 5: **Narrative Consequence** (description of what changes if this choice is made)

**Store the narrative consequence** as a comment in the drafted node's Choices section:
```markdown
- [CHOICE_LABEL](TARGET_NODE) <!-- Effect: [Narrative Consequence from outline] -->
```

**If condition exists**, include both condition and consequence:
```markdown
- [CHOICE_LABEL](TARGET_NODE) <!-- requires: $trust_mira >= 50; Effect: Mira remembers your loyalty -->
```

### 3. Extract Variables & Mechanics

From the outline:
- **Variables Read**: Variables this node checks as conditions
- **Variables Set**: Variables this node changes (from Mechanic Hooks Summary)
- **Mechanic Hooks**: All hooks and their configuration (type, tier, variable, action, timing)

Populate the node frontmatter:
```yaml
variables_read: [var1, var2]  # From outline's "Variables Read" section
variables_set: [var3, var4]   # From outline's "Variables Set" section
```

### 4. Draft Narrative Prose

**Goal**: Write engaging prose that:
- Matches the beat summary from the outline
- Uses the prose_profile (style, register, tone) from constitution.md
- Reads coherently without the mechanic hook blocks
- Respects the outlined choices (don't create new choices)
- Includes all required variables from outline's Variables Read/Set sections

**Opening line** MUST establish:
- Where (location/context)
- Who (character perspective, NPCs present)
- What (the central decision or situation)

**Prose structure**:
1. Opening: Orient the player (location, stakes, context)
2. Middle: Describe the situation, NPCs, choices available
3. Mechanic hooks: Insert [MECHANIC:...] blocks inline (see **Inline Mechanic Hooks** section below)
4. Choices: Terminal ## Choices section with all outlined choices

**Style rules**:
- POV: Use constitution.md default POV (second-person, third-person, first-person) or node-level override
- Tone: Match constitution.md tone (dramatic, comedic, dark, uplifting, etc.)
- Register: If style_mode is humanized-ai, use craft-rules.md to tune beat language and dialogue

### 5. Inline Mechanic Hooks

Insert [MECHANIC:...] blocks within prose where they occur:

**Examples**:

```markdown
You notice a rusty key on the ground.
[MECHANIC:INVENTORY add=key_rusty]
It might be useful.

[MECHANIC:VISITED set=visited_chamber]
You've been here before.

[MECHANIC:TRUST npc=mira delta=+5]
Mira smiles at you warmly, her trust deepening.

[MECHANIC:COUNTER variable=escape_attempts delta=+1]
You count this as your third attempt.

[MECHANIC:CHOICE_MEMORY variable=player_loyalty value="helped_mira"]
You remember: you chose to help Mira earlier.
```

**Inline rules**:
- Prose must read coherently if all [MECHANIC:...] blocks are removed
- Each hook block must be isolated — no mixing multiple hooks in one block unless they fire simultaneously
- The prose surrounding the hook should justify why the mechanic fires (e.g., "You gain her trust" before `[MECHANIC:TRUST delta=+5]`)

### 6. Terminal Choices Section

At the end of the node, create a ## Choices section with format:

```markdown
## Choices

- [Look around carefully](NODE-002) <!-- Effect: You gain awareness of the chamber -->
- [Check the equipment](NODE-003) <!-- Effect: You discover a tool that might help -->
- [Leave immediately](NODE-004) <!-- requires: $flag_danger_sense == true; Effect: You escape before being discovered -->
```

**Rules**:
- Each choice must match exactly one row from the outline's Choices table
- Label MUST be verbatim from outline (or close synonym if prose uses simpler language)
- Target node MUST match outline target
- Include condition comment if outlined choice had a gate condition
- Include Effect comment with the narrative consequence from the outline
- Minimum 2 choices for non-terminal nodes; omit entirely for ending nodes

**For ending nodes**: Single choice pointing to the ending:
```markdown
## Choices

- [Accept your fate](END-001) <!-- Effect: You succumb to the darkness -->
```

### 7. Validate Against Outline

Before marking node as ready:
- ✓ All variables from outline Variables Read are present in prose or hooks
- ✓ All variables from outline Variables Set have corresponding hook blocks
- ✓ All mechanic hooks from outline are present
- ✓ All choices from outline are present with correct labels and targets
- ✓ All narrative consequences from outline are preserved as comments in Choices section
- ✓ Opening line establishes where/who/what
- ✓ Prose reads coherently without hook blocks

### 8. Output Format

Create `draft/[ENGINE_NAME]/[NODE_ID].md` (engine-agnostic markdown):

```markdown
---
node_id: NODE-001
title: [Title from outline]
act: [Act number]
status: DRAFT
pov: [POV from constitution or outline override]
variables_read: [list]
variables_set: [list]
drafted: [YYYY-MM-DD]
outline_ref: outlines/[NODE_ID].md
---

# [Node Title]

<!-- Node ID: NODE_ID | Act: [ACT] | Status: DRAFT -->

[PROSE WITH INLINE MECHANICS]

## Choices

- [Label](NODE_TARGET) <!-- Effect: consequence from outline -->
```

### 9. Report

List all drafted nodes with:
- `[NODE_ID] [title] — [N] vars, [N] hooks, [N] choices, act [N]`

Flag any:
- Missing consequence comments in Choices section
- Undeclared variables
- Outline deviations (new choices, variables, or mechanics not in outline)

Remind the author to:
- Review prose for coherence and tone
- Verify all consequences are documented as comments in Choices section
- Check that all outlined mechanics are present
- Change `status: DRAFT` → `status: APPROVED` when satisfied
- Run `speckit.export` to convert to engine-specific format

### 10. Check for Extension Hooks

Check `hooks.after_implement`: run if present.

---

## Key Principle: Preserve Outline Fidelity

**The implement phase must NOT:**
- Add new choices not in the outline
- Remove outlined choices
- Change choice targets
- **Forget the narrative consequences** ← This is the common mistake

**The implement phase MUST:**
- Preserve all outline information (variables, hooks, choices, consequences)
- Document consequences as comments in the Choices section
- Transfer all mechanic hooks from outline to prose
- Maintain outline structure and gating conditions
- Write prose that matches the beat summary and narrative purpose

Consequences are the **bridge** between mechanical outcome and narrative meaning. They must be preserved.
