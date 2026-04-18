---
description: Cover design command — generates a detailed cover brief, AI image-generation prompt, and platform-specific technical specification for KDP (ebook + print), IngramSpark, Draft2Digital, and social media. Reads existing spec.md and constitution.md for title, author, genre, series, tone, and target audience. Outputs a cover-brief.md with element layout, typography direction, colour palette, style rationale, and a ready-to-paste prompt for Midjourney, DALL-E 3, Adobe Firefly, or Stable Diffusion.
handoffs:
  - label: Export Manuscript (EPUB)
    agent: speckit.export
    prompt: Export the manuscript to EPUB — the cover image has been placed at FEATURE_DIR/cover.jpg
    send: false
  - label: Export Manuscript (Print PDF)
    agent: speckit.export
    prompt: Export the manuscript to LaTeX/PDF for print — use the cover brief for the print canvas dimensions
    send: false
  - label: Refine Story Bible
    agent: speckit.constitution
    prompt: Update tone and target audience in the story bible to align with the cover direction
    send: false
  - label: Run Query Letter
    agent: speckit.query
    prompt: Generate a query letter using the same positioning established in the cover brief
    send: false
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
- *(no argument)* — interactive mode: ask for platform, style, and elements step by step
- `--platform [name]` — target platform: `kdp-ebook` *(default)*, `kdp-print`, `ingramspark`, `d2d`, `social`, `all`
- `--style [name]` — visual style preset (see Style Catalogue below)
- `--include [items]` — comma-separated list: `series-title`, `book-title`, `author`, `genre`, `tagline`, `extra-text`, `custom`
- `--exclude [items]` — remove elements from the default set
- `--tagline [text]` — override or add a tagline (short phrase on cover, ≤ 8 words)
- `--extra [text]` — extra text element (e.g. series numbering label "Book One", award text)
- `--custom [text]` — free-form text element (e.g. contributor note, foreword credit)
- `refresh` — regenerate image prompt variations from the same brief (no re-read of spec)
- `prompt-only` — output only the image generation prompt, no brief document
- `brief-only` — generate the cover brief document without writing an image prompt

---

## Purpose

`speckit.cover` does not generate images — it produces everything needed to commission or generate one:

1. **Cover Brief** (`FEATURE_DIR/cover-brief.md`) — a full creative and technical specification the author can hand to a designer or feed into an AI image tool
2. **Image Generation Prompt** — a ready-to-paste prompt calibrated to the chosen style and platform ratio, with negative prompt and parameter flags
3. **Platform Technical Sheet** — pixel dimensions, DPI, colour model, bleed, and file format requirements per target platform
4. **Typography Direction** — font category pairings (title / author / series), hierarchy, placement zones
5. **Colour Palette** — primary, accent, and background tones derived from genre, tone, and target audience signals in spec.md and constitution.md

**What `speckit.cover` reads from existing files**:

| Source field | Where it reads |
|---|---|
| Book title | `spec.md` — first heading or `## Publication Details` |
| Author name | `spec.md ## Publication Details` |
| Series title + position | `spec.md ## Series & Format` |
| Genre | `spec.md ## Genre & Reader Experience` |
| Tone | `spec.md ## Genre & Reader Experience` or `constitution.md § VII Tone` |
| Target audience | `spec.md ## Publication Details` or `constitution.md § VII Target Audience` |
| Logline / tagline seed | `spec.md ## Logline` |
| Mood / atmosphere | `spec.md ## Premise` and `constitution.md § I Voice Markers` |
| Key imagery / symbols | `spec.md ## Thematic Anchors` and `world-building.md` (if present) |

---

## Style Catalogue

Each style preset defines a default palette direction, image generation model parameters, and typography category recommendation.

| Key | Style Name | Best for | Palette direction | Typography |
|---|---|---|---|---|
| `photorealistic` | Photo-Real Composite | Thriller, crime, contemporary, romance | Naturalistic, cinematic colour grading | Sans-serif title, serif author line |
| `illustrated` | Digital Illustration | Fantasy, YA, middle-grade, sci-fi | Saturated, world-building details visible | Display/fantasy font, clean author line |
| `painterly` | Oil/Watercolour Painterly | Literary fiction, historical, upmarket | Muted, warm, textured surface | Classic serif (Garamond-class) |
| `minimalist` | Minimalist Typographic | Literary fiction, short story, essay | Monochromatic or two-tone | Large typographic title, all elements typeset |
| `typographic` | Bold Typographic | Contemporary fiction, thriller, self-help crossover | High-contrast, one strong accent | Heavy condensed font, title dominates |
| `dark-moody` | Dark & Atmospheric | Horror, dark fantasy, psychological thriller | Near-black ground, neon or ember accent | Gothic or condensed display font |
| `cinematic` | Cinematic Wide | Epic fantasy, sci-fi, war fiction | Deep field, lens flare, hero silhouette | Wide-spaced caps title, gold leaf accent |
| `retro-pulp` | Retro Pulp | Genre fiction, noir, sci-fi homage | Aged paper, two-colour halftone look | Distressed slab serif, bold fill |
| `hand-drawn` | Hand-Drawn / Sketch | MG, quirky YA, cozy mystery, humour | Warm white, ink line art, limited colour wash | Hand-lettered title, friendly weight |
| `abstract` | Abstract / Conceptual | Literary fiction, poetry, experimental | Texture, colour field, no figurative element | Minimal: title only, centred, elegant weight |

If no `--style` is given and the user does not select one interactively, infer the best-fit style from genre + tone + target audience read from the spec.

---

## Platform Technical Requirements

| Platform | Variant | Dimensions | DPI | Colour | Format | Bleed | Notes |
|---|---|---|---|---|---|---|---|
| `kdp-ebook` | Ebook cover | 2560 × 1600 px (portrait: 2560 × 1600 ratio 1.6:1) | 72+ | RGB | JPG or TIFF | None | Spine NOT included in ebook cover |
| `kdp-print` | Print cover (6×9) | Calculated: back + spine + front + bleed | 300 | CMYK | PDF | 0.125 in all sides | Spine width = pages × 0.002252 in (60 gsm paper) |
| `kdp-print` | Print cover (5×8) | Calculated: same formula, 5" wide | 300 | CMYK | PDF | 0.125 in | Same spine formula |
| `ingramspark` | Ebook | 2500 × 1563 px minimum | 72+ | RGB | JPG/TIFF | None | ISBN barcode area on back cover |
| `ingramspark` | Print cover | Calculated + bleed + barcode zone | 300 | CMYK preferred PDF/X-1a | PDF | 0.125 in | ISBN barcode reserved: 2 × 1.2 in lower-right back |
| `d2d` | Ebook | 1600 × 2400 px minimum (ratio 1:1.5) | 72+ | RGB | JPG | None | D2D also accepts higher; no spine |
| `social` | Feed post | 1080 × 1080 px | 72 | RGB | JPG/PNG | None | Crop-safe zone: 140 px each side |
| `social` | Story / reel | 1080 × 1920 px | 72 | RGB | JPG/PNG | None | Title zone: upper 30% |

For `--platform all`, generate one brief that covers all variants and note per-variant adaptations.

---

## Execution Steps

### Step 1 — Load Spec and Constitution

Load the following files if they exist in `FEATURE_DIR/`:

- `spec.md` — extract: title, author, series title, series position, genre, tone, logline, target audience, thematic anchors
- `constitution.md` — extract: Tone field (§ VII), Target Audience field (§ VII), Voice Markers (§ I)
- `world-building.md` — extract: key visual symbols, colours, motifs, dominant environment
- `series/series-bible.md` — extract: series visual identity notes (if present)

If `spec.md` is missing, emit:
```
⚠️ No spec.md found. Cover brief will require manual fill-in for title, author, and genre.
```
and continue — leave those fields as `[FILL IN]` placeholders.

Build an internal **Cover Seed** object:
```
Title:         [extracted or FILL IN]
Author:        [extracted or FILL IN]
Series title:  [extracted or "none"]
Series number: [extracted or "none"]
Genre:         [extracted or FILL IN]
Tone:          [extracted or FILL IN]
Audience:      [extracted or FILL IN]
Logline seed:  [first 15 words of logline, or FILL IN]
Mood words:    [3–5 adjectives from premise/voice markers, or FILL IN]
Key imagery:   [symbols, environments, objects from world-building/thematic anchors, or FILL IN]
```

Print the Cover Seed to the user for confirmation before proceeding.

---

### Step 2 — Resolve Arguments

Parse `$ARGUMENTS` to set:

- `platform` — default `kdp-ebook` if unset
- `style` — infer from genre/tone if unset (see Style Catalogue)
- `elements_include` — default set: `book-title`, `author`; add `series-title` if series position is not "standalone"
- `elements_exclude` — remove from include list
- `tagline` — use `--tagline` value if given; otherwise offer to generate one from the logline (see Step 4)
- `extra_text` — use `--extra` value if given
- `custom_text` — use `--custom` value if given

If `$ARGUMENTS` is empty or style/platform are not specified, enter **interactive mode**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  COVER DESIGN — Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Platform target:
  1  kdp-ebook       — KDP ebook (2560×1600 RGB, no spine)
  2  kdp-print       — KDP print (300 DPI CMYK, includes spine)
  3  ingramspark     — IngramSpark (ebook or print)
  4  d2d             — Draft2Digital (1600×2400 RGB)
  5  social          — Social media (1:1 and 9:16 crops)
  6  all             — All platforms (one brief, variant notes)

Enter number or name (default: kdp-ebook):
```

Wait for response, then:

```
Visual style:
  1  photorealistic  — cinematic photo composite
  2  illustrated     — digital art, world-building detail
  3  painterly       — oil/watercolour texture
  4  minimalist      — type-led, near-no imagery
  5  typographic     — bold type dominates
  6  dark-moody      — atmospheric, low-key
  7  cinematic       — epic wide-angle, hero silhouette
  8  retro-pulp      — genre homage, aged palette
  9  hand-drawn      — ink line art, sketch feel
 10  abstract        — conceptual, no figurative element
 11  auto            — infer from genre + tone [recommended]

Enter number or name:
```

Wait for response, then:

```
Cover elements (default set shown — toggle on/off):
  ✓  book-title      — required
  ✓  author          — required
  [series position = non-standalone → ✓ series-title auto-added]
  ○  genre           — genre label or category flag on cover
  ○  tagline         — short phrase (≤ 8 words)
  ○  extra-text      — series number label, award text, etc.
  ○  custom          — anything else (enter text when prompted)

Enter items to toggle (e.g. "tagline extra-text"), or press Enter to accept defaults:
```

If `tagline` is toggled on and no `--tagline` value was given, ask:
```
Tagline text (≤ 8 words — or press Enter to auto-generate from logline):
```

If `extra-text` is toggled on and no `--extra` value was given, ask:
```
Extra text (e.g. "Book One of the Ashfall Chronicles", "Winner — Best Debut 2024"):
```

If `custom` is toggled on and no `--custom` value was given, ask:
```
Custom text element:
```

---

### Step 3 — Style Inference (if style = auto or not set)

Apply the following inference rules in order:

| Condition | Inferred style |
|---|---|
| Genre contains `horror` or `psychological thriller` | `dark-moody` |
| Genre contains `epic fantasy` or `space opera` | `cinematic` |
| Genre contains `middle-grade` or `cozy` | `hand-drawn` |
| Genre contains `literary fiction` and audience = `adult-literary` | `painterly` or `minimalist` |
| Genre contains `thriller` or `crime` or `mystery` | `photorealistic` or `typographic` |
| Genre contains `fantasy` or `sci-fi` and audience = `young-adult` | `illustrated` |
| Genre contains `historical fiction` | `painterly` |
| Genre contains `romance` | `photorealistic` or `illustrated` |
| No strong signal | `illustrated` |

When two options are listed, prefer the first unless tone is `clinical-precise` or `bureaucratic-deadpan` (prefer `typographic`) or tone is `literary-elevated` (prefer the more restrained option).

Inform the user: `Style auto-selected: [style] — based on genre "[genre]" and tone "[tone]". Pass --style [other] to override.`

---

### Step 4 — Colour Palette Construction

Derive a palette of 3–5 colours from the Cover Seed:

**Primary colour** — the dominant cover ground:
- Dark fiction (horror, thriller, dark fantasy): near-black or deep jewel tone (e.g. `#0E0E14`, `#1A0A2E`)
- Fantasy / adventure: rich saturated mid-tone (e.g. deep teal, burnt sienna, forest green)
- Romance: warm rose, deep burgundy, warm cream
- Literary fiction: muted neutral (warm grey, aged ivory, slate)
- MG / cozy: cheerful mid-tone (sky blue, sage, warm yellow)

**Accent colour** — title and key graphic element:
- Contrast ≥ 4.5:1 against primary (WCAG AA)
- One vivid pop: gold, electric blue, crimson, white

**Tertiary colour** — supporting graphic / author line:
- Desaturated version of accent, or contrasting neutral

**Mood words → palette modifiers**:
- "gritty", "raw", "brutal" → desaturate primaries, reduce saturation 20–30%
- "luminous", "ethereal", "dreamlike" → add luminosity, soft glow on edges
- "warm", "nostalgic" → shift hue toward amber; add paper texture overlay suggestion
- "cold", "isolated", "clinical" → cool all hues; steel-blue or grey-green bias

Output palette as:
```
Primary:    [hex] — [description]
Accent:     [hex] — [description]
Tertiary:   [hex] — [description]
Text:       [hex] — title colour (must contrast primary ≥ 4.5:1)
Background: [hex] — back cover / spine ground (print only)
```

---

### Step 5 — Typography Direction

Based on style + genre, recommend font categories (do not name specific commercial fonts unless they are free/open-source — instead describe the typographic class):

| Element | Recommendation |
|---|---|
| **Title** | Font class, weight, size proportion, tracking |
| **Author name** | Font class, size relative to title, position |
| **Series label** | Font class, size (smallest element), position |
| **Tagline** | Font class, italics or not, placement zone |
| **Extra / custom text** | Font class, placement |

**Placement zones** (relative to cover height, portrait orientation):
- Zone A (top 15%): series title, series number
- Zone B (top 20–40%): title (most common) or hero image region
- Zone C (middle 40–60%): hero image focal point
- Zone D (bottom 20–35%): author name
- Zone E (bottom 10%): extra text, tagline (if bottom-placed)

Specify whether title is top- or bottom-anchored based on style:
- `photorealistic`, `cinematic`: title bottom-anchored (image bleeds top)
- `illustrated`, `painterly`: title top-anchored or overlaid on sky region
- `minimalist`, `typographic`, `abstract`: title centred or dominant, image minimal
- `dark-moody`: title bottom third, glowing/embossed treatment
- `retro-pulp`: title top, bold fill, often reversed on dark band
- `hand-drawn`: title hand-lettered style, integrated with illustration

---

### Step 6 — Image Generation Prompt Construction

Build three prompt variants (the user can choose or use all three as iterations):

**Variant A — Hero Subject**: Foreground subject (character, object, environment) dominant

Template:
```
[STYLE_MODIFIER], [SUBJECT_DESCRIPTION], [ENVIRONMENT_DESCRIPTION], [LIGHTING], [COLOUR_PALETTE], [MOOD_WORDS], book cover illustration, [PLATFORM_RATIO], highly detailed, no text, no letters, no watermark
```

**Variant B — Environment / Atmosphere**: No human figure, environment and atmosphere dominant

Template:
```
[STYLE_MODIFIER], [ENVIRONMENT_DESCRIPTION], dramatic atmosphere, [LIGHTING], [COLOUR_PALETTE], [MOOD_WORDS], landscape composition, book cover, [PLATFORM_RATIO], cinematic quality, no figures, no text
```

**Variant C — Object / Symbol**: Single iconic object or symbol from the story

Template:
```
[STYLE_MODIFIER], close-up of [KEY_OBJECT_FROM_WORLD_BUILDING], [SURFACE_TEXTURE], [LIGHTING], [COLOUR_PALETTE], [MOOD_WORDS], symbolic, book cover composition, [PLATFORM_RATIO], no text
```

For each variant, also output:
- **Negative prompt**: `text, watermark, letters, signature, blurry, deformed, oversaturated, childish, clipart, 3D render` (adjust per style)
- **Midjourney parameters**: `--ar [ratio] --style raw --stylize [value] --chaos [value]` (adjust per style)
- **DALL-E 3 / Firefly note**: which variant tends to produce best results in those tools

**Platform ratio** substitution:
- `kdp-ebook`, `ingramspark`, `d2d`: `portrait 5:8 ratio`
- `kdp-print`: `wide portrait with left margin for spine`
- `social` (1:1): `square composition`
- `social` (9:16): `vertical portrait 9:16`

**Style modifier** substitution per style key:

| Style | Modifier phrase |
|---|---|
| `photorealistic` | `photorealistic, cinematic photography, dramatic lighting, 8K` |
| `illustrated` | `digital art illustration, concept art style, detailed fantasy` |
| `painterly` | `oil painting, impressionist brushwork, museum quality` |
| `minimalist` | `minimalist flat design, clean lines, sparse composition` |
| `typographic` | `graphic design, bold typography-focused, geometric` |
| `dark-moody` | `dark atmospheric, chiaroscuro lighting, cinematic horror` |
| `cinematic` | `cinematic epic, wide angle, anamorphic lens flare, golden ratio` |
| `retro-pulp` | `retro pulp magazine illustration, halftone texture, vintage` |
| `hand-drawn` | `hand-drawn ink illustration, watercolour wash, sketch style` |
| `abstract` | `abstract expressionist, colour field, gestural marks` |

---

### Step 7 — Tagline (if included)

If `tagline` element is included and no `--tagline` text was given, generate three tagline options from the logline seed:

Rules:
- **English and non-agglutinative languages** (`Language = en`, `fr`, `es`, `it`, `pt`): Maximum 8 words
- **Agglutinative languages** (`Language = de`, `nl`, `fi`, `hu`, `tr`) or any language where a single token may represent a multi-word concept: Maximum 4 compound words (a compound noun like *Sternenstaub* counts as 1 word, not 2)
- If Language is not set, apply the 8-word rule
- Must not restate the title
- Must create curiosity or dread — avoid describing the plot
- Present tense or gerund preferred ("Some doors are meant to stay closed.")
- Avoid clichés: "One man…", "In a world…", "A journey…"

> **Image generation note**: AI image prompts (Steps 5–6) are ALWAYS written in English regardless of the publication Language setting — image generation models are English-prompt optimised. The Language setting only affects tagline word-count rules and cover copy text.

Present options:
```
Tagline options (pick one or write your own):
  A: [option A]
  B: [option B]
  C: [option C]
```

Wait for selection. If user enters their own text, use that.

---

### Step 8 — Print Spine Calculation (kdp-print / ingramspark only)

If platform includes print variants, ask:
```
Page count (approximate — needed for spine width calculation):
Paper stock:
  1  white (55 gsm / 20 lb) — 0.002252 in/page
  2  cream (60 gsm / 24 lb) — 0.0025 in/page  [default]
  3  colour (80 gsm)        — 0.003 in/page
```

Calculate:
```
Spine width = page_count × inches_per_page
Cover width = back_width + spine_width + front_width + (2 × bleed)
Cover height = trim_height + (2 × bleed)

KDP Print 6×9:
  Front: 6 in | Back: 6 in | Bleed: 0.125 in
  Height: 9 + 0.25 = 9.25 in | Width: 12 + spine + 0.25 in

At 300 DPI:
  Width px  = round(cover_width_in × 300)
  Height px = round(cover_height_in × 300)
```

Report:
```
Print Cover Canvas (KDP 6×9):
  Trim:        6 × 9 in
  Bleed:       0.125 in all sides
  Spine width: [X.XXX] in  ([PAGE_COUNT] pages × [INCHES_PER_PAGE] in)
  Full canvas: [W] × [H] in  →  [WPX] × [HPX] px at 300 DPI
  Colour:      CMYK
  Format:      PDF (PDF/X-1a for IngramSpark)
  Safe zone:   keep all text/logos 0.5 in from any edge
```

---

### Step 9 — Write Cover Brief

Write `FEATURE_DIR/cover-brief.md` with the following structure:

```markdown
# Cover Brief: [TITLE]

<!-- Generated: [DATE] | speckit.cover | Platform: [PLATFORM] | Style: [STYLE] -->

---

## 1. Publication Details

| Field | Value |
|---|---|
| Book title | [TITLE] |
| Author | [AUTHOR] |
| Series | [SERIES_TITLE] / [SERIES_POSITION] or — |
| Genre | [GENRE] |
| Tone | [TONE] |
| Target audience | [AUDIENCE] |

---

## 2. Cover Elements

| Element | Include | Text |
|---|---|---|
| Book title | ✓ | [TITLE] |
| Author name | ✓ | [AUTHOR] |
| Series title | [✓/—] | [SERIES_TITLE] |
| Genre label | [✓/—] | [GENRE_LABEL] |
| Tagline | [✓/—] | [TAGLINE] |
| Extra text | [✓/—] | [EXTRA_TEXT] |
| Custom | [✓/—] | [CUSTOM_TEXT] |

---

## 3. Visual Style

**Style**: [STYLE_NAME]

[1–2 sentence rationale derived from genre/tone/audience]

**Key imagery directions**:
- [Image direction 1 — from world-building or thematic anchors]
- [Image direction 2]
- [Image direction 3]

**Mood words**: [3–5 adjectives]

---

## 4. Colour Palette

| Role | Hex | Description |
|---|---|---|
| Primary | [HEX] | [description] |
| Accent | [HEX] | [description] |
| Tertiary | [HEX] | [description] |
| Title text | [HEX] | [contrast ratio vs primary] |
| Back/spine ground | [HEX] | print only |

---

## 5. Typography Direction

| Element | Font Class | Weight | Position Zone | Notes |
|---|---|---|---|---|
| Title | [class] | [weight] | [zone] | [notes] |
| Author | [class] | [weight] | [zone] | [notes] |
| Series | [class] | [weight] | [zone] | [notes] |
| Tagline | [class] | [weight] | [zone] | [notes] |

---

## 6. Image Generation Prompts

### Variant A — Hero Subject
```
[PROMPT A]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant B — Environment
```
[PROMPT B]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant C — Symbol / Object
```
[PROMPT C]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

**Recommended tool per variant**:
- A: [tool + reason]
- B: [tool + reason]
- C: [tool + reason]

---

## 7. Platform Technical Specifications

### [PLATFORM NAME]
| Spec | Value |
|---|---|
| Dimensions | [W × H px or in] |
| DPI | [DPI] |
| Colour model | [RGB / CMYK] |
| File format | [JPG / PDF / TIFF] |
| Bleed | [in / none] |
| Safe zone | [in from edge] |
| Notes | [platform-specific notes] |

[Repeat section for each platform if --platform all]

[Print canvas calculation block if print platform]

---

## 8. Revision History

| Date | Change | By |
|---|---|---|
| [DATE] | Initial brief generated | speckit.cover |
```

Confirm to the user:
```
Cover brief written to: FEATURE_DIR/cover-brief.md
Platform:  [PLATFORM]
Style:     [STYLE_NAME]
Elements:  [comma-separated element list]
Prompts:   3 variants (A: hero subject, B: environment, C: symbol)

Next step — place your generated cover image:
  FEATURE_DIR/cover.jpg   ← KDP ebook, IngramSpark, D2D (RGB JPG)
  FEATURE_DIR/cover.png   ← alternative (RGB PNG)

speckit.export will auto-detect this file when you run:
  /speckit.export epub
  /speckit.export epub --platform ingramspark --isbn 978-...

For print (KDP / IngramSpark), the full-wrap cover (back + spine + front)
must be a separate file prepared in a design tool using the canvas
dimensions from Section 7 of the cover brief.
```

---

### Step 10 — Output Summary to Chat

After writing the file, output a condensed summary directly in the chat:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  COVER BRIEF — [TITLE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Platform : [PLATFORM]
  Style    : [STYLE_NAME]
  Elements : [element list]
  Tagline  : "[TAGLINE]" (or — if excluded)

  COLOUR PALETTE
  ■ Primary  [HEX]  [description]
  ■ Accent   [HEX]  [description]
  ■ Text     [HEX]  [description]

  IMAGE PROMPT — Variant A (recommended first pass):
  ──────────────────────────────────────────────────
  [FULL PROMPT A — paste into Midjourney / DALL-E 3 / Firefly]

  Negative: [NEGATIVE PROMPT]

  Full brief with all 3 variants saved → FEATURE_DIR/cover-brief.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If `prompt-only` was passed, output only the prompt block and stop (do not write cover-brief.md).
If `brief-only` was passed, skip Step 10 chat output and write only the file.

---

## Constraints

- **Read-only for source files** — spec.md, constitution.md, world-building.md are never modified
- **No image generation** — this command produces briefs and prompts; actual image generation requires an external tool
- **No font licensing** — suggest font *classes* (e.g. "condensed slab serif") not specific commercial typeface names unless they are clearly free/open-source (e.g. Libre Baskerville, EB Garamond, Oswald)
- **Accessibility note**: always flag if the proposed text-on-background contrast ratio is below 4.5:1 (WCAG AA)
- **Print colour warning**: if platform is `kdp-print` or `ingramspark`, remind the user that RGB colours will be converted to CMYK on upload and that the brief colours are RGB approximations only — proof with a CMYK-calibrated tool before ordering
