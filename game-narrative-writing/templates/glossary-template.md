# Glossary: [GAME_TITLE]

<!-- Feature: [FEATURE_DIR] | Generated: [GENERATION_DATE] -->
<!-- Consistency reference for all invented terms, proper nouns, variable names, and
     game-specific usage rules. speckit.implement and speckit.checklist check prose
     against this file. speckit.continuity checks world-building consistency.
     Add every term the first time it appears in a node draft. -->

---

## How to Use This File

- **Before outlining**: scan relevant sections for terms that appear in the node
- **While drafting**: if you invent a new term or use a proper noun, add it here immediately
- **speckit.checklist**: uses Spelling & Capitalization rules to flag inconsistencies (PR-002)
- **speckit.continuity**: uses Definition and Constraints columns to flag contradictions
- **speckit.implement**: uses Variable Name Register to validate hook declarations

---

## Term Index

<!-- Quick lookup table. Full entries are in the sections below. -->

| Term | Type | Section | First appearance |
|---|---|---|---|
| [Term] | [invented / proper noun / variable / place / faction] | [I / II / III / IV / V / VI] | NODE-[N] |

---

## I. Invented Terms & Neologisms

<!-- Words that do not exist in standard language or that carry game-specific meaning
     different from their real-world use. -->

### [Term]

| Field | Value |
|---|---|
| Spelling | [exact spelling — case-sensitive where relevant] |
| Plural | [plural form, or "uncountable"] |
| Part of speech | [noun / verb / adjective / proper noun] |
| In-world definition | [what it means to characters who use it — their understanding, not the author's] |
| Author definition | [the full meaning the author intends, including subtext characters don't know] |
| Register | [formal / informal / technical / archaic / slang — which characters use it and how] |
| First introduced | NODE-[N] |
| Usage example | "[Direct quote from draft or planned prose]" |
| Constraints | [What this term must NOT be used to mean or do — prevents drift] |

---

### [Term]

*(repeat block)*

---

## II. Proper Nouns — Characters & Titles

<!-- All named characters, titles of address, and honorifics.
     Spelling and capitalization are enforced across all node drafts. -->

| Name / Title | Spelling | Variant forms | Used by | Notes |
|---|---|---|---|---|
| [Full name] | [exact] | [nickname, title, how antagonists refer to them] | [who uses which form] | [e.g., "NPCs use title only; player always uses first name"] |

---

## III. Proper Nouns — Places

<!-- All named locations, regions, buildings, and geographic features.
     Cross-reference with world-building.md for sensory anchors. -->

| Name | Spelling | Abbreviation / informal form | Type | Notes |
|---|---|---|---|---|
| [Place name] | [exact] | [e.g., "The Hold"] | [district / building / region / landmark] | [e.g., "never 'the [Name]' — no article"] |

---

## IV. Proper Nouns — Factions, Institutions & Objects

<!-- Named groups, organizations, artifacts, or any named object that recurs across nodes. -->

| Name | Spelling | Type | Members / contents | Notes |
|---|---|---|---|---|
| [Name] | [exact] | [faction / institution / artifact / vehicle] | | [e.g., "always capitalized, never abbreviated"] |

---

## V. Variable Name Register

<!-- Human-readable mapping of variable names to what they mean in prose.
     Helps writers refer to the correct variable when writing mechanic hooks.
     speckit.implement and speckit.checklist validate hook declarations against this section. -->

| Variable Name | Human Label | Type | Description |
|---|---|---|---|
| $trust_[name] | [NPC] Trust | trust | How much [NPC] trusts the player (0–100) |
| $inv_[item] | [ITEM_NAME] | inventory | Whether player holds [ITEM_DESCRIPTION] |
| $flag_[name] | [EVENT_NAME] | flag | Whether [EVENT] has occurred |
| $npc_[name]_state | [NPC] State | npc_state | Current condition of [NPC] |
| $end_[id]_progress | [ENDING] Progress | ending_condition | Progress toward [ENDING_NAME] |

---

## VI. Game-Specific Usage Rules

<!-- Conventions that override standard usage for this game.
     speckit.checklist enforces these in the PR categories. -->

### Capitalization Rules

| Rule | Applies to | Example |
|---|---|---|
| [e.g., "Faction names are always capitalized"] | [e.g., "all faction names"] | [e.g., "'the Covenant' not 'the covenant'"] |
| [e.g., "Magic system name is always lowercase"] | | |

### Spelling Preferences

| Preferred | Rejected variants | Notes |
|---|---|---|
| [e.g., "grey"] | [e.g., "gray"] | [e.g., "British spelling throughout"] |

### Terms That Must Not Appear

<!-- Words or phrases banned from this game's prose for consistency, register, or
     world-building reasons. Supplements the Prohibited Phrases list in constitution.md. -->

| Term | Reason | Replacement |
|---|---|---|
| [e.g., "okay"] | [anachronistic register] | [e.g., "all right"] |

### Terms Used With Restricted Meaning

<!-- Words that exist in standard language but carry a specific meaning in this game
     world that differs from common use. -->

| Term | Standard meaning | Game-specific meaning | First use | Constraint |
|---|---|---|---|---|
| [e.g., "the Signal"] | [signal in general] | [specific in-world event or system] | NODE-[N] | [always capitalised; never used generically] |

---

## Consistency Log

<!-- Record of spelling/usage errors caught in drafts and corrected.
     Auto-populated by speckit.continuity and speckit.checklist. Do not edit manually. -->

| Date | Node ID | Error | Correct form | Fixed |
|---|---|---|---|---|
| | | | | No |
