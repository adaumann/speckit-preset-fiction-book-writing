---
description: Run comprehensive unit test suite on drafted nodes. Includes structural tests, engine compiler validation, and self-correction loops. Optional; speckit.compile includes basic validation automatically.
handoffs:
  - label: Re-draft failing node
    agent: speckit.implement
    prompt: Re-draft the node that failed validation
    send: true
  - label: View implementation instructions
    agent: speckit.implement
    prompt: Show implement instructions
    send: false
scripts:
  py: scripts/python/verify.py --spec $SPECNAME --engine $ENGINE
---

# speckit.verify

Run comprehensive unit tests on drafted node files. 

**When to use**: After `speckit.compile` if you want thorough validation. Not required for standard workflows.

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `[NODE_ID]` — validate a single node (e.g. `NODE-003`)
- `[NODE_ID] [NODE_ID] ...` — validate a list of nodes
- `--all` — validate every file in `nodes/`
- `--unit-tests` — run the full cross-node unit test suite only (no compiler)
- `--structural-only` — run only structural unit tests (no compiler/linter invocation)
- *(no argument)* — validate every DRAFT node that has no `verified: true` flag in its header

## What this command does

`speckit.verify` runs two layers of validation in sequence:

### Layer 1 — Structural Unit Tests (always runs)

Executes `scripts/python/validation/test_nodes.py` against the target node(s).

Tests included:
| ID | Name | What it checks |
|---|---|---|
| T-01 | YAML-HEADER | YAML front-matter present and parseable |
| T-02 | YAML-FIELDS | All required header fields present (node_id, title, status, drafted) |
| T-03 | HOOK-SYNTAX | Every `[MECHANIC:...]` tag is properly closed |
| T-04 | CURRENCY | CURRENCY hooks have `variable=` declared |
| T-05 | RANDOM | RANDOM hooks have `min=` and `max=` |
| T-06 | DEAD-END | Non-terminal nodes have at least one outgoing choice |
| T-07 | DUPLICATE-ID | No two nodes share the same `node_id` |
| T-08 | VAR-DECLARED | All hook variables are registered in `specs/variables.md` |
| T-09 | CHOICE-TARGET | All choice link targets exist in `specs/plan.md` |

### Layer 2 — Engine Compiler / Linter (skipped if `--structural-only`)

Executes `scripts/python/validation/validate_engine.py [FILE] --target [EXPORT_TARGET]` where
`EXPORT_TARGET` is read from `.specify/memory/constitution.md`.

| Target | Toolchain | Install |
|---|---|---|
| `ink` | `inklecate -p` | https://github.com/inkle/ink/releases |
| `twine` / `sugarcube` | `tweego` | https://www.motoslave.net/tweego/ |
| `renpy` | `renpy [project] lint` | Ren'Py SDK on PATH |
| `unity` (`.yarn`) | `ysc compile` | https://github.com/YarnSpinnerTool/YarnSpinner-Console |
| `unity` (`.cs`) | `dotnet build` | .NET SDK |
| `escoria` | `godot --check-only` | Godot on PATH |
| `ags` | *(static analysis only)* | No CLI compiler available |
| `generic` | *(structural tests only)* | — |

Toolchain `[TOOLCHAIN]` warnings (binary not found) are reported but **do not fail** the build.
Hard errors (syntax errors returned by the compiler) **do fail** the build and trigger the loop.

## Self-Correction Loop

If any hard errors are found in Layer 1 or Layer 2:

```
Attempt 1 of 3
  - Analyze the error messages
  - Identify the specific lines / constructs causing the failure
  - Apply the minimal targeted fix to the node file
  - Re-run validate_engine.py
  → If clean: mark as verified and continue
  → If still failing: proceed to Attempt 2
```

The loop runs up to **3 attempts**. After 3 failed attempts:
- Output the full error log
- Do **NOT** mark the node as verified
- Prompt the user:
  ```
  ⚠ VERIFY FAILED after 3 attempts: nodes/[NODE_ID].[EXT]
  
  Remaining errors:
  [error list]
  
  Options:
    1. Show me the failing section so I can fix it manually.
    2. Retry with a different drafting strategy (delegates to speckit.implement --force).
    3. Skip this node for now and continue with others.
  ```

## Execution Steps

1. **Resolve target list**: From `$ARGUMENTS` or scan `nodes/` for files without `verified: true`.

2. **Load constitution**: Read `.specify/memory/constitution.md` → extract `export_target`.

3. **For each target node file**:

   a. Run Layer 1 (structural tests):
      ```
      python scripts/python/validation/test_nodes.py --nodes-dir nodes --specs-dir specs --json
      ```
      Filter results to the current node only.

   b. Run Layer 2 (compiler):
      ```
      python scripts/python/validation/validate_engine.py nodes/[NODE_ID].[EXT] --target [EXPORT_TARGET]
      ```

   c. If errors found → enter **Self-Correction Loop** (max 3 attempts).

   d. If clean after loop:
      - Add `verified: true` and `verified_at: [YYYY-MM-DD]` to the node's YAML header.
      - Report: `✓ VERIFIED: [NODE_ID] — [n] attempt(s)`

4. **After all nodes processed**, print summary table:
   ```
   | Node     | Status   | Attempts | Errors |
   |----------|----------|----------|--------|
   | NODE-001 | ✓ Clean  | 1        | 0      |
   | NODE-002 | ✓ Fixed  | 2        | 0      |
   | NODE-003 | ✗ Failed | 3        | 4      |
   ```

5. If `--unit-tests` flag was passed (or after all individual nodes are verified), run the full
   cross-node test suite:
   ```
   python scripts/python/validation/test_nodes.py --nodes-dir nodes --specs-dir specs
   ```
   Report failures and suggest corrections.

## Toolchain Setup (first-time)

If any `[TOOLCHAIN]` warning is emitted, print the following once per missing tool:

```
ℹ  TOOLCHAIN MISSING: [tool]
   Install: [install URL]
   Without it, only static/structural checks will run.
   Add [tool] to PATH and re-run speckit.verify to enable full compilation checks.
```
