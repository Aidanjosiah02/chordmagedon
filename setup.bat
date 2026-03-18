@echo off
setlocal

echo [1/4] Creating directory structure...
if not exist "data" mkdir data
if not exist "src\objects" mkdir src\objects
if not exist "src\utils" mkdir src\utils

echo [2/4] Downloading Chordonomicon dataset...
curl -L "https://huggingface.co/datasets/ailsntua/Chordonomicon/resolve/main/chordonomicon_v2.csv?download=true" -o data\chordonomicon_v2.csv

echo [3/4] Setting up Virtual Environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo [4/4] Installing dependencies...
call .venv\Scripts\activate.bat

if exist "requirements.txt" (
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo Warning: requirements.txt not found. Skipping package installation.
)

echo.
echo -----------------------------------------------
echo Setup complete! 
echo To activate your environment, run: .venv\Scripts\activate
echo -----------------------------------------------
pause