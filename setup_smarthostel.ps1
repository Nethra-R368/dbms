# ==========================
# SmartHostel local DB setup
# ==========================
$pgBin = "C:\Program Files\PostgreSQL\18\bin"
$schemaFile = Join-Path $PSScriptRoot "schema.sql"
$user = "postgres"
$pwd  = "Nark@1231"
$db   = "smarthostel"

Write-Host "Verifying PostgreSQL service..."
Start-Service postgresql-x64-18 -ErrorAction SilentlyContinue

Write-Host "Running seed script to initialize smarthostel database with 50+ rows per table..."
& (Join-Path $PSScriptRoot "venv\Scripts\python.exe") (Join-Path $PSScriptRoot "seed.py")

Write-Host "✅ Database `$db` ready. Connect with pgAdmin using user `$user` and password `$pwd` on port 5432."