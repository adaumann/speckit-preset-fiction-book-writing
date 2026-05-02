#!/bin/bash
# Compile drafted nodes to engine-specific output format
# Usage: bash compile.sh --spec "001-forest-guardian" --engine "sugarcube" --output "./output"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/compile.py"

SPEC=""
ENGINE=""
OUTPUT=""
FORCE_REBUILD=""
DRY_RUN=""
MAX_ITERATIONS=3

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --spec)
            SPEC="$2"
            shift 2
            ;;
        --engine)
            ENGINE="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --force-rebuild)
            FORCE_REBUILD="--force-rebuild"
            shift
            ;;
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --json)
            # Ignored for compatibility
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "$SPEC" ] || [ -z "$ENGINE" ]; then
    echo "Usage: $0 --spec <spec-name> --engine <engine> [--output <path>]"
    exit 1
fi

echo "🎮 Speckit Compiler (Bash wrapper)"
echo "Spec: $SPEC"
echo "Engine: $ENGINE"

# Build Python command
PYTHON_CMD="python3 \"$PYTHON_SCRIPT\" --spec \"$SPEC\" --engine \"$ENGINE\""

if [ -n "$OUTPUT" ]; then
    PYTHON_CMD="$PYTHON_CMD --output \"$OUTPUT\""
fi

if [ -n "$FORCE_REBUILD" ]; then
    PYTHON_CMD="$PYTHON_CMD $FORCE_REBUILD"
fi

if [ -n "$DRY_RUN" ]; then
    PYTHON_CMD="$PYTHON_CMD $DRY_RUN"
fi

# Execute Python compiler
eval $PYTHON_CMD
exit $?
