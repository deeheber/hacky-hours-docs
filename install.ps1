$dest = "$env:USERPROFILE\.claude\commands\hacky-hours.md"
$src  = "https://raw.githubusercontent.com/empathetech/hacky-hours-docs/main/.claude/commands/hacky-hours-dev.md"

New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
Invoke-WebRequest -Uri $src -OutFile $dest
(Get-Content $dest) -replace '^(description:.+) \(dev\)$', '$1' | Set-Content $dest

Write-Host "Installed. Type /hacky-hours in any Claude Code session."
