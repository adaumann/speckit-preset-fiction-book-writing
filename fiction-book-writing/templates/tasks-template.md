# Writing Tasks: [STORY_TITLE]

<!-- Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE] -->
<!-- Total tasks: NNN | Scenes: NN | Arcs: P1 (NN), P2 (NN), P3 (NN) -->
<!-- Parallel opportunities: NN | MVP scope suggestion: Act I complete -->

---

## Task Format

```
- [ ] TXXX [P] [CA-n] Action: Description (`draft/{PREFIX}{phase}.{beat_number}_{ShortName}.md`)
```

- `[P]` — can be drafted in parallel with other `[P]` tasks in the same phase
- `[CA-n]` — character arc label (CA-1 = P1 protagonist, CA-2 = P2, etc.)
- No `[P]` marker = sequential dependency on prior task
- Output paths use the structure-aware chapter naming convention: `draft/{PREFIX}{phase}.{beat_number}_{ShortName}.md`
  - PREFIX comes from `constitution.md` plot structure: `A` (three-act), `JO` (heros-journey), `SC` (save-the-cat), `KT` (kishotenketsu), `FT` (freytag), `SL` (story-circle), `FA` (five-act), `P` (generic)
  - Phase digit: act/phase number (e.g., `1`, `2`, `3`)
  - Beat number: 3-digit sequential within each phase (e.g., `101`, `102`, `201`)
  - Short name: PascalCase, 2–4 words (e.g., `Awakening`, `BetrayalRevealed`, `SupremeOrdeal`)
  - Examples: `draft/A1.101_Awakening.md`, `draft/JO3.201_SupremeOrdeal.md`

**Audiodraft tasks** (only present when `OUTPUT_MODE` is `audiobook` or `both` in `constitution.md ## X`):
- Each prose draft task is immediately followed by a paired audiodraft task (no `[P]` — depends on prose draft)
- Format: `TXXX [CA-n] Audiodraft: Generate SSML draft — [Scene Name] → audiodraft/{CHAPTER_ID}_{ShortName}.md`
- Audiobook setup tasks (voice IDs, pronunciation lexicon) appear in Phase 1 before the critical checkpoint

---

## Phase 1: Research & World-Building

<!-- Complete before any drafting. Output goes to specs/[FEATURE_DIR]/ -->

- [ ] T001 Research: Complete world/domain research needed for authenticity (`research.md`)
- [ ] T002 [P] Profile: Write full character profile — P1 protagonist (wound, arc, voice signature, micro-obsession, contradiction) (`characters/[name].md`, register in `characters.md`)
- [ ] T003 [P] Profile: Write full character profiles — all P2/P3 characters (`characters/[name].md` each, register in `characters.md`)
- [ ] T004 World: Document world rules, locations with sensory anchors, internal logic (`world-building.md`)
- [ ] T005 Timeline: Lock chronological event order (fabula) including backstory events (`timeline.md`)
- [ ] T006 Order: Document narrative order (syuzhet) in `timeline.md` Syuzhet section if story is non-linear — skip if linear

## ⚠️ CRITICAL CHECKPOINT: Story Bible Complete

**Do not begin drafting until all Phase 1 tasks are complete.**

Verify before proceeding:
- [ ] `constitution.md` has no `[NEEDS CLARIFICATION]` markers
- [ ] All character voice signatures are distinct (Voice Homogeneity test: could scene from CA-1 be mistaken for CA-2? If yes, profiles are incomplete)
- [ ] All Chekhov items in spec.md have an assigned pay-off scene
- [ ] `timeline.md` has no contradictions
- [ ] Chosen plot structure is documented in `plan.md`

---

## Phase 2: Act I — Setup (≈25% of word count target)

<!-- Establish world, characters, inciting incident, first plot point.
     Chapter IDs use the structure-aware prefix convention from plan.md Scene Outline: `{PREFIX}{phase}.{beat}_{Name}` -->

- [ ] T007 [CA-1] Draft: Opening chapter — establish status quo and opening image (`draft/A1.101_Opening.md`)
- [ ] T008 [CA-1] Draft: Inciting incident — the event that disrupts the status quo (`draft/A1.102_IncitingIncident.md`)
- [ ] T009 [P] [CA-2] Draft: Introduce P2 subplot thread (`draft/A1.103_SubplotIntro.md`)
- [ ] T010 [CA-1] Draft: Protagonist's first response — shows want, hints at wound (`draft/A1.104_FirstResponse.md`)
- [ ] T011 [CA-1] Draft: First plot point — the threshold, life permanently changes (`draft/A1.105_FirstPlotPoint.md`)

**Phase 2 Checkpoint**: Does the dramatic question feel urgent? Would a reader continue?

---

## Phase 3: Act II-A — Rising Action (≈25%)

<!-- Protagonist enters new territory, faces first tests, midpoint commitment. -->

- [ ] T012 [CA-1] Draft: First test in the new situation (`draft/A2.201_FirstTest.md`)
- [ ] T013 [P] [CA-2] Draft: Subplot development — complicates main arc (`draft/A2.202_SubplotDev.md`)
- [ ] T014 [CA-1] Draft: Ally/mentor scene — protagonist gains skill or insight (`draft/A2.203_Ally.md`)
- [ ] T015 [CA-1] Draft: Midpoint — false peak or deep commitment raises stakes (`draft/A2.204_Midpoint.md`)

**Phase 3 Checkpoint**: Is the protagonist's internal wound beginning to surface under pressure?

---

## Phase 4: Act II-B — Dark Night (≈25%)

<!-- Internal flaw costs protagonist, all is lost, dark night of the soul. -->

- [ ] T016 [CA-1] Draft: Antagonist force escalates — protagonist's flaw is exploited (`draft/A2.205_Escalation.md`)
- [ ] T017 [P] [CA-2] Draft: Subplot reaches its own crisis (`draft/A2.206_SubplotCrisis.md`)
- [ ] T018 [CA-1] Draft: All is lost moment — the worst possible outcome seems assured (`draft/A2.207_AllIsLost.md`)
- [ ] T019 [CA-1] Draft: Dark night of the soul — protagonist confronts the internal wound (`draft/A2.208_DarkNight.md`)
- [ ] T020 [CA-1] Draft: Second plot point — protagonist must act or accept defeat (`draft/A2.209_SecondPlotPoint.md`)

**Phase 4 Checkpoint**: Has the protagonist genuinely changed, or merely survived? If merely survived, the dark night needs deeper interiority.

---

## Phase 5: Act III — Resolution (≈25%)

<!-- Climax, protagonist uses need (not just want), closing image. -->

- [ ] T021 [CA-1] Draft: Climax — primary confrontation using the thematic need, not just the want (`draft/A3.301_Climax.md`)
- [ ] T022 [P] [CA-2] Draft: Subplot resolution — intersects and complicates climax (`draft/A3.302_SubplotResolution.md`)
- [ ] T023 [CA-1] Draft: Immediate aftermath — cost and consequence (`draft/A3.303_Aftermath.md`)
- [ ] T024 [CA-1] Draft: Closing chapter — resonant contrast or echo of opening image (`draft/A3.304_Closing.md`)

**Phase 5 Checkpoint**: Does the closing image resonate with the opening image? Has every Chekhov item from spec.md paid off?

---

## Phase 6: Polish Pass

- [ ] T025 Continuity: Cross-check all `draft/` chapters against `timeline.md` for consistency errors
- [ ] T026 Continuity: Verify character voice distinction — run Voice Homogeneity test on all POV chapters in `draft/`
- [ ] T027 Continuity: Verify all Chekhov items introduced have paid off
- [ ] T028 Pacing: Verify act word-count proportions are within acceptable range (±5% of targets)
- [ ] T029 Theme: Read for theme — is it shown through behavior, never stated directly in dialogue?
- [ ] T030 Anti-AI: Scan all `draft/` chapters for prohibited phrases from constitution.md Anti-AI Filter
- [ ] T031 Endings: Verify all chapter endings are off-balance (no tidy summaries)
- [ ] T032 Resonance: Confirm opening chapter (`draft/A1.101_*.md`) and closing chapter (`draft/A3.30N_*.md`) form a meaningful contrast or echo

<!-- Audiodraft polish task — only present when OUTPUT_MODE is audiobook or both in constitution.md ## X -->
<!-- - [ ] T033 Audiodraft: Review all SSML files for pronunciation, break timing, and delivery hints against constitution.md ## X -->
