# Implementation Workflow for Game Narrative Writing

This document explains how `speckit.implement` generates engine-specific node files from approved outlines, with support for multiple export engines.

## Overview

The implementation phase is where approved outlines become playable narrative code. The process:

1. **Outline Approval**: Author writes and approves `outlines/NODE-NNN.md` with status `APPROVED`
2. **Engine Selection**: Constitution specifies which engines to target (`export_engines`)
3. **File Generation**: For each approved node, files are generated in each engine format
4. **Compilation**: Generated files are validated and compiled using native tools

## File Structure

```
spec/[game-name]/
├── spec.yml                           # Contains export_engines list
├── constitution.md                    # Story bible (game rules)
├── outlines/
│   ├── NODE-001.md                   # Approved outline with status: APPROVED
│   ├── NODE-002.md
│   └── NODE-NNN.md
├── draft/
│   ├── generic/                      # Generated .md review files
│   │   ├── NODE-001.md
│   │   └── NODE-NNN.md
│   ├── sugarcube/                    # Generated .twee files
│   │   ├── NODE-001-start.twee
│   │   ├── NODE-002-tier2-demo.twee
│   │   └── NODE-NNN.twee
│   ├── ink/                          # Generated .ink files
│   │   ├── NODE-001-start.ink
│   │   └── NODE-NNN.ink
│   ├── renpy/                        # Generated .rpy files (if configured)
│   │   └── NODE-NNN.rpy
│   └── [other-engines]/
└── output/
    ├── sugarcube/
    │   └── story.html                # Compiled output
    ├── ink/
    │   └── output.ink
    └── [other-engines]/
```

## Configuration

### spec.yml - Engine Selection

```yaml
title: My Game
author: Author Name
export_engines:
  - generic      # Always included for review
  - sugarcube    # Primary target format
  - ink          # Optional: secondary format
```

This list controls what `speckit.implement` will generate.

## Implementation Steps

### 1. Create Outline

Create `outlines/NODE-001.md`:

```markdown
---
node_id: NODE-001
title: Start
act: 1
status: APPROVED
pov: second-person
variables_read: []
variables_set: [visited_start, player_choice]
---

# NODE-001: Start

## Summary
The player enters the game world.

## Beats
1. Establish scene
2. Present choices

## Variables
| Variable | Type | Direction |
|----------|------|-----------|
| visited_start | flag | set |

## Choices
| Choice | Target |
|--------|--------|
| Look around | NODE-002 |
| Check equipment | NODE-002 |
```

**Important**: Set `status: APPROVED` for the outline to be drafted.

### 2. Run Implementation

```bash
speckit.implement NODE-001
```

The command will:
1. Verify `outlines/NODE-001.md` exists and has `status: APPROVED`
2. Read `export_engines` from `spec.yml`
3. Generate one file for each engine:
   - `draft/generic/NODE-001.md`
   - `draft/sugarcube/NODE-001-start.twee`
   - `draft/ink/NODE-001-start.ink`

### 3. Generated Twee File Structure

For SugarCube/Twee format, the generated file will look like:

```twee
{* 
node_id: NODE-001
title: Start
act: 1
status: DRAFT
pov: second-person
variables_read: []
variables_set: [visited_start, player_choice]
drafted: 2026-05-02
outline_ref: outlines/NODE-001.md
*}

:: Start
    [Story prose here - written by LLM based on outline]
    
    [MECHANIC:VISITED variable=visited_start][/MECHANIC]
    [MECHANIC:CHOICE_MEMORY variable=player_choice][/MECHANIC]

:: Look Around
    [Branch 1 prose]
    [[Continue -> NODE-002]]

:: Check Equipment
    [Branch 2 prose]
    [[Continue -> NODE-002]]
```

Key features:
- YAML metadata in `{* ... *}` comment blocks (Twee-specific)
- `:: PassageName` passage headers
- `[[Label -> Target]]` links for navigation
- `[MECHANIC:TYPE]` hooks for gameplay mechanics

### 4. Verification

`speckit.implement` automatically runs `speckit.verify`:
- Validates Twee syntax
- Checks all variables are declared
- Runs mechanical hooks validation
- Confirms choices link to valid nodes

### 5. Compilation

After all nodes are drafted and verified, compile to playable format:

```bash
# SugarCube -> HTML
python compile.py --spec [game-name] --engine sugarcube
# Output: specs/[game-name]/output/sugarcube/story.html

# Ink validation (requires inklecate)
python compile.py --spec [game-name] --engine ink
# Output: specs/[game-name]/output/ink/output.ink
```

## Start Node Requirements

The **NODE-001** (start) node is special:

1. **Must exist**: Every story needs an entry point
2. **Must be first**: Listed first in `specs/plan.md`
3. **Must be approved**: Set `status: APPROVED` in outline
4. **File naming**: 
   - Generic: `NODE-001.md`
   - SugarCube: `NODE-001-start.twee` (typically)
   - Ink: `NODE-001-start.ink`

The "start" suffix is conventional but can be any descriptive title.

## Multi-Engine Generation

With `export_engines: [generic, sugarcube, ink]`, one `speckit.implement NODE-001` call generates **three files**:

```
NODE-001.md        # Human-readable review format
NODE-001-start.twee # SugarCube playable format  
NODE-001-start.ink  # Ink narrative format
```

All three files represent the same logical node, converted to engine-specific syntax by the LLM.

## Engine Differences in Output

### Generic (Markdown)
```markdown
---
node_id: NODE-001
title: Start
---

# Start

Story prose here...

[MECHANIC:FLAG variable=visited][/MECHANIC]

## Choices
- [Look around](NODE-002)
- [Check equipment](NODE-002)
```

### SugarCube (Twee)
```twee
{* node_id: NODE-001 *}

:: Start
    Story prose here...
    [MECHANIC:FLAG variable=visited][/MECHANIC]

:: Look Around
    [[Continue -> NODE-002]]
```

### Ink
```ink
/* node_id: NODE-001 */

=== Start ===
    Story prose here...
    ~ visited = true
    
    * [Look around] -> NODE_002
    * [Check equipment] -> NODE_002
```

## Validation Before Implementation

Before running `speckit.implement`, verify:

1. ✓ Outline exists at `outlines/NODE-001.md`
2. ✓ Outline has `status: APPROVED`
3. ✓ All variables used are declared in `specs/variables.md`
4. ✓ All target nodes exist in `specs/plan.md`
5. ✓ `spec.yml` has `export_engines` list

If any check fails, `speckit.implement` will halt with instructions.

## Troubleshooting

### "No outline found"
Create `outlines/NODE-001.md` first, then run `speckit.implement`.

### "Status is DRAFT"
Set `status: APPROVED` in the outline YAML header.

### "Variable not declared"
Add missing variables to `specs/variables.md` before drafting.

### "Wrong engine format"
Verify `export_engines` in `spec.yml` includes the target engine.

### File not generated for specific engine
1. Check that engine is in `export_engines` list
2. Verify outline is `status: APPROVED`
3. Re-run `speckit.implement [NODE_ID]` with `--force` flag

## Next Steps

1. Create outline for NODE-001 ✓ (Done in this demo)
2. Run `speckit.implement NODE-001`
3. Review generated files in `draft/sugarcube/`, `draft/ink/`, etc.
4. Run `compile.py` to validate and build output
5. Test in-game by opening output HTML or running in Ink player
