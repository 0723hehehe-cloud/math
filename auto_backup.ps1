# Obsidian Vault Daily Auto-Backup Script
Set-Location -Path "D:\ob\考研数学"
$status = git status --porcelain
if ($status) {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    git add .
    git commit -m "Auto backup: $date"
    git push origin main
}
