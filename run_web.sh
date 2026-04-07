#!/bin/bash

# PB2 Natural Frequency Analysis - Web Application Launcher (Linux/Mac)

echo ""
echo "============================================================"
echo "  PB2 Natural Frequency Analysis - Web Server"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
pip3 show flask > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "============================================================"
echo "  Starting Web Server..."
echo "============================================================"
echo ""
echo "The web application will be available at:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python3 app.py
