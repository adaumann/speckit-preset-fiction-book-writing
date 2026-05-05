---
description: Accessibility validator — measure readability (Flesch-Kincaid, sentence length), flag content warnings needed, validate contrast for UI text, identify ableist language.
handoffs:
  - label: Revise Readability
    agent: speckit.revise
    prompt: Some passages have poor readability. Please simplify sentence structure and vocabulary.
    send: true
  - label: Polish
    agent: speckit.polish
    prompt: After accessibility review, refine prose for readability and clarity.
    send: true
---

# speckit.accessibility

Accessibility validator — measure **readability (Flesch-Kincaid grade level, sentence length), flag content warnings, validate contrast for UI text, identify ableist language**.

## Accessibility Principle

**Accessible content** = Readable by broad audience (ages 8–80, various reading abilities), appropriate content warnings provided, UI legible, no unnecessary jargon or ableist language.

**Accessibility barriers include**:
- ❌ High reading level (grade 16+ for general audience)
- ❌ Run-on sentences (40+ words without punctuation)
- ❌ Missing content warnings (violence, gore, trauma, strobe effects)
- ❌ Poor contrast (UI text hard to read on backgrounds)
- ❌ Ableist language ("crazy," "lame," "psycho," "schizo")
- ❌ Inaccessible description (no alt text for images/emojis in parser IF)

**Valid accessibility includes**:
- ✅ Grade 8–10 reading level (general audience)
- ✅ Mix of sentence lengths (avg 15–20 words)
- ✅ Content warnings at game start
- ✅ High contrast (WCAG AA minimum)
- ✅ Respectful language (no slurs, no ableist phrasing)
- ✅ Content descriptions (self-explanatory without prerequisite knowledge)

## User Input

```text
$ARGUMENTS
```

Accepted input:
- Nothing — full accessibility audit across all nodes
- `--readability-only` — check only reading level (skip warnings, contrast, language)
- `--warnings-only` — extract content warnings needed (skip reading level)
- `--contrast-only` — check UI contrast only
- `--language-only` — check for ableist/inaccessible language

Optional flags:
- `--target-grade [N]` — custom target reading level (default: 8–10)
- `--strict` — flag any sentence >30 words
- `--show-violations` — display problematic text passages with suggestions
- `--content-warnings-template` — generate starter content warning block

## Pre-Execution Checks

1. Load all `draft/[ENGINE]/NODE-*.md` files
2. Load `specs/constitution.md` target audience
3. Load `specs/themes.md` if present (for content warning tracking)
4. Extract prose text (separate from code/syntax)
5. Check for UI/theme files (story.css, ink-theme.html) for contrast validation

## Execution Steps

### 1. **Measure Reading Level**

Flesch-Kincaid Grade Level per node:

```
Formula: 0.39 × (words/sentences) + 11.8 × (syllables/words) - 15.59

NODE-010 prose:
  "Marcus sits across from you, hands folded.
   His expression is unreadable. Something shifts in his eyes—
   a flicker of doubt? Understanding? You can't tell."
   
Analysis:
  Words: 43
  Sentences: 3
  Syllables: ~68
  Grade level: (0.39 × 14.3) + (11.8 × 1.58) - 15.59 = 6.2 (Grade 6)
  
Interpretation:
  • Grade 6 = ~12-year-old reading level
  • Accessible to most audiences ✅

NODE-015 prose:
  "The epistemological lacunae inherent in phenomenological discourse 
   regarding intersubjective intentionality necessitate a reconsideration 
   of the hermeneutic apparatus undergirding contemporary metaphysical 
   frameworks."
   
Analysis:
  Words: 32
  Sentences: 1
  Syllables: ~82
  Grade level: (0.39 × 32) + (11.8 × 2.56) - 15.59 = 16.8 (Grade 16+)
  
Interpretation:
  • Grade 16+ = College/academic reading level
  • Only accessible to highly educated readers ❌
  • Need to simplify for general audience
```

### 2. **Analyze Sentence Structure**

Check for run-on sentences and variety:

```
NODE-020 sentences:

1. "You push through the crowd." (6 words)
2. "Bodies press against you from all sides, shoulders colliding, 
   voices rising in cacophony, and you can barely breathe as 
   you fight forward through the sea of humanity." (40 words)
3. "The door is ahead." (4 words)

Analysis:
  • Sentence 1: Very short (6 words) ✅
  • Sentence 2: Run-on (40 words) ⚠️
  • Sentence 3: Very short (4 words) ✅
  
  Average: 17 words
  Variance: Good (4 → 40 → 4 creates rhythm)
  
Problem with Sentence 2:
  • 40 words without primary break is difficult to parse
  • Could be split: "Bodies press against you from all sides. Shoulders collide. 
    Voices rise in cacophony. You can barely breathe as you fight forward 
    through the sea of humanity."
    
Fix: Break at logical points (punctuation or clause boundaries)
```

### 3. **Detect Content Warnings Needed**

Flag sensitive content requiring disclosure:

```
Content warning categories:

VIOLENCE:
  • Gore/graphic description → Label: "Graphic Violence"
  • Combat/action → Label: "Violence"
  • Death of named character → Label: "Character Death"

PSYCHOLOGICAL:
  • Torture, abuse → Label: "Torture, Abuse"
  • Existential dread, body horror → Label: "Psychological Content"
  • Suicide/self-harm → Label: "Suicide, Self-Harm"
  • Trauma revisiting → Label: "Trauma Content"

SENSORY:
  • Flashing lights, strobe effects → Label: "Flashing Lights (Seizure Risk)"
  • Loud sudden noises → Label: "Loud Sound Effects"

CONTENT:
  • Sexual content → Label: "Sexual Content"
  • Drug/alcohol use → Label: "Drug Use, Alcohol"
  • Discrimination, slurs → Label: "Discrimination [specify]"
  • Animal harm/death → Label: "Animal Harm, Death"

Example NODE scan:

NODE-025: "Marcus bleeds out. His body jerks once, then stills. 
          You watch the light leave his eyes."
          
Flags: ✅ Character Death (Marcus), ✅ Graphic Violence
Warnings needed: "Character Death, Graphic Violence"

NODE-030: "Red lights pulse. Red lights pulse. Red lights pulse. 
          [This continues for 10 seconds in-game]"
          
Flags: ✅ Flashing Lights (seizure risk)
Warnings needed: "Flashing Lights (Seizure Risk)" + explanation of duration
```

### 4. **Validate UI Contrast**

Check readability of on-screen text:

```
Contrast Check (WCAG standard):
  • AA (minimum): 4.5:1 for normal text, 3:1 for large text
  • AAA (enhanced): 7:1 for normal text, 4.5:1 for large text

Example (SugarCube CSS):

--color-text: #1a1a1a (near black)
--color-bg: #faf8f3 (off-white)

Contrast ratio: 14.2:1 ✅ EXCELLENT (AAA compliant)

---

Problematic example:

--color-text: #888888 (medium gray)
--color-bg: #999999 (slightly darker gray)

Contrast ratio: 1.1:1 ❌ FAIL (too low)
Issue: Text will be unreadable for colorblind and low-vision players
Fix: Either darken text or lighten background
```

### 5. **Scan for Ableist Language**

Identify harmful or exclusionary phrasing:

```
Ableist language examples to flag:

FLAGGED:
  ❌ "He's crazy" → Use: "He's unstable" or specific behavior
  ❌ "That's lame" → Use: "That's disappointing" or "ineffective"
  ❌ "Blind to the truth" → Use: "Unaware of" or "Missing"
  ❌ "Psycho killer" → Use: "Unstable person" or "Murderer"
  ❌ "Crippled economy" → Use: "Struggling economy" or "Weakened"
  ❌ "Deaf to reason" → Use: "Unwilling to listen" or "Stubborn"
  ❌ "Schizo behavior" → Use: "Fractured" or specific behavior description
  ❌ "Spaz out" → Use: "Lose control" or "Panic"
  ❌ "That's retarded" → Use: "That's slow" or "That's ineffective"
  ❌ "Leper" (slur) → Use: "Exile" or "Outcast" depending on context

ACCEPTABLE:
  ✅ "Blind rage" (metaphorical, common usage)
  ✅ "Crippling doubt" (metaphorical, accepted)
  ✅ Character describing their own disability: "I'm deaf. I read lips."
  ✅ Historical context slurs in dialogue (with content warning)

CONTEXT MATTERS:
  • When? Historical period, modern day, fantasy world?
  • Who? Character slur vs. narrator slur vs. game itself?
  • Why? Authentic to character or gratuitous?

Example NODE scan:

NODE-015: "The militia troops were deaf to reason and blind to mercy.
          Their leader was clearly insane."
          
Flags: 
  • "deaf to reason" → Metaphorical, acceptable ✅
  • "blind to mercy" → Metaphorical, acceptable ✅
  • "clearly insane" → Ableist, imprecise ⚠️
  
Fix: "Their leader was clearly unhinged" or "unstable"
```

### 6. **Generate Accessibility Audit Report**

Create `specs/accessibility-audit.md`:

```markdown
## Accessibility Audit

**Game**: [NAME]
**Target Audience**: [from constitution.md]
**Date**: [ISO]

### Reading Level Analysis

| Node | Grade Level | Target | Status |
|------|-------------|--------|--------|
| NODE-010 | 6.2 | 8–10 | ✅ Pass |
| NODE-015 | 16.8 | 8–10 | ❌ Too High |
| NODE-020 | 8.9 | 8–10 | ✅ Pass |
| NODE-025 | 9.1 | 8–10 | ✅ Pass |

Average game grade level: 10.2 (slightly high)
Recommended target: 8–10
Status: ⚠️ Review NODE-015

### Sentence Structure

| Node | Avg Length | Max Length | Variety | Status |
|------|-----------|-----------|---------|--------|
| NODE-010 | 14 | 22 | Good | ✅ Pass |
| NODE-015 | 28 | 45 | Poor | ⚠️ Review |
| NODE-020 | 16 | 40 | Fair | ⚠️ Review |
| NODE-025 | 12 | 18 | Good | ✅ Pass |

Guideline: Avg 12–18 words, max 30 words
Status: ⚠️ Some nodes need shortening

### Content Warnings Required

**Primary**:
- Character Death (Marcus: NODE-025)
- Graphic Violence (NODE-025, NODE-030)
- Psychological Content (NODE-032: existential crisis)

**Secondary**:
- Drug Use (NODE-018: militia drugs)
- Discrimination (NODE-020: slurs toward outsiders)

**Sensory**:
- None identified

Recommended opening warning:
"⚠️ Content Warning: This game contains character death, 
graphic violence, and psychological content."

### UI Contrast

| Element | Foreground | Background | Ratio | Standard | Status |
|---------|-----------|-----------|-------|----------|--------|
| Main text | #1a1a1a | #faf8f3 | 14.2:1 | AA (4.5:1) | ✅ AAA |
| Link text | #2563eb | #faf8f3 | 8.1:1 | AA | ✅ AAA |
| Button | #faf8f3 | #8b5cf6 | 5.3:1 | AA | ✅ AAA |

All contrast ratios meet WCAG AAA standard ✅

### Ableist Language

**Flagged** (2 instances):
1. NODE-015: "clearly insane" → suggest "unstable" or "unhinged"
2. NODE-020: "lame excuse" → suggest "weak excuse" or "pathetic"

**Acceptable** (3 instances):
1. NODE-010: "blind rage" (metaphorical) ✅
2. NODE-025: "deaf to pleas" (metaphorical) ✅
3. NODE-032: Character says "I'm crazy" (self-identification) ✅

### Recommendations

**Priority 1 (Readability)**:
1. NODE-015: Reduce grade level from 16.8 → 8–10
   - Simplify vocabulary (epistemological → concerning)
   - Break long sentences (40+ words → 25 max)

2. NODE-020: Reduce max sentence from 40 → 25 words
   - Break compound sentences with periods or semicolons

**Priority 2 (Language)**:
1. Replace "insane" with character-appropriate alternative
2. Replace "lame" with "weak" or "pathetic"

**Priority 3 (Polish)**:
1. Add explicit content warning block to opening
2. Consider audio description for key visual scenes
3. Test with colorblind simulation tools

### Accessibility Score: 7/10

Strong: Contrast ratios, content warnings identified
Weak: Reading level, sentence length, some ableist language
Improvements needed before release
```

### 7. **Show Violations** (optional with --show-violations)

Display problematic passages with fixes:

```
READABILITY VIOLATION: High Grade Level

NODE-015 (Grade 16.8):
  Passage:
    "The epistemological lacunae inherent in phenomenological discourse..."
  
  Problem:
    • "epistemological" (college-level: 5 syllables)
    • "lacunae" (rare plural: 3 syllables)
    • "phenomenological" (academic jargon: 6 syllables)
    • Grade 16.8 vs target 8–10
  
  Suggested rewrite:
    "The gaps in how we think about consciousness are becoming clear..."
  
  New grade level: 7.2 ✅

---

RUN-ON SENTENCE VIOLATION

NODE-020:
  Passage:
    "Bodies press against you from all sides, shoulders colliding, voices 
     rising in cacophony, and you can barely breathe as you fight forward 
     through the sea of humanity."
  
  Problem:
    • 40 words in single sentence
    • Multiple clauses linked by commas (hard to parse)
    • Reader loses breath before meaning is clear
  
  Suggested rewrite:
    "Bodies press against you from all sides. Shoulders collide. 
     Voices rise in cacophony. You can barely breathe as you fight 
     forward through the sea of humanity."
  
  Analysis:
    • Split into 4 sentences
    • Avg length: 10 words each
    • Now easier to read while maintaining rhythm

---

ABLEIST LANGUAGE VIOLATION

NODE-015:
  Passage:
    "The general was clearly insane, ordering troops to burn villages."
  
  Problem:
    • "insane" is ableist; conflates mental illness with evil
    • Imprecise (what specific behavior is insane?)
  
  Suggested rewrite:
    "The general was clearly unstable, ordering troops to burn villages."
  
  OR (more specific):
    "The general was clearly ruthless, ordering troops to burn villages."
```

### 8. **Content Warnings Template** (optional with --content-warnings-template)

Generate starter warning block:

```
# Content Warnings

This game contains the following content. 
If any of these are triggers for you, please proceed with caution.

**Violence**:
- Graphic violence (blood, injuries)
- Character death (multiple NPCs)
- Combat/action sequences

**Psychological**:
- Existential dread (NODE-032)
- Betrayal themes

**Other**:
- Drug use (mention, NODE-018)
- Discrimination and slurs (historical setting)

**Sensory**:
- None

**Not included**:
- Sexual content
- Animal harm
- Strobe lights
- Loud sudden noises

---

If you need to skip a section containing any of these elements, 
please let us know and we can suggest an alternate path.
```

### 9. **Report**

Output `accessibility-audit.md` with:
- Reading level analysis (grade level per node, average, target)
- Sentence structure analysis (length, variety, run-on detection)
- Content warnings needed (categorized, specific nodes)
- UI contrast validation (all UI elements checked)
- Ableist language scan (flagged terms, context analysis)
- If `--show-violations`: Problem passages with suggested rewrites
- If `--content-warnings-template`: Generated warning block ready to use

---

## Important Notes

**Grade Level Is Approximate**: Flesch-Kincaid is useful but not perfect. Manual review is important.

**Context Matters for Language**: A character using an ableist slur in dialogue (especially period piece) might be intentional and acceptable. Narrator using it is different.

**Self-Identification Is Valid**: A character saying "I'm crazy" or "I'm deaf" is different from labeling them that way. Respect character voice.

**Test With Real Readers**: Best accessibility testing involves people from target audiences (various ages, abilities, backgrounds). Automated checks are baseline, not comprehensive.

**Warnings Are Spoiler-Free**: Content warnings shouldn't spoil plot. E.g., "Character death" is OK; "Marcus dies at NODE-25" is not.

**Contrast Extends to All Text**: Menu text, button text, link text—all need to meet contrast standards. Don't rely on white text on light backgrounds.

