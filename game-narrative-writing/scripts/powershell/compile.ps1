# Compile drafted nodes to engine-specific output format
# Usage: compile.ps1 -Spec "001-forest-guardian" -Engine "sugarcube"
# Usage: compile.ps1 -Spec "001-forest-guardian" -AllEngines

param(
    [Parameter(Mandatory=$true)]
    [string]$Spec,
    
    [Parameter(Mandatory=$false)]
    [string]$Engine,
    
    [Parameter(Mandatory=$false)]
    [switch]$AllEngines,
    
    [Parameter(Mandatory=$false)]
    [string]$Output,
    
    [Parameter(Mandatory=$false)]
    [switch]$ForceRebuild,
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun,
    
    [Parameter(Mandatory=$false)]
    [int]$MaxIterations = 3
)

# Validate parameters
if (-not $Engine -and -not $AllEngines) {
    Write-Host "❌ Error: Either -Engine or -AllEngines must be specified" -ForegroundColor Red
    exit 1
}

if ($Engine -and $AllEngines) {
    Write-Host "❌ Error: Cannot specify both -Engine and -AllEngines" -ForegroundColor Red
    exit 1
}

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "compile.py"

# Build arguments
$PythonArgs = @(
    "`"$PythonScript`"",
    "--spec", "`"$Spec`""
)

if ($AllEngines) {
    $PythonArgs += "--all-engines"
} else {
    $PythonArgs += "--engine", $Engine
}

if ($Output) {
    $PythonArgs += "--output", "`"$Output`""
}

if ($ForceRebuild) {
    $PythonArgs += "--force-rebuild"
}

if ($DryRun) {
    $PythonArgs += "--dry-run"
}

Write-Host "🎮 Speckit Compiler (PowerShell wrapper)" -ForegroundColor Cyan
Write-Host "Spec: $Spec" -ForegroundColor Gray
if ($AllEngines) {
    Write-Host "Compiling all configured engines..." -ForegroundColor Gray
} else {
    Write-Host "Engine: $Engine" -ForegroundColor Gray
}

# Run Python compiler
& python @PythonArgs

exit $LASTEXITCODE
