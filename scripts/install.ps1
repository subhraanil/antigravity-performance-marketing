# PowerShell One-Click Installer for Antigravity Performance Marketing Skill & Knowledge
# Run on any Windows PC: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Installing Antigravity Performance Marketing Operating System" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$userHome = $env:USERPROFILE
$geminiConfigDir = Join-Path $userHome ".gemini\config\skills\performance-marketing"
$geminiKnowledgeDir = Join-Path $userHome ".gemini\antigravity\knowledge"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot

# 1. Install Skill globally
Write-Host "[1/3] Installing Performance Marketing Skill to $geminiConfigDir..." -ForegroundColor Yellow
if (-not (Test-Path $geminiConfigDir)) {
    New-Item -ItemType Directory -Force -Path $geminiConfigDir | Out-Null
}
Copy-Item -Path "$repoRoot\SKILL.md" -Destination "$geminiConfigDir\SKILL.md" -Force
Copy-Item -Path "$repoRoot\knowledge" -Destination "$geminiConfigDir\" -Recurse -Force
Copy-Item -Path "$repoRoot\rules" -Destination "$geminiConfigDir\" -Recurse -Force
Copy-Item -Path "$repoRoot\subagents" -Destination "$geminiConfigDir\" -Recurse -Force
Copy-Item -Path "$repoRoot\templates" -Destination "$geminiConfigDir\" -Recurse -Force
Copy-Item -Path "$repoRoot\workflows" -Destination "$geminiConfigDir\" -Recurse -Force

# 2. Populate Knowledge Base
Write-Host "[2/3] Installing Knowledge Base to $geminiKnowledgeDir..." -ForegroundColor Yellow
if (-not (Test-Path $geminiKnowledgeDir)) {
    New-Item -ItemType Directory -Force -Path $geminiKnowledgeDir | Out-Null
}
Copy-Item -Path "$repoRoot\knowledge\*.md" -Destination "$geminiKnowledgeDir\" -Force

# 3. Configure Global Rules (GEMINI.md & AGENTS.md)
Write-Host "[3/3] Configuring Global Rules in ~/.gemini..." -ForegroundColor Yellow
$geminiGlobalMd = Join-Path $userHome ".gemini\GEMINI.md"
$agentsGlobalMd = Join-Path $userHome ".gemini\AGENTS.md"
Copy-Item -Path "$repoRoot\rules\GEMINI.md" -Destination $geminiGlobalMd -Force
Copy-Item -Path "$repoRoot\rules\AGENTS.md" -Destination $agentsGlobalMd -Force

Write-Host ""
Write-Host "SUCCESS! The Performance Marketing Skill and Knowledge Base are installed." -ForegroundColor Green
Write-Host "Antigravity will automatically load the skill and rules in any conversation." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
