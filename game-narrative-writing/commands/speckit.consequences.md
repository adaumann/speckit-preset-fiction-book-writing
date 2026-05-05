---
description: Choice consequence mapper — visualize how each choice branches story into different outcomes. Track consequences across all branches, detect orphaned choice branches, map consequence chains.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: After mapping consequences, verify choices actually have meaningful consequences.
    send: true
  - label: Revise Consequences
    agent: speckit.revise
    prompt: Some choice consequences are unclear. Please strengthen outcome differentiation.
    send: true
---

# speckit.consequences

Choice consequence mapper — visualize **how each choice branches into different outcomes**. Tracks consequences across all branches, detects orphaned choices, maps consequence chains (choice → intermediate effect → ending state).

## Consequence Principle

**Clear consequences** = Each choice visibly affects story outcome; player can predict/understand result.

**Unclear consequences include**:
- ❌ Choice made, but outcome is identical to other choices
- ❌ Consequence appears late (5+ nodes after choice)
- ❌ Chain of consequences so complex player can't trace it
- ❌ Choice branch leads to dead end (orphaned consequence)
- ❌ Consequence contradicts prior setup (feels arbitrary)

**Valid consequences include**:
- ✅ Immediate effect (visible within 1–2 nodes)
- ✅ Traced chain (choice → NODE-1 change → NODE-3 payoff)
- ✅ Multiple outcome paths (same choice, different consequences per branch)
- ✅ Cumulative consequences (compound across multiple choices)
- ✅ Latent consequences (delayed but foreshadowed)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — map all choice consequences across all branches
- Choice ID (e.g., `CH-001`) — trace one choice's consequences
- `--choice-point [NODE_ID]` — analyze all choices at a specific node
- `--branch [BRANCH_ID]` — trace consequences in one branch only

Optional flags:
- `--strict` — flag any consequence appearing >3 nodes after choice
- `--orphaned-only` — show only dead-end branches (no payoff)
- `--show-chains` — display multi-step consequence chains
- `--consequence-only` — ignore neutral branches (show only meaningful differences)

## Pre-Execution Checks

1. Load `specs/plan.md`: Branch structure, choice points
2. Load `specs/variables.md`: Variables affected by choices
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Parse for choice syntax (Ink `*[]`, SugarCube `[[]]`, etc.)
5. Extract variable mutations per branch
6. Identify choice points and their outcomes

## Execution Steps

### 1. **Map Choice Points**

Identify all player choices and their branches:

```
CHOICE POINTS:

CH-001: NODE-010 "Help or Betray Victor?"
  Option A: "Help Victor escape"    → NODE-015 [Branch A]
  Option B: "Betray Victor"         → NODE-016 [Branch B]
  Option C: "Flee without helping"  → NODE-017 [Branch C]

CH-002: NODE-015 "Violent or Stealth?" (Branch A only)
  Option A1: "Use force"            → NODE-020A [Branch A1]
  Option A2: "Sneak approach"       → NODE-020B [Branch A2]

CH-003: NODE-025 "Keep or Release Victor?" (Branch A only)
  Option A1a: "Keep him locked up"  → NODE-030A [Branch A1a]
  Option A1b: "Release him"         → NODE-030B [Branch A1b]
```

### 2. **Track Consequences Per Choice**

For each choice, map immediate and delayed consequences:

```
CH-001 CONSEQUENCES:

Option A (Help Victor):
  ├─ Immediate (NODE-015):
  │  • victor_status = "escaped"
  │  • relationship_marcus += 10
  │  • reputation += 2
  │
  ├─ Short-term (NODE-020):
  │  • city_under_siege = true
  │  • militarization_level = 3
  │
  ├─ Medium-term (NODE-025):
  │  • Ending condition: relationship_marcus > 75 (available)
  │  • Victor appears as ally in NODE-030
  │
  └─ Ending (NODE-FINAL):
     • Ending A: "Redemption" (Victor escaped, city stabilizes)

Option B (Betray Victor):
  ├─ Immediate (NODE-016):
  │  • victor_status = "captured"
  │  • relationship_marcus -= 15
  │  • reputation -= 5 (if betrayal is known)
  │
  ├─ Short-term (NODE-021):
  │  • militia_influence = 5
  │  • player_regarded_as "collaborator"
  │
  ├─ Medium-term (NODE-025):
  │  • Ending condition: relationship_marcus < 50 (available)
  │  • Victor's allies seek revenge
  │
  └─ Ending (NODE-FINAL):
     • Ending B: "Tragedy" (Victor imprisoned, player isolated)

Option C (Flee):
  ├─ Immediate (NODE-017):
  │  • victor_status = "abandoned"
  │  • relationship_marcus = 50 (neutral)
  │  • reputation -= 1 (cowardice)
  │
  ├─ Short-term (NODE-022):
  │  • Safe outside city
  │  • But never resolve Victor's story
  │
  └─ Ending (NODE-FINAL):
     • Ending C: "Escape" (Survive, but unresolved threads)
```

### 3. **Analyze Consequence Clarity**

Measure how clear each consequence is:

```
CLARITY METRICS:

Consequence: choice_A → victor_status="escaped"
  Visibility: Explicit (NODE-015 prose: "Victor flees into darkness")
  Immediacy: 0 nodes (happens immediately)
  Traceability: High (choice → direct result, no intermediate steps)
  Clarity: ✅ EXCELLENT

Consequence: choice_A → reputation += 2
  Visibility: Implicit (only shown in variable, no prose)
  Immediacy: 0 nodes (hidden change)
  Traceability: Medium (player might not realize choice affected reputation)
  Clarity: ⚠️  MODERATE (consider adding prose hint)

Consequence: choice_A → ending_A becomes available
  Visibility: Implicit (only know ending exists when reached)
  Immediacy: 15+ nodes (NODE-015 choice, NODE-FINAL ending)
  Traceability: Complex (multiple choices compound to reach ending)
  Clarity: ⚠️  LOW (add foreshadowing or signpost about ending)
```

### 4. **Detect Consequence Problems**

#### 🔴 **PROBLEM: Identical Outcomes**
Multiple choices lead to the same story state.

```
CH-001 Comparison:

Option A (Help Victor):
  • NODE-015: relationship_marcus = 80
  • NODE-025: victor_status = "escaped"
  • ENDING: Ending A

Option B (Betray Victor):
  • NODE-016: relationship_marcus = 80 ???
  • NODE-025: victor_status = "escaped" ???
  • ENDING: Ending A ???

Problem: Both choices lead to SAME state
         Choice feels illusory (doesn't matter)
         Player won't understand difference between help/betray
         
Status: 🔴 ILLUSORY CHOICE

Fix: Ensure each option has distinguishing consequence
     E.g., Option B should have:
       • relationship_marcus = 35 (not 80)
       • victor_status = "captured" (not "escaped")
       • ENDING B (not A)
```

#### 🟡 **PROBLEM: Delayed Consequence**
Consequence appears so late that choice-outcome connection is unclear.

```
CH-001 (NODE-010): Help Victor

Consequence appears:
  NODE-010: Choice made (Help)
  NODE-015: No visible effect
  NODE-020: No visible effect
  NODE-025: Victor appears (5 nodes later!)
  
Problem: Player chooses to help at NODE-010
         Doesn't see Victor again until NODE-025 (15 nodes later)
         By then, has made other choices (might forget original choice)
         Connection is weak
         
Status: 🟡 DELAYED CONSEQUENCE

Standard guideline:
  • 0–1 nodes: Immediate ✅ (player clearly sees result)
  • 2–3 nodes: Short-term ✅ (still feels connected)
  • 4–5 nodes: Medium ⚠️  (connection getting tenuous)
  • 6+ nodes: Long-term ❌ (feels disconnected; foreshadow needed)

Fix: Either:
  1. Add immediate hint at NODE-015 (Victor's absence is absence felt)
  2. Add intermediate consequence (allies mention Victor at NODE-020)
  3. Move Victor's appearance to NODE-015 or NODE-020
```

#### 🟠 **PROBLEM: Orphaned Choice Branch**
Choice leads to dead-end with no payoff or reconnection.

```
CH-001: "Help or Leave?"

Option A (Help):
  NODE-015 → NODE-020 → NODE-025 → ENDING
  ✅ Leads to ending

Option B (Leave):
  NODE-016 → NODE-021 → NODE-026 → ???
  No ENDING node after NODE-026
  NODE-026: Dead end

Problem: Players who choose B get stuck
         No way forward to ending
         Branch is incomplete
         
Status: 🟠 ORPHANED BRANCH

Fix: Either:
  1. Add NODE-027 (ENDING for this branch)
  2. Merge NODE-026 back to main story (reconvergence)
  3. Make NODE-026 itself a final ending node
```

#### 💨 **PROBLEM: Consequence Chain Too Complex**
Multiple steps between choice and payoff; hard to trace.

```
CH-001: Help Victor

Chain:
  NODE-010: Help Victor chosen
    → victor_status = "escaped"
    → alertness_level += 1
    → city_security += 2
  
  NODE-015: (automatic consequence)
    → IF alertness_level > 0: militia_patrols spawn
    → IF city_security > 1: additional checkpoints
    → IF victor_status = "escaped": THEN bounty_hunters_hired
  
  NODE-020: (cascading consequence)
    → IF bounty_hunters_hired: THEN relationship_marcus affected
    → IF relationship_marcus < 50: THEN Marcus becomes hostile
    → IF Marcus hostile: THEN NODE-025 changes completely
  
  NODE-025: (final consequence)
    → Outcome depends on 3 prior conditional variables

Problem: Help choice → 7 variable mutations across 4 nodes
         With 3 IF statements creating branching logic
         Player can't trace: "Did I cause this by helping, or other choices?"
         
Status: 💨 OVERCOMPLICATED

Fix: Simplify chain
     • Direct: choice → 2–3 immediate consequences (max)
     • Transparent: each consequence clearly labeled
     • Optional: add intermediate consequences IF explicitly called out
```

#### 🟢 **PROBLEM: Consequence Contradicts Setup**
Consequence doesn't match foreshadowing or logical expectation.

```
Setup: NODE-005
  Dialogue: "Marcus is a city detective. He values honesty above all."
  (Implies: betrayal would anger him)

Choice: NODE-010
  "Betray Victor to Marcus"
  Expected consequence: Marcus respects your honesty, relationship ↑
  Logical expectation: Since Marcus values honesty → should like you more

Actual consequence: NODE-016
  relationship_marcus = 35 (decreased!)
  Dialogue: "You're a monster. I don't want to see you again."
  
Problem: Consequence contradicts setup
         If Marcus values honesty, why does he hate you for being honest?
         Feels arbitrary/punitive
         
Status: 🟢 SETUP CONTRADICTION

Fix: Either:
  1. Change setup: Marcus doesn't value honesty → betrayal is fine
  2. Change consequence: Betrayal earns Marcus's respect (honesty was right choice)
  3. Add context: Marcus values honesty WITH Victor, not betrayal OF Victor
     → Change dialogue to: "You betrayed him. He trusted you."
     → Now contradiction resolved (honesty != betrayal of trust)
```

### 5. **Generate Consequence Map Report**

Create `specs/consequence-audit.md`:

```markdown
## Choice Consequence Audit

**Game**: [NAME]
**Date**: [ISO]

### Choice Consequence Map

| Choice | Option | Consequence | Immediacy | Clarity | Status |
|--------|--------|-------------|-----------|---------|--------|
| CH-001 | Help | victor=escaped, relationship+10 | 0 nodes | ✅ Explicit | ✅ Pass |
| CH-001 | Betray | victor=captured, relationship-15 | 0 nodes | ✅ Explicit | ✅ Pass |
| CH-001 | Flee | victor=abandoned, reputation-1 | 0 nodes | ⚠️ Implicit | ⚠️ Review |
| CH-002A | Violent | militia_alert+2 | 1 node | ✅ Explicit | ✅ Pass |
| CH-002A | Stealth | militia_alert+0 | 1 node | ✅ Explicit | ✅ Pass |

### Consequence Problems

**🔴 Identical Outcomes** (0):
- None found

**🟡 Delayed Consequences** (1):
- CH-001 Help: Victor payoff appears 5 nodes after choice
  Fix: Add intermediate hint at NODE-015

**🟠 Orphaned Branches** (1):
- CH-001 Flee: NODE-026 leads to dead-end
  Fix: Add NODE-027 or reconverge to main story

**💨 Overcomplicated Chains** (0):
- None found

**🟢 Setup Contradictions** (0):
- None found

### Recommendations

Priority 1: Fix orphaned NODE-026
Priority 2: Add intermediate consequence hint for CH-001 Help
Priority 3: Consider making reputation consequence more explicit
```

### 6. **Show Chains** (optional with --show-chains)

Display multi-step consequence chains:

```
CH-001 HELP: Consequence Chain

NODE-010: Choice "Help Victor"
  ↓ [Direct consequence]
NODE-015: 
  ├─ victor_status = "escaped"
  ├─ relationship_marcus += 10 (now 65)
  ├─ reputation += 2
  │
  └─ [Triggers at NODE-020]
    ├─ Marcus suspicious of you helping prisoner escape
    ├─ IF reputation >= 50: militia doesn't pursue
    ├─ IF reputation < 50: militia pursues
    │
    └─ [Ends at NODE-025]
      ├─ IF militia pursued: bounty on your head → different ending path
      ├─ IF militia didn't pursue: Victor sends message → ally path
      │
      └─ ENDING A or A'
         (Different because of NODE-020 reputation check)

Chain length: 4 nodes (NODE-010 → 015 → 020 → 025 → ENDING)
Complexity: Medium (1 conditional fork)
Clarity: ✅ GOOD (each step builds logically)
```

### 7. **Report**

Output `consequence-audit.md` with:
- Choice-consequence map (all choices, all options, visible consequences)
- Immediacy analysis (how many nodes before consequence appears?)
- Clarity assessment (is connection obvious to player?)
- Problem list (identical, delayed, orphaned, overcomplicated, contradictions)
- If `--show-chains`: Full consequence chains with conditional branches
- If `--orphaned-only`: Only dead-end branches

---

## Important Notes

**Consequences Should Be Visible**: Players won't feel agency if consequences happen "under the hood." Make them explicit in prose, NPC dialogue, or gameplay changes.

**Timing Matters**: 0–2 nodes after choice = feels like direct consequence. 5+ nodes = feels like coincidence.

**Consequences Can Be Conditional**: Same choice can have different outcomes per branch (e.g., Help Victor → escapes if militia alert is low, captured if alert is high). This is valid; just ensure each possibility is traceable.

**Cumulative Consequences**: Different choices can compound (choice A + choice B = different outcome than A alone or B alone). This is good design; just keep chains to <4 steps so players can follow.

**Foreshadow Delayed Consequences**: If a consequence appears 5+ nodes after choice, foreshadow it. Have an NPC mention it, or show the setup for it, so player understands the connection.

