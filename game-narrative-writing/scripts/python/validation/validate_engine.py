"""
validate_engine.py — Speckit Game Narrative Engine Validator
Runs compiler / linter checks on a drafted node file for the configured engine target.

Usage:
    python validate_engine.py <file_path> --target <engine>

Supported targets:
    generic, twine, ink, renpy, escoria, ags, unity

Exit codes:
    0  = validation passed
    1  = validation failed (errors in JSON on stdout)
    2  = toolchain not found (warning; not a hard failure by default)
"""

import sys
import subprocess
import json
import argparse
import os
import re
import yaml

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(cmd, **kwargs):
    """Run a subprocess and return (returncode, stdout, stderr)."""
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    return result.returncode, result.stdout, result.stderr


def _read(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_yaml_header(content):
    """Return parsed YAML front-matter dict or None."""
    if not content.startswith("---"):
        return None
    end = content.find("\n---", 3)
    if end == -1:
        return None
    try:
        return yaml.safe_load(content[3:end])
    except yaml.YAMLError:
        return None


# ---------------------------------------------------------------------------
# Structural / unit tests (engine-agnostic)
# ---------------------------------------------------------------------------

def structural_tests(content, file_path):
    """
    Run engine-agnostic structural unit tests on the raw file content.
    Returns a list of error strings (empty = all passed).
    """
    errors = []

    # T-01: YAML header presence
    header = _extract_yaml_header(content)
    if header is None:
        errors.append("[T-01] Missing or malformed YAML front-matter header.")
    else:
        for required_field in ("node_id", "title", "status", "drafted"):
            if required_field not in header:
                errors.append(f"[T-02] YAML header missing required field: {required_field}")

    # T-03: MECHANIC hook syntax — every opening tag must have a closing ]
    open_hooks = re.findall(r"\[MECHANIC:", content)
    close_hooks = re.findall(r"\[MECHANIC:[^\]]+\]", content)
    if len(open_hooks) != len(close_hooks):
        errors.append(f"[T-03] Malformed MECHANIC hook(s): {len(open_hooks)} opening tag(s), {len(close_hooks)} valid tag(s).")

    # T-04: CURRENCY hooks must include variable=
    for hook in re.findall(r"\[MECHANIC:CURRENCY[^\]]*\]", content):
        if "variable=" not in hook:
            errors.append(f"[T-04] CURRENCY hook missing variable=: {hook}")

    # T-05: RANDOM hooks must include min= and max=
    for hook in re.findall(r"\[MECHANIC:RANDOM[^\]]*\]", content):
        if "min=" not in hook or "max=" not in hook:
            errors.append(f"[T-05] RANDOM hook missing min= or max=: {hook}")

    # T-06: No dead-end nodes (at least one choice or END marker)
    has_choices = bool(
        re.search(r"^- \[", content, re.MULTILINE)    # generic Markdown choice
        or re.search(r"^\* \[", content, re.MULTILINE) # Ink choice
        or re.search(r"^\s+\"", content, re.MULTILINE) # Ren'Py menu option
        or re.search(r"-> END", content)               # Ink END
        or re.search(r"return\s*$", content, re.MULTILINE)  # Ren'Py return
        or header and header.get("status") == "TERMINAL"
    )
    if not has_choices:
        errors.append("[T-06] Node appears to be a dead-end: no choices, END marker, or TERMINAL status found.")

    return errors


# ---------------------------------------------------------------------------
# Engine-specific compiler / linter validators
# ---------------------------------------------------------------------------

def validate_ink(file_path, content):
    """Compile with inklecate (https://github.com/inkle/ink/releases)."""
    errors = structural_tests(content, file_path)
    try:
        rc, stdout, stderr = _run(["inklecate", "-p", file_path])
        if rc != 0:
            for line in stderr.splitlines():
                if line.strip():
                    errors.append(f"[INK] {line.strip()}")
        # inklecate may emit warnings on stdout even with rc=0
        for line in stdout.splitlines():
            if "WARNING" in line.upper() or "ERROR" in line.upper():
                errors.append(f"[INK-WARN] {line.strip()}")
    except FileNotFoundError:
        errors.append("[TOOLCHAIN] inklecate not found. Install from https://github.com/inkle/ink/releases")
    return errors


def validate_twine(file_path, content):
    """Compile with Tweego (https://www.motoslave.net/tweego/)."""
    errors = structural_tests(content, file_path)
    try:
        # Tweego compiles to HTML; -d flag is dry-run / dump mode
        rc, stdout, stderr = _run(["tweego", "--format=SugarCube-2", "--output=/dev/null", file_path])
        if rc != 0:
            for line in (stderr + stdout).splitlines():
                if line.strip():
                    errors.append(f"[TWEE] {line.strip()}")
    except FileNotFoundError:
        errors.append("[TOOLCHAIN] tweego not found. Install from https://www.motoslave.net/tweego/")
    return errors


def validate_renpy(file_path, content):
    """Lint via Ren'Py CLI. Requires renpy executable on PATH."""
    errors = structural_tests(content, file_path)
    # Additional Ren'Py-specific checks (static)
    if "label " not in content:
        errors.append("[RPY] No 'label' declaration found — every Ren'Py node must have a label.")
    if "menu:" in content:
        # Each menu block must have at least one option
        for block in re.findall(r"menu:(.*?)(?=\n\S|\Z)", content, re.DOTALL):
            options = re.findall(r'^\s+"', block, re.MULTILINE)
            if not options:
                errors.append("[RPY] Empty menu: block found — add at least one choice option.")
    project_dir = os.path.dirname(os.path.dirname(file_path))
    try:
        rc, stdout, stderr = _run(["renpy", project_dir, "lint"])
        if rc != 0:
            for line in stderr.splitlines():
                if line.strip():
                    errors.append(f"[RENPY] {line.strip()}")
    except FileNotFoundError:
        errors.append("[TOOLCHAIN] renpy not found. Add Ren'Py to PATH or set RENPY_PATH env var.")
    return errors


def validate_yarn(file_path, content):
    """Compile with Yarn Spinner CLI (https://github.com/YarnSpinnerTool/YarnSpinner-Console)."""
    errors = structural_tests(content, file_path)
    try:
        rc, stdout, stderr = _run(["ysc", "compile", file_path])
        if rc != 0:
            for line in (stderr + stdout).splitlines():
                if line.strip():
                    errors.append(f"[YARN] {line.strip()}")
    except FileNotFoundError:
        errors.append("[TOOLCHAIN] ysc (Yarn Spinner Console) not found. Install from https://github.com/YarnSpinnerTool/YarnSpinner-Console")
    return errors


def validate_unity_cs(file_path, content):
    """Compile C# with dotnet build (requires a .csproj in scope)."""
    errors = structural_tests(content, file_path)
    # Walk up to find a .csproj
    search = os.path.abspath(file_path)
    csproj = None
    for _ in range(5):
        search = os.path.dirname(search)
        candidates = [f for f in os.listdir(search) if f.endswith(".csproj")]
        if candidates:
            csproj = os.path.join(search, candidates[0])
            break
    if csproj:
        try:
            rc, stdout, stderr = _run(["dotnet", "build", csproj, "--nologo", "-v", "quiet"])
            if rc != 0:
                for line in (stderr + stdout).splitlines():
                    if "error" in line.lower() and line.strip():
                        errors.append(f"[CS] {line.strip()}")
        except FileNotFoundError:
            errors.append("[TOOLCHAIN] dotnet not found. Install .NET SDK from https://dotnet.microsoft.com/")
    else:
        errors.append("[CS] No .csproj found within 5 parent directories — cannot run dotnet build.")
    return errors


def validate_escoria(file_path, content):
    """Static checks for Escoria GDScript (.esc) files."""
    errors = structural_tests(content, file_path)
    # Escoria uses Godot CLI for full validation: godot --check-only
    if not re.search(r"^:", content, re.MULTILINE):
        errors.append("[ESC] No state/label declaration found (lines starting with ':').")
    try:
        rc, stdout, stderr = _run(["godot", "--check-only", "--script", file_path, "--headless"])
        if rc not in (0, 255):  # 255 = editor-not-needed warning, safe to ignore
            for line in (stderr + stdout).splitlines():
                if "ERROR" in line.upper() and line.strip():
                    errors.append(f"[GODOT] {line.strip()}")
    except FileNotFoundError:
        errors.append("[TOOLCHAIN] godot not found. Add Godot to PATH for full Escoria/GDScript validation.")
    return errors


def validate_ags(file_path, content):
    """Static checks for AGS script (.asc) files. AGS has no public CLI compiler."""
    errors = structural_tests(content, file_path)
    # Best-effort static checks
    if not re.search(r"function\s+\w+\s*\(", content):
        errors.append("[AGS] No function declaration found — AGS script files require at least one function.")
    open_braces = content.count("{")
    close_braces = content.count("}")
    if open_braces != close_braces:
        errors.append(f"[AGS] Brace mismatch: {open_braces} '{{' vs {close_braces} '}}'.")
    return errors


def validate_generic(file_path, content):
    """YAML header and hook syntax checks for generic Markdown nodes."""
    return structural_tests(content, file_path)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

TARGET_MAP = {
    "ink":     validate_ink,
    "twine":   validate_twine,
    "sugarcube": validate_twine,
    "renpy":   validate_renpy,
    "yarn":    validate_yarn,
    "unity":   validate_unity_cs,
    "escoria": validate_escoria,
    "ags":     validate_ags,
    "generic": validate_generic,
}


def main():
    parser = argparse.ArgumentParser(description="Validate a drafted game narrative node file.")
    parser.add_argument("file", help="Path to the node file to validate.")
    parser.add_argument("--target", required=True,
                        choices=list(TARGET_MAP.keys()),
                        help="Engine target.")
    parser.add_argument("--structural-only", action="store_true",
                        help="Only run structural unit tests; skip compiler/linter invocation.")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(json.dumps({"success": False, "errors": [f"File not found: {args.file}"]}))
        sys.exit(1)

    content = _read(args.file)

    if args.structural_only:
        errors = structural_tests(content, args.file)
    else:
        errors = TARGET_MAP[args.target](args.file, content)

    toolchain_warnings = [e for e in errors if e.startswith("[TOOLCHAIN]")]
    hard_errors = [e for e in errors if not e.startswith("[TOOLCHAIN]")]

    result = {
        "success": len(hard_errors) == 0,
        "errors": hard_errors,
        "warnings": toolchain_warnings,
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
