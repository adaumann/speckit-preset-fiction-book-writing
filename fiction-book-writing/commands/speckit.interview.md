---
description: Interactive one-on-one conversation with an existing character, voiced by AI from their profile and known story presence in spec, plan, outline, or draft. Surfaces character psychology, subtext, and arc state through dialogue. Session can be exported as a summary note to characters/ or notes/.
handoffs:
  - label: Update Character Profile
    agent: speckit.brainstorm
    prompt: Use these interview insights to deepen the character profile
    send: true
  - label: Update Story Bible
    agent: speckit.constitution
    prompt: Apply discovered character facts to the story bible
    send: true
  - label: Revise Draft
    agent: speckit.revise
    prompt: Revise the draft scene using the character insights from this interview
    send: true
  - label: Build Story Structure
    agent: speckit.plan
    prompt: Incorporate these character insights into the story structure
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Accepted arguments:
- `[CHARACTER_NAME]` — name (or partial name) of the character to interview. Resolves against `characters/` directory or `characters.md`.
- `[CHARACTER_NAME] [CHAPTER_ID]` — pin the character's arc context to a specific chapter (e.g. `mira A2.205`). The character speaks from their state at that point in the story — they do not know what happens after.
- `[CHARACTER_NAME] arc` — display the character's arc summary card before the session begins (see Step 3a).
- `[CHARACTER_NAME] stress` — activate **Stress Mode**: the user's questions probe inconsistencies, contradictions, or painful truths. The character must stay in voice but may deflect, deny, or crack under pressure (see Step 5-SM).
- *(no argument)* — prompt for character name in Step 1.

All flags except `arc` may be combined with a chapter ID, e.g. `mira A1.101 stress`.

---

## Purpose

This command lets you sit across the table from one of your characters and talk to them directly. The AI voices the character faithfully — using their profile, vocabulary register, dialogue style, subtext patterns, and arc state — so you can hear how they think, discover contradictions, test their voice, or simply explore who they are.

The session is open-ended: you can ask questions, make accusations, share information the character doesn't yet know, or probe their past. The character responds from inside their own perspective, consistent with what they know at the chosen story point.

**The session is not a scene from the book.** It is a meta-conversation — the author speaking to the character as a creative collaborator. The character answers as themselves, not as a narrator.

Output is only written when you explicitly commit at the end.

---

## Pre-Execution Checks

**Check for extension hooks (before interview)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_interview` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Character Resolution

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Resolve the **target character**:

1. Parse `$ARGUMENTS` for a character name, optional chapter ID, and optional mode flags (`arc`, `stress`).
2. If no name is provided: ask — `Which character do you want to interview? (enter name)`.
3. Look up the character profile:
   - Search `FEATURE_DIR/characters/` for a file whose name contains the given name (case-insensitive). Match on file name or the `# Character Profile: [NAME]` header.
   - If `characters/` does not exist, check `FEATURE_DIR/characters.md` for a section matching the name.
   - If no match is found, report: `No character profile found for "[name]". Check FEATURE_DIR/characters/ or characters.md.` — then abort.
   - If multiple files match, list them and ask the user to pick one.
4. Read the full character profile. Store as `CHARACTER_PROFILE`.

Set the **arc context point**:
- If a `[CHAPTER_ID]` was given: the character's knowledge and emotional state are locked to that chapter. Load the corresponding outline (`outlines/[CHAPTER_ID]_*.md`) or draft (`draft/[CHAPTER_ID]_*.md`) to read recent events. State clearly:  
  `Context locked to [CHAPTER_ID] — the character does not know events after this chapter.`
- If no chapter ID: use the latest chapter present in the draft directory. If no draft exists, use spec/plan state (the character exists in pre-draft conception).

---

## Step 2 — Load Story Context

Load the following documents as background context for voicing the character. All are optional — skip silently if absent. Do not surface their contents to the user at this stage.

| Document | Path | Purpose |
|---|---|---|
| Story bible | `.specify/memory/constitution.md` | Style rules, world-state, voice register baseline |
| Story brief | `spec.md` | Character arc goals, dramatic question |
| Story structure | `plan.md` | Scene-by-scene context, chapter map, arc checkpoints |
| Other characters | `characters/` or `characters.md` | Relationship map, known dynamics |
| Active outline | `outlines/[CHAPTER_ID]_*.md` | Scene state at context point (if chapter ID given) |
| Active draft | `draft/[CHAPTER_ID]_*.md` | Written events at context point (if chapter ID given) |
| Themes | `themes.md` | Active motifs this character carries |
| World-building | `world-building.md` | Facts the character would know |
| Timeline | `timeline.md` | Chronological events the character has experienced |

From this context, derive the **Character Arc State** — a concise internal summary (not shown to user unless `arc` flag is set):
- Current emotional state and dominant mood
- Active want (what they are pursuing right now)
- Active fear (what they are avoiding)
- Key relationships in play at this point
- What they know vs. what they do not yet know
- Where they are on their `Transforms from → to` arc

---

## Step 3 — Session Setup

### 3a — Arc Summary Card (optional)

If the `arc` flag is set, display before starting the session:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHARACTER ARC STATE
  Character : [CHARACTER_NAME]
  Context   : [CHAPTER_ID or "pre-draft conception"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Arc position   : [position on "from → to" arc, e.g. "early — false belief intact"]
  Emotional state: [dominant mood / tension at this point]
  Active want    : [what they are currently pursuing]
  Active fear    : [what they are actively avoiding]
  Key tension    : [the central unresolved tension for this character right now]

  What they know     : [brief summary — events, relationships, facts]
  What they don't    : [key unknowns that affect how they'll answer]
  Voice register     : [primary register from profile, e.g. "Formal / Deflective / Dry"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then continue to 3b.

### 3b — Session Card

Display the session briefing:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHARACTER INTERVIEW
  Character : [CHARACTER_NAME]  [ROLE, e.g. Protagonist]
  Context   : [CHAPTER_ID — ChapterName / "pre-draft"]
  Mode      : [Standard / Stress]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[CHARACTER_NAME] is ready to talk.

  Just type to speak. The character will respond.

  !note           → AI steps out of character: explains subtext or arc intent
  !arc            → show current arc state summary mid-session
  !context [topic]→ surface what this character knows about [topic]
  !voice          → show voice signature reminder (register, vocabulary, patterns)
  !stress         → toggle Stress Mode on/off
  end  or  e      → end session and go to export
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for the user's first message. Do not pre-open the conversation — let the user set the tone.

---

## Step 4 — Conversation Loop

Repeat until the user types `end` or `e`.

### 4a — Receive User Turn

Accept any free-form text from the user as the interviewer's statement or question. Store each user turn verbatim in the **Session Log**.

### 4b — Generate Character Response

Voice the character's reply. Rules:

**Strict voice rules** — derived from `CHARACTER_PROFILE`:
- Use the character's primary register and vocabulary pool. Never stray into registers they avoid.
- Apply their directness level: if they answer obliquely, do so. If they deflect, deploy their default deflection strategy, not a generic one.
- Apply dialogue style: sentence length, use of contractions, verbal habits, intensifiers.
- Apply subtext pattern: what they almost never say aloud — their response surface should conceal their real concern, unless under extreme pressure.
- If under stress or provoked: apply their "under pressure" dialogue changes (shorter sentences, more formal, more chaotic — per profile).

**Arc-consistency rules**:
- The character speaks from their arc state at the context point. They do not reference events or knowledge they do not yet have.
- They may lie, deflect, rationalize, or self-deceive — as their profile allows. This is in-character, not a failure.
- If the user tells the character something they do not know (a spoiler, a future event, another character's secret): the character reacts as themselves, from their current beliefs. They may disbelieve, be shocked, or try to reframe it through their false belief.

**Format**:

```
🎭 [CHARACTER_NAME]
[character's response — natural prose, no attribution tags, no stage directions]
```

Response length: natural conversational length. Typically 2–5 sentences. Longer for complex emotional questions; shorter for defensive or deflective characters under pressure.

### 4c — Subtext Log (silent)

After every response, silently log:
- **Surface**: what the character said
- **Hidden**: what they actually want or fear in this moment, per arc state
- **Deflection**: did they answer the question or redirect it?
- **Arc signal**: does this response reveal, confirm, or contradict their arc?

This log is not shown during the session. It surfaces at export (Step 6).

### 4d — Special Commands

At any turn, if the user's input matches a command:

**`!note`** — AI steps out of character and offers an out-of-character observation:

```
📝 Author Note
[2–4 sentences explaining: what the character was really doing in their last response,
what subtext or arc mechanics drove it, and one craft implication for the author]

(Resuming interview…)
```

**`!arc`** — Display the arc summary card (same format as Step 3a) with the latest session context factored in. Then resume.

**`!context [topic]`** — Surface what this character knows about the given topic at the context point:

```
📋 Context: [topic]
What [CHARACTER_NAME] knows: [1–3 sentences drawn from loaded documents]
What they don't know: [1–3 sentences — gaps that affect how they'd speak about this]
```

Then resume.

**`!voice`** — Display a compact voice reminder:

```
🗣️ Voice: [CHARACTER_NAME]
  Register     : [primary register]
  Vocabulary   : [3–5 key words or clusters]
  Avoids       : [2–3 words/patterns they never use]
  Deflects via : [default deflection strategy]
  Under stress : [how dialogue changes under pressure]
```

Then resume.

**`!stress`** — Toggle Stress Mode on or off. Confirm the change:

```
⚡ Stress Mode ON — [CHARACTER_NAME] is under pressure. They may deflect harder, crack under
   direct challenge, or reveal more than intended.
```

or

```
Stress Mode OFF — returning to standard interview mode.
```

---

## Step 5-SM — Stress Mode

When Stress Mode is active, the following rules are added to Step 4b:

- **Pressure escalation**: if the user pushes on the same topic twice in a row, the character's defences escalate (more deflection, more formal, more chaotic — per profile) on the second turn, then may begin to crack on the third.
- **Crack threshold**: if the character has been pushed on their core wound or false belief for three consecutive turns, they respond with a line that partially breaks their deflection — something more honest than they intended, consistent with their arc. This is not a confession; it is a slip.
- **Recovery**: after a crack, the character immediately attempts to reframe or walk it back in the following turn, unless the user's next message makes that impossible.
- The **subtext log** notes every crack and recovery moment.

---

## Step 6 — Session End and Export

When the user types `end` or `e`:

### 6a — Session Summary

Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  INTERVIEW COMPLETE
  Character : [CHARACTER_NAME]
  Turns     : [count]
  Cracks    : [count — number of deflection breaks, 0 if Stress Mode inactive]
  Key topics covered: [comma-separated list of the main subjects discussed]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 6b — Insight Extraction

Scan the full **Subtext Log** from Step 4c and extract notable insights. Categorize each as:

| Tag | Meaning |
|---|---|
| `VOICE CONFIRM` | A moment where the character's voice worked perfectly — quotable for the author as a reference sample |
| `VOICE DRIFT` | A response that strayed from the voice profile — worth flagging |
| `ARC REVEAL` | The character revealed something about their arc, wound, or false belief (even if unintentionally) |
| `ARC CONTRADICTION` | The character said something inconsistent with their profile or arc state |
| `PROFILE GAP` | The conversation surfaced a topic the profile doesn't cover — the author may want to add it |
| `STORY IMPLICATION` | A line suggests a possible scene, beat, or revelation worth tracking in notes |
| `QUOTABLE` | A line strong enough to use as inspiration for actual prose or dialogue |

List each insight:

```
[TAG] "[brief quote or paraphrase]" — [one-sentence explanation]
```

### 6c — Export Options

Ask:

```
How should this session be saved?

  1  Save full transcript + insights as a character interview note
     → FEATURE_DIR/notes/[character-slug]-interview-[YYYY-MM-DD].md
  2  Save insights only (no transcript)
     → FEATURE_DIR/notes/[character-slug]-interview-[YYYY-MM-DD].md
  3  Append insights to the character profile
     → FEATURE_DIR/characters/[character-file].md  (under a ## Interview Notes section)
  4  Both 1 and 3
  5  Discard (do not save)

Enter 1–5:
```

### 6d — Generate the Note File

For options 1, 2, or 4: generate `FEATURE_DIR/notes/[character-slug]-interview-[YYYY-MM-DD].md` with the following structure:

```markdown
# Interview: [CHARACTER_NAME]
**Date**: [YYYY-MM-DD]  |  **Context**: [CHAPTER_ID or "pre-draft"]  |  **Mode**: [Standard / Stress]

---

## Session Insights

| # | Tag | Note |
|---|-----|------|
| 1 | [TAG] | "[quote or paraphrase]" — [explanation] |
…

---

## Quotable Lines

> "[exact line]"
> — [CHARACTER_NAME], context: [brief topic]

…

---

## Transcript
<!-- Only included for options 1 and 4 -->

**[You]**: [user turn 1]

🎭 **[CHARACTER_NAME]**: [character response 1]

**[You]**: [user turn 2]

🎭 **[CHARACTER_NAME]**: [character response 2]

…
```

If no `notes/` directory exists, create it. Create the file. Confirm:

```
✓ Saved: FEATURE_DIR/notes/[character-slug]-interview-[YYYY-MM-DD].md
```

### 6e — Append to Character Profile

For options 3 or 4: append an `## Interview Notes` section to the character profile file. Do not overwrite existing content.

```markdown
## Interview Notes

### [YYYY-MM-DD] — Context: [CHAPTER_ID or "pre-draft"]

**Key insights**:
- [TAG]: [one-sentence note]
- …

**Quotable lines**:
> "[line 1]"

> "[line 2]"

**Profile gaps surfaced**:
- [topic not covered by the existing profile]
- …
```

Confirm:

```
✓ Appended to: FEATURE_DIR/characters/[character-file].md
```

### 6f — Post-Export Handoffs

After saving, display the available handoffs.
