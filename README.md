# speckit-preset-fiction-book-writing

A [Spec Kit](https://github.com/github/spec-kit) preset for novel and long-form fiction writing.

It adapts the Spec-Driven Development workflow for storytelling: features become story elements, specs become story briefs, plans become story structures, and tasks become scene-by-scene writing tasks. Supports single and multi-POV, all major plot structure frameworks, and two style modes — author voice sample or humanized AI prose.

---

## Contents

```
fiction-book-writing/   ← The installable preset
```

The preset directory contains:

- `preset.yml` — manifest consumed by `specify preset add`
- `commands/` — 25 AI slash commands covering every stage from idea to submission
- `templates/` — 21 story document templates (characters, world-building, timelines, etc.)
- `scripts/` — pandoc-based export script for DOCX, EPUB, and LaTeX

---

## Full Documentation

See **[fiction-book-writing/README.md](fiction-book-writing/README.md)** for:

- Quick Start guide
- Complete commands reference
- Templates reference
- Tutorials (single POV, multi-POV, planning, drafting, revision, submission)
- POV modes and plot structure support
- Style modes (`author-sample` / `humanized-ai`)
- Export formats

---

## Installation

Requires [Spec Kit](https://github.com/github/spec-kit) >= 0.5.0.

```bash
specify preset add --from https://github.com/adaumann/speckit-preset-fiction-book-writing/archive/refs/tags/v1.3.0.zip
```

Or for local development:

```bash
specify preset add --dev /path/to/speckit-preset-fiction-book-writing/fiction-book-writing
```

---

## License

MIT — see [fiction-book-writing/LICENSE](fiction-book-writing/LICENSE).
