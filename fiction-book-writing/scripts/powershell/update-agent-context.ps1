param(
    [Parameter(Mandatory=$true)]
    [string]$AgentType
)

# Minimal script to update agent context
Write-Host "Updating agent context for $AgentType..."
if (!(Test-Path ".specify/memory")) {
    New-Item -ItemType Directory -Force -Path ".specify/memory"
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] Agent context refreshed for $AgentType" | Out-File -FilePath ".specify/memory/agent-status.log" -Append
