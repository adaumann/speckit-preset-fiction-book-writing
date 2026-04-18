#!/usr/bin/env python3
"""export.py — Manuscript exporter for the spec-kit writing preset.

Assembles all drafted chapters from draft/ in chapter_id order and exports to
DOCX (Shunn-style manuscript format) or LaTeX (book class, double-spaced)
via pandoc.

Automatically prefers the latest polished version (_vN.md) of each chapter
when one exists, falling back to the base draft.

Usage:
    python export.py docx [options]
    python export.py latex [options]    # or: tex
    python export.py epub [options]

Options:
    --draft-dir PATH        Path to draft/ directory (auto-detected if omitted)
    --output FILE, -o FILE  Output file (default: manuscript.docx / manuscript.tex / manuscript.epub)
    --title TITLE           Manuscript title (reads from spec.md if omitted)
    --author NAME           Author name (reads from constitution.md/spec.md if omitted)
    --lang LANG             BCP-47 language code for EPUB metadata (reads from constitution.md if omitted; default: en)
    --rights TEXT           Copyright statement for dc:rights metadata (reads from constitution.md if omitted)
    --author-bio TEXT       "About the Author" back matter text (reads from constitution.md if omitted)
    --no-author-bio         Suppress "About the Author" back matter even if set in constitution.md
    --cover-image FILE      Cover image for EPUB (jpg/png)
    --reference-doc FILE    Custom pandoc reference .docx for DOCX formatting
    --epub-css FILE         Custom CSS stylesheet for EPUB
    --polished-only         Skip chapters that have no polished (_vN) version
    --status STATUS         Only include chapters with this status field
                            (e.g. "polished", "draft"; default: all statuses)

Requirements:
    pandoc >= 2.11  (https://pandoc.org/installing.html)
    Python >= 3.9   (no third-party packages required)
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Extract YAML frontmatter dict and body text from a markdown file.

    Only handles simple key: value lines — no nested YAML.  Sufficient for
    the chapter header blocks written by speckit.implement.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    meta: dict[str, str] = {}
    for line in fm_text.splitlines():
        if ":" in line and not line.strip().startswith("#"):
            key, _, val = line.partition(":")
            # Strip inline YAML comments and surrounding quotes/whitespace
            val = val.split("#")[0].strip().strip('"').strip("'")
            meta[key.strip()] = val
    return meta, body


def strip_draft_notes(body: str) -> str:
    """Remove <!-- DRAFT NOTES ... --> comment blocks left by speckit.implement."""
    return re.sub(r"<!--\s*DRAFT NOTES.*?-->", "", body, flags=re.DOTALL).strip()


# ---------------------------------------------------------------------------
# Chapter collection & sorting
# ---------------------------------------------------------------------------

_CHAPTER_ID_RE = re.compile(r"^([A-Za-z]+)(\d+)\.(\d+)$")
_VERSION_RE = re.compile(r"_v(\d+)\.md$")


def _chapter_sort_key(item: tuple[dict[str, str], str]) -> tuple:
    cid = item[0].get("chapter_id", "")
    m = _CHAPTER_ID_RE.match(cid)
    if m:
        return (m.group(1), int(m.group(2)), int(m.group(3)))
    # Fall back to lexicographic sort on the raw id
    return (cid, 0, 0)


def collect_chapters(
    draft_dir: Path,
    polished_only: bool = False,
    status_filter: str | None = None,
) -> list[tuple[dict[str, str], str]]:
    """Return sorted list of (frontmatter, body) for all chapters in draft_dir.

    Prefers the highest-numbered _vN.md polished version when one exists;
    falls back to the base .md file.  Optionally skips unpublished drafts.
    """
    # Group files by their base stem (strip versioning suffix)
    groups: dict[str, list[Path]] = {}
    for f in sorted(draft_dir.glob("*.md")):
        vm = re.match(r"^(.+?)(_v\d+)?\.md$", f.name)
        if vm:
            stem = vm.group(1)
            groups.setdefault(stem, []).append(f)

    chapters: list[tuple[dict[str, str], str]] = []
    for stem, files in groups.items():
        versioned = [f for f in files if _VERSION_RE.search(f.name)]
        if versioned:
            best = max(versioned, key=lambda f: int(_VERSION_RE.search(f.name).group(1)))  # type: ignore[union-attr]
        else:
            if polished_only:
                continue
            base = [f for f in files if not _VERSION_RE.search(f.name)]
            if not base:
                continue
            best = base[0]

        text = best.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        body = strip_draft_notes(body)

        if status_filter and meta.get("status") != status_filter:
            continue

        if body.strip() or meta:
            chapters.append((meta, body))

    chapters.sort(key=_chapter_sort_key)
    return chapters


# ---------------------------------------------------------------------------
# Template directory resolution
# ---------------------------------------------------------------------------

def find_templates_dir() -> Path | None:
    """Locate the scripts/templates/ directory relative to this script."""
    here = Path(__file__).resolve().parent
    candidate = here.parent / "templates"
    if candidate.is_dir():
        return candidate
    return None


# Platform → template file mapping.
# Keys are (format, platform) tuples.
# Values are dicts with optional keys: epub_defaults, epub_css, latex_template, reference_doc.
_PLATFORM_TEMPLATES: dict[tuple[str, str], dict[str, str]] = {
    ("epub", "kdp"):              {"epub_defaults": "epub-kdp.yml",          "epub_css": "epub.css"},
    ("epub", "ingramspark"):      {"epub_defaults": "epub-ingramspark.yml",  "epub_css": "epub.css"},
    ("epub", "d2d"):              {"epub_defaults": "epub-d2d.yml",          "epub_css": "epub-d2d.css"},
    ("latex", "kdp-print-6x9"):   {"latex_template": "latex-kdp-6x9.tex"},
    ("latex", "ingramspark-6x9"): {"latex_template": "latex-ingramspark-6x9.tex"},
    # docx platforms use a reference-doc .docx file placed in the templates dir.
    # The files are not included in the preset (binary); the command tells the
    # user where to place them.
    ("docx", "shunn"):            {"reference_doc": "docx-shunn.docx"},
    ("docx", "smashwords"):       {"reference_doc": "docx-smashwords.docx"},
}

_PLATFORM_DEFAULTS: dict[str, str] = {
    "epub": "kdp",
    "latex": "kdp-print-6x9",
    "docx": "shunn",
}


def resolve_platform_templates(
    fmt: str,
    platform: str | None,
    templates_dir: Path | None,
) -> dict[str, Path | None]:
    """Return resolved Paths for template assets given format + platform.

    Returns a dict with keys: epub_defaults, epub_css, latex_template, reference_doc.
    Any key not applicable to the current format is None.
    """
    result: dict[str, Path | None] = {
        "epub_defaults": None,
        "epub_css": None,
        "latex_template": None,
        "reference_doc": None,
    }
    if platform is None:
        platform = _PLATFORM_DEFAULTS.get(fmt)
    if platform is None or templates_dir is None:
        return result
    mapping = _PLATFORM_TEMPLATES.get((fmt, platform))
    if mapping is None:
        return result
    for key, filename in mapping.items():
        candidate = templates_dir / filename
        if candidate.exists():
            result[key] = candidate
        else:
            print(f"Note: platform template '{filename}' not found in {templates_dir} — skipping.")
    return result



# ---------------------------------------------------------------------------
# Auto-detection helpers
# ---------------------------------------------------------------------------

    """Walk up from *start* looking for a draft/ subdirectory."""
    current = start
    for _ in range(8):
        candidate = current / "draft"
        if candidate.is_dir():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def read_constitution_meta(draft_dir: Path) -> dict[str, str]:
    """Read author_name, language, copyright, and author bios from constitution.md YAML front-matter."""
    for candidate in (
        draft_dir.parent / ".specify" / "memory" / "constitution.md",
        draft_dir.parent / "constitution.md",
    ):
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8", errors="replace")
            # Extract YAML front-matter block
            fm_match = re.match(r"^---\s*\n(.+?)\n---", text, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                meta: dict[str, str] = {}
                for key, field in (
                    ("author_name", "author"),
                    ("language", "language"),
                    ("copyright", "rights"),
                    ("author_bio_short", "bio_short"),
                    ("author_bio_long", "bio_long"),
                ):
                    m = re.search(rf"^{key}:\s*(.+)$", fm, re.MULTILINE | re.IGNORECASE)
                    if m:
                        value = m.group(1).strip()
                        # Skip placeholder values left from the template
                        if value and not value.startswith("["):
                            meta[field] = value
                return meta
    return {}


def read_spec_meta(draft_dir: Path) -> dict[str, str]:
    """Try to read title and author from spec.md adjacent to draft/."""
    spec_path = draft_dir.parent / "spec.md"
    if not spec_path.exists():
        return {}
    text = spec_path.read_text(encoding="utf-8", errors="replace")
    meta: dict[str, str] = {}
    # Look for a markdown H1 as the title
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        meta["title"] = m.group(1).strip()
    # Look for "Author:" or "author:" in frontmatter or a YAML-style field
    for pattern in (r"(?i)^author:\s*(.+)$", r"(?i)\*\*Author\*\*:\s*(.+)$"):
        m2 = re.search(pattern, text, re.MULTILINE)
        if m2:
            meta["author"] = m2.group(1).strip()
            break
    return meta


def check_pandoc() -> bool:
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


# ---------------------------------------------------------------------------
# Markdown assembly
# ---------------------------------------------------------------------------

def build_combined_markdown(
    chapters: list[tuple[dict[str, str], str]],
    title: str,
    author: str,
    author_bio: str | None = None,
) -> str:
    """Assemble chapters into a single pandoc-compatible markdown document."""
    parts: list[str] = []

    # Pandoc title block (% Title / % Author)
    parts.append(f"% {title}\n% {author}\n\n")

    for meta, body in chapters:
        chapter_name = meta.get("chapter_name", "").strip()
        if chapter_name:
            parts.append(f"# {chapter_name}\n\n")
        parts.append(body.strip())
        parts.append("\n\n")

    if author_bio:
        parts.append("# About the Author\n\n")
        parts.append(author_bio.strip())
        parts.append("\n")

    return "".join(parts)


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def _run_pandoc(args: list[str]) -> None:
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"pandoc error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def export_docx(
    combined_md: str,
    output_path: Path,
    title: str,
    author: str,
    reference_doc: Path | None,
    lang: str = "en",
    rights: str | None = None,
) -> None:
    """Export to DOCX via pandoc.

    Pass --reference-doc to apply custom formatting (recommended for
    Shunn manuscript standard: Times New Roman 12pt, double-spaced,
    1-inch margins, running header).  Without a reference doc pandoc
    uses its built-in defaults.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(combined_md)
        tmp_path = tmp.name

    try:
        cmd = [
            "pandoc", tmp_path,
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "docx",
            "--metadata", f"title={title}",
            "--metadata", f"author={author}",
            "--metadata", f"lang={lang}",
        ]
        if rights:
            cmd += ["--metadata", f"rights={rights}"]
        if reference_doc and reference_doc.exists():
            cmd += ["--reference-doc", str(reference_doc)]
        _run_pandoc(cmd)
    finally:
        os.unlink(tmp_path)


def export_latex(
    combined_md: str,
    output_path: Path,
    title: str,
    author: str,
    latex_template: Path | None = None,
    lang: str = "en",
    rights: str | None = None,
) -> None:
    """Export to LaTeX via pandoc.

    Uses a platform-specific LaTeX template when provided (e.g. KDP 6×9 trim).
    Falls back to pandoc built-in book class with 1-inch margins.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(combined_md)
        tmp_path = tmp.name

    try:
        cmd = [
            "pandoc", tmp_path,
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "latex",
            "--standalone",
            "--metadata", f"title={title}",
            "--metadata", f"author={author}",
            "--metadata", f"lang={lang}",
        ]
        if rights:
            cmd += ["--metadata", f"rights={rights}"]
        if latex_template and latex_template.exists():
            cmd += ["--template", str(latex_template)]
        else:
            # Built-in fallback: generic book layout
            cmd += [
                "-V", "documentclass=book",
                "-V", "geometry=margin=1in",
                "-V", "fontsize=12pt",
                "-V", "linestretch=2",
                "-V", "indent=true",
            ]
        _run_pandoc(cmd)
    finally:
        os.unlink(tmp_path)


def export_epub(
    combined_md: str,
    output_path: Path,
    title: str,
    author: str,
    cover_image: Path | None,
    epub_css: Path | None,
    epub_defaults: Path | None = None,
    isbn: str | None = None,
    lang: str = "en",
    rights: str | None = None,
) -> None:
    """Export to EPUB3 via pandoc.

    Produces a valid EPUB3 file suitable for upload to KDP, Draft2Digital,
    IngramSpark, and other distributors.  Chapter H1 headings become the
    table of contents.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(combined_md)
        tmp_path = tmp.name

    try:
        cmd = [
            "pandoc", tmp_path,
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "epub3",
            "--standalone",
            "--toc",
            "--toc-depth", "1",
            "--metadata", f"title={title}",
            "--metadata", f"author={author}",
            "--metadata", f"lang={lang}",
        ]
        if rights:
            cmd += ["--metadata", f"rights={rights}"]
        if epub_defaults and epub_defaults.exists():
            cmd += ["--defaults", str(epub_defaults)]
        if isbn:
            cmd += ["--metadata", f"isbn={isbn}"]
        if cover_image and cover_image.exists():
            cmd += ["--epub-cover-image", str(cover_image)]
        if epub_css and epub_css.exists():
            cmd += ["--css", str(epub_css)]
        _run_pandoc(cmd)
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export spec-kit writing draft to DOCX or LaTeX.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "format",
        choices=["docx", "latex", "tex", "epub"],
        help="Output format",
    )
    parser.add_argument(
        "--platform",
        default=None,
        metavar="PLATFORM",
        help=(
            "Publishing platform: epub → kdp (default), ingramspark, d2d; "
            "latex → kdp-print-6x9 (default), ingramspark-6x9; "
            "docx → shunn (default), smashwords"
        ),
    )
    parser.add_argument(
        "--draft-dir",
        type=Path,
        default=None,
        metavar="PATH",
        help="Path to draft/ directory (auto-detected from cwd if omitted)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        metavar="FILE",
        help="Output file path (default: manuscript.docx or manuscript.tex)",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Manuscript title (reads from spec.md if omitted)",
    )
    parser.add_argument(
        "--author",
        default=None,
        help="Author name (reads from constitution.md / spec.md if omitted)",
    )
    parser.add_argument(
        "--lang",
        default=None,
        metavar="LANG",
        help="BCP-47 language code for EPUB/DOCX/LaTeX metadata (reads from constitution.md if omitted; default: en)",
    )
    parser.add_argument(
        "--rights",
        default=None,
        metavar="TEXT",
        help="Copyright statement for dc:rights metadata (reads from constitution.md if omitted)",
    )
    parser.add_argument(
        "--author-bio",
        default=None,
        metavar="TEXT",
        help="\"About the Author\" back matter text (reads from constitution.md if omitted)",
    )
    parser.add_argument(
        "--no-author-bio",
        action="store_true",
        help="Suppress \"About the Author\" back matter even if set in constitution.md",
    )
    parser.add_argument(
        "--reference-doc",
        type=Path,
        default=None,
        metavar="FILE",
        help="Pandoc reference .docx file for custom DOCX formatting",
    )
    parser.add_argument(
        "--cover-image",
        type=Path,
        default=None,
        metavar="FILE",
        help="Cover image for EPUB output (jpg or png)",
    )
    parser.add_argument(
        "--isbn",
        default=None,
        metavar="ISBN",
        help="ISBN for EPUB metadata (required for IngramSpark)",
    )
    parser.add_argument(
        "--epub-css",
        type=Path,
        default=None,
        metavar="FILE",
        help="Custom CSS stylesheet for EPUB output (overrides platform default)",
    )
    parser.add_argument(
        "--epub-defaults",
        type=Path,
        default=None,
        metavar="FILE",
        help="Custom pandoc defaults YAML for EPUB (overrides platform default)",
    )
    parser.add_argument(
        "--latex-template",
        type=Path,
        default=None,
        metavar="FILE",
        help="Custom LaTeX template file (overrides platform default)",
    )
    parser.add_argument(
        "--polished-only",
        action="store_true",
        help="Only include chapters that have a polished (_vN) version",
    )
    parser.add_argument(
        "--status",
        default=None,
        metavar="STATUS",
        help='Only include chapters with this status value (e.g. "polished")',
    )
    args = parser.parse_args()

    fmt = "latex" if args.format == "tex" else args.format

    # Resolve platform templates
    templates_dir = find_templates_dir()
    platform_assets = resolve_platform_templates(fmt, args.platform, templates_dir)
    effective_platform = args.platform or _PLATFORM_DEFAULTS.get(fmt, "default")

    # Auto-detect cover image and CSS for EPUB if not specified
    cover_image: Path | None = args.cover_image
    epub_css: Path | None = args.epub_css or platform_assets["epub_css"]
    epub_defaults: Path | None = getattr(args, "epub_defaults", None) or platform_assets["epub_defaults"]
    latex_template: Path | None = getattr(args, "latex_template", None) or platform_assets["latex_template"]
    reference_doc: Path | None = args.reference_doc or platform_assets["reference_doc"]

    # Verify pandoc is available
    if not check_pandoc():
        print(
            "Error: pandoc is required but not found in PATH.\n"
            "Install: https://pandoc.org/installing.html",
            file=sys.stderr,
        )
        sys.exit(1)

    # Resolve draft directory
    draft_dir: Path | None = args.draft_dir
    if draft_dir is None:
        draft_dir = find_draft_dir(Path.cwd())
    if draft_dir is None or not draft_dir.is_dir():
        print(
            "Error: Could not find draft/ directory.\n"
            "Run from the project folder or pass --draft-dir.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Read title / author / language defaults: constitution.md takes priority over spec.md
    constitution_meta = read_constitution_meta(draft_dir)
    spec_meta = read_spec_meta(draft_dir)
    title = args.title or spec_meta.get("title") or "Untitled Manuscript"
    author = args.author or constitution_meta.get("author") or spec_meta.get("author") or "Author Name"
    lang = args.lang or constitution_meta.get("language") or "en"
    rights: str | None = args.rights or constitution_meta.get("rights") or None
    author_bio: str | None = None
    if not getattr(args, "no_author_bio", False):
        author_bio = getattr(args, "author_bio", None) or constitution_meta.get("bio_long") or None

    # Collect chapters
    chapters = collect_chapters(
        draft_dir,
        polished_only=args.polished_only,
        status_filter=args.status,
    )
    if not chapters:
        print(
            f"Error: No chapter files found in {draft_dir}.\n"
            "Check --polished-only / --status filters if set.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Report
    print(f"Title:    {title}")
    print(f"Author:   {author}")
    print(f"Language: {lang}")
    if rights:
        print(f"Rights:   {rights}")
    print(f"Format:   {fmt.upper()}")
    print(f"Platform: {effective_platform}")
    print(f"Source: {draft_dir}")
    print(f"\n{len(chapters)} chapter(s):")
    for meta, body in chapters:
        cid = meta.get("chapter_id", "?")
        name = meta.get("chapter_name", "?")
        status = meta.get("status", "?")
        words = len(body.split())
        print(f"  {cid:12s}  {name:<40s}  [{status}]  ~{words:,} words")

    total_words = sum(len(body.split()) for _, body in chapters)
    print(f"\nTotal: ~{total_words:,} words")

    # Determine output path
    ext = ".docx" if fmt == "docx" else (".epub" if fmt == "epub" else ".tex")
    output: Path = args.output or (draft_dir.parent / f"manuscript{ext}")

    # Auto-detect cover image for EPUB when not explicitly provided
    if fmt == "epub" and cover_image is None:
        for candidate_name in ("cover.jpg", "cover.png", "cover.jpeg"):
            candidate = draft_dir.parent / candidate_name
            if candidate.exists():
                cover_image = candidate
                print(f"Cover image: {cover_image.name} (auto-detected)")
                break

    # Auto-detect EPUB CSS when not explicitly provided
    if fmt == "epub" and epub_css is None:
        for candidate_name in ("epub.css", "style.css", "manuscript.css"):
            candidate = draft_dir.parent / candidate_name
            if candidate.exists():
                epub_css = candidate
                print(f"EPUB CSS:    {epub_css.name} (auto-detected)")
                break

    # Build combined markdown and export
    combined = build_combined_markdown(chapters, title, author, author_bio)
    if author_bio:
        bio_words = len(author_bio.split())
        print(f"Bio:        {bio_words} words (\"About the Author\" appended)")

    print(f"\nExporting to {output.resolve()} ...")
    if fmt == "docx":
        export_docx(combined, output, title, author, reference_doc, lang, rights)
    elif fmt == "epub":
        export_epub(combined, output, title, author, cover_image, epub_css, epub_defaults, getattr(args, "isbn", None), lang, rights)
    else:
        export_latex(combined, output, title, author, latex_template, lang, rights)

    tips = {
        "docx": (
            f"Done.  Output: {output.resolve()}\n"
            f"Platform: {effective_platform}\n"
            "Tip: pass --platform shunn for agent/publisher submission (TNR 12pt, double-spaced)\n"
            "     or --platform smashwords for Smashwords DOCX (minimal styles)."
        ),
        "epub": (
            f"Done.  Output: {output.resolve()}\n"
            f"Platform: {effective_platform}\n"
            "Tips:\n"
            "  Validate:     https://www.epubcheck.org/ (or: epubcheck manuscript.epub)\n"
            "  KDP:          --platform kdp  (default; cover required for KDP)\n"
            "  IngramSpark:  --platform ingramspark  (add --isbn 978-... for ISBN metadata)\n"
            "  D2D:          --platform d2d  (no cover embed; upload cover separately on D2D)\n"
            "  Cover image:  place cover.jpg/cover.png next to draft/ for auto-detection"
        ),
        "latex": (
            f"Done.  Output: {output.resolve()}\n"
            f"Platform: {effective_platform}\n"
            "Tips:\n"
            "  KDP Print 6×9:         --platform kdp-print-6x9 (default)\n"
            "  IngramSpark 6×9:       --platform ingramspark-6x9\n"
            "  Compile:               pdflatex manuscript.tex  (twice for headers)\n"
            "  Unicode/OpenType:      xelatex manuscript.tex\n"
            "  IngramSpark PDF/X-1a:  convert output PDF via Ghostscript or Acrobat Preflight"
        ),
    }
    print(tips[fmt])


if __name__ == "__main__":
    main()
