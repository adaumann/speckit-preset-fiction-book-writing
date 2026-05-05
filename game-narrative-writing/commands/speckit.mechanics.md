---
description: Declare, update, or promote mechanic hooks in specs/mechanics.md. Use to register new Tier 2 stubs, promote a stub to Tier 1, add a compatibility warning rule, or audit which hooks are declared vs. in use.
handoffs:
  - label: Update Variables
    agent: speckit.constitution
    prompt: Update constitution.md Section II to reflect the mechanic changes just made
    send: false
  - label: Mechanic Health Check
    agent: speckit.status
    prompt: Run a mechanic health summary
    send: false
---

# speckit.mechanics

Manage the `specs/mechanics.md` hook schema document: declare new hooks, promote stubs, and audit hook coverage.

## User Input

```text
$ARGUMENTS
```

Accepted arguments:
- `declare [HOOK_TYPE]` — register a new Tier 2 stub hook schema in `specs/mechanics.md`
- `promote [HOOK_TYPE]` — move a Tier 2 stub to Tier 1; requires translation tables for all declared engine targets
- `audit` — compare hooks declared in `specs/mechanics.md` against hooks used in `nodes/` and `outlines/`; report unused declared hooks and undeclared in-use hooks
- `list` — print all declared hooks with tier, description, and engine support status
- *(no argument)* — equivalent to `list`

## Pre-Execution Checks

1. Confirm `specs/mechanics.md` exists. If absent: "No mechanics.md found — run `speckit.constitution` first to generate the game bible and mechanics document."
2. Load `.specify/memory/constitution.md` Section II (enabled mechanics list) — used to cross-check declarations.
3. If `declare` or `promote`: confirm the hook type name follows kebab-case convention (e.g. `custom_mood`, `faction`).

---

## Mode: `list`

Print a registry table from `specs/mechanics.md`:

```
Declared hooks in specs/mechanics.md:

Tier 1 (fully exported):
  flag             ? Sugarcube  ? Ink
  counter          ? Sugarcube  ? Ink
  visited          ? Sugarcube  ? Ink
  inventory        ? Sugarcube  ? Ink
  timer            ? Sugarcube  ?? Ink (turn-based only)
  trust            ? Sugarcube  ? Ink
  currency         ? Sugarcube  ? Ink
  npc_state        ? Sugarcube  ? Ink
  ending_condition ? Sugarcube  ? Ink
  random           ? Sugarcube  ? Ink
  choice_memory    ? Sugarcube  ?? Ink (CONST mapping)
  clue             ? Sugarcube  ? Ink

Tier 2 (stubs — export with warning):
  knowledge        [Sugarcube: stub] [Ink: stub]
  faction          [Sugarcube: stub] [Ink: stub]
  location_state   [Sugarcube: stub] [Ink: stub]
  object_state     [Sugarcube: stub] [Ink: stub]
  [custom hooks registered for this project...]

Run `speckit.mechanics audit` to check coverage against node files.
```

---

## Mode: `declare [HOOK_TYPE]`

Register a new Tier 2 stub hook in `specs/mechanics.md`.

1. Ask (=3 questions):
   - What does this hook track? (one sentence)
   - What parameters does it take? (e.g. `set=[variable] value=[x]`, `check=[variable] op=gte value=N`)
   - Is there an authoring analogy to an existing Tier 1 hook? (e.g. "like FLAG but for moods")

2. Generate the stub block and append to the **Tier 2** section of `specs/mechanics.md`:

   ```markdown
   ### `[hook_type]` — [Short Description]

   ```
   [MECHANIC:[HOOK_TYPE] [param1]=[value] [param2]=[value]]
   [conditional prose]
   [/MECHANIC]
   ```

   > // TIER 2 STUB — [target] export not yet implemented. Emits: `// UNSUPPORTED HOOK — [hook_type]`
   > Analogy: [existing hook analogy if provided]
   ```

3. Confirm: "`[HOOK_TYPE]` added to Tier 2 in `specs/mechanics.md`."
4. Remind: "Add `[hook_type]` to `.specify/memory/constitution.md` Section II enabled mechanics list if you want it active for this project."

---

## Mode: `promote [HOOK_TYPE]`

Promote a Tier 2 stub to Tier 1 by adding full translation tables.

1. Load the existing stub block for `[HOOK_TYPE]` from `specs/mechanics.md`.
2. Ask (=4 questions, only what isn't clear from the stub):
   - Sugarcube macro translation for each parameter
   - Ink `~` or conditional translation for each parameter
   - Any compatibility warning conditions (e.g. "Ink requires X")
   - Should `export.py` handle this automatically or emit a manual TODO comment?

3. Replace the Tier 2 stub with a full Tier 1 block (with translation table) in `specs/mechanics.md`.
4. Add a row to the Compatibility Warning Rules table if any edge case was identified.
5. Confirm: "`[HOOK_TYPE]` promoted to Tier 1 in `specs/mechanics.md`. Update `export.py` to implement the translation."
6. Note: "If using `export.py`, the actual translation logic must be added manually to `scripts/python/export.py`. This command only updates the schema document."

---

## Mode: `audit`

Compare declared hooks against in-use hooks across all node and outline files.

1. Scan all `nodes/NODE-*.md` and `outlines/*.md` for `[MECHANIC:` blocks.
2. Build a list of all in-use hook types (unique).
3. Compare against declared hooks in `specs/mechanics.md`.

Output:

```
Mechanic Audit — [GAME_TITLE]

Declared and in use:
  flag, counter, trust, ending_condition, [...]

Declared but never used:
  ??  currency     — declared in mechanics.md, no nodes use it
  ??  timer        — declared in mechanics.md, no nodes use it

Used but not declared in mechanics.md:
  ?  mood_state   — used in NODE-007, NODE-012; run `speckit.mechanics declare mood_state`

Tier 2 stubs in active use (will produce export warnings):
  ??  knowledge    — used in 3 nodes (NODE-004, NODE-009, NODE-014)
  ??  faction      — used in 1 node (NODE-022)
```

Suggest: "Run `speckit.mechanics promote [HOOK_TYPE]` for any Tier 2 hooks in active use before export."

