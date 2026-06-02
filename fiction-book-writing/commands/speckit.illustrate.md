---
description: Book illustration command — generates detailed illustration briefs and AI image-generation prompts for interior book illustrations. Creates chapter opener illustrations, section dividers, and full-page interior art. Focuses on book-appropriate styles with 2-color and greyscale options typical for published books. Reads existing spec.md, constitution.md, and scene outlines to produce book-ready visual direction. Outputs illustration-brief.md with character descriptions, setting details, mood, and ready-to-paste prompts for Midjourney, DALL-E 3, Adobe Firefly, or Stable Diffusion.
handoffs:
  - label: Generate Cover Art
    agent: speckit.cover
    prompt: Generate a cover brief for this story using the same visual style established in the illustration briefs
    send: false
  - label: Export Manuscript
    agent: speckit.export
    prompt: Export the manuscript to EPUB — illustration images can be embedded in the draft files
    send: false
---
## User Input
```text
$ARGUMENTS
```
You **MUST** consider the user input before proceeding (if not empty).
Accepted arguments:
- `--chapter <chapter-id>` — target a specific chapter (e.g., `A1.101`, `JO3.201`)
- `--scene all` — generate illustrations for all drafted chapters
- `--scene description` — generate illustration for a scene description (interactive mode)
- `--style [name]` — visual style preset (see Style Catalogue below)
- `--color [range]` — color range: `2color` (default), `full`, `greyscale`
- `--aspect [ratio]` — output aspect ratio: `portrait` (default), `landscape`, `square`
- `prompt-only` — output only the image generation prompt, no brief document
- `brief-only` — generate the illustration brief document without writing an image prompt

---
## Purpose
`speckit.illustrate` does not generate images — it produces everything needed to commission or generate book illustrations:
1. **Illustration Brief** (`FEATURE_DIR/illustrations/<CHAPTER_ID>-brief.md`) — a full creative specification for the book illustration
2. **Image Generation Prompt** — a ready-to-paste prompt calibrated to the chosen style, color range, and aspect ratio
3. **Character Reference** — visual cues for characters present in the scene
4. **Setting Details** — key visual elements from locations.md and world-building.md

**What `speckit.illustrate` reads from existing files**:
| Source field | Where it reads |
|---|---|
| Chapter title | `outlines/<CHAPTER_ID>-outline.md` or `draft/<CHAPTER_ID>*.md` |
| Scene beats | `outlines/<CHAPTER_ID>-outline.md` |
| POV character | `outlines/<CHAPTER_ID>-outline.md` |
| Setting | `outlines/<CHAPTER_ID>-outline.md` and `locations.md` |
| Characters present | `outlines/<CHAPTER_ID>-outline.md` and `characters/*.md` |
| Mood/Atmosphere | `constitution.md § VII Tone` and scene sensory anchors |
| Key imagery | `world-building.md` and `themes.md` |
| Illustration defaults | `constitution.md § XI Illustration Guidelines` |

---
## Style Catalogue
Each style preset defines a default approach optimized for book illustrations. Book illustrations typically use 2-color or greyscale palettes for cost-effective printing.
| Key | Style Name | Best for | Typical color range |
|---|---|---|---|
| `penandink` | Pen and Ink | Literary fiction, classics, MG | Greyscale with line weight variation |
| `2color` | Two-Color Print | Chapter openers, section dividers | Duotone (black + 1 accent colour) |
| `greyscale` | Greyscale | Interior illustrations, budget printing | Full greyscale range |
| `woodcut` | Woodcut Print | Historical, literary, horror | High contrast black/white |
| `lineart` | Line Art | MG, chapter headers, decorative | Single color line work |
| `engraving` | Copperplate Engraving | Period pieces, literary | Cross-hatching, greyscale |
| `artnouveau` | Art Nouveau | Fantasy, historical romance | 2-color with flowing lines |
| `artdeco` | Art Deco | 1920s-1930s settings | 2-color geometric style |
| `vintage` | Vintage Book Style | Period pieces, nostalgia | Sepia or 2-color vintage |
| `minimalist` | Minimalist | Contemporary, literary | Limited palette, clean lines |

If no `--style` is given, infer from genre + tone + target audience read from the spec.

---
## Color Range Options
Book illustrations typically use cost-effective color schemes:

| Option | Description | Best for |
|---|---|---|
| `full` | Full color (CMYK/RGB) | Premium editions, children's books |
| `2color` | Two-color printing (black + 1 spot color) | Chapter openers, section dividers, most adult fiction |
| `greyscale` | Greyscale only | Interior illustrations, mass market paperbacks |

The color range affects the prompt construction and palette recommendations.

---
## Execution Steps
### Step 1 — Load Chapter Context
Load the following files if they exist in `FEATURE_DIR/`:
- `outlines/<CHAPTER_ID>-outline.md` — extract: chapter title, POV character, setting, beat sequence, sensory anchors
- `draft/<CHAPTER_ID>*.md` — if outline missing, extract from draft
- `characters/<pov_character>.md` — extract: appearance, clothing style, distinguishing features
- `locations.md` — extract: visual details for the scene's setting
- `world-building.md` — extract: key visual symbols, colours, motifs
- `constitution.md` — extract: Tone, Voice Markers for mood guidance

If the chapter file is missing, emit:
```
⚠️ No outline or draft found for [CHAPTER_ID]. Cannot generate illustration brief.
```

Build an internal **Illustration Seed** object:
```
Chapter:       [CHAPTER_ID] — [Chapter Title]
POV Character: [Character name]
Setting:       [Location name]
Key Beats:     [3–5 key visual moments from beat sequence]
Mood:          [3–5 adjectives from tone/sensory anchors]
Characters:    [List of characters present with brief appearance notes]
Key Objects:   [Important items from the scene]
```

### Step 2 — Resolve Arguments
Parse `$ARGUMENTS` to set:
- `chapter` — required unless `--scene all` or `--scene description`
- `style` — infer from constitution.md § XI Illustration Guidelines if unset, else from genre/tone
- `color` — default from constitution.md § XI Illustration Guidelines if unset, else `2color`
- `aspect` — default from constitution.md § XI Illustration Guidelines if unset, else `portrait`

**Load Illustration Defaults from constitution.md:**
- Read `constitution.md § XI Illustration Guidelines` for:
  - `Illustrations` — if `no`, emit: "⚠️ Illustrations not enabled in constitution.md. Set Illustrations: yes to proceed."
  - `Illustration Automation` — determines output behavior in Step 8:
    - `per-chapter` — generate illustration-brief.md AND create placeholder PNG reference at `illustrations/<CHAPTER_ID>.png`
    - `manual` — generate illustration-brief.md only; user manually adds image links
  - `Default Style` — use as style default
  - `Default Color Range` — use as color default
  - `Default Aspect Ratio` — use as aspect default
  - `Base Design Guideline` — include in prompt construction for consistency

If `--scene all` is passed:
- Scan `outlines/` directory for all outline files
- Generate illustration briefs for each in sequence
- Output summary at the end

If `--scene description` is passed:
- Enter interactive mode to describe a scene
- Ask the user interactively about all options (style, color, aspect, output mode)
- Generate a single illustration brief from the description

If no arguments are provided:
- Ask the user interactively about all options (chapter/scene, style, color, aspect, output mode)
- Wait for user responses before proceeding
- Use defaults for any missing options

### Step 3 — Character Visual Reference
For each character present in the scene:
- Extract appearance details from `characters/<name>.md`
- Note distinguishing features, clothing style, typical expressions
- Record any visual motifs or symbolic elements associated with them

Output as:
```
### Character Visual References
**[Character Name]** (POV):
- Appearance: [age, build, hair, eyes, distinguishing features]
- Clothing: [typical attire, colours, style]
- Expression: [usual expression, emotional state in this scene]
- Visual cues: [symbols, accessories, posture notes]
```

### Step 4 — Setting Visual Details
Extract setting information:
- Primary location from outline
- Key visual elements from `locations.md`
- Atmospheric details from sensory anchors
- Time of day and weather if specified

Output as:
```
### Setting Visual Details
**Location**: [Location name]
- Key elements: [3–5 visual elements that must appear]
- Atmosphere: [lighting, weather, mood]
- Time of day: [if specified]
```

### Step 5 — Image Generation Prompt Construction
Build three prompt variants with color range consideration:

**Color Range Modifiers**:
- `full` — full color illustration
- `2color` — two-color printing (black + 1 accent colour)
- `greyscale` — greyscale only

**Variant A — Hero Moment**: The pivotal visual moment of the scene
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] illustration, [CHARACTER_DESCRIPTION], [SETTING_DESCRIPTION], [KEY_ACTION_OR_EMOTION], [LIGHTING], [MOOD_WORDS], book illustration, [ASPECT_RATIO], no text, no letters, no watermark
```

**Variant B — Environmental**: Setting and atmosphere dominant
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] illustration, [SETTING_DESCRIPTION], [ATMOSPHERIC_DETAILS], [LIGHTING], [MOOD_WORDS], book illustration, [ASPECT_RATIO], no figures, no text
```

**Variant C — Character Study**: Close-up or medium shot of a character
Template:
```
[STYLE_MODIFIER], [COLOR_RANGE] illustration, portrait of [CHARACTER_DESCRIPTION], [EXPRESSION], [LIGHTING], [MOOD_WORDS], book illustration, [ASPECT_RATIO], no text
```

For each variant, also output:
- **Negative prompt**: `text, watermark, letters, signature, blurry, deformed, oversaturated, childish, clipart, color bleed`
- **Midjourney parameters**: `--ar [ratio] --style raw --stylize [value]`

### Step 6 — Write Illustration Brief
Write `FEATURE_DIR/illustrations/<CHAPTER_ID>-brief.md` with the following structure:
```markdown
# Illustration Brief: [CHAPTER_ID] — [Chapter Title]
<!-- Generated: [DATE] | speckit.illustrate | Style: [STYLE] | Color: [COLOR] | Aspect: [RATIO] -->

---

## 1. Scene Context

| Field | Value |
|---|---|
| Chapter ID | [CHAPTER_ID] |
| Chapter Title | [TITLE] |
| POV Character | [CHARACTER] |
| Setting | [LOCATION] |
| Key Beats | [3–5 visual moments] |

---

## 2. Character Visual References

**[Character Name]** (POV):
- Appearance: [details]
- Clothing: [style, colours]
- Expression: [emotional state]
- Visual cues: [symbols, accessories]

---

## 3. Setting Visual Details

**Location**: [Location name]
- Key elements: [visual elements]
- Atmosphere: [lighting, weather, mood]
- Time of day: [if specified]

---

## 4. Visual Style

**Style**: [STYLE_NAME]
[1–2 sentence rationale]

**Color Range**: [COLOR_RANGE]
[Printing consideration note]

**Mood words**: [3–5 adjectives]

---

## 5. Image Generation Prompts

### Variant A — Hero Moment
```
[PROMPT A]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant B — Environmental
```
[PROMPT B]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

### Variant C — Character Study
```
[PROMPT C]
```
Negative: `[NEGATIVE PROMPT]`
MJ params: `[PARAMS]`

---

## 6. Revision History
| Date | Change | By |
|---|---|---|
| [DATE] | Initial brief generated | speckit.illustrate |
```

---

### Step 7 — Output Summary to Chat
After writing the file, output a condensed summary directly in the chat:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ILLUSTRATION BRIEF — [CHAPTER_ID]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Chapter : [CHAPTER_ID] — [Title]
  Style   : [STYLE_NAME]
  Color   : [COLOR_RANGE]
  Aspect  : [RATIO]
  MOOD    : [mood words]
  IMAGE PROMPT — Variant A (recommended first pass):
  ──────────────────────────────────────────────────
  [FULL PROMPT A — paste into Midjourney / DALL-E 3 / Firefly]
  Negative: [NEGATIVE PROMPT]
  Full brief with all 3 variants saved → FEATURE_DIR/illustrations/[CHAPTER_ID]-brief.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If `prompt-only` was passed, output only the prompt block and stop (do not write illustration-brief.md).
If `brief-only` was passed, skip Step 7 chat output and write only the file.

---

### Step 8 — Handle Automation Mode
After writing the illustration brief, check `Illustration Automation` from constitution.md:

**If `per-chapter`:**
1. Create a placeholder PNG file at `FEATURE_DIR/illustrations/<CHAPTER_ID>.png` (1x1 transparent pixel or simple placeholder)
2. Add an illustration comment to the draft file: `<!-- illustration: <CHAPTER_ID>.png -->`
   - Insert at the beginning of the chapter content (after any chapter header)
   - If the draft file doesn't exist yet, note this in the output: "⚠️ Draft file not found — add `<!-- illustration: <CHAPTER_ID>.png -->` manually when draft is created."
3. Output confirmation: "✓ Illustration placeholder created at `illustrations/<CHAPTER_ID>.png` and reference added to draft."

**If `manual`:**
- No additional action required
- Output confirmation: "ℹ️ Manual mode — illustration-brief.md generated. Add `<!-- illustration: <filename>.png -->` comments to draft files manually."

---

## File Naming for Export Integration

Illustration files must follow specific naming conventions for proper export integration:

### Cover Images
Place in the project root:
- `cover.png`
- `cover.jpg` or `cover.jpeg`

### Interior Illustration Files

| Automation Mode | File Location | Naming Pattern |
|---|---|---|
| `per-chapter` | `illustrations/` | `<CHAPTER_ID>.*.{png,jpg,jpeg}` (e.g., `A1.101.png`, `A2.201.jpg`) |
| `manual` | Anywhere in project | Any filename referenced in `<!-- illustration: filename.png -->` comments |

**Supported formats:** PNG, JPG, JPEG

### Export Behavior

When you run `speckit.export`:
- **Cover images** are automatically detected and embedded at the manuscript start
- **Per-chapter illustrations** are embedded at chapter boundaries
- **Manual illustrations** are embedded where `<!-- illustration: ... -->` comments appear in draft files

The export script copies all images to a temporary directory alongside the combined markdown, ensuring pandoc can properly embed them in DOCX, EPUB, and LaTeX outputs.

---

## Constraints
- **Read-only for source files** — spec.md, constitution.md, outlines, and character files are never modified
- **No image generation** — this command produces briefs and prompts; actual image generation requires an external tool
- **Style consistency** — use the same style across all illustrations in a book for visual coherence
- **Character consistency** — maintain consistent character appearance across all illustrations featuring them