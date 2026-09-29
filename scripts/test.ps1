$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
& docker compose exec -T -e RUN_DB_TESTS=1 api pytest -q
if ($LASTEXITCODE -ne 0) { throw 'Backend tests failed' }
Push-Location frontend
try { & npm.cmd run build; if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed' }; & npm.cmd run test:e2e; if ($LASTEXITCODE -ne 0) { throw 'Browser tests failed' } }
finally { Pop-Location }
