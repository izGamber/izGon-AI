# izGon AI - Lokalna Instalacija i Setup

## Sistem zahtevi

- **Windows/Mac/Linux** 
- **Python 3.11+** (https://www.python.org/downloads/)
- **Git** (https://git-scm.com/downloads)
- **Docker** (optional, za lakše pokretanje)

---

## Opcija 1: Direktna Instalacija (bez Dockera)

### Korak 1: Kloniranje repozitorijuma

```bash
git clone https://github.com/izGamber/izGon-AI.git
cd izGon-AI
```

### Korak 2: Kreiranje virtual okruženja

**Na Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Na macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Korak 3: Instalacija zavisnosti

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Korak 4: Pokretanje aplikacije

```bash
python -m uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8001 --reload
```

### Korak 5: Pristup aplikaciji

- **Dashboard**: http://localhost:8001/
- **API Dokumentacija**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

---

## Opcija 2: Docker instalacija

### Korak 1: Kloniranje repozitorijuma

```bash
git clone https://github.com/izGamber/izGon-AI.git
cd izGon-AI
```

### Korak 2: Pokretanje sa Docker Compose

```bash
docker compose up -d
```

### Korak 3: Provera stanja

```bash
docker ps  # vidiš pokrenute kontejnere
docker logs izgon-ai-api -f  # prati logove
```

### Korak 4: Pristup aplikaciji

- **Dashboard**: http://localhost:8001/
- **API**: http://localhost:8001/api
- **Docs**: http://localhost:8001/docs

---

## Korišćenje aplikacije

### Dodavanje memorije preko API-ja

```bash
curl -X POST "http://localhost:8001/api/brain/remember?content=Moja%20memorija&memory_type=note&importance=3"
```

### Pregled memorija

```bash
curl "http://localhost:8001/api/brain/memories"
```

### Pravljenje snapshota

```bash
curl -X POST "http://localhost:8001/api/brain/snapshot"
```

### Pretraga memorija

```bash
curl "http://localhost:8001/api/brain/search?keyword=test"
```

---

## Web Dashboard - Funkcionalnosti

### 📊 Dashboard Tab
- **Brain Status** - stanje AI sistema
- **Memorije** - broj čuvanih memorija
- **Projekti** - broj aktivnih projekata  
- **Snapshots** - broj sačuvanih stanja
- **Nedavna aktivnost** - log svih akcija

### 🧠 Brain Tab (coming soon)
- Detaljno profajliranje Brain Engine-a
- Analiza memorija po tipovima
- Performance metriken

### 📝 Memorije Tab
- Pregled svih memorija
- Filter po tipu, važnosti
- Brzo brisanje/editovanje
- Full-text pretraga

### ⚙️ Postavke Tab
- Konfiguracija sistemskih parametara
- Izbor AI modela (OpenAI, Ollama)
- Tema (light/dark mode)
- Backup/Restore opcije

---

## API Endpoints

### Brain endpoints
- `GET /api/brain/stats` - Statistika mozga
- `POST /api/brain/remember` - Dodaj memoriju
- `GET /api/brain/memories` - Sve memorije
- `GET /api/brain/search?keyword=...` - Pretraži memorije
- `POST /api/brain/snapshot` - Pravi snapshot
- `POST /api/brain/snapshot/{id}` - Vrati snapshot
- `DELETE /api/brain/forget/{id}` - Obriši memoriju
- `PATCH /api/brain/importance/{id}` - Promeni važnost

### Project endpoints
- `GET /api/projects` - Svi projekti
- `POST /api/projects?name=...` - Novi projekat

### Admin endpoints
- `POST /api/admin/reset-brain` - Resetuj brain
- `GET /api/admin/db-info` - Info o bazi podataka
- `GET /api/info` - Server info

---

## Troubleshooting

### Greška: "Address already in use"
Port 8001 je zauzet. Koristi drugi port:
```bash
python -m uvicorn app.dashboard:asgi_app --port 8002
```

### Greška: "ModuleNotFoundError"
Nisam aktivirao virtual okruženje:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Greška: "Cannot connect to database"
Obriši staru bazu i ponovo kreni:
```bash
rm -rf data/database.db  # Linux/macOS
del data\database.db     # Windows
python -m uvicorn app.dashboard:asgi_app --port 8001 --reload
```

### Docker greške
```bash
docker compose down    # zaustavi sve
docker compose up -d   # ponovo pokreni
docker logs izgon-ai-api  # vidi greške
```

---

## Razvoj i Testiranje

### Pokretanje testova
```bash
pytest tests/
```

### Proveriti Coverage
```bash
pytest --cov=app tests/
```

### Format koda
```bash
black app/
flake8 app/
```

---

## Performanse i Optimizacija

- **Socket.IO** - Real-time ažuriranja bez osvežavanja
- **SQLite** - Brza lokalna baza, bez setup-a
- **Uvicorn** - Async server za brže zahteve
- **Jinja2 templates** - Brzo renderovanje HTML-a

---

## Logging

Logovi se čuvaju u konzoli. Za trajno čuvanje, dodaj u `app/dashboard.py`:

```python
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
```

---

## Sigurnost

⚠️ **VAŽNO za produkciju:**
- Postavi `DEBUG=False` u `.env`
- Promeni `SECRET_KEY` 
- Koristi HTTPS umesto HTTP
- Limitiraj broj pokušaja (rate limiting)
- Validiraj sve inpute

---

## Sledeće korake

1. **Kustomizuj** postavke u `app/settings.py`
2. **Dodaj** svoje memorije kroz Dashboard
3. **Pravi** snapshots za backup
4. **Koristi** API za integraciju sa drugim alatima
5. **Monitoring** - prati Brain Health indikator

---

## Podrška

Ako imaš problema:
1. Provjeri logove: `docker logs izgon-ai-api` ili terminal output
2. Provjeri health: `curl http://localhost:8001/health`
3. Pogledaj API docs: http://localhost:8001/docs

---

**Status**: ✅ Sve testove PASSED - Ready za produkciju!
