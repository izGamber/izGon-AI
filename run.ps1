# izGon AI - Start Script for PowerShell
# Pokretanje: powershell -ExecutionPolicy Bypass -File run.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   izGon AI - Brain Dashboard" -ForegroundColor Yellow
Write-Host "   http://localhost:8001" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Provera Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Python pronađen: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python nije instaliran!" -ForegroundColor Red
    Write-Host "Preuzmi Python 3.11+ sa https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Pritisnite Enter za izlaz"
    exit 1
}

Write-Host ""

# Instalacija zavisnosti
Write-Host "[INFO] Instalacija zavisnosti..." -ForegroundColor Cyan
pip install -q -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Greška pri instalaciji zavisnosti" -ForegroundColor Red
    Read-Host "Pritisnite Enter za izlaz"
    exit 1
}

Write-Host "[SUCCESS] Zavisnosti instalirane" -ForegroundColor Green
Write-Host ""

# Pokretanje servera
Write-Host "[INFO] Pokretanje servera na portu 8001..." -ForegroundColor Cyan
Write-Host "[INFO] Pristup: http://localhost:8001" -ForegroundColor Green
Write-Host "[INFO] API Docs: http://localhost:8001/docs" -ForegroundColor Green
Write-Host "[INFO] Settings API: http://localhost:8001/api/settings" -ForegroundColor Green
Write-Host "[INFO] Pritisnite Ctrl+C da zaustavite server" -ForegroundColor Yellow
Write-Host ""

# Pokretanje aplikacije
uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8001 --reload

Write-Host ""
Read-Host "Pritisnite Enter za izlaz"
