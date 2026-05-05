---
description: Information gap mapper — visualize what player knows vs what each NPC knows. Detects blind spots, ensures player has enough agency, identifies unrealistic NPC knowledge.
handoffs:
  - label: Check Continuity
    agent: speckit.continuity
    prompt: After analyzing information gaps, verify variable consistency across nodes.
    send: true
  - label: Revise Dialogue
    agent: speckit.revise
    prompt: Some NPCs know too much/too little. Please adjust dialogue and information revelation.
    send: true
---

# speckit.asymmetry

Information gap mapper — visualize **what player knows vs. what each NPC/faction knows**. Detects blind spots, unrealistic knowledge, and player agency conflicts.

## Information Asymmetry Principle

**Healthy asymmetry** = Player and NPCs have different (but plausible) information → creates tension, enables deception, gives player advantage/disadvantage.

**Unhealthy asymmetry includes**:
- ❌ Player knows too much (NPCs clueless; game feels fake)
- ❌ Player knows too little (can't make informed decisions; unfair)
- ❌ NPC knows future information (unrealistic; breaks immersion)
- ❌ Asymmetry is accidental (should be intentional story design)

**Valid asymmetry includes**:
- ✅ Player unaware of NPC's past (NPC has secrets)
- ✅ Player aware of danger; NPC unaware (player can warn or exploit)
- ✅ Player missing piece of puzzle (must ask NPC or find evidence)
- ✅ Faction has specialized knowledge (militia knows patrol routes)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — map information gaps for entire game
- NPC name (e.g., `Marcus`) — analyze one NPC's knowledge
- `--faction [NAME]` — analyze information known to entire faction
- `--branch [BRANCH_ID]` — analyze asymmetry in one branch only

Optional flags:
- `--strict` — flag all asymmetries for review (not just major)
- `--player-only` — show only player's knowledge (what PC knows)
- `--npc-only` — show only NPC knowledge (what NPCs know)
- `--show-gaps` — visualize information gaps with ASCII charts
- `--check-realism` — flag NPC knowledge that's narratively implausible

## Pre-Execution Checks

1. Load `specs/plan.md`: Node sequence, branches, key decision points
2. Load `specs/characters.md`: NPC backgrounds, motivations, access to information
3. Load all `draft/[ENGINE]/NODE-*.md` files
4. Load `specs/variables.md`: What information is tracked (flags, stat changes)
5. Extract dialogue and stage direction mentioning information revelation

## Execution Steps

### 1. **Define Information Categories**

Map types of information in the game:

```
Information categories (examples):

PLOT INFORMATION:
  • "Victor is militia spy"
  • "Sera was kidnapped"
  • "Marcus knows where treasure is"

WORLD INFORMATION:
  • "City is under siege"
  • "Borders are closed"
  • "Plague is spreading"

CHARACTER INFORMATION:
  • "Sera has a daughter"
  • "Marcus was betrayed by militia"
  • "Victor has access to safe house"

SECRET INFORMATION:
  • "Player has hidden alliance with faction A"
  • "NPC is double agent"
  • "Gold is hidden in church"

MECHANICAL INFORMATION:
  • "Choices affect ending"
  • "Some NPCs are tracking you"
  • "Certain locations are dangerous"
```

### 2. **Track Information Per Character**

For each information piece, note who knows it when:

```
INFO: "Victor is militia spy"

Who knows when:
  • Victor: Knows from beginning (it's his identity)
  • Marcus: Knows at NODE-025 (reveals to player)
  • Sera: Knows at NODE-030 (hears from Marcus)
  • Player: Knows at NODE-025 (revelation scene)
  • City militia: Always knew (Victor is their agent)

Timeline:
  NODE-025: Player learns (Marcus reveals)
           Marcus knows (he's been watching)
  NODE-030: Sera learns (Marcus tells her)
           Victor might not want Sera knowing (conflict?)

Asymmetry check:
  • Before NODE-025: Player doesn't know; Marcus & Victor do
    Status: ✅ HEALTHY (creates tension)
  
  • NODE-025: All three know
    Status: ✅ INFORMATION REVEALED
  
  • If Victor tried to hide this after NODE-025:
    Status: ❌ UNREALISTIC (Sera would tell him Marcus told her)
```

### 3. **Map Player Knowledge**

From player POV, track what PC knows at each node:

```
Player Knowledge Timeline (Branch A):

NODE-005:  [ ] Victor is militia spy
           [ ] Sera was kidnapped
           [ ] Marcus is trustworthy
           [X] Player is in danger
           [X] City is under siege
           Status: Low information

NODE-010:  [X] Victor is militia spy (revelation)
           [ ] Sera was kidnapped
           [ ] Marcus is trustworthy
           [X] Player is in danger
           [X] City is under siege
           Status: Plot advancing

NODE-015:  [X] Victor is militia spy
           [X] Sera was kidnapped (from NPC dialogue)
           [X] Marcus helped kidnapping (deduction)
           [X] Player is in danger
           [X] City is under siege
           Status: Full context for choice

Choice NODE-015: "Help Sera" / "Flee"
           Both choices are informed (player has context)
           Status: ✅ GOOD AGENCY

NODE-020:  [X] All plot points
           [X] Consequences of choice are clear
           Status: Player can predict outcomes
```

### 4. **Map NPC Knowledge Per Character**

What does each NPC know?

```
MARCUS (Detective):

NODE-005:  [X] Victor is militia spy (job knowledge)
           [X] Sera was kidnapped (investigation)
           [ ] Player is involved (doesn't know PC yet)
           [X] City is under siege (public knowledge)
           Status: High information (detective role)

NODE-010:  [X] Victor is militia spy
           [X] Sera was kidnapped
           [X] Player is involved (has met PC)
           [ ] Where Sera is (investigating)
           Status: Semi-informed

NODE-025:  [X] Victor is militia spy
           [X] Sera was kidnapped
           [X] Player is involved
           [X] Where Sera is (found her)
           Status: Fully informed

---

SERA (Kidnapped):

NODE-005:  [ ] Victor is militia spy
           [X] She was kidnapped
           [ ] Why (doesn't know yet)
           [ ] Who by (guards are unknown)
           Status: Imprisoned, limited info

NODE-020:  [ ] Victor is militia spy
           [X] She was kidnapped
           [X] Why (militia wants info from PC)
           [X] Who by (guards mentioned militia)
           Status: Partial understanding

NODE-025:  [X] Victor is militia spy (PC tells her)
           [X] She was kidnapped
           [X] Why
           [X] Who by
           Status: Fully informed
```

### 5. **Detect Asymmetry Problems**

#### 🔴 **PROBLEM: Player Knows Too Much**
Player has information that should be NPC-exclusive.

```
Situation:
  Victor: Militia spy (secret)
  Marcus: Investigating Victor (doesn't know he's militia)
  Player: Hears rumor in tavern (NODE-012)
          Now knows Victor is militia
          Marcus still investigating
  
At NODE-015 (choice point):
  Player can tell Marcus "Victor is militia"
  But how did player discover this before detective?
  
Problem: Player jumped ahead of NPC investigation
         Breaks realism (random tavern rumor > detective work?)
         
Status: 🔴 UNREALISTIC

Question: Should tavern rumor be planted by someone?
          Should player find evidence, not hear rumor?
          Should Marcus already know by NODE-015?

Fix options:
  1. Remove tavern rumor; player finds evidence instead
  2. Have Marcus already know by NODE-015
  3. Have NPC who told player be revealed as insider
```

#### 🟡 **PROBLEM: Player Knows Too Little**
Player lacks information needed to make informed choice.

```
Choice NODE-015: "Help Sera or Flee"

Player knowledge:
  [ ] Where Sera is (can't plan rescue)
  [ ] Who kidnapped her (can't predict danger)
  [ ] Why she was kidnapped (can't weigh consequences)
  [ ] Whether rescue is possible (can't assess odds)

Result: Player makes choice blindly
        Feels unfair; choice seems random

Status: 🟡 UNFAIR AGENCY

Question: Should player know more before choice?
          Should choice point be earlier (gather info first)?

Fix options:
  1. Move choice to after NODE-020 (info gathering phase)
  2. Add optional dialogue to learn Sera's location (NODE-013)
  3. Have Marcus hint at kidnapping details (NODE-014)
  4. Give player hint about Marcus's trustworthiness before choice
```

#### 🔵 **PROBLEM: NPC Knows Future**
NPC reacts to information before it's revealed.

```
NODE-015: Player encounters Victor
          Victor: "I know what you're planning to do for Sera."
          
But player hasn't told anyone about Sera yet!
How does Victor know?

Possibilities:
  ✅ VALID: Victor is spy (faction told him)
  ✅ VALID: Victor follows player (guessed from behavior)
  ❌ INVALID: Victor knows the script (NPC omniscience)

Analysis:
  If Victor says this at NODE-015 before revealing militia connection:
    Status: ❌ UNREALISTIC (breaks immersion)
  
  If Victor says this at NODE-025 (after revealing as spy):
    Status: ✅ REALISTIC (spy network told him)

Fix: Move Victor's line to after his reveal, or add explanation
```

#### 🟢 **PROBLEM: Intentional Asymmetry Not Tracked**
Important information gap exists but isn't being used narratively.

```
Example:
  Player knows: Sera was kidnapped by militia
  Marcus knows: Sera was kidnapped, suspects Victor is involved
  Victor knows: Sera was kidnapped BY HIM (ordered it)
  
  But in game:
    • Player never gets chance to use info strategically
    • Marcus's investigation never leads to confrontation
    • Victor never has to defend his role
  
  Status: 🟢 ASYMMETRY NOT USED

Question: Is this asymmetry deliberate setup for later use?
          Or did it get forgotten?

Fix: Either pay off the asymmetry (create scene where it matters)
     Or remove the extra knowledge layer (simplify)
```

### 6. **Generate Information Gap Report**

Create `specs/asymmetry-audit.md`:

```markdown
## Information Asymmetry Audit

**Game**: [NAME]
**Date**: [ISO]

### Information Gap Chart

| Information | Player | Marcus | Victor | Sera | Status |
|-------------|--------|--------|--------|------|--------|
| Victor is spy | NODE-025 | NODE-005 | Always | NODE-030 | ✅ Healthy gap |
| Sera kidnapped | NODE-015 | NODE-005 | Always | Always | ✅ Healthy gap |
| Location: Sera | NODE-020 | NODE-020 | Always | Always | ✅ Timing OK |
| Motivation: kidnap | NODE-020 | NODE-020 | Always | NODE-025 | ✅ Healthy gap |
| Player's choice | NODE-015 | NODE-015 | NODE-025 | NODE-030 | ⚠️ Asymmetry unused |

### Asymmetry Analysis

**Healthy Gaps** (3):
- Victor's spy status: Player unaware until NODE-025; creates tension ✅
- Sera's kidnapping: Player deduces gradually; good pacing ✅
- Motivation details: Player learns through dialogue; natural ✅

**Problem Areas** (1):
- Sera/Marcus know each other before NODE-025, but dynamic never explored

**Unrealistic Gaps** (0):
- No NPC has impossible future knowledge

**Unused Asymmetries** (1):
- Player could use "Victor is spy" info strategically, but choice is already made

### Recommendations

**Priority 1**: 
- NODE-015 choice needs more player information (add info-gathering scene before)

**Priority 2**:
- Consider revealing asymmetry (Sera/Marcus knowing each other) earlier
- Create scene where Victor's spy status matters to player strategy
```

### 7. **Show Gaps** (optional with --show-gaps)

ASCII visualization of information asymmetry:

```
INFORMATION: "Victor is militia spy"

Timeline:
  NODE-005: ░░░░░░░░░░ VICTOR KNOWS 100% (identity)
            ░░░░░░░░░░ MILITIA KNOWS 100% (employer)
            ░░░░░░░░░░ MARCUS KNOWS 100% (investigation)
            ░░░░░░░░░░ SERA KNOWS 0%
            ░░░░░░░░░░ PLAYER KNOWS 0%

  NODE-015: ░░░░░░░░░░ VICTOR KNOWS 100%
            ░░░░░░░░░░ MILITIA KNOWS 100%
            ░░░░░░░░░░ MARCUS KNOWS 100%
            ░░░░░░░░░░ SERA KNOWS 0%
            ░░░░░░░░░░ PLAYER KNOWS 0% ← INFORMATION GAP

  NODE-025: ░░░░░░░░░░ ALL KNOW 100% (revelation scene)

Gap duration: NODE-005 → NODE-025 (20 nodes of tension)
Impact: Player is blind for crucial choice at NODE-015
```

### 8. **Check Realism** (optional with --check-realism)

Verify NPC knowledge is narratively justified:

```
MARCUS knows "Victor is militia spy" at NODE-005

Justification check:
  ✅ Role basis: Marcus is detective (has access to records)
  ✅ Time basis: Has been investigating Victor for 2 years
  ✅ Motive basis: Duty to identify spies
  ✅ Information source: Police records, informants
  
Result: ✅ REALISTIC

---

SERA knows "Militia is targeting Player" at NODE-010 (while imprisoned)

Justification check:
  ✅ Overhears guards talking
  ✅ Guards mention Player in context of ransom demand
  
Result: ✅ REALISTIC

---

VICTOR knows "Player will choose to help Sera" at NODE-015

Justification check:
  ❌ How would Victor know before it happens?
     • Victor doesn't have access to Player
     • Victor hasn't talked to anyone who knows
     • No psychic abilities in game world
  
Result: ❌ UNREALISTIC

Fix: Either Victor says this AFTER the choice (post-action dialogue)
     OR have informant report Player's choice
     OR remove this line entirely
```

### 9. **Report**

Output `asymmetry-audit.md` with:
- Information gap chart (who knows what, when)
- Healthy vs problematic asymmetries
- Realism check per asymmetry
- Impact on player agency
- If `--show-gaps`: Timeline visualization of information reveals
- If `--check-realism`: Justification analysis for each gap

---

## Important Notes

**Asymmetry Is NOT Bad**: Information gaps create tension, mystery, and player agency. The goal is *intentional*, *plausible* gaps that serve the story.

**Player Agency Requires Information**: Don't expect players to make good choices blindly. Ensure critical decisions have enough context. (May be intentional poverty of information if that's your design.)

**NPC Behavior Must Match Knowledge**: If NPC doesn't know something, their dialogue/behavior shouldn't reveal it. Consistency is the test.

**Factions Have Collective Knowledge**: Militia as a group knows more than any individual guard. When NPCs communicate (radio, messenger, etc.), faction knowledge spreads. Track this.

**Unreliable Narrators Are OK**: If an NPC is lying, that creates intentional false asymmetry (player thinks NPC doesn't know, but NPC is deliberately hiding). Mark these distinctly in your tracking.

