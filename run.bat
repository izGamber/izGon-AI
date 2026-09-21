@echo off
REM izGon AI - Start Script for Windows

echo ============================================
echo   izGon AI - Brain Dashboard
echo   http://localhost:8001
echo ============================================
echo.

REM Provera Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nije instaliran!
    echo Preuzmi Python 3.11+ sa https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Python pronađen
echo.

REM Instalacija zavisnosti
echo [INFO] Instalacija zavisnosti...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Greška pri instalaciji zavisnosti
    pause
    exit /b 1
)

echo [SUCCESS] Zavisnosti instalirane
echo.

REM Pokretanje servera
echo [INFO] Pokretanje servera na portu 8001...
echo [INFO] Pristup: http://localhost:8001
echo [INFO] API Docs: http://localhost:8001/docs
echo [INFO] Settings API: http://localhost:8001/api/settings
echo.
echo [INFO] Pritisnite Ctrl+C da zaustavite server
echo.

uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8001 --reload

pause
