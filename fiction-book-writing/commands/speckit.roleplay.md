---
description: Interactive multi-role play-through of an outline or draft chapter. AI identifies all roles in the scene (Author, Lector, scene characters, and more), assigns each to AI or user, then walks through the chapter beat by beat — pausing for Q&A and committing insights back as revision notes. Includes Dialog Workshop mode: speaker-turn segments, live character improvisation, and a Subtext Tracker role.
handoffs:
  - label: Revise Draft
    agent: speckit.revise
    prompt: Apply roleplay revision notes to the draft chapter
    send: true
  - label: Update Outline
    agent: speckit.outline
    prompt: Regenerate the scene outline incorporating roleplay feedback
    send: true
  - label: Continue Drafting
    agent: speckit.implement
    prompt: Draft the next scene
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- `[CHAPTER_ID]` — play through a specific scene (e.g. `A1.101`). The command resolves to the outline file (`outlines/<CHAPTER_ID>_<ChapterName>-outline.md`) if present, otherwise to the draft file (`draft/<CHAPTER_ID>_<ChapterName>.md`).
- `[CHAPTER_ID] outline` — force outline mode even when a draft exists
- `[CHAPTER_ID] draft` — force draft mode even when only an outline exists
- `[CHAPTER_ID] dialog` — enter **Dialog Workshop mode**: segments by speaker turn, live character improvisation, Subtext Tracker active (see Step 5-DW)
- `[CHAPTER_ID] tension` — run a **Tension Curve** analysis pass after the full play-through (see Step 5-TC); compatible with all other modes
- `[CHAPTER_ID] pick` — show the **Section Picker** before the session begins: lists all detected segments with a one-line summary and lets the user choose which to include (see Step 1b)
- `[CHAPTER_ID] [N]-[M]` — play only segments N through M (e.g. `A1.101 3-7`); skips Section Picker
- *(no argument)* — use the most recently modified outline or draft file in `FEATURE_DIR`

Any mode flag (`outline`, `draft`, `dialog`, `tension`) may be combined with `pick` or a range, e.g. `A1.101 dialog pick` or `A1.101 tension 4-9`.

---

## Purpose

This command turns the static text of a scene outline or draft chapter into a live, multi-voice reading session. Different stakeholder **roles** react to the text from their own perspective, surface problems, and generate revision insights — all without leaving the story-writing workflow.

The session proceeds in **segments** (a segment is one beat, one paragraph, or one dialogue block, whichever is shorter). After each segment the session **pauses** and waits for the user to act. Accumulated insights from the session are written back to the source file as structured revision notes when the user ends the session.

**Dialog Workshop mode** is a focused sub-mode for developing and stress-testing dialogue exchanges. It segments by individual speaker turn, enables live character improvisation (you play a character and respond naturally; AI responds as the other), and activates the **Subtext Tracker** role that runs silently in the background and logs what each character is *not* saying after each turn.

---

## Pre-Execution Checks

**Check for extension hooks (before roleplay)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_roleplay` key
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Setup

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Resolve the **target file**:
1. Parse `$ARGUMENTS` for a chapter ID, optional mode flag, and optional scope flag (`pick` or `N-M` range).
2. If no argument: use the most recently modified file in `FEATURE_DIR/outlines/` or `FEATURE_DIR/draft/`, preferring outlines.
3. Determine **session mode**:
   - `OUTLINE` — target is an `outlines/` file (beat sequence, character beats, dialogue requirements).
   - `DRAFT` — target is a `draft/` file (written prose, dialogue, sensory detail).
   - `DIALOG WORKSHOP` — forced by `dialog` flag. Target may be either file type. Extract all dialogue exchanges from the file; non-dialogue beats are summarised as context dividers, not segments. If the outline has a `dialogue requirements` section, load it as the subtext contract for the Subtext Tracker.
4. Read the target file fully. Abort with a clear error if it does not exist.
5. Parse all segments from the file and assign each a sequential number (S1, S2, S3…). Store the **full segment index** — this is used by Step 1b and by `!pick` mid-session.
6. If a `N-M` range was given: restrict the active segment list to that range immediately. Skip Step 1b.

Load supporting documents (all optional, used to enrich role responses):
- `.specify/memory/constitution.md` — story bible: style rules, plot structure, POV
- `spec.md` — character arcs, reader experience goals
- `characters/` or `characters.md` — voice signatures, psychology, arc state
- `plan.md` — scene function, thematic intent
- `themes.md` — active motifs this chapter should carry

---

## Step 1b — Section Picker

The Section Picker is shown when:
- The `pick` flag is present in `$ARGUMENTS`, or
- The user types `!pick` at any pause point during the session (re-opens the picker; already-completed segments are marked).

### Display the Segment Index

List all segments in the chapter with a one-line summary for each. The summary is derived from:
- **OUTLINE mode**: the first half-sentence of the beat entry
- **DRAFT mode**: the first sentence of the paragraph, or the first speaker + opening words of the dialogue exchange
- **DIALOG WORKSHOP mode**: exchange label + participating characters + opening line

```
── Section Picker ─────────────────────────────────────────────
  Chapter : [CHAPTER_ID] — [ChapterName]  ([total] segments)
───────────────────────────────────────────────────────────────

  #   Type      Summary                                    Status
  ─── ─────────  ───────────────────────────────────────────  ──────
  S1  [beat]    Mira enters the archive and finds the door  —
  S2  [beat]    She attempts the lock; it resists            —
  S3  [dialog]  Jonas / Mira — "You knew this was here"      —
  S4  [beat]    Jonas reveals the second key                 —
  S5  [dialog]  Mira / Jonas — "Then we do this together"    —
  S6  [beat]    Chapter closes on Mira pocketing both keys   —

───────────────────────────────────────────────────────────────
Select segments to include in this session.

  Enter numbers or ranges (e.g.  1, 3, 5-6 )
  Press Enter alone to include all segments
  Type  d  to include only dialog segments
  Type  b  to include only beat/action segments
───────────────────────────────────────────────────────────────
```

**Status column** values:
- `—` — not yet played in this session
- `✓` — completed in this session
- `↩` — replayed (Dialog Workshop)
- `⚠️` — has open HIGH issues from this session

### Apply the Selection

Parse the user's input and build the **active segment list** — an ordered subset of the full segment index. Rules:

- Ranges are inclusive: `2-4` = S2, S3, S4.
- Non-contiguous selections are allowed: `1, 3, 5-6` = S1, S3, S5, S6.
- Duplicate numbers are deduplicated; order is always ascending.
- `d` shortcut: select all segments whose `Type` is `dialog` or `exchange`.
- `b` shortcut: select all segments whose `Type` is `beat` or `action`.
- Enter alone: select all segments (default full play-through).

Display a confirmation before proceeding:

```
Active segments: S[N], S[N], S[N-M] ([count] of [total])
Proceeding to Role Assignment.
```

### Mid-Session Re-pick (`!pick`)

When `!pick` is typed at a pause point:
1. Re-display the full Segment Index with current status values filled in.
2. Ask: `Add, remove, or replace selection? (add / remove / replace)`
   - `add [numbers]` — append segments to the active list
   - `remove [numbers]` — remove segments from the remaining active list (already-completed segments cannot be removed)
   - `replace [numbers/shortcut]` — replace the remaining (not yet played) portion of the active list; completed segments are kept
3. Confirm the updated active list and resume the session at the next unplayed segment.

---

## Step 2 — Identify Roles

Analyse the target chapter and produce the **Role Manifest** — a complete list of every role that can contribute meaningful perspective to this scene.

### Standard Roles

Always include the following roles in the manifest:

| Role | Symbol | Perspective |
|---|---|---|
| **Author** | ✍️ | Craft and intent — is the scene doing what the plan demands? |
| **Lector** | 📖 | Attentive first read — flow, clarity, emotional pull; catches what breaks immersion |

### Scene-Character Roles

For each named or unnamed character present in this scene, add a character role:

| Role | Symbol | Perspective |
|---|---|---|
| **[CharacterName]** | 🎭 | First-person voice — motivations, emotional state, what they notice, what they want |

Derive character presence from:
- Outline: characters listed in `characters_present` or inferred from the beat sequence
- Draft: named characters with dialogue or action beats

If a character's voice signature is available in `characters/` or `characters.md`, note it — the AI will use it when voicing that character.

### Optional Roles (include when applicable)

Add these roles only when the scene content makes them relevant. Suggest them to the user during the Role Assignment Interview if applicable:

| Role | Symbol | Include when… |
|---|---|---|
| **Casual Reader** | 📰 | Surface read — entertainment, pace, cover appeal; no craft vocabulary |
| **Critique Reader** | 🔍 | Structural analysis — tropes, arc consistency, genre convention compliance |
| **Editor** | ✏️ | Draft mode — prose line quality, redundancy, sentence rhythm issues |
| **Continuity Checker** | 🗂️ | Draft mode — tracks timeline, world-state, and character consistency against story bible |
| **Beta Reader** | 💬 | Draft mode — general reader emotionally invested in the story; gives gut reactions |
| **Sensitivity Reader** | ❤️ | Scene includes sensitive social, cultural, or trauma content |
| **Genre Expert** | 📚 | Scene's genre conventions (e.g. thriller pacing, romance heat level) need validation |
| **Subtext Tracker** | 🔇 | Dialog Workshop mode — logs what each character is *not* saying; tracks deflection, concealment, and unspoken want vs. stated want per turn. Silent during regular play-through; speaks only in Dialog Workshop mode or when invoked via Q&A |
| **Naive Reader** | 🙈 | Has read only up to the chapter immediately preceding the current one — nothing more. Flags every moment where the segment assumes knowledge the reader does not yet have: unrevealed facts, unintroduced characters, unexplained world-building. Always optional; always AI-assigned. |
| **Tension Curve** | 📈 | Post-play-through analysis role — scores every segment 1–5 for tension/engagement and renders a pacing curve. Activated by the `tension` argument flag or by typing `!tension` at any pause point. Never speaks during segment responses; activated only in Step 5-TC. |

Present the full Role Manifest to the user before proceeding.

---

## Step 3 — Role Assignment Interview

Display the Role Manifest as a numbered table with columns: **#**, **Role**, **Symbol**, **Perspective**, **Assignment** (empty).

Ask the user to assign each role to either **AI** or **You (User)** by responding with a comma-separated list of role numbers:

```
Which roles do you want to play yourself?
Enter role numbers (e.g. 1, 3) or press Enter to let AI play all roles.
```

Rules:
- Unassigned roles default to **AI**.
- A role assigned to the user is **paused** — the AI will prompt the user for that role's response at each relevant pause point instead of generating it.
- The user may change role assignments at any time during the session by typing `!assign [RoleName] AI` or `!assign [RoleName] me`.
- At least one AI role must remain active (warn if the user tries to assign all roles to themselves and disable AI for all).

Store the final assignment in the **Session State**.

---

## Step 4 — Session Briefing

Before the play-through begins, display a concise session card:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ROLEPLAY SESSION
  Chapter  : [CHAPTER_ID] — [ChapterName]
  Mode     : [OUTLINE / DRAFT / DIALOG WORKSHOP]
  Segments : [active count] of [total] selected
  Roles    : [list with symbol + AI/User tag]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type  continue  or  c   → advance to next segment
      question  or  ?   → open Q&A for this segment
      end       or  e   → end session and save notes
      !assign [Role] AI / me → reassign a role mid-session
      !pick             → open Section Picker to change active segments
      !skip             → skip current segment without comment
```

In **Dialog Workshop mode**, also show:

```
  DIALOG WORKSHOP
  Dialogue exchanges found : [count]
  Characters               : [list]
  Subtext contract loaded  : [Yes / No]
  Your character(s)        : [list or — if all AI]

Type your character's line directly to respond in-character.
AI plays all other character turns automatically.
```

Wait for the user to type `continue` (or `c`) to begin.

---

## Step 5 — Play-Through Loop

Repeat for each **segment** until the chapter is exhausted or the user types `end`:

### 5a — Present the Segment

Display the segment text verbatim, clearly framed:

```
── Segment [N/Total] ──────────────────────────────

[segment text from outline beat or draft paragraph/dialogue block]

───────────────────────────────────────────────────
```

For **OUTLINE mode**: a segment is one beat-sequence entry (a single causal step line).
For **DRAFT mode**: a segment is one paragraph or one continuous dialogue exchange (scene break `***` starts a new segment).

### 5b — Generate AI Role Responses

For each AI-assigned role, in the order: scene characters first, then Author, Lector, Casual Reader, then optional roles, then Critique Reader last:

Generate a short focused response (2–5 sentences max per role) from that role's perspective on **this specific segment**. Format each response:

```
[Symbol] [RoleName]
[response text]
```

Rules for role responses:
- **[CharacterName]** roles speak in first person from inside the scene: feelings, intent, what they noticed. Do not break the fourth wall.
- **Author** focuses on craft execution: does this beat do what the plan requires?
- **Lector** reacts as a careful reader: what worked, what tripped, what raised a question?
- **Casual Reader** reacts purely to entertainment and pace — no craft language.
- **Critique Reader** identifies structural or craft issues with diagnostic precision. Labels issues with the standard checklist codes when applicable (e.g. `CHR-002`, `STB-004`).
- **Editor** (draft only) flags line-level prose issues, redundancy, weak verbs.
- **Continuity Checker** (draft only) cross-references against story bible and flags violations.
- **Only generate a response if the role has something meaningful to say about this segment.** Roles may pass silently — signal this with `[Symbol] [RoleName] — (no note)`.

For user-assigned roles: instead of generating text, display a prompt:

```
[Symbol] [RoleName] (Your turn)
What does [RoleName] notice or feel in this segment?
```

Wait for the user's response before continuing. Store it in the session log.

### 5c — Pause Point

After all role responses for the segment, display the pause prompt:

```
────────────────────────────────────────
  c  continue · ?  question · e  end · !assign · !pick · !skip
────────────────────────────────────────
```

Wait for user input:

- **`c` / `continue`**: advance to segment N+1 (loop back to 5a).
- **`?` / `question`**: enter **Q&A Mode** for this segment (see Step 6). Return to 5c after Q&A.
- **`e` / `end`**: exit the loop and go to Step 7.
- **`!assign [Role] AI/me`**: update the assignment for that role. Confirm the change and loop back to 5c.
- **`!pick`**: open the Section Picker (Step 1b) to add, remove, or replace remaining segments. Resume at next unplayed segment after confirming.
- **`!skip`**: record the segment as skipped (no notes) and advance.

---

## Step 5-DW — Dialog Workshop Loop

This loop **replaces** the standard Step 5 when session mode is `DIALOG WORKSHOP`.

### DW-1 — Extract and Index Dialogue Exchanges

Before the loop starts, parse the target file and build a **Dialogue Exchange Index**:

- Identify every contiguous block where two or more characters exchange lines.
- Assign each exchange a label: `EX-1`, `EX-2`, etc.
- Within each exchange, split by speaker turn: `EX-1.T1`, `EX-1.T2`, etc.
- Identify non-dialogue beats between exchanges; store them as **context dividers** (displayed as brief summaries, never as playable segments).
- If the outline's `dialogue requirements` section is loaded, map each requirement (what must be deflected, revealed, or withheld) to the exchange where it applies.

### DW-2 — Pre-Exchange Briefing

Before each exchange begins, display:

```
── Exchange [EX-N] · [N] turns ──────────────────────

[Context divider summary if present]

Subtext contract for this exchange:
  [Requirement 1 — from dialogue requirements, or "none specified"]
  [Requirement 2]

Characters: [list with AI/User assignment]
────────────────────────────────────────────────────
```

Wait for `c` to begin the exchange.

### DW-3 — Turn-by-Turn Improvisation

For each turn in the exchange:

**If the speaking character is AI-assigned:**
Generate the character's line strictly from their voice signature (`characters/` or `characters.md`). The line must:
- Advance or deflect the subtext contract requirement for this exchange
- Be consistent with the character's arc state at this chapter
- Be written as raw dialogue (no action beats, no attribution tags) — those are the writer's job

Display as:

```
🎭 [CharacterName]
"[line]"
```

**If the speaking character is user-assigned:**
Display:

```
🎭 [CharacterName] (Your turn)
Type your line:
```

Wait for the user's input. Accept any free-form text as the character's line. Store it verbatim.

**After every turn (AI or user), the Subtext Tracker logs silently:**
- Stated want: what the line says on the surface
- Hidden want: what the character actually wants based on their arc and the subtext contract
- Deflection status: did this line deflect, comply with, or break the subtext contract requirement?
- Concealment score: `HIGH` / `MED` / `LOW` — how well the subtext is hidden

The Subtext Tracker does **not** display its log during the turn. It accumulates and surfaces at the end of the exchange (DW-4).

### DW-4 — Post-Exchange Debrief

After the final turn of an exchange, display the Subtext Tracker's accumulated log for that exchange:

```
🔇 Subtext Tracker — EX-[N] debrief

| Turn | Character | Stated | Hidden want | Deflection | Concealment |
|---|---|---|---|---|---|
| T1 | [name] | [surface intent] | [hidden want] | [Deflect/Comply/Break] | [H/M/L] |
| T2 | … | … | … | … | … |

Subtext contract status: [HELD / BROKEN / PARTIALLY MET]
[One sentence: was the required deflection/revelation/withholding achieved?]
```

Then display the standard pause prompt:

```
────────────────────────────────────────
  c  next exchange · ?  question · e  end · !assign · !pick · !replay
────────────────────────────────────────
```

Additional command in Dialog Workshop mode:
- **`!replay`**: replay the current exchange from the beginning with the same role assignments. Previous attempt is discarded from session log but preserved in a `discarded` sub-log for reference.
- **`!replay swap`**: replay with all character role assignments inverted (user plays the AI character, AI plays the user character). Useful for testing the exchange from the other side.

### DW-5 — Insight Capture (Dialog Workshop)

In addition to the standard Insight Capture rules, Dialog Workshop automatically generates insights from the Subtext Tracker log:

- Any turn with `Deflection: Break` and `Concealment: LOW` → `ISSUE HIGH`: character states their hidden want too directly
- Any turn where `Subtext contract status: BROKEN` → `ISSUE HIGH`: exchange fails its dialogue requirement
- Any turn where the user's improvised line diverges strongly from the character's voice signature → `SUGGESTION MED`: user's instinct vs. character bible — worth discussing
- Any exchange where `Subtext contract status: HELD` throughout → `CONFIRM`: dialogue requirement successfully executed

### DW-6 — Revised Dialogue Output (Optional)

At the end of the session (before Step 7), if the session mode is `DIALOG WORKSHOP`, ask:

```
Generate a revised dialogue draft from this session?

  1  Yes — assemble best turns from all attempts into a clean dialogue block
  2  Yes — generate a new AI draft incorporating subtext notes (no user turns)
  3  No — save insights only

Enter 1–3:
```

For option 1: assemble the user's accepted turns and AI turns from the final (non-discarded) attempt of each exchange into a clean, attribution-tagged dialogue block. Wrap in a `## Dialog Workshop Draft` section.

For option 2: generate a complete AI-authored dialogue rewrite that satisfies all subtext contract requirements identified in DW-1, informed by Subtext Tracker deflection analysis. Wrap in a `## Dialog Workshop Draft (AI rewrite)` section.

For option 3: skip.

In all cases, the generated draft block (if any) is appended to the chosen commit target(s) in Step 7 as an additional section after the revision notes.

---

## Step 5-NR — Naive Reader Pass

The Naive Reader role may be activated at any time:
- Automatically if the user included it during Role Assignment.
- On demand at any pause point by typing `!naivereader`.

When active, after the standard 5b role responses for each segment, the Naive Reader adds a response **only** if it detects an assumption violation — something the segment requires the reader to know that has not yet been established. If nothing is assumed, it passes silently (`🙈 Naive Reader — (no violation)`).

### Assumption Violation Detection

The Naive Reader checks each segment against four categories:

1. **Character knowledge**: Is every named character introduced by this chapter, or established in a prior chapter in `plan.md`'s chapter map?
2. **World-building facts**: Does the segment rely on a rule, place, object, or system not yet shown or explained to the reader?
3. **Plot state**: Does the segment reference an event, relationship status, or consequence the reader has not witnessed?
4. **Pronoun resolution**: Are all pronouns resolvable from what the reader already knows?

For each violation found, the Naive Reader reports:

```
🙈 Naive Reader
"[quoted fragment that assumes too much]"
Assumed knowledge : [what the segment requires the reader to know]
First established : [where it is established, or "not yet established"]
Suggestion        : [one sentence — front-load the context here, or defer this information]
```

Violations are automatically logged as insights:
- `ISSUE HIGH` — assumption makes the segment unreadable without prior knowledge
- `ISSUE MED` — assumption causes momentary confusion that self-resolves later
- `SUGGESTION LOW` — context is present but buried or easy to miss

---

## Step 5-TC — Tension Curve Analysis

The Tension Curve pass runs **after the full play-through loop is complete** (after the last segment, before Step 7). It is triggered by:
- The `tension` argument flag, or
- Typing `!tension` at any pause point during the session.

If triggered mid-session via `!tension`, it scores only the segments played through so far, renders a partial curve, then returns to the session.

### Scoring

The **Author** and **Lector** roles jointly score every played segment. Each receives a single combined score on a 1–5 scale:

| Score | Meaning |
|---|---|
| 5 | Maximum tension — reader cannot stop; stakes highest, outcome most uncertain |
| 4 | High engagement — propulsive, reader pulled forward |
| 3 | Moderate — functional, scene progressing but not gripping |
| 2 | Low — reader may drift; pace slow or stakes abstract |
| 1 | Flat — no forward pull; filler, over-explanation, or unearned calm |

Skipped segments are scored `0` and marked `SKIP` in the table.

**Scoring criteria** (all factor into the combined score):
- **Stakes clarity**: does the reader know what is at risk?
- **Outcome uncertainty**: is the result of this segment genuinely in doubt?
- **Character want vs. obstacle**: is there active resistance, deflection, or threat?
- **Forward momentum**: does the segment end less stable than it started?

If Author and Lector disagree by ±2 or more, display both scores with a one-sentence reason for the gap. Use the *lower* score in the curve — divergence itself signals a craft problem worth noting.

### Render the Curve

After all segments are scored, render an ASCII tension curve:

```
📈 Tension Curve — [CHAPTER_ID] [ChapterName]

5 │                 ▄▄
4 │         ▄▄   ▄▄    ▄▄
3 │   ▄▄  ▄▄  ▄▄        ▄▄
2 │ ▄▄
1 │
  └─────────────────────────────
    S1 S2 S3 S4 S5 S6 S7 S8 S9…
```

Below the curve, print a compact score table:

```
| Seg | Score | Author | Lector | Flag          |
|-----|-------|--------|--------|---------------|
| S1  |   2   |   2    |   2    | ⚠️ SLOW OPEN  |
| S2  |   3   |   3    |   3    | —             |
…
```

### Automatic Flags

| Pattern | Flag | Threshold |
|---|---|---|
| Score 1 or 2 | `⚠️ FLAT` | Any single segment |
| Three or more consecutive segments ≤ 3 | `⚠️ SAG` | Pacing trough |
| Final segment scores < 3 | `⚠️ WEAK ENDING` | Last segment only |
| First segment scores < 3 | `⚠️ SLOW OPEN` | First segment only |
| Score drops ≥ 2 in one step | `⚠️ DROP` | Any transition |
| Score rises to 4–5 then drops to 1–2 in next segment | `⚠️ DEFLATE` | Any transition |
| No segment scores 4 or 5 in the entire chapter | `⚠️ NO PEAK` | Full chapter |

### Diagnosis

After the curve and flag table, the Author generates a one-paragraph diagnosis:
- Names the most critical pacing problem and its segment range
- Explains the structural cause (e.g. "beats S4–S6 are all exposition; no character want is active")
- Proposes one structural remedy (e.g. "insert an obstacle or time pressure into S5")

If no flags are raised: `📈 Tension Curve: no structural pacing issues detected.`

### Insight Capture (Tension Curve)

| Flag | Insight type |
|---|---|
| SAG, NO PEAK, WEAK ENDING | `ISSUE HIGH` |
| FLAT, DROP, DEFLATE, SLOW OPEN | `ISSUE MED` |

Text format: `Tension [FLAG]: segments [range] — [one-sentence diagnosis].`

The full curve and score table is included in the `## Roleplay Revision Notes` commit block under a `### Tension Curve` subsection.

---

## Step 6 — Q&A Mode

Q&A mode allows the user to ask any question about the current segment and receive an answer from the **most appropriate role** automatically selected by the AI.

### Entering Q&A

The user asks a free-form question. Examples:

> Why does Mira feel so reluctant here?
> Does this beat belong in act two or act three?
> Is this dialogue too on-the-nose?
> What would a casual reader feel at this moment?

### Selecting the Responding Role

Select the most appropriate role to answer based on question type:

| Question type | Primary responder | Secondary (if needed) |
|---|---|---|
| Character motivation / feeling | That character's role | Author |
| Craft / structural | Author | Critique Reader |
| Reader experience | Lector or Casual Reader | — |
| Continuity / consistency | Continuity Checker | Author |
| Line prose | Editor | Lector |
| Genre / market | Genre Expert | Critique Reader |
| Subtext / what a character is hiding | Subtext Tracker | That character's role |
| Pacing / tension in a segment | Tension Curve | Author |
| Assumption / reader knowledge gap | Naive Reader | Lector |
| Open / unclear | Lector | Author |

If the responding role is user-assigned, prompt the user to answer in that role instead (they may delegate to AI by typing `!ai`).

### Response Format

```
[Symbol] [RoleName] answers:
[2–6 sentence answer grounded in the segment and available context documents]

[Symbol] [OtherRole] adds: (optional — only if the secondary perspective adds distinct value)
[1–3 sentences]
```

After answering, ask: `Any follow-up? (or c to continue)` — loop within Q&A until the user types `c`.

### Insight Capture

Every Q&A exchange that surfaces an actionable insight (a problem, a suggested change, a confirmation that something works) is automatically added to the **Session Insight Log** tagged with:
- Segment number
- Role that identified it
- Insight type: `CONFIRM` | `ISSUE` | `SUGGESTION` | `QUESTION`
- Severity (for issues): `HIGH` | `MED` | `LOW`
- Short text (one sentence)

---

## Step 7 — Session End and Commit

When the user types `end`:

### 7a — Session Summary

Display a summary of the full session:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SESSION COMPLETE
  Segments reviewed : [N] / [Total]
  Insights captured : [count]
    CONFIRM   : [n]
    ISSUE     : [n] (HIGH:[n] MED:[n] LOW:[n])
    SUGGESTION: [n]
    QUESTION  : [n]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

List each captured insight with its segment, role symbol, type, severity (if applicable), and text.

### 7b — Commit Options

Ask the user:

```
How should these insights be saved?

  1  Append revision notes to the outline file    (outlines/…)
  2  Append revision notes to the draft file      (draft/…)
  3  Both
  4  Save as a standalone session log only        (roleplay/…)
  5  Discard (do not save)

In Dialog Workshop mode, also note whether a `## Dialog Workshop Draft` block was generated and will be included.

Enter 1–5:
```

### 7c — Write Revision Notes

For options 1, 2, or 3:

Append a `## Roleplay Revision Notes` section to the chosen file(s). Use this structure:

```markdown
## Roleplay Revision Notes

> Session: [ISO date] · Chapter: [CHAPTER_ID] [ChapterName] · Mode: [OUTLINE/DRAFT]
> Roles: [comma-separated list with AI/User tags]

### Issues

| Seg | Role | Severity | Note |
|---|---|---|---|
| [N] | [Symbol] [Role] | [HIGH/MED/LOW] | [text] |

### Suggestions

| Seg | Role | Note |
|---|---|---|
| [N] | [Symbol] [Role] | [text] |

### Confirmations

| Seg | Role | Note |
|---|---|---|
| [N] | [Symbol] [Role] | [text] |

### Open Questions

| Seg | Role | Question |
|---|---|---|
| [N] | [Symbol] [Role] | [text] |
```

Rules:
- Append — never overwrite. If a `## Roleplay Revision Notes` section already exists, append a new dated block under it rather than replacing it.
- In outline files: append after the last existing section.
- In draft files: append after the YAML frontmatter block at the very end of the file.

For option 4 only — create `FEATURE_DIR/roleplay/<CHAPTER_ID>_<ChapterName>-roleplay-<ISO_date>.md` with the same structure plus a full transcript of all role responses in segment order. In Dialog Workshop mode, also include the Subtext Tracker turn-by-turn log for every exchange and any generated dialogue draft blocks.

### 7d — Post-Save Handoff

After writing, analyse the saved insights and produce a concrete **Next Step Block** — not a vague suggestion, but a ready-to-run command the user can invoke immediately.

#### Determine what changed

Classify the session outcome:

| Condition | What changes | Next step |
|---|---|---|
| HIGH issues saved → outline file | Beat sequence, character beats, or dialogue requirements are wrong. The outline needs structural repair before any drafting happens. | Re-run `speckit.outline` to regenerate the repaired beats |
| HIGH issues saved → draft file | Specific passages are failing structural, character, or continuity checks. Those passages need targeted rewriting. | Run `speckit.revise` scoped to the failing items |
| SUGGESTION or MED/LOW issues only | The chapter works structurally; prose or pacing can be improved in a targeted pass. | Run `speckit.revise` with a light scope, or continue to `speckit.polish` |
| CONFIRM only, no issues | Nothing is broken. The session validated the chapter. | Continue to `speckit.implement` (next scene) or `speckit.polish` |
| Dialog Workshop — broken subtext contract | The dialogue exchange does not meet its deflection/withholding requirement. The outline's `dialogue requirements` section needs revision before re-drafting. | Update outline's dialogue requirements, then re-run `speckit.implement` |
| Dialog Workshop — dialogue draft generated | A revised dialogue block was produced in DW-6. It needs to replace the corresponding passage in the draft. | Run `speckit.revise` scoped to the exchange |

#### Format the ready-to-run command

Display the Next Step Block in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NEXT STEP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[One sentence explaining what the roleplay session found and why the following action addresses it.]

  Command  : [speckit.revise / speckit.outline / speckit.implement / speckit.polish]
  Scope    : [CHAPTER_ID] "[comma-separated issue codes or quoted description]"
  Rationale: [One sentence: which specific issues drive this scope]

  Ready to run? Type  y  to invoke now, or  n  to stop here.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If the user types `y`, immediately invoke the suggested command with the formatted scope as its argument. The target agent (`speckit.revise` or `speckit.outline`) will then:

- **`speckit.revise [CHAPTER_ID] "[issue codes]"`**: loads the draft, reads the quoted issue codes as the revision scope (matching the standard checklist code format), rewrites only the failing passages, and produces a versioned draft file with a diff summary. The roleplay revision notes section in the draft is preserved verbatim — it is not treated as prose.
- **`speckit.outline [CHAPTER_ID]`**: reloads `plan.md`, applies HIGH-issue notes from the `## Roleplay Revision Notes` section as correction constraints, regenerates the beat sequence and dialogue requirements for that chapter, and sets `status: DRAFT` so the author can review before re-approving.

If the user types `n`, end the session here. The revision notes remain in the file and can be used as manual input to `speckit.revise` or `speckit.outline` at any time.

#### Multiple issues across outline and draft

If HIGH issues span both the outline and the draft:
1. Address the outline first (structural root cause).
2. After the outline is `APPROVED`, address the draft via `speckit.revise`.
Present both steps in sequence in the Next Step Block, numbered.

---

## Operating Constraints

**SESSION INTEGRITY**: Do not generate prose or revise the chapter during the session. The session surfaces insights only; revision happens via `speckit.revise` or `speckit.outline` afterwards.

**CHARACTER VOICE FIDELITY**: When voicing a scene character, strictly follow their voice signature from `characters/` or `characters.md`. Do not invent personality traits. If no profile is available, use only what the character does and says in the outline or draft.

**STORY BIBLE AUTHORITY**: `.specify/memory/constitution.md` governs all craft judgments. Author and Critique Reader responses must be consistent with the story bible.

**SEGMENT SCOPE**: Role responses address only the **current segment**. Do not let any role comment on future segments or spoil unrevealed beats.

**SUBTEXT TRACKER SILENCE**: In standard play-through mode the Subtext Tracker never speaks unless invoked via Q&A. In Dialog Workshop mode it speaks only at DW-4 post-exchange debrief. It never interrupts a turn mid-improvisation.

**TENSION CURVE TIMING**: The Tension Curve role never speaks during segment responses. It scores silently throughout the session and renders only after the final segment (Step 5-TC) or when explicitly invoked via `!tension`. It does not interrupt the play-through loop.

**NAIVE READER FORWARD-ONLY**: The Naive Reader evaluates only what has been established in chapters before the current one, plus earlier segments already played through in the current session. It must not use knowledge from later segments — it reads strictly forward.

**USER CONTROL**: The user can end the session, skip segments, reassign roles, or delegate any user-assigned role to AI at any time. Do not resist or warn against any of these actions.

**NO FABRICATION**: Do not invent character details, world-building facts, or story events not present in the source documents. If a role needs information that does not exist in the loaded documents, they should say so rather than speculate.
