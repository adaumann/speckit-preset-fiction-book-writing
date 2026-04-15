---
description: Sensitivity and representation review — flags cultural misrepresentation, harmful tropes, anachronisms in historical fiction, and identity portrayal issues across drafted chapters. Read-only analysis with severity tiers (CRITICAL / WARNING / NOTE) and per-issue remediation guidance. Scope to a single chapter, a demographic category, or the full manuscript.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
handoffs:
  - label: Revise Chapter
    agent: speckit.revise
    prompt: Revise this chapter to address the sensitivity issues identified in the report
    send: false
  - label: Update Story Bible
    agent: speckit.constitution
    prompt: Add representation guidelines to the story bible based on the sensitivity review findings
    send: false
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check after sensitivity revisions
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- *(no argument)* — full sensitivity review of all drafted chapters
- `[CHAPTER_ID]` — scope to a single chapter (e.g. `A2.201`)
- `[CHAPTER_ID]–[CHAPTER_ID]` — scope to a chapter range
- `--category [name]` — scope to one check category: `representation`, `tropes`, `historical`, `language`, `trauma`
- `--genre [genre]` — override genre detection for targeted rules (e.g. `--genre historical-fiction`, `--genre fantasy`)

---

## Purpose

`speckit.sensitivity` reviews drafted chapters for issues that could harm, misrepresent, or inadvertently stereotype real or fictional groups — and for anachronisms in period-set work. It does not make style or prose judgments; it focuses exclusively on representation, accuracy, and harm potential.

**This command is**:
- A first-pass screening tool — not a substitute for human sensitivity readers
- Read-only — it never rewrites prose, only flags and advises
- Scope-aware — it respects genre conventions (a fantasy world with invented cultures has different rules than historical fiction set in 1940s Berlin)

**Five check categories**:

| Category | What it covers |
|---|---|
| **Representation** | Identity portrayal: race, ethnicity, gender, sexuality, disability, religion, class |
| **Tropes** | Harmful or tired narrative tropes: Magical Negro, Bury Your Gays, Inspiration Porn, Exotic Other, Fridging |
| **Historical** | Anachronisms: language, technology, attitudes, social structures, dates, terminology out of period |
| **Language** | Slurs, outdated clinical terms, dehumanizing descriptors, cultural terms used incorrectly |
| **Trauma** | Depictions of violence, assault, mental illness, addiction, grief — sensitivity to survivors |

---

## Execution Steps

### Step 1 — Setup

Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

Load:
- Required: all `draft/*.md` files in scope — abort if no draft files exist
- Optional: `spec.md` (genre, setting, character identities), `constitution.md` (representation intentions stated by author), `characters.md` / `characters/` (identity fields per character profile)
- Optional: `world-building.md` (invented cultures — flags cannot apply standard real-world rules to fully fictional cultures without context)

**Detect genre** from `spec.md` or `constitution.md`:
- `historical fiction` → enable Historical check with period-specific rules
- `contemporary fiction` → enable all categories with real-world standards
- `fantasy` / `sci-fi` → apply representation and trope checks; apply historical checks only to real-world elements embedded in the story; flag invented cultures separately
- `literary fiction` → full review; note that difficult subject matter handled with craft intent is different from harmful depiction

### Step 2 — Build identity map

From `characters.md`, `characters/` profiles, and `spec.md`, construct an identity map:

| Character | Ethnicity/culture | Gender | Sexuality | Disability | Class | Religion | POV role |
|---|---|---|---|---|---|---|---|
| [Name] | [from profile] | | | | | | [P1/P2/P3/antagonist] |

If identity fields are absent from profiles, note: `Identity fields not populated in characters.md — review may be incomplete.` Do not invent identity attributes.

### Step 3 — Run checks

#### Category A: Representation

For each non-white, non-cis, non-able-bodied, or minority-religion character in the identity map, scan their scenes for:

**CRITICAL**:
- Character defined entirely by their identity attribute (no personality beyond their marginalization)
- Character exists primarily to further a majority character's arc with no arc of their own (instrumental minority)
- Character's identity treated as a problem to be solved or overcome without narrative acknowledgment
- Disabled character "cured" as a reward or resolution beat

**WARNING**:
- Character's identity mentioned primarily in physical description, rarely in interiority or dialogue
- Multiple minority characters sharing identical voice register or traits (homogenization)
- Minority character dies while majority characters survive equivalent danger (disproportionate sacrifice)
- Same-sex relationship treated as more scandalous or in need of justification than equivalent straight relationship

**NOTE**:
- Character appears in fewer than 20% of chapters relative to their stated arc priority
- Identity markers used inconsistently across chapters (e.g., dialect that appears and disappears)

#### Category B: Tropes

Scan all drafted chapters for these patterns:

| Trope | Detection signal | Severity |
|---|---|---|
| Magical Negro / Magical Minority | Non-white character exists to guide or save white protagonist with no personal stake | CRITICAL |
| Bury Your Gays | LGBTQ+ character killed or suffers while straight characters are spared | CRITICAL |
| Fridging | Female or minority character harmed/killed primarily to motivate a male/majority protagonist | CRITICAL |
| Inspiration Porn | Disabled character's struggle depicted for able-bodied character's emotional growth | CRITICAL |
| Exotic Other | Culture or ethnicity reduced to food, clothing, accent, or "mysterious" descriptors | WARNING |
| Sassy Black Friend / Token | Single minority in a group with no individual characterization | WARNING |
| Strong Female Character (hollow) | Female character defined by toughness with no emotional depth or vulnerability | WARNING |
| Tragic Queer | LGBTQ+ character's arc resolves only in tragedy, rejection, or isolation | WARNING |

#### Category C: Historical (skip if genre is non-historical)

Detect anachronisms by cross-referencing the story's stated period (from `spec.md` or `constitution.md`) against:

**CRITICAL**:
- Technology that did not exist in the period (TV, phones, plastics, specific weapons, medicines)
- Social structures depicted as modern (informal first-name address in formal hierarchies, casual mixed-gender socializing in segregated periods)
- Events referenced that had not yet occurred at the story's date

**WARNING**:
- Language / slang coined after the story's period — list specific terms flagged
- Attitudes depicted as common that were rare or suppressed in the period (anachronistic progressivism without narrative acknowledgment)
- Currency, measurements, titles, or ranks used incorrectly for the period and region

**NOTE**:
- Historical figures mentioned — flag for `speckit.research` verification
- Period-typical prejudices depicted in dialogue or action without authorial framing — note for author review (not automatically a problem; may be intentional)

#### Category D: Language

Scan for:

**CRITICAL**:
- Contemporary slurs used by a narrator or sympathetic character without narrative purpose
- Outdated clinical terms for mental illness, disability, or sexuality used as neutral descriptors (e.g., "retarded", "psychotic" as casual adjectives, "homosexual" as clinical label in contemporary fiction)
- Dehumanizing language applied to any ethnic, religious, or national group without clear narrative condemnation

**WARNING**:
- Cultural terms from a specific culture used by outsider characters without acknowledgment of that outsider status
- Dialect or accent written phonetically in a way that de-dignifies a character
- Religious terminology used incorrectly for the tradition being depicted

#### Category E: Trauma

Scan for depictions of: violence, sexual assault, self-harm, suicide, addiction, eating disorders, abuse, or grief.

**CRITICAL**:
- Sexual assault depicted from an approving or titillating narrator perspective
- Suicide depicted using method detail that could function as instruction (per safe messaging guidelines)
- Addiction "resolved" by willpower alone with no acknowledgment of the medical dimension

**WARNING**:
- Trauma used purely as backstory shorthand with no weight given to the survivor's interiority
- Self-harm or eating disorder romanticized (aestheticized without cost)
- Violence against children depicted in graphic sensory detail with no narrative distance

**NOTE**:
- Depictions that may require a content note at the front of the book — list by chapter
- Scenes that could benefit from a trigger warning for sensitive readers — recommend to author

### Step 4 — Report

```
🔍 Sensitivity Review — [STORY_TITLE]
Chapters reviewed: N  |  Categories: [all / scoped list]
Genre detected: [genre]

Identity coverage: [N characters with identity map entries / N total named characters]
⚠️  Identity fields incomplete for: [character names if any]

Issues: N CRITICAL · N WARNING · N NOTE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ [Chapter ID] — [Category] — [Trope/issue name]
   Finding: [One sentence describing the specific passage or pattern]
   Why it matters: [One sentence on the harm or misrepresentation]
   Suggested fix: [Concrete revision direction — never rewrites prose]

[Repeat for each CRITICAL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WARNING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ [Chapter ID] — [Category] — [Issue name]
   Finding: [One sentence]
   Suggested fix: [Concrete revision direction]

[Repeat for each WARNING]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️ [Chapter ID] — [Category] — [Note]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended front matter content notes:
  [List chapters that may warrant content notes for readers]

IMPORTANT: This is an AI first-pass review. For work featuring communities
the author does not belong to, commission a human sensitivity reader before
querying or publishing.
```

If no issues found:
```
✅ No sensitivity issues flagged.
Note: AI review has known limitations. Human sensitivity readers are
recommended for any work featuring communities outside the author's experience.
```
