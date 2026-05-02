---
description: Glossary management command â€” add (register a new term, proper noun, or usage rule), check (scan drafted chapters for glossary violations â€” misspellings, wrong capitalisation, rejected variants, banned terms, and restricted-meaning drift), audit (completeness check â€” find invented terms in drafts not yet registered), and status (dashboard of all terms, open violations, and coverage). Works with glossary.md as the single consistency authority; speckit.polish and speckit.continuity both enforce it.
handoffs:
  - label: Run Polish Pass
    agent: speckit.polish
    prompt: Run a final line-edit pass and enforce glossary rules
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check including glossary compliance
    send: true
  - label: Revise Chapter
    agent: speckit.revise
    prompt: Revise the chapter to fix glossary violations
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
- *(no argument)* â€” display the glossary status dashboard (same as `status`)
- `add [term]` â€” register a new term interactively (e.g. `add the Shatter`)
- `add [term] --type [type]` â€” skip the type prompt: `invented`, `character`, `place`, `faction`, `rule`
- `check` â€” scan all drafted chapters for glossary violations (read-only)
- `check [CHAPTER_ID]` â€” scope the check to a specific chapter (e.g. `check A2.201`)
- `audit` â€” find invented terms and proper nouns in drafted chapters that are not yet registered in glossary.md (read-only)
- `audit [CHAPTER_ID]` â€” scope the audit to a specific chapter
- `status` â€” glossary dashboard: term counts, open violations, coverage by section

---

## Purpose

`speckit.glossary` manages `glossary.md` as the active consistency authority for invented terms, proper nouns, and story-specific usage rules. It bridges the glossary template â€” generated at `speckit.plan` time â€” with the ongoing drafting and revision workflow.

**What each mode covers**:

| Mode | When to use | Writes files? |
|---|---|---|
| `add` | Any time a new term, name, or rule is established | Yes â€” `glossary.md` only |
| `check` | Before polishing a chapter; before querying/exporting | No â€” read-only |
| `audit` | After drafting a chapter or act, to catch unregistered terms | No â€” read-only |
| `status` | Any time â€” overview of glossary health | No â€” read-only |

**Integration with other commands**:
- `speckit.plan` seeds `glossary.md` with terms from `spec.md` and `constitution.md`.
- `speckit.polish` enforces VR-006 (glossary violations) using this file.
- `speckit.continuity` checks world-building against this file and appends to `## Consistency Log`.
- `speckit.glossary check` is a focused, author-initiated version of those passive checks â€” run it before polishing a chapter to resolve violations proactively.

---

## Pre-Execution Checks

**Check for extension hooks**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_glossary` key.
- Process as standard hook block (Optional/Mandatory). Skip silently if absent.

---

## Step 1 â€” Setup and Mode Resolution

Run `{SCRIPT}` from repo root and parse `FEATURE_DIR`.

Locate `FEATURE_DIR/glossary.md`. If the file does not exist:
- For `add` mode: create it from `glossary-template.md`. Populate the header from `spec.md` (`[STORY_TITLE]`, `[FEATURE_DIR]`, today's date). Seed `## Term Index` from any invented terms or proper nouns found in `spec.md` â€” character names, place names, faction names. Mark each seeded entry as `[NEEDS CLARIFICATION]` for full definition. Emit: `âœ“ Created glossary.md from template. Proceeding to add first term.`
- For `check`, `audit`, or `status`: abort with `âœ— glossary.md not found. Run speckit.glossary add [term] to create it, or run speckit.plan to generate it from the story brief.`

Parse `$ARGUMENTS` for mode, optional term/chapter, and optional flags. Resolve mode:
- `add â€¦` â†’ **Mode: Add**
- `check â€¦` â†’ **Mode: Check**
- `audit â€¦` â†’ **Mode: Audit**
- `status` or *(empty)* â†’ **Mode: Status**

---

## Mode: Add

**Purpose**: Register a new term, proper noun, or usage rule in `glossary.md`.

### Add Step 1 â€” Determine entry type

If `--type` was provided in `$ARGUMENTS`, use it. Otherwise display:

```
What type of entry is this?

  1  invented    â€” A word or phrase that doesn't exist in standard English,
                   or a standard word with a story-specific meaning
  2  character   â€” A character name, title, or honorific (Section II)
  3  place       â€” A location, region, or geographic feature (Section III)
  4  faction     â€” A group, institution, artifact, or named object (Section IV)
  5  rule        â€” A capitalization rule, spelling preference, banned term,
                   or restricted-meaning convention (Section V)

Enter 1â€“5:
```

### Add Step 2 â€” Gather entry fields

#### For type `invented` (Section I):

Ask in sequence (accept inline `--` flags where matching):

1. **Exact spelling** â€” case-sensitive. Prompt: `Exact spelling (case-sensitive):`
2. **Plural form** â€” or "uncountable" / "no plural". Prompt: `Plural form (or "uncountable" / "none"):`
3. **Part of speech** â€” noun / verb / adjective / proper noun
4. **In-world definition** â€” what characters understand it to mean
5. **Author definition** â€” full intended meaning including subtext characters don't know (may match in-world if no gap). Prompt: `Full author definition (including any subtext characters don't know):`
6. **Register** â€” formal / informal / technical / archaic / slang â€” which characters use it
7. **First introduced** â€” Beat ID and chapter ID. Prompt: `First introduced (beat ID and chapter ID, e.g. A1.103):`
8. **Usage example** â€” a line from draft prose or planned prose. May be left blank.
9. **Constraints** â€” what the term must NOT be used to mean or do. Prompt: `Any constraints on how this term must not be used? (leave blank if none):`

If the term already exists in `## Term Index`: warn `âš ï¸ [term] is already in the glossary. Do you want to update the existing entry? (y/n)` â€” if yes, show the current entry and update only the fields the user provides.

#### For type `character` (Section II):

1. **Full name** â€” exact canonical spelling
2. **Variant forms** â€” nicknames, titles, how antagonists refer to them
3. **Used by** â€” who uses which form (family, outsiders, etc.)
4. **Notes** â€” any usage rules (e.g. "never use nickname in narration, only in dialogue")

#### For type `place` (Section III):

1. **Name** â€” exact spelling
2. **Abbreviation or informal form** â€” if any
3. **Type** â€” city / region / building / landmark / other
4. **Article rule** â€” does it take "the"? Is it ever used without the article?
5. **Notes**

#### For type `faction` (Section IV):

1. **Name** â€” exact spelling
2. **Type** â€” faction / institution / artifact / vehicle / other
3. **Members or contents** â€” brief
4. **Notes** â€” capitalization rules, abbreviation policy

#### For type `rule` (Section V):

Display sub-type menu:
```
What kind of rule?
  a  Capitalization rule
  b  Spelling preference (e.g. "grey" not "gray")
  c  Term that must not appear (banned term)
  d  Term used with restricted meaning
```

- **a** â€” gather: Rule statement, Applies to, Example
- **b** â€” gather: Preferred form, Rejected variants, Notes
- **c** â€” gather: Term, Reason for ban, Replacement (if any)
- **d** â€” gather: Term, Standard meaning, Story-specific meaning, First use, Constraint

### Add Step 3 â€” Write the entry

Append the completed entry to the appropriate section of `glossary.md`. Also add a row to `## Term Index`:

```
| [Term] | [type] | [Section I/II/III/IV/V] | [Beat ID] |
```

Confirm:
```
âœ“ Added: "[term]"  â†’  glossary.md  Section [I/II/III/IV/V]
  Type    : [type]
  Spelling: [exact form]
  [Any constraint noted]
  Total terms now: [N]
```

---

## Mode: Check

**Purpose**: Scan drafted chapters for glossary violations. Read-only.

### Check Step 1 â€” Load assets

Load all sections of `glossary.md`. Build the enforcement ruleset:

- **Spelling list**: all entries from Sections Iâ€“IV â€” exact spellings and their rejected variants
- **Capitalization rules**: all rows from `## V. Capitalization Rules`
- **Spelling preferences**: all rows from `## V. Spelling Preferences`
- **Banned terms**: all rows from `## V. Terms That Must Not Appear`
- **Restricted meanings**: all rows from `## V. Terms Used With Restricted Meaning`
- **Consistency Log**: existing entries from `## Consistency Log` â€” do not re-flag already-logged errors that are marked `Fixed: Yes`

Determine draft scope:
- If a chapter ID was given: load only `FEATURE_DIR/draft/[CHAPTER_ID]*.md` (prefer highest `_vN` version).
- Otherwise: load all `FEATURE_DIR/draft/*.md` files (highest version of each stem).
- If no draft files exist: abort with `âœ— No draft files found. Nothing to check.`

### Check Step 2 â€” Scan for violations

For each draft chapter in scope, scan for:

**VG-001 â€” Misspelling or wrong capitalisation**
Scan prose for any occurrence of a term from Sections Iâ€“IV where the spelling or capitalisation differs from the registered canonical form.
Example: glossary registers `the Shatter` (capitalised); draft uses `the shatter`.

**VG-002 â€” Rejected variant form**
Scan for any variant form listed in the `Rejected variants` column of `## V. Spelling Preferences` or recorded as a known alternate in a Section Iâ€“IV entry.
Example: glossary registers `grey` preferred, `gray` rejected; draft uses `gray`.

**VG-003 â€” Banned term**
Scan for exact or near-exact occurrence of any term listed in `## V. Terms That Must Not Appear`.
Example: glossary bans `okay` (anachronistic); draft uses `okay`.

**VG-004 â€” Restricted meaning drift**
Detect any use of a term listed in `## V. Terms Used With Restricted Meaning` where context implies the standard meaning rather than the story-specific meaning.
This is a judgment call â€” flag as WARNING only if the usage is clearly the standard meaning in context.

**VG-005 â€” Invented term used before first appearance**
For any invented term in Section I with a `First introduced` beat ID: check whether any chapter with an earlier chapter ID uses the term.

For each violation found:

```
VG-[N][NN]: [violation type]
  Chapter  : [CHAPTER_ID]
  Passage  : "[quoted fragment â€” 10â€“20 words]"
  Issue    : [what is wrong]
  Correct  : [the canonical form or expected usage]
```

### Check Step 3 â€” Append to Consistency Log

For each new violation found (not already present in `## Consistency Log`): append a row:

| [today's date] | [CHAPTER_ID] | [error description] | [correct form] | No |

This is the only write operation this mode performs.

### Check Step 4 â€” Output report

```
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  GLOSSARY CHECK REPORT
  Scope   : [chapter ID or "all drafted chapters"]
  Terms enforced : [N]  Rules enforced : [N]
  Date    : [YYYY-MM-DD]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

### Violations Found
VG-001 â€” Misspelling / capitalization : [N]
VG-002 â€” Rejected variant             : [N]
VG-003 â€” Banned term                  : [N]
VG-004 â€” Restricted meaning drift     : [N] (WARNINGS)
VG-005 â€” Used before introduction     : [N]

[Detail block per violation]

### PASS
[Dimensions with no violations listed here]

### Summary
Total violations: [N]  |  New Consistency Log entries added: [N]
Recommended action: [run speckit.revise [CHAPTER_ID] to fix violations / all clear â€” safe to polish]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

---

## Mode: Audit

**Purpose**: Find invented terms and proper nouns in draft chapters that are not yet registered in `glossary.md`. Read-only â€” no files are written.

### Audit Step 1 â€” Load assets

Load the full `## Term Index` from `glossary.md`. Build a known-terms list: all registered spellings plus their variant forms.

Determine chapter scope (same logic as Mode: Check).

### Audit Step 2 â€” Extract candidate terms

For each draft chapter in scope, identify candidate unregistered terms by looking for:

1. **Capitalised common nouns** not at sentence start â€” likely proper nouns or invented titles
2. **Words in quotation marks used as terms** (e.g., *"the Warding"*, *"a Null"*) â€” in-world technical vocabulary
3. **Words with story-specific hyphenation or unusual compounding** not in standard English dictionaries
4. **Repeated proper-noun-looking phrases** that appear 2+ times in the chapter but are not in the term index

Filter out: standard proper nouns (real people, real places), common title words (`Mr.`, `Dr.`, etc.), and any term already listed in `## Term Index`.

### Audit Step 3 â€” Output report

```
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  GLOSSARY AUDIT REPORT
  Scope   : [chapter ID or "all drafted chapters"]
  Date    : [YYYY-MM-DD]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

### Unregistered Terms Found
| Term | Appears in | Occurrences | Likely type | Action |
|---|---|---|---|---|
| the Shatter | A1.103, A1.105 | 4 | invented / place | Add to glossary |
| Commander Vasek | A1.103 | 2 | character | Add to Section II |
| grey-bond | A2.201 | 1 | invented | Add to glossary or verify spelling |

### Already Registered (confirmed)
[N] terms found in scope â€” all registered in glossary.md.

### Recommendation
[N] unregistered candidates found. Run `speckit.glossary add [term]` for each, or confirm they are standard English terms that do not need registration.
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

---

## Mode: Status

**Purpose**: Glossary health dashboard. Read-only.

```
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  GLOSSARY STATUS: [STORY_TITLE]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

### Term Coverage
| Section | Terms registered | Needs clarification |
|---|---|---|
| I  â€” Invented terms       | [N] | [N] |
| II â€” Characters & titles  | [N] | [N] |
| III â€” Places              | [N] | [N] |
| IV â€” Factions & objects   | [N] | [N] |
| V  â€” Usage rules          | [N] rules | â€” |

Total: [N] terms + [N] rules

### Open Consistency Log Violations
| Date | Chapter | Error | Correct | Fixed |
|---|---|---|---|---|
| [date] | [chapter] | [error] | [correct] | No |
â€¦
([N] open / [M] total)

### Terms with [NEEDS CLARIFICATION]
| Term | Section | Missing field |
|---|---|---|
| [term] | I | Author definition |
â€¦
([N] incomplete entries)
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

If there are open Consistency Log violations:
```
âš ï¸  [N] open violation(s) in Consistency Log. Run `speckit.revise [CHAPTER_ID]` to fix each,
    then update the Fixed column to Yes.
```

If there are `[NEEDS CLARIFICATION]` entries:
```
â„¹ï¸  [N] incomplete glossary entries. Run `speckit.glossary add [term]` to complete them.
```

If all entries are complete and no open violations exist:
```
âœ“ Glossary complete â€” no open violations. Safe to proceed with speckit.polish or speckit.export.
```

---

## Post-Execution Hooks

Check for extension hooks after execution:
- Look for `hooks.after_glossary` in `.specify/extensions.yml`. Process as standard hook block. Skip silently if absent.

**Update search index** (optional â€” large projects):
- If `.specify/index/` exists, run: `python scripts/python/index.py update` from the project root.
- Updated `glossary.md` is re-indexed so semantic queries return current terminology and constraints.
- If the command fails or the index does not exist, skip silently.
