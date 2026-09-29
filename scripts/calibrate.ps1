param()
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$revision = & git -c safe.directory=D:/Projects/RunBookQA rev-parse HEAD
& docker compose exec -T -e "GIT_COMMIT=$revision" api python -m app.cli calibrate
if ($LASTEXITCODE -ne 0) { throw 'Calibration failed' }
$calibration = Get-Content reports/calibration.json -Raw | ConvertFrom-Json
$config = Get-Content config/retrieval.json -Raw | ConvertFrom-Json
$config.threshold = $calibration.selected.threshold
$config | ConvertTo-Json | Set-Content config/retrieval.json
Write-Output $calibration.selected
