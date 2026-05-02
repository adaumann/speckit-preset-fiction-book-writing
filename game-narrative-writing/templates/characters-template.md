# Character Profile: [CHARACTER_NAME]

<!-- NPC ID: [NPC_ID] | First Node: [FIRST_NODE_ID] | Last Node: [LAST_NODE_ID] -->

**Role**: [Key NPC / Antagonist / Ally / Mentor / Foil / etc.] | **Age**: [Age at story start] | **Background**: [One-sentence background summary]

---

## I. Core Identity

**Psychological Profile**:
- **Dominant Trait**: [The most defining personality trait — specific, e.g., "Controlled paranoia masking grief" not just "suspicious"]
- **Strength**: [What this character genuinely does well — visible in behavior, not just stated]
- **Flaw**: [The specific failure mode — what goes wrong when their trait is under pressure]
- **Drive**: [What they are actively pursuing — the want, from their own perspective]
- **Fear**: [What they are avoiding — the wound's surface expression]

**Background Foundation**:
<!-- 3–5 sentences. The formative facts that explain who they are NOW.
     Every sentence should connect to the flaw, drive, or fear above. -->
- [Formative experience 1 — connects to flaw or fear]
- [Formative experience 2 — connects to drive or wound]
- [Formative experience 3 — explains a key relationship or default behavior]

**Internal Arc**:
- **Wound / False belief**: [What they believe about themselves or the world that is not quite true]
- **Want** (surface goal they pursue): [NEEDS CLARIFICATION]
- **Need** (thematic truth they resist): [NEEDS CLARIFICATION]
- **Transforms from -> to**: [Starting state -> range of ending states across the branching endings]

---

## II. Speech Patterns & Voice

### Vocabulary Preferences
<!-- The goal: a node written in this character's voice should be unmistakably theirs
     even without the name tag. Dialogue at every trust level must sound like the same person. -->
- **Primary register**: [Formal / Clinical / Casual / Street / Academic / Poetic / etc.]
- **Recurring word clusters**: [2–3 semantic fields this character orbits — e.g., "control language," "precision language," "sensory-emotional language"]
- **Intensifiers / verbal habits**: [Specific fillers, qualifiers, or emphasis words they overuse]
- **Contractions**: [Heavy / moderate / rare — and what that signals]

**Example Vocabulary Pool**:
<!-- ~15 words or short phrases characteristic of this character.
     Include a few words they would NEVER use — negative space is also voice. -->
[word], [word], [word], [word], [word], [word], [word], [word], [word], [word]

*Words they avoid*: [word], [word], [word]

### Dialogue Style
- **Directness level**: [Do they answer questions directly or obliquely? How many beats before the honest answer?]
- **Power in conversation**: [Do they control the exchange, follow, or negotiate for scraps?]
- **Default deflection strategy**: [How do they avoid saying the real thing? Humor? Clinical distance? Redirection?]
- **Under pressure**: [How does their dialogue change when stressed? Shorter sentences? More formal? More chaotic?]
- **Subtext pattern**: [What they almost never say aloud that drives their half of every scene]

### Sample Dialogue

**[Context 1 — e.g., low trust / first meeting]**:
- "[Sample line]"
- Tone: [descriptor]
- Subtext: "[What they really mean / want / fear]"

**[Context 2 — e.g., neutral trust / collaborative moment]**:
- "[Sample line]"
- Tone: [descriptor]
- Subtext: "[What they really mean]"

**[Context 3 — e.g., high trust / moment of vulnerability]**:
- "[Sample line]"
- Tone: [descriptor]
- Subtext: "[What they really mean]"

---

## III. Internal Monologue

### Thought Pattern
- **Primary cognitive mode**: [Feeling-first / Analytical-first / Image-first / Action-first]
- **Blind spot**: [What do they systematically fail to notice or misinterpret?]
- **Self-deception pattern**: [How do they lie to themselves?]
- **Obsessive loop**: [The thought that keeps returning under pressure]

### Voice Examples

**[Situation 1 — e.g., a moment of desire or discovery]**:
> [3–5 sentences in this character's internal voice. Match vocabulary register.
>  Show the self-deception or blind spot in action if possible.]

**[Situation 2 — e.g., a moment of conflict or confrontation]**:
> [3–5 sentences. The inner voice must feel distinct from all other characters'.]

**[Situation 3 — e.g., a decision moment]**:
> [3–5 sentences. Show how they rationalize or commit.]

---

## IV. Physical Expression

- **Micro-obsession**: [The recurring habit that escalates under stress — must appear across multiple nodes]
- **Stress tell**: [The involuntary physical reaction under pressure before they can control it]
- **Comfort behavior**: [What they do when relaxed or among allies]
- **Authority posture**: [How their body language shifts when in control vs. not]
- **Signature appearance detail**: [The one thing about their appearance that recurs across scenes]

---

## V. Emotional Landscape

### Primary Emotions

| Emotion | Trigger | Visible as | Masks |
|---|---|---|---|
| [Emotion 1 — baseline] | [What reliably triggers it] | [Visible behavior] | [What deeper feeling it covers] |
| [Emotion 2] | | | |
| [Emotion 3] | | | |
| [Emotion 4] | | | |
| [Emotion 5 — suppressed] | | [How it leaks despite suppression] | |

- **Default channel**: [Direct expression / Displacement / Intellectualization / Physical action / Humor]
- **Overflow pattern**: [What breaks first when they can't contain an emotion]
- **Recovery pattern**: [How they return to baseline after an emotional event]

**Moments of real doubt** (must be honored in nodes, not bypassed):
- **Doubt 1**: [The situation, what they briefly see, how they suppress it]
- **Doubt 2**: [NEEDS CLARIFICATION]

---

## VI. Relationship to Player & Other Characters

### With the Player Character
- **Communication pattern**: [How they talk to the player — not what they say but how]
- **Subtext**: [What this character is really always asking for from the player]
- **Dynamic**: [The repeating loop — what they do -> player response -> escalation pattern]
- **Trust variable**: `$trust_[name]`
- **Arc**: [How does this relationship change across the branch range?]

### With [NPC Name] — [Relationship label]
- **Communication pattern**: [NEEDS CLARIFICATION]
- **Subtext**: [NEEDS CLARIFICATION]
- **Dynamic**: [NEEDS CLARIFICATION]
- **Arc**: [NEEDS CLARIFICATION]

---

## VII. Trust State Thresholds

<!-- Defines what the trust score means narratively and mechanically.
     speckit.implement and speckit.checklist use this to validate trust hook usage. -->

| Score Range | State Label | Dialogue Register | Available Choices Unlocked |
|---|---|---|---|
| 0–25 | hostile | Cold, clipped, suspicious. Minimal words. | Basic options only |
| 26–49 | cautious | Guarded, non-committal. No personal information. | Standard options |
| 50–74 | neutral | Polite, professional. Answers direct questions. | Most options |
| 75–89 | friendly | Warm, forthcoming. Shares context unprompted. | Friendly options |
| 90–100 | ally | Loyal, direct. Reveals hidden information. | All options including secret |

**Starting trust**: [N]

---

## VIII. Dialogue Register by Trust State

<!-- How this character speaks at each trust level.
     Calibrate from the voice established in Section II — same person, different armour. -->

### Hostile (0–25)
[Description — how Section II voice sounds when armoured, suspicious, closed]

**Sample line**: "[SAMPLE_HOSTILE_LINE]"

### Cautious (26–49)
[Description]

**Sample line**: "[SAMPLE_CAUTIOUS_LINE]"

### Neutral (50–74)
[Description]

**Sample line**: "[SAMPLE_NEUTRAL_LINE]"

### Friendly (75–89)
[Description]

**Sample line**: "[SAMPLE_FRIENDLY_LINE]"

### Ally (90–100)
[Description — how Section II voice sounds when the armour is fully down]

**Sample line**: "[SAMPLE_ALLY_LINE]"

---

## IX. NPC State Machine

<!-- All valid states for this character. Maps to $npc_[name]_state variable.
     Ink integer enum mapping listed for export. -->

| State Value | Label | Ink Integer | Description | Triggered In |
|---|---|---|---|---|
| alive | alive | 0 | Default — character present and interactable | — |
| dead | dead | 1 | Character is dead — replaced by body/ghost/reference | NODE-[N] (choice [X]) |
| hostile | hostile | 2 | Actively opposed to player | NODE-[N] (if trust < 25) |
| absent | absent | 3 | Character has left the scene | NODE-[N] |
| [CUSTOM] | [custom] | 4 | [DESCRIPTION] | NODE-[N] |

**Default state**: alive
**State variable**: `$npc_[name]_state`

---

## X. Bark Lines

<!-- Short ambient one-liners for exploration and incidental moments.
     Not in dialogue trees — used for atmosphere and characterisation.
     Must be consistent with the voice in Section II. -->

### Greeting Barks
- "[BARK_GREETING_1]"
- "[BARK_GREETING_2]"

### Reaction Barks (player action)
- "[BARK_REACTION_1]"
- "[BARK_REACTION_2]"

### Ambient Barks (overheard)
- "[BARK_AMBIENT_1]"
- "[BARK_AMBIENT_2]"

---

## XI. Branch Behavior Map

| Condition | Node ID | Effect |
|---|---|---|
| trust >= 75 | NODE-[N] | Unlocks choice: "[choice text]" |
| trust < 25 | NODE-[N] | Removes choice: "[choice text]" |
| npc_state = dead | NODE-[N] | Replaces dialogue with body description |
| npc_state = hostile | NODE-[N] | Forces conflict branch; disables dialogue |
| trust >= 90 | NODE-[N] | Reveals hidden information: [INFO] |

---

## XII. Knowledge State

<!-- What does this character know, and when/how does the player learn it?
     Prevents speckit.continuity flagging "NPC shares information they cannot have." -->

| Information | Character Knows From | Player Can Learn In | Condition |
|---|---|---|---|
| [INFO_1] | Game start (backstory) | NODE-[N] | trust >= 75 |
| [INFO_2] | After NODE-[N] event | NODE-[N] | trust >= 50 AND flag_[event] |
| [SECRET] | Game start (hidden) | NODE-[N] | trust >= 90 (ally only) |

---

## XIII. Scene Guidance

### Nodes This Character Drives
- **[Node type 1]**: What it must accomplish for this character's arc
- **[Node type 2]**: What it must accomplish
- **[Node type 3]**: What it must accomplish

### Sensory Signature
- **Primary sensory anchor**: [The recurrent sensory detail connected to this character]
- **Emotional sensation**: [How strong emotion manifests physically for them specifically]
- **Environment tell**: [What kind of physical space reflects their internal state]

### Emotional Arc Progression Across Acts

| Act | Emotional State | Visible Behavior | Node Types |
|---|---|---|---|
| Act 1 | [Emotional baseline] | [Default observable behavior] | [What kinds of nodes they appear in] |
| Act 2 | | | |
| Act 3 | [Transformed state or range] | [Changed or locked behavior] | |

---

## XIV. Verbal Tics & Repeated Phrases

**Repeated phrases** (and what state they signal):
- "[Phrase 1]..." -> [signals: what emotional state this reveals]
- "[Phrase 2]..." -> [signals: ]
- "[Phrase 3]..." -> [signals: ]

**Speech pattern under stress**:
[How sentence structure, vocabulary, or rhythm breaks under pressure]

**What they never say** (but mean constantly):
[The sentence this character could never bring themselves to say aloud — the core of their subtext]

---

## XV. Summary for Writers

**Core Challenge**: [The hardest thing about writing this character well — what goes wrong if you are not careful]

**Default Tone**: [2–3 words that sum up their register in a normal node]

**Variance Points**: [The 2–3 circumstances where they break from their default — the moments that reveal depth]

**Voice Homogeneity Test**: [A one-line statement that is unmistakably this character and no other. If another character could say it, rewrite until they could not.]

**Success Indicator**: [What should the player feel about this character at the end? Not what happens to them — what the player *feels*.]

---

## XVI. Series Arc State
<!-- Only relevant for series. Skip if standalone.
     Copy the latest row into specs/series-bible.md Character State Registry after each entry is completed. -->

| After Entry | Trust range (end) | Physical state | Knowledge state | Arc position | Emotional state | Notes |
|---|---|---|---|---|---|---|
| Game 1 | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | [NEEDS CLARIFICATION] | |
