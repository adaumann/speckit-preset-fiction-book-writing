---
description: Cover design command â€” generates a detailed cover brief, AI image-generation prompt, and platform-specific technical specification for KDP (ebook + print), IngramSpark, Draft2Digital, and social media. Reads existing spec.md and constitution.md for title, author, genre, series, tone, and target audience. Outputs a cover-brief.md with element layout, typography direction, colour palette, style rationale, and a ready-to-paste prompt for Midjourney, DALL-E 3, Adobe Firefly, or Stable Diffusion.
handoffs:
  - label: Export Manuscript (EPUB)
    agent: speckit.export
    prompt: Export the manuscript to EPUB â€” the cover image has been placed at FEATURE_DIR/cover.jpg
    send: false
  - label: Export Manuscript (Print PDF)
    agent: speckit.export
    prompt: Export the manuscript to LaTeX/PDF for print â€” use the cover brief for the print canvas dimensions
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
- *(no argument)* â€” interactive mode: ask for platform, style, and elements step by step
- `--platform [name]` â€” target platform: `kdp-ebook` *(default)*, `kdp-print`, `ingramspark`, `d2d`, `social`, `all`
- `--style [name]` â€” visual style preset (see Style Catalogue below)
- `--include [items]` â€” comma-separated list: `series-title`, `book-title`, `author`, `genre`, `tagline`, `extra-text`, `custom`
- `--exclude [items]` â€” remove elements from the default set
- `--tagline [text]` â€” override or add a tagline (short phrase on cover, â‰¤ 8 words)
- `--extra [text]` â€” extra text element (e.g. series numbering label "Book One", award text)
- `--custom [text]` â€” free-form text element (e.g. contributor note, foreword credit)
- `refresh` â€” regenerate image prompt variations from the same brief (no re-read of spec)
- `prompt-only` â€” output only the image generation prompt, no brief document
- `brief-only` â€” generate the cover brief document without writing an image prompt

---

## Purpose

`speckit.cover` does not generate images â€” it produces everything needed to commission or generate one:

1. **Cover Brief** (`FEATURE_DIR/cover-brief.md`) â€” a full creative and technical specification the author can hand to a designer or feed into an AI image tool
2. **Image Generation Prompt** â€” a ready-to-paste prompt calibrated to the chosen style and platform ratio, with negative prompt and parameter flags
3. **Platform Technical Sheet** â€” pixel dimensions, DPI, colour model, bleed, and file format requirements per target platform
4. **Typography Direction** â€” font category pairings (title / author / series), hierarchy, placement zones
5. **Colour Palette** â€” primary, accent, and background tones derived from genre, tone, and target audience signals in spec.md and constitution.md

**What `speckit.cover` reads from existing files**:

| Source field | Where it reads |
|---|---|
| Book title | `spec.md` â€” first heading or `## Publication Details` |
| Author name | `spec.md ## Publication Details` |
| Series title + position | `spec.md ## Series & Format` |
| Genre | `spec.md ## Genre & Reader Experience` |
| Tone | `spec.md ## Genre & Reader Experience` or `constitution.md Â§ VII Tone` |
| Target audience | `spec.md ## Publication Details` or `constitution.md Â§ VII Target Audience` |
| Logline / tagline seed | `spec.md ## Logline` |
| Mood / atmosphere | `spec.md ## Premise` and `constitution.md Â§ I Voice Markers` |
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
| `kdp-ebook` | Ebook cover | 2560 Ã— 1600 px (portrait: 2560 Ã— 1600 ratio 1.6:1) | 72+ | RGB | JPG or TIFF | None | Spine NOT included in ebook cover |
| `kdp-print` | Print cover (6Ã—9) | Calculated: back + spine + front + bleed | 300 | CMYK | PDF | 0.125 in all sides | Spine width = pages Ã— 0.002252 in (60 gsm paper) |
| `kdp-print` | Print cover (5Ã—8) | Calculated: same formula, 5" wide | 300 | CMYK | PDF | 0.125 in | Same spine formula |
| `ingramspark` | Ebook | 2500 Ã— 1563 px minimum | 72+ | RGB | JPG/TIFF | None | ISBN barcode area on back cover |
| `ingramspark` | Print cover | Calculated + bleed + barcode zone | 300 | CMYK preferred PDF/X-1a | PDF | 0.125 in | ISBN barcode reserved: 2 Ã— 1.2 in lower-right back |
| `d2d` | Ebook | 1600 Ã— 2400 px minimum (ratio 1:1.5) | 72+ | RGB | JPG | None | D2D also accepts higher; no spine |
| `social` | Feed post | 1080 Ã— 1080 px | 72 | RGB | JPG/PNG | None | Crop-safe zone: 140 px each side |
| `social` | Story / reel | 1080 Ã— 1920 px | 72 | RGB | JPG/PNG | None | Title zone: upper 30% |

For `--platform all`, generate one brief that covers all variants and note per-variant adaptations.

---

## Execution Steps

### Step 1 â€” Load Spec and Constitution

Load the following files if they exist in `FEATURE_DIR/`:

- `spec.md` â€” extract: title, author, series title, series position, genre, tone, logline, target audience, thematic anchors
- `constitution.md` â€” extract: Tone field (Â§ VII), Target Audience field (Â§ VII), Voice Markers (Â§ I)
- `world-building.md` â€” extract: key visual symbols, colours, motifs, dominant environment
- `series/series-bible.md` â€” extract: series visual identity notes (if present)

If `spec.md` is missing, emit:
```
âš ï¸ No spec.md found. Cover brief will require manual fill-in for title, author, and genre.
```
and continue â€” leave those fields as `[FILL IN]` placeholders.

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
Mood words:    [3â€“5 adjectives from premise/voice markers, or FILL IN]
Key imagery:   [symbols, environments, objects from world-building/thematic anchors, or FILL IN]
```

Print the Cover Seed to the user for confirmation before proceeding.

---

### Step 2 â€” Resolve Arguments

Parse `$ARGUMENTS` to set:

- `platform` â€” default `kdp-ebook` if unset
- `style` â€” infer from genre/tone if unset (see Style Catalogue)
- `elements_include` â€” default set: `book-title`, `author`; add `series-title` if series position is not "standalone"
- `elements_exclude` â€” remove from include list
- `tagline` â€” use `--tagline` value if given; otherwise offer to generate one from the logline (see Step 4)
- `extra_text` â€” use `--extra` value if given
- `custom_text` â€” use `--custom` value if given

If `$ARGUMENTS` is empty or style/platform are not specified, enter **interactive mode**:

```
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  COVER DESIGN â€” Setup
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

Platform target:
  1  kdp-ebook       â€” KDP ebook (2560Ã—1600 RGB, no spine)
  2  kdp-print       â€” KDP print (300 DPI CMYK, includes spine)
  3  ingramspark     â€” IngramSpark (ebook or print)
  4  d2d             â€” Draft2Digital (1600Ã—2400 RGB)
  5  social          â€” Social media (1:1 and 9:16 crops)
  6  all             â€” All platforms (one brief, variant notes)

Enter number or name (default: kdp-ebook):
```

Wait for response, then:

```
Visual style:
  1  photorealistic  â€” cinematic photo composite
  2  illustrated     â€” digital art, world-building detail
  3  painterly       â€” oil/watercolour texture
  4  minimalist      â€” type-led, near-no imagery
  5  typographic     â€” bold type dominates
  6  dark-moody      â€” atmospheric, low-key
  7  cinematic       â€” epic wide-angle, hero silhouette
  8  retro-pulp      â€” genre homage, aged palette
  9  hand-drawn      â€” ink line art, sketch feel
 10  abstract        â€” conceptual, no figurative element
 11  auto            â€” infer from genre + tone [recommended]

Enter number or name:
```

Wait for response, then:

```
Cover elements (default set shown â€” toggle on/off):
  âœ“  book-title      â€” required
  âœ“  author          â€” required
  [series position = non-standalone â†’ âœ“ series-title auto-added]
  â—‹  genre           â€” genre label or category flag on cover
  â—‹  tagline         â€” short phrase (â‰¤ 8 words)
  â—‹  extra-text      â€” series number label, award text, etc.
  â—‹  custom          â€” anything else (enter text when prompted)

Enter items to toggle (e.g. "tagline extra-text"), or press Enter to accept defaults:
```

If `tagline` is toggled on and no `--tagline` value was given, ask:
```
Tagline text (â‰¤ 8 words â€” or press Enter to auto-generate from logline):
```

If `extra-text` is toggled on and no `--extra` value was given, ask:
```
Extra text (e.g. "Book One of the Ashfall Chronicles", "Winner â€” Best Debut 2024"):
```

If `custom` is toggled on and no `--custom` value was given, ask:
```
Custom text element:
```

---

### Step 3 â€” Style Inference (if style = auto or not set)

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

Inform the user: `Style auto-selected: [style] â€” based on genre "[genre]" and tone "[tone]". Pass --style [other] to override.`

---

### Step 4 â€” Colour Palette Construction

Derive a palette of 3â€“5 colours from the Cover Seed:

**Primary colour** â€” the dominant cover ground:
- Dark fiction (horror, thriller, dark fantasy): near-black or deep jewel tone (e.g. `#0E0E14`, `#1A0A2E`)
- Fantasy / adventure: rich saturated mid-tone (e.g. deep teal, burnt sienna, forest green)
- Romance: warm rose, deep burgundy, warm cream
- Literary fiction: muted neutral (warm grey, aged ivory, slate)
- MG / cozy: cheerful mid-tone (sky blue, sage, warm yellow)

**Accent colour** â€” title and key graphic element:
- Contrast â‰¥ 4.5:1 against primary (WCAG AA)
- One vivid pop: gold, electric blue, crimson, white

**Tertiary colour** â€” supporting graphic / author line:
- Desaturated version of accent, or contrasting neutral

**Mood words â†’ palette modifiers**:
- "gritty", "raw", "brutal" â†’ desaturate primaries, reduce saturation 20â€“30%
- "luminous", "ethereal", "dreamlike" â†’ add luminosity, soft glow on edges
- "warm", "nostalgic" â†’ shift hue toward amber; add paper texture overlay suggestion
- "cold", "isolated", "clinical" â†’ cool all hues; steel-blue or grey-green bias

Output palette as:
```
Primary:    [hex] â€” [description]
Accent:     [hex] â€” [description]
Tertiary:   [hex] â€” [description]
Text:       [hex] â€” title colour (must contrast primary â‰¥ 4.5:1)
Background: [hex] â€” back cover / spine ground (print only)
```

---

### Step 5 â€” Typography Direction

Based on style + genre, recommend font categories (do not name specific commercial fonts unless they are free/open-source â€” instead describe the typographic class):

| Element | Recommendation |
|---|---|
| **Title** | Font class, weight, size proportion, tracking |
| **Author name** | Font class, size relative to title, position |
| **Series label** | Font class, size (smallest element), position |
| **Tagline** | Font class, italics or not, placement zone |
| **Extra / custom text** | Font class, placement |

**Placement zones** (relative to cover height, portrait orientation):
- Zone A (top 15%): series title, series number
- Zone B (top 20â€“40%): title (most common) or hero image region
- Zone C (middle 40â€“60%): hero image focal point
- Zone D (bottom 20â€“35%): author name
- Zone E (bottom 10%): extra text, tagline (if bottom-placed)

Specify whether title is top- or bottom-anchored based on style:
- `photorealistic`, `cinematic`: title bottom-anchored (image bleeds top)
- `illustrated`, `painterly`: title top-anchored or overlaid on sky region
- `minimalist`, `typographic`, `abstract`: title centred or dominant, image minimal
- `dark-moody`: title bottom third, glowing/embossed treatment
- `retro-pulp`: title top, bold fill, often reversed on dark band
- `hand-drawn`: title hand-lettered style, integrated with illustration

---

### Step 6 â€” Image Generation Prompt Construction

Build three prompt variants (the user can choose or use all three as iterations):

**Variant A â€” Hero Subject**: Foreground subject (character, object, environment) dominant

Template:
```
[STYLE_MODIFIER], [SUBJECT_DESCRIPTION], [ENVIRONMENT_DESCRIPTION], [LIGHTING], [COLOUR_PALETTE], [MOOD_WORDS], book cover illustration, [PLATFORM_RATIO], highly detailed, no text, no letters, no watermark
```

**Variant B â€” Environment / Atmosphere**: No human figure, environment and atmosphere dominant

Template:
```
[STYLE_MODIFIER], [ENVIRONMENT_DESCRIPTION], dramatic atmosphere, [LIGHTING], [COLOUR_PALETTE], [MOOD_WORDS], landscape composition, book cover, [PLATFORM_RATIO], cinematic quality, no figures, no text
```

**Variant C â€” Object / Symbol**: Single iconic object or symbol from the story

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

### Step 7 â€” Tagline (if included)

If `tagline` element is included and no `--tagline` text was given, generate three tagline options from the logline seed:

Rules:
- **English and non-agglutinative languages** (`Language = en`, `fr`, `es`, `it`, `pt`): Maximum 8 words
- **Agglutinative languages** (`Language = de`, `nl`, `fi`, `hu`, `tr`) or any language where a single token may represent a multi-word concept: Maximum 4 compound words (a compound noun like *Sternenstaub* counts as 1 word, not 2)
- If Language is not set, apply the 8-word rule
- Must not restate the title
- Must create curiosity or dread â€” avoid describing the plot
- Present tense or gerund preferred ("Some doors are meant to stay closed.")
- Avoid clichÃ©s: "One manâ€¦", "In a worldâ€¦", "A journeyâ€¦"

> **Image generation note**: AI image prompts (Steps 5â€“6) are ALWAYS written in English regardless of the publication Language setting â€” image generation models are English-prompt optimised. The Language setting only affects tagline word-count rules and cover copy text.

Present options:
```
Tagline options (pick one or write your own):
  A: [option A]
  B: [option B]
  C: [option C]
```

Wait for selection. If user enters their own text, use that.

---

### Step 8 â€” Print Spine Calculation (kdp-print / ingramspark only)

If platform includes print variants, ask:
```
Page count (approximate â€” needed for spine width calculation):
Paper stock:
  1  white (55 gsm / 20 lb) â€” 0.002252 in/page
  2  cream (60 gsm / 24 lb) â€” 0.0025 in/page  [default]
  3  colour (80 gsm)        â€” 0.003 in/page
```

Calculate:
```
Spine width = page_count Ã— inches_per_page
Cover width = back_width + spine_width + front_width + (2 Ã— bleed)
Cover height = trim_height + (2 Ã— bleed)

KDP Print 6Ã—9:
  Front: 6 in | Back: 6 in | Bleed: 0.125 in
  Height: 9 + 0.25 = 9.25 in | Width: 12 + spine + 0.25 in

At 300 DPI:
  Width px  = round(cover_width_in Ã— 300)
  Height px = round(cover_height_in Ã— 300)
```

Report:
```
Print Cover Canvas (KDP 6Ã—9):
  Trim:        6 Ã— 9 in
  Bleed:       0.125 in all sides
  Spine width: [X.XXX] in  ([PAGE_COUNT] pages Ã— [INCHES_PER_PAGE] in)
  Full canvas: [W] Ã— [H] in  â†’  [WPX] Ã— [HPX] px at 300 DPI
  Colour:      CMYK
  Format:      PDF (PDF/X-1a for IngramSpark)
  Safe zone:   keep all text/logos 0.5 in from any edge
```

---

### Step 9 â€” Write Cover Brief

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
| Series | [SERIES_TITLE] / [SERIES_POSITION] or â€” |
| Genre | [GENRE] |
| Tone | [TONE] |
| Target audience | [AUDIENCE] |

---

## 2. Cover Elements

| Element | Include | Text |
|---|---|---|
| Book title | âœ“ | [TITLE] |
| Author name | âœ“ | [AUTHOR] |
| Series title | [âœ“/â€”] | [SERIES_TITLE] |
| Genre label | [âœ“/â€”] | [GENRE_LABEL] |
| Tagline | [âœ“/â€”] | [TAGLINE] |
| Extra text | [âœ“/â€”] | [EXTRA_TEXT] |
| Custom | [âœ“/â€”] | [CUSTOM_TEXT] |

---

## 3. Visual Style

**Style**: [STYLE_NAME]

[1â€“2 sentence rationale derived from genre/tone/audience]

**Key imagery directions**:
- [Image direction 1 â€” from world-building or thematic anchors]
- [Image direction 2]
- [Image direction 3]

**Mood words**: [3â€“5 adjectives]

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

### Variant A â€” Hero Subject
```
[PROMPT A]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant B â€” Environment
```
[PROMPT B]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant C â€” Symbol / Object
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
| Dimensions | [W Ã— H px or in] |
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

Next step â€” place your generated cover image:
  FEATURE_DIR/cover.jpg   â† KDP ebook, IngramSpark, D2D (RGB JPG)
  FEATURE_DIR/cover.png   â† alternative (RGB PNG)

speckit.export will auto-detect this file when you run:
  /speckit.export epub
  /speckit.export epub --platform ingramspark --isbn 978-...

For print (KDP / IngramSpark), the full-wrap cover (back + spine + front)
must be a separate file prepared in a design tool using the canvas
dimensions from Section 7 of the cover brief.
```

---

### Step 10 â€” Output Summary to Chat

After writing the file, output a condensed summary directly in the chat:

```
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  COVER BRIEF â€” [TITLE]
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
  Platform : [PLATFORM]
  Style    : [STYLE_NAME]
  Elements : [element list]
  Tagline  : "[TAGLINE]" (or â€” if excluded)

  COLOUR PALETTE
  â–  Primary  [HEX]  [description]
  â–  Accent   [HEX]  [description]
  â–  Text     [HEX]  [description]

  IMAGE PROMPT â€” Variant A (recommended first pass):
  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  [FULL PROMPT A â€” paste into Midjourney / DALL-E 3 / Firefly]

  Negative: [NEGATIVE PROMPT]

  Full brief with all 3 variants saved â†’ FEATURE_DIR/cover-brief.md
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

If `prompt-only` was passed, output only the prompt block and stop (do not write cover-brief.md).
If `brief-only` was passed, skip Step 10 chat output and write only the file.

---

## Constraints

- **Read-only for source files** â€” spec.md, constitution.md, world-building.md are never modified
- **No image generation** â€” this command produces briefs and prompts; actual image generation requires an external tool
- **No font licensing** â€” suggest font *classes* (e.g. "condensed slab serif") not specific commercial typeface names unless they are clearly free/open-source (e.g. Libre Baskerville, EB Garamond, Oswald)
- **Accessibility note**: always flag if the proposed text-on-background contrast ratio is below 4.5:1 (WCAG AA)
- **Print colour warning**: if platform is `kdp-print` or `ingramspark`, remind the user that RGB colours will be converted to CMYK on upload and that the brief colours are RGB approximations only â€” proof with a CMYK-calibrated tool before ordering
