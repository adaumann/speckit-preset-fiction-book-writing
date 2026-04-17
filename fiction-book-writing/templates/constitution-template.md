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
       hybrid        → intentional cross-profile; active profile per act documented in Section VIII
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

#### hybrid
- **Usage**: The prose profile shifts deliberately at act boundaries or for specific POV characters. Document the active profile per act/character in Section VIII Story Bible.
- **Constraint**: Each segment must fully satisfy its designated profile's rules for the duration of that segment. Mixing profiles within a single scene is not permitted.
- **Transition rule**: A profile shift MUST coincide with a structural boundary (act break, chapter, or POV change). Never mid-scene.
- **Additional Anti-AI filter**: Inherits all prohibited phrases from every active profile used in this story

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

### Scene-Opening Orientation
Every scene MUST establish **who, where, and approximate time** within the first 2–3 sentences before entering interiority or dialogue. The reader cannot be oriented by character thought alone.

- Acceptable: a brief sensory anchor tied to a specific location
- Not acceptable: opening mid-thought with no spatial grounding, then orienting the reader three paragraphs later

### Narrative Distance Consistency
Within a single scene, POV distance MUST NOT drift. Choose one distance at the scene's opening and hold it:

| Distance | Characteristics |
|---|---|
| Close | Direct access to thoughts; "she thought"; body sensations named |
| Deep | Thoughts embedded as narration; no "she thought" scaffolding; sensation IS prose |
| Remote | External behavior only; no inner access; reader infers entirely |

Zooming in and out within one scene is only permitted if it serves a deliberate disorientation effect AND is documented in the scene's `scene-outline.md` note.

### Exposition & Infodump Rule
World-facts, backstory, and technical information MUST be delivered through **character need or perception**, not narrator explanation.

- A character explains only what they would plausibly say, to someone who would plausibly need to hear it, in the pressure of the moment
- Backstory arrives in fragments — provoked by a current stimulus, not summarized in sequence
- **Two-sentence rule**: Any block of expository narration longer than two sentences in a row is a red flag. Cut or redistribute into dialogue, sensory detail, or action

### Flashback Rules
Flashbacks are permitted only under these conditions:
1. The present-tense trigger (smell, object, sound) that pulls the character into the memory MUST be shown first
2. Maximum flashback length: **one scene** (no multi-chapter excursions into the past)
3. Return to the present MUST include a sensory re-anchoring beat — not "she snapped back to reality"
4. A flashback may not be used to deliver exposition that could be shown in forward-moving plot

### Repetition & Echo Discipline
The same descriptive word, image, or comparison MUST NOT recur within the same scene. Rules:
- No repeated key adjectives within 500 words
- No repeated metaphor vehicle within a chapter (e.g., using "water" as a metaphor for memory twice)
- If a word or image is deliberately echoed for thematic resonance, it MUST be separated by at least one full scene and land with measurably more weight than its first use

### Simile & Metaphor Budget
- Maximum **two extended comparisons** (simile or metaphor developed across more than one clause) per scene
- Comparisons MUST be drawn from the POV character's lived world — a soldier's metaphors come from combat, not astronomy
- Dead metaphors ("heart sank", "blood ran cold") count toward the budget and should be replaced with physical feedback instead

### Narrator Editorializing Prohibition
The narrator MUST NOT interpret, summarize, or editorialize about characters, situations, or meaning. The reader draws the conclusion; the narrator provides only the evidence.

**Prohibited narrator moves:**

| ❌ Telling | ✅ Showing |
|---|---|
| "She was the kind of person who never asked for help." | Show her decline three offers within the scene. |
| "He was clearly lying." | Show the pause, the redirected eye, the too-specific detail. |
| "The situation was hopeless." | Show every exit closing, one by one. |
| "Despite everything, she still cared." | Show the involuntary action that betrays it. |
| "It was the worst day of his life." | Show what he does with his hands. |

**Specific prohibitions:**
- No "she was the kind of person who…" constructions
- No "clearly," "obviously," "undeniably" in narration — if it is clear, the prose made it clear; stating it is redundant and condescending
- No narrator summary of what a scene meant: "And so she finally understood…" — end the scene on the moment; let the understanding be implicit
- No authorial intrusion declaring a character's trait: establish it through behavior across multiple scenes, never in a single descriptive sentence

**Permitted exception**: A POV character's *filtered* interpretation of another character is allowed ("Marcus looked like a man who had never asked for help in his life") — this is characterization of the observer, not narrator editorializing.

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

> **Architecture**: Which POV mode is used, who narrates which structural phase, the rotation schedule, and the information asymmetry map are defined in `pov-structure.md`. This file governs the rules that apply to all POV prose regardless of mode.

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

### Chapter Endings
Chapter endings carry disproportionate reader-retention weight and require separate discipline:

| Chapter position | Required ending type |
|---|---|
| Mid-story chapters (default) | End on a micro-hook — a decision made, a threat entered, or a revelation whose implications are not yet processed. The reader must feel pulled forward, not satisfied. |
| Act-break chapters | End on a **status shift**, not an emotion. Something the character had is now gone, or something unavoidable has arrived. |
| Final chapter | Resolution of dramatic question MUST precede the final image. The last paragraph is sensory, not expository — no summarizing of what was learned. |

**Prohibited chapter endings**: characters going to sleep (unless it is structurally ironic), neutral scene-setting that recaps what just happened, and dialogue that tidily closes a conflict.

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
| POV Strategy | [POV_STRATEGY] — full architecture in `pov-structure.md` |
| Tense | [TENSE] |
| Tone | [TONE] |
| Vocabulary Register | [VOCABULARY_REGISTER] |
| Sentence Rhythm | Variable: short/jagged during panic or action; long/winding during reflection or exhaustion |
| Target Word Count | [WORD_COUNT_TARGET] |
| Genre | [GENRE] |
| Target Audience | [TARGET_AUDIENCE] |
| Series Position | [SERIES_POSITION] |

<!-- VOCABULARY_REGISTER values and what they govern:

     plain-colloquial     → Everyday speech; contractions permitted; no specialist terms;
                            short words preferred over long synonyms. Accessible to all readers.

     clinical-precise     → Technical and exact; minimal emotional language; domain-specific
                            jargon used correctly and without apology. Suits science, legal,
                            or procedural settings. Jargon must be consistent — do not swap
                            between lay and technical terms for the same concept.

     literary-elevated    → Careful, deliberate word selection; some rare or archaic words
                            permitted if they earn their place; no padding. Suits literary
                            fiction where language itself is part of the experience.

     working-class-direct → Short words, concrete nouns, distrust of abstraction; no
                            performative vocabulary; idiom and ellipsis over formal structure.
                            Characters think in things, not concepts.

     bureaucratic-deadpan → Passive constructions, procedural language, institutional
                            vocabulary; irony and horror emerge from the flatness. Suits
                            dystopian, corporate, or satirical registers.

     custom               → Register defined in [VOCABULARY_REGISTER_NOTES] below. Use when
                            the story requires a blend or a register not listed above (e.g.,
                            archaic fantasy diction, dialect-inflected narration). -->

[VOCABULARY_REGISTER_NOTES]
<!-- Required only when Vocabulary Register is `custom`.
     Describe: formality level, domain specificity, permitted jargon, class/cultural markers,
     and any words or constructions that are prohibited or mandatory. -->

<!-- TARGET_AUDIENCE values and what they govern:

     literary-reader   → Expects ambiguity, rewards slow prose, tolerates unresolved endings.
                         Interiority may run long; subtext can be dense; theme need not be
                         signposted. Prose Profile literary or dark-realist recommended.

     casual-reader     → Reads for story and character momentum. Needs clear stakes per chapter,
                         regular payoffs, and accessible vocabulary. Subtext present but not
                         opaque. Prose Profile commercial recommended.

     naive-reader      → Little genre experience or unfamiliar with literary convention.
                         Exposition must be slightly more explicit; subtext should be backed
                         by a more visible behavioral cue; chapter hooks must be unambiguous.
                         Avoid ironic or deeply unreliable narrators without clear signals.

     young-adult       → Teen protagonist or readership. Coming-of-age stakes. Emotional
                         intensity is HIGH but content levels (violence, sexual content) are
                         moderated. Voice is close and immediate. Pacing is faster than adult
                         literary; no chapter should feel like it marks time.

     middle-grade      → Age 8–12. Protagonist is the reader's age. Dark themes permitted
                         but consequence must be proportionate and not hopeless. Vocabulary
                         accessible; sentences shorter on average; wonder and agency central.

     children          → Age 6–8. Simple sentence structure. Concrete sensory world. Stakes
                         feel large to the character; no ambiguous morality; resolution is
                         emotionally satisfying. Speckit.implement adjusts language complexity.

     custom            → Audience defined in [TARGET_AUDIENCE_NOTES] below. Set this when
                         the story targets a niche (e.g., genre-savvy thriller readers,
                         academic SF audience, romance subgenre readers). -->

[TARGET_AUDIENCE_NOTES]
<!-- Required only when Target Audience is `custom`.
     Describe the assumed reader: prior genre knowledge, tolerance for ambiguity,
     expected vocabulary level, and any content expectations specific to this readership. -->

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

### Protagonist Want vs. Need
<!-- The engine of the arc. These must be in tension — if they align, there is no arc.
     Want: What the protagonist consciously pursues (external goal)
     Need: What the protagonist must confront or accept to be whole (internal wound)
     The story forces the protagonist to choose between them at the climax. -->

| | Protagonist |
|---|---|
| **Want** (surface goal) | [PROTAGONIST_WANT] |
| **Need** (deep wound / truth) | [PROTAGONIST_NEED] |
| **Misbelief** (lie they tell themselves) | [PROTAGONIST_MISBELIEF] |

<!-- Add additional rows for co-protagonists if applicable. -->

### Antagonist Design
[ANTAGONIST_DESIGN]
<!-- The antagonist is not a villain — they are a mirror.
     Document:
     - Core motivation: what the antagonist wants and why they believe they are justified
     - Worldview: the governing logic that makes their actions coherent from their own perspective
     - Method: how they pursue their goal (coercion, manipulation, systemic force, ideology)
     - Mirror function: which aspect of the protagonist's misbelief does the antagonist embody or weaponize?
     The antagonist MUST NOT be defeated by a flaw the reader could not have anticipated. -->

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

### Subplot Integration Rule
Every subplot MUST relate to the main theme at a competing angle — not simply fill page count. Each subplot should:
1. Force the protagonist (or a POV character) to act in a way that either deepens their misbelief OR chips at it
2. Resolve on a different timeline than the main plot, so its resolution either foreshadows or ironizes the main climax
3. Be documented in `subplots.md` with its thematic function stated explicitly

[HYBRID_PROFILE_ACT_MAP]
<!-- REQUIRED only when PROSE_PROFILE is `hybrid`.
     Map each structural unit to its designated profile.
     Example:
     | Act / POV strand | Profile |
     |---|---|
     | Act I | commercial |
     | Act II (Elena chapters) | literary |
     | Act II (Marcus chapters) | thriller |
     | Act III | dark-realist |
     Delete this block entirely if PROSE_PROFILE is not hybrid. -->

---

## IX. Content & Sensitivity Policy
<!-- Governs how speckit.implement and speckit.sensitivity handle difficult material.
     This section does not restrict story content — it specifies HOW difficult content
     is handled so the AI produces consistent, intentional prose rather than
     defaulting to genre conventions or sanitizing without instruction. -->

### Violence
**Level**: [VIOLENCE_LEVEL]
<!-- Set to ONE of the following:
     - implied       → consequence shown, act kept off-page
     - functional    → act shown with minimal physical detail; emphasis on consequence
     - visceral      → full sensory detail; physical and psychological aftermath required
     - unflinching   → no restraint; lingering on cost is part of the narrative purpose -->

**Rules**:
- Violence MUST carry cost — physical, psychological, or relational. Consequence-free violence is prohibited regardless of level.
- Perpetrator's interiority during violence MUST be shown if they are a POV character.

### Sexual Content
**Level**: [SEXUAL_CONTENT_LEVEL]
<!-- Set to ONE of the following:
     - none          → no sexual content; intimacy closed-door
     - suggestive    → tension and implication only; physical detail stops at the threshold
     - moderate      → tasteful explicit content; body described but not graphic
     - explicit      → fully on-page; consistent with adult commercial fiction standards -->

### Trauma Depiction
**Level**: [TRAUMA_LEVEL]
<!-- Set to ONE of the following:
     - referenced    → trauma acknowledged as backstory, not dramatized
     - present       → trauma affects character behavior visibly; flashback fragments permitted
     - immersive     → trauma rendered in full sensory and psychological depth -->

**Rules**:
- Trauma responses MUST be consistent with the character's established history — no convenient recovery for plot convenience
- Recovery arcs, if present, must be earned (see Section III Earned Growth)

### Reader Advisory Flags
[CONTENT_WARNINGS]
<!-- List any content advisory flags this story carries for sensitivity readers or front-matter disclosure.
     Examples: suicide, sexual violence, child harm, addiction, racial violence, eating disorders.
     Set to "none" if no advisories apply.
     speckit.sensitivity uses this list to flag relevant scenes during review. -->

---

## X. Series Context
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

## XI. Audiobook Production
<!-- Skip this section entirely if Output Mode is `book`.
     When Output Mode is `audiobook` or `both`, speckit.implement generates a parallel
     audiobook draft alongside each prose draft in audiodraft/. -->

**Output Mode**: [OUTPUT_MODE]
<!-- Set to ONE of the following values:
     - book        → prose drafts only; no audiobook files generated
     - audiobook   → audiobook drafts generated; prose drafts still created
     - both        → prose drafts AND audiobook drafts generated -->

**TTS Engine**: [TTS_ENGINE]
<!-- Set to ONE of the following values (ignored when Output Mode is `book`):
     - ssml-cloud  → SSML-tagged XML; compatible with Azure TTS, Google Cloud TTS, Amazon Polly
     - elevenlabs  → ElevenLabs voice IDs, break tags, and .pls lexicon sidecar
     - both        → generate both ssml-cloud and elevenlabs variants per chapter -->

**Speaker Mode**: [SPEAKER_MODE]
<!-- Set to ONE of the following values:
     - single      → all narration and dialogue read by one narrator voice
     - multi       → narrator voice for prose; each named character's dialogue routed
                     to a distinct voice using the Speaker Configuration table below -->

### Speaker Configuration
<!-- Map narration and character dialogue roles to TTS voice identifiers.
     ssml-cloud voice: provider voice name (e.g. en-US-JennyNeural for Azure, en-US-Neural2-F for Google).
     ElevenLabs voice ID: the 20-character ID or the display name from your ElevenLabs account.
     For single speaker mode: only the narrator row is required. -->

| Role | Character / Function | SSML-Cloud Voice | ElevenLabs Voice ID | Notes |
|---|---|---|---|---|
| narrator | Narration & stage directions | [NARRATOR_VOICE_SSML] | [NARRATOR_VOICE_EL] | |
| dialogue | [CHARACTER_NAME] | [VOICE_SSML] | [VOICE_EL] | |
<!-- Add one row per named speaking character in multi speaker mode. -->

### Pronunciation Lexicon
<!-- Words, names, or terms that TTS engines commonly mispronounce.
     IPA: International Phonetic Alphabet transcription.
     SSML phoneme: used verbatim in <phoneme alphabet="ipa" ph="..."> tags.
     ElevenLabs substitute: plain-text replacement injected inline in EL files and
     also written into audiodraft/lexicon.pls as a <phoneme> entry. -->

| Word / Name | IPA | Plain Hint | ElevenLabs Substitute |
|---|---|---|---|
| [WORD] | [IPA] | [PLAIN_HINT] | [SUBSTITUTE] |
<!-- Examples:
     | Caoimhe  | ˈkiːvə  | KEE-vuh  | Keeva  |
     | Niamh    | niːv    | Neev     | Neev   |
     | Siobhán  | ʃɪˈvɔːn | shih-VAWN | Shivawn | -->

### Audiobook Style Hints
<!-- Per-character or per-context delivery notes.
     Copied as HTML comments into every audiobook draft file.
     Human narrators and SSML prosody tuning both use these. -->

| Character / Context | Hint |
|---|---|
| [CHARACTER_NAME] | [DELIVERY_NOTE] |
<!-- Examples:
     | Narrator            | Measured, cool, slight distance — never warm or excited          |
     | Marcus (angry)      | Clipped. Short sentences. Pause before the last word.            |
     | Chapter openings    | Slower pace; longer pauses between paragraphs                    |
     | Whispered dialogue  | Add <prosody volume="soft" rate="slow"> in SSML                  | -->

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
Each chapter draft MUST be checked against all of the following:

| Section | Rule | Check |
|---|---|---|
| II | Dirt Rule — at least one environmental flaw per scene | per scene |
| II | Physical Feedback — emotions shown through involuntary bodily reaction | per scene |
| II | Scene-Opening Orientation — who/where/time within first 2–3 sentences | per scene |
| II | Exposition & Infodump Rule — no narrator explanation blocks longer than 2 sentences | per scene |
| II | Repetition & Echo Discipline — no repeated key word within 500 words | per scene |
| II | Simile & Metaphor Budget — max two extended comparisons per scene | per scene |
| II | Narrator Editorializing Prohibition — no narrator interpretation, summary, or trait declaration | per scene |
| III | Micro-Obsessions — POV character habit recurs and escalates | per chapter |
| III | Voice Homogeneity — each POV character passes the name-tag swap test | per chapter |
| IV | Oblique Dialogue — no character answers directly first | per scene |
| IV | Physical Presence in Dialogue — each character has at least one physical action | per scene |
| IV | Em-dash density cap — no more than 3 em-dashes per 1,000 words | per scene |
| V | Triple Purpose — plot advance + character reveal + world deepening | per scene |
| V | Off-Balance Ending — no tidy scene closure | per scene |
| V | Chapter Ending type — matches required type for chapter position | per chapter |
| VI | Chronological Consistency — no contradicted world-state details | per chapter |
| VII | Anti-AI Filter — no prohibited phrases | per scene |

### Author Rule Overrides
<!-- Formal record of universal rules deliberately relaxed for this story.
     An override does NOT remove the rule globally — it documents an intentional,
     scoped exception. speckit.continuity will not flag drafts for overridden rules
     within the declared scope.
     Leave empty if no overrides apply. -->

| Rule | Section | Scope (scene / chapter / whole book) | Rationale |
|---|---|---|---|
| [RULE_NAME] | [SECTION] | [SCOPE] | [RATIONALE] |
<!-- Example:
     | Dirt Rule | II | Ch. 1 opening scene only | First impression of the station must feel pristine to mirror the protagonist's false sense of safety. Flaw introduced in Ch. 2. |
     | Em-dash cap | IV | Marcus chapters throughout | Marcus's speech pattern is defined by mid-thought redirection; cap raised to 5 per 1,000 words for his POV only. | -->

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
