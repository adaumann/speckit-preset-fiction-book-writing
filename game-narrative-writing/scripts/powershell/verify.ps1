# Verify and validate drafted nodes
# Usage: verify.ps1 -Spec "001-forest-guardian" -Engine "sugarcube" -All

param(
    [Parameter(Mandatory=$true)]
    [string]$Spec,
    
    [Parameter(Mandatory=$true)]
    [string]$Engine,
    
    [Parameter(Mandatory=$false)]
    [switch]$All,
    
    [Parameter(Mandatory=$false)]
    [switch]$UnitTests,
    
    [Parameter(Mandatory=$false)]
    [switch]$StructuralOnly,
    
    [Parameter(Mandatory=$false)]
    [int]$MaxAttempts = 3
)

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "\..\python\verify.py"

# Build arguments
$PythonArgs = @(
    "`"$PythonScript`"",
    "--spec", "`"$Spec`"",
    "--engine", $Engine
)

if ($All) {
    $PythonArgs += "--all"
}

if ($UnitTests) {
    $PythonArgs += "--unit-tests"
}

if ($StructuralOnly) {
    $PythonArgs += "--structural-only"
}

if ($MaxAttempts -ne 3) {
    $PythonArgs += "--max-attempts", $MaxAttempts
}

Write-Host "🧪 Speckit Verifier (PowerShell wrapper)" -ForegroundColor Cyan
Write-Host "Spec: $Spec" -ForegroundColor Gray
Write-Host "Engine: $Engine" -ForegroundColor Gray

# Run Python verifier
& python @PythonArgs

exit $LASTEXITCODE
