---
name: speckit.bio
description: Author bio manager — draft, refine, and generate context-specific bio variants (agent query, reader back matter, platform profile, social media, first-person). Stores canonical short and long bios in constitution.md § VII.
commands:
  - label: Draft Bio
    icon: edit
    prompt: Draft an author bio from scratch for both query letters and back matter
  - label: Refine Bio
    icon: sparkle
    prompt: Refine and improve the existing author bio
  - label: Generate Variants
    icon: copy
    prompt: Generate bio variants for agent, reader, platform, social, and first-person contexts
---

## Purpose

`speckit.bio` manages the author's canonical bio text and generates context-specific variants. The canonical bios (short and long) live in `constitution.md § VII` and are read automatically by `speckit.query` (for the query-letter bio paragraph) and `speckit.export` (for "About the Author" back matter). Use this command whenever you need to draft, refine, or adapt the bio for a specific submission or platform.

**Variant types**:

| Variant | Length | Person | Use case |
|---|---|---|---|
| `agent` | ≤50 words | 3rd | Query-letter bio paragraph (professional, credential-forward) |
| `reader` | 100–150 words | 3rd | "About the Author" back matter in published book |
| `platform` | ≤25 words | 3rd | KDP/D2D Author Central, IngramSpark contributor bio |
| `social` | ≤160 chars | 1st or 3rd | X/Twitter, Instagram, Bluesky bio field |
| `first-person` | 80–120 words | 1st | Personal website, newsletter, Substack About page |
| `long` | 200–300 words | 3rd | Press kit, festival programme, book club guide |

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding.
Expected formats:
- `draft` — interactive bio drafting from scratch
- `refine` — improve the existing bio stored in constitution.md
- `variant [type]` — generate a specific variant (agent / reader / platform / social / first-person / long)
- `list` — display all bio text currently stored in constitution.md
- `set short [text]` — save a new short bio to constitution.md § VII Author Bio (Short)
- `set long [text]` — save a new long bio to constitution.md § VII Author Bio (Long)
- *(empty)* → default to **draft** if no bio exists in constitution.md; otherwise show `list`

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_bio` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 — Setup and Context Load

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Locate `constitution.md` (at `.specify/memory/constitution.md` or `FEATURE_DIR/constitution.md`).

Read from `constitution.md § VII Stylistic Parameters`:
- `Author Name` — the byline
- `Author Bio (Short)` — existing short bio (≤50 words), if set
- `Author Bio (Long)` — existing long bio (100–150 words), if set
- `Language` — used to determine bio language (default: `en`)

Also read `spec.md` for genre, tone, and logline — used to infer the author's personal connection to the story if not stated.

---

## Mode: List

Display the current bio content from `constitution.md`:

```
Author Bio — [AUTHOR_NAME]

SHORT BIO (agent / platform)
─────────────────────────────
[Author Bio Short text — or "(not set)"]

LONG BIO (back matter / reader)
────────────────────────────────
[Author Bio Long text — or "(not set)"]
```

Suggest next steps:
- If both are unset: `Run speckit.bio draft to create your canonical bios.`
- If only short is set: `Run speckit.bio variant reader to generate the long back-matter version.`
- If both are set: `Run speckit.bio variant [type] to generate platform-specific versions.`

---

## Mode: Draft

Interactive bio creation. All bios are written in `constitution.md § VII Language` (default: English).

### Draft Step 1 — Gather raw material

Ask the following questions one at a time:

```
1. Publication credits (books, stories, journals — or "none / debut"):
```
Wait for answer.
```
2. Relevant professional background (if any — or skip):
   Examples: "Worked as a nurse for 15 years", "Former criminal defence lawyer",
             "Software engineer turned novelist", "Studied history at university"
```
Wait for answer.
```
3. Personal connection to this story or genre (optional but recommended):
   Examples: "Grew up in rural Scotland where the novel is set",
             "This story began as a way to process grief",
             "Has been fascinated by Cold War history since childhood"
```
Wait for answer.
```
4. Where do you live? (City/country — optional, used in some bio styles):
```
Wait for answer.
```
5. Any other facts to include? (awards, memberships, other pen names, pets — or skip):
```
Wait for answer.

### Draft Step 2 — Generate canonical bios

Generate both bios in one pass:

**SHORT BIO** (≤50 words, 3rd person):
- Lead with strongest credential (if debut, open with genre or connection instead)
- One sentence on credential → one sentence on connection or setting → closing hook (what they're working on, or where they live)
- No rhetorical questions. No "When not writing…" opener.
- No "passionate about" or "lifelong lover of"

**LONG BIO** (100–150 words, 3rd person):
- Expand the short bio with one additional credential or story detail
- Add a paragraph about personal connection to the story's theme or setting
- Optional: one sentence on current project or series
- Warm but professional — trade publication tone, not social media tone
- End on forward motion (what they're writing, where they live, what's next)

### Draft Step 3 — Present and confirm

Present both bios:

```
SHORT BIO (for query letters / platform profiles)
──────────────────────────────────────────────────
[SHORT BIO TEXT]
Word count: N

LONG BIO (for "About the Author" back matter)
───────────────────────────────────────────────
[LONG BIO TEXT]
Word count: N
```

Ask:
```
Save these bios to constitution.md? (y/n/edit)
  y     → save as-is
  n     → discard
  edit  → paste revised text to replace
```

If `y`: update `constitution.md § VII Author Bio (Short)` and `Author Bio (Long)`.
Confirm: `✓ Bios saved to constitution.md § VII.`
Remind: `speckit.query will use the short bio. speckit.export will append the long bio as "About the Author".`

---

## Mode: Refine

Load the existing short and long bios from `constitution.md`. Display them (same as `list`).

Ask:
```
Which bio do you want to refine?
  1  Short bio  (currently N words)
  2  Long bio   (currently N words)
  3  Both
```

For each selected bio, ask:
```
What to improve?
  1  Tighten — reduce word count while keeping all key facts
  2  Strengthen opening — make the first sentence more distinctive
  3  Add credential — add a new fact or credit
  4  Remove something — specify what to cut
  5  Change tone — more formal / more warm / more casual
  6  Free edit — describe the change you want
```

Apply the edit, present the revised version, wait for confirmation before saving to `constitution.md`.

---

## Mode: Variant

Generate a context-specific bio variant. Does **not** overwrite the canonical short/long bios in `constitution.md` — variants are for copy-paste use only.

Read the type from `$ARGUMENTS`:

### `agent`
3rd person, ≤50 words, professional register. Same rules as Short Bio draft. If short bio exists, derive from it. Present with word count.

### `reader`
3rd person, 100–150 words, warm register. Same rules as Long Bio draft. If long bio exists, derive from it. Add personal connection if not already present. Present with word count.

### `platform`
3rd person, ≤25 words. KDP / D2D / IngramSpark author profile field.
- One sentence only: credential + genre + one humanising detail.
- Example: "Jane Smith writes psychological thrillers. A former prosecutor, she lives in Edinburgh."
Present with word count. Warn if over 25 words.

### `social`
≤160 characters, 1st or 3rd person (ask preference). X/Twitter/Instagram/Bluesky.
- Lead with what you write, not who you are.
- Example: "Writing psychological thrillers from Edinburgh. Former prosecutor. Debut novel OUT NOW."
Present with character count. Warn if over 160.

### `first-person`
1st person, 80–120 words. Personal website / newsletter / Substack.
- Conversational, warm. Direct address to reader.
- Avoid: "I've always loved books." "Stories have been my passion."
- Open with what you write and why this story matters to you.
Present with word count.

### `long`
3rd person, 200–300 words. Press kit / festival programme / book club guide.
- Three paragraphs: credentials → story connection → current work + contact/social.
Present with word count.

If type not recognised, list available types and ask the user to choose.

---

## Mode: Set Short / Set Long

`set short [text]` — Update `Author Bio (Short)` in `constitution.md § VII` with the provided text.
`set long [text]` — Update `Author Bio (Long)` in `constitution.md § VII` with the provided text.

If `[text]` is missing from `$ARGUMENTS`, prompt:
```
Paste the bio text to save (press Enter twice when done):
```

After saving, confirm:
```
✓ [Short/Long] bio saved to constitution.md § VII.
Word count: N
```

---

## Output Reminder

Canonical bios are consumed by:
- `speckit.query` — uses **short bio** for the query-letter bio paragraph
- `speckit.export` — appends **long bio** as "About the Author" section in EPUB/DOCX back matter
- `speckit.cover` — reads `Author Name` from constitution.md (name only, not bio text)

Variants generated by this command are for copy-paste use and are not saved to any project file.
