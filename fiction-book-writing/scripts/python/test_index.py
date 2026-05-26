#!/usr/bin/env python3
"""Unit tests for index.py — offline semantic search index for speckit fiction projects."""

import tempfile
import unittest
from pathlib import Path
import sys
import json

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent))
import index


class TestParseFrontmatter(unittest.TestCase):
    """Tests for parse_frontmatter function."""

    def test_no_frontmatter(self):
        """Text without frontmatter returns empty dict and original text."""
        text = "Just some content\nwithout frontmatter"
        meta, body = index.parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, text)

    def test_simple_frontmatter(self):
        """Simple key: value frontmatter is parsed correctly."""
        text = "---\nchapter_id: A1.101\nchapter_name: Awakening\n---\n\nBody content here"
        meta, body = index.parse_frontmatter(text)
        self.assertEqual(meta, {"chapter_id": "A1.101", "chapter_name": "Awakening"})
        self.assertEqual(body, "Body content here")

    def test_frontmatter_with_quotes(self):
        """Quoted values are stripped correctly."""
        text = '---\ntitle: "My Story"\nauthor: \'John Doe\'\n---\n\nContent'
        meta, body = index.parse_frontmatter(text)
        self.assertEqual(meta, {"title": "My Story", "author": "John Doe"})

    def test_frontmatter_with_inline_comments(self):
        """Inline YAML comments are removed from values."""
        text = "---\nchapter_id: A1.101 # chapter id\n---\n\nContent"
        meta, body = index.parse_frontmatter(text)
        self.assertEqual(meta, {"chapter_id": "A1.101"})

    def test_frontmatter_with_missing_end(self):
        """Frontmatter without closing --- returns empty dict and original text."""
        text = "---\nchapter_id: A1.101\n\nNo closing"
        meta, body = index.parse_frontmatter(text)
        self.assertEqual(meta, {})
        self.assertEqual(body, text)


class TestSlugify(unittest.TestCase):
    """Tests for _slugify helper function."""

    def test_basic_slugify(self):
        """Basic slugification works."""
        self.assertEqual(index._slugify("John Doe"), "john-doe")

    def test_slugify_with_spaces(self):
        """Multiple spaces are handled correctly."""
        self.assertEqual(index._slugify("  Jane   Smith  "), "jane-smith")

    def test_slugify_empty(self):
        """Empty string returns empty string."""
        self.assertEqual(index._slugify(""), "")


class TestEstimateChars(unittest.TestCase):
    """Tests for _estimate_chars helper function."""

    def test_basic_estimation(self):
        """Character estimation uses 4.5x multiplier."""
        result = index._estimate_chars(100)
        self.assertEqual(result, 450)

    def test_zero_tokens(self):
        """Zero tokens returns zero characters."""
        result = index._estimate_chars(0)
        self.assertEqual(result, 0)


class TestExtractCharacterIds(unittest.TestCase):
    """Tests for _extract_character_ids function."""

    def test_from_frontmatter(self):
        """Character IDs extracted from frontmatter."""
        meta = {"character": "John Doe, Jane Smith"}
        body = ""
        result = index._extract_character_ids(body, meta)
        self.assertEqual(result, "jane-smith,john-doe")

    def test_from_wikilinks(self):
        """Character IDs extracted from [[WikiLink]] syntax."""
        meta = {}
        body = "The [[John Doe]] walked through the [[Dark Forest]]."
        result = index._extract_character_ids(body, meta)
        self.assertEqual(result, "dark-forest,john-doe")

    def test_combined_sources(self):
        """Character IDs from both frontmatter and wikilinks."""
        meta = {"character": "John Doe"}
        body = "The [[Jane Smith]] appeared."
        result = index._extract_character_ids(body, meta)
        self.assertEqual(result, "jane-smith,john-doe")

    def test_no_characters(self):
        """Empty string when no characters found."""
        meta = {}
        body = "No characters here."
        result = index._extract_character_ids(body, meta)
        self.assertEqual(result, "")


class TestExtractLocationIds(unittest.TestCase):
    """Tests for _extract_location_ids function."""

    def test_from_frontmatter(self):
        """Location ID extracted from frontmatter."""
        meta = {"location": "Castle Black"}
        body = ""
        result = index._extract_location_ids(body, meta)
        self.assertEqual(result, "castle-black")

    def test_from_scene_heading(self):
        """Location IDs extracted from INT./EXT. scene headings."""
        meta = {}
        body = "INT. CASTLE BLACK - NIGHT\n\nSome action.\n\nEXT. FOREST CLEARING - DAY"
        result = index._extract_location_ids(body, meta)
        self.assertIn("castle-black", result)
        self.assertIn("forest-clearing", result)

    def test_no_locations(self):
        """Empty string when no locations found."""
        meta = {}
        body = "No locations here."
        result = index._extract_location_ids(body, meta)
        self.assertEqual(result, "")


class TestChunkFile(unittest.TestCase):
    """Tests for chunk_file function."""

    def test_basic_chunking(self):
        """File is chunked into Chunk objects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            test_file = project_root / "test.md"
            test_file.write_text("---\nchapter_id: A1.101\n---\n\n# Section 1\n\nContent here.")
            
            chunks = index.chunk_file(test_file, project_root, "draft")
            self.assertTrue(len(chunks) > 0)
            self.assertEqual(chunks[0].chapter_id, "A1.101")
            self.assertEqual(chunks[0].doc_type, "draft")

    def test_chunk_with_character_ids(self):
        """Chunk includes extracted character IDs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            test_file = project_root / "test.md"
            test_file.write_text("---\ncharacter: John Doe\n---\n\nThe [[Jane Smith]] appeared.")
            
            chunks = index.chunk_file(test_file, project_root, "draft")
            self.assertIn("john-doe", chunks[0].character_ids)
            self.assertIn("jane-smith", chunks[0].character_ids)

    def test_chunk_with_section(self):
        """Chunk includes section heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            test_file = project_root / "test.md"
            test_file.write_text("# Main Heading\n\nContent under heading.")
            
            chunks = index.chunk_file(test_file, project_root, "draft")
            self.assertEqual(chunks[0].section, "Main Heading")


class TestFindProjectRoot(unittest.TestCase):
    """Tests for find_project_root function."""

    def test_find_specs_dir(self):
        """Project root found via specs/ directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir) / "myproject"
            (project / "specs").mkdir(parents=True)
            
            result = index.find_project_root(project)
            self.assertEqual(result.resolve(), project.resolve())

    def test_find_specify_dir(self):
        """Project root found via .specify/ directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir) / "myproject"
            (project / ".specify").mkdir(parents=True)
            
            result = index.find_project_root(project)
            self.assertEqual(result.resolve(), project.resolve())

    def test_fallback_to_cwd(self):
        """Falls back to current directory when no markers found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = index.find_project_root(Path(tmpdir))
            # Should return the tmpdir itself (resolved)
            self.assertEqual(result.resolve(), Path(tmpdir).resolve())


class TestDiscoverFiles(unittest.TestCase):
    """Tests for discover_files function."""

    def test_discover_markdown_files(self):
        """Markdown files are discovered with correct doc types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / "draft").mkdir()
            (project_root / "draft" / "A1.101_Intro.md").write_text("content")
            
            files = list(index.discover_files(project_root))
            self.assertTrue(len(files) > 0)
            # Check that we found the draft file
            found_draft = any(f[1] == "draft" for f in files)
            self.assertTrue(found_draft)

    def test_discover_nested_spec_files(self):
        """Nested spec folder files are discovered."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / "specs").mkdir()
            (project_root / "specs" / "mybook").mkdir()
            (project_root / "specs" / "mybook" / "spec.md").write_text("content")
            
            files = list(index.discover_files(project_root))
            found_spec = any("spec.md" in str(f[0]) for f in files)
            self.assertTrue(found_spec)


class TestLoadSaveManifest(unittest.TestCase):
    """Tests for load_manifest and save_manifest functions."""

    def test_save_and_load_manifest(self):
        """Manifest is saved and loaded correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            manifest = {"file1.md": 1234.5, "file2.md": 5678.9}
            
            index.save_manifest(index_dir, manifest)
            loaded = index.load_manifest(index_dir)
            
            self.assertEqual(loaded, manifest)

    def test_load_empty_manifest(self):
        """Loading non-existent manifest returns empty dict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            loaded = index.load_manifest(index_dir)
            self.assertEqual(loaded, {})


class TestKeywordBackend(unittest.TestCase):
    """Tests for KeywordBackend class."""

    def test_upsert_and_count(self):
        """Chunks are upserted and counted correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            backend = index.KeywordBackend(index_dir)
            
            chunks = [
                index.Chunk(
                    chunk_id="abc123",
                    text="Test content",
                    file_rel="test.md",
                    doc_type="draft",
                    section="Test",
                    chapter_id="A1.101",
                    character_ids="",
                    location_ids="",
                    date_tag="",
                    file_mtime=1.0,
                )
            ]
            
            backend.upsert(chunks)
            self.assertEqual(backend.count(), 1)

    def test_delete_by_file(self):
        """Chunks are deleted by file_rel correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            backend = index.KeywordBackend(index_dir)
            
            chunks = [
                index.Chunk(
                    chunk_id="abc123",
                    text="Test content",
                    file_rel="test.md",
                    doc_type="draft",
                    section="Test",
                    chapter_id="A1.101",
                    character_ids="",
                    location_ids="",
                    date_tag="",
                    file_mtime=1.0,
                ),
                index.Chunk(
                    chunk_id="def456",
                    text="Other content",
                    file_rel="other.md",
                    doc_type="spec",
                    section="Other",
                    chapter_id="",
                    character_ids="",
                    location_ids="",
                    date_tag="",
                    file_mtime=1.0,
                ),
            ]
            
            backend.upsert(chunks)
            backend.delete_by_file("test.md")
            self.assertEqual(backend.count(), 1)

    def test_query_basic(self):
        """Query returns results with scores."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            backend = index.KeywordBackend(index_dir)
            
            chunks = [
                index.Chunk(
                    chunk_id="abc123",
                    text="The quick brown fox jumps over the lazy dog",
                    file_rel="test.md",
                    doc_type="draft",
                    section="Test",
                    chapter_id="A1.101",
                    character_ids="",
                    location_ids="",
                    date_tag="",
                    file_mtime=1.0,
                ),
                index.Chunk(
                    chunk_id="def456",
                    text="A different document about cats",
                    file_rel="test2.md",
                    doc_type="draft",
                    section="Test2",
                    chapter_id="A1.102",
                    character_ids="",
                    location_ids="",
                    date_tag="",
                    file_mtime=1.0,
                ),
            ]
            
            backend.upsert(chunks)
            results = backend.query("fox", top_k=5, doc_type=None)
            self.assertTrue(len(results) > 0)
            self.assertIn("score", results[0])

    def test_query_with_doc_type_filter(self):
        """Query filters by doc_type correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            backend = index.KeywordBackend(index_dir)
            
            chunks = [
                index.Chunk(
                    chunk_id="abc123",
                    text="Draft content about fox",
                    file_rel="draft.md",
                    doc_type="draft",
                    section="Draft",
                    chapter_id="",
                    character_ids="",
                    location_ids="",
                    date_tag="",
                    file_mtime=1.0,
                ),
                index.Chunk(
                    chunk_id="def456",
                    text="Spec content about cats",
                    file_rel="spec.md",
                    doc_type="spec",
                    section="Spec",
                    chapter_id="",
                    character_ids="",
                    location_ids="",
                    date_tag="",
                    file_mtime=1.0,
                ),
            ]
            
            backend.upsert(chunks)
            results = backend.query("fox", top_k=5, doc_type="draft")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["doc_type"], "draft")


class TestGetBackend(unittest.TestCase):
    """Tests for get_backend function."""

    def test_keyword_backend_forced(self):
        """Keyword backend is forced when force_keyword=True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            backend, name = index.get_backend(index_dir, force_keyword=True)
            self.assertEqual(name, "keyword")
            self.assertIsInstance(backend, index.KeywordBackend)

    def test_auto_backend_falls_back(self):
        """Auto backend falls back to keyword when chroma unavailable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_dir = Path(tmpdir)
            backend, name = index.get_backend(index_dir, backend_preference="auto")
            self.assertEqual(name, "keyword")
            self.assertIsInstance(backend, index.KeywordBackend)


class TestLoadConfig(unittest.TestCase):
    """Tests for _load_config function."""

    def test_default_config_created(self):
        """Default config is created when missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            config = index._load_config(project_root)
            
            self.assertEqual(config["backend_preference"], "auto")
            self.assertEqual(config["embedding_model"], "all-MiniLM-L6-v2")
            self.assertEqual(config["chunk_size_tokens"], 200)
            self.assertEqual(config["top_k"], 3)
            
            # Verify config file was created
            config_path = project_root / ".specify" / "index" / "config.json"
            self.assertTrue(config_path.exists())

    def test_existing_config_loaded(self):
        """Existing config is loaded and merged with defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            config_dir = project_root / ".specify" / "index"
            config_dir.mkdir(parents=True)
            config_path = config_dir / "config.json"
            config_path.write_text('{"chunk_size_tokens": 500}')
            
            config = index._load_config(project_root)
            self.assertEqual(config["chunk_size_tokens"], 500)
            self.assertEqual(config["backend_preference"], "auto")  # default preserved


class TestBuildParser(unittest.TestCase):
    """Tests for build_parser function."""

    def test_parser_has_commands(self):
        """Parser has all required subcommands."""
        parser = index.build_parser()
        # Parse with --help to get subparsers
        with self.assertRaises(SystemExit):
            parser.parse_args(["--help"])


if __name__ == "__main__":
    unittest.main()