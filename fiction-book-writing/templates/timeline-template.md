# Timeline: [STORY_TITLE]

<!-- Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE] -->
<!-- Two layers: Fabula (chronological event order) and Syuzhet (narrative order as told).
     Complete Fabula first. Syuzhet only required if story is non-linear. -->

---

## Temporal Parameters

| Parameter | Value |
|---|---|
| Story span (real time covered) | [NEEDS CLARIFICATION] |
| Backstory span (pre-story events that matter) | [NEEDS CLARIFICATION] |
| Narrative non-linearity | [linear / flashbacks / dual-timeline / fragmented] |
| Calendar system | [real-world Gregorian / fictional / relative ("Day 1")] |
| Time-of-day sensitivity | [yes — scenes depend on light/shift/tide/etc. / no] |

---

## Fabula — Chronological Event Order

<!-- Every event in the order it actually happened, including backstory.
     Events the reader never sees directly still belong here if they cause plot.
     Format: [DATE_OR_OFFSET] | [EVENT] | [Affects arc / scene beat] -->

### Backstory (before story opens)

| Date / Offset | Event | Arc / Impact |
|---|---|---|
| [e.g., "–15 years"] | [e.g., "P1's father disappears at sea"] | [P1 wound] |
| | | |

### Story Period

| Date / Offset | Event | Beat ID | Arc |
|---|---|---|---|
| [Day 1 / Chapter 1 equivalent] | [Status quo opening event] | A1.101 | P1 |
| | | | |

---

## Syuzhet — Narrative Order

<!-- Only complete this section if the story is non-linear.
     Maps the order events are presented to the reader vs. when they happened.
     If linear, mark this section: "N/A — story is told in chronological order." -->

| Narrative Position | Event | Fabula Date | Technique |
|---|---|---|---|
| [Opening scene] | | | [in medias res / flashback / etc.] |
| | | | |

---

## Continuity Constraints

<!-- Hard rules derived from the timeline that drafting must not violate.
     speckit.continuity checks these. One row per constraint. -->

| Constraint ID | Rule | Enforced at Beat |
|---|---|---|
| TC-001 | [e.g., "P1 cannot know about X until scene A2.203"] | A2.203 |
| TC-002 | | |

---

## Unresolved Contradictions

<!-- Use this section to flag timeline conflicts before they reach draft stage.
     Mark RESOLVED once fixed. -->

| ID | Conflict | Status |
|---|---|---|
| TX-001 | [e.g., "Backstory says father died in winter; A1.102 references a summer funeral"] | OPEN |

---

## Chekhov Register

<!-- Every object, fact, or detail introduced early that must pay off later.
     Cross-reference with spec.md Key Scenes. -->

| Item | Introduced at | Pay-off scene | Status |
|---|---|---|---|
| [e.g., "The locked drawer"] | A1.101 | A3.301 | PENDING |
