# izGon AI - Windows Setup Guide

## Quick Install (Windows)

### Option 1: One-Click Setup (Easiest) ⭐
Double-click **`izGon-AI-Setup.cmd`**

This will:
1. ✓ Check Docker is running
2. ✓ Generate secure `.env` file
3. ✓ Build Docker image
4. ✓ Start all services
5. ✓ Open dashboard in browser

Then visit: **http://localhost:8001**

---

### Option 2: PowerShell Setup
Right-click on **`izGon-AI-Setup.ps1`** → "Run with PowerShell"

Or in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\izGon-AI-Setup.ps1
```

---

### Option 3: Manual Docker Compose
```powershell
docker compose up -d
```

Visit: **http://localhost:8001**

---

## What Gets Installed

After setup, you'll have:

```
izGon-AI/
├── data/                    # SQLite database
│   └── memory.db           # Your memories here
├── app/                     # Python FastAPI backend
├── web/                     # Web dashboard & static files
├── .env                     # Config (auto-generated)
├── docker-compose.yml       # Docker setup
└── Dockerfile              # Container definition
```

---

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Dashboard** | http://localhost:8001 | Web UI for managing memories |
| **API Docs** | http://localhost:8001/docs | Interactive FastAPI docs |
| **API Endpoint** | http://localhost:8001/api/brain | REST API for agents |
| **Database** | ./data/memory.db | SQLite file |

---

## First Steps After Install

### 1. Store a Memory
```bash
curl -X POST http://localhost:8001/api/brain/remember \
  -H "Content-Type: application/json" \
  -d '{
    "content": "My first memory in izGon AI!",
    "tags": ["test", "welcome"],
    "importance": 10
  }'
```

### 2. View in Dashboard
Go to http://localhost:8001 → Click **"Memories"**

### 3. Search Memories
```bash
curl "http://localhost:8001/api/brain/search?q=memory"
```

### 4. Take a Snapshot
```bash
curl -X POST http://localhost:8001/api/brain/snapshot
```

---

## Useful Commands

### View Logs
```powershell
docker compose logs -f
```

### Stop Services
```powershell
docker compose down
```

### Restart
```powershell
docker compose restart
```

### Clean Everything (Start Fresh)
```powershell
docker compose down -v
```

---

## Troubleshooting

### Docker not running?
- Start Docker Desktop
- Re-run setup script

### Port 8001 already in use?
```powershell
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Need to rebuild?
```powershell
docker compose build --no-cache
docker compose up -d
```

---

## Next Steps

- **Dashboard**: Manage memories, view activity, take snapshots
- **API Integration**: Connect your AI agent via REST endpoints
- **Configuration**: Edit `.env` for custom settings
- **License**: Purchase commercial license at https://izgamber.github.io/IZgoN/izgon-ai/

---

**Happy memory-storing!** 🧠✨
