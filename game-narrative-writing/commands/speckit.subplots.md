---
description: Subplot resolution tracker — verify all subplots are started AND resolved in each branch. Detects dangling plot threads and incomplete arcs across different playthroughs.
handoffs:
  - label: Check Continuity
    agent: speckit.continuity
    prompt: After verifying subplot resolution, check cross-node continuity.
    send: true
  - label: Revise Subplots
    agent: speckit.revise
    prompt: Some subplots are unresolved. Please add resolution nodes.
    send: true
---

# speckit.subplots

Subplot resolution tracker — verify all subplots are **started, developed, and resolved** (not abandoned) across all branches and endings. Ensures no playthrough feels unfinished due to dropped threads.

## Subplot Principle

A **subplot** is a secondary story arc (distinct from main plot). 

**Well-executed subplot**:
- ✅ Introduced clearly (player understands a thread exists)
- ✅ Developed (plot progresses, stakes raised)
- ✅ Resolved (thread tied off, tension released)
- ✅ Consistent across branches (same subplot handled similarly in all paths)

**Failed subplot**:
- ❌ Started but never mentioned again (dangling thread)
- ❌ Resolved prematurely (anticlimactic)
- ❌ Resolved differently per branch (inconsistent handling)
- ❌ Only resolved in some branches (abandoned in others)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit all subplots across all branches
- Subplot ID (e.g., `SUB-001`) — audit one subplot only
- `--branch [BRANCH_ID]` — audit subplots in one story branch only
- `--unresolved-only` — show only subplots with missing resolutions

Optional flags:
- `--strict` — flag unresolved subplots in any branch as failures (not warnings)
- `--show-threads` — display introduction → development → resolution for each subplot
- `--consistency-check` — verify subplot handling is consistent across branches

## Pre-Execution Checks

1. Load `specs/subplots-template.md` if present (or create from spec.md secondary arcs)
2. Confirm `specs/plan.md` exists with branch structure
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Parse plan.md to identify branch divergence points
5. Map which nodes are reachable per branch

## Execution Steps

### 1. **Define Subplots**

Subplots come from `specs/subplots-template.md` or extracted from spec.md secondary story arcs. Each subplot has:
- **SUB-ID**: Unique identifier
- **Name**: Subplot title (e.g., "The Heist with Victor")
- **Start node**: Where subplot is introduced
- **Key scenes**: Development beats
- **Resolution nodes**: Where subplot concludes (may vary per branch)

**Example subplot definition**:
```
SUB-001: Victor's Redemption
  Introduction: NODE-005 (Victor asks for help escaping mob)
  Development:
    • NODE-010: Victor reveals his daughter
    • NODE-015: Mob catches up; must choose: help Victor or flee
  Resolution:
    • Path A (help): NODE-020 (Victor escapes; gratitude scene)
    • Path B (flee): NODE-022 (Victor captured; regret later)
```

### 2. **Trace Subplots Through Branches**

For each subplot, trace through ALL possible story branches:

**Branch A (help Victor)**:
```
NODE-005 → SUB-001 STARTS
  victor_status = "needs_help"
  
NODE-010 → SUB-001 DEVELOPS
  player_knows: victor_daughter = "Lily"
  
NODE-015 → SUB-001 CHOICE
  Choice: "Help Victor" → victor_status = "escaped"
  
NODE-020 → SUB-001 RESOLVES
  "Victor embraces you. 'Lily will never forget this.'"
  ✅ SUBPLOT COMPLETE
```

**Branch B (flee Victor)**:
```
NODE-005 → SUB-001 STARTS
  victor_status = "needs_help"
  
NODE-010 → SUB-001 DEVELOPS
  player_knows: victor_daughter = "Lily"
  
NODE-015 → SUB-001 CHOICE
  Choice: "Flee" → victor_status = "abandoned"
  
NODE-022 → SUB-001 RESOLVED DIFFERENTLY
  "Later, you hear Victor was caught. Lily was placed in foster care."
  ✅ SUBPLOT COMPLETE (different variant)
```

**Branch C (never meet Victor)**:
```
NODE-005 → SUB-001 SKIPPED (this branch doesn't encounter Victor)
  
NODE-003 → ALTERNATE PATH (no Victor)

NODE-025 → ENDING REACHED
  SUB-001 never mentioned
  ❌ SUBPLOT ABANDONED
  (This branch has no Victor arc at all)
```

### 3. **Detect Subplot Violations**

#### 🔴 **VIOLATION: Dangling Thread**
Subplot is introduced but never resolved in one or more branches.

```
SUB-002: The Prophecy

Branch A (help Victor):
  NODE-005: Prophet: "You will face three trials"
  NODE-010: First trial appears
  NODE-015: Second trial appears
  NODE-020: ENDING REACHED
  ❌ Third trial never appears; prophecy unresolved

Branch B (flee Victor):
  NODE-005: Prophet: "You will face three trials"
  NODE-010: First trial appears
  NODE-015: Second trial appears
  NODE-022: Third trial appears; prophecy fulfilled
  ✅ Resolved
```

**Report**:
```
SUB-002: The Prophecy
  Branch A: Introduced ✅ → Partial development ✅ → NO RESOLUTION ❌
  Branch B: Introduced ✅ → Full development ✅ → Resolved ✅
  
  Status: ⚠️  INCONSISTENT
  Impact: Branch A playthrough feels unfinished
  Fix: Either add 3rd trial to Branch A, or remove from prophecy
```

#### 🟡 **VIOLATION: Premature Resolution**
Subplot is resolved before proper development.

```
SUB-003: Love Triangle
  NODE-005: Introduce Sera and Marcus as romantic interests
  NODE-010: Hint at tension between them
  NODE-012: ENDING REACHED before love choice is forced
  
  ❌ Subplot introduced but never developed
  Fix: Add at least one "must choose between them" moment before ending
```

#### 🟠 **VIOLATION: Inconsistent Resolution**
Subplot is resolved differently in different branches for no narrative reason.

```
SUB-004: The Artifact

Branch A:
  NODE-005-015: Artifact is important MacGuffin
  NODE-020: Player destroys artifact; magical chaos ensues; chaos averted through effort
  ✅ Consistent with build-up

Branch B:
  NODE-005-015: Artifact is important MacGuffin
  NODE-022: Artifact mentioned once, then forgotten
  NODE-025: Ending reached, artifact never mentioned again
  ❌ Subplot dropped for no reason

Status: ⚠️  INCONSISTENT
Impact: Same subplot handled completely differently despite similar setup
Fix: Either include artifact resolution in Branch B, or explain why it's omitted
```

#### ✅ **VALID: Consistent Multi-Variant**
Subplot resolved in all branches, but with meaningful variations.

```
SUB-005: Trust with Marcus

Branch A (help Marcus):
  NODE-010: Marcus confides secret
  NODE-015: Must prove trust via sacrifice
  NODE-020: "We did it together. I'll never forget this."
  ✅ Resolved with partnership
  
Branch B (betray Marcus):
  NODE-010: Marcus confides secret
  NODE-015: Can exploit secret for gain
  NODE-022: "You have what you wanted. Marcus is ruined."
  ✅ Resolved with betrayal

Branch C (neutral):
  NODE-010: Marcus hints at secret
  NODE-018: Subplot fades; Marcus reassigned
  NODE-025: Brief mention: "Marcus moved on. We never got close."
  ✅ Resolved with distance (intentional ambivalence)

All variants: Subplot initiated, developed, and concluded
Variations: Meaningful based on player choice
Status: ✅ EXCELLENT handling
```

### 4. **Generate Subplot Resolution Report**

Create `specs/subplot-audit.md`:

```markdown
## Subplot Resolution Audit

**Game**: [NAME]
**Date**: [ISO]

### Subplot Status Table

| SUB-ID | Name | Start | Branch A | Branch B | Branch C | Status |
|--------|------|-------|----------|----------|----------|--------|
| SUB-001 | Victor | NODE-005 | ✅ Resolved | ✅ Resolved | N/A | ✅ PASS |
| SUB-002 | Prophecy | NODE-005 | ⚠️ Unresolved | ✅ Resolved | ✅ Resolved | ⚠️ INCONSISTENT |
| SUB-003 | Love Triangle | NODE-005 | ⚠️ Premature | ✅ Developed | ✅ Developed | ⚠️ INCONSISTENT |
| SUB-004 | Artifact | NODE-005 | ✅ Resolved | ❌ Abandoned | ✅ Resolved | ❌ ABANDONED |

### Violations

**🔴 Abandoned in Branch(es)** (3):
- SUB-002 (Prophecy): Unresolved in Branch A
- SUB-004 (Artifact): Dropped in Branch B entirely
- SUB-007 (Sister's Fate): Not mentioned in Branch C

**🟡 Inconsistent Resolution** (2):
- SUB-003 (Love Triangle): Premature in Branch A, full arc in Branches B/C
- SUB-006 (Rebellion): Different outcomes with no linking narrative

**✅ Consistent & Complete** (3):
- SUB-001 (Victor): Different resolutions per choice, both satisfying
- SUB-005 (Trust with Marcus): Varied per player agency, all conclusive
- SUB-008 (The Mystery): Resolved in all branches

### Recommendations

**Priority 1 (Fix before release)**:
1. SUB-002 (Prophecy): Add 3rd trial to Branch A OR remove from prophecy
2. SUB-004 (Artifact): Either include artifact payoff in Branch B OR justify omission
3. SUB-007 (Sister's Fate): Ensure at least brief mention in Branch C

**Priority 2 (Polish)**:
1. SUB-003 (Love Triangle): Add at least one development beat to Branch A before ending
2. SUB-006 (Rebellion): Add transitional dialogue explaining different outcomes

**Priority 3 (Enhancement)**:
1. Consider expanding SUB-008 to add Branch-specific variant details
```

### 5. **Show Threads** (optional with --show-threads)

For each subplot, display full intro → development → resolution path:

```
SUB-001: Victor's Redemption

BRANCH A (Help Victor):
  NODE-005 [INTRO]
    "A man approaches. His hands shake. 'Please, you have to help me.'"
    → victor_status = "needs_help"
  
  NODE-010 [DEVELOP]
    "Victor shows you a photograph. 'This is Lily. My daughter.'"
    → player_knows["victor_daughter"] = true
  
  NODE-015 [CHOICE POINT]
    "The mob's car turns the corner. Victor looks at you.
     What do you do?"
    Choice A: Help Victor
    Choice B: Run
  
  → IF Choice A:
    NODE-020 [RESOLVE]
    "Victor embraces you. 'Lily will never forget this.'"
    → victor_status = "escaped"
    → relationship["victor"] += 3
    ✅ COMPLETE
  
  → IF Choice B:
    NODE-022 [RESOLVE]
    "Later, you hear Victor was captured.
     His daughter was placed in state care."
    → victor_status = "captured"
    → relationship["victor"] -= 2
    → reputation -= 1
    ✅ COMPLETE (different variant)
```

### 6. **Consistency Check** (optional with --consistency-check)

Compare how same subplot is handled across branches:

```
SUB-002: The Prophecy

Branch A vs Branch B:
  Introduction:
    Both: Prophet appears at NODE-005 ✅ (consistent)
  Development:
    Branch A: 2 of 3 trials ⚠️
    Branch B: All 3 trials ✅
    Consistency: ❌ UNEVEN
  Resolution:
    Branch A: None ❌
    Branch B: Full prophecy fulfilled ✅
    Consistency: ❌ INCONSISTENT
  
  Verdict: Subplots handled inconsistently
  Fix: Either add trial 3 to Branch A OR reduce trial count to 2
```

### 7. **Report**

Output `subplot-audit.md` with:
- Subplot status table (all branches checked)
- Violation list (abandoned, inconsistent, premature)
- Specific recommendations for each issue
- If `--show-threads`: Full intro → dev → resolution paths
- If `--consistency-check`: Branch-by-branch comparison table

---

## Important Notes

**Branch-Specific Variants Are OK**: Same subplot can resolve differently per branch if the variation is **intentional and meaningful**. A subplot can end in triumph in one branch and tragedy in another—that's good interactive narrative design.

**"No subplot" is OK Too**: A subplot can be skipped entirely in a branch if the branch diverges before it's introduced. But if a subplot is *introduced*, it must be *resolved* (even if resolution is "this branch doesn't pursue it").

**Consistency Standard**: All resolved subplots should resolve *approximately* at the same story point. If one subplot resolves in NODE-10 in one branch and NODE-30 in another, flag it as pacing inconsistency (use `speckit.pacing` for details).

**Dangling Threads**: In moderation, a minor unresolved thread can add realism ("not everything wraps up perfectly"). But systematically unresolved subplots across multiple branches = incomplete narrative. Flag anything that feels like unfinished business.

