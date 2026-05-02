# Writing Tasks: [GAME_TITLE]

<!-- Spec: specs/spec.md | Flowmap: specs/flowmap.md | Generated: [GENERATION_DATE] -->
<!-- Total tasks: NNN | Outline: NN | Draft: NN | QA: NN | Export: NN | Parallel opportunities: NN -->

---

## Task Format

```
| TXXX | [P] Action: Description | NODE-ID | `output/path.md` |
```

- `[P]` � can be worked in parallel with other `[P]` tasks in the same phase (independent branches)
- No `[P]` marker = sequential dependency on prior task (check branch dependency in `flowmap.md`)
- Node IDs from `flowmap.md` (NODE-NNN, END-A, etc.)
- Output paths: `outlines/NODE-NNN.md` for outlines, `nodes/NODE-NNN.md` for drafts

---

## Phase 0 � Setup & Research

| ID | Task | Output | Priority |
|---|---|---|---|
| T001 | Generate `variables.md` � register all state variables from flowmap.md | `specs/[FEATURE_DIR]/variables.md` | high |
| T002 | Generate `mechanics.md` � configure active hook schemas from constitution.md | `specs/[FEATURE_DIR]/mechanics.md` | high |
| T003 | Generate `endings.md` � register all planned endings with condition requirements | `specs/[FEATURE_DIR]/endings.md` | high |
| T004 | Research: [RESEARCH_TOPIC_1] � resolve world/technical knowledge gap | `specs/[FEATURE_DIR]/world-building.md` | high |
| T005 | Research: [RESEARCH_TOPIC_2] | | medium |
| T006 | Document world-building � locations, objects, world rules, ambient states | `specs/[FEATURE_DIR]/world-building.md` | medium |
| T007 | Write NPC profiles � [NPC_NAME_1] (trust thresholds, states, bark lines) | `specs/[FEATURE_DIR]/characters/NPC-001.md` | medium |
| T008 | Write NPC profiles � [NPC_NAME_2] | `specs/[FEATURE_DIR]/characters/NPC-002.md` | medium |
| T009 | Write glossary � world terms and variable name register | `specs/[FEATURE_DIR]/glossary.md` | low |

---

## ? Phase 0 Critical Checkpoint

**Do not begin node outlining until all Phase 0 tasks are complete.**

Verify before proceeding:
- [ ] `specs/[FEATURE_DIR]/variables.md` complete � all variables declared with valid value ranges
- [ ] `specs/[FEATURE_DIR]/mechanics.md` complete � all active hooks configured
- [ ] `specs/[FEATURE_DIR]/endings.md` complete � all endings registered with prerequisite conditions traceable in `flowmap.md`
- [ ] All NPC profiles written � trust thresholds, state behaviors, and bark lines defined
- [ ] No unresolved OQ-NNN items blocking Act 1 outlining
- [ ] `flowmap.md` has no dead-end nodes or unreachable branches

**Diagnostic**: Can you trace a complete player path from the opening node to each registered ending? If not, the flowmap is incomplete.

---

## Phase 1 � Node Outlines (Act 1)

<!-- Generate node outlines for all Act 1 nodes. Status: DRAFT ? APPROVED before Phase 2. -->

| ID | Task | Node | Output |
|---|---|---|---|
| T010 | Outline: [NODE_TITLE] � opening, player orientation | NODE-001 | `outlines/NODE-001.md` |
| T011 | Outline: [NODE_TITLE] � first branching decision | NODE-002 | `outlines/NODE-002.md` |
| T012 | Outline: [NODE_TITLE] | NODE-003 | `outlines/NODE-003.md` |
| T013 | **Review & approve all Act 1 outlines** (status: DRAFT ? APPROVED) | Act 1 | � |

---

## Phase 2 � Node Drafting (Act 1)

<!-- speckit.implement gates on APPROVED outline status.
     [P] = can be drafted in parallel (independent branches). -->

| ID | Task | Node | Output |
|---|---|---|---|
| T014 | [P] Draft: [NODE_TITLE] | NODE-001 | `nodes/NODE-001.md` |
| T015 | [P] Draft: [NODE_TITLE] | NODE-002 | `nodes/NODE-002.md` |
| T016 | Draft: [NODE_TITLE] � depends on NODE-002 outcome | NODE-003 | `nodes/NODE-003.md` |

**Phase 2 Checkpoint**: Do Act 1 nodes establish the player's agency clearly? Are branching consequences distinct enough to make the first choice meaningful?

---

## Phase 3 � Node Outlines (Act 2)

| ID | Task | Node | Output |
|---|---|---|---|
| T020 | Outline: [NODE_TITLE] | NODE-[N] | `outlines/NODE-[N].md` |
| T021 | **Review & approve all Act 2 outlines** | Act 2 | � |

---

## Phase 4 � Node Drafting (Act 2)

| ID | Task | Node | Output |
|---|---|---|---|
| T022 | [P] Draft: [NODE_TITLE] | NODE-[N] | `nodes/NODE-[N].md` |

**Phase 4 Checkpoint**: Does Act 2 escalate variable states meaningfully? Are NPC relationship scores responding correctly to player decisions across branches?

---

## Phase 5 � Node Outlines (Act 3 / Endings)

| ID | Task | Node | Output |
|---|---|---|---|
| T030 | Outline: [CLIMAX_NODE_TITLE] | NODE-[N] | `outlines/NODE-[N].md` |
| T031 | Outline: Ending node � END-A ([ENDING_NAME]) | END-A | `outlines/END-A.md` |
| T032 | Outline: Ending node � END-B ([ENDING_NAME]) | END-B | `outlines/END-B.md` |
| T033 | **Review & approve all Act 3 / ending outlines** | Act 3 | � |

---

## Phase 6 � Node Drafting (Act 3 / Endings)

| ID | Task | Node | Output |
|---|---|---|---|
| T034 | Draft: [CLIMAX_NODE_TITLE] | NODE-[N] | `nodes/NODE-[N].md` |
| T035 | Draft: Ending � END-A ([ENDING_NAME]) | END-A | `nodes/END-A.md` |
| T036 | Draft: Ending � END-B ([ENDING_NAME]) | END-B | `nodes/END-B.md` |

**Phase 6 Checkpoint**: Can you trace a complete variable-state path from the opening node to each ending? Are all endings reachable without requiring incompatible variable combinations?

---

## Phase 7 � Quality Gates

| ID | Task | Scope |
|---|---|---|
| T040 | Run `speckit.analyze` � full branch audit (dead ends, unreachable nodes, undeclared variables) | All nodes |
| T041 | Run `speckit.checklist` for all nodes � choice meaningfulness, hook declarations, POV drift | All nodes |
| T042 | Run `speckit.continuity` � variable state consistency, branch reachability | All nodes |
| T043 | Revise flagged nodes (`speckit.revise`) | Failing nodes |
| T044 | Re-run `speckit.checklist` on revised nodes | Revised nodes |

---

## Phase 8 – Polish & Documentation

| ID | Task | Output |
|---|---|---|
| T050 | Review export warnings in node compiler output | – |
| T051 | Document final variable state log | `variables.md` |
