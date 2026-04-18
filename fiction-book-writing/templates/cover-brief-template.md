# Cover Brief: [STORY_TITLE]

<!-- Created: [CREATION_DATE] | speckit.cover | Platform: [PLATFORM] | Style: [STYLE] -->
<!-- Edit this file directly to refine direction, then re-run /speckit.cover refresh to get new prompts. -->

---

## 1. Publication Details

| Field | Value |
|---|---|
| Book title | [STORY_TITLE] |
| Author | [AUTHOR_NAME] |
| Series | [SERIES_TITLE] — [SERIES_POSITION] |
| Genre | [GENRE] |
| Tone | [TONE] |
| Target audience | [TARGET_AUDIENCE] |

---

## 2. Cover Elements

| Element | Include | Text / Value |
|---|---|---|
| Book title | ✓ | [STORY_TITLE] |
| Author name | ✓ | [AUTHOR_NAME] |
| Series title | [✓/—] | [SERIES_TITLE] |
| Genre label | [✓/—] | [GENRE_LABEL] |
| Tagline | [✓/—] | [TAGLINE] |
| Extra text | [✓/—] | [EXTRA_TEXT] |
| Custom | [✓/—] | [CUSTOM_TEXT] |

---

## 3. Visual Style

**Style**: [STYLE_NAME]

<!-- 1–2 sentences explaining why this style fits the genre/tone/audience. -->
[STYLE_RATIONALE]

### Key Imagery Directions

<!-- Derived from world-building.md, thematic anchors, and spec.md premise. -->
- [IMAGE_DIRECTION_1]
- [IMAGE_DIRECTION_2]
- [IMAGE_DIRECTION_3]

**Mood words**: [MOOD_WORD_1], [MOOD_WORD_2], [MOOD_WORD_3], [MOOD_WORD_4]

---

## 4. Colour Palette

| Role | Hex | Description |
|---|---|---|
| Primary | [HEX] | [e.g. dominant cover ground — near-black] |
| Accent | [HEX] | [e.g. title and key graphic element — gold] |
| Tertiary | [HEX] | [e.g. author line, secondary graphic — muted amber] |
| Title text | [HEX] | [contrast ratio vs. primary: X.X:1 — WCAG AA ≥ 4.5:1] |
| Back/spine ground | [HEX] | [print only — may match primary] |

> ⚠️ **Print note**: These are RGB approximations. Convert to CMYK using a calibrated tool before uploading for print. IngramSpark requires PDF/X-1a; KDP print accepts CMYK PDF.

---

## 5. Typography Direction

| Element | Font Class | Weight | Position Zone | Notes |
|---|---|---|---|---|
| Title | [e.g. condensed display serif] | Bold / Heavy | Zone B (top 20–40%) | [e.g. large, tracked wide, all-caps option] |
| Author | [e.g. clean humanist sans-serif] | Regular | Zone D (bottom 20–35%) | [e.g. smaller than title, centred] |
| Series label | [e.g. small caps serif] | Light | Zone A (top 15%) | [e.g. smallest element, above title] |
| Tagline | [e.g. italic serif] | Regular Italic | Zone E (bottom 10%) | [e.g. line under author, or above title] |
| Extra text | [e.g. sans-serif] | Light | Zone E | [e.g. series number label] |

**Title anchor**: [top-anchored / bottom-anchored / centred]
<!-- photorealistic/cinematic → bottom-anchored; illustrated/painterly → top-anchored or overlaid; minimalist/typographic → centred dominant -->

---

## 6. Image Generation Prompts

> Paste any of these directly into Midjourney, DALL-E 3, Adobe Firefly, or Stable Diffusion.
> The prompt is designed for [PLATFORM_RATIO] composition.
> Run all three as iterations; pick the strongest, then refine with inpainting or variations.

### Variant A — Hero Subject
<!-- Foreground subject (character, object, environment) dominant -->
```
[PROMPT_A]
```
**Negative prompt**: `[NEGATIVE_PROMPT_A]`
**Midjourney**: `--ar [RATIO] --style raw --stylize [VALUE] --chaos [VALUE]`
**Best tool**: [e.g. Midjourney v6 — handles the figure-environment blend best]

### Variant B — Environment / Atmosphere
<!-- No human figure; atmosphere and environment dominant -->
```
[PROMPT_B]
```
**Negative prompt**: `[NEGATIVE_PROMPT_B]`
**Midjourney**: `--ar [RATIO] --style raw --stylize [VALUE] --chaos [VALUE]`
**Best tool**: [e.g. DALL-E 3 — strong on atmospheric landscapes without figure distortion]

### Variant C — Symbol / Object
<!-- Single iconic object or symbol from the story world -->
```
[PROMPT_C]
```
**Negative prompt**: `[NEGATIVE_PROMPT_C]`
**Midjourney**: `--ar [RATIO] --style raw --stylize [VALUE] --chaos [VALUE]`
**Best tool**: [e.g. Adobe Firefly — strong on object isolation with clean background]

---

## 7. Platform Technical Specifications

<!-- speckit.cover fills this section automatically. Edit manually if adapting the brief. -->

### [PLATFORM_NAME]

| Spec | Value |
|---|---|
| Dimensions | [W × H px] |
| DPI | [DPI] |
| Colour model | [RGB / CMYK] |
| File format | [JPG / PDF / TIFF] |
| Bleed | [in or none] |
| Safe zone | [distance from edge for all text/logos] |
| Notes | [platform-specific notes] |

<!-- For print platforms: -->
<!-- Print Canvas Calculation
  Trim:         [W] × [H] in
  Spine width:  [X.XXX] in  ([PAGE_COUNT] pages × [IN_PER_PAGE] in/page)
  Full canvas:  [W_in] × [H_in] in  →  [W_px] × [H_px] px at 300 DPI
  ISBN barcode: lower-right back, 2 × 1.2 in reserved zone (IngramSpark)
-->

---

## 8. Designer Handoff Notes

<!-- Optional: add any notes for a human designer or AI tool operator -->
- [NOTE_1]
- [NOTE_2]

### Cover Image Placement for Export

Once the final cover image is ready, place it here so `speckit.export` auto-detects it:

| File | Used by |
|---|---|
| `FEATURE_DIR/cover.jpg` | KDP ebook EPUB, IngramSpark EPUB, D2D EPUB |
| `FEATURE_DIR/cover.png` | Alternative — same detection, same path |

`speckit.export epub` will embed the file automatically via `--epub-cover-image`.
For **print** (KDP print / IngramSpark), the full-wrap cover (back + spine + front) is a
separate deliverable — use the canvas dimensions from Section 7 above and upload directly
to the platform dashboard.

---

## 9. Revision History

| Date | Change | By |
|---|---|---|
| [CREATION_DATE] | Initial brief generated | speckit.cover |
