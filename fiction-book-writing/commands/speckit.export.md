---
description: Export all drafted chapters to DOCX, EPUB, or LaTeX via pandoc. Assembles chapters in chapter_id order, preferring polished versions when available.
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
   - **Format**: Read from `$ARGUMENTS` (`docx`, `latex`, `tex`, or `epub`).
     If not specified, ask the user: "Export format? `docx` (Word, submission), `epub` (KDP/distributors), or `latex` (typeset)?"
   - **Title**: Read from `$ARGUMENTS` if given; otherwise look for a YAML `title:` field
     or H1 heading in `spec.md`; fall back to `"Untitled Manuscript"`.
   - **Author**: Read from `$ARGUMENTS` if given; otherwise look in `spec.md`; fall back to `"Author Name"`.
   - **Output path**: `FEATURE_DIR/manuscript.docx`, `FEATURE_DIR/manuscript.epub`, or `FEATURE_DIR/manuscript.tex`
     (overridden by `--output` in `$ARGUMENTS` if present).
   - **Reference doc** (DOCX only): If `FEATURE_DIR/manuscript-template.docx` exists,
     pass it as `--reference-doc` for Shunn manuscript formatting.
   - **Cover image** (EPUB only): If `FEATURE_DIR/cover.jpg` or `cover.png` exists,
     pass it as `--cover-image`. If not auto-detected and format is EPUB, note it in the output.
   - **CSS** (EPUB only): If `FEATURE_DIR/epub.css` or `style.css` exists, pass as `--epub-css`.

5. **Run the export script**:
   ```
   python .specify/presets/writing/scripts/python/export.py <format> \
     --draft-dir FEATURE_DIR/draft \
     --output FEATURE_DIR/manuscript.<ext> \
     --title "<title>" \
     --author "<author>" \
     [--reference-doc FEATURE_DIR/manuscript-template.docx]  # DOCX only
     [--cover-image FEATURE_DIR/cover.jpg]                   # EPUB only
     [--epub-css FEATURE_DIR/epub.css]                       # EPUB only
   ```
   On Windows, use `python` or `python3` as available.

6. **Report the result**:
   ```
   ✅ Export complete

   | Field         | Value                              |
   |---|---|
   | Format        | DOCX / LaTeX                       |
   | Chapters      | N                                  |
   | Total words   | ~N,NNN                             |
   | Output        | FEATURE_DIR/manuscript.<ext>       |
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
   > - **Draft2Digital / IngramSpark**: accepted as-is; D2D reformats automatically

   If format is **LaTeX**, add:
   > **Compilation note**: Open `manuscript.tex` in your editor and compile with
   > `pdflatex manuscript.tex` (or `xelatex` for full Unicode/font support).
   > For Overleaf, upload the `.tex` file directly.

7. **Optional — export polished chapters only**:
   If the user passes `polished` or `--polished-only` in `$ARGUMENTS`, add the
   `--polished-only` flag to the script invocation. Report which chapters were
   **skipped** (no polished version yet) in the output table.
