# Build script for Szoftverfejlesztes Vizsgagyakarlo
# Output: dist\SzoftverfejlesztesVizsgagyakarlo.exe

Set-Location $PSScriptRoot

Write-Host "Building executable..." -ForegroundColor Cyan

pyinstaller `
    --noconfirm `
    --onefile `
    --windowed `
    --name "SzoftverfejlesztesVizsgagyakarlo" `
    --add-data "data\questions.json;data" `
    --collect-data customtkinter `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Executable: $PSScriptRoot\dist\SzoftverfejlesztesVizsgagyakarlo.exe" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: stats.json will be created next to the .exe on first run." -ForegroundColor Yellow
} else {
    Write-Host "Build FAILED (exit code $LASTEXITCODE)" -ForegroundColor Red
}
