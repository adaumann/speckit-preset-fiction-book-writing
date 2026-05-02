#!/bin/bash
# Verify and validate drafted nodes
# Usage: bash verify.sh --spec <spec-name> --engine <engine> [--all]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/../python/verify.py"

SPEC=""
ENGINE=""
ALL=""
OPTIONS=""

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
        --all)
            ALL="--all"
            shift
            ;;
        --unit-tests)
            OPTIONS="$OPTIONS --unit-tests"
            shift
            ;;
        --structural-only)
            OPTIONS="$OPTIONS --structural-only"
            shift
            ;;
        --max-attempts)
            OPTIONS="$OPTIONS --max-attempts $2"
            shift 2
            ;;
        --json)
            # Ignored for compatibility
            shift
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z "$SPEC" ] || [ -z "$ENGINE" ]; then
    echo "Usage: $0 --spec <spec-name> --engine <engine> [--all]"
    exit 1
fi

python3 "$PYTHON_SCRIPT" --spec "$SPEC" --engine "$ENGINE" $ALL $OPTIONS
