#!/usr/bin/env python3
"""index.py — Offline semantic search index for large fiction projects.

Walks all project markdown files, chunks them into ~300-token segments with
metadata (file, section, character IDs, location IDs, date tags), and stores
embeddings in a local ChromaDB index (no external services — fully offline).

Primary backend  : ChromaDB + sentence-transformers (semantic / vector search)
Fallback backend : BM25 keyword search (pure Python, zero ML dependencies)

Usage:
    python index.py build   [--project-root PATH]
    python index.py update  [--project-root PATH]
    python index.py query   "siege warfare tactics 8th century" [--top 5] [--type draft]
    python index.py status  [--project-root PATH]
    python index.py purge   [--project-root PATH]   # wipe and rebuild

Options:
    --project-root PATH   Root of the speckit project (default: auto-detected)
    --top N               Number of results to return (default: 5)
    --type TYPE           Filter by doc type: spec | draft | outline | character | world |
                          research | glossary | relations | subplot | theme |
                          timeline | location | series | constitution
    --min-score FLOAT     Minimum similarity score threshold (0.0–1.0, default: 0.0)
    --index-dir PATH      Override index storage path (default: .specify/index/)

Primary backend requirements:
    pip install chromadb sentence-transformers

Fallback backend requirements (auto-detected, no install needed):
    rank_bm25  (optional: pip install rank-bm25)
    Built-in keyword search is used if neither chromadb nor rank_bm25 is available.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterator, NamedTuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

INDEX_DIR_NAME = ".specify/index"
MANIFEST_FILE = "manifest.json"
COLLECTION_NAME = "speckit_fiction"
CHUNK_TARGET_TOKENS = 300          # ~1 200–1 500 characters for English prose
CHUNK_OVERLAP_TOKENS = 30          # overlap to preserve sentence context
APPROX_CHARS_PER_TOKEN = 4.5       # rough estimate; avoids tiktoken dependency
DEFAULT_TOP_K = 5
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 45 MB, fast, good quality

# Directories and files to index, relative to project root.
# Globs are evaluated against the project root.
INDEX_GLOBS: list[tuple[str, str]] = [
    ("specs/*/spec.md",                    "spec"),
    (".specify/memory/constitution.md",    "constitution"),
    ("draft/*.md",                         "draft"),
    ("outlines/*.md",                      "outline"),
    ("characters/*.md",                    "character"),
    ("characters.md",                      "character"),
    ("world-building.md",                  "world"),
    ("research.md",                        "research"),
    ("glossary.md",                        "glossary"),
    ("relationships.md",                   "relations"),
    ("subplots.md",                        "subplot"),
    ("themes.md",                          "theme"),
    ("timeline.md",                        "timeline"),
    ("locations.md",                       "location"),
    ("series/series-bible.md",             "series"),
    ("series/*.md",                        "series"),
]

# ---------------------------------------------------------------------------
# Frontmatter parsing  (mirrors export.py)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Extract simple YAML frontmatter and body from markdown text."""
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
            val = val.split("#")[0].strip().strip('"').strip("'")
            meta[key.strip()] = val
    return meta, body


# ---------------------------------------------------------------------------
# Project root detection
# ---------------------------------------------------------------------------

def find_project_root(start: Path | None = None) -> Path:
    """Walk up from start (or cwd) to find a directory with specs/ or .specify/."""
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "specs").is_dir() or (candidate / ".specify").is_dir():
            return candidate
    return here


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

class Chunk(NamedTuple):
    chunk_id: str       # sha1 of (file_rel + "::" + chunk_index)
    text: str
    file_rel: str       # path relative to project root (forward slashes)
    doc_type: str
    section: str        # nearest H1/H2/H3 heading above this chunk
    chapter_id: str     # from frontmatter, or ""
    character_ids: str  # comma-separated character slugs (may be empty)
    location_ids: str   # comma-separated location slugs (may be empty)
    date_tag: str       # from frontmatter date / chapter_date (may be empty)
    file_mtime: float


_CHAR_WIKILINK_RE = re.compile(r"\[\[([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\]\]")
_LOCATION_SLUG_RE = re.compile(r"^(?:INT\.|EXT\.|INT\.\/EXT\.)\s+([A-Z][^—\n]{2,60})", re.MULTILINE)


def _estimate_chars(tokens: int) -> int:
    return int(tokens * APPROX_CHARS_PER_TOKEN)


def _slugify(text: str) -> str:
    return text.strip().lower().replace(" ", "-")


def _extract_character_ids(body: str, meta: dict[str, str]) -> str:
    ids: set[str] = set()
    for key in ("character", "characters", "pov_character"):
        if val := meta.get(key):
            for name in re.split(r"[,;]", val):
                slug = _slugify(name)
                if slug:
                    ids.add(slug)
    for m in _CHAR_WIKILINK_RE.finditer(body):
        ids.add(_slugify(m.group(1)))
    return ",".join(sorted(ids))


def _extract_location_ids(body: str, meta: dict[str, str]) -> str:
    ids: set[str] = set()
    if val := meta.get("location"):
        ids.add(_slugify(val)[:60])
    for m in _LOCATION_SLUG_RE.finditer(body):
        slug = _slugify(m.group(1).rstrip("-"))[:60]
        if slug:
            ids.add(slug)
    return ",".join(sorted(ids))


def chunk_file(path: Path, project_root: Path, doc_type: str) -> list[Chunk]:
    """Read a markdown file and return Chunk objects."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    meta, body = parse_frontmatter(text)
    file_rel = str(path.relative_to(project_root)).replace("\\", "/")
    mtime = path.stat().st_mtime

    chapter_id = meta.get("chapter_id", "")
    date_tag = meta.get("date", meta.get("chapter_date", ""))
    char_ids = _extract_character_ids(body, meta)
    loc_ids  = _extract_location_ids(body, meta)

    # Split body into (heading, text) sections at H1/H2/H3 boundaries
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_lines: list[str] = []

    for line in body.splitlines(keepends=True):
        hm = re.match(r"^#{1,3}\s+(.+)$", line.rstrip())
        if hm:
            if current_lines:
                sections.append((current_heading, "".join(current_lines)))
            current_heading = hm.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_heading, "".join(current_lines)))

    target_chars  = _estimate_chars(CHUNK_TARGET_TOKENS)
    overlap_chars = _estimate_chars(CHUNK_OVERLAP_TOKENS)
    chunks: list[Chunk] = []
    chunk_index = 0

    for heading, section_body in sections:
        start = 0
        while start < len(section_body):
            end = start + target_chars
            # Extend to next paragraph break to avoid mid-paragraph cuts
            next_break = section_body.find("\n\n", end)
            if next_break != -1 and next_break < end + 300:
                end = next_break
            chunk_text = section_body[start:end].strip()
            if not chunk_text:
                start = max(start + 1, end)
                continue

            display_text = f"## {heading}\n\n{chunk_text}" if heading else chunk_text
            raw_id = f"{file_rel}::{chunk_index}"
            chunk_id = hashlib.sha1(raw_id.encode()).hexdigest()[:16]

            chunks.append(Chunk(
                chunk_id=chunk_id,
                text=display_text,
                file_rel=file_rel,
                doc_type=doc_type,
                section=heading,
                chapter_id=chapter_id,
                character_ids=char_ids,
                location_ids=loc_ids,
                date_tag=date_tag,
                file_mtime=mtime,
            ))
            chunk_index += 1
            start = max(start + 1, end - overlap_chars)

    return chunks


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def discover_files(project_root: Path) -> Iterator[tuple[Path, str]]:
    """Yield (path, doc_type) for all indexable markdown files."""
    seen: set[Path] = set()
    for pattern, doc_type in INDEX_GLOBS:
        for path in sorted(project_root.glob(pattern)):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path, doc_type


# ---------------------------------------------------------------------------
# Manifest (tracks mtimes for incremental updates)
# ---------------------------------------------------------------------------

def load_manifest(index_dir: Path) -> dict[str, float]:
    mf = index_dir / MANIFEST_FILE
    if mf.exists():
        try:
            return json.loads(mf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_manifest(index_dir: Path, manifest: dict[str, float]) -> None:
    index_dir.mkdir(parents=True, exist_ok=True)
    (index_dir / MANIFEST_FILE).write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Backend: ChromaDB + sentence-transformers
# ---------------------------------------------------------------------------

def _try_import_chroma():
    try:
        import chromadb  # type: ignore
        from chromadb.utils import embedding_functions  # type: ignore
        return chromadb, embedding_functions
    except ImportError:
        return None, None


def _try_import_bm25():
    try:
        from rank_bm25 import BM25Okapi  # type: ignore
        return BM25Okapi
    except ImportError:
        return None


class ChromaBackend:
    def __init__(self, index_dir: Path) -> None:
        chromadb, ef = _try_import_chroma()
        if chromadb is None:
            raise ImportError("chromadb not installed — run: pip install chromadb sentence-transformers")
        self._client = chromadb.PersistentClient(path=str(index_dir / "chroma"))
        emb_fn = ef.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
        self._col = self._client.get_or_create_collection(
            COLLECTION_NAME, embedding_function=emb_fn
        )

    def upsert(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        self._col.upsert(
            ids=[c.chunk_id for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[{
                "file_rel":      c.file_rel,
                "doc_type":      c.doc_type,
                "section":       c.section,
                "chapter_id":    c.chapter_id,
                "character_ids": c.character_ids,
                "location_ids":  c.location_ids,
                "date_tag":      c.date_tag,
            } for c in chunks],
        )

    def delete_by_file(self, file_rel: str) -> None:
        results = self._col.get(where={"file_rel": file_rel})
        if results["ids"]:
            self._col.delete(ids=results["ids"])

    def query(self, text: str, top_k: int, doc_type: str | None) -> list[dict]:
        where = {"doc_type": doc_type} if doc_type else None
        results = self._col.query(
            query_texts=[text],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        out = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            score = max(0.0, 1.0 - dist)  # cosine: distance → similarity
            out.append({"text": doc, "score": score, **meta})
        return out

    def count(self) -> int:
        return self._col.count()


# ---------------------------------------------------------------------------
# Fallback: BM25 / keyword backend
# ---------------------------------------------------------------------------

class KeywordBackend:
    """BM25 or basic TF fallback when ChromaDB / sentence-transformers are unavailable."""

    _DATA_FILE = "keyword_index.json"

    def __init__(self, index_dir: Path) -> None:
        self._index_dir = index_dir
        self._data: list[dict] = []
        self._load()

    def _load(self) -> None:
        path = self._index_dir / self._DATA_FILE
        if path.exists():
            try:
                self._data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._data = []

    def _save(self) -> None:
        self._index_dir.mkdir(parents=True, exist_ok=True)
        path = self._index_dir / self._DATA_FILE
        path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def upsert(self, chunks: list[Chunk]) -> None:
        existing_ids = {d["chunk_id"] for d in self._data}
        for c in chunks:
            record = {
                "chunk_id":      c.chunk_id,
                "text":          c.text,
                "file_rel":      c.file_rel,
                "doc_type":      c.doc_type,
                "section":       c.section,
                "chapter_id":    c.chapter_id,
                "character_ids": c.character_ids,
                "location_ids":  c.location_ids,
                "date_tag":      c.date_tag,
            }
            if c.chunk_id in existing_ids:
                self._data = [d if d["chunk_id"] != c.chunk_id else record for d in self._data]
            else:
                self._data.append(record)
        self._save()

    def delete_by_file(self, file_rel: str) -> None:
        self._data = [d for d in self._data if d["file_rel"] != file_rel]
        self._save()

    def query(self, text: str, top_k: int, doc_type: str | None) -> list[dict]:
        BM25Okapi = _try_import_bm25()
        pool = [d for d in self._data if doc_type is None or d["doc_type"] == doc_type]
        if not pool:
            return []

        query_tokens = text.lower().split()
        corpus = [d["text"].lower().split() for d in pool]

        if BM25Okapi:
            bm25 = BM25Okapi(corpus)
            scores = list(bm25.get_scores(query_tokens))
        else:
            # Built-in TF scoring — zero dependencies
            scores = []
            for tokens in corpus:
                token_set = set(tokens)
                scores.append(float(sum(1 for t in query_tokens if t in token_set)))

        max_score = max(scores) if scores else 1.0
        ranked = sorted(zip(scores, pool), key=lambda x: x[0], reverse=True)[:top_k]
        return [
            {"score": s / max(max_score, 1e-9), **d}
            for s, d in ranked
            if s > 0
        ]

    def count(self) -> int:
        return len(self._data)


# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------

def get_backend(index_dir: Path, force_keyword: bool = False):
    if not force_keyword:
        chromadb, _ = _try_import_chroma()
        if chromadb is not None:
            try:
                return ChromaBackend(index_dir), "chroma"
            except Exception as exc:
                print(f"[warn] ChromaDB unavailable ({exc}); falling back to keyword search.", file=sys.stderr)
    return KeywordBackend(index_dir), "keyword"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_build(args: argparse.Namespace) -> None:
    root = find_project_root(Path(args.project_root) if args.project_root else None)
    index_dir = Path(args.index_dir) if args.index_dir else root / INDEX_DIR_NAME
    index_dir.mkdir(parents=True, exist_ok=True)

    backend, backend_name = get_backend(index_dir)
    print(f"Building index (backend: {backend_name}) …")
    print(f"  Project root : {root}")
    print(f"  Index dir    : {index_dir}")

    manifest: dict[str, float] = {}
    total_files = total_chunks = 0

    for path, doc_type in discover_files(root):
        file_rel = str(path.relative_to(root)).replace("\\", "/")
        chunks = chunk_file(path, root, doc_type)
        if chunks:
            backend.upsert(chunks)
            manifest[file_rel] = path.stat().st_mtime
            total_files += 1
            total_chunks += len(chunks)
            print(f"  [{doc_type:>12}]  {file_rel}  ({len(chunks)} chunks)")

    save_manifest(index_dir, manifest)
    print(f"\nDone. {total_files} files, {total_chunks} chunks indexed.")


def cmd_update(args: argparse.Namespace) -> None:
    root = find_project_root(Path(args.project_root) if args.project_root else None)
    index_dir = Path(args.index_dir) if args.index_dir else root / INDEX_DIR_NAME

    backend, backend_name = get_backend(index_dir)
    manifest = load_manifest(index_dir)
    print(f"Updating index (backend: {backend_name}) …")

    added = updated = skipped = 0

    for path, doc_type in discover_files(root):
        file_rel = str(path.relative_to(root)).replace("\\", "/")
        mtime = path.stat().st_mtime
        if manifest.get(file_rel) == mtime:
            skipped += 1
            continue
        backend.delete_by_file(file_rel)
        chunks = chunk_file(path, root, doc_type)
        if chunks:
            backend.upsert(chunks)
        if file_rel in manifest:
            updated += 1
            print(f"  [updated]  {file_rel}  ({len(chunks)} chunks)")
        else:
            added += 1
            print(f"  [added]    {file_rel}  ({len(chunks)} chunks)")
        manifest[file_rel] = mtime

    save_manifest(index_dir, manifest)
    print(f"\nDone. {added} added, {updated} updated, {skipped} skipped.")


def cmd_query(args: argparse.Namespace) -> None:
    root = find_project_root(Path(args.project_root) if args.project_root else None)
    index_dir = Path(args.index_dir) if args.index_dir else root / INDEX_DIR_NAME

    if not index_dir.exists():
        print("No index found. Run: python index.py build", file=sys.stderr)
        sys.exit(1)

    backend, backend_name = get_backend(index_dir)
    results = backend.query(args.query, top_k=args.top, doc_type=args.type)
    min_score = getattr(args, "min_score", 0.0)
    results = [r for r in results if r["score"] >= min_score]

    if not results:
        print("No results found.")
        return

    print(f'Query: "{args.query}"  (backend: {backend_name}, top {args.top})\n')
    for i, r in enumerate(results, 1):
        section_label = f" § {r['section']}" if r.get("section") else ""
        char_label    = f"  chars: {r['character_ids']}" if r.get("character_ids") else ""
        loc_label     = f"  locs: {r['location_ids']}" if r.get("location_ids") else ""
        print(f"[{i}] {r['file_rel']}{section_label}  (score: {r['score']:.3f}  type: {r['doc_type']}){char_label}{loc_label}")
        preview = "\n    ".join(r["text"].splitlines()[:3])
        print(f"    {preview}\n")


def cmd_status(args: argparse.Namespace) -> None:
    root = find_project_root(Path(args.project_root) if args.project_root else None)
    index_dir = Path(args.index_dir) if args.index_dir else root / INDEX_DIR_NAME

    manifest = load_manifest(index_dir)
    backend, backend_name = get_backend(index_dir)

    stale   = sum(1 for fr, mt in manifest.items() if (root / fr).exists() and (root / fr).stat().st_mtime != mt)
    missing = sum(1 for fr in manifest if not (root / fr).exists())
    new_files = sum(
        1 for path, _ in discover_files(root)
        if str(path.relative_to(root)).replace("\\", "/") not in manifest
    )

    print(f"Index status")
    print(f"  Backend      : {backend_name}")
    print(f"  Index dir    : {index_dir}")
    print(f"  Files indexed: {len(manifest)}")
    print(f"  Total chunks : {backend.count()}")
    print(f"  Stale files  : {stale}  (run: python index.py update)")
    print(f"  Missing files: {missing}")
    print(f"  New files    : {new_files}")


def cmd_purge(args: argparse.Namespace) -> None:
    import shutil
    root = find_project_root(Path(args.project_root) if args.project_root else None)
    index_dir = Path(args.index_dir) if args.index_dir else root / INDEX_DIR_NAME
    if index_dir.exists():
        shutil.rmtree(index_dir)
        print(f"Purged index at {index_dir}.")
    else:
        print("No index found.")
    cmd_build(args)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="index.py",
        description="Offline semantic/keyword search index for speckit fiction projects.",
    )
    p.add_argument("--project-root", metavar="PATH", default=None)
    p.add_argument("--index-dir",    metavar="PATH", default=None)

    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("build",  help="Build index from scratch")
    sub.add_parser("update", help="Incrementally update index (changed files only)")

    qp = sub.add_parser("query", help="Search the index")
    qp.add_argument("query",       help="Search query string")
    qp.add_argument("--top",       type=int,   default=DEFAULT_TOP_K, metavar="N")
    qp.add_argument("--type",      metavar="TYPE", default=None,
                    help="Filter by doc type: spec|draft|character|world|research|…")
    qp.add_argument("--min-score", type=float, default=0.0, metavar="FLOAT")

    sub.add_parser("status", help="Show index statistics and staleness")
    sub.add_parser("purge",  help="Wipe index and rebuild from scratch")

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    {
        "build":  cmd_build,
        "update": cmd_update,
        "query":  cmd_query,
        "status": cmd_status,
        "purge":  cmd_purge,
    }[args.command](args)


if __name__ == "__main__":
    main()
