---
description: Validate player agency — verify choices have consequences and aren't illusory. Detects dead choices, forced branches, and choice-outcome impact via variable state tracking.
handoffs:
  - label: Revise Branches
    agent: speckit.revise
    prompt: Some choices are forced or illusory. Please revise to add real consequences.
    send: true
  - label: Check Endings
    agent: speckit.endings
    prompt: After validating choice agency, check if all endings are satisfying.
    send: true
---

# speckit.agency

Validate player agency — ensure player choices **meaningfully affect outcomes** rather than being illusory or forced.

## Agency Principle

**True agency** = Player choice determines outcome state. **False agency** = Choice appears to matter but leads to same endpoint regardless of selection.

This command validates:
- ✅ Each choice branches to meaningfully different outcomes
- ✅ Chosen branch leads to different ending(s) than unchosen branches
- ✅ Variable state diverges based on choice selection
- ✅ No "forced branches" (all paths reconverge to identical state before reaching ending)
- ✅ Choice consequences are **meaningful** (not cosmetic text differences only)

**NOT validated here** (use other tools):
- ❌ Ending quality (use `speckit.endings`)
- ❌ Emotional impact of choices (use `speckit.tone`)
- ❌ Whether consequences are telegraphed (use `speckit.foreshadow`)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit entire game for all choice nodes
- Node ID (e.g., `NODE-005`) — audit a single node's choices
- `--branch [BRANCH_ID]` — audit all choices in one branch

Optional flags:
- `--strict` — fail on cosmetic-only consequences (not just endpoint differences)
- `--show-paths` — display all possible endpoints from each choice
- `--variable-only` — focus only on variable state divergence (skip dialogue differences)

## Pre-Execution Checks

1. Confirm `specs/plan.md` exists with node graph and branch structure
2. Confirm `specs/variables.md` exists with all declared variables
3. Confirm `specs/endings.md` exists with all registered endings
4. Load all `draft/[ENGINE]/NODE-*.md` files to analyze actual choice text and variable reads/sets
5. If `--show-paths` flag: load `specs/relationships.md` if present (for NPC state impact)

## Execution Steps

### 1. **Load Spec**
   - Read `plan.md`: node graph, branch structure, ending nodes
   - Read `variables.md`: all variables with type and scope
   - Read `endings.md`: all registered ending IDs
   - Read all node draft files: extract choice syntax and variable operations

### 2. **Map Choice → Outcome**

For each **choice node** in the game:
   - **Parse choice targets**: Where does each option branch?
   - **Trace variable impact**: What variables are read/set in each branch?
   - **Follow to endpoints**: Do both branches lead to the same ending(s)?

**Example structure**:
```
NODE-005 (choice node):
  Choice A → NODE-007
    Variables set: trust(marcus) = 1, player_suspicion = true
    
  Choice B → NODE-008
    Variables set: trust(marcus) = -1, player_awareness = true
    
  Both → NODE-020 (final node)
```

### 3. **Detect Agency Violations**

#### 🔴 **VIOLATION: Forced Branch**
A choice where all options lead to **identical variable state AND same ending**.

```
NODE-005 (FORCED):
  Choice A → NODE-007 → [set nothing] → NODE-020
  Choice B → NODE-008 → [set nothing] → NODE-020
  
  BOTH lead to ending: ENDING-001 with no variable diff
  → This choice is ILLUSORY
```

**Report**:
```
❌ NODE-005: Forced branch
   Both options reconverge with zero variable divergence
   Impact: Choice is cosmetic only
   Fix: Ensure Choice A and Choice B set different variables or lead to different ending
```

#### 🟡 **VIOLATION: Cosmetic-Only (if --strict)**
A choice where branches diverge in **dialogue/prose** but not in **game state** (variables or endings).

```
NODE-005 (COSMETIC):
  Choice A: "I trust you" → Same dialogue, no variable change
  Choice B: "I doubt you" → Different dialogue, no variable change
  Both → NODE-020 with identical variables
  
  → Choice affects only TEXT, not GAME STATE
```

**Report** (only with `--strict`):
```
⚠️  NODE-005: Cosmetic choice (--strict mode)
   Variables unchanged by either option
   Impact: Choice affects tone but not outcome
   Consider: Add relationship variable to make choice meaningful
```

#### ✅ **VALID: Divergent Outcome**
A choice where branches lead to:
- Different variable state, OR
- Different endpoints, OR
- Different ending(s) with different variable snapshots

```
NODE-005 (VALID):
  Choice A: "Help Marcus" 
    → NODE-007: set trust(marcus) += 1
    → Can reach: ENDING-ALLY or ENDING-RIVAL
    
  Choice B: "Betray Marcus"
    → NODE-008: set trust(marcus) -= 2
    → Can reach: ENDING-ENEMY only
    
  ✅ Different endings reachable based on choice
```

### 4. **Generate Agency Audit Report**

Create `specs/agency-audit.md`:

```markdown
## Agency Audit: [GAME_NAME]

**Date**: [ISO]
**Scope**: [all nodes | NODE-XXX | branch name]

| Node ID | Choice Type | Option A | Option B | Divergence | Status |
|---------|-------------|----------|----------|-----------|--------|
| NODE-005 | Trust? | Help | Betray | Variables + Endings | ✅ VALID |
| NODE-010 | Path choice | North | South | Variables only | ✅ VALID |
| NODE-015 | Dialogue | Agree | Refuse | Dialogue only | ⚠️ COSMETIC |
| NODE-020 | Illusory | Accept | Decline | NONE | ❌ FORCED |

### Violations Found

**🔴 Forced Branches**: 3
- NODE-020: Both options reconverge with zero state change
- NODE-025: "Yes/No" leads to identical ending regardless
- NODE-030: Dialogue differs but no variable impact

**🟡 Cosmetic-Only (--strict)**: 2
- NODE-015: Text flavor choice, no game state impact
- NODE-018: Tone variation, no mechanical consequence

### Summary

- **Total choice nodes**: 45
- **Fully branching choices**: 38 (84%)
- **Forced branches**: 3 (7%)
- **Cosmetic-only**: 2 (4%)
- **Ambiguous**: 2 (5%)

### Recommendations

**Priority 1 (Fix Forced Branches)**:
1. NODE-020: Add variable to differentiate outcomes
2. NODE-025: Split branch to lead to different endings
3. NODE-030: Add trust/relationship variable consequences

**Priority 2 (Enhance Cosmetic Choices)**:
1. NODE-015: Add exploration flag or character knowledge state
2. NODE-018: Link to later NPC reaction or dialogue option

**Priority 3 (Clarify Ambiguous)**:
1. NODE-XXX: Review for hidden variable implications
```

### 5. **Agency Strength Metric**

Calculate and report:

**Agency Ratio** = (Branching choices) / (Total choices)
- 80%+ = Strong agency (player feels empowered)
- 50-79% = Moderate agency (mostly player-driven)
- 20-49% = Weak agency (many forced moments)
- <20% = Weak agency (linear with illusion of choice)

**Endpoint Diversity** = (Unique ending states reachable) / (Theoretical maximum)
- How many of the endings.md entries are actually reachable from the root?
- Are some endings inaccessible due to forced branches blocking paths?

### 6. **Show Paths** (optional with --show-paths)

For each choice node, display all possible outcome states:

```
NODE-005: "Confront or Forgive?"

Path 1: Confront
  → NODE-007 → trust(marcus) = -2
  → NODE-012 → marcus_hostile = true
  → NODE-015 (ending gate)
  → Can reach: ENDING-BETRAYED, ENDING-RIVAL, ENDING-ENEMY

Path 2: Forgive
  → NODE-008 → trust(marcus) = 2
  → NODE-013 → marcus_grateful = true
  → NODE-015 (ending gate)
  → Can reach: ENDING-ALLY, ENDING-NEUTRAL, ENDING-HERO
```

**This helps writers visualize**: 
- Which ending(s) are reachable from which choice
- What variable state must exist to reach specific endings
- Where forced reconvergences happen

### 7. **Report**

Output `agency-audit.md` with:
- Violation count by type (forced, cosmetic, valid)
- Agency strength metrics
- Specific recommendations for fixes
- If `--show-paths`: Full endpoint visualization for each choice

---

## Important Notes

**Agency vs. Outcome**: A choice has **agency** if it changes state, NOT if it changes ending. Some choices can diverge on variables but converge back to the same ending (this is still valid agency — the journey differs).

**Forced Branches**: The enemy of agency. If both paths lead to identical state AND ending with no difference, remove the choice or add consequences.

**Cosmetic Choices**: Acceptable in moderation (flavor decisions). If >10% of choices are cosmetic-only, consider adding mechanical weight to player decisions.

**Reachability**: High agency doesn't matter if all choices lead to the same ending. Use `speckit.endings` to verify multiple endings are actually reachable from the agency nodes you're testing.

