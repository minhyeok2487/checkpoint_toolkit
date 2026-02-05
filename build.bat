@echo off
chcp 65001 > nul
title CheckPoint Toolkit Build

echo ========================================
echo   CheckPoint Toolkit v3.7 Build
echo   Hyundai AutoEver Security Team
echo ========================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [3/4] Installing dependencies...
pip install customtkinter requests pyinstaller

if errorlevel 1 (
    echo [ERROR] Failed to install packages.
    pause
    exit /b 1
)

echo.
echo [4/4] Building executable...
echo Please wait (1-3 minutes)...
echo.

pyinstaller --noconfirm --onefile --windowed ^
    --name "CheckPointToolkit" ^
    --add-data "config.py;." ^
    --add-data "lang.py;." ^
    --add-data "widgets.py;." ^
    --add-data "api;api" ^
    --add-data "tabs;tabs" ^
    --hidden-import customtkinter ^
    --hidden-import tkinter ^
    --hidden-import requests ^
    --collect-all customtkinter ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Output: dist\CheckPointToolkit.exe
echo.

explorer dist
pause
