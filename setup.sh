#!/bin/bash

# Quick setup script for PB2 Natural Frequency Analysis (Linux/Mac)

echo ""
echo "============================================================"
echo "  PB2 Natural Frequency Analysis - Setup Script"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    echo ""
    echo "On macOS with Homebrew:"
    echo "  brew install python3"
    echo ""
    echo "On Ubuntu/Debian:"
    echo "  sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo ""
echo "Installing packages from requirements.txt..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Package installation failed"
    exit 1
fi

echo ""
echo "============================================================"
echo "  Setup completed successfully!"
echo "============================================================"
echo ""
echo "To run the program:"
echo "  1. Interactive Mode:"
echo "     python3 pb2_natural_frequency.py"
echo ""
echo "  2. Run Examples:"
echo "     python3 examples.py"
echo ""
echo "For more information, see README.md"
echo ""
