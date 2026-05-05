---
description: Interactive brainstorming session for any game narrative topic — spec, plan, characters, branches, endings, mechanics, world-building, variables, or series. Loads existing files as context, asks probing questions in a loop, and produces a brainstorm notes file, a patch to the topic file, or nothing if cancelled. Supports challenge mode and quick/standard/deep session lengths.
handoffs:
  - label: Create Narrative Design Doc
    agent: speckit.specify
    prompt: Use these brainstorm notes to create the narrative design doc
    send: true
  - label: Build Plan
    agent: speckit.plan
    prompt: Use these brainstorm notes to build the plan and act structure
    send: true
  - label: Clarify Open Questions
    agent: speckit.clarify
    prompt: Clarify the narrative design doc using these brainstorm insights
    send: true
  - label: Generate Node Outline
    agent: speckit.outline
    prompt: Use these brainstorm notes to outline the target node
    send: true
---

# speckit.brainstorm

Run an interactive, question-driven brainstorming session on any aspect of the game narrative. Produces a notes file, applies findings to an existing spec file, or does nothing if cancelled. All file writes happen only at session end.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- A topic name (e.g. `branches`, `characters`, `endings`) — skip the topic prompt
- `node NODE-003` — pre-fill node ID as the brainstorm target
- `npc [name]` — pre-fill NPC name as the brainstorm target
- `challenge` — activate Challenge Mode: questions stress-test existing file decisions
- A session length flag: `quick`, `standard`, or `deep` — skip the session length prompt
- Any combination (e.g. `endings challenge quick`)

## Pre-Execution Checks

**Check for extension hooks (before brainstorming)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_brainstorm` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Topic Selection

If no topic was provided as an argument, display the topic menu:

```
---------------------------------------------
  BRAINSTORM — Topic Selection
---------------------------------------------

  What do you want to brainstorm?

   1  spec           — Game concept, premise, dramatic question
   2  plan           — Act structure, branches, node graph
   3  characters     — NPC cast, arcs, trust dynamics
   4  npc            — A single specific NPC (you name them)
   5  branches       — Choice design, branch alternatives, gate logic
   6  endings        — Ending conditions, reachability, emotional payoff
   7  mechanics      — Hook types, mechanic applications, variable design
   8  world-building — Setting rules, locations, factions, ambient states
   9  variables      — Variable registry, carry-over design, state logic
  10  series         — Series arc, carry-over canon, entry-to-entry continuity
  11  glossary       — In-world terms, proper nouns, variable naming

  Type a number, a topic name, or a custom topic.
  Type  q  to quit without doing anything.
---------------------------------------------
```

- Accept both number and name as valid input.
- If the user types `4` or `npc`, immediately ask: `Which NPC? (name or ID)` and store as `NPC_NAME`.
- If the user types `node NODE-NNN`, store the node ID as the brainstorm target.
- Free-form topics not on the list are accepted as custom topics.
- `q` exits with: `Brainstorm cancelled. No files were changed.`

---

## Step 2 — Context Load

Run `{SCRIPT}` from repo root and parse JSON for spec file paths.

Resolve the **canonical file path** for the selected topic:

| Topic | Candidate file paths (check in order) |
|---|---|
| `spec` | `specs/spec.md` |
| `plan` | `specs/plan.md` |
| `characters` | `specs/characters/` (directory index) |
| `npc` | `specs/characters/[NPC_NAME].md`, then fuzzy-match in `specs/characters/` |
| `branches` | `specs/plan.md`, then target node's `outlines/[NODE_ID].md` |
| `endings` | `specs/endings.md` |
| `mechanics` | `specs/mechanics.md` |
| `world-building` | `specs/world-building.md` |
| `variables` | `specs/variables.md` |
| `series` | `series/series-bible.md` |
| `glossary` | `specs/glossary.md` |
| `(custom)` | No canonical file — blank-slate topic |

**Resume check**: look for `specs/brainstorm-[topic].md` (or `specs/brainstorm-npc-[NPC_NAME].md`).
- Found: offer `(r) Resume` or `(n) New session`. If `r`: load prior notes into `SESSION.prior_log`.
- Not found: proceed.

**Branch on file existence**:
- **File found**: read it. Set `SESSION.has_context = true`. Summarise in 2–3 bullets so the user can confirm the AI read it correctly.
- **File not found**: set `SESSION.has_context = false`. Display: `? No [filename] found — starting from scratch.`

Load these **secondary context files** silently (use only to avoid re-asking settled facts and to surface cross-topic conflicts):

| Topic | Secondary files |
|---|---|
| `spec` | `.specify/memory/constitution.md` |
| `plan` | `specs/spec.md`, `specs/endings.md` |
| `characters` / `npc` | `specs/spec.md`, `specs/plan.md` |
| `branches` | `specs/spec.md`, `specs/variables.md`, `specs/mechanics.md` |
| `endings` | `specs/plan.md`, `specs/variables.md` |
| `mechanics` | `.specify/memory/constitution.md`, `specs/variables.md` |
| `world-building` | `specs/spec.md`, `specs/variables.md` |
| `variables` | `specs/plan.md`, `specs/mechanics.md` |
| `series` | `specs/spec.md`, `specs/endings.md` |
| `glossary` | `specs/world-building.md`, `specs/variables.md` |
| `(custom)` | None |

---

## Step 3 — Session Start

If session length not set via argument, ask:
```
How deep do you want to go?
  q  quick    — ~5 questions, highest-priority gaps only
  s  standard — ~10 questions, core coverage  (default)
  d  deep     — unlimited, follow every thread
```

Display session header:
```
---------------------------------------------
  BRAINSTORM SESSION
  Topic    : [topic]  [? loaded from file | ? new topic]
  Mode     : [With context | Blank slate | Challenge]
  Depth    : [Quick · Standard · Deep]
  Resuming : [Yes — [N] prior insights loaded | No]
---------------------------------------------
Commands available at any time:
  done        — end session and choose what to do with notes
  cancel / q  — discard everything and exit
  switch      — change topic (current insights preserved)
  summary     — show running insight summary
  !skip       — skip this question
---------------------------------------------
```

Initialise an **Insight Log** — ordered list of Q&A pairs plus derived insight and any conflict flags.

---

## Step 4 — Brainstorm Loop

Runs until the user types `done`, `cancel`, or `switch`.

### 4a — Select the next question

**Depth gate**: if `quick` and N = 5, or `standard` and N = 10, surface a stopping point before continuing.

**Challenge mode**: lead with questions that stress-test the most confident decisions in the loaded file. Frame as: *"Your [element] is [current value] — what is the strongest argument this is wrong?"*

**Normal priority order**:
1. **Tension probe**: if the previous answer introduced a contradiction with the loaded file or a prior answer, probe that tension first.
2. **Gap probe**: identify the most important unanswered dimension for this topic (see question banks) and ask about it.
3. **Depth probe**: if a previous answer was vague, follow up by naming the narrative or mechanical function the element must serve.
4. **Wildcard**: once core gaps are covered, draw from the Wildcard bank.

Never repeat a question or ask about something definitively answered in the loaded file (except in Challenge mode).

### 4b — Ask the question

```
[Q{N}]  {question text}

(done · cancel · switch · summary · !skip)
```

After the user answers:
- Acknowledge in 1–2 sentences. The acknowledgement **must name at least one** of:
  - The **narrative or mechanical function** this element serves
  - The **tension it creates** with another locked decision
  - A **specific node, variable, or spec section** it will affect
  Do not produce generic filler.
- Log the Q&A pair and derived insight into the Insight Log.
- If the answer conflicts with the loaded file or a prior answer:
  ```
  ?  Conflict with [filename / Q{N}] — [brief description].
     Logged as Change Candidate [K].
  ```

### 4c — Mid-loop commands

| Command | Action |
|---|---|
| `done` | End loop. Go to Step 5. |
| `cancel` / `q` | Discard all data. Exit: `Brainstorm cancelled. No files were changed.` |
| `switch` | Return to Step 1. Prior insights preserved and labelled. |
| `summary` | Display current Insight Log. Return to loop after. |
| `!skip` | Skip question; doesn't count toward depth limit. |

---

## Question Banks

Select the most valuable questions based on what is already known — do not ask all.

### `spec`
- What is the central dramatic question — the one sentence the whole game answers?
- What is the player's core agency in this story — what can they actually change?
- What genre conventions does this game follow — and which does it subvert?
- What is the emotional promise to the player? (e.g. tension, catharsis, discovery)
- What must the ending feel like — not what happens, but what it resolves?

### `plan`
- What is the shape of the branch graph — wide-then-narrow, tree, parallel paths?
- Where is the point of no return — the node where all paths converge?
- Are there nodes the player is likely to miss entirely — is that intentional?
- How does the act structure create escalating stakes across the node graph?
- Which branches are purely cosmetic vs. which create genuinely different story outcomes?

### `characters` / `npc`
- What does this NPC want from the player — and what do they actually need?
- What is the lie this NPC believes about themselves or the world?
- How does this NPC's behaviour change based on trust level?
- What is the most surprising thing this NPC would do under pressure?
- How does this NPC speak differently from every other character in the game?
- What state change for this NPC has the most downstream narrative impact?

### `branches`
- What makes choice A genuinely different from choice B — not just cosmetically?
- What is the player actually trading off when they pick each option?
- Is there an obviously dominant choice — and if so, how do you rebalance it?
- What information does the player need to make this choice meaningfully?
- What are the downstream consequences that make this branch matter two acts later?
- Are there conditional choices here — what variable gates them and why?

### `endings`
- What variable states does this ending require — and can they all be achieved on one path?
- What is the emotional register of this ending — how should the player feel?
- Is this ending clearly distinguishable from the others — what makes it unique?
- What does this ending say about the player's choices throughout the game?
- Is this ending reachable by a player who isn't trying to find it?
- What is the minimum set of choices that locks this ending in vs. others?

### `mechanics`
- What narrative experience does this mechanic create — what does it feel like to the player?
- Is this mechanic Tier 1 (export-ready) or Tier 2 (requires custom implementation)?
- How does this mechanic interact with the player's sense of agency and consequence?
- What is the failure mode of this mechanic — what breaks if it's misapplied?
- Are there nodes where this mechanic would feel forced or gamey — how do you avoid them?

### `world-building`
- What is the single most important rule of this world — what happens when it breaks?
- What does everyday life look like for the people who live here?
- What history do the characters not fully know but that shapes their reality?
- What does this world cost its inhabitants — what is the everyday price of living here?
- Which world rule has the most impact on the branch structure and variable design?

### `variables`
- Is this variable tracking player behaviour, world state, or NPC relationship — are those categories clean?
- What is the default value for this variable on a fresh playthrough — is it the right narrative assumption?
- Are there variable combinations that produce contradictions or unreachable nodes?
- Which variable has the most downstream impact on ending conditions?
- Is any variable doing double duty — tracking two things at once — that should be split?

### `series`
- What variable states must carry over to Entry N+1 — and what is the canonical default for a fresh start?
- What world rule established in this entry must not be contradicted in later entries?
- Which NPC survival or state has the most downstream impact on series continuity?
- What series-level question does this entry open without answering?
- Are there contradictions between this entry's endings and the series bible?

### `glossary`
- What invented terms appear in node prose that a player would not intuitively understand?
- Are there in-world variable names visible to the player that need consistent spelling?
- Which term is most likely to be used inconsistently across a long set of nodes?
- Are there terms that appear in choice labels — do they feel natural and unambiguous?

### Wildcard bank

- Which node are you most unsure about — what is the design question it hasn't answered yet?
- What would the player do if they could break one rule in this world?
- Which ending is currently least satisfying — what would make it feel earned?
- What mechanic are you avoiding implementing because it feels too complex — is the complexity actually worth it?
- What is the one NPC relationship that has the most unrealised narrative potential?
- Which branch currently feels like a trap rather than a choice — and why?
- What does this game have to say that no similar game has said in quite this way?

---

## Step 5 — Session End

When the user types `done`:

```
---------------------------------------------
  BRAINSTORM COMPLETE
  Topic    : [topic]
  Questions: [N] asked
  Insights : [M] logged
  Conflicts: [K] flagged
---------------------------------------------

Key findings:
  • [1-sentence insight]
  • ...  (max 6 bullets)

What do you want to do with these results?

  1  Save brainstorm notes      — write notes file alongside the topic file
  2  Update [topic file]        — apply findings and resolve conflicts directly
                                  (only shown if SESSION.has_context = true)
  3  Both                       — save notes AND update the topic file
  4  Merge all topics           — combine notes from every topic this session
                                  (only shown if user used  switch  at least once)
  5  Cancel                     — discard everything, no files written
```

---

## Step 6 — Output

### Option 1 or 3 — Save brainstorm notes

Write to `specs/brainstorm-[topic].md` (or `specs/brainstorm-npc-[NPC_NAME].md`):

```markdown
# Brainstorm Notes — [Topic]

<!-- Generated: [DATE] | Questions: [N] | Insights: [M] -->

## Session Summary

[2–3 sentences on what the session explored and what it surfaced]

## Key Insights

### [Short insight title]
**Question asked**: [Q text]
**Answer**: [verbatim key points]
**Derived insight**: [AI synthesis — what this means for the design]

[repeat block per insight]

## Change Candidates

| # | Existing ([filename]) | Brainstorm suggests | Priority | Status |
|---|---|---|---|---|
| 1 | [current content] | [new direction] | HIGH / MED / LOW | PENDING |

## Open Questions

- [ ] [unresolved question]

## Raw Q&A Log

**Q1**: [question]
**A**: [answer]

[continue for all N questions]
```

### Option 2 or 3 — Update topic file

For each Change Candidate: show proposed edit (old ? new) and ask for confirmation before writing:
```
Change [N] of [K]:
File    : [filename]
Current : [existing text snippet]
Replace : [new text]
Apply this change? (y / n / edit)
```
For new insights that add information without conflict: append to the appropriate section. Do not restructure sections not being changed.

If no topic file exists and the user chose option 2 or 3: offer to create from the appropriate template and populate `[NEEDS CLARIFICATION]` tokens with brainstorm findings. Leave all other placeholders intact.

### Option 4 — Merge all topics

Write `specs/brainstorm-merged-[date].md` with one `## [Topic]` section per topic covered, plus a `## Cross-Topic Connections` section linking insights that affect multiple files (e.g. a variable design decision that changes an ending condition).

---

## Operating Rules

- **Never write any file until Step 6.** The entire loop is non-destructive.
- **One question at a time.** Never present multiple questions in a single turn.
- **No leading the witness.** Questions must be open-ended — do not embed an assumed answer.
- **Honour the loaded file.** Do not contradict or silently ignore existing content. Surface conflicts as Change Candidates.
- **No fabrication.** Do not invent design decisions. Ask, synthesise, and reflect — do not author.
- **Depth is binding.** When the depth limit is reached, surface the stopping point — do not slip in extra questions.
- **Acknowledgements must be specific.** Every post-answer acknowledgement must name a narrative function, a mechanical implication, or an affected node/variable. Generic affirmations are not permitted.
- **Prior session data is read-only.** Prior brainstorm notes inform question selection and conflict detection but cannot be modified by the current session.

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_brainstorm` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

