$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
for ($i=0; $i -lt 30; $i++) {
    try { Invoke-RestMethod http://127.0.0.1:8081/healthz | Out-Null; break }
    catch { if ($i -eq 29) { throw }; Start-Sleep -Seconds 1 }
}
$body = @{question='The API returns 401 after deployment. What should I check?';retrieval_mode='keyword'} | ConvertTo-Json
$answer = Invoke-RestMethod http://127.0.0.1:8081/v1/ask -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 250
$answer | ConvertTo-Json -Depth 20 | Set-Content ('reports/current-smoke-attempt-' + (Get-Date -Format yyyyMMddHHmmss) + '.json')
if ($answer.status -ne 'answered') { throw 'First supported answer abstained' }
$answer | ConvertTo-Json -Depth 20 | Set-Content reports/current-smoke-answer.json
foreach ($passage in $answer.passages) {
    $doc = Invoke-RestMethod ('http://127.0.0.1:8081/v1/documents/' + $passage.document_id)
    if ($doc.version -ne $passage.version) { throw 'Source version mismatch' }
    if ($doc.markdown -notmatch [regex]::Escape($passage.heading)) { throw 'Source heading missing' }
}
$body = @{question='What is the office Wi-Fi password?';retrieval_mode='keyword'} | ConvertTo-Json
$unsupported = Invoke-RestMethod http://127.0.0.1:8081/v1/ask -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 250
if ($unsupported.status -ne 'abstained') { throw 'Unsupported question did not abstain' }
$unsupported | ConvertTo-Json -Depth 20 | Set-Content reports/current-smoke-abstention.json
Write-Output $answer
Write-Output 'Real API answer, source versions and unsupported abstention verified.'
