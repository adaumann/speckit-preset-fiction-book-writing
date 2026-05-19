# Writing Tasks: [STORY_TITLE]

<!-- Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE]
     LEGEND:
     - [P] Parallel task | [CA-n] Character Arc | TXXX Task ID
     - Path: draft/{PLOT_PREFIX}{ACT}.{BEAT}_{ShortName}.md
     - Prefix: A (3-Act), JO (Hero), SC (Cat), KT (Kisho), FT (Freytag), SL (Circle), FA (5-Act)
-->

---

## Phase 1: Pre-Production
<!-- Complete before drafting. -->

- [ ] T001 Research: World/domain research (`research.md`)
- [ ] T002 [P] Profile: P1 protagonist arc & voice (`characters/[name].md`)
- [ ] T003 [P] Profile: P2/P3 supporting cast (`characters/[name].md`)
- [ ] T004 World: Rules & sensory anchors (`world-building.md`)
- [ ] T005 Timeline: Chronological order/backstory (`timeline.md`)

## ⚠️ CHECKPOINT: Story Bible Complete
<!-- Verify constitution.md has no [NEEDS CLARIFICATION] and voice signatures are locked. -->

---

## Phase 2: Act I — Setup (≈25%)
<!-- Chapter IDs: {PREFIX}{phase}.{beat}_{Name} -->

- [ ] T007 [CA-1] Draft: Opening & Status Quo (`draft/A1.101_Opening.md`)
- [ ] T008 [CA-1] Draft: Inciting Incident (`draft/A1.102_IncitingIncident.md`)
- [ ] T009 [P] [CA-2] Draft: Subplot thread intro (`draft/A1.103_SubplotIntro.md`)
- [ ] T010 [CA-1] Draft: First Response (`draft/A1.104_FirstResponse.md`)
- [ ] T011 [CA-1] Draft: First Plot Point (`draft/A1.105_FirstPlotPoint.md`)

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
- [ ] T028 Statistics: Run `speckit.statistics` across all drafted chapters — review readability score, sentence length variance, passive voice %, adverb density, and dialogue balance; address CRITICAL flags before polishing
- [ ] T029 Pacing: Run `speckit.pacing` — verify tension arc shape; no sagging middle, climax scores ≥8, act-band alignment holds
- [ ] T030 Pacing: Verify act word-count proportions are within acceptable range (±5% of targets)
- [ ] T031 Theme: Read for theme — is it shown through behavior, never stated directly in dialogue?
- [ ] T032 Anti-AI: Scan all `draft/` chapters for prohibited phrases from constitution.md Anti-AI Filter
- [ ] T033 Endings: Verify all chapter endings are off-balance (no tidy summaries)
- [ ] T034 Resonance: Confirm opening chapter (`draft/A1.101_*.md`) and closing chapter (`draft/A3.30N_*.md`) form a meaningful contrast or echo

<!-- Audiodraft polish task — only present when OUTPUT_MODE is audiobook or both in constitution.md ## X -->
<!-- - [ ] T035 Audiodraft: Review all SSML files for pronunciation, break timing, and delivery hints against constitution.md ## X -->
