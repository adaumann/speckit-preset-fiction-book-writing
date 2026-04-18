---
description: Generate a query letter from spec.md and synopsis.md — hook, story body, housekeeping, comp titles, and author bio. Enforces industry-standard format (250–350 words). Also updates the submission tracker.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
handoffs:
  - label: Write Synopsis First
    agent: speckit.specify
    prompt: The synopsis is missing or incomplete. Help me write the query synopsis section.
    send: false
  - label: Run Polish Pass
    agent: speckit.polish
    prompt: Run a final line-edit pass on the query letter text
    send: true
---

## User Input

```text
$ARGUMENTS
```

Consider user input before proceeding. Accepted arguments:
- `draft` — generate a new draft of the query letter
- `update` / `log` — add a submission log entry to an existing query-letter.md
- `track` — show submission tracker table
- `comp-titles` — suggest comp titles only, based on spec.md genre and themes
- agent name (free text) — generate a personalization paragraph for that specific agent

---

## Purpose

`speckit.query` produces a submission-ready query letter in the standard industry format.  It reads from `spec.md` and `synopsis.md` (if present) so the letter stays in sync with the story itself.

**The query letter has four distinct jobs** — each paragraph must do exactly one:
1. **Personalization** — why this agent (omit for cold)
2. **Hook** — protagonist + inciting incident + stakes in ≤50 words
3. **Body** — setup, escalation, and central dramatic question (~200 words)
4. **Housekeeping + bio** — word count, genre, comp titles, credentials

---

## Steps

1. **Setup**: Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

   **Market detection**: Read `constitution.md § VII Language`. If Language is not `en`, determine the submission convention for that market before proceeding:
   - `de` (German): Standard format is a **German Exposé** — a formal 3–5 page synopsis followed by the first 3 sample chapters. The short US-style query letter (hook + body + comp titles in 300 words) is not standard in German-speaking publishing. Generate an Exposé cover letter instead (see note at the end of Step 4).
   - `fr`, `it`, `es`, `pt`: Query formats vary by publisher — generate the standard US-style structure but add a note: `ℹ️ Query letter conventions differ in [MARKET]. Verify the target publisher's submission guidelines before sending.`
   - Other languages: Generate standard US-style structure with the same market-convention note.
   If Language is `en` or not set: proceed with standard US query letter format.

2. **Check for required sources**:
   - Read `spec.md` — extract: title, genre, logline, protagonist name + identity, central dramatic question, stakes, word count estimate (from tasks.md if not in spec)
   - If `synopsis.md` exists: read the One-Page Synopsis section (250–350 words) as the story body source
   - If `synopsis.md` is absent: warn the user and generate a placeholder body from the spec beats
   - Read `FEATURE_DIR/query-letter.md` if it exists (update mode)

3. **Determine actual word count**:
   - Scan `FEATURE_DIR/draft/*.md` for `actual_words` frontmatter fields; sum them
   - If no drafts exist, use the estimated total from `tasks.md` and note it is an estimate

4. **Generate the query letter** in this exact structure (250–350 words total for the letter body, excluding metadata):

   **Personalization** (0–2 sentences; skip if no specific agent named):
   - Reference a specific MSWL post, recent sale, or panel statement if the agent was named in `$ARGUMENTS`
   - If no agent named: leave a `[PERSONALIZATION]` placeholder

   **Hook** (1–2 sentences, ≤50 words):
   - Model: "[PROTAGONIST], a [role/identity], [inciting incident]. Now [protagonist] must [action] or [consequence]."
   - Draw directly from the logline in `spec.md` — do not invent details
   - No rhetorical questions. No "In a world where…"

   **Body paragraph 1 — Setup** (~75 words):
   - Introduce protagonist with one-phrase identifier (as used in the synopsis)
   - Establish the world in one sentence (genre + setting flavor only)
   - Inciting incident: the event that destroys the protagonist's status quo

   **Body paragraph 2 — Escalation** (~75 words):
   - The central conflict: protagonist vs. antagonistic force (person, system, or internal)
   - The ticking clock or impossible choice
   - What the protagonist has already tried and why it failed

   **Body paragraph 3 — Stakes** (~50 words, optional):
   - What the protagonist stands to lose (internal + external)
   - End on the central dramatic question — do NOT reveal the ending

   **Housekeeping** (1 paragraph):
   - "[TITLE] is a [WORD COUNT]-word [GENRE]."
   - Standalone or series note
   - Comp titles (2 titles, last 3–5 years, same genre/tone)
   - Simultaneous submission note if applicable

   **Bio** (1 paragraph):
   - If `constitution.md § VII Author Bio (Short)` is set, use it verbatim — do not rewrite unless the user explicitly asks.
   - If not set: generate from publication credits → relevant professional credentials → personal connection → debut disclosure-free fallback. Suggest running `speckit.bio draft` to save a canonical version.
   - Never: "This is my first novel." Never: "I've been writing since childhood."

5. **Comp title suggestions** (always include, even without `comp-titles` argument):
   - Suggest 3–4 titles published 2021–2026, same genre as spec.md
   - For each: title, author, year, and one sentence on why it's a comp
   - Flag any suggestion as `[VERIFY — confirm pub date and genre fit]`

6. **Write output** to `FEATURE_DIR/query-letter.md`:
   - Use the `query-letter-template.md` structure
   - Fill the Metadata table from actual values
   - For update mode: add a row to the Version Log and Submission Tracker; do not overwrite the letter text

7. **Quality check on the generated letter**:
   - Word count 250–350 for the letter body (personalization through bio, excluding housekeeping)
   - Hook ≤50 words
   - No rhetorical questions
   - No marketing language ("gripping", "unique", "page-turner", "thought-provoking")
   - Present tense throughout the story body
   - Agent name spelled correctly (if provided)
   - Report any violations as ⚠️ items below the letter

8. **Report**:
   ```
   ✅ Query letter drafted

   | Field         | Value                          |
   |---|---|
   | Title         | [title]                        |
   | Genre         | [genre]                        |
   | Word count    | [N,NNN] (actual / estimated)   |
   | Letter words  | [N] (target: 250–350)          |
   | Output        | FEATURE_DIR/query-letter.md    |

   ⚠️ Issues: [list or "None"]
   ```

---

## German Exposé Format (Language: de)

When `constitution.md § VII Language` is `de`, generate a **Exposé** instead of a US query letter.
Structure:
1. **Anschreiben** (cover letter, 1 page): Greeting, one-sentence pitch (title, genre, word count), brief personal note, closing.
2. **Exposé-Hauptteil** (3–5 pages): Character-driven synopsis with full plot arc including the ending (unlike US query letters, German publishers expect the ending revealed). Tone: clear and professional. Active voice. No rhetorical questions.
3. **Leseprobe** (sample chapters): First 3 chapters or approximately the first 10,000 words — attach separately, not embedded.

File output: `FEATURE_DIR/expose.md` (cover letter + Exposé body). Note separately that the Leseprobe is `draft/*.md` chapters 1–3.

Quality check adjustments for Exposé:
- No comp-title paragraph needed (German publishers rely on genre categories, not comp titles)
- Word count target for the Exposé body: 1,500–3,000 words
- Full plot spoilers required — do not use the US hook-only structure
