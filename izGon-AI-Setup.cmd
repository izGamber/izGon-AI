@echo off
setlocal enabledelayedexpansion

REM ========================================
REM   izGon AI - Windows Setup Script
REM ========================================
REM One-click setup: checks Docker, generates .env, starts services, opens dashboard

color 0A
title izGon AI Setup

cls
echo.
echo  ███████╗██████╗ ███████╗████████╗██╗   ██╗██████╗
echo  ██╔════╝██╔════╝ ██╔════╝╚══██╔══╝██║   ██║██╔══██╗
echo  ███████╗██║  ███╗███████╗   ██║   ██║   ██║██████╔╝
echo  ╚════██║██║   ██║╚════██║   ██║   ██║   ██║██╔═══╝
echo  ███████║╚██████╔╝███████║   ██║   ╚██████╔╝██║
echo  ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝ ╚═╝
echo.
echo  izGon AI - Persistent Memory for Your Agents
echo  ═════════════════════════════════════════════════════
echo.

REM Check if Docker is running
echo [1/5] Checking Docker...
docker ps >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ✗ Docker is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)
color 0A
echo ✓ Docker is running

REM Generate .env if not exists
echo.
echo [2/5] Checking configuration...
if not exist .env (
    echo Generating .env file...
    
    REM Generate a random 32-char secret
    setlocal enabledelayedexpansion
    set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    set "secret="
    for /L %%i in (1,1,32) do (
        set /a index=!random! %% 62
        for /F %%j in ('echo prompt $H ^| cmd') do set "BS=%%j"
        for %%k in (!index!) do set "secret=!secret!!chars:~%%k,1!"
    )
    
    (
        echo DATABASE_URL=sqlite:///./data/memory.db
        echo SECRET_KEY=!secret!
        echo DEBUG=False
        echo PYTHONUNBUFFERED=1
    ) > .env
    
    echo ✓ .env created with secure key
) else (
    echo ✓ .env already exists
)

REM Create data directory
echo.
echo [3/5] Preparing storage...
if not exist data mkdir data
echo ✓ Data directory ready

REM Pull latest image
echo.
echo [4/5] Building Docker image...
docker compose build >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ✗ Docker build failed. Check your connection and try again.
    pause
    exit /b 1
)
color 0A
echo ✓ Image ready

REM Start services
echo.
echo [5/5] Starting izGon AI...
docker compose up -d
if errorlevel 1 (
    color 0C
    echo ✗ Failed to start services.
    pause
    exit /b 1
)
color 0A

REM Wait for service to be ready
echo.
echo ⏳ Waiting for dashboard to be ready...
timeout /t 5 /nobreak

REM Open dashboard
echo.
echo ✓ izGon AI is running!
echo.
echo ═════════════════════════════════════════════════════
echo Dashboard:    http://localhost:8001
echo API Docs:     http://localhost:8001/docs
echo Database:     ./data/memory.db
echo Config:       .env
echo ═════════════════════════════════════════════════════
echo.
echo Opening dashboard in your browser...
echo.

REM Open browser
start http://localhost:8001

REM Show logs hint
echo.
echo To view logs:
echo   docker compose logs -f
echo.
echo To stop services:
echo   docker compose down
echo.

pause
