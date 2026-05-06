$ErrorActionPreference = 'Stop'

$repo       = 'empathetech/hacky-hours-docs'
$branch     = if ($env:HH_BRANCH) { $env:HH_BRANCH } else { 'main' }
$devSubpath = '.claude\skills\hacky-hours-dev'
$skillName  = 'hacky-hours'
$skillsDir  = Join-Path $env:USERPROFILE '.claude\skills'
$dest       = Join-Path $skillsDir $skillName
$oldFile    = Join-Path $env:USERPROFILE '.claude\commands\hacky-hours.md'

$tmp = Join-Path $env:TEMP ("hacky-hours-install-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $tmp -Force | Out-Null

try {
    Write-Host "Downloading hacky-hours from $repo ($branch)..."
    $zipPath = Join-Path $tmp 'archive.zip'
    Invoke-WebRequest -Uri "https://github.com/$repo/archive/refs/heads/$branch.zip" -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath $tmp -Force

    # GitHub zip extracts to "$tmp\hacky-hours-docs-main\..." — find that top-level dir.
    $extracted = Get-ChildItem -Path $tmp -Directory |
        Where-Object { $_.Name -like 'hacky-hours-docs-*' } |
        Select-Object -First 1

    if (-not $extracted) {
        throw "Could not find extracted repo directory in $tmp"
    }

    $skillSrc = Join-Path $extracted.FullName $devSubpath
    if (-not (Test-Path $skillSrc)) {
        throw "Skill directory not found in repo archive at $devSubpath"
    }

    New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Move-Item -Path $skillSrc -Destination $dest

    # Transform SKILL.md from dev shape to installed shape:
    # - name: hacky-hours-dev -> hacky-hours
    # - description: "... (dev) vX.Y.Z" -> "... vX.Y.Z"
    $skillFile = Join-Path $dest 'SKILL.md'
    (Get-Content $skillFile) `
        -replace '^(name:\s*)hacky-hours-dev$', '${1}hacky-hours' `
        -replace '^(description:.+) \(dev\)$', '$1' `
        | Set-Content $skillFile

    # Clean up the v2.x single-file install if present.
    if (Test-Path $oldFile) {
        Remove-Item $oldFile
        Write-Host "Removed old v2.x slash command at $oldFile"
    }

    Write-Host "Installed at $dest"
    Write-Host "Restart Claude Code, then type /hacky-hours in any session."
} finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}
