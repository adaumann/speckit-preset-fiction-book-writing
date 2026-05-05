---
description: Story pacing analyzer — measure word count, beat spacing, emotional tempo, and reading time per branch. Detects pacing problems (info dumps, draggy sections, rushed climax).
handoffs:
  - label: Check Tone
    agent: speckit.tone
    prompt: After analyzing pacing, validate emotional beats align with pace.
    send: true
  - label: Revise Pacing
    agent: speckit.revise
    prompt: Some sections have pacing problems. Please adjust prose length and beat spacing.
    send: true
---

# speckit.pacing

Story pacing analyzer — measure **word count, beat spacing, emotional tempo, and reading time** per branch. Detects problems: info dumps, draggy middle, rushed climax, dead zones.

## Pacing Principle

**Good pacing** = Emotional beats, prose length, and scene changes maintain consistent reading rhythm; player never feels bored or overwhelmed.

**Bad pacing includes**:
- ❌ Info dump (1,000+ word exposition block with no dialogue/action)
- ❌ Draggy middle (sequences where nothing changes; minimal prose but feels slow)
- ❌ Rushed climax (2,000 words leading to 500 word payoff)
- ❌ Dead zones (nodes with low word count AND no emotional/mechanical change)
- ❌ Inconsistent node size (NODE-010 is 300 words, NODE-011 is 4,000 words for same scene weight)

**Valid pacing includes**:
- ✅ Varied node length (300–3,000 words) reflecting emotional weight
- ✅ Short nodes for decisions/transitions
- ✅ Long nodes for climactic moments
- ✅ Beat spacing matches emotional progression (clusters during tension, space after climax)
- ✅ Reading time roughly equal across same-weight story phases

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — analyze entire game pacing across all branches
- Branch ID (e.g., `BRANCH-A`) — analyze pacing in one branch only
- `--act [N]` — analyze pacing of a single act only
- `--node [NODE-ID]` — analyze one node in detail

Optional flags:
- `--strict` — flag any node >2,500 words or <100 words
- `--target-wc [NUMBER]` — custom target word count per node (default: 800)
- `--show-stats` — display full statistics table
- `--show-graph` — ASCII graph of word count per node

## Pre-Execution Checks

1. Load `specs/plan.md`: Branch structure, act boundaries
2. Load all `draft/[ENGINE]/NODE-*.md` files
3. Parse node prose (exclude YAML frontmatter, metadata)
4. Identify emotional beat markers (dialogue, action, revelation)
5. Load `specs/constitution.md` target reading time if specified

## Execution Steps

### 1. **Measure Word Count Per Node**

For each node, count prose words (exclude code/syntax):

```
NODE-010: (drama scene, relationship intro)
  Prose: "The cafe was crowded, but Marcus stood out.
          His dark suit looked expensive, dangerous. 
          He waited at the corner table, watching the door.
          When I entered, his expression didn't change,
          but his hand tightened on the coffee cup."
          
  Word count: 47 words
  Status: ✅ SHORT (appropriate for intro)

NODE-015: (exposition + dialogue)
  Prose: [1,800 words of dialogue explaining backstory]
  Status: ⚠️ LONG (but contains dialogue, so justified)

NODE-020: (climactic confrontation)
  Prose: [2,400 words of action, dialogue, emotional beats]
  Status: ✅ LONG (appropriate for climax weight)

NODE-025: (quiet aftermath)
  Prose: [250 words of reflection]
  Status: ✅ SHORT (appropriate for post-climax space)
```

### 2. **Categorize Nodes by Weight**

Assign emotional/mechanical weight to each node:

```
Weight categories:
  🔴 MAJOR (climax, major choice, major revelation)
     Expected: 1,500–3,000 words
     Example: NODE-020 (confrontation), NODE-015 (plot twist)
  
  🟡 MODERATE (development, dialogue, moderate stakes)
     Expected: 800–1,500 words
     Example: NODE-010 (relationship intro), NODE-017 (subplot progress)
  
  🟢 MINOR (transition, decision point, brief scene)
     Expected: 300–800 words
     Example: NODE-005 (setup), NODE-025 (quiet moment)
  
  ⚪ MICRO (navigation, brief exchange, mechanical)
     Expected: 50–300 words
     Example: NODE-003 (intro), NODE-012 (door passage)
```

**Node categorization example**:
```
NODE-005: Setting introduction       → MINOR (300–800 wc)
NODE-010: Character intro           → MODERATE (800–1,500 wc)
NODE-015: Major revelation          → MAJOR (1,500–3,000 wc)
NODE-020: Choice moment             → MODERATE (800–1,500 wc)
NODE-025: Aftermath reflection      → MINOR (300–800 wc)
ENDING:   Narrative resolution      → MODERATE/MAJOR (600–2,000 wc)
```

### 3. **Analyze Pacing Per Branch**

Create a pacing timeline:

```
BRANCH A: Redemption Path
═════════════════════════════════════

NODE-005 (MINOR):  50 wc  | Setup intro          | ✅ Appropriate
NODE-010 (MOD):    950 wc | Relationship intro   | ✅ Appropriate
NODE-012 (MOD):    1,200 wc | Dialogue reveal    | ⚠️ LONG but justified (dialogue)
NODE-015 (MAJOR):  2,300 wc | Choice climax      | ✅ Appropriate for weight
NODE-020 (MOD):    800 wc  | Victor escape scene | ✅ Appropriate
NODE-025 (MINOR):  400 wc  | Quiet moment       | ✅ Appropriate
ENDING (MOD):      900 wc  | Resolution         | ✅ Appropriate

Reading time: ~15 minutes
Total words: 6,600 wc
Average node: 943 wc
Pace stability: ✅ GOOD (varied but consistent)

Pacing analysis:
  • Climax (NODE-015) is longest: ✅ Good
  • Post-climax (NODE-020, NODE-025): Short & medium ✅ Good spacing
  • Overall rhythm: Builds to NODE-015, then releases ✅ Satisfying
```

### 4. **Detect Pacing Problems**

#### 🔴 **PROBLEM: Info Dump**
Single node has 2,000+ words of exposition with minimal dialogue/action.

```
NODE-012 (backstory reveal):
  Prose: [2,100 words of character monologue explaining family history]
  
Analysis:
  • Word count: 2,100 wc (HIGH)
  • Dialogue: 5% (minimal)
  • Action: 0% (static)
  • Beat changes: None (single scene, same location, no mechanical change)
  
Problem: Reader must absorb 2,100 words of exposition without break
Status: 🔴 INFO DUMP

Flag: Feels like encyclopedia dump
Fix options:
  1. Break into 2-3 nodes with intervening action
  2. Add dialogue interaction (character responds, interrupts)
  3. Reduce to 1,200 words max with key details only
  4. Move to multiple scenes with dialogue/action interspersed
```

#### 🟡 **PROBLEM: Draggy Middle**
Sequence where nothing mechanically/emotionally changes; minimal prose but feels slow.

```
NODE-013 → NODE-014 → NODE-015:
  
NODE-013 (travel to city):  150 wc
  Prose: "We rode for three days. The landscape changed."
  No decision. No emotional beat. No new information.
  
NODE-014 (arrive at city):  200 wc
  Prose: "The city gates loomed. Guards checked papers."
  No decision. No emotional beat. No new information.
  
NODE-015 (enter tavern):    180 wc
  Prose: "Inside smelled of ale and smoke."
  No decision. No emotional beat. No new information.

Combined: 530 wc across 3 nodes with NO mechanical/emotional change
Reading time: ~3 minutes
Impact: Player feels like progress stalls despite prose

Problem: Transitional beats stretched thin
Status: 🟡 DRAGGY MIDDLE

Flag: These nodes could be combined or cut entirely
Fix options:
  1. Combine into single 300-word transition
  2. Add decision point in NODE-014 (different routes to tavern?)
  3. Add emotional beat (nervous about city? Excited?)
  4. Add NPC interaction (helpful guide? Suspicious merchant?)
```

#### 🟠 **PROBLEM: Rushed Climax**
Climactic moment receives disproportionately short prose compared to build-up.

```
Build-up:
  NODE-010: 1,200 wc (tension rises)
  NODE-012: 1,400 wc (stakes revealed)
  NODE-015: 1,600 wc (choice point)
  Subtotal: 4,200 wc of build-up

Climax:
  NODE-020: 500 wc (confrontation resolved)
  
Analysis:
  Build-up:Climax ratio = 4,200:500 = 8.4:1
  Standard ratio should be ~3:1 to 5:1
  
Problem: 4,200 words of build-up paid off in 500 words
         Feels anticlimactic, rushed, unearned
         
Status: 🟠 RUSHED CLIMAX

Flag: Climax underwritten relative to investment
Fix: Expand NODE-020 to 1,500–2,000 words minimum
```

#### 💨 **PROBLEM: Dead Zone**
Node with low word count AND no emotional/mechanical change; feels pointless.

```
NODE-018 (transition scene):
  Word count: 85 wc
  Prose: "I left the apartment and walked to the street.
          A taxi was waiting."
  
Analysis:
  • Word count: 85 wc (VERY SHORT)
  • Emotional beat: None
  • Mechanical change: None (no choice, no new information)
  • Purpose: Scene transition only
  
Problem: Too short to matter, too long to ignore
         Reads like a vestigial scene that could be cut

Status: 💨 DEAD ZONE

Flag: Cut this node entirely OR combine with adjacent node
Fix: Either delete NODE-018, or merge with NODE-017 or NODE-019
```

#### 📊 **PROBLEM: Inconsistent Node Size**
Similar-weight scenes vary wildly in length.

```
Same act, same scene weight:

NODE-010 (dialogue scene):   300 wc
NODE-015 (dialogue scene):   2,800 wc
NODE-020 (dialogue scene):   500 wc

Analysis:
  All three are dialogue-driven relationship development
  All three occur at similar story points
  Word counts vary 300x → 2,800x → 500x
  
Problem: Why does NODE-015 get 9x the space as NODE-010?
         If both are "dialogue scenes," they should be closer
         
Status: 📊 INCONSISTENT NODE SIZE

Possible reasons (verify):
  ✅ VALID: NODE-015 is climactic dialogue; others are exposition
  ✅ VALID: NODE-010 is quick intro; NODE-020 is complex negotiation
  ❌ PROBLEM: Inconsistency is accidental; editor missed one scene

Fix: Either justify the difference in weight, or normalize to 800–1,200 wc
```

### 5. **Calculate Reading Time**

Estimate total reading time per branch:

```
Standard reading speed: 200–250 words per minute
Conservative: 200 wpm (slower, more thoughtful reading)
Aggressive: 250 wpm (faster, skimming)

BRANCH A word count: 6,600 words

Estimated reading time:
  • At 200 wpm (conservative): 33 minutes
  • At 225 wpm (average): 29 minutes
  • At 250 wpm (fast): 26 minutes

Report: "BRANCH A estimated reading time: 26–33 minutes"

Target check:
  If constitution specifies "30-minute gameplay":
    BRANCH A (26–33 min) ✅ WITHIN RANGE
  
  If constitution specifies "15-minute gameplay":
    BRANCH A (26–33 min) ⚠️  TOO LONG
    Fix: Cut 3,300+ words (50% reduction needed)
```

### 6. **Generate Pacing Audit Report**

Create `specs/pacing-audit.md`:

```markdown
## Pacing Audit

**Game**: [NAME]
**Target Reading Time**: 30 minutes (from constitution)
**Date**: [ISO]

### Branch Pacing Summary

| Branch | Total WC | Avg Node | Reading Time | Status |
|--------|----------|----------|--------------|--------|
| Branch A | 6,600 | 943 | 26–33 min | ✅ On target |
| Branch B | 5,200 | 867 | 21–26 min | ✅ On target |
| Branch C | 7,800 | 1,040 | 31–39 min | ⚠️ 6 min over |

### Node Length Analysis

| Node | Weight | WC | Target | Status |
|------|--------|----|---------| -------|
| NODE-005 | MINOR | 50 | 300–800 | ✅ Short but OK |
| NODE-010 | MOD | 950 | 800–1,500 | ✅ Good |
| NODE-012 | MOD | 2,100 | 800–1,500 | 🔴 INFO DUMP |
| NODE-015 | MAJOR | 2,300 | 1,500–3,000 | ✅ Good |
| NODE-020 | MOD | 500 | 800–1,500 | 🟠 SHORT FOR WEIGHT |

### Pacing Problems

**🔴 Info Dump** (1):
- NODE-012: 2,100 wc backstory monologue (fix: break into 2 scenes)

**🟡 Draggy Middle** (1):
- NODE-013→014→015: 530 wc across 3 nodes, no change (fix: combine or add decision)

**🟠 Rushed Climax** (1):
- NODE-020: 500 wc payoff vs 4,200 wc build-up (fix: expand to 1,500+ wc)

**💨 Dead Zone** (1):
- NODE-018: 85 wc transition-only (fix: delete or merge)

**📊 Inconsistent Size** (1):
- NODE-010/015/020: Similar weight, 300–2,800 wc variance (fix: normalize)

### Recommendations

**Priority 1 (Major impact)**:
1. NODE-012: Break info dump into 2–3 scenes with dialogue/action
2. NODE-020: Expand rushed climax to match build-up investment
3. Branch C: Cut 1,500+ words to match 30-minute target

**Priority 2 (Polish)**:
1. NODE-013→014→015: Consolidate dead transitions
2. NODE-010/015/020: Normalize similar scenes to 800–1,200 wc

**Overall Assessment**: Pacing generally good; 5 specific problem areas identified.
```

### 7. **Show Stats** (optional with --show-stats)

Full statistics table:

```
PACING STATISTICS

Nodes:          37 total
Total WC:       18,600 words
Average WC:     502 words/node

Word count distribution:
  • Under 100 wc:    5 nodes (13%)    [MICRO]
  • 100–300 wc:      8 nodes (22%)    [MINOR]
  • 300–800 wc:      12 nodes (32%)   [MINOR+]
  • 800–1,500 wc:    8 nodes (22%)    [MODERATE]
  • 1,500–2,500 wc:  3 nodes (8%)     [MAJOR]
  • 2,500+ wc:       1 node  (3%)     [MAJOR+]

Longest node:   NODE-012 (2,100 wc)
Shortest node:  NODE-018 (85 wc)
Median node:    618 wc
Standard dev:   487 wc

Reading time (estimated):
  • Total: 18,600 wc ÷ 225 wpm = 82.7 minutes (all branches combined)
  • Branch A: 29–33 minutes
  • Branch B: 21–26 minutes
  • Branch C: 31–39 minutes
```

### 8. **Show Graph** (optional with --show-graph)

ASCII visualization of word count per node:

```
WORD COUNT PER NODE (Branch A)

NODE-005: ████ (50)
NODE-010: ████████████████████████ (950)
NODE-012: ████████████████████████████████████████████ (2,100)
NODE-015: ███████████████████████████████████████████ (2,300)
NODE-020: ██████████████████ (800)
NODE-025: ███████████ (400)
ENDING:   ███████████████████ (900)

[Each █ = ~50 words]

Shape analysis: Rises to NODE-015 (climax), then descends ✅ Good arc
```

### 9. **Report**

Output `pacing-audit.md` with:
- Branch pacing summary (total words, reading time, status)
- Node length analysis (weight vs actual word count)
- Problem list (info dump, draggy middle, rushed climax, dead zones, inconsistency)
- Reading time comparison vs constitution target
- If `--show-stats`: Full statistics distribution
- If `--show-graph`: ASCII word count visualization per branch

---

## Important Notes

**Word Count Is Not Sacred**: A 300-word emotional climax can work if prose is dense and impactful. A 2,000-word comedy scene can work if it's entertaining. Judge pacing by *reading experience*, not just numbers.

**Emotional Beats Matter More Than Words**: A 500-word scene with 3 major emotional shifts reads faster than a 2,000-word static scene. Word count is a proxy for complexity, not absolute measure.

**Reading Speed Varies**: Non-native readers, accessibility needs (dyslexia, screen readers), and engagement level all affect perceived pacing. 200–250 wpm is average; adjust for target audience.

**Branch Pacing Consistency**: Different branches can have different total word counts (different story paths), but similar-weight scenes should have similar node lengths. Inconsistency signals either intentional weight difference or editor oversight.

**Silent Scenes Count**: Even if a node has minimal prose, if it contains emotional beats, decision points, or mechanical changes, it's not a dead zone. Dead zones are purely transitional with nothing else.

