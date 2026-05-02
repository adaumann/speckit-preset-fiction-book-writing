---
description: Audiobook production command â€” draft (convert a prose chapter to SSML/ElevenLabs audiodraft), voice (add or update narrator/character voice assignments in the story bible), lexicon (register pronunciation entries and export a .pls lexicon file), check (find stale or missing audiodrafts vs. prose drafts), and status (audiodraft production dashboard). Works with constitution.md ## X. Audiobook Production as the single authority for voice configuration.
handoffs:
  - label: Export Audiobook
    agent: speckit.export
    prompt: Assemble the audiobook chapter manifest and validate all audiodraft files
    send: true
  - label: Run Polish Pass
    agent: speckit.polish
    prompt: Run a final prose line-edit pass before generating audiobook drafts
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a continuity check before converting chapters to audiodraft format
    send: true
  - label: Update Story Bible
    agent: speckit.constitution
    prompt: Update the audiobook production section of the story bible
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
- *(no argument)* â€” display the audiobook status dashboard (same as `status`)
- `draft [CHAPTER_ID]` â€” convert a prose draft chapter to an audiodraft file (e.g. `draft A1.101`)
- `draft all` â€” convert all prose draft chapters that do not yet have an up-to-date audiodraft
- `voice add [CHARACTER_NAME]` â€” add or update a voice assignment for a character or the narrator
- `voice list` â€” list all current voice assignments from constitution.md
- `lexicon add [WORD]` â€” register a new pronunciation entry interactively
- `lexicon list` â€” display the full pronunciation lexicon table
- `lexicon export` â€” write the lexicon to `audiodraft/lexicon.pls` (W3C PLS format, compatible with Azure, Google, Amazon Polly, and ElevenLabs upload)
- `check` â€” scan for stale audiodrafts (prose draft newer than audiodraft) and missing audiodrafts (drafted chapters with no audiodraft)
- `status` â€” audiodraft production dashboard

---

## Purpose

`speckit.audiobook` manages the audiobook production pipeline for the fiction writing preset. It reads and writes `constitution.md ## X. Audiobook Production` as the single authority for TTS engine, speaker mode, voice assignments, and the pronunciation lexicon. Audiodraft files live in `FEATURE_DIR/audiodraft/` and are generated from prose drafts using the `audiobook-draft-template.md`.

**What each mode covers**:

| Mode | When to use | Writes files? |
|---|---|---|
| `draft` | After prose drafting or revision; after any voice/lexicon change | Yes â€” `audiodraft/` only |
| `voice add` | When adding a new character; when changing a TTS voice | Yes â€” `constitution.md` only |
| `voice list` | Any time â€” review current assignments | No â€” read-only |
| `lexicon add` | When a new invented name or term needs TTS guidance | Yes â€” `constitution.md` only |
| `lexicon list` | Any time â€” review pronunciation rules | No â€” read-only |
| `lexicon export` | Before synthesis; after adding new lexicon entries | Yes â€” `audiodraft/lexicon.pls` |
| `check` | After prose revisions; before export | No â€” read-only |
| `status` | Any time â€” overview of audiodraft production health | No â€” read-only |

**Integration with other commands**:
- `speckit.implement` can generate audiodrafts automatically when `OUTPUT_MODE` is `audiobook` or `both` in `constitution.md`. `speckit.audiobook draft` is the explicit, per-chapter alternative.
- `speckit.export audio` assembles the chapter manifest and validates all audiodraft files before synthesis. Run `speckit.audiobook check` first to resolve gaps.
- `speckit.continuity` flags chapters whose audiodraft `version` is lower than their prose draft `version` (`STALE AUDIODRAFT`). `speckit.audiobook check` surfaces the same signal and drives regeneration.
- `speckit.glossary` manages the story's invented terms. `speckit.audiobook lexicon add` supplements that with TTS-specific pronunciation guidance for any term that TTS engines commonly mispronounce.

---

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_audiobook` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 â€” Setup and Mode Resolution

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Locate `constitution.md` (at `.specify/memory/constitution.md` or `FEATURE_DIR/constitution.md`). Parse `## X. Audiobook Production`:
- `OUTPUT_MODE` â€” `book` / `audiobook` / `both`
- `TTS_ENGINE` â€” `ssml-cloud` / `elevenlabs` / `both`
- `SPEAKER_MODE` â€” `single` / `multi`
- Speaker Configuration table â€” all `| Role | Character / Function | SSML-Cloud Voice | ElevenLabs Voice ID | Notes |` rows
- Pronunciation Lexicon table â€” all `| Word / Name | IPA | Plain Hint | ElevenLabs Substitute |` rows
- Audiobook Style Hints table â€” all `| Character / Context | Hint |` rows

If `constitution.md` does not exist: abort for all modes with:
```
âœ— constitution.md not found.
Run speckit.constitution to create the story bible first.
Audiobook production settings are configured in ## X. Audiobook Production.
```

If `OUTPUT_MODE` is `book` and mode is `draft`:
```
âš ï¸ Output Mode is set to `book` in constitution.md ## X. Audiobook Production.
Set Output Mode to `audiobook` or `both` to enable audiodraft generation.
Run speckit.audiobook voice add to configure TTS settings and update Output Mode.
```
For `voice`, `lexicon`, `check`, and `status` modes: proceed regardless of `OUTPUT_MODE`.

Parse `$ARGUMENTS` for mode and optional arguments. Resolve mode:
- `draft â€¦` â†’ **Mode: Draft**
- `voice add â€¦` â†’ **Mode: Voice Add**
- `voice list` â†’ **Mode: Voice List**
- `lexicon add â€¦` â†’ **Mode: Lexicon Add**
- `lexicon list` â†’ **Mode: Lexicon List**
- `lexicon export` â†’ **Mode: Lexicon Export**
- `check` â†’ **Mode: Check**
- `status` or *(empty)* â†’ **Mode: Status**

---

## Mode: Draft

**Purpose**: Convert one or all prose draft chapters to audiodraft files using the audiobook-draft-template.

### Draft Step 1 â€” Resolve scope

If argument is `all`:
- Collect all files in `FEATURE_DIR/draft/*.md`. Sort by `chapter_id` from YAML frontmatter.
- For each chapter, check if a corresponding audiodraft exists in `FEATURE_DIR/audiodraft/` and whether it is current (audiodraft `version` â‰¥ prose draft `version`).
- Build the work list: chapters with no audiodraft OR chapters whose audiodraft `version` is lower than the prose draft `version` (STALE).
- If the work list is empty, report:
  ```
  âœ“ All chapters have up-to-date audiodraft files. Nothing to generate.
  ```
  and stop.
- Report the planned work list before proceeding:
  ```
  Generating audiodrafts for N chapter(s):
    [CHAPTER_ID] [Chapter Name]  â€” [NEW / STALE (prose v3, audiodraft v1)]
  ```

If argument is a `[CHAPTER_ID]`:
- Locate `FEATURE_DIR/draft/[CHAPTER_ID]*.md` â€” use the highest `_vN` version if multiple versions exist.
- If no prose draft file is found, abort:
  ```
  âœ— No prose draft found for [CHAPTER_ID] in FEATURE_DIR/draft/.
  Draft the chapter with speckit.implement first.
  ```

### Draft Step 2 â€” Load audiobook configuration

From the parsed `constitution.md ## X. Audiobook Production`:
- `TTS_ENGINE`: determines which variant(s) to generate.
  - `ssml-cloud` â†’ generate `.ssml` file only
  - `elevenlabs` â†’ generate `_el.xml` file only
  - `both` â†’ generate both `.ssml` and `_el.xml`
- `SPEAKER_MODE`: `single` or `multi`
- Speaker Configuration table: narrator voice + per-character voice assignments
- Pronunciation Lexicon table: phoneme rules to apply inline
- Audiobook Style Hints table: delivery notes to insert as HTML comments

Also read `constitution.md Â§ VII Language` to determine `[LANGUAGE]`. Use this BCP-47 value for:
- The `xml:lang` attribute on the SSML `<speak>` element (e.g. `xml:lang="de"` for German)
- The `xml:lang` attribute on the `<lexicon>` root element in `lexicon.pls`

If Language is not set, default to `en`. If Language â‰  `en`, display:
```
âš ï¸ Language is set to [LANGUAGE]. Ensure your TTS voice models (SSML-cloud and/or ElevenLabs)
   support [LANGUAGE]. ElevenLabs and Azure/Google TTS have language-specific voice models â€”
   a mismatch will degrade pronunciation quality significantly.
   Current narrator voice: [NARRATOR_VOICE]
   Verify it is a [LANGUAGE]-capable model before synthesis.
```

If `SPEAKER_MODE` is `multi` and the Speaker Configuration table contains only the narrator row (no character rows), warn:
```
âš ï¸ Speaker Mode is `multi` but no character voices are configured.
Run speckit.audiobook voice add [CHARACTER_NAME] to assign voices before drafting.
Continuing in single-speaker mode for this run.
```
and proceed as `single` speaker mode for this run only.

### Draft Step 3 â€” Parse the prose chapter

Read the prose draft file. Identify:
- Chapter ID and chapter name (from YAML frontmatter: `chapter_id`, `chapter_name`; fall back to filename)
- Prose draft `version` (from frontmatter `version` field; default to `1` if absent)
- All narration passages (prose between dialogue lines)
- All dialogue passages: speaker attribution + quoted text
- Scene breaks (lines containing `* * *`, `---`, or similar)

For each dialogue passage in `multi` speaker mode:
- Extract the speaking character's name from the attribution (e.g., "Marcus said," â†’ `Marcus`)
- Look up that name in the Speaker Configuration table (case-insensitive, also check variant names)
- If no matching row exists, flag the character as `[UNASSIGNED VOICE]` â€” continue but list at the end of the step output

Apply the Pronunciation Lexicon to all text:
- For SSML-cloud: wrap matching words in `<phoneme alphabet="ipa" ph="[IPA]">[Word]</phoneme>`
- For ElevenLabs: replace the word with its `ElevenLabs Substitute` value inline, and record it for the `.pls` entry

Apply Audiobook Style Hints as `<!-- DELIVERY: [hint] -->` HTML comments immediately before each passage where the speaker or context matches a row in the Hints table.

### Draft Step 4 â€” Generate the audiodraft file(s)

Create `FEATURE_DIR/audiodraft/` if it does not exist.

Output file naming:
- SSML-cloud: `FEATURE_DIR/audiodraft/[CHAPTER_ID]_[ChapterName].ssml`
- ElevenLabs: `FEATURE_DIR/audiodraft/[CHAPTER_ID]_[ChapterName]_el.xml`

Populate from `audiobook-draft-template.md`. Fill in:
- YAML frontmatter: `chapter_id`, `chapter_name`, `audiobook_format` (matching `TTS_ENGINE`), `speaker_mode`, `source_draft` (path to prose draft file), `status: audiodraft`, `generated` (today's date), `version` (matching prose draft version)
- For each narration passage:
  - SSML-cloud: wrap in `<voice name="[NARRATOR_VOICE_SSML]"><p>â€¦</p></voice>` with `<break time="600ms"/>` after each paragraph
  - ElevenLabs: emit as a `<!-- VOICE: [NARRATOR_VOICE_EL] | role: narrator -->` segment block
- For each dialogue passage (multi mode):
  - SSML-cloud: close narrator `</voice>`, open `<voice name="[CHARACTER_VOICE_SSML]">`, emit dialogue with `<break time="250ms"/>`, close, reopen narrator voice
  - ElevenLabs: emit as a new `<!-- VOICE: [CHARACTER_EL_VOICE_ID] | role: [CHARACTER_NAME] -->` segment block
- For each scene break: insert `<break time="1500ms"/>` (SSML) or a `<break time="1500ms"/>` line in the narrator segment (ElevenLabs)

### Draft Step 5 â€” Report

```
âœ“ Audiodraft generated

| Field         | Value                                            |
|---|---|
| Chapter       | [CHAPTER_ID] [Chapter Name]                      |
| Prose version | v[N]                                             |
| Format        | ssml-cloud / elevenlabs / both                   |
| Speaker mode  | single / multi                                   |
| SSML file     | audiodraft/[CHAPTER_ID]_[ChapterName].ssml       |
| EL file       | audiodraft/[CHAPTER_ID]_[ChapterName]_el.xml     |
| Lexicon hits  | N words substituted from pronunciation lexicon   |
| Delivery hints| N comments inserted from style hints table       |
```

If any `[UNASSIGNED VOICE]` characters were found:
```
âš ï¸ N character(s) had no voice assignment â€” rendered in narrator voice:
   - [CHARACTER_NAME] (appears in beat [BEAT_ID])
Run: speckit.audiobook voice add [CHARACTER_NAME]
Then re-run: speckit.audiobook draft [CHAPTER_ID]
```

If `all` mode: repeat the table for each chapter and show a summary:
```
âœ… Audiodraft batch complete: N generated, N skipped (already current)
```

---

## Mode: Voice Add

**Purpose**: Add a new narrator/character voice assignment or update an existing one in `constitution.md ## X. Audiobook Production` â†’ Speaker Configuration table.

### Voice Add Step 1 â€” Identify the role

Determine the target role from `$ARGUMENTS`:
- If argument is `narrator` or empty: target the narrator row
- Otherwise: treat argument as a character name and look it up in the Speaker Configuration table (case-insensitive, including variant name forms)

If an existing row is found, display it:
```
Existing voice assignment for [ROLE]:
  SSML-Cloud Voice    : [current value or "not set"]
  ElevenLabs Voice ID : [current value or "not set"]
  Notes               : [current value or "â€”"]

Update this assignment? (y/n)
```
If user answers `n`, stop.

### Voice Add Step 2 â€” Gather TTS engine

Display the current `TTS_ENGINE` from `constitution.md`. Ask:
```
Which TTS engine does this voice apply to?
  1  ssml-cloud â€” Azure TTS, Google Cloud TTS, Amazon Polly
  2  elevenlabs â€” ElevenLabs voice ID
  3  both       â€” fill in both identifiers

Current TTS Engine in constitution.md: [TTS_ENGINE]
Enter 1â€“3:
```

If `TTS_ENGINE` is already set and the user's choice conflicts with it, warn:
```
âš ï¸ TTS Engine in constitution.md is set to [TTS_ENGINE] but you selected [choice].
Do you want to update TTS Engine in constitution.md to match? (y/n)
```

### Voice Add Step 3 â€” Gather voice identifiers

Ask for the applicable fields based on the TTS engine selection:

**SSML-Cloud voice name** (if ssml-cloud or both):
```
SSML-Cloud voice name:
  Examples:
    Azure TTS  : en-US-JennyNeural, en-US-GuyNeural, en-GB-LibbyNeural
    Google TTS : en-US-Neural2-F, en-US-Neural2-D, en-GB-Neural2-A
    Amazon Polly: Joanna, Matthew, Amy
Enter voice name (or leave blank to skip):
```

**ElevenLabs Voice ID** (if elevenlabs or both):
```
ElevenLabs Voice ID or display name:
  Find your voice IDs at: https://elevenlabs.io/app/voice-lab
  Examples: 21m00Tcm4TlvDq8ikWAM  or  Rachel
Enter voice ID or name (or leave blank to skip):
```

**Character function** (if not narrator):
```
Character function (e.g. "protagonist", "antagonist", "comic relief"):
```

**Notes** (optional for both narrator and character):
```
Any notes? (e.g. "use only for chapters 1â€“12", "switch to this voice in Act III", leave blank if none):
```

**Delivery hint** (optional):
```
Delivery hint for this voice (e.g. "Measured, cool, slight distance"):
  This will appear as a style note in all audiodraft files for this character.
  Leave blank if none:
```

### Voice Add Step 4 â€” Update constitution.md

Apply changes to `constitution.md ## X. Audiobook Production`:

1. **Speaker Configuration table**: update the matching row or append a new row:
   ```
   | [role] | [Character / Function] | [SSML-Cloud Voice] | [ElevenLabs Voice ID] | [Notes] |
   ```
2. If `TTS_ENGINE` update was confirmed: update the `**TTS Engine**:` line.
3. If `OUTPUT_MODE` is `book` and a voice was successfully added: offer:
   ```
   Output Mode is currently set to `book`. Update to `audiobook` to enable audiodraft generation? (y/n)
   ```
   If yes: update `**Output Mode**:` to `audiobook`.
4. If a delivery hint was provided: add or update the row in the `### Audiobook Style Hints` table:
   ```
   | [CHARACTER_NAME] | [delivery hint] |
   ```

Confirm:
```
âœ“ Voice assigned: [CHARACTER_NAME or "narrator"]
  SSML-Cloud Voice    : [value or "â€”"]
  ElevenLabs Voice ID : [value or "â€”"]
  Notes               : [value or "â€”"]

constitution.md updated (## X. Audiobook Production).

Audiodraft files already generated for this character will be STALE.
Run: speckit.audiobook check
Then: speckit.audiobook draft all  (to regenerate stale files)
```

---

## Mode: Voice List

**Purpose**: Display all current voice assignments. Read-only.

Print the Speaker Configuration table from `constitution.md ## X. Audiobook Production`, formatted clearly:

```
â”â” Voice Assignments â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  TTS Engine  : [TTS_ENGINE]
  Speaker Mode: [SPEAKER_MODE]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

| Role | Character / Function | SSML-Cloud Voice | ElevenLabs Voice ID | Notes |
|---|---|---|---|---|
[all rows]

â”â” Audiobook Style Hints â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
[hints table or "(none configured)"]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

If `SPEAKER_MODE` is `multi` and only the narrator row is present, append:
```
âš ï¸ No character voices configured for multi-speaker mode.
Run: speckit.audiobook voice add [CHARACTER_NAME]
```

---

## Mode: Lexicon Add

**Purpose**: Register a new pronunciation entry in `constitution.md ## X. Audiobook Production` â†’ Pronunciation Lexicon table.

### Lexicon Add Step 1 â€” Gather the word

If a word was provided in `$ARGUMENTS` after `lexicon add`, use it as the starting value. Otherwise prompt:
```
Word or name to add to the pronunciation lexicon:
```

Check if the word already exists in the Pronunciation Lexicon table (case-insensitive). If found:
```
âš ï¸ "[word]" is already in the pronunciation lexicon:
  IPA               : [current]
  Plain Hint        : [current]
  ElevenLabs Substitute: [current]
Update this entry? (y/n)
```
If `n`, stop.

### Lexicon Add Step 2 â€” Gather pronunciation fields

Ask in sequence:

1. **IPA transcription**:
   ```
   IPA transcription (e.g. ËˆkiËvÉ™ for "Caoimhe"):
   If you're unsure, try: https://www.ipachart.com or https://tophonetics.com
   Enter IPA (or leave blank to skip):
   ```

2. **Plain-text hint**:
   ```
   Plain-text pronunciation hint (e.g. "KEE-vuh"):
   This appears in human narrator scripts and as a fallback guide.
   Enter hint (or leave blank to skip):
   ```

3. **ElevenLabs substitute**:
   ```
   ElevenLabs plain-text substitute (the word ElevenLabs should synthesize instead):
   e.g. "Keeva" instead of "Caoimhe"
   This is injected inline in ElevenLabs audiodraft files and written to lexicon.pls.
   Enter substitute (or leave blank to skip):
   ```

4. **Context note** (optional):
   ```
   Any usage context? (e.g. "only in dialogue", "narrator pronounces differently from characters"):
   Leave blank if none:
   ```

### Lexicon Add Step 3 â€” Write the entry

Append or update the row in `constitution.md ## X. Audiobook Production` â†’ `### Pronunciation Lexicon`:
```
| [Word] | [IPA] | [Plain Hint] | [ElevenLabs Substitute] |
```

Confirm:
```
âœ“ Added: "[word]"  â†’  Pronunciation Lexicon
  IPA               : [value or "â€”"]
  Plain hint        : [value or "â€”"]
  ElevenLabs sub    : [value or "â€”"]
  Total lexicon entries now: N

Next steps:
  Run: speckit.audiobook lexicon export   (to update audiodraft/lexicon.pls)
  Run: speckit.audiobook draft [affected chapters]   (to apply phonemes inline)
```

---

## Mode: Lexicon List

**Purpose**: Display the full pronunciation lexicon. Read-only.

Print the Pronunciation Lexicon table from `constitution.md ## X. Audiobook Production`:

```
â”â” Pronunciation Lexicon â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  N entries

| Word / Name | IPA | Plain Hint | ElevenLabs Substitute |
|---|---|---|---|
[all rows]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

If no entries exist, print:
```
(no pronunciation entries yet)
Run: speckit.audiobook lexicon add [WORD]
```

---

## Mode: Lexicon Export

**Purpose**: Write the pronunciation lexicon to `audiodraft/lexicon.pls` in W3C PLS 1.0 format.

### Lexicon Export Step 1 â€” Load and validate

Load all rows from `constitution.md ## X. Audiobook Production` â†’ `### Pronunciation Lexicon`.

If the lexicon is empty, abort:
```
âœ— Pronunciation Lexicon is empty in constitution.md.
Add entries with: speckit.audiobook lexicon add [WORD]
```

### Lexicon Export Step 2 â€” Generate the .pls file

Create `FEATURE_DIR/audiodraft/` if it does not exist.

Write `FEATURE_DIR/audiodraft/lexicon.pls` with W3C PLS 1.0 XML.
Substitute `[LANGUAGE]` with the BCP-47 code from `constitution.md Â§ VII Language` (default: `en`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
         xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon
           http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"
         alphabet="ipa"
         xml:lang="[LANGUAGE]">
  <!-- Generated by speckit.audiobook lexicon export â€” [DATE] -->
  <!-- [STORY_TITLE] -->
  <!-- Upload to ElevenLabs: Project â†’ Pronunciation Dictionary        -->
  <!-- Azure TTS: attach via SpeechSynthesizer lexicon reference       -->
  <!-- Google TTS: not natively supported; apply phonemes in SSML      -->
  <!-- Amazon Polly: attach via SpeechSynthesizeSpeech with LexiconNames -->
  <lexeme>
    <grapheme>[WORD]</grapheme>
    <phoneme>[IPA]</phoneme>
    <!-- Plain hint: [PLAIN_HINT] | EL substitute: [SUBSTITUTE] -->
  </lexeme>
  <!-- â€¦ one <lexeme> per entry â€¦ -->
</lexicon>
```

For each lexicon row with a non-blank IPA value: emit a `<lexeme>` block.
For entries with no IPA but a non-blank ElevenLabs substitute: emit a `<lexeme>` with `<alias>[SUBSTITUTE]</alias>` instead of `<phoneme>`.
Skip rows where both IPA and ElevenLabs Substitute are blank.

### Lexicon Export Step 3 â€” Report

```
âœ“ Lexicon exported: audiodraft/lexicon.pls
  Entries     : N
  IPA entries : N
  Alias entries: N
  Skipped     : N (no IPA or substitute defined)

Distribution guidance:
  ElevenLabs  : Upload lexicon.pls via Project â†’ Pronunciation Dictionary
  Azure TTS   : Reference via SpeechSynthesizer.AuthorizationToken or SDK lexicon attach
  Amazon Polly: PutLexicon API â†’ reference by LexiconNames in SynthesizeSpeech
  Google TTS  : Lexicon upload not supported â€” phonemes are applied inline in SSML files
```

---

## Mode: Check

**Purpose**: Identify stale and missing audiodrafts relative to prose drafts. Read-only.

### Check Step 1 â€” Load assets

Collect all prose draft files from `FEATURE_DIR/draft/*.md`. For each, read `chapter_id`, `chapter_name`, `version` from YAML frontmatter (default version to `1` if absent).

Collect all audiodraft files from `FEATURE_DIR/audiodraft/` (`.ssml` and `_el.xml`). For each, read `chapter_id`, `version`, `audiobook_format` from YAML frontmatter.

Determine expected files based on `TTS_ENGINE`:
- `ssml-cloud` â†’ expect one `.ssml` per prose draft
- `elevenlabs` â†’ expect one `_el.xml` per prose draft
- `both` â†’ expect both per prose draft

### Check Step 2 â€” Compare and classify

For each prose draft chapter, determine audiodraft state:

| State | Condition |
|---|---|
| âœ… Current | Audiodraft exists and `version` = prose `version` |
| âš ï¸ Stale | Audiodraft exists but `version` < prose `version` |
| âœ— Missing | No audiodraft file found for this chapter ID |

### Check Step 3 â€” Report

```
â”â” Audiodraft Check â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  Prose drafts   : N chapters
  TTS Engine     : [TTS_ENGINE]
  Speaker Mode   : [SPEAKER_MODE]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

| Chapter ID | Chapter Name       | Status      | Prose v | Audio v |
|---|---|---|---|---|
| A1.101     | Chapter One        | âœ… Current   | 2       | 2       |
| A2.201     | The Turning Point  | âš ï¸ Stale     | 3       | 1       |
| A3.301     | Endgame            | âœ— Missing   | 1       | â€”       |

Summary: N current Â· N stale Â· N missing
```

If everything is current:
```
âœ… All audiodraft files are up to date. Nothing to regenerate.
```

If stale or missing files exist, append:
```
To regenerate all stale and missing audiodrafts:
  speckit.audiobook draft all
To regenerate a specific chapter:
  speckit.audiobook draft [CHAPTER_ID]
```

---

## Mode: Status

**Purpose**: Audiobook production dashboard.

```
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  AUDIOBOOK STATUS â€” [STORY_TITLE]
  [Date]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

Production Settings (from constitution.md ## X):
  Output Mode  : [OUTPUT_MODE]
  TTS Engine   : [TTS_ENGINE]
  Speaker Mode : [SPEAKER_MODE]

Voice Assignments:
  Configured   : N voices (narrator + N characters)
  Unassigned   : N characters with dialogue in drafts but no voice entry
  [List unassigned character names if any]

Pronunciation Lexicon:
  Entries      : N
  Exported     : [Yes â€” audiodraft/lexicon.pls exists | No â€” not yet exported]

Audiodraft Files:
  Total prose drafts  : N
  Current audiodrafts : N  (âœ…)
  Stale audiodrafts   : N  (âš ï¸ â€” prose revised after audiodraft)
  Missing audiodrafts : N  (âœ—)

Chapter Table:
| # | Chapter ID | Chapter Name       | Prose Status | Audiodraft | Prose v | Audio v |
|---|---|---|---|---|---|---|
| 1 | A1.101     | Chapter One        | polished     | âœ… current  | 3       | 3       |
| 2 | A2.201     | The Turning Point  | revised      | âš ï¸ stale    | 2       | 1       |
| 3 | A3.301     | Endgame            | draft        | âœ— missing   | 1       | â€”       |

â”â” Recommended Actions â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
[If stale or missing audiodrafts]:
  speckit.audiobook draft all
[If unassigned voices and speaker mode is multi]:
  speckit.audiobook voice add [CHARACTER_NAME]
[If lexicon not exported]:
  speckit.audiobook lexicon export
[If all current]:
  speckit.export audio   â€” assemble chapter manifest and validate for synthesis
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

---

## Post-Execution Hooks

- Look for `hooks.after_audiobook` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.
