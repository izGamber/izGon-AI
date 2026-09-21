# 🧠 izGon AI - AI Memory Management System

![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

> **Revolucionaran sistem za upravljanje AI memorijom** - Nastavi gde si stao sa bilo kojim AI modelom!

## 📋 Što je izGon AI?

**izGon AI** je inteligentni sistem koji rešava najveću borbu korisnika AI alata:

> 🔴 **Problem:** Svaki put kada resetuješ AI sesiju, gube se svi kontekst, ciljevi i memorije iz prethodnog rada.

> 🟢 **Rešenje:** izGon AI automatski čuva sve što si radio, pamti tvoj kontekst, i omogućava nastavak rada bez ponovnog objašnjavanja svega!

---

## ✨ Ključne Prednosti

### 🧠 AI Memory Engine
- **Inteligentno čuvanje** - Čuva kontekst, ciljeve, i sve što radiš
- **Automatsko nastavaljenje** - Kreni od tačke gde si stao
- **Brze snapshote** - Spremi stanja rada u sekundi
- **Pretraga po ključnim rečima** - Pronađi šta treba u sekundi

### 💾 Memorijski Sistemi
- **5 tipova memorija** - note, learning, insights, errors, solutions
- **Prioriteti** - Označi važne stavke (1-5)
- **Temporalna organizacija** - Sve je sortirano po važnosti i vremenu
- **Unlimited memorije** - Čuvaj koliko god trebaš

### 🎨 Moderni Dashboard
- **Real-time statistike** - Uvek znaj šta se dešava
- **Dark mode** - Za nocne radne sesije
- **Responsive dizajn** - Radi na svim uređajima
- **WebSocket live** - Trenutna ažuriranja bez osvežavanja

### 🚀 Naprednute Funkcionalnosti
- **Multi-AI support** - GPT-4, Claude, Gemini, Custom API
- **Automatski backup** - Nikada ne gubi podatke
- **Export/Import** - Preuzmi sve memorije u JSON
- **Admin panel** - Kontrola nad svim podacima

---

## 🎯 Za Koga Je izGon AI?

### ✅ Idealan Za:

| Tip Korisnika | Primer Upotrebe |
|---|---|
| 👨‍💻 **Programeri** | Razvijaj veće projekte sa AI pomoćnikom bez resetovanja svaki put |
| 📝 **Content Kreatoru** | Piši serijale, knjige, članke sa konzistentnom AI pomoću |
| 📊 **Data Analitičari** | Vrši kompleksne analize sa AI, čuvajući sve korake |
| 🎓 **Studenti** | Nauči sa AI tutorima bez gubljenja konteksta |
| 🏢 **Kompaniji** | Centralizovani AI memory za sve zaposlene |
| 🤖 **AI Entuzijaste** | Eksperientiraj sa raznim AI modelima sa kontinuitetom |

---

## 💰 Cena i Licenciranje

### 🎁 Šta Dobijaš?

```
🛒 Jednorazna kupovina: $20 USD
├─ ✅ Doživotni pristup
├─ ✅ Besplatna ažuriranja
├─ ✅ Cloud sinhronizacija
├─ ✅ Premium podrška
└─ ✅ Komercialna upotreba
```

### 📜 Licenca

izGon AI je objavljen pod **MIT licencom**, što znači:
- ✅ Možeš ga koristiti za bilo šta
- ✅ Možeš ga modifikovati
- ✅ Možeš ga distribuirati
- ✅ Možeš ga koristiti komercijalno

**Samo obaveza:** Uključi copyright obavijest

---

## 🚀 Brzi Start

### Preduslov
- Python 3.11+
- pip ili conda
- Pretraživač (Chrome, Firefox, Safari, Edge)

### 1. Instalacija

```bash
git clone https://github.com/izGamber/izGon-AI.git
cd izGon-AI
pip install -r requirements.txt
```

### 2. Pokretanje

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Docker:**
```bash
docker-compose up -d
```

### 3. Pristup

Otvori pretraživač na: **http://localhost:8001**

---

## 📊 Karakteristike

### 🧠 Brain Engine
- Memorijsko čuvanje sa SQLite
- Kontekstni recall sa sortiranjem po važnosti
- Snapshot sistem za vraćanje stanja
- Pretraga po ključnim rečima
- AI Learning sistem

### 📈 Real-Time Dashboard
- Live statistike (Memorije, Projekti, Snapshots)
- Aktivnost timeline
- Pie chart memorija po tipu
- Brze akcije
- Dark/Light mode

### 🔌 WebSocket Komunikacija
- Socket.IO integracija
- Instant live ažuriranja
- Multi-client podrška
- Event streaming

### ⚙️ Postavke
- AI model toggle (GPT-4, Claude, Gemini)
- Tema i jezik
- Backup opcije
- Notifikacije
- Memory limits

---

## 📚 API Dokumentacija

### Brain Endpoints

#### Dodaj Memoriju
```bash
POST /api/brain/remember
{
  "content": "Rad sa AI-om",
  "memory_type": "note",
  "importance": 3
}
```

#### Vrati Memorije
```bash
GET /api/brain/memories?limit=20&memory_type=note
```

#### Pretraži
```bash
GET /api/brain/search?keyword=python
```

#### Brain Statistika
```bash
GET /api/brain/stats
```

#### Snapshot
```bash
POST /api/brain/snapshot
```

#### Export Memorija
```bash
GET /api/memories/export
```

Puna dokumentacija dostupna na: **http://localhost:8001/docs**

---

## 🛠️ Tehnički Stack

### Backend
- **FastAPI 0.109.0** - Web framework
- **Uvicorn 0.27.0** - ASGI server
- **Socket.IO 5.10.0** - Real-time komunikacija
- **SQLite3** - Baza podataka
- **Pydantic 2.5.3** - Data validation

### Frontend
- **HTML5** - Struktura
- **CSS3** - Moderan dizajn sa Glassmorphism
- **JavaScript (Vanilla)** - Interaktivnost
- **Chart.js** - Grafikoni
- **Font Awesome** - Ikonice

### DevOps
- **Docker** - Kontejnerizacija
- **Docker Compose** - Orkestracija
- **Python 3.11+** - Runtime

---

## 📁 Struktura Projekta

```
izGon-AI/
├── 📄 Dockerfile              # Production image
├── 📄 docker-compose.yml      # Development setup
├── 📄 requirements.txt        # Python zavisnosti
├── 📄 LICENSE                 # MIT licenca
├── 📄 README.md              # Dokumentacija
├── 📁 app/
│   ├── 📄 dashboard.py       # FastAPI endpoints
│   ├── 📄 brain.py           # AI Memory Engine
│   ├── 📄 settings.py        # Postavke
│   ├── 📄 admin.py           # Admin funkcionalnosti
│   ├── 📄 storage.py         # Database layer
│   ├── 📁 templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── settings.html
│   └── 📁 static/
│       ├── css/
│       └── js/
└── 📁 tests/
    └── test_brain.py
```

---

## 🧪 Testiranje

### Pokreni sve testove
```bash
pytest tests/ -v
```

### Testiraj specifičan modul
```bash
pytest tests/test_brain.py::TestBrainEngine::test_remember -v
```

### Sa coverage
```bash
pytest tests/ --cov=app
```

---

## 🚀 Deployment

### Na Server-u

```bash
# Build image
docker build -t izgon-ai:latest .

# Run container
docker run -d -p 8001:8000 \
  -v $(pwd)/data:/app/data \
  -e DEBUG=False \
  --name izgon-ai-prod \
  izgon-ai:latest
```

### Sa Gunicorn (više workers-a)

```bash
pip install gunicorn
gunicorn app.dashboard:asgi_app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001
```

---

## 📊 Primeri Upotrebe

### 1. Razvoj Softvera
```
Sednica 1: Diskusijaš sa AI o arhitekturi projekta
→ izGon AI čuva sve sugeste i odluke

Sednica 2: AI se seća šta ste diskutovali
→ Nastaviš od tačke gde si stao
→ Bez ponovnog objašnjavanja
```

### 2. Pisanje Knjige
```
Dan 1: Napraviš plan knjige sa AI
→ Sve se čuva u memoriji

Dan 5: AI se seća karaktera, teme, stila
→ Nastaviš pisanje bez resetovanja
```

### 3. Data Analiza
```
Faza 1: Eksploracijaš podatke
→ Memorije čuvaju sve korake

Faza 2: Detaljnija analiza
→ AI zna šta si već pokušao
→ Izbegavaš duplikate
```

---

## 🎨 Inovacijske Karakteristike

### AI Model Rotation
- Prelazi između GPT-4, Claude, Gemini
- Svi imaju istu memoriju
- Pronađi najbolji model za svaki task

### Smart Snapshots
- Automatski snapshot svakih 30 min
- Brzo vrati se na bilo koji snapshot
- Spremi ceo kontekst rada

### Context Recall
- AI automatski učita relevantne memorije
- Sortira po važnosti
- Kontekst je uvek dostupan

### Memory Analytics
- Analiza šta radiš najčešće
- Šta ti potiče greške
- Optimizuj tvoj rad

---

## 🐛 Troubleshooting

### Problem: Port 8001 je već zauzet
```bash
# Koristi drugi port
uvicorn app.dashboard:asgi_app --port 8002
```

### Problem: Zavisnosti nisu instalirane
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Problem: Database greška
```bash
# Obriši bazu i kreiraj novu
rm data/database.db
# Aplikacija će kreirati novu pri startu
```

---

## 📞 Podrška i Kontakt

- **GitHub Issues:** [Otvori issue](https://github.com/izGamber/izGon-AI/issues)
- **Email:** support@izgamber.com
- **Discord:** [Pridruži se serverima](https://discord.gg/izgamber)

---

## 🤝 Doprinos

Trebalo bi:
1. Fork repo
2. Kreiraj feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Otvori Pull Request

---

## 📈 Roadmap

### v1.1.0 (Q4 2026)
- [ ] WebSocket chat sa AI agentima
- [ ] Advanced analytics
- [ ] Mobile app

### v1.2.0 (Q1 2027)
- [ ] Multi-user kolaboracija
- [ ] Cloud sinhronizacija
- [ ] API integracija sa AI servisima

### v2.0.0 (Q2 2027)
- [ ] AI Model fine-tuning
- [ ] Local LLM podrška
- [ ] Enterprise features

---

## 📄 Licenca

Ovaj projekat je pod **MIT licencom**. Pogledaj [LICENSE](LICENSE) fajl.

---

## 👤 Autor

**izGamber**
- GitHub: [@izGamber](https://github.com/izGamber)
- Twitter: [@izGamber](https://twitter.com/izGamber)
- Web: [izGamber.com](https://izgamber.com)

---

## 🙏 Zahvalnost

Inspiracija iz AI revolution-a i potrebe za boljim memory management-om.

---

**⭐ Ako ti se svidja, ostavi star! ⭐**

```
Made with ❤️ by izGamber
```
