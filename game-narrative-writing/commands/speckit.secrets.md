---
description: Secret content tracker — map achievements, hidden content, easter eggs. Verify all secrets are discoverable, reachable, and properly documented.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: After mapping secrets, verify secret choices have meaningful consequences.
    send: true
  - label: Revise Secrets
    agent: speckit.revise
    prompt: Some secrets need better discovery hints. Please add foreshadowing.
    send: true
---

# speckit.secrets

Secret content tracker — map **achievements, hidden content, easter eggs, secret endings**. Verify all secrets are discoverable, reachable, properly documented, and balanced in unlock difficulty.

## Secrets Principle

**Good secrets** = Discoverable for attentive players; optional (not required); rewarding to find; properly documented in external guide if needed.

**Bad secrets include**:
- ❌ Impossible to discover (no hint anywhere)
- ❌ Inaccessible by design (requires code modification)
- ❌ Required for "real" ending (frustrates players who miss them)
- ❌ Undocumented (players don't know they exist)
- ❌ Unfair locks (achievement requires frame-perfect timing)

**Valid secrets include**:
- ✅ Hinted but non-obvious (attentive player might find)
- ✅ Optional alternate content (doesn't gate main story)
- ✅ Multiple unlock paths (can reach same secret via different choices)
- ✅ Proportional reward (difficulty matches value)
- ✅ Discoverable in new game+ (if design supports replay)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — map all secrets (achievements, hidden content, easter eggs)
- `--achievement` — list only achievements
- `--hidden-content` — list only hidden scenes/endings
- `--easter-eggs` — list only easter eggs and references
- `--secret [SECRET_ID]` — analyze one secret only

Optional flags:
- `--reachability` — verify each secret can be unlocked
- `--hints-check` — verify each secret has clue to unlock
- `--difficulty-map` — categorize secrets by unlock difficulty
- `--show-unlock-paths` — display all ways to unlock each secret

## Pre-Execution Checks

1. Load `specs/secrets-template.md` or extract from spec.md (Secret Registry)
2. Load `specs/plan.md`: Branch structure for reachability
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Load `specs/variables.md`: Variables that unlock secrets
5. Parse for conditions that trigger hidden content

## Execution Steps

### 1. **Define Secret Registry**

From template or spec, categorize all secrets:

```
SECRET REGISTRY:

ACHIEVEMENTS:
  ACH-001: "Redeemed Victor"
    Unlock: Reach Ending A (Victor escaped + relationship_marcus > 75)
    Reward: Achievement badge
    Description: "Helped Victor escape and earned Marcus's respect"
  
  ACH-002: "Betrayer"
    Unlock: Reach Ending B (Victor captured)
    Reward: Achievement badge
    Description: "Betrayed Victor to the militia"
  
  ACH-003: "Speedrunner"
    Unlock: Complete game in <20 minutes
    Reward: Achievement badge
    Description: "Completed the game in record time"

HIDDEN CONTENT (scenes):
  HID-001: "Victor's Letter"
    Unlock: Ending A + check specific location (NODE-030 secret passage)
    Reward: Additional scene (1,000 words)
    Description: "Discover a letter Victor left for you"
    Gating: Optional; doesn't affect main ending
  
  HID-002: "Marcus Betrayal"
    Unlock: Ending B + high militia_influence
    Reward: Alternate scene NODE-025 (different dialogue)
    Description: "Marcus confronts you about your betrayal"

EASTER EGGS:
  EGG-001: "Hidden NPC"
    Unlock: Find specific item in NODE-020, examine it
    Reward: Cameo appearance of developer
    Description: "Developer appears as background NPC"
  
  EGG-002: "Tribute Reference"
    Unlock: Name your character after [AUTHOR]
    Reward: Dialogue reference
    Description: "NPCs recognize your name (developer tribute)"
  
  EGG-003: "Speed Run Reference"
    Unlock: Visit specific nodes in order NODE-005 → 010 → 015 → 020
    Reward: Easter egg dialogue
    Description: "NPC acknowledges your 'efficiency'"

SECRET ENDINGS:
  END-SEC-001: "True Ending"
    Unlock: Reach Ending A + unlock HID-001 + find secret item
    Reward: Final alternate ending (3,000 words)
    Description: "Discover what really happened"
    Gating: Requires multiple secrets
```

### 2. **Analyze Secret Discoverability**

Rate how easy each secret is to find:

```
DISCOVERABILITY SCALE:

1. OBVIOUS (Explicitly mentioned)
   → Player will find it
   
2. CLEAR (Strong hint provided)
   → Attentive player will find it
   
3. MODERATE (Subtle hint exists)
   → Player might find it on 2nd playthrough
   
4. OBSCURE (Requires experimentation)
   → Player must explore to find
   
5. IMPOSSIBLE (No hint)
   → Requires guide or luck

Example secrets:

ACH-001 (Redeemed Victor):
  Hint: Constitution describes "Redemption ending" as goal
  Discoverability: 2 (CLEAR)
  Expected finder rate: 70%+ of players

HID-001 (Victor's Letter):
  Location: NODE-030 secret passage (not labeled)
  Hint: Marcus mentions "checking the old safehouse"
  Discoverability: 3 (MODERATE)
  Expected finder rate: 30–40% of attentive players

EGG-002 (Name Reference):
  Unlock: Name character "Stephen King"
  Hint: None (pure Easter egg)
  Discoverability: 5 (IMPOSSIBLE without guide)
  Expected finder rate: 1–5% (accidental)
```

### 3. **Verify Reachability**

Trace whether each secret can actually be unlocked:

```
SECRET: HID-001 "Victor's Letter"

Unlock condition: 
  Ending A (Help Victor) 
  + relationship_marcus > 75
  + Discover secret passage NODE-030

Reachability analysis:

Path to Ending A:
  NODE-010: Help Victor ✅ (choice available)
  NODE-015: Violent approach ✅ (choice available)
  NODE-020: Execute escape ✅ (NODE exists)
  NODE-025: Victory achieved ✅ (NODE exists)
  Ending A reached ✅ POSSIBLE

Path to relationship_marcus > 75:
  NODE-010: Help Victor (+15) → 65 total
  NODE-015: No change → 65 total
  NODE-020: Execute perfectly (+10) → 75 total
  CHECK: relationship_marcus = 75 ✅ REACHED

Path to NODE-030 secret passage:
  NODE-025 → NODE-030 ✅ NODE exists
  BUT: Passage marked as [SECRET - no description]
  Question: Is passage actually discoverable in-game?
  
Investigation:
  • NODE-030 prose: "The safe house is empty."
  • No indication of passage
  • No mechanic to "examine walls"
  • No NPC dialogue mentions it
  
Verdict: 🔴 UNREACHABLE (hidden too well; player can't find)

Fix: Either:
  1. Add passage hint in NODE-030 prose
  2. Add examine mechanic (if game supports it)
  3. Have Marcus mention it at NODE-025
  4. Mark as 6/10 difficulty (requires guide)
```

### 4. **Detect Secret Problems**

#### 🔴 **PROBLEM: Impossible to Discover**
Secret has no hint; requires blind luck or guide.

```
EGG-001: "Hidden NPC"
  Unlock: Find NPC in NODE-020 crowd
  Description: Examine 50 background NPCs to find developer cameo
  
Problem: 
  • No hint that Easter egg exists
  • No indication which NPC is special
  • Requires guide or exhaustive testing
  • Player won't discover organically
  
Status: 🔴 IMPOSSIBLE (requires guide)

Assessment: Is this acceptable?
  ✅ YES if: You've documented it in FAQ/guide
  ❌ NO if: You expect players to find it themselves
```

#### 🟡 **PROBLEM: Inaccessible by Design**
Secret requires mechanical action game doesn't support, or is locked behind unwinnable state.

```
HID-002: "Marcus Betrayal" alternate scene

Unlock: Ending B + relationship_marcus > 50

But trace the variables:
  NODE-010: Betray Victor → relationship_marcus = 35
  NODE-016: Continued betrayal → relationship_marcus = 30
  NODE-021: Final betrayal → relationship_marcus = 25
  
Final state: relationship_marcus = 25

Unlock requires: relationship_marcus > 50
Final state is: 25

Problem: Impossible to satisfy both conditions
         To reach Ending B, you must betray (lowering relationship)
         To unlock secret, you need high relationship
         These are contradictory
         
Status: 🟡 INACCESSIBLE (contradictory conditions)

Fix: Either:
  1. Change unlock: Ending B + relationship_marcus < 50 (matches betrayal)
  2. Add alternate path: Ending B + high militia_influence (different variable)
  3. Allow neutral path to Ending B (don't lower relationship)
```

#### 🟠 **PROBLEM: Required for Main Content**
Secret is gated behind obscure unlock; players think they're missing "real" ending.

```
END-SEC-001: "True Ending" secret

Description: "Real story is revealed only in True Ending"
Unlock: Reach Ending A + unlock 5 hidden scenes + find 3 collectibles

Problem:
  • Players reach Ending A (think they're done)
  • Realize there's a "True Ending" (feels incomplete)
  • Must unlock 5 hidden scenes (significant replay burden)
  • Feels mandatory, not optional
  
Status: 🟠 GATING ISSUE

Question: Is this design intentional?
  ✅ YES if: Game is designed as collectathon; players expect this
  ✅ YES if: Documentation clearly indicates "True Ending is bonus"
  ❌ NO if: Players think Ending A is "the" ending and feel cheated

Fix: Either:
  1. Clearly mark in opening: "There are 3+ endings; collect secrets to unlock all"
  2. Make "True Ending" fully optional (doesn't invalidate Ending A)
  3. Reduce unlock requirements (make it less burdensome)
```

#### 💨 **PROBLEM: Secret Not Documented**
Developer knows about secret, but hasn't documented it for guide/wiki.

```
Secret: "Alternative NODE-020 scene if you find hidden item"

Status:
  • Secret exists in code
  • Discoverable by player (with effort)
  • BUT: Not in FAQ, guide, or achievement list
  • Player doesn't know it exists even after finding it
  
Impact:
  • Player thinks they found a bug
  • Posts about it online ("Is this intentional?")
  • Community speculates on meaning
  • Developer confusion: "Yes, that's a secret!"
  
Status: 💨 UNDOCUMENTED

Fix: Add to FAQ or create "Secrets & Easter Eggs" wiki page
```

#### 🟢 **PROBLEM: Unfair Unlock**
Secret requires mechanical execution that's frustrating or frame-perfect.

```
ACH-003: "Speedrunner"
  Unlock: Complete game in <20 minutes

Implementation:
  • Requires skipping all dialogue
  • Mandatory cinematics total 2 minutes
  • Combat encounters have no skip
  • Result: Actual speedrun requires ~24 minutes
  • Speedrunner achievement: Impossible with current design
  
Status: 🟢 UNFAIR (requires external tools or code modification)

Fix: Either:
  1. Adjust timer: <25 minutes (realistic with skips)
  2. Add speedrun mode (skip cutscenes)
  3. Remove if achievement isn't core to design
```

### 5. **Analyze Unlock Paths**

Map multiple ways to reach same secret:

```
SECRET: HID-001 "Victor's Letter"

Unlock path 1 (Primary):
  NODE-010: Help Victor
  → NODE-015: Violent approach
  → NODE-020: Perfect execution
  → Ending A (relationship > 75)
  → NODE-030: Find secret passage
  
Unlock path 2 (Alternate):
  NODE-010: Help Victor
  → NODE-015: Stealth approach
  → NODE-020: Perfect execution
  → Ending A (relationship > 75)
  → NODE-030: Find secret passage
  
Unlock path 3 (New Game+):
  (If game supports carry-over)
  Second playthrough: Skip to NODE-025
  → Ending A (relationship automatically high)
  → NODE-030: Find secret passage

Analysis:
  • 2–3 discovery paths (good)
  • All require Ending A (single main path)
  • Secret passage is bottleneck (same location every time)
  
Accessibility: MODERATE (not too easy, not impossible)
```

### 6. **Generate Secrets Audit Report**

Create `specs/secrets-audit.md`:

```markdown
## Secret Content Audit

**Game**: [NAME]
**Date**: [ISO]

### Secret Inventory

| Secret | Type | Unlock Difficulty | Discoverable? | Reachable? | Documented? | Status |
|--------|------|------------------|---------------|-----------|------------|--------|
| ACH-001 | Achievement | Easy | ✅ Clear | ✅ Yes | ✅ Yes | ✅ Pass |
| HID-001 | Hidden Scene | Hard | ⚠️ Moderate | ❌ No | ✅ Yes | ❌ Fail |
| EGG-002 | Easter Egg | Impossible | ❌ Impossible | ✅ Yes | ❌ No | ⚠️ Warn |
| END-SEC-001 | Secret Ending | Very Hard | ⚠️ Moderate | ✅ Yes | ⚠️ Partial | ⚠️ Warn |

### Discoverability Analysis

**Tier 1 (Obvious — 70%+ find)**:
- ACH-001: Clear from marketing/constitution

**Tier 2 (Clear — 40–70% find)**:
- ACH-002: Logical consequence of betrayal

**Tier 3 (Moderate — 20–40% find)**:
- HID-001: Requires exploration; moderate hint
- HID-002: Requires specific variable combo

**Tier 4 (Obscure — 5–20% find)**:
- END-SEC-001: Requires multiple unlocks; documented but complex

**Tier 5 (Impossible — <5% find)**:
- EGG-002: No hint; pure Easter egg

### Reachability Issues

**🔴 Unreachable** (1):
- HID-001 secret passage: No in-game hint or mechanic to find
  Fix: Add passage hint in NODE-030 prose

**🟡 Contradictory** (1):
- HID-002: Unlock requires relationship > 50, but Ending B path leads to 25
  Fix: Change unlock condition to relationship < 50

**✅ Reachable** (3):
- ACH-001, ACH-002, EGG-002 all reachable with conditions

### Documentation

**Well documented**:
- ACH-001, ACH-002, HID-001 (in FAQ)

**Partially documented**:
- END-SEC-001 (in spec.md but not README)

**Undocumented**:
- EGG-002 (No documentation; pure Easter egg)

### Recommendations

**Priority 1 (Fix before release)**:
1. Add discovery hint for HID-001 secret passage
2. Fix contradictory unlock for HID-002 (change condition)

**Priority 2 (Enhancement)**:
1. Add EGG-002 to FAQ (mark as secret Easter egg)
2. Clarify in opening that END-SEC-001 is optional "True Ending"

**Priority 3 (Balance)**:
1. Consider adding 1–2 more easy secrets (Tier 1–2)
   Currently top-heavy on hard secrets

### Secret Content Summary

- Total secrets: 6 (2 achievements, 2 hidden scenes, 1 Easter egg, 1 secret ending)
- Average difficulty: Hard (mostly Tier 3–4)
- Documentation: 67% documented (4/6)
- Reachability: 67% reachable without fixes (4/6)

Status: ⚠️ GOOD baseline; fix 2 reachability issues before release
```

### 7. **Show Unlock Paths** (optional with --show-unlock-paths)

Display all ways to discover each secret:

```
SECRET: HID-001 "Victor's Letter"

Primary discovery path:
  1. Choose "Help Victor" (NODE-010)
  2. Choose Violent approach (NODE-015)
  3. Execute perfectly (NODE-020 checks)
  4. Reach Ending A (NODE-025)
  5. Examine secret passage (NODE-030)
  
Alternate discovery path:
  1. Choose "Help Victor" (NODE-010)
  2. Choose Stealth approach (NODE-015)
  3. Execute perfectly (NODE-020 checks)
  4. Reach Ending A (NODE-025)
  5. Examine secret passage (NODE-030)

New Game+ path (if supported):
  1. Start 2nd playthrough with carry-over
  2. Jump to NODE-025 (relationship pre-loaded as high)
  3. Go to NODE-030
  4. Examine secret passage

All paths converge at: NODE-030 secret passage discovery
Estimated player who find: 15–25% (requires multiple correct choices)
```

### 8. **Difficulty Map** (optional with --difficulty-map)

Categorize secrets by unlock complexity:

```
DIFFICULTY TIER BREAKDOWN:

Tier 1 (Easy — <5 minutes replay time):
  ACH-001: "Redeemed Victor" — Natural consequence of main path

Tier 2 (Moderate — 5–15 minutes):
  ACH-002: "Betrayer" — Alternate main ending
  HID-002: "Marcus Betrayal" — Specific variable combo

Tier 3 (Hard — 15–45 minutes):
  HID-001: "Victor's Letter" — Requires exploration + multiple choices
  EGG-002: "Name Reference" — Requires custom naming

Tier 4 (Very Hard — 45+ minutes):
  END-SEC-001: "True Ending" — Requires 5+ hidden scene unlocks
  ACH-003: "Speedrunner" — Requires optimized playthrough

Tier 5 (Extreme — Requires guide):
  None currently

Difficulty distribution:
  • Tier 1–2 (Easy): 50% of secrets ✅ Good (accessible to casual players)
  • Tier 3–4 (Hard): 50% of secrets ✅ Good (content for completionists)
  • Tier 5 (Impossible): 0% ✅ Good (all secrets are discoverable)
```

### 9. **Report**

Output `secrets-audit.md` with:
- Secret inventory (all achievements, hidden content, easter eggs)
- Discoverability analysis (tier by findability)
- Reachability verification (can each secret be unlocked?)
- Unlock path analysis (how many ways to find?)
- Documentation status (which secrets are documented?)
- If `--show-unlock-paths`: Full unlock path trees per secret
- If `--difficulty-map`: Difficulty tier breakdown

---

## Important Notes

**Balance Discoverability**: Mix of obvious and obscure secrets keeps players engaged. All-easy is boring; all-impossible is frustrating.

**Document Everything**: Even if secret is meant to be hidden, document it in FAQ/guide. Players deserve to know what exists.

**Test Secret Unlock Paths**: It's easy to accidentally make secrets unreachable. Trace every unlock condition through your variables and branches.

**Easter Eggs Are Different**: Easter eggs can be harder to find since they're fun surprises. Achievements and hidden content should be more discoverable (or have hints).

**Optional Is Key**: Secrets should never gate core story or required endings. If secret is needed for "real" ending, make that explicit in opening warning.

**New Game+ Extends Replayability**: If designing for replay, secrets unlocked in later playthroughs extend the "want to play again" factor significantly.

