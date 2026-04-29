# Playtest Feedback Log: [GAME_TITLE]

<!-- Feedback from playtest sessions. Processed by speckit.feedback.
     Issues are categorized, mapped to node IDs, severity-rated, and converted to revision tasks.
     File: feedback/[tester-slug]-[YYYY-MM-DD].md -->

---

## Metadata

| Field | Value |
|---|---|
| Tester | [Name / anonymous] |
| Tester slug | [auto-computed from tester name — used in file name and task IDs, e.g. `alice`] |
| Session label | [PLAYTEST_SESSION_LABEL] |
| Playtest round | [N — matches `## Playtest Round N` section in tasks.md] |
| Date received | [YYYY-MM-DD] |
| Export target | [sugarcube / ink] |
| Nodes played | [e.g. "All", "NODE-001–NODE-015", "Act 1"] |
| Approximate play path | [KEY_CHOICES_TAKEN] |
| Status | [unprocessed / triaged / tasks generated / closed] |

---

## Raw Notes

<!-- Paste or transcribe the tester's notes verbatim here. -->
<!-- speckit.feedback will parse this section to create categorized issues. -->

```
[Paste raw playtest feedback here]
```

---

## Categorized Issues

<!-- Auto-populated by speckit.feedback. Do not edit manually. -->
<!-- ✅ = resolved  🔄 = in progress  ⬜ = open -->

### BR — Branch

<!-- Branching logic, dead ends, missing choices, unreachable paths, incorrect targets -->

| Issue ID | Severity | Node ID | Description | Status |
|---|---|---|---|---|
| BR-001 | CRITICAL / HIGH / MEDIUM / LOW | NODE-[N] | [DESCRIPTION] | open |

### VA — Variable

<!-- Variable read-before-set, wrong values, missing hook, trust not changing, flag not firing -->

| Issue ID | Severity | Node ID | Description | Status |
|---|---|---|---|---|
| VA-001 | | NODE-[N] | | open |

### PA — Pacing

<!-- Too slow, too fast, tension drop, arc imbalance, over-long node -->

| Issue ID | Severity | Node ID | Description | Status |
|---|---|---|---|---|
| PA-001 | | NODE-[N] | | open |

### CL — Clarity

<!-- Confusing prose, unclear choice labels, orientation failure, missing context -->

| Issue ID | Severity | Node ID | Description | Status |
|---|---|---|---|---|
| CL-001 | | NODE-[N] | | open |

### BA — Balance

<!-- Dominant choices, no meaningful trade-offs, trivial mechanics, no-cost decisions -->

| Issue ID | Severity | Node ID | Description | Status |
|---|---|---|---|---|
| BA-001 | | NODE-[N] | | open |

### CO — Continuity

<!-- Contradiction with world rules, NPC wrong state, POV drift, remembered-wrong error -->

| Issue ID | Severity | Node ID | Description | Status |
|---|---|---|---|---|
| CO-001 | | NODE-[N] | | open |

### EX — Export

<!-- Hook translation error, unsupported syntax, crashed output, wrong passage name -->

| Issue ID | Severity | Node ID | Description | Status |
|---|---|---|---|---|
| EX-001 | | NODE-[N] | | open |

### POS — Positive

<!-- What's working — keep these intentional, do not revise away -->

| Node ID | Note |
|---|---|
| NODE-[N] | [WHAT WORKED] |

---

## Severity Key

| Code | Meaning | Action |
|---|---|---|
| CRITICAL | Blocks progression, crashes export, breaks variable state | Fix before next playtest |
| HIGH | Significantly degrades experience (confusion, dominant choice, NPC contradiction) | Fix in current revision cycle |
| MEDIUM | Noticeable but non-blocking | Fix in polish pass |
| LOW | Minor preference — "nice to have" | Address if time allows; not added to tasks.md |

---

## Revision Tasks Generated

<!-- Auto-populated by speckit.feedback when tasks are generated. Maps to tasks.md entries. -->

| Issue ID | Task ID | Node ID | Action |
|---|---|---|---|
| BR-001 | [tester-slug·BR-001] | NODE-[N] | [REVISION_ACTION] |

---

## Resolution Log

<!-- Track which issues were fixed, in which node version, and how. -->

| Issue ID | Resolution | Node Version | Date |
|---|---|---|---|
| BR-001 | [RESOLUTION_DESCRIPTION] | NODE-[N]_v2.md | [DATE] |
