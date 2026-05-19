---
chapter_id: [e.g. A1.101 / JO3.201 / SC.101]
chapter_name: [Short title — 2–4 words]
pov_character: [Character name]
pov_type: [3rd person limited / 1st person / 3rd person omniscient]
act_phase: [Act I / Act II-A / Act II-B / Act III]
plot_structure_stage: [e.g. Inciting Incident / Midpoint / All Is Lost]
timeline_position: [e.g. Day 3, late afternoon]
setting: [Location name — maps to LOC-NNN in locations.md]
estimated_words: [number]
status: DRAFT
# Change status to APPROVED when the outline is correct and ready to draft.
# Use SKIP if you will write this chapter yourself (no AI prose will be generated).
# You can also bypass this outline entirely with: /speckit.implement --dismiss-outline <CHAPTER_ID>

## Required Context
<!-- Populated by speckit.outline. Documents and sections needed for drafting this scene. -->
<!-- speckit.implement will use these to query only the necessary context via RAG. -->

### Documents Needed
- [ ] constitution.md §VII (Tone, Target Audience, Tense, Sentence Rhythm, Language)
- [ ] constitution.md §IX (Anti-AI Filter)
- [ ] constitution.md §VI (Active prose profile)
- [ ] characters/[pov_character].md (full profile)
- [ ] characters/[secondary_char].md (if present)
- [ ] locations.md LOC-[NNN] (if setting exists)
- [ ] timeline.md (timeline_position section)
- [ ] themes.md (active motif for this phase)
- [ ] plan.md ## Scene Outline (this chapter's entry)
- [ ] spec.md (character arcs, Key Scenes)
- [ ] craft-rules.md (Dirt Rule, Triple Purpose, Oblique Dialogue)
- [ ] [Other: specify file and section]

### RAG Query Suggestions
<!-- Use these queries when .specify/index/ exists -->
- "[pov_character] voice register micro-obsession arc state"
- "[setting] sensory anchors atmosphere dirt rule"
- "[active_motif] thematic delivery"
- "[chapter_id] [pov_character] scene context"
---

## Opening Hook

[One sentence: the first image, action, or sensory detail the reader encounters. Must place the POV character in motion, not in reflection.]

## Beat Sequence

Ordered beats from entry to exit. Each beat must follow causally from the previous one.

1. [Entry beat — what is already in motion when we arrive]
2. [Complication or escalation — what changes or resists]
3. [Pivot — the moment the scene's direction shifts]
4. [Decision or revelation — the beat that makes the next scene necessary]
5. [Exit beat — the closing image; must leave the scene in a new instability]

> Add or remove beats as needed. Minimum 3, no hard maximum. Keep each beat to one sentence — this is a brief, not prose.

## Character Beats

What each character present needs, does, and fails to get in this scene. Include only characters with a significant presence.

- **[Character Name]** (POV): wants — [goal entering the scene] / gets — [actual outcome]
- **[Character Name]**: function in this scene — [what they represent, oppose, or reveal]

## Dialogue Requirements

List exchanges that MUST occur. Do not write the dialogue itself — note what must be communicated, deflected, or left unspoken.

- **[Character A → B]**: must surface [topic] — the honest answer must be avoided or deflected
- **[Character B → A]**: the word-failure moment — [what cannot be named directly]

> If no dialogue is required, write: `No dialogue required — silent scene.`

## Sensory Anchors

The scene must be grounded in at least two senses. List the primary anchors.

- **Sight**: [dominant visual — avoid generic; be specific to this setting and moment]
- **Sound / Touch / Smell / Taste**: [at least one non-visual anchor]
- **Dirt Rule detail**: [one imperfection, wear mark, or asymmetry from locations.md — or note as TBD]

## Thematic Work

Which motif or thematic strand is active in this scene? How is it carried through action and image?

- **Active motif**: [name from themes.md, e.g. MTF-002 — The Locked Room]
- **Delivery method**: [action / object / spatial relationship / silence — never via stated dialogue]

## Story Bible Compliance Notes

Optional. Note any constitution.md constraints particularly relevant to this scene (prohibited patterns, style markers to watch for, POV distance rules, etc.).

- [Note or leave blank]

## Deviations from plan.md

If this outline changes anything from the plan, record it here before APPROVING. The plan must be updated first.

- [None / describe any structural change]
