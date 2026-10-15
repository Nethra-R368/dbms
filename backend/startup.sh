#!/bin/bash

echo "=== Starting SmartHostel Backend Startup Script ==="

# Check and activate virtual environment if present
if [ -d "$HOME/antenv" ]; then
    echo "Found antenv in $HOME"
    source "$HOME/antenv/bin/activate"
elif [ -d "/antenv" ]; then
    echo "Found antenv in /antenv"
    source "/antenv/bin/activate"
elif [ -d "$HOME/site/wwwroot/antenv" ]; then
    echo "Found antenv in wwwroot"
    source "$HOME/site/wwwroot/antenv/bin/activate"
fi

# If uvicorn or psycopg is not found in environment, install requirements
if ! python -c "import uvicorn, psycopg" &> /dev/null; then
    echo "Dependencies missing, running pip install -r requirements.txt..."
    python -m pip install -r requirements.txt
fi

echo "Starting Uvicorn Server on 0.0.0.0:8000..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
