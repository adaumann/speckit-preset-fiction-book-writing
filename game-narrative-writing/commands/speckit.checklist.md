---
description: Run the quality checklist for one or more node files. Checks structural integrity, craft rules, hook declarations, choice design, and game bible compliance. "Unit tests for nodes." Saves a checklist file per node and produces a weighted PASS/FAIL verdict.
handoffs:
  - label: Fix Checklist Failures
    agent: speckit.revise
    prompt: Fix the failures flagged by the checklist for this node
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Per-node checks have passed — run a full continuity check now
    send: true
---

# speckit.checklist

**CRITICAL CONCEPT**: Node checklists are **quality gates for node files** — unit tests that validate whether a drafted node fulfils its structural and craft obligations.

**NOT for verifying story events**:
- ? NOT "Does this node match the plan?"
- ? NOT "Is the plot logical here?"

**FOR node quality validation**:
- ? "Are all choice targets valid node IDs?" (structural integrity)
- ? "Are all variables declared in variables.md?" (hook compliance)
- ? "Is prose coherent without hook blocks?" (craft)
- ? "Do choice labels avoid meta-language?" (player experience)
- ? "Are prohibited phrases absent?" (game bible compliance)

**Metaphor**: If your node is a unit of player experience, the checklist is its test suite — verifying the node works structurally, the prose works as prose, and the mechanic hooks work as intended.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- A node ID (e.g. `NODE-003`) — run checklist for that node
- A list of node IDs — run checklist for each
- `--act [N]` — check all nodes in the specified act
- `--all` — check all nodes with status DRAFT or APPROVED
- `--strict` — also validate Tier 2 stub hooks for completeness
- Nothing — check the most recently modified node file

## Pre-Execution Checks

**Check for extension hooks (before checklist generation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_checklist` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Execution Steps

### Step 1 — Setup

Run `{SCRIPT}` from repo root. Determine target node(s) from `$ARGUMENTS`.

For each target node:
- Confirm the node file exists in `nodes/`.
- Read the node file (YAML frontmatter + prose body).
- If the node has status SKIP, skip it and note in the report.

### Step 2 — Load Context

Load the following (required):
- `.specify/memory/constitution.md` — POV, tone, Prose Style Mode (Section VII), `style_mode`, `prose_profile`
- `.specify/memory/craft-rules.md` — craft rules (NR-NNN, PR-NNN per active prose profile), prohibited phrases, anti-AI clichés filter
- `specs/variables.md` — declared variable registry for NR-003 / NR-006
- `specs/mechanics.md` — valid hook types and syntax for MC checks

Load the following (if present):
- `specs/characters/` — NPC profiles for trust range and dialogue register checks (dialogue style per prose profile)
- `outlines/[NODE_ID].md` — node outline for outline-gate compliance check
- `specs/plan.md` — for upstream path analysis (NR-006)

### Step 3 — Clarifying Questions (=2)

Ask at most 2 targeted questions if the node file or loaded context leaves a check ambiguous:
- Only ask what cannot be resolved from the files
- Focus on: intended trust state at this node, whether a specific prohibited phrase is intentional dialect, whether a Tier 2 stub is expected to remain unimplemented

Skip if the node and context provide enough information to run all checks without ambiguity.

### Step 4 — Run Checks

For each node, evaluate all items in the four sections below using `templates/checklist-template.md` as the output structure. Mark each item ? / ? / ??.

**NR — Node Rules** (structural integrity)
- NR-001: Non-terminal nodes have = 2 choices in `## Choices`
- NR-002: All choice targets are valid node IDs (exist in `outlines/` or `nodes/`)
- NR-003: All variables in `variables_read` and `variables_set` are declared in `variables.md`
- NR-004: All mechanic hook blocks use valid syntax and registered hook types (per `mechanics.md`)
- NR-005: Tier 2 hook stubs include `// TIER 2 STUB` comment
- NR-006: No variable is read that cannot be set on any upstream path leading to this node
- NR-007: Ending nodes have no outgoing choices
- NR-008: Trust score changes are within the declared NPC range (per `characters/` profile)
- NR-009: Choices use the export-required format: `- [Label](NODE_ID) <!-- condition -->` under `## Choices` heading

**PR — Prose Rules** (craft and voice)
- PR-001: POV is consistent with `constitution.md` `player_perspective` (or has an approved override)
- PR-002: No prohibited phrases from `constitution.md` appear in prose
- PR-003: Choice labels use active verb phrases and avoid meta-language (e.g. "Ask about the key" not "Select dialogue option")
- PR-004: Dialogue register matches NPC trust state at this node's variable value
- PR-005: Prose coheres without hook blocks (narrative reads as complete if mechanic blocks are removed)
- PR-006: At least one concrete sensory detail (sound, smell, texture, temperature — not visual only)
- PR-007: No choice or action is trivialized or telegraphed by the prose (player's decision space is respected)
- PR-008: Prose tense, sentence rhythm, and vocabulary register are consistent with Prose Style Mode (Section VII of `constitution.md`); anti-AI filter patterns are absent
- PR-009: Location atmosphere is established through sensory detail or description (from `specs/locations.md` Setting Anchors field if present)
- PR-010: Sensory details are consistent with the location or NPC context (e.g., a sterile facility has clinical smells/sounds, not organic ones)
- PR-011: Emotional subtext is shown through character reaction or environmental description, not explicitly named (e.g., "tension hung in the air" not "I felt tense")

**MC — Mechanic Compliance** (hook balance and fairness)
- MC-001: Every trust-shifting choice has narrative justification in prose
- MC-002: No single choice dominates trivially — all choices are meaningful trade-offs
- MC-003: Timer failure conditions are handled in a downstream node (or flagged as `[NEEDS NODE]`)
- MC-004: If `--strict`: Tier 2 stub hooks include a `// TODO:` comment describing expected implementation
- MC-005: No mechanic hook reads a variable not listed in `variables_read` in the frontmatter
- MC-006: Every `MECHANIC:CURRENCY` hook includes `variable=` and that variable is declared as `type: currency` in `variables.md`; flag missing or wrong-type declaration as CRITICAL

**GB — Game Bible Compliance** (spec authority)
- GB-001: Node tone is consistent with the genre and emotional register defined in `constitution.md`
- GB-002: Any NPC appearing in this node is consistent with their character profile (voice, state, goal)
- GB-003: World-rule constraints (from `world-building.md`) are not violated in prose or choice outcomes
- GB-004: Engine target constraints are respected (no unsupported syntax for the declared export target)

### Step 5 — Score and Verdict

Calculate the weighted **RTG — Overall Rating**:

| Section | Weight |
|---|---|
| Node Rules (NR) | 30% |
| Prose Rules (PR) | 25% |
| Mechanic Compliance (MC) | 25% |
| Game Bible Compliance (GB) | 20% |

Score each section 1–10 based on items passed. Apply weights. A weighted total = 7 is required to pass.

**Hard-fail gates** (FAIL regardless of weighted score):
- Any NR-002 failure (unknown choice target — export will break)
- Any NR-006 failure (unreadable variable — runtime error)
- Any NR-009 failure (wrong choices format — `export.py` will drop all choices)

### Step 6 — Write Checklist File

Save to `checklists/[NODE_ID]-checklist.md` using `templates/checklist-template.md`.

Confirm: `? Saved: checklists/[NODE_ID]-checklist.md`

### Step 7 — Report

Output per node:

```
[NODE_ID] — [PASS / FAIL]  (score: [N.N] / 10)

  NR  [N passed / 9]   PR  [N passed / 11]   MC  [N passed / 6]   GB  [N passed / 4]

  Failures:
    [RULE_CODE]  [brief description]
      ? [quoted offending line or frontmatter value]

  Hard-fail gates:
    NR-002  ? / ?
    NR-006  ? / ?
    NR-009  ? / ?

  Top revision priorities:
    1. [Highest-impact item]
    2. [Second priority]
    3. [Third priority if applicable]
```

If FAIL: `Run speckit.revise [NODE_ID] to fix failures before this node can be approved.`

If checking multiple nodes, append a summary table:

```
| Node | Score | Verdict | Hard-fail? | Top failure |
|---|---|---|---|---|
| NODE-003 | 8.1 | PASS | — | — |
| NODE-007 | 5.4 | FAIL | NR-009 | choices format |
```

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_checklist` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

