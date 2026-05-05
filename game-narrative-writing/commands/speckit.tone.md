---
description: Emotional beat progression mapper — validate consistent tone trajectory, detect tonal whiplash, ensure emotional moments feel earned and thematically aligned.
handoffs:
  - label: Review Endings
    agent: speckit.endings
    prompt: After validating emotional progression, verify endings land emotionally.
    send: true
  - label: Check Pacing
    agent: speckit.pacing
    prompt: Cross-check emotional beats against story pacing.
    send: true
---

# speckit.tone

Emotional beat progression mapper — validate tone trajectory is **consistent, earned, and thematically coherent** across the game. Detects tonal whiplash, emotionally hollow moments, and manipulation tactics.

## Tone Principle

**Earned tone** = Emotional moment feels deserved based on prior build-up and character development.  
**Tonal whiplash** = Abrupt shift in emotional temperature (e.g., tragic death followed immediately by comedy without transition).  
**Hollow emotion** = Moment claims emotional weight but hasn't been set up (sudden "I love you" with no prior romantic build).

**Valid tone includes**:
- ✅ Dark humor (maintains dark tone while adding levity)
- ✅ Bittersweet (tragedy + hope coexist)
- ✅ Tonal subversion (intentional, explained shift: e.g., comic relief before tragedy)
- ✅ Silence and space (emotional quiet after climax)

**Invalid tone includes**:
- ❌ Tonal whiplash (abrupt shift with no transition or explanation)
- ❌ Hollow emotion (emotional beat without groundwork)
- ❌ Manipulative tone (guilt-tripping, forced sentiment with no story support)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit entire game's tone progression
- Branch ID (e.g., `BRANCH-A`) — audit tone in one branch only
- `--act [N]` — audit tone progression of a single act only

Optional flags:
- `--strict` — flag any tonal shift as requiring explanation (not just major shifts)
- `--emotional-only` — focus only on high-emotion moments (skip low-key beats)
- `--show-arcs` — display emotional arc visualization for each branch

## Pre-Execution Checks

1. Load `specs/constitution.md`: Tone (§VII), Target Audience, Tense
2. Load `specs/plan.md`: Act structure, node sequence per branch
3. Load all `draft/[ENGINE]/NODE-*.md` files: Extract prose to identify emotional beats
4. Load `specs/themes.md` if present: Thematic resonance expectations
5. Parse node prose for emotional markers (see step 2 below)

## Execution Steps

### 1. **Define Expected Tone Baseline**

From `constitution.md` §VII Tone, identify the game's **baseline emotional temperature**:

**Examples**:
- "Dark fantasy with moments of dark humor and camaraderie"
  - Baseline: Dark, threatening
  - Allowed shifts: Dark → darker, dark → darkly comic
  - Forbidden shifts: Dark → bubbly without transition

- "Coming-of-age drama with humor"
  - Baseline: Hopeful, emotional, sometimes funny
  - Allowed shifts: Hope → heartbreak (natural in coming-of-age), humor → poignancy
  - Forbidden shifts: Humor → horror without setup

- "Noir thriller"
  - Baseline: Cynical, suspicious, morally gray
  - Allowed shifts: Cynical → resigned, cynicism questioned
  - Forbidden shifts: Noir → whimsical

**Report baseline**:
```
Constitution Tone: "Dark fantasy with dark humor"
Baseline temperature: DARK
Allowed tone movements:
  • Dark → Darker (intensity increase, within baseline)
  • Dark → Darkly Comic (tone subversion, maintained baseline)
  • Dark → Quiet (respite, will return to dark)
Forbidden movements:
  • Dark → Heartwarming (contradicts baseline without prior setup)
  • Dark → Comedic Relief (undercuts established tone)
```

### 2. **Identify Emotional Beats**

Read through each node and mark emotional moments:

**High-emotion markers**:
- Sudden change in perspective ("I realized...")
- Relationship shift ("She looked at me differently")
- Stakes revelation ("We have 3 days left")
- Character breaking point ("I can't do this")
- Victory or defeat moment
- Betrayal or trust
- Death or loss
- Reconciliation or separation

**Low-emotion markers**:
- Dialogue / information exchange
- Environmental description
- Puzzle solving / mechanical action
- Travel / transition
- Routine interaction

**Example beat tagging**:
```
NODE-010:
  "You find Marcus bleeding on the steps. His hand reaches for yours.
   'I trusted you,' he whispers."
  → EMOTIONAL BEAT: Betrayal + Loss
  → Temperature: SHARP COLD (trust broken)
  → Build-up so far: Node-005 (Marcus vouched for you)
                    Node-007 (Marcus gave you intel)
  → Earned? YES (3 nodes of relationship building)

NODE-015:
  "The door opens. A puppy bounces out, tail wagging!"
  → EMOTIONAL BEAT: Surprise joy
  → Temperature: SUDDEN WARM
  → Previous node was NODE-014 (serious confrontation)
  → Build-up: None (no hint of pet)
  → Earned? UNCLEAR (needs transition to avoid whiplash)
```

### 3. **Map Emotional Arc Per Branch**

Create a beat-by-beat emotional trajectory:

```
BRANCH A: Help Victor

NODE-005:  Baseline (neutral)           ≈ 0°
NODE-010:  Relationship deepens         ↑ +2° (warm)
NODE-012:  Danger escalates             ↓ -2° (tense)
NODE-015:  Critical choice point        ↓ -3° (climactic tension)
           → Choose to help (compassion)
NODE-020:  Victor escapes safely        ↑ +2° (relief + triumph)
NODE-025:  Meeting Victor's daughter    ↑ +1° (warmth, earned)
ENDING:    "You find peace together"    ↑ +1° (bittersweet closure)

Arc summary:
  Start: Neutral (0°)
  Peak tension: -3° (NODE-015)
  Climax: +2° (NODE-020)
  Resolution: +2° (steady warmth through end)
  Trajectory: Trough-and-rise (tension → relief → earned warmth)
  ✅ EARNED: Each warm beat preceded by stakes/effort

BRANCH B: Betray Victor

NODE-005:  Baseline (neutral)           ≈ 0°
NODE-010:  Relationship deepens         ↑ +2° (warm)
NODE-012:  Danger escalates             ↓ -2° (tense)
NODE-015:  Critical choice point        ↓ -3° (climactic tension)
           → Choose to betray (selfish)
NODE-022:  Victor captured; guilt hits  ↓ -3° (guilt, darkness)
NODE-025:  Regret eats at you           ↓ -2° (persistent sorrow)
ENDING:    "You escape alone"           ↓ -1° (hollow victory)

Arc summary:
  Start: Neutral (0°)
  Peak tension: -3° (NODE-015, choice point)
  Climax: -3° (NODE-022, consequences)
  Resolution: -1° (persistent unease)
  Trajectory: Descent into darkness (escalating moral consequences)
  ✅ EARNED: Darkness earned through betrayal choice

COMPARISON: Branch A (redemptive), Branch B (tragic)
Tonal consistency within each branch: ✅ YES
Tonal coherence across branches: ✅ YES (different paths, consistent principle)
```

### 4. **Detect Tone Violations**

#### 🔴 **VIOLATION: Tonal Whiplash**
Abrupt emotional shift without transition or explanation.

```
NODE-020: "Marcus bleeds out in your arms. You've lost him forever."
          → TEMPERATURE: -4° (grief, darkness)

NODE-021: "Days later, you meet a comedian at the tavern.
          He tells terrible jokes. You both laugh hard."
          → TEMPERATURE: +3° (light, comedy)
          → SHIFT: -4° → +3° = 7° SWING

Problem: No transition between grief and laughter
Is there a time skip? Yes (days later)
Is grief processed? Not addressed directly
Is the tone shift intentional? Unclear

Status: ⚠️  QUESTIONABLE
Flag: Does the time gap + character resilience justify this shift?
      Or is this tonally jarring to readers who are still in grief?
```

**Report**:
```
NODE-020 → NODE-021: Tonal Shift Detected
  From: Grief / Darkness (-4°)
  To: Comedy / Light (+3°)
  Shift magnitude: -7° (LARGE)
  Transition: Days pass (time skip provided)
  Status: ⚠️  REVIEW NEEDED
  Question: Is it emotionally jarring or narratively natural?
  
Recommendation: Add one line in NODE-021 acknowledging grief before comedy
  ("The grief still weighs, but maybe laughter helps" or similar)
  This softens the tonal shift and makes it feel earned.
```

#### 🟡 **VIOLATION: Hollow Emotion**
Emotional beat lacks groundwork; feels manipulative.

```
NODE-025: "I love you."
          
Prior build-up: NONE
              NODE-010: Met character
              NODE-015: Basic conversation
              NODE-020: One collaborative task
              NODE-025: "I love you"
              
Problem: No romantic build-up; sudden emotional claim
         Character hasn't expressed affection before
         No vulnerable moments with this character

Status: ❌ HOLLOW
Flag: Emotional manipulation; readers won't believe the love
      
Recommendation: Add at least ONE moment of romantic tension/vulnerability
              before the "I love you" declaration
              Examples:
              • NODE-023: "Your hand finds mine"
              • NODE-024: "I've never felt this way about anyone"
              Then NODE-025: "I love you" (now earned)
```

#### 🟠 **VIOLATION: Manipulative Tone**
Emotional beat designed to guilt or shame player without story justification.

```
NODE-020: "You made the wrong choice. Marcus died because of you.
          The city will never forgive you.
          Everything is your fault."
          
Context: Player chose A (seemingly neutral choice)
         Marcus was supposed to be safe based on prior dialogue
         No indication this choice would cause death
         
Problem: Guilt-tripping without fair warning
         Player made reasonable choice with bad outcome
         Game is shaming player, not through story, but through narrator voice
         
Status: ❌ MANIPULATIVE
Flag: Feels punitive rather than narrative-driven
      
Recommendation: Either:
  1. Foreshadow this consequence earlier (Marion hints at danger)
  2. Change outcomes so choice feels more obviously risky
  3. Remove shame language; use neutral tone ("Marcus fell")
     Let players draw own conclusions instead of being told they're "wrong"
```

### 5. **Check Thematic Tone Alignment**

Does emotional progression serve the theme?

```
Theme: "Love survives conflict"

Emotional arc:
  NODE-010: Characters meet (hope introduced)      ✅ Thematic
  NODE-015: Conflict erupts (relationship tested)  ✅ Thematic
  NODE-020: Characters separate (love tested)      ✅ Thematic
  NODE-025: Reunion (love survives)                ✅ Thematic
  ENDING: Together despite odds                    ✅ Thematic

Arc conclusion: Every emotional beat reinforces central theme
Status: ✅ EXCELLENT ALIGNMENT

---

Theme: "Power corrupts"

Emotional arc:
  NODE-010: Character gains power (excitement)     ✅ Thematic setup
  NODE-015: Character uses power selfishly (horror) ✅ Thematic warning
  NODE-020: Consequence appears (tragic)           ✅ Thematic payoff
  NODE-025: Character is alone (sorrow)            ✅ Thematic
  ENDING: Character has everything but lost everyone  ✅ Thematic
  
Arc conclusion: Emotional progression perfectly illustrates theme
Status: ✅ EXCELLENT ALIGNMENT
```

### 6. **Generate Emotional Arc Report**

Create `specs/tone-audit.md`:

```markdown
## Emotional Tone Audit

**Game**: [NAME]
**Constitution Tone**: "Dark fantasy with dark humor"
**Date**: [ISO]

### Branch Emotional Arcs

**BRANCH A: Redemption Path**

| Node | Moment | Temp | Build-up | Earned? | Status |
|------|--------|------|----------|---------|--------|
| NODE-005 | Baseline | 0° | - | - | ✅ |
| NODE-010 | Relationship | +2° | NODE-005 | ✅ | ✅ |
| NODE-015 | Choice | -3° | NODE-010,012 | ✅ | ✅ |
| NODE-020 | Victory | +2° | NODE-015 choice | ✅ | ✅ |
| NODE-025 | Warmth | +1° | NODE-020 | ✅ | ✅ |
| END | Closure | +2° | Whole arc | ✅ | ✅ |

Tone trajectory: Earned trough-and-rise (tension → earned relief)
Thematic alignment: ✅ Matches "love survives"
Overall: ✅ PASS

**BRANCH B: Betrayal Path**

[Similar table showing dark descent]

### Violations

**🔴 Tonal Whiplash** (1):
- NODE-020 → NODE-021: Shift from grief (-4°) to comedy (+3°) without transition
  Fix: Add acknowledgment of grief before comedy

**🟡 Hollow Emotion** (0):
- None found

**🟠 Manipulative** (0):
- None found

### Recommendations

Priority 1: Add transition in NODE-021 to soften tonal shift
Priority 2: Consider extending emotional quiet after NODE-020 climax

### Thematic Alignment

All branches maintain thematic coherence with constitution tone
Emotional arcs actively reinforce central themes
Status: ✅ EXCELLENT
```

### 7. **Show Arcs** (optional with --show-arcs)

Visual representation of emotional temperature across branch:

```
BRANCH A (Redemption)
Temperature arc:
  0°  ↗ +2°  ↘ -3°  ↗ +2°  ↗ +1°  ↗ +2°
      N-005  N-010  N-015  N-020  N-025  END
      
  Shape: V-shape trough (tension midpoint, relief at end)
  Build: Steady, predictable escalation
  Payoff: Earned warmth through effort
  Status: ✅ Satisfying arc

BRANCH B (Betrayal)
Temperature arc:
  0°  ↗ +2°  ↘ -3°  ↘ -3°  ↘ -2°  ↘ -1°
      N-005  N-010  N-015  N-022  N-025  END
      
  Shape: Sustained descent (consequences deepen)
  Build: Choices lead to escalating darkness
  Payoff: Hollow victory (earned sorrow)
  Status: ✅ Thematically consistent tragedy
```

### 8. **Report**

Output `tone-audit.md` with:
- Baseline tone definition (from constitution)
- Emotional arc table for each branch
- Violation list (whiplash, hollow, manipulative)
- Thematic alignment analysis
- If `--show-arcs`: Visual temperature charts per branch
- If `--strict`: All detected tone shifts flagged for review

---

## Important Notes

**Tone Shifts Are Not Inherently Bad**: Tonal variation (dark humor, bittersweet) is legitimate and often enhances narrative. The issue is *abruptness* and *lack of justification*.

**Context Matters**: A comedy beat after tragedy can work if:
1. Time has passed (processing), OR
2. Character actively chooses humor as coping, OR
3. Dark humor fits baseline tone, OR
4. Transition beat softens the shift

**Thematic Tone**: If your game has a theme ("love survives," "power corrupts"), emotional beats should generally reinforce it. Tonal anomalies that serve theme are OK; random tonal anomalies are usually problems.

**Audience Matters**: Target audience affects tone tolerance. Middle-grade audiences need more stable tone; adult audiences accept more tonal variation. Check constitution.md §VII Target Audience.

**Player Agency + Tone**: Different branches can have different emotional arcs (one optimistic, one tragic). This is fine—it's the result of player choice. Just ensure each branch is internally coherent.

