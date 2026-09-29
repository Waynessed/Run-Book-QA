$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
function Invoke-Checked { param([string[]]$Arguments)
    & docker @Arguments
    if ($LASTEXITCODE -ne 0) { throw "docker $Arguments failed ($LASTEXITCODE)" }
}
Invoke-Checked @('compose','up','-d','db','ollama')
for ($i = 0; $i -lt 60; $i++) {
    & docker compose exec -T ollama ollama list 2>$null
    if ($LASTEXITCODE -eq 0) { break }
    Start-Sleep -Seconds 2
}
Invoke-Checked @('compose','exec','-T','ollama','ollama','pull','qwen2.5:1.5b')
Invoke-Checked @('compose','up','-d','--build','api','web')
Invoke-Checked @('compose','exec','-T','api','python','-m','app.cli','models')
Invoke-Checked @('compose','exec','-T','api','python','-m','app.cli','ingest')
for ($i = 0; $i -lt 60; $i++) {
    try { $ready = Invoke-RestMethod http://127.0.0.1:8081/readyz; Write-Output $ready; break }
    catch { if ($i -eq 59) { throw }; Start-Sleep -Seconds 2 }
}
Write-Output 'Open http://127.0.0.1:5174. CPU generation can take up to 120 seconds.'
