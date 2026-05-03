---
description: Generate or adjust themes for compiled stories. For SugarCube: creates story.css with customizable colors, fonts, layout. For Ink: creates ink-theme.html wrapper with themed HTML presentation.
handoffs:
  - label: Compile with Theme
    agent: speckit.compile
    prompt: Compile the game with the new theme applied
    send: false
  - label: Review in Browser
    agent: speckit.polish
    prompt: Check the theme rendering and polish if needed
    send: false
---

# speckit.theme

Generate or update theme files for compiled stories: `story.css` for SugarCube or `ink-theme.html` for Ink.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). Accept free-form
requests like *"dark theme with purple accents and serif font"* or structured flags.

### Flags

| Flag | Values | Effect |
|---|---|---|
| `--engine` | `sugarcube` \| `ink` | Target engine (default: `sugarcube`) |
| `--base` | `dark` \| `light` \| `minimal` | Base template to start from (default: `dark`) |
| `--bg` | any CSS colour value | Override background colour |
| `--text` | any CSS colour value | Override text colour |
| `--accent` | any CSS colour value | Override accent and link colours |
| `--font-body` | CSS font-family string | Override body font |
| `--font-ui` | CSS font-family string | Override UI font |
| `--font-size` | CSS size value | Override base font size |
| `--width` | CSS length value | Override prose column width (SugarCube only) |
| `--no-sidebar` | — | Hide sidebar UI (SugarCube only) |

### Natural language shortcuts (infer from user input if flags not used)

| User says | Interpretation |
|---|---|
| *dark*, *night*, *noir*, *gothic* | `--base dark` |
| *light*, *clean*, *bright*, *paper* | `--base light` |
| *minimal*, *literary*, *invisible UI* | `--base minimal` |
| *purple*, *violet* | `--accent #8b5cf6`, `--color-link` to match |
| *red*, *blood*, *crimson* | `--accent #dc2626`, dark bg variant |
| *green*, *forest*, *terminal* | `--accent #22c55e`, dark bg variant |
| *sepia*, *aged paper* | `--base light`, bg `#f4f0e0`, text `#3b2f1e`, accent `#8b6914` |
| *serif* (already default) | No change |
| *sans-serif*, *modern* | `--font-body: 'Segoe UI', 'Helvetica Neue', sans-serif` |
| *monospace*, *terminal* | `--font-body: 'Fira Code', 'Consolas', monospace` |
| *wide* | `--prose-max-width: 800px` |
| *narrow* | `--prose-max-width: 520px` |

---

## Pre-Execution Checks

1. **Determine target engine** from `--engine` flag, or default to `sugarcube`:
   - If `--engine ink`: proceed to Ink theme generation
   - If `--engine sugarcube`: proceed to SugarCube theme generation

2. **For SugarCube**: Confirm the base template file exists:
   - `dark` → `templates/sugarcube-theme-dark.css`
   - `light` → `templates/sugarcube-theme-light.css`
   - `minimal` → `templates/sugarcube-theme-minimal.css`

3. **For Ink**: Confirm the base template file exists:
   - `dark` → `templates/ink-theme-dark.html`
   - `light` → `templates/ink-theme-light.html`
   - `minimal` → `templates/ink-theme-minimal.html`

4. If output file already exists (story.css for SugarCube / ink-theme.html for Ink):
   - Inform the user and ask: **overwrite** or **edit existing**?
   - If editing existing, apply changes as targeted replacements in the existing file
   - Do NOT regenerate the whole file unless user requests it

5. Read `.specify/memory/constitution.md` (if present) to infer genre and tone:
   - `horror` / `thriller` / `noir` ? suggest `dark` if no base given
   - `romance` / `cosy` / `contemporary` ? suggest `light`
   - `literary` / `experimental` ? suggest `minimal`
   - Apply only as default if user has not specified `--base`

---

## Execution

### Step 1 — Determine mode and engine

Choose the base template file based on `--base` flag or user language inference. Read the
chosen template file in full.

### Step 2 — Apply overrides

For each override requested (flags or natural language), modify the corresponding CSS
custom property value(s) in the `:root {}` block:

| Override target | Properties to change |
|---|---|
| Background | `--color-bg`, `--color-bg-passage`, `--color-bg-sidebar`, `--color-bg-overlay` |
| Text colour | `--color-text`, `--color-text-heading`, `--color-text-muted`, `--color-text-sidebar` |
| Accent / links | `--color-accent`, `--color-accent-dim`, `--color-link`, `--color-link-hover` |
| Body font | `--font-body` |
| UI font | `--font-ui` |
| Font size | `--font-size-base` |
| Prose width | `--prose-max-width` |
| Hide sidebar | Add `#ui-bar { display: none !important; }` after `:root {}` |

When changing a colour:
- Derive `--color-accent-dim` as a desaturated / lower-opacity version of the accent.
- Derive `--color-link-hover` as a lightened (dark theme) or darkened (light theme) version of `--color-link`.
- Derive `--color-bg-sidebar` and `--color-bg-overlay` as slight tonal variants of `--color-bg`.
- Keep contrast ratio = 4.5:1 between `--color-text` and `--color-bg-passage` (WCAG AA).

When changing the font:
- Set both `--font-body` and `--font-ui` if user asks for a single font change with no
  qualifier; split them if user specifies *body font* or *UI font* separately.
- Always include a fallback stack ending in `serif`, `sans-serif`, or `monospace`.

### Step 3 — Write story.css

Write the complete modified CSS to `story.css` in the project root.

Include this header comment block at the very top (fill in the blanks):

```css
/* story.css — [GAME TITLE] — generated by speckit.theme
   Base: [dark|light|minimal]
   Customisations: [list each change made, one per line]
   To regenerate: speckit.theme --base [base] [applied flags]
   Export command: python scripts/python/export.py --target sugarcube --stylesheet story.css
*/
```

### Step 4 — Report

After writing `story.css`, output a brief report:

```
story.css written.

Base:        [dark|light|minimal]
Changes:
  --color-bg          #0f0f13 ? #1a0a2e
  --color-accent      #a78bfa ? #22c55e
  [... list each changed property and old?new value]

Export command:
  python scripts/python/export.py --target sugarcube --stylesheet story.css
```

If nothing was changed (user ran `speckit.theme` with no arguments), copy the base
template verbatim, state which base was used, and suggest common customisation flags.

---

## Adjustment mode (`speckit.theme adjust`)

If the user runs `speckit.theme adjust [description]` and `story.css` already exists:
- Read the existing `story.css` file.
- Apply only the targeted changes described — do NOT regenerate the whole file.
- Update only the relevant custom property values inside `:root {}`.
- Append a comment above the changed line: `/* adjusted: [reason] */`
- Report which properties changed and their old → new values.

---

## Mode: Ink Theme

**Purpose**: Generate or update `ink-theme.html` with a themed HTML wrapper for compiled Ink stories.

### Ink Step 1 — Determine output file

Output file is always `ink-theme.html` in the project root (alongside story.css if present).

Check if `ink-theme.html` exists:
- If yes: ask **overwrite** or **edit existing**?
- If editing: explain that changes must be made manually (HTML is not CSS-property based)
- If creating: proceed to Step 2

### Ink Step 2 — Load base template

Load the base template HTML file from `templates/`:
- `dark` → `templates/ink-theme-dark.html`
- `light` → `templates/ink-theme-light.html`
- `minimal` → `templates/ink-theme-minimal.html`

### Ink Step 3 — Apply overrides (CSS custom properties)

For each override requested, modify the CSS custom property values in the `<style>` block's `:root {}`:

| Override target | Properties |
|---|---|
| Background | `--color-bg`, `--color-bg-passage` |
| Text colour | `--color-text`, `--color-text-heading` |
| Accent / links | `--color-accent`, `--color-link`, `--color-link-hover` |
| Body font | `--font-body` |
| UI font | `--font-ui` |
| Font size | `--font-size-base` |
| Prose width | `--prose-max-width` |

Apply the same principles as SugarCube mode:
- Derive hover states as lightened/darkened variants
- Maintain WCAG AA contrast ratios (4.5:1)
- Always provide fallback font families

### Ink Step 4 — Write ink-theme.html

Write the complete modified HTML to `ink-theme.html` in the project root.

Include this header comment block at the very top (fill in the blanks):

```html
<!-- ink-theme.html — [GAME TITLE] — generated by speckit.theme
     Base: [dark|light|minimal]
     Customisations: [list each change made, one per line]
     To regenerate: speckit.theme --engine ink --base [base] [applied flags]
     Usage: Compile with `python compile.py --spec ... --engine ink`
-->
```

### Ink Step 5 — Report

After writing `ink-theme.html`, output a brief report:

```
✓ ink-theme.html written.

Base:        [dark|light|minimal]
Changes:
  --color-bg          #1a1a1a → #0a0a0a
  --color-accent      #8b5cf6 → #6d28d9
  [... list each changed property and old → new value]

Compilation command:
  python scripts/python/compile.py --spec [SPEC_NAME] --engine ink
  
Output will include themed wrapper in output/ink/story.html
```

---

## SugarCube Theme Reminder

The generated `story.css` targets **Sugarcube 2.x only**. It has no effect on `.ink` or `.rpy` exports. The compiler will automatically include it when present.

For Sugarcube 2.x font loading from Google Fonts or similar, add an `@import` line at the very top of `story.css` before the `:root {}` block:

```css
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;1,400&display=swap');
```

Then reference the loaded family name in `--font-body`.

---

## Ink Theme Reminder

The generated `ink-theme.html` is used automatically by `python compile.py` when:

1. The file `ink-theme.html` exists in the project root
2. Compilation target is `--engine ink`
3. The compiled story.json is wrapped in the themed HTML during output generation

The theme can be switched per-compilation by renaming or temporarily moving `ink-theme.html`, or by running `speckit.theme --engine ink --base [other_base]` to regenerate.
