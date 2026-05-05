---
description: Ending quality gate — verify endings resolve the central dramatic question, maintain thematic consistency, and provide satisfying closure for player character and stakes.
handoffs:
  - label: Check Agency
    agent: speckit.agency
    prompt: Before finalizing endings, verify player choices actually lead to different endings.
    send: true
  - label: Review Themes
    agent: speckit.tone
    prompt: Check that endings emotionally land and thematically resolve.
    send: true
---

# speckit.endings

Ending quality gate — verify all registered endings provide **satisfying closure** by resolving the central dramatic question, maintaining thematic consistency, and giving narrative weight to player agency.

## Ending Quality Rubric

An ending is **satisfying** when it:
- ✅ **Resolves the central dramatic question** (from constitution.md §V Dramatic Question)
- ✅ **Player character has changed** (arc closure, not reset)
- ✅ **Stakeholder fates are clear** (key NPCs, supporting cast, world state)
- ✅ **Thematic resonance** (echoes central theme, resolves or ironizes it)
- ✅ **Consequence weight** (player choices matter; stakes have real payoff)
- ✅ **Emotional landing** (tone matches content; doesn't feel cheap or manipulative)
- ✅ **Explicitness** (not ambiguous about what happened and what it means)

**NOT validated here** (use other tools):
- ❌ Whether all endings are reachable (use `speckit.agency`)
- ❌ Pacing/prose quality (use `speckit.polish`)
- ❌ Whether foreshadowing pays off (use `speckit.foreshadow`)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — audit all endings in `specs/endings.md`
- Ending ID (e.g., `ENDING-001`) — audit one specific ending
- `--endings-only` — check only ending node files (skip variable/consequence validation)
- `--show-variants` — display all conditional ending variants based on variable state

Optional flags:
- `--strict` — fail on ambiguous or emotionally hollow endings
- `--check-reachability` — verify each ending is actually reachable from root node

## Pre-Execution Checks

1. Confirm `specs/endings.md` exists with all registered endings
2. Confirm `specs/constitution.md` exists with central dramatic question and theme
3. Confirm `specs/plan.md` exists with ending node identifiers
4. Confirm `draft/[ENGINE]/` contains ending node files for each ending
5. Load `specs/characters.md` if available (for character arc closure)
6. Load `specs/themes.md` if available (for thematic resonance check)

## Execution Steps

### 1. **Load Spec Documents**
   - Read `constitution.md`: Extract central dramatic question (§V), theme, ending tone preferences
   - Read `endings.md`: All ending IDs, names, win/loss classification, required variables
   - Read `plan.md`: Ending node IDs (where endings are written)
   - Read ending node files: Extract prose and variable state snapshots

### 2. **Audit Each Ending**

For each registered ending in `endings.md`:

#### A. **Central Question Resolution Check**

**Question**: Does the ending answer the central dramatic question from constitution.md?

**Central Dramatic Question examples**:
- "Can the protagonist overcome their trust issues?"
- "Will the rebellion succeed against the tyranny?"
- "Does love survive conflict?"

**Validation**:
```
Constitution: "Can the protagonist escape their past?"

ENDING-ESCAPE:
  Prose: "You leave the city behind. The ghosts don't follow."
  ✅ YES — Directly answers the question (protagonist escapes)

ENDING-AMNESIA:
  Prose: "You lose your memories. The past no longer haunts you."
  ⚠️  INDIRECT — Answers via memory loss rather than actual escape
  → Flag as "thematic dodge" — is this intentional?

ENDING-RETURN:
  Prose: "You come back home. Your family waits."
  ❌ NO — Doesn't address the question (protagonist doesn't escape)
  → Flag as failure to resolve central question
```

**Report**:
```
ENDING-ESCAPE:
  Central Question: "Can protagonist escape their past?"
  Resolution: ✅ Direct — protagonist leaves
  Status: RESOLVES

ENDING-RETURN:
  Central Question: "Can protagonist escape their past?"
  Resolution: ❌ Avoids — doesn't address escape
  Status: DOES NOT RESOLVE
  Fix: Either reframe question, or rewrite ending to address escape
```

#### B. **Player Character Arc Closure Check**

**Question**: Has the player character changed from start to this ending?

**Arc closure exists when**:
- Character belief shifts (e.g., "I can't trust anyone" → "I can trust selectively")
- Capability increases (learns skill, gains confidence)
- Relationship changes (with mentor, with love interest, with self)
- Stakes are paid (if cost promised, cost is collected; if victory promised, victory achieved)

**Validation**:
```
ENDING-HERO:
  Start state: player_agency = 0, courage = 2, trust = -5
  End state: player_agency = 1, courage = 5, trust = 2
  ✅ ARC EXISTS — Multiple character stats have changed
  
ENDING-RESET:
  Start state: courage = 2, trust = -5
  End state: courage = 2, trust = -5
  ❌ NO ARC — Character unchanged, returns to start
  Fix: Add character change (even if tragic/hollow)
```

**Report**:
```
ENDING-HERO:
  Player arc: courage -2→5, trust -5→2
  Status: ✅ Strong arc with stakes paid

ENDING-RESET:
  Player arc: (no change from start state)
  Status: ❌ No character growth
  Fix: Add at least one variable shift to show change
```

#### C. **Stakeholder Fate Clarity Check**

**Question**: Is the fate of key NPCs and world state explicitly stated?

Key stakeholders:
- Protagonist (should be addressed; see arc closure above)
- Love interest / key relationship (what happens to this bond?)
- Mentor / antagonist (alive? dead? reconciled?)
- Supporting cast (at least mentioned, not completely abandoned)
- World state (changed by player choices or reset?)

**Validation**:
```
ENDING-PEACE:
  Prose: "The city is quiet. Marcus smiles from the balcony.
          You realize Sera went back to her family.
          The war council never meets again."
  ✅ All key NPCs addressed:
     • Protagonist: at peace, contemplative
     • Marcus (mentor): alive, content
     • Sera (love interest): departed but acknowledged
     • Antagonists: implicitly defeated (war council dissolved)
     • World: permanently changed

ENDING-BETRAYED:
  Prose: "You're alone in the basement.
         The door closes. You hear footsteps above,
         then silence."
  ⚠️  AMBIGUOUS:
     • Protagonist: trapped, possibly dead?
     • Marcus: fate unclear (was he the betrayer?)
     • Sera: fate unknown
     • Antagonists: not addressed
     Fix: Add 1-2 lines clarifying fates of key NPCs
```

**Report**:
```
ENDING-PEACE:
  Marcus (mentor): Addressed ✅
  Sera (love interest): Addressed ✅
  Antagonists: Addressed ✅
  World state: Addressed ✅
  Status: ✅ All stakeholders clear

ENDING-BETRAYED:
  Marcus: Unknown ⚠️
  Sera: Unknown ⚠️
  Antagonists: Unknown ⚠️
  Status: ⚠️ Multiple ambiguous fates
```

#### D. **Thematic Resonance Check**

**Question**: Does the ending echo the central theme and resolve or ironize it meaningfully?

**Theme examples** (from constitution.md §V Theme):
- "Trust must be earned" → Ending should show trust dynamics
- "Power corrupts" → Ending should show player power usage
- "Love transcends boundaries" → Ending should center on love

**Validation**:
```
Theme: "Trust must be earned"

ENDING-PARTNERSHIP:
  Prose: "Marcus extends his hand. 'I trust you now.' 
          Years of small choices led here."
  ✅ RESONATES — Centers on trust being earned through action
  
ENDING-BETRAYAL:
  Prose: "Marcus smiles as he stabs you.
          You gave him everything. He didn't earn your trust—he took it."
  ✅ RESONATES (ironically) — Subverts the theme darkly; trust was misplaced

ENDING-ESCAPE:
  Prose: "You flee the city. Nobody follows."
  ❌ IGNORES THEME — Doesn't address trust at all
  Fix: Add element showing trust dynamics (or reconsider if this is right ending for this theme)
```

**Report**:
```
ENDING-PARTNERSHIP:
  Central theme: "Trust must be earned"
  Resonance: ✅ Strong — explores earning trust
  Type: Direct resolution

ENDING-ESCAPE:
  Central theme: "Trust must be earned"
  Resonance: ❌ None — ending avoids theme
  Type: Thematic gap
  Fix: Rewrite to include trust element OR reconsider if ending fits this game
```

#### E. **Consequence Weight Check**

**Question**: Do player choices feel like they matter? Does the ending prove that stakes were real?

**Consequence weight exists when**:
- Different endings reachable based on different choice paths
- High-stakes choices lead to visibly different outcomes
- Player agency decisions are reflected in ending variation
- Sacrifices made in-game are acknowledged in ending

**Validation**:
```
Choice at NODE-010: "Save Marcus or Protect City"

Save Marcus path:
  → Marcus alive in ending prose
  → City falls, mentioned as lost
  → Variables: marcus_alive = true, city_standing = -5
  ✅ Consequence clear

Protect City path:
  → Marcus mentioned as fallen hero
  → City stands but wounded
  → Variables: marcus_alive = false, city_standing = 2
  ✅ Consequence clear

Both paths → ENDING-001 but with different variable snapshots
✅ Same ending ID, but meaningful state difference
```

**Report**:
```
ENDING-VICTORY:
  Consequence weight (choice → outcome):
    • "Save Marcus" path has marcus_alive = true ✅
    • "Protect City" path has marcus_alive = false ✅
    • Ending prose reflects both variants
  Status: ✅ Strong consequence weight
```

### 3. **Generate Ending Quality Report**

Create `specs/ending-audit.md`:

```markdown
## Ending Quality Audit

**Game**: [NAME]
**Central Question**: [from constitution]
**Theme**: [from constitution]
**Date**: [ISO]

| Ending ID | Name | Central Q | Arc | Clarity | Thematic | Consequence | Status |
|-----------|------|-----------|-----|---------|----------|-------------|--------|
| ENDING-001 | Victory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ PASS |
| ENDING-002 | Escape | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ⚠️ REVIEW |
| ENDING-003 | Death | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ PASS |
| ENDING-004 | Reset | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ FAIL |

### Violations

**Fail (4 - Need fixes)**:
- ENDING-004 (Reset): Doesn't resolve central question, no character arc

**Review (2 - Consider fixes)**:
- ENDING-002 (Escape): Weak arc, ambiguous thematic payoff

**Pass (2)**:
- ENDING-001 (Victory): Fully resolving
- ENDING-003 (Death): Thematically resonant tragedy

### Recommendations

**Priority 1 (Fix before release)**:
1. ENDING-004: Either add character arc or cut this ending
2. ENDING-002: Strengthen emotional closure and thematic tie-in

**Priority 2 (Polish)**:
1. ENDING-001: Clarify one ambiguous NPC fate
2. ENDING-003: Consider adding epilogue variant for different variable states
```

### 4. **Ending Variants** (optional with --show-variants)

Some endings may have multiple variants based on variables:

```
ENDING-PEACE (base):
  Base prose: "The city is quiet."
  
  + if marcus_alive: "Marcus smiles from the balcony."
  + elif marcus_dead: "We honor Marcus's memory at the memorial."
  
  + if rebellion_won: "The new council meets in the square."
  + elif rebellion_lost: "The occupiers have left, but the wound remains."

Variants generated: 4 (2 × 2 combinations)
Status: ✅ Ending reflects major choice branches
```

**Report all variants** so writers can verify each feels satisfying.

### 5. **Reachability Check** (optional with --check-reachability)

Trace from root node → each ending:
- Is there at least one valid path to this ending?
- Are there choice combinations that make this ending unreachable?

**Report unreachable endings** — they may be dead code or blocked by agency violations.

### 6. **Report**

Output `ending-audit.md` with:
- Audit table (all 7 quality dimensions per ending)
- Violation list (fail, review, pass categories)
- Specific recommendations for each failing ending
- If `--show-variants`: Variant table for each ending
- If `--check-reachability`: Reachability analysis

---

## Important Notes

**Satisfying ≠ Happy**: Tragic, bittersweet, and dark endings can be fully satisfying if they resolve the dramatic question and close character arcs. A sad ending where the character changed is more satisfying than a happy ending where nothing mattered.

**Ambiguity Rule**: Minor ambiguities are fine (reader interpretation space). Major ambiguities (protagonist fate, world state, key NPC survival) should be explicit.

**Theme Payoff**: If you chose a central theme, every ending should either resolve it directly, subvert it meaningfully, or explain why it doesn't apply. Ignoring your own theme is weak.

**Variable Snapshots**: Different paths can reach the same ending ID but with different variable states. This is GOOD — it shows player choices matter. Always include prose variants or metadata showing how the same ending plays differently based on player history.

