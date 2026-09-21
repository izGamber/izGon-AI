# 🚀 UPUTSTVO ZA POKRETANJE izGon-AI

## KORAK 1: Instalacija zavisnosti

### Na Windows:
```bash
cd izGon-AI
pip install -r requirements.txt
```

### Na Linux/Mac:
```bash
cd izGon-AI
pip3 install -r requirements.txt
```

---

## KORAK 2: Pokretanje Aplikacije

### OPCIJA A: Direktno (Development)
```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

### OPCIJA B: Sa uvicorn manuelno
```bash
uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8000 --reload
```

### OPCIJA C: Sa Docker-om
```bash
docker-compose up -d
```

---

## KORAK 3: Pristup Aplikaciji

Otvori u pregledniku:
- **Dashboard:** http://localhost:8000
- **API dokumentacija:** http://localhost:8000/docs (Swagger UI)
- **ReDoc API:** http://localhost:8000/redoc

---

## 🧠 TESTIRANJE BRAIN SISTEMA

### 1. Dodaj Memoriju
```bash
curl -X POST "http://localhost:8000/api/brain/remember?content=Moja%20prva%20memorija&memory_type=note&importance=3"
```

### 2. Vrati Memorije
```bash
curl "http://localhost:8000/api/brain/memories"
```

### 3. Vrati Statistiku
```bash
curl "http://localhost:8000/api/brain/stats"
```

### 4. Kreiraj Snapshot
```bash
curl -X POST "http://localhost:8000/api/brain/snapshot"
```

---

## 🎨 UI FEATURES - SVE JE DOSTUPNO!

### Dashboard Kartice:
- 🧠 **Brain Status** - Stanje sistema
- 💾 **Memorije** - Broj čuvanih memorija
- 📁 **Projekti** - Broj projekata
- 📸 **Snapshots** - Broj snapshota

### Brze Akcije:
- ➕ **Nova Memorija** - Dodaj novu memoriju
- 🔬 **Analiza Mozga** - Brain analysis
- 📸 **Pravi Snapshot** - Kreiraj snapshot
- 📋 **Sve Memorije** - Pregled svih memorija

### Dark Mode:
- Klikni na **🌙 moon ikonicu** u gornjem desnom uglu
- Preference se čuva automatski

---

## 📊 API PRIMERI

### 1. POST - Nova Memorija
```bash
curl -X POST "http://localhost:8000/api/brain/remember" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Python je odličan jezik",
    "memory_type": "learning",
    "importance": 4
  }'
```

### 2. GET - Sve Memorije
```bash
curl "http://localhost:8000/api/brain/memories?limit=10"
```

### 3. GET - Pretraga
```bash
curl "http://localhost:8000/api/brain/search?keyword=python"
```

### 4. GET - Brain Stats
```bash
curl "http://localhost:8000/api/brain/stats"
```

### 5. POST - Snapshot
```bash
curl -X POST "http://localhost:8000/api/brain/snapshot"
```

### 6. DELETE - Obriši Memoriju
```bash
curl -X DELETE "http://localhost:8000/api/brain/forget/1"
```

---

## 🧪 POKRETANJE TESTOVA

```bash
# Svi testovi
pytest tests/ -v

# Određeni test
pytest tests/test_brain.py::TestBrainEngine::test_remember -v

# Sa Coverage
pytest tests/ --cov=app
```

---

## 📁 STRUKTURA PROJEKTA

```
izGon-AI/
├── app/
│   ├── dashboard.py      ← FastAPI endpoints
│   ├── brain.py          ← AI Memory Engine
│   ├── storage.py        ← Database layer
│   ├── templates/        ← HTML stranice
│   │   ├── base.html
│   │   └── dashboard.html
│   └── static/           ← CSS, JS, resursi
│       ├── css/style.css
│       └── js/app.js
├── requirements.txt      ← Zavisnosti
├── Dockerfile            ← Docker image
├── docker-compose.yml    ← Docker setup
├── run.bat/run.sh        ← Start scripti
└── README.md             ← Dokumentacija
```

---

## 🔧 TROUBLESHOOTING

### Problem: Port 8000 je već zauzet
```bash
# Koristi drugi port
uvicorn app.dashboard:asgi_app --host 0.0.0.0 --port 8001 --reload
```

### Problem: Zavisnosti nisu instalirane
```bash
# Prosirena instalacija
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Problem: Database greška
```bash
# Obriši staru bazu i kreiraj novu
rm data/database.db
# Aplikacija će kreirati novu pri pokretanju
```

### Problem: Socket.IO konekcija
- Proveri da je port 8000 otvoren
- Proveri firewall
- Ponovna konekcija je automatska

---

## 🚀 PRODUCTION DEPLOYMENT

### Sa Docker-om:
```bash
docker build -t izgon-ai .
docker run -d -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DEBUG=False \
  --name izgon-ai-prod \
  izgon-ai
```

### Sa Gunicorn (više worker-a):
```bash
pip install gunicorn
gunicorn app.dashboard:asgi_app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## 📚 DODATNI RESURSI

- [FastAPI Dokumentacija](https://fastapi.tiangolo.com/)
- [Socket.IO Dokumentacija](https://python-socketio.readthedocs.io/)
- [SQLite Dokumentacija](https://www.sqlite.org/docs.html)
- [Docker Dokumentacija](https://docs.docker.com/)

---

## 💬 PODRŠKA

Za probleme ili pitanja:
1. Proveri [README.md](README.md)
2. Otvori [GitHub Issue](https://github.com/izGamber/izGon-AI/issues)
3. Prosledi detalje i logove

---

**Sretno sa izGon AI! 🧠✨**
