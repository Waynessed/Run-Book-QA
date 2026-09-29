$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
Invoke-RestMethod http://127.0.0.1:8081/readyz
$body = @{question='The API returns 401 after deployment. What should I check?'; retrieval_mode='keyword'} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8081/v1/ask -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 250 | ConvertTo-Json -Depth 10
