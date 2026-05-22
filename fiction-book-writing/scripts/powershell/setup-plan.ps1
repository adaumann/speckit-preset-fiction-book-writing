param(
    [switch]$Json
)

# Install required Python packages for the search index
# Create virtual environment if it doesn't exist
if (!(Test-Path "./.venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Determine the venv python executable
$pythonExe = if (Test-Path "./.venv/Scripts/python.exe") { "./.venv/Scripts/python.exe" } else { "./.venv/bin/python" }

# Install packages using the venv python
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install chromadb sentence-transformers rank-bm25
