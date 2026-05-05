---
description: Compile drafted node files to playable output format (HTML for Twine/SugarCube, compiled JSON for Ink with HTML wrapper, etc.). Includes built-in structural validation and automatic retry logic for compilation errors.
handoffs:
  - label: Run full test suite
    agent: speckit.verify
    prompt: Run optional full unit tests if you want comprehensive validation beyond compilation checks
    send: false
  - label: Re-draft failing nodes
    agent: speckit.implement
    prompt: Some nodes failed validation. Show which ones and suggest fixes, then re-draft them
    send: true
  - label: View node drafts
    agent: speckit.implement
    prompt: Show me the current drafted nodes
    send: false
scripts:
  py: scripts/python/compile.py --spec $SPECNAME --engine $ENGINE
---

# speckit.compile

Compile all drafted node files from `spec/<specname>/draft/<ENGINE>/` to a playable output file in `spec/<specname>/output/<ENGINE>/`.

Uses native compilers (tweego for SugarCube, inklecate for Ink) with automatic retry logic for compilation errors.

**Output formats**:
- **Twine/SugarCube** (twee) → HTML file with StoryData JSON header (via tweego.exe)
- **Ink** (.ink) → Compiled JSON + HTML wrapper (via inklecate.exe)
- **Renpy** (.rpy) → Python script for Ren'py engine
- **Generic** (markdown) → Linked HTML pages

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `[ENGINE]` - compile for a specific engine (e.g., `sugarcube`, `ink`, `renpy`, `generic`)
- `--all-engines` - compile all engines in export_engines configuration simultaneously
- `--force-rebuild` - force full rebuild even if output exists
- `--dry-run` - validate without writing output files
- *(no argument)* - compile to the engine specified in `constitution.md`

## Pre-Execution Checks

**Verify drafted nodes exist**:
- Scan `spec/<specname>/draft/<ENGINE>/` for node files
- If no files found - halt: "No drafted nodes found for engine `$ENGINE`. Run `speckit.implement` first."

**Verify engine configuration**:
- Check `constitution.md` for `export_engines`
- Check `variables.md` for export names for the target engine
- Check `mechanics.md` for Tier 1 hook compatibility with target engine

## Execution Steps

### 1. Structural Validation (automatic)
- Parse all node YAML headers
- Validate required fields (node_id, title, status)
- Check mechanic hook syntax ([MECHANIC:...] blocks)
- Check choice block syntax ([CHOICE:...] blocks)
- Report all validation errors with line context

### 2. Load Node Files
- Read validated node files into memory
- Parse YAML headers and body content
- Handle both individual NODE files and combined story files

### 3. Engine-Specific Compilation

#### Twine/SugarCube (twee → HTML via tweego)

**Compiler**: `tweego.exe` (from Twine installation)

**Process**:
1. Create `spec/<specname>/output/sugarcube/` directory
2. Read `spec.md`, `constitution.md`, and `variables.md` to build StoryData JSON
3. Concatenate all node .twee files in order
4. Convert mechanic hooks to SugarCube syntax
5. Run tweego.exe with all .twee files as input
6. Generate `spec/<specname>/output/sugarcube/story.html`

**Output**: Playable HTML file - open in browser to play

**Retry logic**: 
- If tweego fails, attempts to auto-fix common issues (unmatched braces, etc.)
- Retries up to 3 times with error feedback

#### Ink (ink → JSON + HTML via inklecate)

**Compiler**: `inklecate.exe` (from Ink installation)

**Process**:
1. Create `spec/<specname>/output/ink/` directory
2. Validate with inklecate (-p flag):
   - Checks for syntax errors
   - Validates knot/stitch references
   - Reports validation errors
3. If validation passes, compile with inklecate (-c flag):
   - Generates `story.json` (compiled story format)
   - Generates `story.html` (HTML wrapper for story.json)
4. HTML wrapper includes:
   - Story metadata and info
   - Links to Ink web player and Inky IDE
   - Embedded story JSON for reference

**Output files**:
- `spec/<specname>/output/ink/story.json` - Compiled story (use with Ink runtime)
- `spec/<specname>/output/ink/story.html` - HTML display wrapper

**Retry logic**:
- If inklecate fails, attempts to auto-fix common divert syntax errors
- Retries up to 3 times with error feedback

#### Multi-Engine Compilation

When using `--all-engines`:
1. Reads export_engines from constitution.md or spec.yml
2. Iterates through each configured engine
3. Compiles each with its appropriate compiler
4. Reports success/failure for each engine
5. Exit code is 0 only if ALL engines succeed

Example:
```bash
speckit.compile --all-engines
# Compiles: sugarcube → tweego, ink → inklecate, etc.
# Outputs results for each engine
```

## Compiler Installation

### SugarCube/Tweego
1. Install Twine: https://twinery.org/
2. Tweego is included in Twine installation
3. Add Twine directory to PATH, or place tweego.exe in scripts/bin/

### Ink/Inklecate
1. Download from: https://github.com/inkle/ink/releases
2. Extract inklecate.exe
3. Add to PATH, or place inklecate.exe in scripts/bin/

## Error Handling

**If compilation fails**:
- Shows specific error from compiler (first 10 lines)
- Attempts automatic fix for common errors
- Retries up to 3 times
- Shows which line numbers have issues (when possible)
- Offers next steps (re-draft nodes, check configuration, etc.)

**Example error output**:
```
❌ Compilation error:
   NODE-001.twee:15: Error: Unmatched '<<'
   NODE-003.twee:8: Error: Undefined variable: $player_name

🔧 Attempting auto-fix...
   Detected: Unmatched macro braces
   Fixed: NODE-001.twee

▶️  Attempt 2/3...
❌ Compilation failed (still has errors)

❌ Compilation failed after 3 attempts
   Check the errors above and fix the source files
```

## Compilation Success Output

When compilation completes successfully:

```
✅ Compilation succeeded on attempt 1
✅ Output: spec/<specname>/output/sugarcube/story.html
   Size: 125000 bytes

Next steps:
- Open story.html in browser to playtest
- Gather feedback with speckit.feedback
- Document issues in tasks.md
```

## Script Support

The scripts support multiple invocation methods:

**Python**:
```bash
python scripts/python/compile.py --spec my-game --engine sugarcube
python scripts/python/compile.py --spec my-game --all-engines
```

**Python**:
```bash
python scripts/python/compile.py --spec my-game --engine sugarcube
python scripts/python/compile.py --spec my-game --all-engines
```

---

## About speckit.verify

`speckit.verify` is now **optional**. The `speckit.compile` command includes all basic structural validation automatically. 

Use `speckit.verify` if you want:
- Full unit test suite (beyond what compile checks)
- Deep branch coverage analysis
- Self-correction loops for complex fixes
   ```

**Compile steps**:
1. Read all files in `spec/<specname>/draft/sugarcube/NODE-*.twee` in node ID order
2. Strip YAML header (front matter) from each file
3. Convert `[MECHANIC:...]` blocks to SugarCube macro syntax:
   - `[MECHANIC:FLAG set=var value=true]` → `<<run $store.variables.var = true>>`
   - `[MECHANIC:VISITED set=visited_NODE_001]` → `<<run $store.visited.NODE_001 = true>>`
   - `[MECHANIC:INVENTORY add=key]` → `<<run $store.inventory.push('key')>>`
   - Other hooks converted per `mechanics.md` specifications
4. Convert `[CHOICE: N options]` blocks to SugarCube `<<link>>` macros
5. Concatenate all processed node files into a single `.twee` file
6. Wrap in Twee 3 StoryData structure with proper header
7. Generate HTML using tweego compiler (if available) or template-based HTML generation

**Output file**: `spec/<specname>/output/sugarcube/[specname].html` (playable)

**Error handling**:
- If `tweego.exe` not found, generate HTML directly from Twee template
- If macro conversion fails, report line number and hook type; offer re-draft option

### Ink (ink → single file)

**Status**: Placeholder (coming soon)

### Renpy (rpy file)

**Status**: Placeholder (coming soon)

### Generic/Markdown (markdown → linked HTML)

**Status**: Placeholder (coming soon)

## Validation Error Report

If validation fails before compilation:

```
🔍 Validating node files...
  ✓ NODE-001.md
  ✓ NODE-002.md
  ❌ NODE-003.md
     • YAML validation failed: Missing required fields: node_id
     • Unclosed MECHANIC hooks: 3 open, 2 closed

❌ Validation failed: 2 error(s) found

⚠️  Compilation halted due to validation errors.
Fix the errors above and try again.
```

## Compilation Success Output

When compilation completes successfully:

```
COMPILATION SUCCESSFUL

Engine: [ENGINE]
Source nodes: spec/<specname>/draft/<ENGINE>/NODE-001.md ... NODE-NNN.md
Output file: spec/<specname>/output/<ENGINE>/[specname].[ext]

Playable: [Y/N]
- For SugarCube: Open [output file] in browser
- For Ink: Compile with Ink compiler: inklecate.exe [output file]
- For Ren'py: Run `renpy [output_directory]`

Node count: [N] nodes compiled
Variable count: [N] variables exported
Total hooks: [N] mechanic hooks converted

Next steps:
- playtest and gather feedback with speckit.feedback
- run speckit.analyze --report for full audit
- document issues in tasks.md
```

## Python Script Support

The `scripts/python/compile.py` script handles:
- Structural validation (YAML, hooks, variables)
- Parsing node YAML headers
- Converting mechanic hooks to engine syntax
- Generating proper StoryData/metadata headers
- Running iterative compilation with error capture
- Generating compilation report with statistics
- Supporting user-defined compilation plugins

**Usage**: `python scripts/python/compile.py --spec [specname] --engine [engine] [--output path] [--skip-validation]`

---

## About speckit.verify

`speckit.verify` is now **optional**. The `speckit.compile` command includes all basic structural validation automatically. 

Use `speckit.verify` if you want:
- Full unit test suite (beyond what compile checks)
- Deep branch coverage analysis
- Self-correction loops for complex fixes
- Detailed test reports

Most workflows: `speckit.compile` alone is sufficient.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "No drafted nodes found" | No files in `draft/<ENGINE>/` | Run `speckit.implement` first |
| "YAML validation failed" | Malformed front matter | Check node header syntax |
| "Unknown hook type" | Invalid [MECHANIC:...] block | Check hook type against mechanics.md |
| "Unclosed hooks" | Mismatched [MECHANIC] and [/MECHANIC] | Balance opening/closing tags |
| "Variable undefined" | Export name missing in `variables.md` | Add export name for target engine |
| "tweego.exe not found" | Twine toolchain not installed | Use template-based HTML generation or install tweego |

---

