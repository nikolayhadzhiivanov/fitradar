#!/usr/bin/env bash
# FitRadar BG - Start Local Server & Public Internet Tunnel

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

echo "=================================================="
echo "🚀 Стартиране на FitRadar BG (EUR Price Index)..."
echo "=================================================="

# Check virtualenv
if [ ! -d "venv" ]; then
    echo "Създаване на venv..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install beautifulsoup4 requests flask
fi

# Run background Flask server if not already running
if ! lsof -i :5055 > /dev/null 2>&1; then
    echo "Стартиране на локален Flask сървър на порт 5055..."
    ./venv/bin/python3 fitradar/app.py &
    sleep 2
else
    echo "Flask сървърът вече работи на порт 5055."
fi

echo ""
echo "Локален адрес: http://localhost:5055"
echo ""
echo "Стартиране на публичен криптиран тунел за външен достъп..."
echo "Свързване към localhost.run през SSH..."
echo "=================================================="

ssh -o StrictHostKeyChecking=no -R 80:localhost:5055 nokey@localhost.run
