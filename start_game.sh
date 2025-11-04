#!/bin/bash
# Star Trek: Captain's Career Simulator
# Launch script for Unix-based systems (Linux, macOS)

echo "========================================"
echo "Star Trek: Captain's Career Simulator"
echo "========================================"
echo ""
echo "Checking Python installation..."

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo ""
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.7 or later:"
    echo "  - Ubuntu/Debian: sudo apt install python3"
    echo "  - macOS: brew install python3"
    echo "  - Or visit: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Python $PYTHON_VERSION detected!"
echo ""
echo "Starting game..."
echo ""

# Run the game
$PYTHON_CMD main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Game exited with an error."
    read -p "Press Enter to continue..."
fi
