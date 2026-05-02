# Node Quality Checklist: [NODE_ID]

<!-- Purpose: Quality gate for drafted node files — "unit tests for nodes"
     Created: [CREATION_DATE] | Node: [NODE_ID] | Status: [DRAFT / APPROVED]
     Checklist file: nodes/checklists/[NODE_ID]-checklist.md -->

<!-- IMPORTANT: This checklist validates node quality, not story events.
     ? = satisfied  ? = needs revision  ?? = marginal / discuss

     DO NOT check:
     - ? Whether the node matches the plan
     - ? Whether the plot is logical at this point
     - ? Whether the choices are "good" design choices

     DO check:
     - ? Whether the node structure is valid (all targets exist, variables declared)
     - ? Whether the prose works as prose
     - ? Whether mechanic hooks are correctly declared
     - ? Whether the node complies with the game bible -->

---

## NR — Node Rules

| # | Check | Status | Notes |
|---|---|---|---|
| NR-001 | Non-terminal node has = 2 choices under `## Choices` | | |
| NR-002 | All choice targets are valid node IDs (exist in `outlines/` or `nodes/`) | | |
| NR-003 | All variables in `variables_read` and `variables_set` are declared in `variables.md` | | |
| NR-004 | All mechanic hook blocks use valid syntax and registered hook types (per `mechanics.md`) | | |
| NR-005 | Tier 2 hook stubs include `// TIER 2 STUB` comment | | |
| NR-006 | No variable is read that cannot be set on any upstream path to this node | | |
| NR-007 | Ending nodes have no outgoing choices | | |
| NR-008 | Trust score changes are within the declared NPC range (per character profile) | | |
| NR-009 | Choices use export format: `- [Label](NODE_ID) <!-- condition -->` under `## Choices` | | |

---

## PR — Prose Rules

| # | Check | Status | Notes |
|---|---|---|---|
| PR-001 | POV is consistent with `constitution.md` `player_perspective` (or has approved override) | | |
| PR-002 | No prohibited phrases from `constitution.md` appear in prose | | |
| PR-003 | Choice labels use active verb phrases; no meta-language (e.g. not "Select option") | | |
| PR-004 | Dialogue register matches NPC trust state at this node's variable value | | |
| PR-005 | Prose coheres without hook blocks (narrative reads as complete if mechanics are removed) | | |
| PR-006 | At least one concrete sensory detail (sound, smell, texture, temperature — not visual only) | | |
| PR-007 | No choice is telegraphed or trivialized by the prose (player's decision space is respected) | | |
| PR-008 | Prose tense, sentence rhythm, and vocabulary register are consistent with Prose Style Mode (Section VII of `constitution.md`); anti-AI filter patterns are absent | | |

---

## MC — Mechanic Compliance

| # | Check | Status | Notes |
|---|---|---|---|
| MC-001 | Every trust-shifting choice has narrative justification in prose | | |
| MC-002 | No single choice dominates trivially — all choices are meaningful trade-offs | | |
| MC-003 | Timer failure conditions are handled in a downstream node (or flagged `[NEEDS NODE]`) | | |
| MC-004 | (--strict only) Tier 2 stub hooks include a `// TODO:` comment describing expected implementation | | |
| MC-005 | No mechanic hook reads a variable not listed in `variables_read` in the frontmatter | | |
| MC-006 | Every `MECHANIC:CURRENCY` hook includes `variable=` and that variable is `type: currency` in `variables.md` | | |

---

## GB — Game Bible Compliance

| # | Check | Status | Notes |
|---|---|---|---|
| GB-001 | Node tone matches the genre and emotional register defined in `constitution.md` | | |
| GB-002 | Any NPC in this node is consistent with their character profile (voice, state, goal) | | |
| GB-003 | World-rule constraints (from `world-building.md`) are not violated in prose or choice outcomes | | |
| GB-004 | Engine target constraints are respected (no unsupported syntax for the declared export target) | | |

---

## RTG — Overall Rating

<!-- Score each section 1–10 based on how many items pass.
     Apply weights to compute the weighted total.
     Score = 7 is required to PASS. Hard-fail gates override the score. -->

| Section | Weight | Score (1–10) | Rationale |
|---|---|---|---|
| Node Rules (NR) | 30% | | |
| Prose Rules (PR) | 25% | | |
| Mechanic Compliance (MC) | 25% | | |
| Game Bible Compliance (GB) | 20% | | |

**Weighted Total**: [calculated score] / 10

| Gate | Result |
|---|---|
| Score = 7 | ? PASS / ? FAIL |
| NR-002 — all choice targets valid | ? PASS / ? FAIL |
| NR-006 — no unreadable variable | ? PASS / ? FAIL |
| NR-009 — choices format correct for export.py | ? PASS / ? FAIL |

**Verdict**: [PASS — node may proceed to APPROVED / FAIL — must revise before approval]

**Top revision priorities** (if FAIL or score < 8):
1. [Highest-impact item to fix — cite rule code]
2. [Second priority]
3. [Third priority if applicable]

---

## Notes

[Free-form notes on revision priorities, edge cases, or decisions made during checklist review]
