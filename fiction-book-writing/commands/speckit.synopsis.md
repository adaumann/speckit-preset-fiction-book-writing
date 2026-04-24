---
description: Generate a one-page (250–350 words) and full (1,000–2,000 words) synopsis from plan.md and the draft. Both formats are in present tense, third person, and reveal the ending. Run after speckit.plan (outline synopsis) or after drafting (accurate synopsis).
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
handoffs:
  - label: Write Query Letter
    agent: speckit.query
    prompt: Use the synopsis to draft a query letter
    send: true
  - label: Polish Synopsis
    agent: speckit.polish
    prompt: Run a line-edit polish pass on the synopsis prose
    send: true
  - label: Fix Story Structure
    agent: speckit.plan
    prompt: The synopsis exposed structural gaps — revisit the plan
    send: false
---

## User Input

```text
$ARGUMENTS
```

Consider user input before proceeding. Accepted arguments:
- `draft` / (empty) — generate both one-page and full synopsis
- `one-page` — generate or regenerate only the 250–350 word version
- `full` — generate or regenerate only the 1,000–2,000 word version
- `update` — regenerate from current draft (post-draft accuracy pass)
- `check` — validate an existing synopsis.md against spec.md and plan.md for accuracy

---

## Purpose

`speckit.synopsis` produces two submission-ready synopsis formats that agents and editors require:

- **One-page synopsis** (250–350 words): The compressed narrative arc. Used in most query packages.
- **Full synopsis** (1,000–2,000 words): The complete beat-by-beat account. Required by many publishers on partial/full requests.

Both formats **reveal the ending**. A synopsis is not a blurb. Every major plot turn and character arc resolution must be stated explicitly.

**Key rules**:
- Present tense, even if the novel is past tense
- Third person, even if the novel is first person
- No marketing language ("gripping", "heart-wrenching", "unforgettable")
- No rhetorical questions
- Name only characters essential to the plot (P1, P2, and named antagonist)
- Introduce named characters with a one-phrase identifier on first mention: `ELENA (a disgraced archivist)`

---

## Steps

1. **Setup**: Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

2. **Load source documents** (in priority order):
   - `FEATURE_DIR/spec.md` — extract: title, genre, logline, protagonist, central dramatic question, theme, word count target
   - `FEATURE_DIR/plan.md` — extract: act breakdown, chapter map, phase summaries
   - `FEATURE_DIR/draft/*.md` — if present, read for actual plot events (post-draft mode)
   - **Large project optimization** (if `.specify/index/` exists and project has >30 drafted chapters): instead of loading all draft files, query the index for the key structural passages at each arc section:
     ```
     python scripts/python/index.py query "inciting incident point of no return" --type draft --top 3
     python scripts/python/index.py query "midpoint reversal first act break" --type draft --top 3
     python scripts/python/index.py query "darkest moment all is lost crisis" --type draft --top 3
     python scripts/python/index.py query "climax resolution closing image" --type draft --top 3
     ```
     Use returned chunks (with `chapter_id` and `section` metadata) to identify the actual prose events for each arc section. Load those specific chapter files in full for accurate quotation. Supplement with `plan.md` for any section not covered by the index.
   - If `FEATURE_DIR/synopsis.md` already exists: load it and report in `update` or `check` mode

3. **Determine mode**:
   - If `draft/` exists and contains chapter files → **post-draft mode** (use actual events)
   - Otherwise → **outline mode** (use plan.md act breakdown as source)
   - Report the active mode before generating

4. **Check: does synopsis.md already exist?**
   - If yes and argument is empty/`draft`: ask the user to confirm overwrite, or use `update` argument to proceed automatically
   - If `check`: run step 8 only (validation), do not regenerate

5. **Build the narrative arc** from source documents:

   | Arc section | Source | Target length (full) |
   |---|---|---|
   | Opening situation & inciting incident | Act I / chapters 1–3 | ~200 words |
   | Point of no return | Act I close | ~150 words |
   | Rising stakes & midpoint | Act II first half | ~300 words |
   | Darkest moment / all is lost | Act II close | ~150 words |
   | Climax | Act III opening | ~200 words |
   | Resolution | Act III close | ~100 words |

   Cross-check each section against:
   - Central dramatic question from `spec.md` (must be answered at Climax)
   - Named character arcs (every named character's arc must resolve in Resolution)
   - Theme statement (must be reflected in the Resolution paragraph)

6. **Generate the full synopsis** (1,000–2,000 words):
   - Follow the arc structure above
   - Use `synopsis-template.md` section headings
   - On first mention of each named character: `NAME (one-phrase identifier)`
   - Every plot turn that would surprise a reader must be stated explicitly — no ellipsis, no "and things get worse"
   - End every section with a sentence that creates forward momentum into the next section

7. **Generate the one-page synopsis** (250–350 words) by compressing the full synopsis:
   - Keep: protagonist identity, inciting incident, central conflict, midpoint reversal, darkest moment, climax decision, resolution
   - Cut: subplots, secondary character arcs, world-building detail, chapter-level events
   - Target: one paragraph per act (3–4 paragraphs total)
   - Final sentence must state the resolution — do not end on a question

8. **Quality validation** (run on both formats):

   | Check | Pass condition |
   |---|---|
   | Word count (one-page) | 250–350 words |
   | Word count (full) | 1,000–2,000 words |
   | Ending revealed | Resolution section names the outcome explicitly |
   | Tense | Present tense throughout |
   | Person | Third person throughout |
   | Dramatic question answered | CDQ from spec.md is resolved at Climax |
   | No marketing language | No "gripping", "haunting", "unforgettable", "powerful", "timely" |
   | No rhetorical questions | No sentences ending in `?` |
   | Character arcs resolved | Every named character's arc outcome stated |

   Report any violations as ⚠️ items. Fix automatically where possible (tense, person drift).

9. **Write output** to `FEATURE_DIR/synopsis.md` using `synopsis-template.md`:
   - Fill the Metadata table from actual values
   - Place the one-page synopsis in the **One-Page Synopsis** section
   - Place the full synopsis in the **Full Synopsis** section with sub-headings

10. **Report**:
    ```
    ✅ Synopsis generated

    | Field            | Value                        |
    |---|---|
    | Mode             | outline / post-draft         |
    | One-page words   | NNN                          |
    | Full words       | N,NNN                        |
    | Output           | FEATURE_DIR/synopsis.md      |
    | Warnings         | N (listed below if any)      |
    ```

    If `next step` is query letter: suggest `/speckit.query draft`.
