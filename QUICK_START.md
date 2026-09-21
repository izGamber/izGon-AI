# 🚀 izGon AI - QUICK START GUIDE

## Pokretanje na Windows

### Opcija 1: Koristi `run.bat` (PREPORUČENO)
```bash
cd izGon-AI
run.bat
```

### Opcija 2: Koristi PowerShell
```powershell
cd izGon-AI
powershell -ExecutionPolicy Bypass -File run.ps1
```

### Opcija 3: Direktno sa cmd
```bash
cd izGon-AI
pip install -r requirements.txt
uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8001 --reload
```

---

## Pokretanje na Linux/Mac

```bash
cd izGon-AI
chmod +x run.sh
./run.sh
```

---

## Pokretanje sa Docker

```bash
# Iz root direktorijuma
docker-compose up -d

# Ili build i run
docker build -t izgon-ai:1.0 .
docker run -d -p 8001:8000 -v $(pwd)/data:/app/data izgon-ai:1.0
```

---

## Pristup Aplikaciji

Nakon pokretanja:

- **Dashboard:** http://localhost:8001
- **API Documentation:** http://localhost:8001/docs
- **Settings API:** http://localhost:8001/api/settings
- **Brain Stats:** http://localhost:8001/api/brain/stats

---

## Zaustavljanje Servera

- **Windows (run.bat):** Pritisnite `Ctrl+C` pa `Enter`
- **PowerShell:** Pritisnite `Ctrl+C`
- **Linux/Mac:** Pritisnite `Ctrl+C`
- **Docker:** `docker-compose down` ili `docker stop <container-id>`

---

## Česta Pitanja

### Problem: "Python nije instaliran"
**Rešenje:** Preuzmi Python 3.11+ sa https://www.python.org/

### Problem: "Port 8001 je zauzet"
**Rešenje:** Promeni port u:
- `run.bat`: `--port 8002`
- `run.sh`: `--port 8002`
- `run.ps1`: `--port 8002`

### Problem: "ModuleNotFoundError"
**Rešenje:**
```bash
pip install -r requirements.txt
```

### Problem: "Permission denied" na Linux/Mac
**Rešenje:**
```bash
chmod +x run.sh
```

---

## Testiranje

```bash
# Instaliraj pytest
pip install pytest

# Pokreni testove
pytest tests/

# Sa verboznim izlazom
pytest tests/ -v
```

---

## Debugging

### Vidi detaljan log
```bash
uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

### Vidi Docker log
```bash
docker-compose logs -f app
```

---

## Sledeće Korake

1. ✅ Pokrenuta je aplikacija
2. Otvori http://localhost:8001
3. Proba Brain funkcionalnosti
4. Kreni sa testiranjem sa AI modelima
5. Prilagodi postavke po potrebi

---

**Napravljeno sa ❤️ od izGamber**
