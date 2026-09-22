# =========================================
# izGon AI - Windows Setup Script (PowerShell)
# =========================================

Write-Host ""
Write-Host "  ███████╗██████╗ ███████╗████████╗██╗   ██╗██████╗" -ForegroundColor Cyan
Write-Host "  ██╔════╝██╔════╝ ██╔════╝╚══██╔══╝██║   ██║██╔══██╗" -ForegroundColor Cyan
Write-Host "  ███████╗██║  ███╗███████╗   ██║   ██║   ██║██████╔╝" -ForegroundColor Cyan
Write-Host "  ╚════██║██║   ██║╚════██║   ██║   ██║   ██║██╔═══╝" -ForegroundColor Cyan
Write-Host "  ███████║╚██████╔╝███████║   ██║   ╚██████╔╝██║" -ForegroundColor Cyan
Write-Host "  ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝ ╚═╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  izGon AI - Persistent Memory for Your Agents" -ForegroundColor Yellow
Write-Host "  ════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

# Check Docker
Write-Host "[1/5] Checking Docker..." -ForegroundColor Cyan
try {
    docker ps > $null 2>&1
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Generate .env
Write-Host ""
Write-Host "[2/5] Checking configuration..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    Write-Host "Generating .env file..." -ForegroundColor Yellow
    $secret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    
    @"
DATABASE_URL=sqlite:///./data/memory.db
SECRET_KEY=$secret
DEBUG=False
PYTHONUNBUFFERED=1
"@ | Out-File -Encoding UTF8 ".env"
    Write-Host "✓ .env created with secure key" -ForegroundColor Green
} else {
    Write-Host "✓ .env already exists" -ForegroundColor Green
}

# Create data directory
Write-Host ""
Write-Host "[3/5] Preparing storage..." -ForegroundColor Cyan
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" > $null
}
Write-Host "✓ Data directory ready" -ForegroundColor Green

# Build Docker image
Write-Host ""
Write-Host "[4/5] Building Docker image..." -ForegroundColor Cyan
docker compose build 2>&1 > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Docker build failed. Check your connection." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Image ready" -ForegroundColor Green

# Start services
Write-Host ""
Write-Host "[5/5] Starting izGon AI..." -ForegroundColor Cyan
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start services." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "⏳ Waiting for dashboard to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "✓ izGon AI is running!" -ForegroundColor Green
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "Dashboard:    http://localhost:8001" -ForegroundColor Cyan
Write-Host "API Docs:     http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "Database:     ./data/memory.db" -ForegroundColor Cyan
Write-Host "Config:       .env" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

Write-Host "Opening dashboard in your browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8001"

Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  View logs:      docker compose logs -f" -ForegroundColor Gray
Write-Host "  Stop services:  docker compose down" -ForegroundColor Gray
Write-Host "  Restart:        docker compose restart" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"
