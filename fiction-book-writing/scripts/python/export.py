#!/usr/bin/env python3
"""export.py — Manuscript exporter for the spec-kit writing preset.

Assembles all drafted chapters from draft/ in chapter_id order and exports to
DOCX (Shunn-style manuscript format), LaTeX (book class, double-spaced),
EPUB3, or audiobook manifest via pandoc.

Automatically prefers the latest polished version (_vN.md) of each chapter
when one exists, falling back to the base draft.

Usage:
    python export.py docx [options]
    python export.py latex [options]    # or: tex
    python export.py epub [options]
    python export.py audio [options]    # audiobook manifest

Options:
    --draft-dir PATH        Path to draft/ directory (auto-detected if omitted)
    --illustrations-dir PATH  Path to illustrations/ directory (auto-detected if omitted)
    --output FILE, -o FILE  Output file (default: manuscript.docx / manuscript.tex / manuscript.epub)
    --title TITLE           Manuscript title (reads from spec.md if omitted)
    --author NAME           Author name (reads from constitution.md/spec.md if omitted)
    --lang LANG             BCP-47 language code for EPUB/DOCX/LaTeX metadata (reads from constitution.md if omitted; default: en)
    --rights TEXT           Copyright statement for dc:rights metadata (reads from constitution.md if omitted)
    --author-bio TEXT       "About the Author" back matter text (reads from constitution.md if omitted)
    --no-author-bio         Suppress "About the Author" back matter even if set in constitution.md
    --cover-image FILE      Cover image for all formats (jpg/png) - auto-detected as cover*.{png,jpg,jpeg}
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


def _ensure_docx_templates(templates_dir: Path) -> None:
    """Generate DOCX templates on-demand if missing."""
    import importlib.util
    
    creator_script = Path(__file__).parent / "create_docx_templates.py"
    if not creator_script.exists():
        return
    
    # Check if templates exist
    shunn = templates_dir / "docx-shunn.docx"
    smashwords = templates_dir / "docx-smashwords.docx"
    
    if not shunn.exists() or not smashwords.exists():
        print("DOCX templates not found — generating them now...")
        spec = importlib.util.spec_from_file_location("create_docx_templates", creator_script)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.main()


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
            # Auto-generate DOCX templates if missing
            if fmt == "docx" and key == "reference_doc":
                _ensure_docx_templates(templates_dir)
                if candidate.exists():
                    result[key] = candidate
                else:
                    print(f"Note: platform template '{filename}' not found in {templates_dir} — skipping.")
            else:
                print(f"Note: platform template '{filename}' not found in {templates_dir} — skipping.")
    return result



# ---------------------------------------------------------------------------
# Auto-detection helpers
# ---------------------------------------------------------------------------

def find_draft_dir(start: Path) -> Path | None:
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
    blurb: str | None = None,
    cover_image: Path | None = None,
    fmt: str = "docx",
    rights: str | None = None,
) -> str:
    """Assemble chapters into a single pandoc-compatible markdown document."""
    parts: list[str] = []

    # Pandoc title block (% Title / % Author)
    parts.append(f"% {title}\n% {author}\n\n")

    # Add cover image if provided (for DOCX and EPUB; LaTeX uses title page)
    if cover_image and cover_image.exists() and fmt != "latex":
        parts.append(f"![]({cover_image.name})\n\n")

    # Add copyright page if provided (for DOCX and EPUB)
    if rights and fmt != "latex":
        parts.append(f"\n\n# Copyright\n\n\n\n{rights}\n\n\n\n")

    # Add blurb as description if provided (EPUB metadata)
    if blurb:
        parts.append(f"\n\n# Description\n\n{blurb}\n\n")

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
# Illustration processing
# ---------------------------------------------------------------------------

def read_illustration_config(draft_dir: Path) -> dict[str, str]:
    """Read illustration settings from constitution.md."""
    for candidate in (
        draft_dir.parent / ".." / ".." / ".specify" / "memory" / "constitution.md",
        draft_dir.parent / "constitution.md",
    ):
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8", errors="replace")
            meta: dict[str, str] = {}
            # Check both YAML format (key:) and markdown format (**Key**:)
            # Note: "illustrations_enabled" maps to "**Illustrations**:" in the template
            for key, label in (
                ("illustrations_enabled", "Illustrations"),
                ("illustration_automation", "Illustration Automation"),
                ("default_style", "Default Style"),
                ("default_color_range", "Default Color Range"),
                ("default_aspect_ratio", "Default Aspect Ratio"),
            ):
                # Try YAML format first
                m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
                if m:
                    meta[key] = m.group(1).strip()
                else:
                    # Try markdown format: **Key**: value
                    m = re.search(rf"\*\*{label}\*\*:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
                    if m:
                        meta[key] = m.group(1).strip()
            return meta
    return {}


def find_illustration_file(illustrations_dir: Path, chapter_id: str) -> Path | None:
    """Find illustration file for a chapter, checking multiple extensions."""
    for ext in (".png", ".jpg", ".jpeg"):
        ill_file = illustrations_dir / f"{chapter_id}{ext}"
        if ill_file.exists():
            return ill_file
    return None


def process_illustrations(
    chapters: list[tuple[dict[str, str], str]],
    draft_dir: Path,
    fmt: str,
) -> list[tuple[dict[str, str], str]]:
    """Process illustrations and insert image references at chapter boundaries."""
    config = read_illustration_config(draft_dir)
    enabled = config.get("illustrations_enabled", "no")
    automation = config.get("illustration_automation", "manual")
    illustrations_dir = draft_dir.parent / "illustrations"

    if enabled != "yes":
        return chapters

    if automation == "per-chapter" and illustrations_dir.is_dir():
        # Per-chapter mode: look for <CHAPTER_ID>.* files (png/jpg/jpeg)
        for i, (meta, body) in enumerate(chapters):
            chapter_id = meta.get("chapter_id", "")
            ill_file = find_illustration_file(illustrations_dir, chapter_id)
            if ill_file is not None:
                # Insert image reference after chapter heading
                if fmt == "epub":
                    img_tag = f'<img src="{ill_file.name}" width="100%" alt="Chapter illustration"/>\n\n'
                elif fmt == "docx":
                    img_tag = f"![]({ill_file.name})\n\n"
                else:  # latex
                    img_tag = f"\\begin{{center}}\n\\includegraphics[width=0.8\\textwidth]{{{ill_file.name}}}\n\\end{{center}}\n\n"
                # Insert after first heading or at start
                if body.strip().startswith("#"):
                    # Find end of first line
                    nl = body.find("\n")
                    if nl != -1:
                        body = body[:nl+1] + "\n" + img_tag + body[nl+1:]
                    else:
                        body = body + "\n" + img_tag
                else:
                    body = img_tag + body
                chapters[i] = (meta, body)
    else:
        # Manual mode: look for <!-- illustration: filename.* --> comments
        found_illustration = False
        for i, (meta, body) in enumerate(chapters):
            # Replace illustration comments with format-appropriate syntax (supports png, jpg, jpeg)
            if fmt == "epub":
                new_body = re.sub(
                    r"<!--\s*illustration:\s*(\S+\.(png|jpg|jpeg))\s*-->",
                    r'<img src="\1" width="100%" alt="Illustration"/>',
                    body,
                )
            elif fmt == "docx":
                new_body = re.sub(
                    r"<!--\s*illustration:\s*(\S+\.(png|jpg|jpeg))\s*-->",
                    r"![](\1)",
                    body,
                )
            else:  # latex
                new_body = re.sub(
                    r"<!--\s*illustration:\s*(\S+\.(png|jpg|jpeg))\s*-->",
                    r"\\begin{center}\\includegraphics[width=0.8\\textwidth]{\1}\\end{center}",
                    body,
                )
            if "illustration:" in body:
                found_illustration = True
            chapters[i] = (meta, new_body)

        if not found_illustration:
            print("[WARN] No illustration references found in draft files. Add `<!-- illustration: <filename>.png -->` comments where images should appear.", file=sys.stderr)

    return chapters


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def _run_pandoc(args: list[str]) -> None:
    print(f"Running pandoc command: {' '.join(args)}")
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"pandoc error:\n{result.stderr}", file=sys.stderr)
        print(f"pandoc stdout:\n{result.stdout}", file=sys.stderr)
        print(f"Command failed with return code: {result.returncode}", file=sys.stderr)
        sys.exit(1)
    else:
        print("pandoc command succeeded")


def find_cover_image(project_dir: Path) -> Path | None:
    """Find cover image file in project root (cover*.png/jpg/jpeg)."""
    for pattern in ("cover*.png", "cover*.jpg", "cover*.jpeg"):
        matches = list(project_dir.glob(pattern))
        if matches:
            return matches[0]
    return None


def export_docx(
    combined_md: str,
    output_path: Path,
    title: str,
    author: str,
    reference_doc: Path | None,
    cover_image: Path | None,
    illustrations_dir: Path | None,
    lang: str = "en",
    rights: str | None = None,
) -> None:
    """Export to DOCX via pandoc.

    Pass --reference-doc to apply custom formatting (recommended for
    Shunn manuscript standard: Times New Roman 12pt, double-spaced,
    1-inch margins, running header).  Without a reference doc pandoc
    uses its built-in defaults.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "combined.md"
        tmp_path.write_text(combined_md, encoding="utf-8")

        # Copy cover image to temp dir if found
        if cover_image and cover_image.exists():
            cover_dest = Path(tmpdir) / cover_image.name
            cover_dest.write_bytes(cover_image.read_bytes())
            print(f"Copied cover image: {cover_image.name} to {cover_dest}")

        # Copy illustrations to temp dir if found
        if illustrations_dir and illustrations_dir.is_dir():
            print(f"Found illustrations directory: {illustrations_dir}")
            for img_file in illustrations_dir.glob("*.png"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())
                print(f"Copied PNG illustration: {img_file.name}")
            for img_file in illustrations_dir.glob("*.jpg"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())
                print(f"Copied JPG illustration: {img_file.name}")
            for img_file in illustrations_dir.glob("*.jpeg"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())
                print(f"Copied JPEG illustration: {img_file.name}")
        else:
            print(f"No illustrations directory found: {illustrations_dir}")

        # Use absolute paths for pandoc
        cmd = [
            "pandoc", str(tmp_path),
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "docx",
            "--metadata", f"title={title}",
            "--metadata", f"author={author}",
            "--metadata", f"lang={lang}",
            "--embed-resources",
            "--resource-path", str(tmpdir),
            "--link-images",
        ]
        if rights:
            cmd += ["--metadata", f"rights={rights}"]
        if reference_doc and reference_doc.exists():
            cmd += ["--reference-doc", str(reference_doc)]
        _run_pandoc(cmd)


def export_latex(
    combined_md: str,
    output_path: Path,
    title: str,
    author: str,
    latex_template: Path | None,
    cover_image: Path | None,
    illustrations_dir: Path | None,
    lang: str = "en",
    rights: str | None = None,
) -> None:
    """Export to LaTeX via pandoc.

    Uses a platform-specific LaTeX template when provided (e.g. KDP 6×9 trim).
    Falls back to pandoc built-in book class with 1-inch margins.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "combined.md"
        tmp_path.write_text(combined_md, encoding="utf-8")

        # Copy cover image to temp dir if found
        if cover_image and cover_image.exists():
            cover_dest = Path(tmpdir) / cover_image.name
            cover_dest.write_bytes(cover_image.read_bytes())

        # Copy illustrations to temp dir if found
        if illustrations_dir and illustrations_dir.is_dir():
            for img_file in illustrations_dir.glob("*.png"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())
            for img_file in illustrations_dir.glob("*.jpg"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())
            for img_file in illustrations_dir.glob("*.jpeg"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())

        cmd = [
            "pandoc", str(tmp_path),
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "latex",
            "--standalone",
            "--top-level-division=chapter",
            "--metadata", f"title={title}",
            "--metadata", f"author={author}",
            "--metadata", f"lang={lang}",
        ]
        if cover_image and cover_image.exists():
            cmd += ["--metadata", f"cover-image={cover_image.name}"]
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


def export_epub(
    combined_md: str,
    output_path: Path,
    title: str,
    author: str,
    cover_image: Path | None,
    epub_css: Path | None,
    epub_defaults: Path | None,
    illustrations_dir: Path | None,
    isbn: str | None = None,
    lang: str = "en",
    rights: str | None = None,
    blurb: str | None = None,
) -> None:
    """Export to EPUB3 via pandoc.

    Produces a valid EPUB3 file suitable for upload to KDP, Draft2Digital,
    IngramSpark, and other distributors.  Chapter H1 headings become the
    table of contents.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "combined.md"
        tmp_path.write_text(combined_md, encoding="utf-8")

        # Copy cover image to temp dir if found
        if cover_image and cover_image.exists():
            cover_dest = Path(tmpdir) / cover_image.name
            cover_dest.write_bytes(cover_image.read_bytes())

        # Copy illustrations to temp dir if found
        if illustrations_dir and illustrations_dir.is_dir():
            for img_file in illustrations_dir.glob("*.png"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())
            for img_file in illustrations_dir.glob("*.jpg"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())
            for img_file in illustrations_dir.glob("*.jpeg"):
                img_dest = Path(tmpdir) / img_file.name
                img_dest.write_bytes(img_file.read_bytes())

        cmd = [
            "pandoc", str(tmp_path),
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "epub3",
            "--standalone",
            "--toc",
            "--toc-depth", "1",
            "--metadata", f"title={title}",
            "--metadata", f"author={author}",
            "--metadata", f"lang={lang}",
            "--embed-resources",
            "--resource-path", str(tmpdir),            
        ]
        if rights:
            cmd += ["--metadata", f"rights={rights}"]
        if epub_defaults and epub_defaults.exists():
            cmd += ["--defaults", str(epub_defaults)]
        if isbn:
            cmd += ["--metadata", f"isbn={isbn}"]
        if cover_image and cover_image.exists():
            cmd += ["--epub-cover-image", str(cover_dest)]
        if epub_css and epub_css.exists():
            cmd += ["--css", str(epub_css)]
        # Add description from blurb if present
        if blurb:
            cmd += ["--metadata", f"description={blurb}"]
        _run_pandoc(cmd)


def read_audiobook_config(draft_dir: Path) -> dict[str, str]:
    """Read audiobook settings from constitution.md § X."""
    for candidate in (
        draft_dir.parent / ".specify" / "memory" / "constitution.md",
        draft_dir.parent / "constitution.md",
    ):
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8", errors="replace")
            meta: dict[str, str] = {}
            for key in ("TTS_ENGINE", "SPEAKER_MODE"):
                m = re.search(rf"^\*\*{key}\*\*:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
                if m:
                    meta[key.lower()] = m.group(1).strip()
            return meta
    return {}


def export_audio(draft_dir: Path, output_path: Path) -> None:
    """Generate audiobook chapter manifest from audiodraft/ directory."""
    audiodraft_dir = draft_dir.parent / "audiodraft"
    if not audiodraft_dir.is_dir():
        print(
            f"[WARN] No audiobook drafts found in {audiodraft_dir}\n"
            "Run speckit.implement with Output Mode set to `audiobook` or `both`\n"
            "in constitution.md ## X to generate audiobook draft files first.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Collect audiobook files
    ssml_files = sorted(audiodraft_dir.glob("*.ssml"))
    el_files = sorted(audiodraft_dir.glob("*_el.xml"))

    if not ssml_files and not el_files:
        print(
            f"[WARN] No audiobook drafts found in {audiodraft_dir}\n"
            "Run speckit.implement with Output Mode set to `audiobook` or `both`\n"
            "in constitution.md ## X to generate audiobook draft files first.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Read audiobook configuration
    audiobook_config = read_audiobook_config(draft_dir)
    speaker_mode = audiobook_config.get("speaker_mode", "single")

    # Collect prose draft chapters for comparison
    prose_chapters = collect_chapters(draft_dir, polished_only=False, status_filter=None)
    prose_chapter_ids = {meta.get("chapter_id", "") for meta, _ in prose_chapters}
    audio_chapter_ids = set()

    # Build manifest
    manifest_lines = [
        f"# Audiobook Chapter Manifest: {draft_dir.parent.name}",
        "",
        "| # | Chapter ID | Chapter Name | SSML File | EL File | Segments | Status |",
        "|---|---|---|---|---|---|---|",
    ]

    for i, ssml_file in enumerate(ssml_files, 1):
        # Read frontmatter for chapter info
        text = ssml_file.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        chapter_id = meta.get("chapter_id", ssml_file.stem)
        audio_chapter_ids.add(chapter_id)
        chapter_name = meta.get("chapter_name", "")
        el_file = ssml_file.parent / f"{ssml_file.stem}_el.xml"
        el_name = el_file.name if el_file.exists() else "-"
        # Count segments (voice blocks) in SSML
        segments = str(len(re.findall(r"<voice", text)))
        manifest_lines.append(
            f"| {i} | {chapter_id} | {chapter_name} | {ssml_file.name} | {el_name} | {segments} | audiodraft |"
        )

    manifest_path = draft_dir.parent / "audiodraft" / "manifest.md"
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # Check for missing audiobook drafts
    missing_drafts = prose_chapter_ids - audio_chapter_ids
    lexicon_path = audiodraft_dir / "lexicon.pls"
    lexicon_exists = lexicon_path.exists()

    # Validate lexicon XML if present
    if lexicon_exists:
        try:
            lexicon_text = lexicon_path.read_text(encoding="utf-8")
            # Basic XML well-formedness check
            if not (lexicon_text.strip().startswith("<?xml") or lexicon_text.strip().startswith("<lexicon")):
                print("[WARN] lexicon.pls may not be valid XML — check format", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] Could not read lexicon.pls: {e}", file=sys.stderr)

    # Report table
    print("[OK] Audiobook export complete\n")
    print("| Field          | Value                                   |")
    print("|---|---|")
    print(f"| Chapters       | {len(ssml_files)}                                   |")
    print(f"| SSML files     | audiodraft/*.ssml                       |")
    print(f"| EL files       | audiodraft/*_el.xml                     |")
    print(f"| Lexicon        | audiodraft/lexicon.pls                  |" if lexicon_exists else "| Lexicon        | (none)                                    |")
    print(f"| Manifest       | audiodraft/manifest.md                  |")
    print(f"| Speaker mode   | {speaker_mode}                          |")
    if missing_drafts:
        print(f"| Missing drafts | {len(missing_drafts)} chapters have no audiobook draft yet  |")
    else:
        print("| Missing drafts | 0                                       |")

    # Distribution guidance
    print("\n> **SSML-cloud (Azure / Google / Amazon Polly)**:")
    print("> - Pass each `.ssml` file's content to your TTS API. One API call per chapter.")
    print("> - Azure TTS: `POST /cognitiveservices/v1` with `Content-Type: application/ssml+xml`")
    print("> - Amazon Polly: `SynthesizeSpeech` with `TextType: ssml`")
    print("> - Google Cloud TTS: `synthesize` with `input.ssml`")
    print("> - Output format: MP3 192kbps, mono or stereo — required by ACX")
    print()
    print("> **ElevenLabs**:")
    print("> - Upload `audiodraft/lexicon.pls` to your ElevenLabs project's pronunciation dictionary first")
    print("> - For each `_el.xml` file: split on `<!-- VOICE: ... -->` segment boundaries and POST each segment to `/v1/text-to-speech/{voice_id}` with `model_id: eleven_multilingual_v2`")
    print("> - Stitch segments in order to produce the chapter MP3")
    print()
    print("> **ACX submission (Audible)**:")
    print("> - Required: MP3 192kbps, -23 LUFS integrated loudness, -3 dBFS peak, room tone under -60 dBFS")
    print("> - One MP3 per chapter + one retail audio sample (first 5 minutes or opening chapter)")
    print("> - Tools: normalize with Auphonic (automatic) or Audacity (manual) before submission")


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
        choices=["docx", "latex", "tex", "epub", "audio"],
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
        "--illustrations-dir",
        type=Path,
        default=None,
        metavar="PATH",
        help="Directory containing illustration images (default: illustrations/ next to draft/)",
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
    if fmt == "audio":
        output: Path = args.output or (draft_dir.parent / "audiodraft")
    else:
        ext = ".docx" if fmt == "docx" else (".epub" if fmt == "epub" else ".tex")
        output: Path = args.output or (draft_dir.parent / f"manuscript{ext}")

    # Auto-detect cover image for all formats when not explicitly provided
    if cover_image is None:
        cover_image = find_cover_image(draft_dir.parent)
        if cover_image:
            print(f"Cover image: {cover_image.name} (auto-detected)")

    # Auto-detect illustrations directory (use --illustrations-dir if provided)
    illustrations_dir = args.illustrations_dir
    if illustrations_dir is None:
        illustrations_dir = draft_dir.parent / "illustrations"
    if illustrations_dir is None or not illustrations_dir.is_dir():
        illustrations_dir = None

    # Auto-detect EPUB CSS when not explicitly provided
    if fmt == "epub" and epub_css is None:
        for candidate_name in ("epub.css", "style.css", "manuscript.css"):
            candidate = draft_dir.parent / candidate_name
            if candidate.exists():
                epub_css = candidate
                print(f"EPUB CSS:    {epub_css.name} (auto-detected)")
                break

    # Read or generate blurb for EPUB
    blurb: str | None = None
    if fmt == "epub":
        blurb_path = draft_dir.parent / "blurb.md"
        if blurb_path.exists():
            blurb_text = blurb_path.read_text(encoding="utf-8").strip()
            # Extract first non-comment paragraph
            for line in blurb_text.splitlines():
                if line and not line.startswith("<!--"):
                    blurb = line
                    break
            # Validate word count
            if blurb:
                blurb_words = len(blurb.split())
                if blurb_words < 100 or blurb_words > 150:
                    print(f"[WARN] blurb.md has {blurb_words} words (recommended: 100-150)", file=sys.stderr)
        else:
            # Generate blurb from spec.md
            spec_path = draft_dir.parent / "spec.md"
            if spec_path.exists():
                spec_text = spec_path.read_text(encoding="utf-8")
                # Look for logline or dramatic question
                logline_match = re.search(r"(?i)^#+\s*Logline\s*\n(.+?)(?=\n#|\Z)", spec_text, re.MULTILINE | re.DOTALL)
                dramatic_match = re.search(r"(?i)^\*\*Dramatic Question\*\*:\s*(.+?)(?=\n\*\*|\n##|\Z)", spec_text, re.MULTILINE | re.DOTALL)
                if logline_match:
                    blurb = logline_match.group(1).strip()
                elif dramatic_match:
                    blurb = dramatic_match.group(1).strip()
                else:
                    blurb = f"A story about {title}."
                # Write generated blurb
                blurb_content = f"# Back-Cover Blurb: {title}\n\n<!-- 100–150 words. Edit here and re-run speckit.export epub to update the EPUB metadata. -->\n\n{blurb}\n"
                blurb_path.write_text(blurb_content, encoding="utf-8")
                print(f"[OK] blurb.md generated — review and edit before final distribution.")
                blurb_words = len(blurb.split())
                if blurb_words < 100 or blurb_words > 150:
                    print(f"[WARN] Generated blurb has {blurb_words} words (recommended: 100-150)", file=sys.stderr)

    # Process illustrations for EPUB/DOCX/LaTeX
    if fmt in ("epub", "docx", "latex"):
        chapters = process_illustrations(chapters, draft_dir, fmt)

    # Build combined markdown and export
    combined = build_combined_markdown(chapters, title, author, author_bio, blurb, cover_image, fmt=fmt, rights=rights)
    if author_bio:
        bio_words = len(author_bio.split())
        print(f"Bio:        {bio_words} words (\"About the Author\" appended)")

    # ISBN warning for IngramSpark
    if fmt == "epub" and effective_platform == "ingramspark" and not getattr(args, "isbn", None):
        print("[WARN] --isbn not set — IngramSpark requires an ISBN in EPUB metadata. Add --isbn 978-... to the command.")

    print(f"\nExporting to {output.resolve()} ...")
    if fmt == "docx":
        export_docx(combined, output, title, author, reference_doc, cover_image, illustrations_dir, lang, rights)
    elif fmt == "epub":
        export_epub(combined, output, title, author, cover_image, epub_css, epub_defaults, illustrations_dir, getattr(args, "isbn", None), lang, rights, blurb)
    elif fmt == "audio":
        export_audio(draft_dir, output)
    else:
        export_latex(combined, output, title, author, latex_template, cover_image, illustrations_dir, lang, rights)

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
        "audio": (
            f"Done.  Output: {output.resolve()}\n"
            "Audiobook manifest generated at audiodraft/manifest.md\n"
            "Tips:\n"
            "  SSML files:  Use with Azure TTS, Google Cloud TTS, or Amazon Polly\n"
            "  EL files:    Use with ElevenLabs API (POST /v1/text-to-speech/{voice_id})\n"
            "  Lexicon:     Upload audiodraft/lexicon.pls to your TTS platform first"
        ),
    }
    print(tips.get(fmt, tips.get("docx")))


if __name__ == "__main__":
    main()
