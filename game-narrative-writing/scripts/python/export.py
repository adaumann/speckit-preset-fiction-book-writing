"""
export.py — speckit game-narrative-writing export script

Translates intermediate Markdown node files to:
  - Twee 3 / Sugarcube (.twee)
  - Ink (.ink)

Usage:
  python export.py --target sugarcube --output export/
  python export.py --target ink --output export/
  python export.py --target both --output export/
  python export.py --target sugarcube --dry-run

Requires:
  - nodes/NODE-*.md: node files with YAML frontmatter and [MECHANIC:TYPE] hook blocks
  - variables.md: variable registry (for initialization blocks)
  - .speckit/memory/constitution.md: engine target and POV configuration

No third-party dependencies for core functionality.
PyYAML is used for frontmatter parsing; falls back to manual parse if unavailable.
"""

import argparse
import os
import re
import sys
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

NODES_DIR = "nodes"
VARIABLES_FILE = "variables.md"
CONSTITUTION_FILE = os.path.join(".speckit", "memory", "constitution.md")
DEFAULT_OUTPUT_DIR = "export"

# Tier 2 hook types — export as stubs with warning comments
TIER2_HOOKS = {
    "KNOWLEDGE",
    "FACTION",
    "LOCATION_STATE",
    "OBJECT_STATE",
}

# ---------------------------------------------------------------------------
# Frontmatter parsing (no third-party dependency fallback)
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter delimited by --- lines.
    Returns (metadata_dict, body_text).
    Falls back to simple key:value parsing if PyYAML is unavailable.
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    frontmatter_text = text[3:end].strip()
    body = text[end + 4:].strip()

    try:
        import yaml  # type: ignore
        metadata = yaml.safe_load(frontmatter_text) or {}
    except ImportError:
        metadata = _parse_simple_yaml(frontmatter_text)

    return metadata, body


def _parse_simple_yaml(text: str) -> dict:
    """Minimal key: value YAML parser for environments without PyYAML."""
    result = {}
    list_key = None
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("  - ") and list_key:
            result.setdefault(list_key, []).append(line.strip()[2:].strip())
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value == "":
                list_key = key
                result[key] = []
            else:
                list_key = None
                result[key] = value
    return result


# ---------------------------------------------------------------------------
# Node file loading
# ---------------------------------------------------------------------------


def load_nodes(nodes_dir: str) -> list[dict]:
    """Load all approved node files. Returns list of node dicts."""
    nodes = []
    node_path = Path(nodes_dir)
    if not node_path.exists():
        print(f"ERROR: nodes directory not found: {nodes_dir}", file=sys.stderr)
        sys.exit(1)

    for filepath in sorted(node_path.glob("*.md")):
        text = filepath.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        status = meta.get("status", "DRAFT")
        if status == "SKIP":
            continue
        if status != "APPROVED":
            print(
                f"WARNING: {filepath.name} has status '{status}' — excluded from export.",
                file=sys.stderr,
            )
            continue

        nodes.append(
            {
                "file": filepath.name,
                "node_id": meta.get("node_id", filepath.stem),
                "title": meta.get("title", filepath.stem),
                "act": meta.get("act", ""),
                "pov": meta.get("pov", None),
                "variables_read": meta.get("variables_read", []),
                "variables_set": meta.get("variables_set", []),
                "body": body,
                "meta": meta,
            }
        )

    return nodes


# ---------------------------------------------------------------------------
# Mechanic hook block parser
# ---------------------------------------------------------------------------

# Pattern: [MECHANIC:TYPE] ... [/MECHANIC] (block or inline)
HOOK_BLOCK_RE = re.compile(
    r"\[MECHANIC:(\w+)\](.*?)\[/MECHANIC\]", re.DOTALL | re.IGNORECASE
)
# Inline single-line hooks: [MECHANIC:TYPE key=value key2=value2]
# Double-parsing against block spans is handled in parse_hooks() below.
HOOK_INLINE_RE = re.compile(r"\[MECHANIC:(\w+)\s([^\]\n]*)\]", re.IGNORECASE)


def parse_hooks(body: str) -> list[dict]:
    """
    Extract all mechanic hook blocks and inline hooks from node body.
    Returns list of hook dicts with 'type', 'params', and 'raw'.
    Block hooks ([MECHANIC:TYPE]...[/MECHANIC]) are parsed first and their
    spans are tracked so the inline pass does not double-parse them.
    """
    hooks = []
    block_spans: list[tuple[int, int]] = []

    for match in HOOK_BLOCK_RE.finditer(body):
        hook_type = match.group(1).upper()
        content = match.group(2).strip()
        params = _parse_hook_params(content)
        hooks.append({"type": hook_type, "params": params, "raw": match.group(0)})
        block_spans.append((match.start(), match.end()))

    for match in HOOK_INLINE_RE.finditer(body):
        # Skip if this position is inside an already-parsed block
        pos = match.start()
        if any(start <= pos < end for start, end in block_spans):
            continue
        hook_type = match.group(1).upper()
        content = match.group(2).strip()
        params = _parse_hook_params(content)
        hooks.append({"type": hook_type, "params": params, "raw": match.group(0)})

    return hooks


def _parse_hook_params(content: str) -> dict:
    """Parse hook parameter string: 'key: value' or 'key=value' pairs."""
    params = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for sep in (":", "="):
            if sep in line:
                key, _, value = line.partition(sep)
                params[key.strip()] = value.strip()
                break
    return params


def strip_hooks(body: str) -> str:
    """Remove all hook blocks from body text, leaving clean prose."""
    body = HOOK_BLOCK_RE.sub("", body)
    body = HOOK_INLINE_RE.sub("", body)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


# ---------------------------------------------------------------------------
# Choice block parser
# ---------------------------------------------------------------------------

# Choices section header
CHOICES_SECTION_RE = re.compile(r"^##\s+Choices\s*$", re.MULTILINE | re.IGNORECASE)
# Choice line: - [Label text](target_node_id) [optional condition note]
CHOICE_LINE_RE = re.compile(
    r"^\s*-\s+\[([^\]]+)\]\(([^)]+)\)(?:\s+<!--\s*(.*?)\s*-->)?", re.MULTILINE
)


def parse_choices(body: str) -> list[dict]:
    """
    Extract choices from the Choices section.
    Returns list of {'label': str, 'target': str, 'condition': str|None}.
    """
    choices = []
    section_match = CHOICES_SECTION_RE.search(body)
    if not section_match:
        return choices

    section_text = body[section_match.end():]
    # Stop at next heading
    next_heading = re.search(r"^##", section_text, re.MULTILINE)
    if next_heading:
        section_text = section_text[: next_heading.start()]

    for match in CHOICE_LINE_RE.finditer(section_text):
        choices.append(
            {
                "label": match.group(1).strip(),
                "target": match.group(2).strip(),
                "condition": match.group(3).strip() if match.group(3) else None,
            }
        )

    return choices


# ---------------------------------------------------------------------------
# Prose extraction (body without choices section and without hooks)
# ---------------------------------------------------------------------------


def extract_prose(body: str) -> str:
    """Return clean prose: no hooks, no choices section."""
    # Remove choices section
    section_match = CHOICES_SECTION_RE.search(body)
    if section_match:
        body = body[: section_match.start()].strip()
    return strip_hooks(body)


# ---------------------------------------------------------------------------
# Hook translation — Sugarcube
# ---------------------------------------------------------------------------

WARNINGS: list[str] = []


def translate_hook_sugarcube(hook: dict) -> str:
    """Translate a mechanic hook to Sugarcube macro syntax."""
    t = hook["type"]
    p = hook["params"]

    if t in TIER2_HOOKS:
        _warn(f"Tier 2 hook [{t}] — exports as stub (unsupported in Sugarcube)")
        return f"/* UNSUPPORTED HOOK: {t} — {p} */"

    if t == "FLAG":
        var = p.get("variable", p.get("var", ""))
        value = p.get("value", "true")
        return f"<<set ${_clean_var(var)} to {value}>>"

    if t == "COUNTER":
        var = p.get("variable", p.get("var", ""))
        delta = p.get("delta", p.get("change", "1"))
        op = p.get("op", "add")
        if op == "set":
            return f"<<set ${_clean_var(var)} to {delta}>>"
        return f"<<set ${_clean_var(var)} += {delta}>>"

    if t == "VISITED":
        var = p.get("variable", p.get("var", ""))
        return f"<<set ${_clean_var(var)} to true>>"

    if t == "INVENTORY":
        # Hook syntax: [MECHANIC:INVENTORY add=item_var] / remove=item_var / check=item_var
        item = p.get("add") or p.get("remove") or p.get("check") or p.get("item", "")
        if "add" in p:
            return f"<<set $inv_{_clean_var(item)} to true>>"
        if "remove" in p:
            return f"<<set $inv_{_clean_var(item)} to false>>"
        if "check" in p:
            return f"<<if $inv_{_clean_var(item)}>>"
        _warn(f"INVENTORY hook: missing add=/remove=/check= parameter")
        return f"/* INVENTORY: missing add/remove/check parameter */"

    if t == "TRUST":
        npc = p.get("npc", "")
        delta = p.get("delta", "0")
        sign = "+" if not str(delta).startswith("-") else ""
        return f"<<set $trust_{_clean_var(npc)} to Math.clamp($trust_{_clean_var(npc)} {sign} {delta}, 0, 100)>>"

    if t == "CURRENCY":
        var = p.get("variable", p.get("var", ""))
        if not var:
            print(
                f"ERROR: MECHANIC:CURRENCY is missing variable= — add the currency variable name.",
                file=sys.stderr,
            )
            sys.exit(1)
        delta = p.get("delta", "0")
        return f"<<set ${_clean_var(var)} += {delta}>>"

    if t == "NPC_STATE":
        npc = p.get("npc", "")
        state = p.get("set", p.get("state", ""))  # hook syntax uses set=
        return f"<<set $npc_{_clean_var(npc)}_state to \"{state}\">>"

    if t == "ENDING_CONDITION":
        var = p.get("variable", p.get("var", ""))
        delta = p.get("delta", "1")
        sign = "+" if not str(delta).startswith("-") else ""
        return f"<<set ${_clean_var(var)} to ${_clean_var(var)} {sign} {delta}>>"

    if t == "TIMER":
        timer_type = p.get("type", "turns")
        if timer_type == "seconds":
            _warn(
                "TIMER hook with type=seconds: Sugarcube requires a custom JS widget. "
                "Export emits a stub comment — implement widget separately."
            )
            return (
                f"/* TIMER (seconds): requires JS widget — "
                f"duration={p.get('duration', '?')} var={p.get('variable', '?')} "
                f"on_expire={p.get('on_expire', '?')} */"
            )
        # Turn-based timer: implemented as counter
        var = p.get("variable", "timer")
        duration = p.get("duration", "10")
        return f"<<set ${_clean_var(var)} to {duration}>>"

    if t == "RANDOM":
        var = p.get("variable", p.get("var", ""))
        min_val = p.get("min", "1")
        max_val = p.get("max", "10")
        return f"<<set ${_clean_var(var)} to random({min_val}, {max_val})>>"

    if t == "CHOICE_MEMORY":
        var = p.get("variable", p.get("var", ""))
        value = p.get("value", "")
        return f'<<set ${_clean_var(var)} to "{value}">>'

    if t == "CLUE":
        clue_id = p.get("add") or p.get("check") or p.get("variable", "")
        if "add" in p:
            return f"<<set $clue_{_clean_var(clue_id)} to true>>"
        if "check" in p:
            return f"<<if $clue_{_clean_var(clue_id)}>>"
        return f"<<set $clue_{_clean_var(clue_id)} to true>>"

    _warn(f"Unknown hook type: {t}")
    return f"/* UNKNOWN HOOK: {t} — {p} */"


# ---------------------------------------------------------------------------
# Hook translation — Ink
# ---------------------------------------------------------------------------


def translate_hook_ink(hook: dict) -> str:
    """Translate a mechanic hook to Ink syntax."""
    t = hook["type"]
    p = hook["params"]

    if t in TIER2_HOOKS:
        _warn(f"Tier 2 hook [{t}] — exports as stub (unsupported in Ink)")
        return f"// UNSUPPORTED HOOK: {t} — {p}"

    if t == "FLAG":
        var = p.get("variable", p.get("var", ""))
        value = p.get("value", "true")
        ink_val = "true" if value.lower() in ("true", "1", "yes") else "false"
        return f"~ {_clean_var(var)} = {ink_val}"

    if t == "COUNTER":
        var = p.get("variable", p.get("var", ""))
        delta = p.get("delta", p.get("change", "1"))
        op = p.get("op", "add")
        if op == "set":
            return f"~ {_clean_var(var)} = {delta}"
        try:
            d = int(delta)
        except ValueError:
            return f"~ {_clean_var(var)} += {delta}"
        if d >= 0:
            return f"~ {_clean_var(var)} += {d}"
        return f"~ {_clean_var(var)} -= {abs(d)}"

    if t == "VISITED":
        var = p.get("variable", p.get("var", ""))
        return f"~ {_clean_var(var)} = true"

    if t == "INVENTORY":
        # Hook syntax: [MECHANIC:INVENTORY add=item_var] / remove=item_var / check=item_var
        item = p.get("add") or p.get("remove") or p.get("check") or p.get("item", "")
        item_var = f"inv_{_clean_var(item)}"
        if "add" in p:
            return f"~ {item_var} = true"
        if "remove" in p:
            return f"~ {item_var} = false"
        if "check" in p:
            return f"// INVENTORY CHECK: {item_var} — implement conditional in Ink with {{ {item_var}: }}"
        _warn(f"INVENTORY hook: missing add=/remove=/check= parameter")
        return f"// INVENTORY: missing add/remove/check parameter"

    if t == "TRUST":
        npc = p.get("npc", "")
        delta = p.get("delta", "0")
        var = f"trust_{_clean_var(npc)}"
        try:
            d = int(delta)
        except ValueError:
            return f"~ {var} += {delta}"
        if d >= 0:
            return f"~ {var} += {d}"
        return f"~ {var} -= {abs(d)}"

    if t == "CURRENCY":
        var = p.get("variable", p.get("var", ""))
        delta = p.get("delta", "0")
        try:
            d = int(delta)
        except ValueError:
            return f"~ {_clean_var(var)} += {delta}"
        if d >= 0:
            return f"~ {_clean_var(var)} += {d}"
        return f"~ {_clean_var(var)} -= {abs(d)}"

    if t == "NPC_STATE":
        npc = p.get("npc", "")
        state = p.get("set", p.get("state", ""))  # hook syntax uses set=
        # Ink: NPC states as integer enum
        state_map = {"alive": 0, "dead": 1, "hostile": 2, "absent": 3}
        int_val = state_map.get(state.lower(), 0)
        _warn(
            f"NPC_STATE hook: state '{state}' mapped to integer {int_val} in Ink. "
            f"Ensure VAR npc_{_clean_var(npc)}_state is declared as INT."
        )
        return f"~ npc_{_clean_var(npc)}_state = {int_val}"

    if t == "ENDING_CONDITION":
        var = p.get("variable", p.get("var", ""))
        delta = p.get("delta", "1")
        try:
            d = int(delta)
        except ValueError:
            return f"~ {_clean_var(var)} += {delta}"
        if d >= 0:
            return f"~ {_clean_var(var)} += {d}"
        return f"~ {_clean_var(var)} -= {abs(d)}"

    if t == "TIMER":
        timer_type = p.get("type", "turns")
        if timer_type == "seconds":
            _warn(
                "TIMER hook with type=seconds: Ink has no real-time timer support. "
                "Export emits a turn-based counter stub."
            )
        var = p.get("variable", "timer")
        duration = p.get("duration", "10")
        return f"~ {_clean_var(var)} = {duration}"

    if t == "RANDOM":
        var = p.get("variable", p.get("var", ""))
        min_val = p.get("min", "1")
        max_val = p.get("max", "10")
        return f"~ {_clean_var(var)} = RANDOM({min_val}, {max_val})"

    if t == "CHOICE_MEMORY":
        var = p.get("variable", p.get("var", ""))
        value = p.get("value", "")
        # Ink has no string variables — emit a CONST mapping comment
        const_name = re.sub(r"[^A-Z0-9_]", "_", value.upper())
        _warn(
            f"CHOICE_MEMORY '{var}' = '{value}': Ink requires an integer CONST. "
            f"Add 'CONST {const_name} = N' to the knot and replace string with integer."
        )
        return (
            f"// CHOICE_MEMORY mapping: CONST {const_name} = N (assign integer value)\n"
            f"~ {_clean_var(var)} = {const_name}  // replace with integer CONST value"
        )

    if t == "CLUE":
        clue_id = p.get("add") or p.get("check") or p.get("variable", "")
        clue_var = f"clue_{_clean_var(clue_id)}"
        if "add" in p:
            return f"~ {clue_var} = true"
        if "check" in p:
            return f"// CLUE CHECK: {clue_var} — implement conditional in Ink with {{ {clue_var}: }}"
        return f"~ {clue_var} = true"

    if t == "CURRENCY":
        var = p.get("variable", p.get("var", ""))
        if not var:
            print(
                "ERROR: MECHANIC:CURRENCY is missing variable= — add the currency variable name.",
                file=sys.stderr,
            )
            sys.exit(1)
        delta = p.get("delta", "0")
        try:
            d = int(delta)
        except ValueError:
            return f"~ {_clean_var(var)} += {delta}"
        if d >= 0:
            return f"~ {_clean_var(var)} += {d}"
        return f"~ {_clean_var(var)} -= {abs(d)}"

    _warn(f"Unknown hook type: {t}")
    return f"// UNKNOWN HOOK: {t} — {p}"


# ---------------------------------------------------------------------------
# Hook translation — Escoria
# ---------------------------------------------------------------------------


def translate_hook_escoria(hook: dict) -> str:
    """Translate a mechanic hook to Escoria (.esc) syntax."""
    t = hook["type"]
    p = hook["params"]

    if t == "MOVE":
        actor = p.get("actor", "PLAYER")
        target = p.get("target", "")
        return f":walk {actor} {target}"

    if t == "VERB":
        verb_type = p.get("type", "examine")
        return f"> [{verb_type}]"

    if t == "AUDIO":
        trigger = p.get("trigger", "")
        action = p.get("action", "play")
        if action == "play":
            return f"snd_play {trigger}"
        return f"// AUDIO action={action} not mapped to Escoria command"

    if t == "HOTSPOT":
        hotspot_id = p.get("id", "")
        visibility = p.get("visibility", p.get("hi/re", ""))
        active_val = "true" if visibility in ("true", "revealed") else "false"
        return f"set_active {hotspot_id} {active_val}"

    if t == "INVENTORY":
        # Supports add/result=R
        item = p.get("add") or p.get("result") or p.get("item", "")
        if item:
            return f"inventory_add {item}"
        _warn("INVENTORY hook (Escoria): missing add= or result= parameter")
        return "// inventory_add ?"

    # Dialogue handling (optional for hook parser, but if passed as hook)
    if t == "SAY":
        actor = p.get("actor", "player")
        text = p.get("text", "")
        return f'say {actor} "{text}"'

    # Fallback for Tier 1 common hooks (translated to comments or best effort generic)
    if t == "FLAG":
        var = p.get("variable", p.get("var", ""))
        val = p.get("value", "true")
        return f"set_global {var} {val}"

    _warn(f"Hook [{t}] not natively mapped to Escoria — exported as comment stub.")
    return f"// {t}: {p}"


# ---------------------------------------------------------------------------
# Sugarcube emitter
# ---------------------------------------------------------------------------


def emit_sugarcube(
    nodes: list[dict],
    variables_path: str,
    game_title: str,
    stylesheet_path: str | None = None,
    script_path: str | None = None,
    interface_path: str | None = None,
) -> str:
    """Build full Twee 3 Sugarcube output string."""
    parts = []

    # Story title
    parts.append(f":: StoryTitle\n{game_title}\n")

    # StoryData — auto-generate a real IFID so every export is unique
    ifid = str(uuid.uuid4()).upper()
    parts.append(
        f':: StoryData\n{{\n  "ifid": "{ifid}",\n'
        '  "format": "SugarCube",\n  "format-version": "2.36.1",\n'
        '  "start": "' + (nodes[0]["node_id"] if nodes else "Start") + '"\n}\n'
    )

    # Stylesheet
    if stylesheet_path:
        if not os.path.exists(stylesheet_path):
            _warn(f"Stylesheet not found: '{stylesheet_path}' — skipping.")
        else:
            css = Path(stylesheet_path).read_text(encoding="utf-8")
            parts.append(f":: Stylesheet [stylesheet]\n{css}\n")

    # StoryScript (custom JavaScript)
    if script_path:
        if not os.path.exists(script_path):
            _warn(f"Script not found: '{script_path}' — skipping.")
        else:
            js = Path(script_path).read_text(encoding="utf-8")
            parts.append(f":: StoryScript [script]\n{js}\n")

    # StoryInterface (custom save/load UI HTML)
    if interface_path:
        if not os.path.exists(interface_path):
            _warn(f"Interface not found: '{interface_path}' — skipping.")
        else:
            html = Path(interface_path).read_text(encoding="utf-8")
            parts.append(f":: StoryInterface [nobreak]\n{html}\n")

    # StoryInit — variable initialisation from variables.md
    init_vars = _extract_variable_inits_sc(variables_path)
    if init_vars:
        parts.append(":: StoryInit\n" + "\n".join(init_vars) + "\n")

    # Node passages
    for node in nodes:
        passage_name = node["title"] or node["node_id"]
        tags = f"[act-{node['act']}]" if node.get("act") else ""
        parts.append(f":: {passage_name} {tags}\n")

        prose = extract_prose(node["body"])
        parts.append(prose + "\n\n")

        # Mechanic hooks
        hooks = parse_hooks(node["body"])
        for hook in hooks:
            translated = translate_hook_sugarcube(hook)
            if translated:
                parts.append(translated + "\n")

        # Choices
        choices = parse_choices(node["body"])
        if choices:
            parts.append("\n")
            for choice in choices:
                target = choice["target"]
                label = choice["label"]
                cond = choice.get("condition")
                if cond:
                    parts.append(f'<<if {cond}>>[[{label}|{target}]]<</if>>\n')
                else:
                    parts.append(f"[[{label}|{target}]]\n")

        parts.append("\n")

    return "\n".join(parts)


# Known variable types in variables.md
_KNOWN_TYPES = {
    "visited", "flag", "counter", "inventory", "trust", "currency",
    "string", "npc_state", "ending_condition", "timer", "clue",
    "choice_memory", "random",
}
_KNOWN_SCOPES = {"global", "session", "branch"}
_SKIP_CELLS = {"-", "—", "n/a", "variable", "item variable", "default",
               "type", "scope", "range", "description", "---", ""}


def _is_variable_row(cells: list[str]) -> bool:
    """Return True if this table row looks like a variable declaration."""
    if len(cells) < 3:
        return False
    name = cells[0].lower()
    if name in _SKIP_CELLS or name.startswith("-"):
        return False
    # Must have a known type in column 1
    return cells[1].lower().strip("`") in _KNOWN_TYPES


def _default_col(cells: list[str]) -> str:
    """
    Find the Default value in a table row.
    All variable table headers put Default at index 3. Skip backtick-wrapped
    export names (they start/end with backtick).
    """
    if len(cells) > 3:
        val = cells[3].strip().strip("`")
        if val.lower() not in _SKIP_CELLS:
            return val
    return ""


def _extract_variable_inits_sc(variables_path: str) -> list[str]:
    """
    Parse variables.md and return a list of <<set $var to default>> lines.
    Detects variable rows by checking for a known type in column 1.
    """
    if not os.path.exists(variables_path):
        _warn(f"variables.md not found at '{variables_path}' — StoryInit will be empty.")
        return []

    text = Path(variables_path).read_text(encoding="utf-8")
    inits = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not _is_variable_row(cells):
            continue
        var_name = _clean_var(cells[0])
        default_val = _default_col(cells)
        if not default_val:
            continue
        if default_val.lower() in ("true", "false"):
            inits.append(f"<<set ${var_name} to {default_val.lower()}>>")
        elif _is_int(default_val):
            inits.append(f"<<set ${var_name} to {default_val}>>")
        else:
            inits.append(f'<<set ${var_name} to "{default_val}">>')
    return inits


# ---------------------------------------------------------------------------
# Ink emitter
# ---------------------------------------------------------------------------


def emit_ink(nodes: list[dict], variables_path: str, _game_title: str) -> str:
    """Build full Ink output string."""
    parts = []

    # VAR declarations
    var_decls = _extract_variable_inits_ink(variables_path)
    if var_decls:
        parts.extend(var_decls)
        parts.append("")

    # Node knots
    for node in nodes:
        knot_name = _to_ink_knot_name(node["node_id"])
        parts.append(f"=== {knot_name} ===")

        prose = extract_prose(node["body"])
        parts.append(prose)
        parts.append("")

        # Mechanic hooks
        hooks = parse_hooks(node["body"])
        for hook in hooks:
            translated = translate_hook_ink(hook)
            if translated:
                parts.append(translated)

        # Choices
        choices = parse_choices(node["body"])
        if choices:
            parts.append("")
            for choice in choices:
                target_knot = _to_ink_knot_name(choice["target"])
                label = choice["label"]
                cond = choice.get("condition")
                if cond:
                    # Ink conditional option: condition must be inline on the option line
                    parts.append(f"* {{{cond}}} [{label}] -> {target_knot}")
                else:
                    parts.append(f"* [{label}] -> {target_knot}")
            # Gather point: required for any post-choice flow; with ->divert options
            # each option already diverts, so a bare gather acts as unreachable safety net
            parts.append("- -> END  // safety gather: each option above must divert")
        else:
            # Terminal node — end
            parts.append("-> END")

        parts.append("")

    return "\n".join(parts)


def _extract_variable_inits_ink(variables_path: str) -> list[str]:
    """Parse variables.md and return Ink VAR declaration lines."""
    if not os.path.exists(variables_path):
        _warn(f"variables.md not found at '{variables_path}' — no VAR declarations emitted.")
        return []

    text = Path(variables_path).read_text(encoding="utf-8")
    decls = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not _is_variable_row(cells):
            continue
        var_name = _clean_var(cells[0])
        var_type = cells[1].lower().strip("`")
        default_val = _default_col(cells)
        if not default_val:
            continue
        if var_type == "npc_state":
            decls.append(f"VAR {var_name} = 0  // integer enum: 0=alive 1=dead 2=hostile 3=absent")
        elif default_val.lower() in ("true", "false"):
            decls.append(f"VAR {var_name} = {default_val.lower()}")
        elif _is_int(default_val):
            decls.append(f"VAR {var_name} = {default_val}")
        else:
            # Ink has no string type — emit as 0 with a comment
            _warn(f"Variable '{var_name}' has string default '{default_val}' — Ink has no string type; declared as 0. Use CHOICE_MEMORY integer mapping.")
            decls.append(f"VAR {var_name} = 0  // string variable; use integer CONST mapping")
    return decls


# ---------------------------------------------------------------------------
# Escoria emitter
# ---------------------------------------------------------------------------


def emit_escoria(nodes: list[dict], _variables_path: str, _game_title: str) -> str:
    """Build full Escoria (.esc) output string."""
    parts = []

    for node in nodes:
        # Node ID header
        parts.append(f"// --- NODE: {node['node_id']} ---")

        # In Escoria, dialogue usually looks like `say [actor] "text"`
        # We'll try to parse the prose lines to wrap them in `say` if they look like dialogue
        # Or just emit the prose as comments if it's mostly descriptive.
        # But per the requirement, we should handle standard dialogue.
        # "say [actor_id] \"text\"" should be handled.

        prose = extract_prose(node["body"])
        for line in prose.splitlines():
            line = line.strip()
            if not line:
                continue

            # Check for dialogue pattern: Actor Name: "Dialogue text" or Actor Name: Dialogue text
            dialogue_match = re.match(r"^([^:]+):\s*(.*)$", line)
            if dialogue_match:
                actor = _to_ink_knot_name(dialogue_match.group(1))
                text = dialogue_match.group(2).strip('"')
                parts.append(f'say {actor} "{text}"')
            else:
                # Descriptive prose as comments or just raw (Escoria usually uses commands)
                parts.append(f"// {line}")

        # Mechanic hooks
        hooks = parse_hooks(node["body"])
        for hook in hooks:
            translated = translate_hook_escoria(hook)
            if translated:
                parts.append(translated)

        # Choices in Escoria use `?` syntax for questions/menus
        choices = parse_choices(node["body"])
        if choices:
            parts.append("?")
            for choice in choices:
                target_node = choice["target"]
                label = choice["label"]
                # Escoria question syntax: - Label: set_scene target_node
                parts.append(f"    - {label}: set_scene {target_node}")
            parts.append("!")

        parts.append("")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def _clean_var(name: str) -> str:
    """Normalise a variable name: strip $, replace spaces/hyphens with underscores."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", name.lstrip("$")).strip("_")


def _to_ink_knot_name(node_id: str) -> str:
    """Convert a node ID to a valid Ink knot name (lowercase, underscores)."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", node_id).lower().strip("_")


def _is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def _warn(message: str) -> None:
    WARNINGS.append(message)
    print(f"WARNING: {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Game title extraction
# ---------------------------------------------------------------------------


def get_game_title(game_bible_path: str) -> str:
    """Extract game title from constitution.md frontmatter or first heading."""
    if not os.path.exists(game_bible_path):
        return "game"
    text = Path(game_bible_path).read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    if meta.get("title"):
        return meta["title"]
    # Fallback: first H1 heading
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "game"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export speckit game-narrative-writing nodes to engine formats."
    )
    parser.add_argument(
        "--target",
        choices=["sugarcube", "ink", "escoria", "both"],
        required=True,
        help="Export target engine format.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR}/).",
    )
    parser.add_argument(
        "--nodes",
        default=NODES_DIR,
        help=f"Nodes directory (default: {NODES_DIR}/).",
    )
    parser.add_argument(
        "--variables",
        default=VARIABLES_FILE,
        help=f"Variables file path (default: {VARIABLES_FILE}).",
    )
    parser.add_argument(
        "--bible",
        default=CONSTITUTION_FILE,
        help=f"Constitution file path (default: {CONSTITUTION_FILE}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report warnings without writing output files.",
    )
    parser.add_argument(
        "--act",
        type=int,
        default=None,
        help="Export only nodes from the specified act number.",
    )
    parser.add_argument(
        "--stylesheet",
        default=None,
        metavar="CSS",
        help="Path to a CSS file; emitted as :: Stylesheet [stylesheet] (Sugarcube only).",
    )
    parser.add_argument(
        "--script",
        default=None,
        metavar="JS",
        help="Path to a JS file; emitted as :: StoryScript [script] (Sugarcube only).",
    )
    parser.add_argument(
        "--interface",
        default=None,
        metavar="HTML",
        help="Path to an HTML file; emitted as :: StoryInterface [nobreak] for custom save/load UI (Sugarcube only).",
    )
    args = parser.parse_args()

    # Load nodes
    nodes = load_nodes(args.nodes)
    if not nodes:
        print("ERROR: No APPROVED nodes found. Nothing to export.", file=sys.stderr)
        sys.exit(1)

    # Filter by act if requested
    if args.act is not None:
        nodes = [n for n in nodes if str(n.get("act", "")) == str(args.act)]
        if not nodes:
            print(f"ERROR: No APPROVED nodes found for act {args.act}.", file=sys.stderr)
            sys.exit(1)
        print(f"Act filter: exporting act {args.act} only.")

    print(f"Loaded {len(nodes)} APPROVED nodes.")

    game_title = get_game_title(args.bible)
    safe_title = re.sub(r"[^a-zA-Z0-9_\-]", "_", game_title).lower()

    output_files = []

    # Sugarcube export
    if args.target in ("sugarcube", "both"):
        content = emit_sugarcube(
            nodes,
            args.variables,
            game_title,
            stylesheet_path=args.stylesheet,
            script_path=args.script,
            interface_path=args.interface,
        )
        out_file = os.path.join(args.output, f"{safe_title}.twee")
        if not args.dry_run:
            os.makedirs(args.output, exist_ok=True)
            Path(out_file).write_text(content, encoding="utf-8")
            output_files.append(out_file)
            print(f"Sugarcube output written: {out_file}")

    # Ink export
    if args.target in ("ink", "both"):
        content = emit_ink(nodes, args.variables, game_title)
        out_file = os.path.join(args.output, f"{safe_title}.ink")
        if not args.dry_run:
            os.makedirs(args.output, exist_ok=True)
            Path(out_file).write_text(content, encoding="utf-8")
            output_files.append(out_file)
            print(f"Ink output written: {out_file}")

    # Escoria export
    if args.target in ("escoria", "both"):
        content = emit_escoria(nodes, args.variables, game_title)
        out_file = os.path.join(args.output, f"{safe_title}.esc")
        if not args.dry_run:
            os.makedirs(args.output, exist_ok=True)
            Path(out_file).write_text(content, encoding="utf-8")
            output_files.append(out_file)
            print(f"Escoria output written: {out_file}")

    # Summary
    print(f"\nExport complete: {len(nodes)} nodes, {len(WARNINGS)} warning(s).")
    if WARNINGS:
        print("\nWarnings:")
        for i, w in enumerate(WARNINGS, 1):
            print(f"  {i}. {w}")

    if args.dry_run:
        print("\nDry run — no files written.")
    else:
        print(f"\nOutput files: {', '.join(output_files)}")


if __name__ == "__main__":
    main()
