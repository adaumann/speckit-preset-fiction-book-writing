"""
test_nodes.py — Speckit Game Narrative Unit Test Suite
Runs cross-node integrity checks across all drafted nodes in a project.

Usage:
    python test_nodes.py [--nodes-dir <path>] [--specs-dir <path>] [--target <engine>]

All paths default to the standard speckit project layout relative to cwd.

Exit codes:
    0 = all tests passed
    1 = one or more tests failed
"""

import os
import sys
import re
import json
import glob
import argparse
import yaml

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_yaml_header(content):
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        return {}


def _load_variables_md(specs_dir):
    """Return set of declared variable names from specs/variables.md."""
    path = os.path.join(specs_dir, "variables.md")
    if not os.path.isfile(path):
        return None, f"specs/variables.md not found at {path}"
    content = _read(path)
    # Expect lines like: `$var_name` — description
    names = set(re.findall(r"`\$([a-zA-Z_]\w*)`", content))
    return names, None


def _load_plan_md(specs_dir):
    """Return set of node IDs from specs/plan.md."""
    path = os.path.join(specs_dir, "plan.md")
    if not os.path.isfile(path):
        return None, f"specs/plan.md not found at {path}"
    content = _read(path)
    node_ids = set(re.findall(r"\bNODE-\d+\b", content))
    return node_ids, None


def _collect_node_files(nodes_dir):
    patterns = ["*.md", "*.twee", "*.ink", "*.rpy", "*.esc", "*.asc", "*.yarn"]
    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(nodes_dir, p)))
    return sorted(files)


# ---------------------------------------------------------------------------
# Test definitions
# Each test function receives (nodes_data, variables, plan_node_ids)
# and returns a list of Failure dicts: {"test": str, "file": str, "detail": str}
# ---------------------------------------------------------------------------

def test_all_yaml_headers(nodes_data, *_):
    """Every node file must have a valid YAML header with required fields."""
    failures = []
    required = ("node_id", "title", "status", "drafted")
    for path, content, header in nodes_data:
        fname = os.path.basename(path)
        if not header:
            failures.append({"test": "YAML-HEADER", "file": fname,
                              "detail": "Missing or unparseable YAML front-matter."})
            continue
        for field in required:
            if field not in header:
                failures.append({"test": "YAML-HEADER", "file": fname,
                                  "detail": f"Missing required field: {field}"})
    return failures


def test_node_id_matches_filename(nodes_data, *_):
    """The node_id in the header must match the file stem."""
    failures = []
    for path, content, header in nodes_data:
        fname = os.path.basename(path)
        stem = os.path.splitext(fname)[0].upper()
        node_id = str(header.get("node_id", "")).upper()
        if node_id and node_id != stem:
            failures.append({"test": "ID-FILENAME", "file": fname,
                              "detail": f"node_id '{node_id}' does not match filename stem '{stem}'."})
    return failures


def test_variables_declared(nodes_data, variables, *_):
    """All variables referenced in MECHANIC hooks must be declared in variables.md."""
    if variables is None:
        return []
    failures = []
    var_pattern = re.compile(r"variable=(\$?[a-zA-Z_]\w*)")
    for path, content, header in nodes_data:
        fname = os.path.basename(path)
        for match in var_pattern.finditer(content):
            var = match.group(1).lstrip("$")
            if var not in variables:
                failures.append({"test": "VAR-DECLARED", "file": fname,
                                  "detail": f"Variable '{var}' used in hook but not declared in variables.md."})
    return failures


def test_choice_targets_in_plan(nodes_data, _, plan_node_ids):
    """All link targets in choices must reference node IDs present in plan.md."""
    if plan_node_ids is None:
        return []
    failures = []
    # Generic Markdown: [Label](NODE-NNN)
    md_link = re.compile(r"\[([^\]]+)\]\((NODE-\d+)\)")
    # Ink: -> node_name  (knot names are lowercased node IDs by convention)
    ink_jump = re.compile(r"->\s+(node_\d+|NODE_\d+|NODE-\d+)")
    # Ren'Py: jump NODE_NNN
    rpy_jump = re.compile(r"\bjump\s+(NODE_\d+|NODE-\d+)")

    for path, content, header in nodes_data:
        fname = os.path.basename(path)
        targets = set()
        for m in md_link.finditer(content):
            targets.add(m.group(2))
        for m in ink_jump.finditer(content):
            targets.add(m.group(1).replace("_", "-").upper())
        for m in rpy_jump.finditer(content):
            targets.add(m.group(1).replace("_", "-").upper())
        for target in targets:
            if target not in plan_node_ids:
                failures.append({"test": "CHOICE-TARGET", "file": fname,
                                  "detail": f"Choice target '{target}' not found in plan.md."})
    return failures


def test_no_dead_end_nodes(nodes_data, *_):
    """Non-terminal nodes must have at least one outgoing choice."""
    failures = []
    choice_patterns = [
        re.compile(r"^- \[", re.MULTILINE),       # generic
        re.compile(r"^\* \[", re.MULTILINE),       # ink
        re.compile(r"^\s{4}\"", re.MULTILINE),     # renpy menu option
        re.compile(r"-> END"),                     # ink terminal
        re.compile(r"\breturn\b"),                 # renpy return
        re.compile(r"\bset_scene\b"),              # escoria
    ]
    for path, content, header in nodes_data:
        fname = os.path.basename(path)
        if str(header.get("status", "")).upper() == "TERMINAL":
            continue
        has_choice = any(p.search(content) for p in choice_patterns)
        if not has_choice:
            failures.append({"test": "DEAD-END", "file": fname,
                              "detail": "No outgoing choices found and status is not TERMINAL."})
    return failures


def test_no_duplicate_node_ids(nodes_data, *_):
    """Every node_id must be unique across all drafted files."""
    seen = {}
    failures = []
    for path, content, header in nodes_data:
        fname = os.path.basename(path)
        nid = header.get("node_id")
        if not nid:
            continue
        if nid in seen:
            failures.append({"test": "DUPLICATE-ID", "file": fname,
                              "detail": f"node_id '{nid}' already used in {seen[nid]}."})
        else:
            seen[nid] = fname
    return failures


def test_mechanic_hook_syntax(nodes_data, *_):
    """MECHANIC hooks must be well-formed: [MECHANIC:TYPE key=value ...]"""
    failures = []
    bad_open = re.compile(r"\[MECHANIC:[^\]]*$", re.MULTILINE)
    for path, content, header in nodes_data:
        fname = os.path.basename(path)
        for line_num, line in enumerate(content.splitlines(), 1):
            if bad_open.search(line):
                failures.append({"test": "HOOK-SYNTAX", "file": fname,
                                  "detail": f"Line {line_num}: MECHANIC hook opened but not closed: {line.strip()}"})
    return failures


ALL_TESTS = [
    test_all_yaml_headers,
    test_node_id_matches_filename,
    test_variables_declared,
    test_choice_targets_in_plan,
    test_no_dead_end_nodes,
    test_no_duplicate_node_ids,
    test_mechanic_hook_syntax,
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Run unit tests across all drafted node files.")
    parser.add_argument("--nodes-dir", default="nodes", help="Path to the nodes/ directory.")
    parser.add_argument("--specs-dir", default="specs", help="Path to the specs/ directory.")
    parser.add_argument("--target", default="generic", help="Engine target (for context).")
    parser.add_argument("--json", action="store_true", help="Output results as JSON.")
    args = parser.parse_args()

    node_files = _collect_node_files(args.nodes_dir)
    if not node_files:
        msg = {"summary": "No node files found.", "failures": [], "passed": 0, "failed": 0}
        print(json.dumps(msg, indent=2) if args.json else "No node files found.")
        sys.exit(0)

    nodes_data = []
    for path in node_files:
        content = _read(path)
        header = _extract_yaml_header(content)
        nodes_data.append((path, content, header))

    variables, var_err = _load_variables_md(args.specs_dir)
    plan_node_ids, plan_err = _load_plan_md(args.specs_dir)

    all_failures = []
    for test_fn in ALL_TESTS:
        all_failures.extend(test_fn(nodes_data, variables, plan_node_ids))

    passed = len(ALL_TESTS) - len({f["test"] for f in all_failures})
    report = {
        "summary": f"{len(node_files)} node(s) tested | "
                   f"{len(all_failures)} failure(s) across {len({f['test'] for f in all_failures})} test(s)",
        "warnings": [w for w in [var_err, plan_err] if w],
        "failures": all_failures,
        "passed_tests": passed,
        "failed_tests": len({f["test"] for f in all_failures}),
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n=== Speckit Node Unit Tests ===")
        print(f"Nodes scanned : {len(node_files)}")
        print(f"Failures      : {len(all_failures)}")
        if report["warnings"]:
            print("\nWarnings:")
            for w in report["warnings"]:
                print(f"  ⚠  {w}")
        if all_failures:
            print("\nFailures:")
            for f in all_failures:
                print(f"  ✗ [{f['test']}] {f['file']}: {f['detail']}")
        else:
            print("\n  ✓ All structural tests passed.")
        print()

    sys.exit(0 if not all_failures else 1)


if __name__ == "__main__":
    main()
