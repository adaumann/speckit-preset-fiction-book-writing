---
description: Interactive brainstorming session for any story topic — spec, plan, characters, relationships, themes, world-building, locations, series, glossary, pov, research, or timeline. Loads existing topic files and prior brainstorm notes as context, asks probing questions in a loop, and produces a brainstorm notes file, a patch to the topic file, or nothing if cancelled. Supports challenge mode (stress-tests existing file decisions) and quick/standard/deep session lengths.
handoffs:
  - label: Create Story Brief
    agent: speckit.specify
    prompt: Use these brainstorm notes to create a story brief
    send: true
  - label: Build Story Structure
    agent: speckit.plan
    prompt: Use these brainstorm notes to build the story structure
    send: true
  - label: Update Story Bible
    agent: speckit.constitution
    prompt: Apply these brainstorm findings to the story bible
    send: true
  - label: Clarify Story Brief
    agent: speckit.clarify
    prompt: Clarify the story brief using these brainstorm insights
    send: true
  - label: Draft POV Architecture
    agent: speckit.pov
    prompt: Draft the POV structure based on these brainstorm findings
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accepted arguments:
- A topic name (e.g. `locations`, `characters`, `themes`) — use as the initial topic and skip the topic prompt in Step 1.
- `character [name]` (e.g. `character mira`) — pre-fill `CHARACTER_NAME` and skip that sub-prompt.
- `challenge` — activate **Challenge Mode** after topic resolution: questions stress-test the loaded file's decisions rather than fill gaps (see Step 4a).
- A session length flag: `quick`, `standard`, or `deep` — skip the session length prompt in Step 3.
- Any combination of the above (e.g. `locations challenge quick`).

---

## Purpose

This command runs a free-form, question-driven brainstorming loop before any formal document work begins. It is designed to run **before `speckit.specify`** (idea stage) or **before `speckit.plan`** (structure stage), but it can target any existing story document to deepen or challenge its current state.

The session is fully opt-out: the user may cancel at any time with no side effects. Output is only written when the user explicitly commits at the end.

---

## Pre-Execution Checks

**Check for extension hooks (before brainstorming)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_brainstorm` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Topic Selection

If no topic was provided as an argument, display the topic menu:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BRAINSTORM — Topic Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What do you want to brainstorm?

   1  spec           — Story concept, logline, dramatic question
   2  plan           — Story structure, acts, chapter map
   3  characters     — Cast of characters, arcs, dynamics
   4  character      — A single specific character (you name them)
   5  themes         — Central themes, motifs, symbolic layer
   6  world-building — Setting rules, geography, culture, history
   7  locations      — Specific places, sensory anchors, atmosphere
   8  pov            — Narrative perspective, voice strategy
   9  research       — Factual grounding, open questions
  10  timeline       — Story chronology, scene durations, gaps
  11  series         — Series arc, canon, book-to-book continuity
  12  glossary       — Invented terms, proper nouns, spelling rules

  Type a number, a topic name, or a custom topic.
  Type  q  to quit without doing anything.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

- Accept both the number and the name as valid input.
- If the user types `4` or `character`, immediately ask: `Which character? (name or role)` and store the answer as `CHARACTER_NAME`.
- If the user types a free-form topic not on the list, accept it as a custom topic. Store it in `SESSION.topic`.
- If the user types `q`, exit cleanly with: `Brainstorm cancelled. No files were changed.`

---

## Step 2 — Context Load

Run `{SCRIPT}` from repo root and parse JSON for `FEATURE_DIR` and `SPECS_DIR`.

Resolve the **canonical file path** for the selected topic using the table below:

| Topic | Candidate file paths (check in order) |
|---|---|
| `spec` | `{FEATURE_DIR}/spec.md` |
| `plan` | `{FEATURE_DIR}/plan.md` |
| `characters` | `{FEATURE_DIR}/characters.md` (index), `{FEATURE_DIR}/characters/` (directory) |
| `character` | `{FEATURE_DIR}/characters/{CHARACTER_NAME}.md`, then fuzzy-match inside `{FEATURE_DIR}/characters/` |
| `themes` | `{FEATURE_DIR}/themes.md` |
| `world-building` | `{FEATURE_DIR}/world-building.md` |
| `locations` | `{FEATURE_DIR}/locations.md` |
| `pov` | `{FEATURE_DIR}/pov-structure.md` |
| `research` | `{FEATURE_DIR}/research.md` |
| `timeline` | `{FEATURE_DIR}/timeline.md` |
| `series` | `{FEATURE_DIR}/series/series-bible.md`, then `.specify/memory/series-bible.md` |
| `glossary` | `{FEATURE_DIR}/glossary.md` |
| `(custom)` | No canonical file — treat as a blank-slate topic |

**Resume check**:

Before proceeding to the file existence check, look for `{FEATURE_DIR}/brainstorm-[topic].md` (or `{FEATURE_DIR}/brainstorm-character-[CHARACTER_NAME].md` for the `character` topic).

- **Prior notes found**: Display:
  ```
  ↩ Prior brainstorm notes found for [topic] ([N] insights).
    (r) Resume — load prior notes; new questions will build on them
    (n) New session — start fresh (prior file kept on disk, not loaded)
  ```
  If `r`: read the file into `SESSION.prior_log`. Set `SESSION.resuming = true`.
  If `n`: proceed normally.

- **No prior notes**: proceed directly.

**Branch on file existence**:

- **File found**: Read the full file content. Set `SESSION.has_context = true`. Display:
  ```
  ✓ Found [filename] — I'll use this as context for the session.
  ```
  Summarise the document in 2–3 bullets (key decisions already locked in) so the user can confirm AI read it correctly before questions begin.

- **File not found**: Set `SESSION.has_context = false`. Display:
  ```
  ✗ No [filename] found — I'll start from scratch with foundational questions.
  ```

Also load `.specify/memory/constitution.md` if it exists — it applies to all topics as background context.

Load the following **secondary context files** silently (do not summarise unless a question directly touches them):

| Topic | Secondary files to load |
|---|---|
| `spec` | `constitution.md`, `characters.md` |
| `plan` | `spec.md`, `constitution.md` |
| `characters` / `character` | `spec.md`, `themes.md`, `constitution.md` |
| `themes` | `spec.md`, `characters.md` |
| `world-building` | `locations.md`, `research.md` |
| `locations` | `world-building.md`, `timeline.md` |
| `pov` | `spec.md`, `characters.md`, `constitution.md` |
| `research` | `spec.md`, `world-building.md` |
| `timeline` | `plan.md`, `characters.md` |
| `series` | `spec.md`, `plan.md` |
| `glossary` | `world-building.md`, `locations.md` |
| `(custom)` | None |

Use secondary files only to avoid asking about already-decided facts and to surface cross-topic conflicts during question selection.

---

## Step 3 — Session Start

**Session length** — if not already set via argument, ask:
```
How deep do you want to go?
  q  quick    — ~5 questions, highest-priority gaps only
  s  standard — ~10 questions, core coverage  (default)
  d  deep     — unlimited, follow every thread
```
Store in `SESSION.depth`. Default to `standard` if the user presses Enter.

Display the session header:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BRAINSTORM SESSION
  Topic    : [topic]  [✓ loaded from file | ✗ new topic]
  Mode     : [With context | Blank slate | Challenge]
  Depth    : [Quick · Standard · Deep]
  Resuming : [Yes — [N] prior insights loaded | No]  ← omit if not resuming
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Commands available at any time:
  done        — end session and choose what to do with notes
  cancel / q  — discard everything and exit
  switch      — change to a different topic (your current insights are preserved)
  summary     — show a running summary of insights so far
  !skip       — skip this question and move to the next one
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Initialise an internal **Insight Log** — an ordered list of brainstorm findings that grows throughout the session. Each entry records:
- The question asked
- The user's answer (verbatim key points)
- Any insight, tension, or contradiction the AI derived from the answer

---

## Step 4 — Brainstorm Loop

The loop runs until the user types `done`, `cancel`, or `switch`.

### 4a — Select the next question

**Depth gate**: if `SESSION.depth` is `quick` and N ≥ 5, or `standard` and N ≥ 10, surface a natural stopping point before asking another question:
```
That covers the core ground for [topic]. Type  done  to wrap up, or  !skip  to keep going.
```
Wait for the user. Only continue if they explicitly request it.

**Challenge mode**: if `SESSION.mode` is `Challenge`, invert the normal priority. Lead with questions that directly challenge the most confident decisions in the loaded file. Frame each as: *“Your [element] is [current value] — what is the strongest argument that this is wrong?”* Do not fabricate a counter-argument; only ask the question.

**Normal priority order**:

1. **Tension probe**: if the user’s previous answer introduced a contradiction — with the loaded file, a prior answer in this session, or the loaded `SESSION.prior_log` (if resuming) — probe that tension first.
2. **Gap probe**: identify the most important unanswered dimension for this topic (see question banks below) and ask about it.
3. **Depth probe**: if a previous answer was shallow or vague, ask a follow-up that specifically names the narrative function the element must serve.
4. **Wildcard**: once core gaps are covered, draw from the **Wildcard bank** for this topic (see question banks below) to unlock unexpected directions.

Never repeat a question already asked in this session or present in `SESSION.prior_log`. Never ask about something definitively answered in the loaded file — except in Challenge mode.

### 4b — Ask the question

Present one question at a time. Format:

```
[Q{N}]  {question text}

(done · cancel · switch · summary · !skip)
```

Where `{N}` is the sequential question number in this session.

After the user answers:
- Acknowledge in 1–2 sentences. The acknowledgement **must name at least one** of:
  - The **narrative function** this element serves (e.g. “That gives the wound a physical anchor in Act 1”)
  - The **tension it creates** with another locked decision (e.g. “This sits in tension with the timeline — she can’t have been in both places”)
  - A **specific scene beat or document section** it will affect (e.g. “This reshapes the midpoint directly”)
  Do not produce generic filler (“Interesting!”, “That’s a great point”, “Good thinking”).
- Log the Q&A pair and any derived insight into the Insight Log.
- If the answer conflicts with the loaded file or a prior answer in this session:
  ```
  ⚠  Conflict with [filename / Q{N}] — [brief description].
     Logged as Change Candidate [K].
  ```
- Proceed to 4a for the next question.

### 4c — Mid-loop commands

At any pause point the user may type:

| Command | Action |
|---|---|
| `done` | End the loop. Go to Step 5. |
| `cancel` / `q` | Discard all session data. Exit with: `Brainstorm cancelled. No files were changed.` |
| `switch` | Go back to Step 1. Display: `Your [N] insights for [old topic] are preserved and will appear in the final output.` The Insight Log for the old topic is labelled and kept. |
| `summary` | Display the current Insight Log as a structured summary without ending the session. Return to the loop after. |
| `!skip` | Skip this question without answering. Mark it as skipped in the log. Skipped questions do not count toward the depth limit. Go to 4a. |

---

## Question Banks

Use these banks to populate the question queue for each topic. Do not ask all questions — select the most valuable based on what is already known.

### `spec`
- What is the single most important thing that happens to the protagonist?
- What does the protagonist want vs. what do they actually need?
- What is the central dramatic question — the one sentence the whole book answers?
- What is the emotional promise to the reader? (e.g. catharsis, wonder, dread)
- What does the ending feel like — not what happens, but how it feels?
- What is the inciting incident and why does it destabilise the protagonist's world?
- What genre conventions does this story follow — and which does it subvert?

### `plan`
- Which plot structure are you using and why does it fit this story?
- Where is the midpoint reversal and what does it change?
- What is the darkest moment before the climax?
- Are there subplot arcs and how do they intersect the main plot?
- How many acts / phases do you need and what does each one do?
- What is the opening image and how does it echo the closing image?

### `characters` / `character`
- What is this character's core wound — the thing that happened before the story began?
- What does this character want (external goal) and what do they need (thematic truth)?
- What lie does this character believe about themselves or the world?
- What is the moment this character could change — and do they?
- How does this character speak differently from every other character?
- What is one thing about this character that would surprise the reader?
- What repeating behaviour pattern does this character fall into under pressure?
- Who in the cast challenges this character most — and why?

### `themes`
- What is the central thematic question the story poses without answering definitively?
- What is the dominant motif and where does it first appear?
- How is the theme expressed differently by the protagonist vs. the antagonist?
- Is there a false version of the theme that gets dismantled during the story?
- What symbol carries the thematic weight and how does it transform?

### `world-building`
- What is the single most important rule of this world — and what happens when it breaks?
- What does everyday life look like for ordinary people in this world?
- What is the history that the characters don't fully know but shapes their reality?
- What is a detail of this world that no similar story has used?
- What does this world cost its inhabitants — what is the everyday price of living here?

### `locations`
- What does this place smell like, sound like, feel like underfoot?
- What is the emotional register of this location — what do people feel when they enter?
- What happened here before the story started that the walls would remember?
- How does this location change between night and day, or across seasons?
- What is the one thing a character would always do or never do in this place?

### `pov`
- Whose perspective is primary and why is this story theirs to tell?
- If multiple POVs: what does each perspective know that the others don't?
- How do the narrative voices differ — what does each character notice that the others miss?
- Where does information asymmetry create the most dramatic tension?
- Are there events in the story that no current POV character can witness — how do you handle them?- What is each POV character’s greatest blind spot — what are they systematically wrong about?
- Does the narrative distance (intimate vs. distant) stay consistent, or does it shift — and if it shifts, where and why?
- What does the reader know that the POV character doesn’t, and when does that asymmetry close?
- Is there a character whose POV is deliberately withheld — what is the narrative cost and gain of that choice?
- How do you prevent reader confusion when switching POV — what are the grounding cues for each voice?
### `research`
- What is the one factual domain where getting it wrong would break reader trust?
- What real-world event, profession, or place is this story drawing from?
- What do you currently not know that you need to know before writing?
- Is there an expert reader (a nurse, a sailor, a historian) who would catch errors — what would they flag?
- What is a piece of authentic texture — a smell, a procedure, a sound — that only someone who was there would know?
- Is there a commonly held belief about this subject that is actually wrong — one the story could use or subvert?
- What is the emotional texture of the real-world domain you’re drawing from? Not just facts, but how it feels to live inside it?
- Which scene depends most heavily on research being correct — what breaks if you get it wrong?
- Are there legal, ethical, or sensitivity implications to how you portray this domain?

### `timeline`
- How much time does the story span — hours, months, decades?
- Are there time jumps — and what is revealed vs. hidden in the gap?
- What is the most time-pressured moment in the story?
- Does the narrative time (order of telling) differ from story time (order of events)?
- Are there two or more threads running simultaneously that must converge?

### `series`
- What state must each major character be in at the end of this book to set up the next?
- What series-level question does this book open without answering?
- What world rule is established in this book that must hold for the entire series?
- What is the series arc (across all books) vs. the book arc (resolved within this one)?
- Are there contradictions between this book's plan and the series bible?

### `glossary`
- What invented terms appear in the story that a reader would not intuitively understand?
- Are there proper nouns with multiple variant forms or spellings that need locking down?
- What real words are used with a story-specific meaning that differs from normal usage?
- Which term is most likely to be used inconsistently across a long draft — what are its variant forms?
- Are there terms that appear in dialogue — do they feel natural in a character’s mouth, or too technical, formal, or anachronistic?
- Which invented terms are load-bearing (plot or world-rule depends on their exact meaning) vs. flavour-only?
- Is there a term that feels forced or coined-for-the-sake-of-it — could it be replaced with something more organic?
- Are there terms borrowed from a real-world source (another language, a technical field) that carry unintended connotations?

### Wildcard bank

Draw from this bank once the topic’s core question gaps are covered. These apply to any topic and are designed to surface unexpected angles.

- If this story never got published and only you would ever read it, what would you add that you’re currently holding back?
- What is the most dangerous choice your protagonist could make right now — and what would it cost them?
- Which scene are you most afraid to write? What does that fear tell you about the story?
- What would happen if the antagonist were right?
- What does this story have to say that no other story has said in quite this way?
- Which supporting character is quietly trying to become the protagonist — should you let them?
- What would need to be true about the world for your ending to feel inevitable rather than just earned?
- What is the one thing the reader will carry out of this story years later — and are you building toward it deliberately?

---

## Step 5 — Session End

When the user types `done`, display the **Session Summary**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BRAINSTORM COMPLETE
  Topic    : [topic]
  Questions: [N] asked
  Insights : [M] logged
  Conflicts: [K] flagged  ← omit line if K = 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Key findings:
  • [1-sentence insight]
  • [1-sentence insight]
  • ...  (max 6 bullets, highest-value only)

What do you want to do with these results?

  1  Save brainstorm notes      — write a notes file alongside the topic file
  2  Update [topic file]        — apply findings and resolve conflicts directly
                                  (only shown if SESSION.has_context = true)
  3  Both                       — save notes AND update the topic file
  4  Merge all topics           — combine notes from every topic covered this session
                                  into one cross-topic brainstorm file
                                  (only shown if the user used  switch  at least once)
  5  Cancel                     — discard everything, no files written

```

Wait for the user's choice. If the user types `5` or `cancel`, exit with: `Brainstorm cancelled. No files were changed.`

---

## Step 6 — Output

### Option 1 or 3 — Save brainstorm notes

Determine the notes file path:
- If `SESSION.has_context = true`: write to `{FEATURE_DIR}/brainstorm-[topic].md`
  (e.g. `brainstorm-locations.md`, `brainstorm-character-mira.md`)
- If `SESSION.has_context = false` (blank slate): same path convention

Write the notes file with this structure:

```markdown
# Brainstorm Notes — [Topic]

<!-- Generated: [DATE] | Questions: [N] | Insights: [M] -->

## Session Summary

[2–3 sentence summary of what the session explored and what it surfaced]

## Key Insights

<!-- Highest-value findings, each with the question that triggered it -->

### [Short insight title]
**Question asked**: [Q text]
**Answer**: [verbatim key points from user]
**Derived insight**: [AI synthesis — what this means for the story]

[repeat block for each insight]

## Change Candidates

<!-- Only present if conflicts were flagged during the session -->
<!-- Each item states what the existing file says vs. what brainstorming suggests -->
<!-- Status: PENDING → APPLIED / SKIPPED / EDITED (updated during Step 6 interactive review) -->

| # | Existing ([filename]) | Brainstorm suggests | Priority | Status |
|---|---|---|---|---|
| 1 | [current statement] | [new direction] | HIGH / MED / LOW | PENDING |

## Open Questions

<!-- Things the brainstorm raised but did not resolve -->

- [ ] [open question]
- [ ] [open question]

## Raw Q&A Log

<!-- Full ordered record of every exchange in this session -->

**Q1**: [question]
**A**: [answer]

**Q2**: [question]
**A**: [answer]

[continue for all N questions]
```

Confirm to the user: `✓ Saved: {path to notes file}`

### Option 2 or 3 — Update topic file

Apply the brainstorm findings to the existing topic file:

1. **For each Change Candidate**: show the proposed edit (old text → new text) and ask the user to confirm before writing:
   ```
   Change [N] of [K]:
   File    : [filename]
   Current : [existing text snippet]
   Replace : [new text]
   Apply this change? (y / n / edit)
   ```
   - `y` — apply as shown
   - `n` — skip this change
   - `edit` — the user types the replacement text directly

2. **For each new insight that adds information without conflict**: append it to the appropriate section of the topic file. Do not restructure sections or reformat content not being changed.

3. After all changes are applied, display:
   ```
   ✓ Updated: [filename]
     [N changes applied, M skipped]
   ```

### Option 4 — Merge all topics

Only available if the user used `switch` at least once. Write a single cross-topic file:
- Path: `{FEATURE_DIR}/brainstorm-merged-[date].md`
- Structure: one `## [Topic]` section per topic covered in the session, each containing its Insight Log and Change Candidates in the standard format.
- Add a final `## Cross-Topic Connections` section listing insights from one topic that directly affect another (e.g. a character decision that conflicts with a world-building rule).
- Confirm: `✓ Saved: {path} ([N] topics merged, [M] cross-topic connections noted.)`

If no topic file exists and the user chose option 2 or 3, offer to create the file from the appropriate template instead:
```
No [filename] exists yet. Create it from the [topic] template and apply brainstorm findings? (y / n)
```
If `y`:
- Create the file from the appropriate preset template.
- For each section that maps to a brainstorm insight, replace the `[NEEDS CLARIFICATION]` or `[PLACEHOLDER]` token with the insight text.
- Leave all other `[NEEDS CLARIFICATION]` and `[PLACEHOLDER]` tokens intact — do not fill them with invented content.
- Confirm: `✓ Created: {path} ([N] sections populated from brainstorm, [M] left as template placeholders.)`

---

## Operating Rules

- **Never write any file until Step 6.** The entire loop is non-destructive.
- **One question at a time.** Never present multiple questions in a single turn.
- **No leading the witness.** Questions must be open-ended. Do not embed an assumed answer.
- **Stay on topic.** All questions must be relevant to `SESSION.topic`. Do not drift into other topics unless the user explicitly switches.
- **Honour the loaded file.** Do not contradict or silently ignore existing content. Surface conflicts explicitly as Change Candidates.
- **No fabrication.** Do not invent story facts. The AI’s role is to ask, synthesise, and reflect — not to author.
- **Depth is binding.** When the depth limit is reached, surface the stopping point — do not slip in extra questions without prompting.
- **Acknowledgements must be specific.** See Step 4b: every post-answer acknowledgement must name a narrative function, a tension, or an affected scene. Generic affirmations are not permitted.
- **Prior session data is read-only.** Loaded prior brainstorm notes inform question selection and conflict detection, but cannot be modified by the current session.
