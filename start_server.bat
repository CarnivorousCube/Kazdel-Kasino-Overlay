@echo off
title Kazdel Kasino Overlay Server
color 0A

echo ========================================
echo   Kazdel Kasino Overlay Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [*] Python found
echo.

REM Check if requirements are installed
echo [*] Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
    echo [*] Dependencies installed successfully
    echo.
) else (
    echo [*] Dependencies already installed
    echo.
)

REM Start the server and open browser
echo [*] Starting server...
echo [*] Server will be available at http://localhost:8000
echo [*] Opening control panel in your default browser...
echo.
echo Press Ctrl+C to stop the server
echo.

REM Open browser after 2 seconds delay (using PowerShell)
powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8000?controls'"

REM Run the server (this will block until Ctrl+C)
python server.py

