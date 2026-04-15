# [STORY_TITLE] Story Bible
<!-- Your story's governing document. This overrides all writing prompts and templates. -->

---

## Style Mode

**[STYLE_MODE]**
<!-- Set to ONE of the following values:
     - author-sample   → Your own key chapter defines the voice (Section I-A)
     - humanized-ai    → Use the Humanized AI Prose principles (Section I-B)
     Set this first. The AI will use whichever section matches your choice
     and treat the other as inactive reference material. -->

---

<!-- ═══════════════════════════════════════════════════════════════════
     MODE A: AUTHOR VOICE SAMPLE
     Paste 500–2000 words from a key chapter or scene that represents
     the exact voice, rhythm, and style you want for this story.
     The AI will use this text as the authoritative style reference
     and extract the markers below from it.
     ═══════════════════════════════════════════════════════════════════ -->

## I-A. Author Voice Sample
<!-- ACTIVE when STYLE_MODE: author-sample | Ignored otherwise -->

[AUTHOR_VOICE_SAMPLE]
<!-- Paste your reference text here. Guidelines:
     - Minimum 500 words for reliable style extraction
     - Choose a passage that contains both dialogue AND narration
     - Include at least one moment of emotional intensity
     - This text defines: sentence rhythm, vocabulary register,
       POV distance, dialogue style, and sensory density
     The AI will populate the Extracted Style Markers below
     when running speckit.constitution for the first time. -->

### Extracted Style Markers
<!-- Populated automatically by speckit.constitution from your sample.
     Override manually if the inference is wrong. -->

| Marker | Extracted Value |
|---|---|
| POV & Distance | [NEEDS CLARIFICATION] |
| Tense | [NEEDS CLARIFICATION] |
| Sentence rhythm | [NEEDS CLARIFICATION] |
| Vocabulary register | [NEEDS CLARIFICATION] |
| Dialogue style | [NEEDS CLARIFICATION] |
| Sensory density | [NEEDS CLARIFICATION] |
| Tone | [NEEDS CLARIFICATION] |
| Anti-patterns to avoid | [NEEDS CLARIFICATION] |

---

<!-- ═══════════════════════════════════════════════════════════════════
     MODE B: HUMANIZED AI PROSE PRINCIPLES
     A detailed craft ruleset for commercially viable fiction that
     avoids AI clichés, achieves psychological depth, and maintains
     tactile sensory grounding.
     ═══════════════════════════════════════════════════════════════════ -->

## I-B. Mission
<!-- ACTIVE when STYLE_MODE: humanized-ai | Ignored otherwise -->

[STORY_MISSION]
<!-- State the core creative intent for this story. Example:
     "Craft an engaging, commercially viable novel for KDP that avoids
     AI clichés, emphasizes psychological depth, includes tactile
     sensory details, and maintains a clear narrative structure." -->

---

## I-C. Prose Profile
<!-- ACTIVE when STYLE_MODE: humanized-ai | Ignored otherwise
     The Prose Profile tunes HOW the universal craft principles
     (Sections II–VII) are weighted. It does not override or relax
     any universal rule — Triple Purpose, Dirt Rule, Anti-AI Filter,
     and Off-Balance Endings apply in all profiles.

     Set to ONE of the following values:
       commercial    → balanced pace, moderate interiority, alternating rhythm
       literary      → deep interiority, high sensory texture, reflection-forward
       thriller      → action-forward, minimal interiority, short-dominant sentences
       atmospheric   → maximum sensory density, slow burn, atmosphere as plot engine
       dark-realist  → clipped declarative prose, cold interiority, consequence-forward
-->

**[PROSE_PROFILE]**

### Profile Specifications

#### commercial
- **Sentence rhythm**: Alternating short and long; no run longer than 3+ sentences in either direction
- **Sensory density**: Medium — one strong anchor per scene beat, not every paragraph
- **Interiority**: Balanced — inner monologue present but keeps pace; never exceeds the external action duration
- **Dialogue subtext**: Moderate — deflection present in key exchanges; some exchanges are allowed to be direct
- **Pacing bias**: Scene/Sequel balance — each action scene is followed by a reaction/processing beat of comparable length
- **Additional Anti-AI filter**: "a journey of self-discovery" · "more than they bargained for" · "a world turned upside down" · "everything changes when"

#### literary
- **Sentence rhythm**: Long-dominant in introspection and observation; fragments and staccato bursts during shock or rupture only
- **Sensory density**: High — texture, decay, and layered sensory detail; the environment carries thematic weight
- **Interiority**: Deep — extended interior passages are expected; characters process contradictions at length; self-deception must be visible in the logic of the internal monologue itself
- **Dialogue subtext**: Heavy — almost no exchange should be taken at face value; silence and action carry as much or more than speech
- **Pacing bias**: Reflection-forward — the interior consequence of events is at least as long as the events; plot advancement is secondary to resonance
- **Additional Anti-AI filter**: "liminal" · "ineffable" · "the weight of" · "something shifted inside her" · "she couldn't quite put into words" · "a mosaic of memories"

#### thriller
- **Sentence rhythm**: Short-dominant (1–2 clauses); long sentences reserved for immediate aftermath only, never mid-action
- **Sensory density**: Low-to-medium — precise and functional detail only; sensory anchors are obstacles or threats, not texture
- **Interiority**: Minimal — inner monologue is compressed to single-sentence observations or cut entirely during action; characters act before they reflect
- **Dialogue subtext**: Light — dialogue is terse and functional; subtext is carried by what is NOT said or done, not by elaborate deflection; silences are weaponized
- **Pacing bias**: Action-forward — sequel beats are compressed; reflection happens in motion, not in stillness
- **Additional Anti-AI filter**: "heart pounding" · "adrenaline surged" · "pulse quickened" · "fight-or-flight" · "every instinct screamed" · "she had no choice"

#### atmospheric
- **Sentence rhythm**: Long and winding; syntactic embedding is expected; rhythm mirrors environment (oppressive/lush/decaying)
- **Sensory density**: Maximum — every scene contains multi-layered sensory detail; non-visual senses are mandatory (smell, texture, temperature, sound); environment is a character
- **Interiority**: Deep — inner life and environment blur; characters project onto surroundings; pathetic fallacy is permitted if handled as character perception, not authorial statement
- **Dialogue subtext**: Heavy — dialogue is sparse and loaded; characters are not articulate about their fears; setting description often replaces or interrupts speech
- **Pacing bias**: Atmosphere as plot engine — the reader's experience of the environment IS the plot momentum; external events are catalysts for sensory and psychological immersion, not endpoints
- **Additional Anti-AI filter**: "an oppressive silence" · "the darkness seemed alive" · "she could feel the history" · "the place had a way of" · "wrapped in mystery"

#### dark-realist
- **Sentence rhythm**: Clipped and declarative; no ornament; sentence fragments for emphasis; no semicolons in narration
- **Sensory density**: Medium, with bias toward failure, decay, and physical wear; beauty is mentioned only when it is ironic or about to be lost
- **Interiority**: Selective and cold — inner monologue is brief, factual, and often wrong about itself; characters rationalize rather than feel; the gap between stated thought and apparent emotion is always visible to the reader
- **Dialogue subtext**: Deflationary — characters understate, deflect with practicalities, and refuse emotional vocabulary; the most devastating lines must sound mundane
- **Pacing bias**: Consequence-forward — causes are skipped over or presented as given; the story opens in the aftermath and works backward or proceeds through accumulating costs; no catharsis
- **Additional Anti-AI filter**: "broken but not beaten" · "found her strength" · "it was what it was" · "at the end of the day" · "despite everything" · "survivors"

---

## II. Sensory Detail & Environment

### Grounded Realism
Prioritize **sensory truth** over lofty metaphors. Avoid statistics and overwhelming scientific explanations unless they directly serve character voice.

| ❌ Less Human | ✅ More Human |
|---|---|
| "The silence was a heavy blanket of forgotten dreams." | "The room smelled of stale coffee and the ozone from a failing air scrubber." |

### The Dirt Rule
No environment should feel perfect. Every scene MUST include at least one small flaw — a smudge on a lens, a fraying cuff, a flickering light, an unscratched itch. These imperfections make the world feel lived-in.

### Physical Feedback
Show emotions through **involuntary bodily reactions**, not named feelings.

| ❌ | ✅ |
|---|---|
| "She felt despair." | "Her knees went soft. She leaned on the door frame and did not push off." |

---

## III. Character Depth & Contradiction

### Unreliable Self
Characters often deceive themselves. Inner monologue MAY focus on surface problems to avoid confronting deeper trauma. The reader sees the real wound through behavior and deflection — not through confession.

### Earned Growth
Arcs are rarely linear. Characters take two steps forward, one step back — or regress entirely under pressure. A character who only improves is not believable.

### Micro-Obsessions
Every POV character MUST have one small, seemingly useless habit (counting pen clicks, checking a mask seal, straightening labels). Rules:
- The habit MUST recur and **escalate** across scenes
- A single instance does not satisfy this requirement
- The habit intensifies under emotional pressure — this is how the reader tracks internal state

### Human Paradox
Contradictions make characters believable. A brilliant scientist can be superstitious. A cold leader might secretly cherish a child's drawing. Assign at least one contradiction to each major character in their `characters/[name].md` profile.

### Voice Homogeneity Warning ⚠️
All POV characters MUST sound distinct — not just in vocabulary, but in **observational register**:
- What they notice first when entering a room
- What they skip over or dismiss
- How their sentences break under pressure

**Test**: If a scene from Character A could plausibly be narrated by Character B without the name tags, rewrite until it cannot.

---

## IV. Dialogue & Subtext

### Oblique Dialogue
Characters MUST NOT answer directly first. They deflect, misinterpret, or use silence strategically. The honest answer arrives **last**, not first — characters respond beside the question before reaching it.

### Distinct Voices
Each POV character must have a documented voice signature in their `characters/[name].md` profile covering: vocabulary range, sentence rhythm under stress, observational register, and default deflection strategy.

### Power Dynamics
Dialogue MUST reflect hierarchy and tension: who controls the room, who fears, who negotiates for scraps. This should be visible in sentence length, interruption, and topic avoidance — not stated.

### Misunderstanding Requirement
Every scene with dialogue SHOULD include at least one moment where a character **misunderstands** someone else OR **fails to find the right word**. This is more humanizing than eloquence.

### Physical Presence in Dialogue
Characters in conversation MUST exist in bodies. Each character gets **at least one physical action per scene** — not tagged with emotion, just described. The reader infers.

Mundane actions carry more weight than deliberate gestures:
- Refilling a cup
- Repositioning a folder
- Going completely still

### Incomplete Speech
- Use **em dash (—)** for mid-sentence redirects when a character catches where the sentence is going and re-routes
- Use **ellipsis (…)** only for genuine trailing off — never for dramatic pause
- Characters MUST NOT accurately name their own worst motivations aloud in real time; show the motive through behavior or deflection
- **Em-dash density cap**: no scene may contain more than **3 em-dashes per 1,000 words** (all uses combined). Overuse turns technique into tic.

### Dry Irony
[DRY_IRONY_CHARACTERS]
<!-- List which characters (if any) are permitted one quiet moment of
     situational irony per scene. Rules:
     - Must not read as a joke — it reads as a precise observation
       that happens to be quietly absurd
     - If it feels like a humor beat, cut it and find the version that doesn't
     - Never use near emotional peaks
     - Set to "none" if dry irony is not part of this story's register -->

---

## V. Scene Integrity

### Triple Purpose
Every scene MUST simultaneously achieve all three:

1. **Advance the plot** — a physical or situational state has changed by the end
2. **Reveal character** — a new facet, contradiction, or micro-behavior has been shown
3. **Deepen the world** — sensory detail, world logic, or lore has been established

A scene that achieves only two of three requires revision or cutting.

### Off-Balance Endings
Scenes MUST NOT end on tidy summaries or emotional resolution. End on:
- Unresolved tension
- A question (stated or implied)
- A lingering sensory impression
- An action whose meaning is not yet clear

### Strand Interaction
When multiple POV strands or characters meet, show **clashing perceptions** — how trauma, bias, or prior experience colors the same event differently for each person present.

---

## VI. Timeline & Logical Coherence

### Chronological Consistency
All timelines are tracked in `timeline.md`. Rules:
- If a physical or world-state detail is established in Scene A, it MUST be consistent in Scene B unless a reason for change is explicitly shown
- Track: resource levels, injuries, elapsed time, distances, states of objects

### Strategic Revelation
Prefer showing **consequence before cause** to create dramatic irony. Use time jumps to withhold information — the reader should know something happened before they know why.

---

## VII. Stylistic Parameters

| Parameter | Value |
|---|---|
| POV Strategy | [POV_STRATEGY] |
| Tense | [TENSE] |
| Sentence Rhythm | Variable: short/jagged during panic or action; long/winding during reflection or exhaustion |
| Target Word Count | [WORD_COUNT_TARGET] |
| Genre | [GENRE] |
| Target Audience | [TARGET_AUDIENCE] |
| Series Position | [SERIES_POSITION] |

### Anti-AI Filter ⚠️
The following phrases are PROHIBITED — they mark prose as AI-generated:

> "In the heart of" · "A testament to" · "Shimmering" · "Dance of shadows" · "Echoes of the past" · "The air was thick with" · "Little did they know" · "Tapestry of" · "Navigating" (metaphorical) · "Delve into" · "Vibrant" · "It was a reminder that"

[ADDITIONAL_PROHIBITED_PHRASES]
<!-- Add story-specific phrases to avoid here.
     Common additions: pet phrases from your own drafts that become tics,
     genre clichés specific to your category. -->

---

## VIII. Story Bible

### Plot Structure
[PLOT_STRUCTURE]
<!-- Choose one:
     - three-act          → Setup → Confrontation → Resolution (default)
     - heros-journey      → Departure → Initiation → Return (Vogler 12 stages)
     - freytag            → Exposition → Rising Action → Climax → Falling Action → Denouement
     - save-the-cat       → 15 beats with word-count pacing targets
     - story-circle       → Dan Harmon's 8-step character transformation loop
     - kishotenketsu      → Ki → Shō → Ten → Ketsu (no central conflict required)
     - five-act           → Introduction → Rise → Climax → Fall → Catastrophe/Resolution -->

### Central Dramatic Question
[DRAMATIC_QUESTION]
<!-- The spine of the entire story. One sentence.
     Example: "Will Elena expose the conspiracy before it exposes her?" -->

### Theme
[THEME]
<!-- Stated as a question, not an answer.
     Example: "Is survival worth becoming what you fought against?"
     The theme is explored through multiple characters at competing angles.
     It is NEVER stated directly in dialogue. -->

### Story-Specific Principles
[STORY_SPECIFIC_PRINCIPLES]
<!-- List 3–5 rules unique to this story. Examples:
     - The antagonist believes they are the hero
     - Every named character death must be earned through prior investment
     - The resolution cannot rely on information withheld from the reader
     - No rescue; characters solve their own problems or accept the cost -->

---

## IX. Series Context
<!-- ACTIVE only when Series Position is non-standalone.
     Skip this section entirely if Series Position is `standalone`.
     This section is a per-book read-out of the series-level constraints that directly govern THIS book.
     Populated by speckit.constitution from series/series-bible.md.
     Do NOT edit these values manually — update series/series-bible.md instead,
     then re-run speckit.constitution to refresh this section. -->

**Series title**: [SERIES_TITLE]
**Series position**: [SERIES_POSITION]
**Series bible**: `series/series-bible.md`
**Series POV strategy**: [consistent with series / departs — variance documented below]
**Series tense**: [consistent with series / departs — variance documented below]

### Active Series Canon Constraints (this book)
<!-- World rules and facts from series/series-bible.md ## Series Canon that are already established
     and cannot be contradicted by this book's drafts.
     Populated from SC-NNN entries. speckit.continuity enforces these at draft time. -->

| Canon ID | Rule | Source |
|---|---|---|
| SC-001 | [Propagated from series-bible.md] | [Book N, Chapter ID] |
<!-- Add rows for all SC-NNN entries relevant to this book's time period and cast. -->

### Open Series Continuity Constraints (entering this book)
<!-- Character facts, relationship states, and knowledge disclosures established in prior books
     that MUST be honored at the opening of this book.
     Populated from STC-NNN entries with "Must hold from: Book N" ≤ this book.
     speckit.analyze cross-references character ## X. Series Arc State tables against these. -->

| Constraint ID | Rule | Established at | Characters affected |
|---|---|---|---|
| STC-001 | [Propagated from series-bible.md] | [Book N, chapter ID] | [Names] |
<!-- Add rows for all STC-NNN entries that apply at the opening of this book. -->

### Series Variance Log
<!-- Document any intentional departures from series-level style parameters.
     A departure requires explicit justification — it does not change the series default.
     Leave empty if no variances apply. -->

| Parameter | Series default | This book's value | Justification |
|---|---|---|---|
| POV strategy | [from series-bible.md] | [this book's value] | [reason] |
| Tense | [from series-bible.md] | [this book's value] | [reason] |

---

## Governance

This Story Bible overrides all writing prompts and templates.

### Amendment Process
Any changes require:
1. Documented rationale
2. Impact assessment (which scenes/chapters are affected)
3. Updates to all dependent templates (`spec-template.md`, `plan-template.md`, `tasks-template.md`)

### Retroactive Change Protocol

When the constitution is amended **after drafting has begun**, follow this protocol before continuing to draft:

**Step 1 — Record the change in `## Change Log` below.**
Document: version bump, date, what changed (exact principle or prohibition), and impact scope (which sections of the story are potentially affected).

**Step 2 — Bump the version number.**
Update the `Version` / `Last Amended` line at the bottom of this file.

**Step 3 — Run `speckit.continuity`.**
It will flag all draft files whose `constitution_version` field is older than the current version (`STALE CONSTITUTION`). It will cross-reference the change log to produce a targeted `Constitution Change Impact` table showing which specific principles must be checked in each stale draft.

**Step 4 — Triage each stale draft.**
For every draft flagged `STALE CONSTITUTION`:
- Compare the change log entry's `Impact` column against that draft's content.
- If the draft is **not affected** by the specific change (e.g., a new prohibited phrase doesn't appear in it), update only the `constitution_version` field in the draft YAML header — no rewrite needed.
- If the draft **is affected**, add it to the revision queue with the specific violation(s) noted.

**Step 5 — Revise affected drafts** (run `speckit.revise` on each).
Revise only the passages that violate the new or amended principle. Mark the draft's `constitution_version` field with the current version and increment `version` in the YAML header after rewriting.

> ⚠️ Do not advance drafting of new chapters until all `STALE CONSTITUTION` drafts from the impact scope are resolved or triaged.

### Compliance Review
Each chapter draft MUST be checked against:
- Section II (Sensory Detail — Dirt Rule + Physical Feedback)
- Section V (Triple Purpose scene test)
- Section VII Anti-AI Filter

### Versioning
- **MAJOR**: Structural changes (e.g., switching plot structure, adding/removing POV strands)
- **MINOR**: New principles or stylistic guidance added
- **PATCH**: Typos, clarifications, minor refinements

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]

---

## Change Log

<!-- Record every amendment made after ratification.
     This table is the source speckit.continuity uses to produce the Constitution Change Impact report.
     Impact: list beat IDs or phases potentially affected, or "all drafts" for global style changes. -->

| Version | Date | Type | What Changed | Impact |
|---|---|---|---|---|
| [CONSTITUTION_VERSION] | [RATIFICATION_DATE] | — | Initial ratification | — |
