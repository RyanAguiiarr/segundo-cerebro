# brain-sync.ps1 — Sync Tila_Brain to Git
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
Set-Location "c:\Tila\Tila_Brain"
git add .
git commit -m "sync: $timestamp"
git push
Write-Host "Tila_Brain synced at $timestamp"
