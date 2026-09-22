@echo off
REM ================================================
REM Build izGon-AI-Setup.exe using NSIS
REM ================================================

setlocal enabledelayedexpansion

echo Creating izGon AI Setup Installer...
echo.

REM Check if NSIS is installed
where makensis >nul 2>&1
if errorlevel 1 (
    echo ERROR: NSIS is not installed!
    echo.
    echo Download and install NSIS from:
    echo   https://nsis.sourceforge.io/
    echo.
    pause
    exit /b 1
)

REM Create NSIS script
(
echo ; izGon AI Setup Script for NSIS
echo ; ================================================
echo.
echo !include "MUI2.nsh"
echo.
echo Name "izGon AI"
echo OutFile "izGon-AI-Setup.exe"
echo InstallDir "$PROGRAMFILES\izGon AI"
echo.
echo !insertmacro MUI_PAGE_DIRECTORY
echo !insertmacro MUI_PAGE_INSTFILES
echo !insertmacro MUI_PAGE_FINISH
echo !insertmacro MUI_LANGUAGE "English"
echo.
echo Section "Install"
echo   SetOutPath "$INSTDIR"
echo   File "izGon-AI-Setup.cmd"
echo   File "izGon-AI-Setup.ps1"
echo   File "docker-compose.yml"
echo   File "Dockerfile"
echo   File "requirements.txt"
echo   File ".dockerignore"
echo   SetOutPath "$INSTDIR\app"
echo   File /r "app\*"
echo   SetOutPath "$INSTDIR\web"
echo   File /r "web\*"
echo   CreateDirectory "$SMPROGRAMS\izGon AI"
echo   CreateShortCut "$SMPROGRAMS\izGon AI\Setup.lnk" "$INSTDIR\izGon-AI-Setup.cmd"
echo   CreateShortCut "$SMPROGRAMS\izGon AI\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
echo SectionEnd
echo.
echo Section "Uninstall"
echo   RMDir /r "$INSTDIR"
echo   RMDir /r "$SMPROGRAMS\izGon AI"
echo SectionEnd
) > build-setup.nsi

echo Building NSIS installer...
makensis build-setup.nsi

if exist izGon-AI-Setup.exe (
    echo.
    echo SUCCESS! Created: izGon-AI-Setup.exe
    echo.
    del build-setup.nsi
) else (
    echo FAILED to create Setup.exe
    pause
    exit /b 1
)

pause
