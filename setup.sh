#!/bin/bash

echo "Creating directory structure."
mkdir -p data src/objects src/utils

echo "Downloading Chordonomicon dataset."
curl -L "https://huggingface.co/datasets/ailsntua/Chordonomicon/resolve/main/chordonomicon_v2.csv?download=true" -o data/chordonomicon_v2.csv

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

echo "Installing packages from requirements.txt."
source .venv/bin/activate
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Packages not installed."
fi

echo "-----------------------------------------------"
echo "Setup complete. To start working, run:"
echo "source .venv/bin/activate"