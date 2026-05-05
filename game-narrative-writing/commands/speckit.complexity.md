---
description: Branch complexity analyzer — detect exponential growth, warn on unsustainable branching patterns, estimate maintenance effort per branch depth.
handoffs:
  - label: Check Replayability
    agent: speckit.replayability
    prompt: After analyzing branch complexity, measure unique content per playthrough.
    send: true
  - label: Review Planning
    agent: speckit.plan
    prompt: Branch complexity is high. Consider consolidating or scoping.
    send: true
---

# speckit.complexity

Branch complexity analyzer — detect **exponential branch growth**, warn on unsustainable branching patterns, estimate maintenance effort. Helps prevent "branching hell" (250+ nodes with 2^N combinations).

## Complexity Principle

**Sustainable branching** = Each choice is meaningful; maintenance effort scales linearly or sub-exponentially.

**Unsustainable branching includes**:
- ❌ Every node has 3+ branches (exponential explosion)
- ❌ Deep nesting (15+ levels of branching)
- ❌ Reconvergence-free design (all branches stay separate)
- ❌ Poor branch tracking (can't maintain code quality)

**Valid complexity includes**:
- ✅ Early choices create major branches; later consolidate
- ✅ Linear main path with occasional 2-branch splits
- ✅ Deep complexity in limited areas (side quests), linear elsewhere
- ✅ Deliberate branching: each branch has distinct content/mechanics

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze overall branch complexity
- `--depth` — focus on branch depth (longest path length)
- `--breadth` — focus on branch breadth (# parallel branches at each point)
- `--maintenance` — estimate work per branch variant

Optional flags:
- `--strict` — flag any node with >2 branches as risky
- `--show-tree` — ASCII tree of branch structure
- `--convergence-map` — show where branches merge
- `--estimate-nodes` — calculate total node count needed for all branches

## Pre-Execution Checks

1. Load `specs/plan.md`: Complete branch structure
2. Load all `draft/[ENGINE]/NODE-*.md` files to count existing nodes
3. Map branch divergence points and convergence points
4. Estimate unwritten nodes per branch
5. Calculate maintenance metrics

## Execution Steps

### 1. **Map Branch Structure**

From plan.md, create branch topology:

```
Branch tree structure (ASCII simplified):

NODE-001 [START]
│
├─ NODE-005 [INTRO]
│  │
│  ├─ NODE-010 [Help Victor?]
│  │  ├─ YES → NODE-015 [BRANCH A: Redemption]
│  │  │  ├─ NODE-020
│  │  │  └─ NODE-025 [END A]
│  │  │
│  │  └─ NO → NODE-016 [BRANCH B: Betrayal]
│  │     ├─ NODE-021
│  │     └─ NODE-026 [END B]
│  │
│  └─ NODE-011 [Flee?]
│     └─ NODE-017 [BRANCH C: Escape]
│        ├─ NODE-022
│        └─ NODE-027 [END C]

Topology metrics:
  • Depth: 4 levels (START → choice → content → ending)
  • Breadth at NODE-010: 3 branches (high)
  • Total branches: 3 distinct endings
  • Convergence: Branches don't reconverge (stay separate)
```

### 2. **Analyze Branch Depth**

Measure the longest path:

```
Longest path (critical path depth):
  NODE-001 → NODE-005 → NODE-010 → NODE-015 → NODE-020 → NODE-025
  Depth: 6 nodes

Branch A depth: 6 nodes
Branch B depth: 6 nodes
Branch C depth: 6 nodes

Max depth: 6 (moderate)

Complexity assessment:
  • 1–3: Minimal branching (linear story)
  • 4–8: Moderate branching (sustainable)
  • 9–15: Complex branching (intensive)
  • 16+: Exponential (risky, unsustainable)

Status: ✅ MODERATE (depth is sustainable)
```

### 3. **Analyze Branch Breadth**

Measure branching factor at each point:

```
Branching factor (# of branches at each choice point):

NODE-010 [choice point]: 3 branches (Help / Betray / Flee)
  Branching factor: 3
  
NODE-015 [sub-choice within branch A]: 2 branches (Violent / Stealth)
  Branching factor: 2
  
NODE-020 [convergence check]: Do all branches arrive here?
  Branch A: arrives
  Branch B: arrives
  Branch C: arrives
  Convergence: YES
  
Analysis:
  Total branches from NODE-010: 3
  Sub-branches at NODE-015 (A only): 2
  Total possible combinations at NODE-020: 3 × 1 × 2 = 6 combinations

But wait:
  Branch B and C have no NODE-015 sub-choice
  So actual combinations:
    • Branch A: 1 × 2 = 2 combinations (main × sub-choice)
    • Branch B: 1 combination (no sub-choice)
    • Branch C: 1 combination (no sub-choice)
    • Total: 4 combinations (not 6)

Status: ✅ MANAGEABLE (branching is localized to Branch A)
```

### 4. **Calculate Total Node Requirements**

Estimate nodes needed for all branches:

```
Node accounting:

Shared nodes (all branches):
  NODE-001 through NODE-010: 10 nodes × 1 = 10 nodes

Branch A (Help Victor):
  NODE-015 → NODE-020 → NODE-025: 3 nodes
  Sub-choice at NODE-015: × 2 variants
  Total Branch A: 6 nodes (3 nodes × 2 variants)

Branch B (Betray Victor):
  NODE-016 → NODE-021 → NODE-026: 3 nodes × 1 = 3 nodes

Branch C (Flee):
  NODE-017 → NODE-022 → NODE-027: 3 nodes × 1 = 3 nodes

Total: 10 + 6 + 3 + 3 = 22 nodes

Breakdown:
  • Shared: 45% (10/22)
  • Branch-specific: 55% (12/22)
  
Efficiency: ✅ Reasonable ratio (some shared content reduces duplication)
```

### 5. **Detect Complexity Problems**

#### 🔴 **PROBLEM: Exponential Explosion**
Every node spawns multiple branches; combinations grow uncontrollably.

```
Hypothetical design:

NODE-001 [choice point]: 3 branches
NODE-010 [choice point in each branch]: 3 branches × 3 options = 9 paths
NODE-015 [choice point in each path]: 9 paths × 3 options = 27 paths
NODE-020 [choice point in each path]: 27 paths × 3 options = 81 paths

Exponential formula: 3^N where N=4 choices = 81 paths

At 81 paths with 5 unique nodes per path = 405 nodes needed
At average 2 hours per node = 810 hours of writing

Status: 🔴 EXPONENTIAL EXPLOSION
        This is "branching hell"

Red flags:
  • >100 possible paths
  • >200 nodes estimated
  • Writer spending >50% of time on minor branch variations
  
Fix options:
  1. Reduce branching factor (use binary choices, not ternary)
  2. Add convergence points (branches merge after divergence)
  3. Scope branching to specific areas (main story linear, side quests branchy)
  4. Use variable flags instead of node branching (same state, different prose)
```

#### 🟡 **PROBLEM: Uncontrolled Depth**
Branches continue diverging without convergence; maintenance becomes impossible.

```
Design:

NODE-001 → NODE-005 → NODE-010 → NODE-015 → NODE-020 → NODE-025
  (each node diverges into 2 branches, never reconverges)

Paths: 2^6 = 64 possible paths

At 64 paths:
  • Impossible to test all variations
  • Changes to shared content affects all 64 paths
  • Bug in NODE-010 might not manifest until NODE-025
  
Status: 🟡 MAINTENANCE NIGHTMARE
        Not exponential in scope, but high in dependency risk

Red flags:
  • Depth >8 without convergence
  • No "sync points" where branches meet
  • Test matrix is >32 combinations

Fix options:
  1. Add convergence after each divergence (e.g., NODE-010 diverges, NODE-012 reconverges)
  2. Use convergence at story beats (e.g., "all branches meet before act 2")
  3. Limit depth to <5 without reconvergence
```

#### 🟠 **PROBLEM: Unnecessary Parallelism**
Multiple branches do the same thing; duplication instead of branching.

```
Branch A (NODE-010):
  Prose: "You hide behind the boxes."
  Next: NODE-015
  
Branch B (NODE-010):
  Prose: "You duck behind the wall."
  Next: NODE-015
  
Branch C (NODE-010):
  Prose: "You crouch under the table."
  Next: NODE-015
  
All three branches:
  • Accomplish same goal (hide)
  • Lead to same node (NODE-015)
  • Have same outcome (NPC doesn't see you)
  
Status: 🟠 UNNECESSARY BRANCHING
        These are cosmetic flavor variants, not meaningful choices

Problem: Uses 3 node slots for flavor text
         Increases maintenance (changes to NODE-015 need 3 paths updated)

Fix options:
  1. Combine into single node with multiple hide descriptions
  2. Keep as branches only if each has meaningfully different consequences
  3. Use conditional prose (if player_choice=hide_boxes, show that text)
```

#### 💨 **PROBLEM: Orphaned Branches**
Branch has no convergence back to main story; stranded content.

```
NODE-010 [choice point]: Explore / Don't Explore

Explore branch:
  NODE-015 [side quest start]
  NODE-020 [side quest middle]
  NODE-025 [side quest complete]
  NODE-030: ??? (where do players go after quest?)
           No connection back to main story
           Side quest ends in vacuum
  
Don't Explore branch:
  NODE-012 [main story continues]
  NODE-017 [main story]
  NODE-022 [reconverges with Explore branch]
  
Status: 💨 ORPHANED BRANCH
        Explore path leads to NODE-030 (dead end)
        No way back to main story

Problem: Players get stuck after completing side quest
         Design was incomplete at NODE-025

Fix: Either
  1. Merge NODE-030 back to main story (e.g., NODE-030 → NODE-022)
  2. Make NODE-025 ending final (side quest completes game)
  3. Add explicit "return to town" choice at NODE-025
```

### 6. **Estimate Maintenance Effort**

Calculate work per branch variant:

```
Maintenance effort formula:
  E = S + (B × V × C)
  
  S = Shared node work (write once, maintain everywhere)
  B = Branch-specific node work
  V = Variant work (conditional prose, state changes)
  C = Complexity multiplier (testing, debugging)

Example game:

S (shared): 10 nodes × 2 hrs = 20 hrs (written once, impacts all branches)
B (branch-specific): 12 nodes × 2 hrs = 24 hrs
V (variant prose): 4 variants × 0.5 hrs = 2 hrs
C (complexity): 3 branches, 6 choice points = 18 test combinations

Initial effort: 20 + 24 + 2 = 46 hours

Ongoing maintenance cost (per 1-hour edit in shared content):
  • 1 hour edit in shared node = impacts all 3 branches = 3x review time
  • 1 hour edit in branch-specific = 1 hour per branch = 3 hours
  • Regression testing: 18 combinations must be tested = 18 hours

Total maintenance multiplier: 3x–5x per edit in shared content

Risk assessment:
  • Low risk: <5 branches, depth <5, >50% shared content
  • Medium risk: 5–10 branches, depth 5–8, 30–50% shared content
  • High risk: >10 branches, depth >8, <30% shared content
  
This game: 3 branches, depth 6, 45% shared = MEDIUM RISK
```

### 7. **Generate Complexity Audit Report**

Create `specs/complexity-audit.md`:

```markdown
## Branch Complexity Audit

**Game**: [NAME]
**Date**: [ISO]

### Complexity Metrics

| Metric | Value | Limit | Status |
|--------|-------|-------|--------|
| Max depth | 6 | 8 | ✅ OK |
| Max breadth | 3 | 5 | ✅ OK |
| Total branches | 3 | 10 | ✅ OK |
| Possible paths | 4 | 50 | ✅ OK |
| Total nodes | 22 | 100 | ✅ OK |
| Shared % | 45% | >30% | ✅ OK |

### Branch Structure

```
Shared intro (10 nodes)
├─ Branch A: Help Victor (6 nodes, 2 variants)
├─ Branch B: Betray Victor (3 nodes)
└─ Branch C: Flee (3 nodes)
```

Depth: 6 levels
Breadth: 3 parallel paths at main choice
Branching factor: 3 at NODE-010, 2 at NODE-015 (A only)

### Maintenance Effort

- Initial development: ~46 hours
- Per 1-hour shared edit: ~3–5 hours ongoing (testing all branches)
- Branch testing: 18 combinations to verify
- Risk level: MEDIUM

### Sustainability Assessment

**Current design**: ✅ SUSTAINABLE
- Depth is manageable (6 levels)
- Branching is controlled (3 at main point, 2 sub-branches)
- Convergence exists (no orphaned paths)
- Shared content is >40% (reduces duplication)

**Growth warning**: If you add more than 5 more choice points,
                    or deepen beyond 10 levels,
                    or increase branches to 6+, consider consolidating.

### Recommendations

**Current**: No immediate changes needed

**Future expansion**:
1. If adding side quests, keep them shallow (<3 levels) and reconverge
2. If adding sub-choices, limit to 1–2 per main branch
3. Target <100 total nodes to keep testing manageable
4. Maintain >40% shared content to reduce duplication

**Optimization opportunities**:
- NODE-010 choices could be condensed if variants don't differ substantively
- Consider variable flags for flavor choices instead of node duplication
```

### 8. **Show Tree** (optional with --show-tree)

ASCII tree of complete branch structure:

```
BRANCH TREE

START [shared]
├─ INTRO [shared, 10 nodes]
│
└─ NODE-010 CHOICE: Help / Betray / Flee
   │
   ├─ BRANCH A: Help Victor
   │  ├─ NODE-015 SUB-CHOICE: Violent / Stealth
   │  │  ├─ VARIANT A1: Violent approach
   │  │  │  └─ NODE-020 → NODE-025 [END A1]
   │  │  │
   │  │  └─ VARIANT A2: Stealth approach
   │  │     └─ NODE-020 → NODE-025 [END A2]
   │  │
   │  └─ NOTE: Both A1 and A2 converge at NODE-020
   │
   ├─ BRANCH B: Betray Victor
   │  └─ NODE-016 → NODE-021 → NODE-026 [END B]
   │
   └─ BRANCH C: Flee
      └─ NODE-017 → NODE-022 → NODE-027 [END C]

Convergence points: NODE-020 (A variants merge)
Divergence points: NODE-010 (3-way split), NODE-015 (2-way A only)
Dead-ends: NODE-025 (A1), NODE-025 (A2), NODE-026 (B), NODE-027 (C)
```

### 9. **Convergence Map** (optional with --convergence-map)

Show where branches merge:

```
CONVERGENCE POINTS

NODE-010 [divergence]:
  ├─ Branch A (Help)
  ├─ Branch B (Betray)
  └─ Branch C (Flee)
  
NODE-015 [sub-divergence in A only]:
  ├─ A1 (Violent)
  └─ A2 (Stealth)

NODE-020 [convergence]:
  Branches that merge here:
    ✅ A1 arrives (from NODE-025 variant A1)
    ✅ A2 arrives (from NODE-025 variant A2)
  
  Branches that DON'T merge here:
    ❌ B continues separately
    ❌ C continues separately
  
  Convergence quality: PARTIAL (A variants merge, B and C stay separate)

Assessment: B and C don't reconverge with A
            This is intentional (different ending paths)
            Acceptable design
```

### 10. **Report**

Output `complexity-audit.md` with:
- Complexity metrics (depth, breadth, total nodes, paths)
- Branch structure summary
- Maintenance effort estimate
- Sustainability assessment (sustainable / risky / critical)
- If `--show-tree`: ASCII branch tree
- If `--convergence-map`: Where branches merge/diverge
- If `--estimate-nodes`: Projected node count for full implementation

---

## Important Notes

**Branching Is Not Inherently Bad**: Games like *Disco Elysium* and *Outer Wilds* have hundreds of nodes with complex branching. The issue is whether you can maintain it.

**Test Matrix Grows Exponentially**: 4 binary choices = 16 paths to test. 8 binary choices = 256 paths. Even moderate branching requires systematic testing.

**Convergence Is Your Friend**: Branches that reconverge let you reduce exponential growth. "All paths lead to this scene" is a powerful design pattern.

**Linear With Side Branches**: Consider a linear main story with optional side quests. Main path is manageable; side content is branchy but isolated.

**Scope Branching Deliberately**: Different games support different branching levels:
- Visual novels: Can handle 100+ nodes, high branching
- Parser IF: Often keep to <50 nodes, moderate branching
- Choice-based IF: Usually 20–80 nodes, controlled branching
- Twine games: Highly variable; depends on target

Know your scope before designing branching.

