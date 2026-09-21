#!/bin/bash
# izGon AI - Start Script za Linux/Mac

set -e

echo "============================================"
echo "  izGon AI - Brain Dashboard"
echo "  http://localhost:8001"
echo "============================================"
echo ""

# Provera Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 nije instaliran!"
    exit 1
fi

echo "[INFO] Python pronađen: $(python3 --version)"
echo ""

# Instalacija zavisnosti
echo "[INFO] Instalacija zavisnosti..."
pip install -q -r requirements.txt

echo "[SUCCESS] Zavisnosti instalirane"
echo ""

# Pokretanje servera
echo "[INFO] Pokretanje servera na portu 8001..."
echo "[INFO] Pristup: http://localhost:8001"
echo "[INFO] API Docs: http://localhost:8001/docs"
echo "[INFO] Settings API: http://localhost:8001/api/settings"
echo "[INFO] Pritisnite Ctrl+C da zaustavite server"
echo ""

uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8001 --reload
