#!/bin/bash
# Quick start script for Vhape Dummy API

echo "Starting Vhape Dummy API..."
echo "FastAPI docs will be available at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT" || exit

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Use python -m uvicorn instead of direct uvicorn command
echo "Starting server..."
python -m uvicorn api_dummy.main:app --reload --host 0.0.0.0 --port 8000

