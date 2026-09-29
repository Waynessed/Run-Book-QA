$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$path = Join-Path (Get-Location) 'corpus/db-pool.md'
$source = Get-Content -LiteralPath $path -Raw
if ($source -match 'version: 1') {
    $source = $source.Replace('version: 1','version: 2').Replace('pool maximum of 10 connections per replica','pool maximum of 6 connections per replica')
    Set-Content -LiteralPath $path -Value $source -NoNewline
    & docker compose exec -T api python -m app.cli ingest
    if ($LASTEXITCODE -ne 0) { throw 'Updated document ingestion failed' }
} else { Write-Output 'db-pool already updated; checking the current index.' }
$doc = Invoke-RestMethod http://127.0.0.1:8081/v1/documents/db-pool
if ($doc.version -ne '2' -or $doc.markdown.Contains('pool maximum of 10 connections per replica')) { throw 'Current document still contains obsolete guidance' }
& docker compose exec -T api python -c "from app.db import Session,Chunk; from sqlalchemy import select; s=Session(); cs=s.scalars(select(Chunk).where(Chunk.document_id=='db-pool')).all(); assert cs and all(c.version=='2' and 'pool maximum of 10 connections per replica' not in c.text for c in cs); print('Only v2 chunks active; obsolete pool guidance removed.')"
if ($LASTEXITCODE -ne 0) { throw 'Obsolete chunk check failed' }
$doc | ConvertTo-Json -Depth 10 | Set-Content reports/document-update.json
