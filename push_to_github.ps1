<#
Simple helper script to initialize a local git repo and provide commands to push to GitHub.
You still need to create the remote repo on GitHub and set the remote URL below.
#>

if (-not (Test-Path .git)) {
    git init
    git add .
    git commit -m "Initial commit"
}

Write-Host "Repository initialized locally. To push to GitHub, run these commands:" -ForegroundColor Cyan
Write-Host "git remote add origin https://github.com/<your-username>/<your-repo>.git" -ForegroundColor Yellow
Write-Host "git branch -M main" -ForegroundColor Yellow
Write-Host "git push -u origin main" -ForegroundColor Yellow
