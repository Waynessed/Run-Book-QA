param([ValidateSet('development','test')] [string]$Split='development',[switch]$Freeze,[switch]$AllowHeldOut)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$revision = & git -c safe.directory=D:/Projects/RunBookQA rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot record Git revision' }
if ($Split -eq 'test' -and -not $AllowHeldOut) { throw 'Test execution requires -AllowHeldOut and frozen configuration' }
if ($Freeze) {
    & docker compose exec -T -e "GIT_COMMIT=$revision" api python -m app.cli freeze
    if ($LASTEXITCODE -ne 0) { throw 'Freeze failed' }
}
$arguments = @('compose','exec','-T','-e',"GIT_COMMIT=$revision",'api','python','-m','app.cli','evaluate','--split',$Split)
if ($AllowHeldOut) { $arguments += '--allow-held-out' }
& docker @arguments
if ($LASTEXITCODE -ne 0) { throw 'Evaluation failed' }
