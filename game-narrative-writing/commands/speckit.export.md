---
description: Export all approved nodes to Twine/Sugarcube (.twee) or Ink (.ink) via scripts/python/export.py.
handoffs:
  - speckit.analyze: If structural errors block export
  - speckit.checklist: If nodes have open checklist failures
scripts:
  - scripts/python/export.py
---

# speckit.export

Export all approved node files to a target engine format using `export.py`.

**Gate requirement**: All nodes must have `status: APPROVED` in their frontmatter. Nodes with `status: DRAFT` are excluded from export with a warning. `status: SKIP` nodes are silently excluded.

## User Input

Provide one of:
- `--target sugarcube` — export to Twee 3 format (Sugarcube)
- `--target ink` — export to Ink format
- `--target renpy` — export to Ren'Py format (`.rpy`) *(v1.x roadmap — see note below)*
- `--target both` — export to Sugarcube and Ink

Required flags:
- `--target sugarcube|ink|both`

Optional flags:
- `--dry-run` — validate export without writing output files; report all warnings
- `--output [path]` — specify output directory (default: `export/`)
- `--act [N]` — export one act only (useful for staged testing)

## Pre-Execution Checks

1. Confirm `nodes/` contains at least one APPROVED node.
2. Confirm `variables.md` exists — required for variable initialization in export header.
3. Warn for any node with `status: DRAFT` — it will be excluded.
4. Load `.specify/memory/constitution.md` — engine target, POV configuration.
5. Confirm engine target in constitution.md matches `--target` flag (or warn if different).

## Outline

1. **Collect approved nodes**:
   - Read all `nodes/NODE-*.md` files with `status: APPROVED`
   - Build ordered node list from `flowmap.md` node order
   - Identify the root node (first node — no incoming edges)

2. **Run export.py**:
   ```
   python scripts/python/export.py --target [sugarcube|ink] --output export/
   ```
   - export.py parses each node's YAML frontmatter and prose body
   - Translates `[MECHANIC:TYPE]` hook blocks to engine syntax using translation tables in `specs/mechanics.md`
   - **Tier 1 hooks translated**: `flag`, `counter`, `visited`, `inventory`, `timer`, `trust`, `currency` (requires `variable=`), `npc_state`, `ending_condition`, `random`, `choice_memory` (Ink: emits CONST mapping comment block), `clue`
   - **CURRENCY**: if `variable=` is absent, export aborts with: `Error: MECHANIC:CURRENCY in [NODE_ID] is missing variable= — add the currency variable name.`
   - **RANDOM**: translates to `random(min, max)` (Sugarcube) / `RANDOM(min, max)` (Ink); emits a warning if Ink version < 1.1 cannot be confirmed
   - **CHOICE_MEMORY** (Ink): emits `CONST [LABEL_CONST] = N` declarations before the knot and maps string values to integer constants; includes a `// CHOICE_MEMORY mapping:` comment block
   - **Compound `condition=`**: emits the expression verbatim after the choice link — no translation
   - Emits Tier 2 hook stubs as `// UNSUPPORTED HOOK: [TYPE]` comments in output
   - Emits compatibility warnings for: timer seconds (Sugarcube: JS required, Ink: not supported), inventory capacity check in Ink, `npc_state` with > 4 custom values in Ink

3. **Sugarcube output** (`export/[game_title].twee`):
   - File header: `:: StoryTitle` passage + `:: StoryData` JSON with tag/format config
   - Variable initialization: `:: StoryInit` passage deriving from `variables.md` defaults
   - One `:: NodeTitle [tags]` passage per node
   - Mechanic hooks translated to Sugarcube macro syntax

4. **Ink output** (`export/[game_title].ink`):
   - `VAR` declarations block deriving from `variables.md`
   - One `=== node_title ===` knot per node
   - Mechanic hooks translated to Ink `~` and `->` syntax
   - NPC state integer enums declared as `VAR npc_[name]_state = 0`

5. **Ren'Py output** (`export/[game_title].rpy`) *(roadmap — not yet implemented)*:
   - Emit a clear error: "Ren'Py export is not yet supported in export.py. Declare `engine_target: renpy` in `constitution.md` to reserve this target for a future export.py update."
   - List what would be needed: `label` per node, `menu:` blocks for choices, variable `$` declarations, `jump` for branch targets.
   - Output a skeleton `.rpy` file with `# TODO: RENPY EXPORT` stubs so the author can see the intended structure.

6. **Output**
   - Report: "Exported [N] nodes to [target]. Warnings: [N]."
   - List all warnings by node and hook type
   - If `--dry-run`: "Dry run complete — no files written. [N] warnings found."
   - Suggest: "Review compatibility warnings above. Run `speckit.status --export` to confirm export readiness."
