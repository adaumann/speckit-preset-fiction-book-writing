#!/usr/bin/env bash
# Install required Python packages for the search index
# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv || python -m venv .venv
fi

# Determine the venv python executable
PYTHON_EXE="./.venv/bin/python"
if [ ! -f "$PYTHON_EXE" ]; then
    PYTHON_EXE="./.venv/Scripts/python.exe"
fi

# Install packages using the venv python
"$PYTHON_EXE" -m pip install --upgrade pip
"$PYTHON_EXE" -m pip install chromadb sentence-transformers rank-bm25
