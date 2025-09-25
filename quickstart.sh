#!/bin/bash

# Quick virtual environment setup for Linux/Mac
# Usage: source quickstart.sh

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo "Virtual environment activated."
echo "Python: $(which python)"
echo "Run 'deactivate' to exit."