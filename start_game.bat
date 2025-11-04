@echo off
title Star Trek: Captain's Career Simulator
echo.
echo ========================================
echo Star Trek: Captain's Career Simulator
echo ========================================
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or later from:
    echo   - Microsoft Store, OR
    echo   - https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python detected!
echo.
echo Starting game in GUI mode...
echo.
python gui_main.py

if errorlevel 1 (
    echo.
    echo Game exited with an error.
    pause
)
