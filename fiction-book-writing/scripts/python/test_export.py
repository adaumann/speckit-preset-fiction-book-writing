#!/usr/bin/env python3
"""Unit tests for export.py — manuscript exporter for the spec-kit writing preset."""

import tempfile
import unittest
from pathlib import Path
import sys

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent))
import export


class TestParseFrontmatter(unittest.TestCase):
    """Tests for parse_frontmatter function."""

    def test_no_frontmatter(self):
        """Text without frontmatter returns empty dict and original text."""
        text = "Just some content\nwithout frontmatter"
        meta, body = export.parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, text)

    def test_simple_frontmatter(self):
        """Simple key: value frontmatter is parsed correctly."""
        text = "---\nchapter_id: A1.101\nchapter_name: Awakening\n---\n\nBody content here"
        meta, body = export.parse_frontmatter(text)
        self.assertEqual(meta, {"chapter_id": "A1.101", "chapter_name": "Awakening"})
        self.assertEqual(body, "Body content here")

    def test_frontmatter_with_quotes(self):
        """Quoted values are stripped correctly."""
        text = '---\ntitle: "My Story"\nauthor: \'John Doe\'\n---\n\nContent'
        meta, body = export.parse_frontmatter(text)
        self.assertEqual(meta, {"title": "My Story", "author": "John Doe"})

    def test_frontmatter_with_inline_comments(self):
        """Inline YAML comments are removed from values."""
        text = "---\nchapter_id: A1.101 # chapter id\n---\n\nContent"
        meta, body = export.parse_frontmatter(text)
        self.assertEqual(meta, {"chapter_id": "A1.101"})

    def test_frontmatter_with_missing_end(self):
        """Frontmatter without closing --- returns empty dict and original text."""
        text = "---\nchapter_id: A1.101\n\nNo closing"
        meta, body = export.parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, text)


class TestStripDraftNotes(unittest.TestCase):
    """Tests for strip_draft_notes function."""

    def test_no_draft_notes(self):
        """Text without draft notes is unchanged."""
        text = "This is regular content.\nNo notes here."
        result = export.strip_draft_notes(text)
        self.assertEqual(result, text)

    def test_single_draft_note(self):
        """Single draft note block is removed."""
        text = "Content<!-- DRAFT NOTES: some notes -->more content"
        result = export.strip_draft_notes(text)
        self.assertEqual(result, "Contentmore content")

    def test_multiline_draft_note(self):
        """Multiline draft note block is removed."""
        text = "Content<!-- DRAFT NOTES:\nline 1\nline 2\n-->more content"
        result = export.strip_draft_notes(text)
        self.assertEqual(result, "Contentmore content")

    def test_multiple_draft_notes(self):
        """Multiple draft note blocks are all removed."""
        text = "A<!-- DRAFT NOTES: note1 -->B<!-- DRAFT NOTES: note2 -->C"
        result = export.strip_draft_notes(text)
        self.assertEqual(result, "ABC")


class TestChapterSortKey(unittest.TestCase):
    """Tests for _chapter_sort_key function."""

    def test_standard_chapter_id(self):
        """Standard chapter ID formats sort correctly."""
        item = ({"chapter_id": "A1.101"}, "body")
        key = export._chapter_sort_key(item)
        self.assertEqual(key, ("A", 1, 101))

    def test_chapter_id_with_prefix(self):
        """Chapter IDs with letter prefixes sort correctly."""
        item = ({"chapter_id": "B2.201"}, "body")
        key = export._chapter_sort_key(item)
        self.assertEqual(key, ("B", 2, 201))

    def test_invalid_chapter_id(self):
        """Invalid chapter IDs fall back to lexicographic sort."""
        item = ({"chapter_id": "intro"}, "body")
        key = export._chapter_sort_key(item)
        self.assertEqual(key, ("intro", 0, 0))

    def test_missing_chapter_id(self):
        """Missing chapter_id falls back to lexicographic sort."""
        item = ({}, "body")
        key = export._chapter_sort_key(item)
        self.assertEqual(key, ("", 0, 0))


class TestCollectChapters(unittest.TestCase):
    """Tests for collect_chapters function."""

    def test_collect_chapters_basic(self):
        """Chapters are collected and sorted by chapter_id."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            
            # Create test chapter files
            (draft_dir / "A1.101_Intro.md").write_text("---\nchapter_id: A1.101\nchapter_name: Intro\n---\nContent 1")
            (draft_dir / "A1.201_Next.md").write_text("---\nchapter_id: A1.201\nchapter_name: Next\n---\nContent 2")
            
            chapters = export.collect_chapters(draft_dir)
            self.assertEqual(len(chapters), 2)
            self.assertEqual(chapters[0][0]["chapter_id"], "A1.101")
            self.assertEqual(chapters[1][0]["chapter_id"], "A1.201")

    def test_collect_chapters_polished_only(self):
        """Polished-only flag filters to _vN files only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            
            # Create base and polished versions
            (draft_dir / "A1.101_Intro.md").write_text("---\nchapter_id: A1.101\n---\nBase content")
            (draft_dir / "A1.101_Intro_v1.md").write_text("---\nchapter_id: A1.101\n---\nPolished content")
            
            # Without polished_only - gets polished version
            chapters = export.collect_chapters(draft_dir, polished_only=False)
            self.assertEqual(len(chapters), 1)
            self.assertIn("Polished", chapters[0][1])

    def test_collect_chapters_status_filter(self):
        """Status filter includes only matching chapters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            
            (draft_dir / "A1.101_Intro.md").write_text("---\nchapter_id: A1.101\nstatus: polished\n---\nContent")
            (draft_dir / "A1.201_Next.md").write_text("---\nchapter_id: A1.201\nstatus: draft\n---\nContent")
            
            chapters = export.collect_chapters(draft_dir, status_filter="polished")
            self.assertEqual(len(chapters), 1)
            self.assertEqual(chapters[0][0]["chapter_id"], "A1.101")


class TestReadConstitutionMeta(unittest.TestCase):
    """Tests for read_constitution_meta function."""

    def test_read_author_name(self):
        """Author name is read from constitution.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("---\nauthor_name: Jane Doe\nlanguage: en\ncopyright: Copyright 2025 Jane Doe\n---\nContent")
            
            meta = export.read_constitution_meta(draft_dir)
            self.assertEqual(meta.get("author"), "Jane Doe")
            self.assertEqual(meta.get("language"), "en")
            self.assertEqual(meta.get("rights"), "Copyright 2025 Jane Doe")

    def test_skip_placeholder_values(self):
        """Placeholder values in brackets are skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("---\nauthor_name: [Your Name Here]\nlanguage: en\n---\nContent")
            
            meta = export.read_constitution_meta(draft_dir)
            self.assertNotIn("author", meta)


class TestReadSpecMeta(unittest.TestCase):
    """Tests for read_spec_meta function."""

    def test_read_title_from_h1(self):
        """Title is read from H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            spec_path = draft_dir.parent / "spec.md"
            spec_path.write_text("# My Great Story\n\nSome content")
            
            meta = export.read_spec_meta(draft_dir)
            self.assertEqual(meta.get("title"), "My Great Story")

    def test_read_author_from_frontmatter(self):
        """Author is read from YAML frontmatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            spec_path = draft_dir.parent / "spec.md"
            spec_path.write_text("---\nauthor: John Smith\n---\n# Title")
            
            meta = export.read_spec_meta(draft_dir)
            self.assertEqual(meta.get("author"), "John Smith")

    def test_read_author_from_bold_format(self):
        """Author is read from **Author**: format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            spec_path = draft_dir.parent / "spec.md"
            spec_path.write_text("# Title\n\n**Author**: Jane Doe")
            
            meta = export.read_spec_meta(draft_dir)
            self.assertEqual(meta.get("author"), "Jane Doe")


class TestReadIllustrationConfig(unittest.TestCase):
    """Tests for read_illustration_config function."""

    def test_read_illustration_settings_yaml(self):
        """Illustration settings are read from YAML format in constitution.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("illustrations_enabled: yes\nillustration_automation: per-chapter\ndefault_style: penandink\n")
            
            config = export.read_illustration_config(draft_dir)
            self.assertEqual(config.get("illustrations_enabled"), "yes")
            self.assertEqual(config.get("illustration_automation"), "per-chapter")
            self.assertEqual(config.get("default_style"), "penandink")

    def test_read_illustration_settings_markdown(self):
        """Illustration settings are read from markdown format in constitution.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("**Illustrations**: yes\n**Illustration Automation**: per-chapter\n**Default Style**: penandink\n")
            
            config = export.read_illustration_config(draft_dir)
            self.assertEqual(config.get("illustrations_enabled"), "yes")
            self.assertEqual(config.get("illustration_automation"), "per-chapter")
            self.assertEqual(config.get("default_style"), "penandink")


class TestReadAudiobookConfig(unittest.TestCase):
    """Tests for read_audiobook_config function."""

    def test_read_tts_engine(self):
        """TTS_ENGINE is read from constitution.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("**TTS_ENGINE**: azure\n**SPEAKER_MODE**: single\n")
            
            config = export.read_audiobook_config(draft_dir)
            self.assertEqual(config.get("tts_engine"), "azure")
            self.assertEqual(config.get("speaker_mode"), "single")


class TestProcessIllustrations(unittest.TestCase):
    """Tests for process_illustrations function."""

    def test_per_chapter_mode_png(self):
        """Per-chapter mode embeds PNG images at chapter boundaries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            illustrations_dir = draft_dir.parent / "illustrations"
            illustrations_dir.mkdir()
            
            # Create a dummy PNG file
            (illustrations_dir / "A1.101.png").write_bytes(b"fake png")
            
            chapters = [
                ({"chapter_id": "A1.101", "chapter_name": "Intro"}, "# Intro\n\nContent here"),
            ]
            
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("illustrations_enabled: yes\nillustration_automation: per-chapter\n")
            
            result = export.process_illustrations(chapters, draft_dir, "epub")
            self.assertIn("<img src=", result[0][1])

    def test_per_chapter_mode_jpg(self):
        """Per-chapter mode embeds JPG images at chapter boundaries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            illustrations_dir = draft_dir.parent / "illustrations"
            illustrations_dir.mkdir()
            
            # Create a dummy JPG file
            (illustrations_dir / "A1.101.jpg").write_bytes(b"fake jpg")
            
            chapters = [
                ({"chapter_id": "A1.101", "chapter_name": "Intro"}, "# Intro\n\nContent here"),
            ]
            
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("illustrations_enabled: yes\nillustration_automation: per-chapter\n")
            
            result = export.process_illustrations(chapters, draft_dir, "docx")
            self.assertIn("![](A1.101.jpg)", result[0][1])

    def test_manual_mode_with_comments(self):
        """Manual mode processes illustration comments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            
            chapters = [
                ({"chapter_id": "A1.101"}, "Text<!-- illustration: image.png -->more text"),
            ]
            
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("illustrations_enabled: yes\nillustration_automation: manual\n")
            
            result = export.process_illustrations(chapters, draft_dir, "docx")
            self.assertIn("![](image.png)", result[0][1])

    def test_manual_mode_jpg_comments(self):
        """Manual mode processes JPG illustration comments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            
            chapters = [
                ({"chapter_id": "A1.101"}, "Text<!-- illustration: image.jpg -->more text"),
            ]
            
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("illustrations_enabled: yes\nillustration_automation: manual\n")
            
            result = export.process_illustrations(chapters, draft_dir, "latex")
            self.assertIn("includegraphics", result[0][1])

    def test_manual_mode_no_comments(self):
        """Manual mode warns when no illustration comments found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            
            chapters = [
                ({"chapter_id": "A1.101"}, "Just text, no illustrations"),
            ]
            
            const_path = draft_dir.parent / "constitution.md"
            const_path.write_text("illustrations_enabled: yes\nillustration_automation: manual\n")
            
            # Capture stderr
            import io
            old_stderr = sys.stderr
            sys.stderr = io.StringIO()
            
            try:
                result = export.process_illustrations(chapters, draft_dir, "epub")
                stderr_output = sys.stderr.getvalue()
                self.assertIn("No illustration references found", stderr_output)
            finally:
                sys.stderr = old_stderr


class TestFindCoverImage(unittest.TestCase):
    """Tests for find_cover_image function."""

    def test_find_cover_png(self):
        """Cover PNG is found with cover*.png pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / "cover.png").write_bytes(b"fake png")
            
            result = export.find_cover_image(project_dir)
            self.assertEqual(result.name, "cover.png")

    def test_find_cover_jpg(self):
        """Cover JPG is found with cover*.jpg pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / "cover.jpg").write_bytes(b"fake jpg")
            
            result = export.find_cover_image(project_dir)
            self.assertEqual(result.name, "cover.jpg")

    def test_find_cover_jpeg(self):
        """Cover JPEG is found with cover*.jpeg pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / "cover.jpeg").write_bytes(b"fake jpeg")
            
            result = export.find_cover_image(project_dir)
            self.assertEqual(result.name, "cover.jpeg")

    def test_no_cover_returns_none(self):
        """Returns None when no cover image found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            result = export.find_cover_image(project_dir)
            self.assertIsNone(result)


class TestFindIllustrationFile(unittest.TestCase):
    """Tests for find_illustration_file function."""

    def test_find_png(self):
        """PNG illustration is found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ill_dir = Path(tmpdir)
            (ill_dir / "A1.101.png").write_bytes(b"fake png")
            
            result = export.find_illustration_file(ill_dir, "A1.101")
            self.assertEqual(result.name, "A1.101.png")

    def test_find_jpg(self):
        """JPG illustration is found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ill_dir = Path(tmpdir)
            (ill_dir / "A1.101.jpg").write_bytes(b"fake jpg")
            
            result = export.find_illustration_file(ill_dir, "A1.101")
            self.assertEqual(result.name, "A1.101.jpg")

    def test_find_jpeg(self):
        """JPEG illustration is found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ill_dir = Path(tmpdir)
            (ill_dir / "A1.101.jpeg").write_bytes(b"fake jpeg")
            
            result = export.find_illustration_file(ill_dir, "A1.101")
            self.assertEqual(result.name, "A1.101.jpeg")

    def test_no_illustration_returns_none(self):
        """Returns None when no illustration file found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ill_dir = Path(tmpdir)
            result = export.find_illustration_file(ill_dir, "A1.101")
            self.assertIsNone(result)


class TestBuildCombinedMarkdown(unittest.TestCase):
    """Tests for build_combined_markdown function."""

    def test_basic_assembly(self):
        """Chapters are assembled with title and author."""
        chapters = [
            ({"chapter_id": "A1.101", "chapter_name": "Intro"}, "Content 1"),
        ]
        
        result = export.build_combined_markdown(chapters, "Test Title", "Test Author")
        self.assertIn("% Test Title", result)
        self.assertIn("% Test Author", result)
        self.assertIn("# Intro", result)

    def test_blurb_included(self):
        """Blurb is included as description section."""
        chapters = [
            ({"chapter_id": "A1.101"}, "Content"),
        ]
        
        result = export.build_combined_markdown(chapters, "Title", "Author", blurb="A great story.")
        self.assertIn("# Description", result)
        self.assertIn("A great story.", result)

    def test_author_bio_included(self):
        """Author bio is appended at the end."""
        chapters = [
            ({"chapter_id": "A1.101"}, "Content"),
        ]
        
        result = export.build_combined_markdown(chapters, "Title", "Author", author_bio="Author bio text")
        self.assertIn("# About the Author", result)
        self.assertIn("Author bio text", result)

    def test_cover_image_included(self):
        """Cover image is included at the beginning for DOCX/EPUB."""
        chapters = [
            ({"chapter_id": "A1.101"}, "Content"),
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            cover_path = Path(tmpdir) / "cover.png"
            cover_path.write_bytes(b"fake cover")
            
            result = export.build_combined_markdown(chapters, "Title", "Author", cover_image=cover_path, fmt="docx")
            self.assertIn("![](cover.png)", result)

    def test_cover_image_skipped_for_latex(self):
        """Cover image is skipped for LaTeX output."""
        chapters = [
            ({"chapter_id": "A1.101"}, "Content"),
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            cover_path = Path(tmpdir) / "cover.png"
            cover_path.write_bytes(b"fake cover")
            
            result = export.build_combined_markdown(chapters, "Title", "Author", cover_image=cover_path, fmt="latex")
            self.assertNotIn("![](cover.png)", result)


class TestFindDraftDir(unittest.TestCase):
    """Tests for find_draft_dir function."""

    def test_find_draft_upwards(self):
        """Draft directory is found by walking up from start path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir) / "project"
            draft_dir = project / "draft"
            draft_dir.mkdir(parents=True)
            
            # Start from a subdirectory
            subdir = project / "subdir"
            subdir.mkdir()
            
            result = export.find_draft_dir(subdir)
            self.assertEqual(result, draft_dir)

    def test_no_draft_returns_none(self):
        """Returns None when no draft directory found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = export.find_draft_dir(Path(tmpdir))
            self.assertIsNone(result)


class TestResolvePlatformTemplates(unittest.TestCase):
    """Tests for resolve_platform_templates function."""

    def test_epub_kdp_templates(self):
        """EPUB KDP platform resolves correct templates."""
        with tempfile.TemporaryDirectory() as tmpdir:
            templates_dir = Path(tmpdir)
            (templates_dir / "epub.css").write_text("css")
            (templates_dir / "epub-kdp.yml").write_text("yaml")
            
            result = export.resolve_platform_templates("epub", "kdp", templates_dir)
            self.assertTrue(result["epub_css"].exists())
            self.assertTrue(result["epub_defaults"].exists())

    def test_latex_kdp_templates(self):
        """LaTeX KDP platform resolves correct templates."""
        with tempfile.TemporaryDirectory() as tmpdir:
            templates_dir = Path(tmpdir)
            (templates_dir / "latex-kdp-6x9.tex").write_text("latex")
            
            result = export.resolve_platform_templates("latex", "kdp-print-6x9", templates_dir)
            self.assertTrue(result["latex_template"].exists())

    def test_missing_templates_returns_none(self):
        """Missing templates return None gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            templates_dir = Path(tmpdir)
            
            result = export.resolve_platform_templates("epub", "kdp", templates_dir)
            # Should not crash, just return None for missing files
            self.assertIsNotNone(result)


class TestExportDocx(unittest.TestCase):
    """Tests for export_docx function."""

    def test_export_docx_creates_file(self):
        """DOCX export creates output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.docx"
            combined_md = "% Test Title\n% Test Author\n\n# Chapter 1\n\nContent here"
            
            export.export_docx(combined_md, output_path, "Test Title", "Test Author", None)
            self.assertTrue(output_path.exists())


class TestExportLatex(unittest.TestCase):
    """Tests for export_latex function."""

    def test_export_latex_creates_file(self):
        """LaTeX export creates output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.tex"
            combined_md = "% Test Title\n% Test Author\n\n# Chapter 1\n\nContent here"
            
            export.export_latex(combined_md, output_path, "Test Title", "Test Author")
            self.assertTrue(output_path.exists())


class TestExportEpub(unittest.TestCase):
    """Tests for export_epub function."""

    def test_export_epub_creates_file(self):
        """EPUB export creates output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.epub"
            combined_md = "% Test Title\n% Test Author\n\n# Chapter 1\n\nContent here"
            
            export.export_epub(combined_md, output_path, "Test Title", "Test Author", None, None)
            self.assertTrue(output_path.exists())


class TestExportAudio(unittest.TestCase):
    """Tests for export_audio function."""

    def test_export_audio_no_audiodraft_dir(self):
        """Audio export fails gracefully when no audiodraft directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            
            import io
            old_stderr = sys.stderr
            old_exit = sys.exit
            old_stdout = sys.stdout
            sys.stderr = io.StringIO()
            sys.stdout = io.StringIO()
            sys.exit = lambda code: (_ for _ in ()).throw(SystemExit(code))
            
            try:
                with self.assertRaises(SystemExit):
                    export.export_audio(draft_dir, Path(tmpdir) / "output")
            finally:
                sys.stderr = old_stderr
                sys.stdout = old_stdout
                sys.exit = old_exit

    def test_export_audio_creates_manifest(self):
        """Audio export creates manifest.md when audiodraft exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            draft_dir = Path(tmpdir) / "draft"
            draft_dir.mkdir()
            audiodraft_dir = draft_dir.parent / "audiodraft"
            audiodraft_dir.mkdir()
            
            # Create a test SSML file
            ssml_content = """---
chapter_id: A1.101
chapter_name: Intro
---
<speak><voice>Content</voice></speak>"""
            (audiodraft_dir / "A1.101.ssml").write_text(ssml_content)
            
            # Create a prose chapter for comparison
            (draft_dir / "A1.101_Intro.md").write_text("---\nchapter_id: A1.101\n---\nContent")
            
            import io
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            try:
                export.export_audio(draft_dir, audiodraft_dir)
            finally:
                sys.stdout = old_stdout
            
            manifest_path = audiodraft_dir / "manifest.md"
            self.assertTrue(manifest_path.exists())
            manifest_content = manifest_path.read_text()
            self.assertIn("A1.101", manifest_content)
            self.assertIn("Intro", manifest_content)


if __name__ == "__main__":
    unittest.main()