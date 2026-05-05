---
description: Replayability metrics — measure unique content per playthrough, branch coverage, variation in dialogue/prose, and content reuse across paths.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: After measuring replayability, verify choices provide meaningful variations.
    send: true
  - label: Analyze Complexity
    agent: speckit.complexity
    prompt: Review branch structure to optimize replayability coverage.
    send: true
---

# speckit.replayability

Replayability metrics — measure **unique content per playthrough, branch coverage, dialogue variation, and content reuse**. Helps optimize for "want to play again" factor.

## Replayability Principle

**High replayability** = Each playthrough reveals different content, choices lead to distinct experiences, player has reason to see other branches.

**Low replayability includes**:
- ❌ Same prose in all branches (only variables change)
- ❌ High content reuse (>70% of prose is shared across branches)
- ❌ Limited branching (all paths converge quickly)
- ❌ Predictable outcomes (choices don't produce surprising variations)

**Valid replayability includes**:
- ✅ Distinct prose per branch (each path has unique dialogue/scenes)
- ✅ Moderate content reuse (40–60% shared, rest branch-specific)
- ✅ Multiple endings with meaningful differences
- ✅ Hidden content (only revealed in certain branches)
- ✅ Variant NPCs (different characters appear per path)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze overall replayability metrics
- `--branch [BRANCH_ID]` — analyze replayability within one branch only
- `--content` — focus on unique prose content per branch

Optional flags:
- `--strict` — flag >50% content reuse as excessive
- `--show-coverage` — ASCII grid of which branches see which content
- `--show-variance` — display variant prose per branch
- `--unique-only` — show only branch-specific content (hide shared prose)

## Pre-Execution Checks

1. Load `specs/plan.md`: Branch structure, node mapping
2. Load all `draft/[ENGINE]/NODE-*.md` files
3. Parse prose content (separate from code/mechanics)
4. Identify shared vs. branch-specific nodes
5. Calculate word count per branch type
6. Trace which nodes are reachable per branch

## Execution Steps

### 1. **Measure Unique Content Per Branch**

For each branch, measure original prose:

```
Content accounting:

Shared nodes (all branches visit):
  NODE-001 through NODE-010: 10 nodes
  Total prose: 5,500 words
  Reachability: 100% (every playthrough includes)

Branch A (Help Victor):
  NODE-015, NODE-020, NODE-025 (6 variants): 3,200 words
  Reachability: A path only
  Exclusivity: 0% shared with B/C (100% unique to A)

Branch B (Betray Victor):
  NODE-016, NODE-021, NODE-026: 2,800 words
  Reachability: B path only
  Exclusivity: 0% shared with A/C (100% unique to B)

Branch C (Flee):
  NODE-017, NODE-022, NODE-027: 2,100 words
  Reachability: C path only
  Exclusivity: 0% shared with A/B (100% unique to C)

Totals:
  • Shared: 5,500 words (45%)
  • Branch-specific: 8,100 words (55%)
  • Total: 13,600 words

Per-playthrough content:
  • Branch A playthrough: 5,500 (shared) + 3,200 (A) = 8,700 words
  • Branch B playthrough: 5,500 (shared) + 2,800 (B) = 8,300 words
  • Branch C playthrough: 5,500 (shared) + 2,100 (C) = 7,600 words
  
Content overlap between playthroughs:
  • A vs B overlap: 5,500 / 8,700 = 63% (large shared content)
  • A vs C overlap: 5,500 / 8,700 = 63%
  • B vs C overlap: 5,500 / 8,300 = 66%

Unique content per fresh playthrough:
  • Playthrough 1: 100% unique
  • Playthrough 2: 37% unique (65% shared with playthrough 1)
  • Playthrough 3: 37% unique (65% shared with previous plays)
```

### 2. **Calculate Content Reuse Ratio**

Measure how much prose is recycled across branches:

```
Content reuse matrix:

         A      B      C
A        —     5,500  5,500
B      5,500   —     5,500
C      5,500  5,500   —

Reading: Row A, Column B = both A and B contain the shared 5,500-word intro

Reuse percentage:
  • A–B overlap: 5,500 / (3,200 + 2,800) = 5,500 / 6,000 = 92% (very high)
    Interpretation: 92% of branch-specific content is actually shared
  
  • A–C overlap: 5,500 / (3,200 + 2,100) = 5,500 / 5,300 = 104% ???
    Wait, that's >100%; recalculate using union instead
  
  Better formula (Jaccard similarity):
  overlap / (A_content + B_content - overlap)
  = 5,500 / (8,700 + 7,600 - 5,500)
  = 5,500 / 10,800
  = 51% (moderate)

Interpretation:
  • 51% of content is seen in both A and C paths
  • 49% of content is unique to each branch
  • This is GOOD (neither over-reused nor too sparse)

Reuse assessment by category:
  • <30% reuse: Too branch-specific (wasteful, no consistency)
  • 30–50% reuse: Good balance (consistent intro, unique development)
  • 50–70% reuse: Moderate (shared story with variations)
  • >70% reuse: Excessive (feels like only variables change)
  
This game: 51% reuse = ✅ GOOD BALANCE
```

### 3. **Analyze Content Variation Per Branch**

Examine how prose differs across similar scenes:

```
SCENE: "Confronting Marcus" (appears in all branches)

Branch A version:
  "Marcus sits across from you, hands folded.
   'You helped Victor escape,' he says quietly.
   'I know it was the right choice.'
   His expression has changed—there's respect there."
   
Prose quality: Warm, accepting tone
Word count: 45 words
Mechanical effect: relationship_marcus += 10

Branch B version:
  "Marcus stands when you enter, face dark with anger.
   'You let him go,' he hisses.
   'Victor will cause more death.'
   His jaw clenches. He won't even look at you."
   
Prose quality: Cold, disappointed tone
Word count: 42 words
Mechanical effect: relationship_marcus -= 15

Branch C version:
  "Marcus shows no reaction when you walk in.
   'You ran,' he observes.
   'Smart. I would have done the same.'
   He returns to his paperwork, dismissing you."
   
Prose quality: Detached, pragmatic tone
Word count: 38 words
Mechanical effect: relationship_marcus += 0

Variation analysis:
  • All three versions address same event (confrontation)
  • All three have same mechanical purpose (affect relationship)
  • Prose DIFFERS significantly (warm vs cold vs indifferent)
  • Tone REFLECTS branch outcomes (aligned with Victor choice)
  
Content variation quality: ✅ EXCELLENT
              (Same scene, different prose, supports narrative)
```

### 4. **Detect Replayability Problems**

#### 🔴 **PROBLEM: Same Prose Across Branches**
Multiple branches have identical dialogue despite different contexts.

```
Branch A (Help Victor):
  NODE-020: "The city gate opens. You slip through."

Branch B (Betray Victor):
  NODE-020: "The city gate opens. You slip through."

Branch C (Flee):
  NODE-020: "The city gate opens. You slip through."

Problem: All three branches have IDENTICAL prose
         Yet outcomes are completely different (help/betray/flee)
         This feels fake—prose should reflect choice
         
Status: 🔴 SAME PROSE, DIFFERENT CHOICES

Fix options:
  1. Rewrite prose for each branch (B1: grateful escape, B2: guilty escape, C: cowardly escape)
  2. Use variable prose (if help: "...grateful"; if betray: "...guilty")
  3. Move this shared prose earlier (before divergence)
  
Impact: Players who replay feel like they're reading same content
        Reduces replayability
```

#### 🟡 **PROBLEM: Excessive Content Reuse**
>70% of content is shared across branches; branches feel cosmetic.

```
Game structure:
  • Shared nodes: 40 nodes
  • Branch A: 2 unique nodes
  • Branch B: 2 unique nodes
  • Branch C: 2 unique nodes
  
Reuse calculation:
  Shared: 40 nodes
  Total unique content: 6 nodes
  Reuse ratio: 40 / (40 + 6) = 87%
  
Problem: 87% reuse is excessive
         Feels like only variables change, not actual story
         Branches lack distinct identity
         
Status: 🟡 EXCESSIVE REUSE

Example: If reuse is >70%, the question becomes:
         "Am I really playing a different game, or just the same game with different flags?"

Fix options:
  1. Expand branch-specific content (write more unique scenes)
  2. Consolidate branches (merge similar paths into one)
  3. Keep >70% reuse if intentional (e.g., "same story, different player stats")
```

#### 🟠 **PROBLEM: Limited Branching**
Branches converge so quickly that unique content per path is minimal.

```
Design:
  NODE-001 (shared, 10 nodes)
  NODE-010 [divergence]: 3 branches
  NODE-015 [reconvergence]: All branches meet
  NODE-020+ (shared)
  
Content per branch:
  A: NODE-011, NODE-012, NODE-013 (3 nodes, ~600 wc)
  B: NODE-011, NODE-012, NODE-013 (same nodes, different prose) ???
  
Problem: Branch A and B share THE SAME NODE IDs
         But with different prose variants
         This is variable-based branching, not node branching
         
Results in:
  • Branch A: 10 (shared) + 3 (variant) = 13 nodes total
  • Branch B: 10 (shared) + 3 (variant) = 13 nodes total
  • Unique content: 3 nodes × 2 variants = only 6 unique nodes of actual branching
  
Replayability: ⚠️ LIMITED
              With quick reconvergence, branches feel superficial
              
Assessment: Is this acceptable?
  ✅ YES if: variants are SIGNIFICANTLY different (large prose changes, different mechanics)
  ❌ NO if: variants are cosmetic (same story, different flavor text)
```

#### 💨 **PROBLEM: Hidden Content Never Revealed**
Content exists in some branches but is inaccessible to most players.

```
Game structure:
  3 main branches (Help / Betray / Flee)
  
Branch A only content (secret scene):
  NODE-020A: Special dialogue with Marcus (only if relationship > 80)
  Content: 1,200 words (10% of branch A content)
  
Reachability:
  • Requires: Help Victor + Violent approach + no prior betrayals
  • Reachable in: 1 of 3 main paths
  • Percentage of players seeing it: ~33% (if distribution is even)
  
Problem: If players don't explore all branches, they'll miss content
         Hidden content isn't replayability if it's required for "completion"
         But if it's optional bonus: it's GOOD for replayability
         
Status: ✅ IF INTENTIONAL BONUS, otherwise 💨 WASTED CONTENT

Question: Is this secret designed to be found?
         Or accidentally hidden?
         
If intentional: mark it clearly (Achievements, guides)
If accidental: either remove or move to more accessible branch
```

### 5. **Generate Replayability Report**

Create `specs/replayability-audit.md`:

```markdown
## Replayability Audit

**Game**: [NAME]
**Date**: [ISO]

### Content Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Total prose | 13,600 wc | Good volume |
| Shared content | 5,500 wc (40%) | ✅ Balanced |
| Branch-unique | 8,100 wc (60%) | ✅ Good variation |
| Content reuse | 51% | ✅ Healthy |
| Avg playthrough | 8,200 wc | ~40 min reading |
| Fresh content per playthrough | 37% | Moderate |

### Branch Coverage

| Branch | Playthrough | Unique | Reuse | Content |
|--------|------------|--------|-------|---------|
| A | 8,700 wc | 3,200 wc | 63% | Redemption |
| B | 8,300 wc | 2,800 wc | 66% | Tragedy |
| C | 7,600 wc | 2,100 wc | 72% | Escape |

### Replayability Assessment

**Content variation**: ✅ GOOD
- Each branch has distinct prose and tone
- Choice consequences reflected in prose variations
- No identical scenes across branches

**Branch distinctness**: ✅ GOOD
- 3 main branches with clear thematic differences
- A: Redemption (relationship +10 with Marcus, Victor escaped)
- B: Betrayal (relationship -15, Victor captured)
- C: Escape (relationship neutral, Victor fate ambiguous)

**Hidden content**: ✅ INTENTIONAL BONUS
- Secret scene in Branch A (relationship > 80)
- Discoverable on 2nd playthrough
- Not required for completion

**Replayability score**: 7/10

### Issues

**🔴 None critical**

**🟡 Moderate**:
1. Branch C has lowest unique content (2,100 wc)
   Consider: Add one more Branch C unique scene (~1,000 wc)

**Opportunities**:
1. Add hidden dialogue variant in Branch B (if relationship > 50 despite betrayal)
2. Consider alternate ending in Branch A (romantic vs platonic reconciliation)

### Recommendations

**For higher replayability** (if desired):
1. Expand Branch C to match A/B in unique content
2. Add 1–2 more choice points to create sub-variants (currently A has 1 sub-choice)
3. Consider new game+ content (unlocks after completing 1 branch)
4. Mark secrets clearly so players know they missed content

**Current design**: ✅ Solid baseline replayability
                   Players will want to see all 3 branches
                   Each playthrough offers ~37% new content
                   Recommend for players who like branching narratives
```

### 6. **Show Coverage** (optional with --show-coverage)

ASCII grid of which nodes appear in which branches:

```
CONTENT COVERAGE MATRIX

Node        A  B  C  Shared  Unique
────────────────────────────────────
NODE-001    ✅ ✅ ✅  YES      —
NODE-005    ✅ ✅ ✅  YES      —
NODE-010    ✅ ✅ ✅  YES      —
NODE-015    ✅ ❌ ❌  NO       A only
NODE-020A   ✅ ❌ ❌  NO       A (secret)
NODE-016    ❌ ✅ ❌  NO       B only
NODE-021    ❌ ✅ ❌  NO       B only
NODE-017    ❌ ❌ ✅  NO       C only
NODE-022    ❌ ❌ ✅  NO       C only
NODE-025    ✅ ✅ ✅  YES      —
────────────────────────────────────

Shared content: 5 nodes (visible in all paths)
A-only: 2 nodes (NODE-015, NODE-020A)
B-only: 2 nodes (NODE-016, NODE-021)
C-only: 2 nodes (NODE-017, NODE-022)

Key insight:
  • Half of game is shared introduction
  • Each branch has ~2 unique scenes
  • Very little overlap between B and C content
  • A has extra secret scene (NODE-020A)
```

### 7. **Show Variance** (optional with --show-variance)

Display variant prose for identical scene points:

```
SCENE: "Confronting Marcus"

─ Branch A (Help Victor) ─
"Marcus sits across from you, hands folded.
 'You helped Victor escape,' he says quietly.
 'I know it was the right choice.'
 His expression has changed—there's respect there."
[+10 relationship]

─ Branch B (Betray Victor) ─
"Marcus stands when you enter, face dark with anger.
 'You let him go,' he hisses.
 'Victor will cause more death.'
 His jaw clenches. He won't even look at you."
[-15 relationship]

─ Branch C (Flee) ─
"Marcus shows no reaction when you walk in.
 'You ran,' he observes.
 'Smart. I would have done the same.'
 He returns to his paperwork, dismissing you."
[+0 relationship]

Prose variations:
  A: Warm, accepting (seated, makes eye contact, praises)
  B: Angry, disappointed (stands, won't look at you, hisses)
  C: Detached, pragmatic (ignores you, returns to work)
  
Quality: ✅ EXCELLENT variation
         (Same scene beats, completely different emotional tone)
```

### 8. **Report**

Output `replayability-audit.md` with:
- Content metrics (total prose, shared vs unique, reuse ratio)
- Branch coverage analysis (what % of content is per-branch-only)
- Replayability score (1–10)
- Assessment of variation quality
- If `--show-coverage`: Content coverage matrix
- If `--show-variance`: Variant prose for key scenes
- If `--unique-only`: Only branch-specific content (hide shared intro)

---

## Important Notes

**Content Reuse 40–60% Is Ideal**: Allows consistency (shared world-building) while maintaining branch distinctness. Anything >70% starts feeling repetitive; anything <30% wastes effort.

**Hidden Content Has Diminishing Returns**: Most players won't see all branches on first playthrough. Hidden content is a bonus for completionists. Don't hide critical story behind low-probability branches.

**"New Game+" Extends Replayability**: If you unlock content after completing a branch, players have reason to replay. Sequential content unlock is powerful.

**Prose Quality > Quantity**: A 5,000-word unique branch with identical prose feels worse than a 2,000-word branch with totally distinct voice. Variation matters more than volume.

**Player Motivation Matters**: Players replay because:
1. Multiple endings (want to see them all)
2. Different protagonist choices (want to play their way)
3. Unlockable content (want to complete collection)
4. Challenge/speedrun (want optimal path)

Design for at least 1–2 of these motivations to maximize replayability.

