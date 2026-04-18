---
description: Export all drafted chapters to DOCX, EPUB, or LaTeX via pandoc. Supports platform-specific formatting for KDP (ebook + print), IngramSpark (ebook + print), Draft2Digital, and Shunn manuscript standard. Assembles chapters in chapter_id order, preferring polished versions when available.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
handoffs:
  - label: Polish Chapters First
    agent: speckit.polish
    prompt: Run a final line-edit polish pass before exporting
    send: true
  - label: Run Continuity Check
    agent: speckit.continuity
    prompt: Run a full continuity check before export
    send: true
---

## User Input

```text
$ARGUMENTS
```

Consider user input before proceeding (format override, title, author, options).

## Platform Presets

Passing `--platform` selects a pre-configured set of pandoc defaults, CSS, and LaTeX templates from `scripts/templates/`. All platform assets are in the preset and require no setup unless noted.

| Format | Platform | What it configures | Notes |
|---|---|---|---|
| `epub` | `kdp` *(default)* | EPUB 3, `epub.css` (indent, drop cap, chapter breaks), KDP metadata | Cover image required for KDP listing |
| `epub` | `ingramspark` | EPUB 3, same CSS + accessibility metadata slots | Add `--isbn 978-...` for ISBN field |
| `epub` | `d2d` | Minimal EPUB 3 + `epub-d2d.css` (stripped for D2D auto-formatter) | No cover embed; upload cover on D2D dashboard |
| `latex` | `kdp-print-6x9` *(default)* | 6"×9" trim, 0.5" gutter, running headers, chapter title 1/3 down | Compile with `pdflatex` or `xelatex` |
| `latex` | `ingramspark-6x9` | Same geometry + font embedding notes + greyscale option | PDF/X-1a conversion needed; see template header |
| `docx` | `shunn` *(default)* | Shunn manuscript format via `docx-shunn.docx` reference doc | Place `docx-shunn.docx` in `scripts/templates/` — not included (binary) |
| `docx` | `smashwords` | Minimal-style DOCX via `docx-smashwords.docx` reference doc | Place `docx-smashwords.docx` in `scripts/templates/` — not included (binary) |

**DOCX note**: The `.docx` reference files for Shunn and Smashwords are not bundled in the preset (binary files cannot be distributed in a ZIP preset). To use them:
- Shunn: download the official Shunn template from [shunn.net/format/novel](https://www.shunn.net/format/novel/) and place as `scripts/templates/docx-shunn.docx`
- Smashwords: create a blank DOCX with only Normal, Heading 1, and Heading 2 styles, no tabs, no manual line breaks

If no reference doc is found, pandoc uses its built-in defaults (functional but unformatted).

## Export Purpose

`speckit.export` assembles the full manuscript from `draft/` in chapter order and produces a submission-ready DOCX or print-ready LaTeX file.  It delegates all conversion to **pandoc** — a standalone tool that must be installed separately.

**Chapter selection logic** (automatic):
- Files named `<CHAPTER_ID>_<ChapterName>_vN.md` → highest N wins (polished version)
- Files named `<CHAPTER_ID>_<ChapterName>.md` → base draft (used if no polished version)
- Sorted by `chapter_id` from frontmatter (`A1.101`, `A2.201`, etc.)

---

## Steps

1. **Setup**: Run `{SCRIPT}` from repo root. Parse `FEATURE_DIR`.

2. **Check for draft directory**:
   - Look for `FEATURE_DIR/draft/`
   - If it does not exist or contains no `.md` files, stop and report:
     ```
     ⚠️ No chapters found in FEATURE_DIR/draft/
     Draft at least one chapter with speckit.implement before exporting.
     ```

3. **Check for pandoc**:
   - Run `pandoc --version`
   - If pandoc is not installed, stop and display:
     ```
     ⚠️ pandoc not found.
     Install from: https://pandoc.org/installing.html

     macOS:    brew install pandoc
     Windows:  winget install --id JohnMacFarlane.Pandoc -e
     Linux:    sudo apt install pandoc   # or see pandoc.org
     ```

4. **Determine export parameters**:
   - **Format**: Read from `$ARGUMENTS` (`docx`, `latex`, `epub`, or `audio`).
     If not specified, ask the user: "Export format? `docx` (Word, submission), `epub` (KDP/distributors), `latex` (typeset), or `audio` (assemble audiobook drafts from audiodraft/)?"
   - **Platform**: Read from `$ARGUMENTS` (`--platform [name]`).
     If not specified, use the format default: `epub` → `kdp`, `latex` → `kdp-print-6x9`, `docx` → `shunn`.
     Inform the user which platform preset is active: `Platform: kdp (default) — pass --platform ingramspark or --platform d2d to change.`
   - **ISBN** (EPUB + IngramSpark only): Read `--isbn` from `$ARGUMENTS`. If platform is `ingramspark` and no ISBN is provided, emit a WARNING: `⚠️ --isbn not set — IngramSpark requires an ISBN in EPUB metadata. Add --isbn 978-... to the command.`
   - **Title**: Read from `$ARGUMENTS` if given; otherwise look for a YAML `title:` field
     or H1 heading in `spec.md`; fall back to `"Untitled Manuscript"`.
   - **Author**: Read from `$ARGUMENTS` (`--author "..."`) if given; otherwise read `author_name` from `constitution.md § VII Author Name`; then look in `spec.md`; fall back to `"Author Name"`.
   - **Language**: Read `language` from `constitution.md § VII Language` (or pass `--lang` in `$ARGUMENTS` to override). Passed as the `lang` metadata field in EPUB (`dc:language`), DOCX, and LaTeX output. Default: `en`.
   - **Copyright**: Read `copyright` from `constitution.md § VII Copyright` (or pass `--rights "© 2025 ..."` in `$ARGUMENTS` to override). Written as `dc:rights` in EPUB metadata; omitted from output if not set.
   - **About the Author** (EPUB and DOCX): Read `Author Bio (Long)` from `constitution.md § VII`. If set, it is appended as a `# About the Author` section after the final chapter. Pass `--no-author-bio` in `$ARGUMENTS` to suppress. Use `speckit.bio draft` to create the canonical bio if not yet set.
   - **Output path**: `FEATURE_DIR/manuscript.docx`, `FEATURE_DIR/manuscript.epub`, or `FEATURE_DIR/manuscript.tex`
     (overridden by `--output` in `$ARGUMENTS` if present).
   - **Reference doc** (DOCX only): If `FEATURE_DIR/manuscript-template.docx` exists,
     pass it as `--reference-doc` for Shunn manuscript formatting.
   - **Cover image** (EPUB only): If `FEATURE_DIR/cover.jpg` or `cover.png` exists,
     pass it as `--cover-image`. If not auto-detected and format is EPUB, note it in the output.
   - **CSS** (EPUB only): If `FEATURE_DIR/epub.css` or `style.css` exists, pass as `--epub-css`.
   - **Blurb** (EPUB only): If `FEATURE_DIR/blurb.md` exists, read the first 150-word block as
     the back-cover description. If the file does not exist, generate a blurb (see Step 4b) and
     write it to `FEATURE_DIR/blurb.md` before proceeding.

4b. **Blurb generation** (EPUB only — skip for DOCX and LaTeX):

   If `FEATURE_DIR/blurb.md` does not exist, generate a back-cover blurb and write it:

   **Blurb rules** (KDP / retailer standard):
   - 100–150 words. Present tense. Third person (even if the novel is first person).
   - Structure: **hook sentence** (protagonist + disruption) → **escalation** (what they must do, what stands in the way) → **stakes closer** (what is lost if they fail — do NOT reveal the ending or resolution).
   - No rhetorical questions. No marketing language ("gripping", "unforgettable", "page-turning").
   - End on tension, not resolution — the blurb sells the question, not the answer.
   - Source material: `spec.md` logline, character arcs, dramatic question. Do not invent details not in the spec.

   After generating, write to `FEATURE_DIR/blurb.md`:
   ```markdown
   # Back-Cover Blurb: [STORY_TITLE]

   <!-- 100–150 words. Edit here and re-run speckit.export epub to update the EPUB metadata. -->

   [GENERATED_BLURB_TEXT]
   ```
   Notify the user: `✓ blurb.md generated — review and edit before final distribution.`

   If `FEATURE_DIR/blurb.md` already exists, read the first non-comment paragraph as the description text. Validate it is 100–150 words; warn if outside that range but proceed.

5. **Run the export script**:
   ```
   python .specify/presets/fiction-book-writing/scripts/python/export.py <format> \
     --draft-dir FEATURE_DIR/draft \
     --output FEATURE_DIR/manuscript.<ext> \
     --title "<title>" \
     --author "<author>" \
     [--reference-doc FEATURE_DIR/manuscript-template.docx]  # DOCX only
     [--cover-image FEATURE_DIR/cover.jpg]                   # EPUB only
     [--epub-css FEATURE_DIR/epub.css]                       # EPUB only
     [--epub-description FEATURE_DIR/blurb.md]               # EPUB only
   ```
   On Windows, use `python` or `python3` as available.

6. **Report the result**:
   ```
   ✅ Export complete

   | Field         | Value                              |
   |---|---|
   | Format        | DOCX / LaTeX / EPUB                |
   | Chapters      | N                                  |
   | Total words   | ~N,NNN                             |
   | Output        | FEATURE_DIR/manuscript.<ext>       |
   | Blurb         | FEATURE_DIR/blurb.md (EPUB only)   |
   | Pandoc ver.   | X.X                                |
   ```

   If format is **DOCX**, add this guidance:
   > **Manuscript formatting note**: For Shunn manuscript standard (Times New Roman 12pt,
   > double-spaced, 1-inch margins, running header), place a `manuscript-template.docx`
   > in `FEATURE_DIR/` configured with those styles. Pandoc will apply its styles on
   > the next export run. See: https://pandoc.org/MANUAL.html#option--reference-doc

   If format is **EPUB**, add:
   > **EPUB distribution notes**:
   > - **Validate**: run `epubcheck manuscript.epub` or upload to https://www.epubcheck.org/ before distributing
   > - **KDP**: upload `.epub` directly on the manuscript upload step
   > - **Cover image**: place `cover.jpg` or `cover.png` next to `draft/` for auto-detection on the next run
   > - **Custom styling**: place `epub.css` next to `draft/` to control font, spacing, and indentation
   > - **Blurb**: edit `blurb.md` and re-run export to update the back-cover description embedded in the EPUB metadata
   > - **Draft2Digital / IngramSpark**: accepted as-is; D2D reformats automatically

   If format is **LaTeX**, add:
   > **Compilation note**: Open `manuscript.tex` in your editor and compile with
   > `pdflatex manuscript.tex` (or `xelatex` for full Unicode/font support).
   > For Overleaf, upload the `.tex` file directly.

7. **Optional — export polished chapters only**:
   If the user passes `polished` or `--polished-only` in `$ARGUMENTS`, add the
   `--polished-only` flag to the script invocation. Report which chapters were
   **skipped** (no polished version yet) in the output table.

8. **Audio export** (format `audio` only — skip for all other formats):

   8a. **Locate audiobook drafts**:
   - Look for `FEATURE_DIR/audiodraft/` containing `.ssml` and/or `_el.xml` files
   - If the directory does not exist or is empty, stop and report:
     ```
     ⚠️ No audiobook drafts found in FEATURE_DIR/audiodraft/
     Run speckit.implement with Output Mode set to `audiobook` or `both`
     in constitution.md ## X to generate audiobook draft files first.
     ```

   8b. **Read audiobook configuration** from `constitution.md ## X. Audiobook Production`:
   - `TTS_ENGINE`, `SPEAKER_MODE`, Speaker Configuration table, Pronunciation Lexicon

   8c. **Validate drafts**:
   - Collect all `.ssml` / `_el.xml` files; sort by `chapter_id` from each file's YAML header
   - Identify any prose draft chapters (`draft/`) that have **no corresponding audiobook draft** — list them in the report as `⚠️ Missing audiobook draft`
   - If `audiodraft/lexicon.pls` exists, validate XML is well-formed; report a warning if not

   8d. **Assemble and report**:
   - Do NOT concatenate audio drafts into a single file (ACX and most TTS platforms require per-chapter files)
   - Instead, produce a **chapter manifest** at `FEATURE_DIR/audiodraft/manifest.md`:
     ```markdown
     # Audiobook Chapter Manifest: [STORY_TITLE]

     | # | Chapter ID | Chapter Name | SSML File | EL File | Segments | Status |
     |---|---|---|---|---|---|---|
     | 1 | A1.101 | Awakening | A1.101_Awakening.ssml | A1.101_Awakening_el.xml | N | audiodraft |
     ```
   - Report:
     ```
     ✅ Audiobook export complete

     | Field          | Value                                   |
     |---|---|
     | Chapters       | N                                       |
     | SSML files     | audiodraft/*.ssml                       |
     | EL files       | audiodraft/*_el.xml                     |
     | Lexicon        | audiodraft/lexicon.pls                  |
     | Manifest       | audiodraft/manifest.md                  |
     | Speaker mode   | single / multi                          |
     | Missing drafts | N chapters have no audiobook draft yet  |
     ```

   8e. **Distribution guidance** (append to report):

   > **SSML-cloud (Azure / Google / Amazon Polly)**:
   > - Pass each `.ssml` file's content to your TTS API. One API call per chapter.
   > - Azure TTS: `POST /cognitiveservices/v1` with `Content-Type: application/ssml+xml`
   > - Amazon Polly: `SynthesizeSpeech` with `TextType: ssml`
   > - Google Cloud TTS: `synthesize` with `input.ssml`
   > - Output format: MP3 192kbps, mono or stereo — required by ACX

   > **ElevenLabs**:
   > - Upload `audiodraft/lexicon.pls` to your ElevenLabs project's pronunciation dictionary first
   > - For each `_el.xml` file: split on `<!-- VOICE: ... -->` segment boundaries and POST each segment to `/v1/text-to-speech/{voice_id}` with `model_id: eleven_multilingual_v2`
   > - Stitch segments in order to produce the chapter MP3

   > **ACX submission (Audible)**:
   > - Required: MP3 192kbps, -23 LUFS integrated loudness, -3 dBFS peak, room tone under -60 dBFS
   > - One MP3 per chapter + one retail audio sample (first 5 minutes or opening chapter)
   > - Tools: normalize with Auphonic (automatic) or Audacity (manual) before submission
