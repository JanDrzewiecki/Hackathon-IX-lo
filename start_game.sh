#!/bin/bash
# Uranek Reactor Run - Quick Start Script

echo "🎮 Uranek Reactor Run"
echo "===================="
echo ""

# Check if we're in the right directory
if [ ! -d "src" ] || [ ! -d "game" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Check dependencies
echo "🔍 Checking dependencies..."
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "❌ Pygame not found! Installing..."
    pip3 install -r requirements.txt
fi

echo "✅ Dependencies installed"
echo ""
echo "🚀 Starting game..."
echo ""

python3 main.py
