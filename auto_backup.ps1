# Obsidian Vault Daily Auto-Backup Script
$vaultPath = $PSScriptRoot
Set-Location -Path $vaultPath
$status = git status --porcelain
if ($status) {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    git add .
    git commit -m "Auto backup: $date"
    git push origin main
}
