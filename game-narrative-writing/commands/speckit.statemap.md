---
description: Variable state mapper — visualize game state transitions across branches. Detects unreachable states, dead-end variable combos, untracked variable mutations.
handoffs:
  - label: Check Continuity
    agent: speckit.continuity
    prompt: After analyzing state reachability, verify variables are consistent across nodes.
    send: true
  - label: Audit Agency
    agent: speckit.agency
    prompt: After mapping state transitions, verify choice consequences map to state changes.
    send: true
---

# speckit.statemap

Variable state mapper — visualize **game state transitions** across branches. Detects unreachable states, dead-end variable combinations, and untracked variable mutations.

## State Mapping Principle

**Well-mapped state** = All reachable game states are intentional; variable transitions are tracked; no dead ends.

**Poor state mapping includes**:
- ❌ Unreachable state (variable combo possible by definition, but no branch reaches it)
- ❌ Dead-end state (state reached, but next node requires incompatible variable)
- ❌ Untracked mutation (variable changes silently; no node explicitly sets it)
- ❌ State paradox (two branches converge with conflicting variable states)

**Valid state mapping includes**:
- ✅ All reachable states are intentional
- ✅ Variable transitions are explicit (node says "set X=3")
- ✅ Branches can merge when variables are compatible
- ✅ Multiple branches can reach same state intentionally

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — map all variable states across all branches
- Variable name (e.g., `relationship_marcus`) — track state transitions of one variable
- `--branch [BRANCH_ID]` — map state transitions in one branch only
- `--reachability-check` — verify all theoretical states are reachable

Optional flags:
- `--strict` — flag any variable change not explicitly set in node
- `--show-graph` — ASCII state transition graph
- `--show-paths` — display variable state for each branch path
- `--check-convergence` — verify branch merge points have compatible states

## Pre-Execution Checks

1. Load `specs/variables.md`: All game variables, types, ranges, initial values
2. Load `specs/plan.md`: Branch structure, node sequence, merge points
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Extract all variable mutations (assignments, increments, flag sets)
5. Identify branch divergence and convergence points

## Execution Steps

### 1. **Define State Space**

From variables.md, define all possible variable states:

```
VARIABLE: relationship_marcus
  Type: Integer (0–100)
  Initial: 50
  
Reachable values (by design):
  • 50: Initial (neutral)
  • 65: After NODE-010 (help scene)
  • 80: After NODE-015 (trust proven)
  • 90: After NODE-020 (alliance)
  • 35: After NODE-025 (betrayal)
  
Theoretical max: 100
Theoretical min: 0
Actual reachable: 50, 65, 80, 90, 35
Unreachable: 0–34, 36–49, 51–64, 66–79, 81–89, 91–100

---

VARIABLE: city_status
  Type: Enum (safe | under_siege | locked_down | fallen)
  Initial: safe
  
State transitions:
  safe → under_siege (at NODE-012)
  under_siege → locked_down (at NODE-018)
  locked_down → fallen (at NODE-025+)
  under_siege → safe (optional choice at NODE-020)
```

### 2. **Track State Per Branch**

For each branch, track variable states at each node:

```
BRANCH A: Help Victor

Checkpoint:  state_victor / relationship_marcus / city_status

NODE-005:    freed / 50 / safe
NODE-010:    freed / 65 / safe             [relationship +15]
NODE-015:    freed / 65 / under_siege      [city upgraded]
NODE-020:    freed / 80 / under_siege      [relationship +15, choice confirmed]
NODE-025:    escaped / 80 / locked_down    [victor_status=escaped, city upgraded]
ENDING:      escaped / 90 / locked_down    [relationship +10]

State trajectory:
  ✅ All transitions explicit (each change noted)
  ✅ No sudden changes (variables consistent)
  ✅ Linear progression (no conflicts)

---

BRANCH B: Betray Victor

Checkpoint:  state_victor / relationship_marcus / city_status

NODE-005:    freed / 50 / safe
NODE-010:    freed / 65 / safe
NODE-015:    freed / 65 / under_siege
NODE-020:    freed / 35 / under_siege      [relationship -30, betrayal]
NODE-022:    captured / 35 / under_siege   [victor_status=captured]
NODE-025:    captured / 30 / locked_down   [relationship -5, guilt], city upgraded]
ENDING:      captured / 25 / locked_down   [relationship -5 more]

State trajectory:
  ✅ All transitions explicit
  ✅ Betrayal causes major relationship drop
  ✅ No conflicts (consistent throughout)

---

BRANCH C: Neutral

Checkpoint:  state_victor / relationship_marcus / city_status

NODE-005:    freed / 50 / safe
NODE-010:    freed / 50 / safe            [no action, no change]
NODE-012:    freed / 50 / safe            [ignored Victor entirely]
NODE-018:    freed / 50 / under_siege     [automatic upgrade]
NODE-025:    freed / 50 / locked_down     [automatic upgrade]
ENDING:      freed / 50 / locked_down     [no relationship change]

State trajectory:
  ✅ Neutral path: Variables unchanged when not acted on
  ✅ Automatic transitions apply equally
  ✅ No conflicts
```

### 3. **Detect State Space Problems**

#### 🔴 **PROBLEM: Unreachable State**
Variable combo possible by definition, but no branch reaches it.

```
Variables:
  • relationship_marcus: 0–100
  • alliance_status: none | weak | strong

Theoretical states: 101 × 3 = 303 combinations

Actual reachable (from branch analysis):
  • relationship_marcus: 35, 50, 65, 80, 90
  • alliance_status: none, weak, strong

Reachable combos: 5 × 3 = 15 combos

Unreachable examples:
  ❌ relationship_marcus=75, alliance_status=strong
     (No branch reaches this combo; why define it?)
  
  ❌ relationship_marcus=0, alliance_status=weak
     (Variable ranges allow it, but no story path creates it)

Impact:
  • Ending check: If ending requires relationship > 70 + strong alliance,
    player MUST get exactly 80/90 + strong (limited paths)
  • Dead end: If late-game node requires relationship=75, unreachable!

Status: 🔴 DESIGN BLOAT

Fix options:
  1. Add branch that reaches this state (expand design)
  2. Remove this variable combo from theoretical space (tighten definition)
  3. Add conditional route to this state (add choice node)
```

#### 🟡 **PROBLEM: Dead-End State**
State is reached, but next content requires incompatible state.

```
BRANCH A progression:
  NODE-020: state_victor = escaped, relationship_marcus = 80
  
NODE-025 requirement:
  "If relationship_marcus > 75, Marcus helps you"
  
Check:
  relationship_marcus = 80 ✅ PASSES (>75)
  
---

BRANCH B progression:
  NODE-020: state_victor = captured, relationship_marcus = 35
  
NODE-025 requirement:
  "If relationship_marcus > 75, Marcus helps you"
  
Check:
  relationship_marcus = 35 ❌ FAILS (<75)
  Marcus doesn't help
  
But what if:
  NODE-025: "If state_victor=captured AND relationship_marcus < 50, you're arrested"
  35 < 50 ✅ PASSES
  
  NODE-026: Prison escape required
  
This isn't dead-end, it's a branch. ✅ OK

---

ACTUAL DEAD-END EXAMPLE:

NODE-015: relationship_marcus = 65
NODE-020 requirement: "If relationship_marcus > 75, proceed to NODE-025"
           "Else fail requirement and loop back to NODE-018"
           
But if relationship = 65:
  • Doesn't pass requirement
  • Loop back to NODE-018 (already visited, what do you do?)
  • No way to increase relationship further
  
Status: 🟡 DEAD END (trapped in loop)

Fix: Add alternate path at NODE-020 for low relationship:
     "If relationship < 75, take alternate route to NODE-025"
```

#### 🔵 **PROBLEM: Untracked Mutation**
Variable changes but no node explicitly sets it.

```
NODE-015:
  Dialogue: "Marcus looks disappointed. Things between us are different now."
  
Game state check:
  Before NODE-015: relationship_marcus = 80
  After NODE-015: relationship_marcus = 65
  
Question: Where did the -15 come from?
  
Search node:
  No line says "relationship_marcus = 65"
  No line says "relationship_marcus -= 15"
  
Cause: Unknown (probably editor error or implicit consequence)

Status: 🔵 UNTRACKED MUTATION

Problem: Future content won't know why relationship dropped
         If loop back to NODE-015 happens, does relationship drop again?

Fix: Add explicit line:
     "Marcus's disapproval impacts relationship"
     relationship_marcus = 65  [was 80]
     
     OR add dialogue hint:
     "You've hurt his trust. Things between you shift."
```

#### 🟢 **PROBLEM: Branch Convergence Conflict**
Two branches merge with conflicting variable states.

```
BRANCH A at NODE-020:
  state_victor = escaped
  relationship_marcus = 80
  city_status = under_siege

BRANCH B at NODE-020:
  state_victor = captured
  relationship_marcus = 35
  city_status = under_siege

Merge NODE-025:
  Story expects: "Marcus brings you news about Victor"
  
If state_victor=escaped: "Victor sent word from safety"
If state_victor=captured: "Victor is prisoner; militia controls info"

These are DIFFERENT continuations!
Branches cannot safely merge here (story would fork again anyway)

Status: 🟢 UNNECESSARY MERGE
        (Looks like merge point, but immediately branches again)

Fix: Either
  1. Keep branches separate (have NODE-025A and NODE-025B)
  2. Add earlier merge point (before relationship diverges)
  3. Add reconciliation logic: accept both variable states, branch appropriately
```

### 4. **Analyze Convergence Points**

Map where branches merge:

```
Convergence Analysis:

NODE-015 (choice point): BRANCH A / BRANCH B diverge
  A: Help Victor
  B: Betray Victor
  
NODE-020: Both branches have different content
  A: Escape sequence
  B: Capture sequence
  STATUS: ✅ Branches running parallel

NODE-025: Branches attempt to merge
  A: state_victor = escaped, city = locked_down, relationship = 80
  B: state_victor = captured, city = locked_down, relationship = 30
  
  Merged content: "City is locked down"
  
  Can branches merge?
    ✅ YES: city_status is compatible (both locked_down)
    ❌ NO: state_victor differs → story would fork again
  
  Assessment: Branches can share intro (city status)
              Must split for Victor handling

---

NODE-030: Another merge attempt
  Convergence status:
    A: status = resolved_peacefully (Victor escaped)
    B: status = resolved_sadly (Victor captured)
    
  Merged content: Final scenes
  
  Can branches merge?
    ✅ YES if ending can handle both outcomes
    ❌ NO if ending specifically refers to Victor's fate
  
  Recommendation: Have two ending variants (variant A vs variant B)
                  OR have single ending that acknowledges both possibilities
```

### 5. **Generate State Map Report**

Create `specs/statemap-audit.md`:

```markdown
## Variable State Map Audit

**Game**: [NAME]
**Date**: [ISO]

### State Space Overview

| Variable | Type | Reachable Values | Theoretical | Used |
|----------|------|------------------|------------|------|
| state_victor | Enum | freed, escaped, captured | Same | ✅ |
| relationship_marcus | Int | 35, 50, 65, 80, 90 | 0–100 | ⚠️ Bloated |
| city_status | Enum | safe, under_siege, locked_down | 4 total | ✅ |
| player_alliance | Enum | none, weak, strong | Same | ✅ |

Total reachable states: ~60
Total theoretical: 303
Coverage: 20% (bloated design or 80% dead code)

### Branch State Trajectories

**BRANCH A** (Help Victor):
  NODE-020: freed / 80 / under_siege
  NODE-025: escaped / 80 / locked_down
  ENDING: escaped / 90 / locked_down
  Status: ✅ Linear progression

**BRANCH B** (Betray Victor):
  NODE-020: freed / 35 / under_siege
  NODE-025: captured / 30 / locked_down
  ENDING: captured / 25 / locked_down
  Status: ✅ Linear progression

### State Problems

**🔴 Unreachable States** (2):
- relationship_marcus=75: No branch reaches this value
  Fix: Add optional choice to fine-tune relationship
  
- alliance_status=weak + relationship > 70: Combination never occurs
  Fix: Decide if this should be reachable

**🟡 Dead-End States** (0):
- None found

**🔵 Untracked Mutations** (1):
- NODE-015: relationship_marcus drops 15 points with no explicit code
  Fix: Add "relationship_marcus = 65" line with explanation

**🟢 Convergence Issues** (1):
- NODE-025 merge: Branches have incompatible state_victor
  Fix: Keep branches separate or add conditional logic

### Recommendations

**Priority 1**:
1. Declare relationship_marcus=75 unreachable (remove from design), OR add path to reach it
2. Add explicit relationship change at NODE-015
3. Split NODE-025 or add conditional handling for state_victor difference

**Priority 2**:
1. Review theoretical vs reachable state ratio (20% seems low)
2. Verify all variable definitions are actively used

**Overall Assessment**: State space is coherent but has 4 fixable issues
```

### 6. **Show Graph** (optional with --show-graph)

ASCII state transition graph:

```
STATE TRANSITIONS: relationship_marcus

50 [initial]
│
├─ NODE-010 (+15)
│  └─ 65 [moderate]
│     │
│     ├─ NODE-015 (no change)
│     │  └─ 65 [stays]
│     │     │
│     │     ├─ NODE-020 [+15, help]
│     │     │  └─ 80 [strong]
│     │     │
│     │     └─ NODE-020 [-30, betray]
│     │        └─ 35 [broken]
│     │
│     └─ NODE-025
│        ├─ 80 [+10] → 90 [ending A]
│        └─ 35 [-5] → 30 [ending B]

State space:
  • 50 (initial) → always present
  • 65 (moderate) → after NODE-010, before choice
  • 80/35 (after choice, divergent)
  • 90/30 (endings, divergent)

Coverage: 5 distinct values reachable
Unused: 51–64, 66–79, 81–89, 91–100 (defined but unreachable)
```

### 7. **Show Paths** (optional with --show-paths)

Display full variable state for each branch:

```
BRANCH A STATE PROGRESSION

NODE-005:  state_victor=freed, relationship=50, city=safe, alliance=none
NODE-010:  state_victor=freed, relationship=65, city=safe, alliance=none  [+15]
NODE-015:  state_victor=freed, relationship=65, city=under_siege, alliance=weak  [city changed]
NODE-020:  state_victor=freed, relationship=80, city=under_siege, alliance=weak  [+15]
NODE-025:  state_victor=escaped, relationship=80, city=locked_down, alliance=weak  [victor escaped, city upgraded]
ENDING:    state_victor=escaped, relationship=90, city=locked_down, alliance=strong  [+10, +alliance]

Changes per node:
  NODE-005 → NODE-010: relationship +15
  NODE-010 → NODE-015: city upgrade, alliance initiated
  NODE-015 → NODE-020: relationship +15
  NODE-020 → NODE-025: victor escape, city upgrade
  NODE-025 → ENDING: relationship +10, alliance strengthened
```

### 8. **Check Convergence** (optional with --check-convergence)

Verify branch merge points:

```
MERGE POINT: NODE-025

Branch A state:
  state_victor: escaped
  relationship: 80
  city_status: locked_down
  alliance: weak

Branch B state:
  state_victor: captured
  relationship: 35
  city_status: locked_down
  alliance: weak

Compatible fields:
  ✅ city_status: both locked_down (MERGE OK)
  ✅ alliance: both weak (MERGE OK)

Incompatible fields:
  ❌ state_victor: escaped vs captured (CANNOT MERGE)
  ❌ relationship: 80 vs 35 (CANNOT MERGE)

Merge verdict: ❌ CANNOT SAFELY MERGE
              Branches should remain separate or use conditional logic

Recommendation: Have NODE-025A (for escaped state) and NODE-025B (for captured state)
                OR add check at NODE-025: if state_victor=escaped → NODE-025A else NODE-025B
```

### 9. **Report**

Output `statemap-audit.md` with:
- State space overview (variables, reachable vs theoretical)
- Branch state trajectories per node
- Problem list (unreachable states, dead ends, untracked mutations, convergence conflicts)
- Convergence point analysis
- If `--show-graph`: ASCII state transition visualization
- If `--show-paths`: Full state for each branch per node
- If `--check-convergence`: Merge point compatibility analysis

---

## Important Notes

**State Space Can Be Large**: A game with 10 binary flags alone has 2^10 = 1,024 theoretical states. Most will be unreachable by design. This is normal; don't aim for 100% coverage.

**Reachability Is Design**: Mark intended unreachable states explicitly in variables.md. "This state is possible by definition but not part of our design" is fine; accidentally unreachable states are problems.

**Convergence Is Optional**: Branches don't need to merge if they have different states. Running parallel branches is valid design. Merge only where story/design supports it.

**Mutation Must Be Explicit**: Every variable change should be visible in node prose or code. "Silent" variable changes are debugging nightmares. Use explicit assignment comments.

**Dead Ends Are Design Failures**: If a reachable state leads to a node with incompatible requirements, fix it. Either make the state unreachable, or add an alternate path from that state.

