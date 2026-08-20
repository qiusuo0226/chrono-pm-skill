#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Generic Qoder Skill distribution packer

.DESCRIPTION
    Packages any Qoder Skill project into a distribution zip.
    Includes ALL project files, excludes only known dev/build artifacts.
    Does NOT assume any skill-specific directory structure.

    Cross-platform reference implementation.
    Actual packaging on this machine uses pack.py (PowerShell execution policy restricted).

    v3.0.0（G-3）双包：仓库根打 Project 包时排除 ChronoPM-Portfolio/；
    Portfolio 包用 -SkillRoot <repo>/ChronoPM-Portfolio 单独打第二包。
    pack.py 在仓库根运行时自动依次打两包。

.PARAMETER SkillRoot
    Path to the Skill project root (where SKILL.md lives). Required.

.PARAMETER OutputDir
    Output directory for the zip. Defaults to SkillRoot.

.PARAMETER DryRun
    Preview only, do not create zip.

.PARAMETER Exclude
    Additional directory names to exclude (e.g. "docs","examples").

.EXAMPLE
    .\pack.ps1 -SkillRoot "C:\projects\my-skill" -DryRun
    .\pack.ps1 -SkillRoot "C:\projects\my-skill"
    .\pack.ps1 -SkillRoot "." -Exclude "docs","scratch"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillRoot,

    [string]$OutputDir,

    [switch]$DryRun,

    [string[]]$Exclude
)

$ErrorActionPreference = "Stop"

# ── Resolve paths ─────────────────────────────────────────
$SkillRoot = (Resolve-Path $SkillRoot).Path
if (-not $OutputDir) { $OutputDir = $SkillRoot }

# ── Validate Skill project ────────────────────────────────
$skillMd = Join-Path $SkillRoot "SKILL.md"
if (-not (Test-Path $skillMd)) {
    Write-Error "Not a Qoder Skill project: SKILL.md not found in $SkillRoot"
    exit 1
}

# ── Read version ──────────────────────────────────────────
$version = $null
$versionFile = Join-Path $SkillRoot "VERSION"
if (Test-Path $versionFile) {
    $version = (Get-Content $versionFile -Raw -Encoding UTF8).Trim()
}
if (-not $version) {
    $skillJsonPath = Join-Path $SkillRoot "skill.json"
    if (Test-Path $skillJsonPath) {
        $json = Get-Content $skillJsonPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $version = $json.version
    }
}
if (-not $version) {
    Write-Error "Cannot determine version: no VERSION file or skill.json version field"
    exit 1
}

# ── Read skill name + brand name ──────────────────────────
$skillName = "skill"
$brandName = $null
$skillJsonPath = Join-Path $SkillRoot "skill.json"
if (Test-Path $skillJsonPath) {
    $json = Get-Content $skillJsonPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($json.name) { $skillName = $json.name }
    # Extract brand name from displayName (text before first — or ()
    if ($json.displayName) {
        $brandName = ($json.displayName -split '[—\(]')[0].Trim()
    }
}
if (-not $brandName) {
    Write-Error "skill.json missing 'displayName' field. Cannot determine brand name — refusing to guess."
    exit 1
}

Write-Host "Detected: $skillName ($brandName) v$version at $SkillRoot"

# ── Exclusion rules ───────────────────────────────────────
# Directory names to always exclude (matched anywhere in path)
$excludeDirs = @(
    ".git",
    ".idea",
    ".vscode",
    ".qoder",
    "__pycache__",
    "governance",
    "tests",
    "tools",
    # v3.1.1（CR-G）：打包根已是 ChronoPM-Project/ 或 ChronoPM-Portfolio/，
    # 下列名称用于防误把兄弟目录/共享目录打进包
    "ChronoPM-Portfolio",
    "ChronoPM-Project",
    "governance-shared"
)
if ($Exclude) { $excludeDirs += $Exclude }

# Exception: files to INCLUDE even if parent dir is excluded
# Paths use forward slash; matched after normalizing \ → /
$includeExceptions = @(
    "governance/contracts/skill-contract.md",
    "governance/migrations/"
)

# File extensions to exclude
$excludeExts = @(".pyc", ".pyo")

# File names to exclude
$excludeFiles = @(
    ".DS_Store", "Thumbs.db", ".gitignore",
    "SKILL_BLUEPRINT.md"  # Architecture review doc — developer-side, not needed by PM users
)

# Specific file paths to exclude (matched by normalized relative path)
# Customize per project: these are ChronoPM-specific governance artifacts
$excludeFilePaths = @(
    "references/16-skill-governance-rules.md",  # Skill self-governance rules — developer-side process
    "source-split-skill/SKILL.md"  # 清单性文件，防宿主递归发现成第二 Skill
)

# ── Test function ─────────────────────────────────────────
function Test-Excluded {
    param([System.IO.FileInfo]$File)

    $rel = $File.FullName.Substring($SkillRoot.Length + 1)
    # Normalize path separators to forward slash for consistent matching
    $relNorm = $rel -replace '\\', '/'

    # Check exception list first (include even if parent dir is excluded).
    # Trailing "/" = directory prefix (CR-G: governance/migrations/ 当前 upgrade 入包)
    foreach ($exc in $includeExceptions) {
        if ($relNorm -eq $exc) { return $false }
        if ($exc.EndsWith("/")) {
            $prefix = $exc.TrimEnd("/")
            if ($relNorm -eq $prefix -or $relNorm.StartsWith("$prefix/")) { return $false }
        }
    }

    $parts = $relNorm -split '/'

    # Check directory segments against excludeDirs
    for ($i = 0; $i -lt $parts.Length - 1; $i++) {
        if ($excludeDirs -contains $parts[$i]) { return $true }
    }

    # Check file extension
    if ($excludeExts -contains $File.Extension.ToLower()) { return $true }

    # Check file name
    if ($excludeFiles -contains $File.Name) { return $true }

    # Check specific file paths
    foreach ($ep in $excludeFilePaths) {
        if ($relNorm -eq $ep) { return $true }
    }

    # Check archive extensions
    if ($File.Extension -eq ".zip" -or $File.Name -match "\.tar\.\w+$") { return $true }

    return $false
}

# ── Stage files ───────────────────────────────────────────
$stageName = "$brandName-Skill-v$version"
$stagePath = Join-Path ([System.IO.Path]::GetTempPath()) $stageName

if (Test-Path $stagePath) { Remove-Item $stagePath -Recurse -Force }
New-Item -ItemType Directory -Path $stagePath -Force | Out-Null

$allFiles = Get-ChildItem -Path $SkillRoot -Recurse -File | Where-Object { -not (Test-Excluded $_) }
$fileCount = 0

foreach ($item in $allFiles) {
    $rel = $item.FullName.Substring($SkillRoot.Length)
    $target = Join-Path $stagePath $rel
    $targetDir = Split-Path $target -Parent
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    Copy-Item $item.FullName -Destination $target
    $fileCount++
    if ($DryRun) { Write-Host "  + $rel" }
}

# ── DryRun output ─────────────────────────────────────────
if ($DryRun) {
    $stageSize = (Get-ChildItem $stagePath -Recurse -File | Measure-Object -Property Length -Sum).Sum
    Write-Host ""
    Write-Host "=== DRY RUN ==="
    Write-Host "Skill   : $skillName"
    Write-Host "Version : $version"
    Write-Host "Files   : $fileCount"
    Write-Host "Size    : $([math]::Round($stageSize / 1024, 1)) KB (uncompressed)"
    Write-Host "Output  : $(Join-Path $OutputDir "$stageName.zip")"
    Remove-Item $stagePath -Recurse -Force
    exit 0
}

# ── Create zip ────────────────────────────────────────────
$zipName = "$stageName.zip"
$zipPath = Join-Path $OutputDir $zipName
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

Compress-Archive -Path $stagePath -DestinationPath $zipPath -CompressionLevel Optimal

$zipSize = (Get-Item $zipPath).Length
$zipSizeKB = [math]::Round($zipSize / 1024, 1)

Remove-Item $stagePath -Recurse -Force

# ── Summary ───────────────────────────────────────────────
Write-Host ""
Write-Host "============================================"
Write-Host "  Skill Distribution Package"
Write-Host "============================================"
Write-Host "  Name    : $skillName"
Write-Host "  Version : $version"
Write-Host "  Files   : $fileCount"
Write-Host "  Zip size: $zipSizeKB KB"
Write-Host "  Output  : $zipPath"
Write-Host "============================================"
