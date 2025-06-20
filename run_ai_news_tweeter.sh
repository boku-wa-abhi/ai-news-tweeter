#!/bin/bash

# AI News Tweeter - Complete Setup and Run Script
# This script creates a virtual environment, installs dependencies, runs the app, and cleans up

set -e  # Exit on any error

echo "🚀 Starting AI News Tweeter Setup and Execution..."
echo "================================================"

# Variables
VENV_NAME="ai_news_venv"
PROJECT_DIR="$(pwd)"
PYTHON_CMD="python3"

# Check if Python 3 is available
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

echo "✅ Python 3 found: $($PYTHON_CMD --version)"

# Function to cleanup
cleanup() {
    echo "\n🧹 Cleaning up..."
    
    # Deactivate virtual environment if active
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "   Deactivating virtual environment..."
        deactivate 2>/dev/null || true
    fi
    
    # Remove virtual environment
    if [ -d "$VENV_NAME" ]; then
        echo "   Removing virtual environment: $VENV_NAME"
        rm -rf "$VENV_NAME"
    fi
    
    # Remove Python cache files
    echo "   Removing Python cache files..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "*.pyo" -delete 2>/dev/null || true
    
    # Remove pip cache (optional)
    echo "   Clearing pip cache..."
    $PYTHON_CMD -m pip cache purge 2>/dev/null || true
    
    echo "✅ Cleanup completed!"
}

# Set trap to cleanup on script exit (success or failure)
trap cleanup EXIT

# Step 1: Create virtual environment
echo "\n📦 Creating virtual environment: $VENV_NAME"
if [ -d "$VENV_NAME" ]; then
    echo "   Removing existing virtual environment..."
    rm -rf "$VENV_NAME"
fi

$PYTHON_CMD -m venv "$VENV_NAME"
echo "✅ Virtual environment created"

# Step 2: Activate virtual environment
echo "\n🔧 Activating virtual environment..."
source "$VENV_NAME/bin/activate"
echo "✅ Virtual environment activated"

# Step 3: Upgrade pip
echo "\n⬆️  Upgrading pip..."
pip install --upgrade pip
echo "✅ Pip upgraded"

# Step 4: Install dependencies
echo "\n📚 Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Step 5: Check environment variables
echo "\n🔑 Checking environment variables..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
    # Load environment variables using export
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️  .env file not found - Twitter posting may not work"
fi

# Step 6: Run the application
echo "\n🎯 Running AI News Tweeter..."
echo "================================================"

# Run main.py
python main.py

echo "\n================================================"
echo "🎉 AI News Tweeter execution completed!"

# Note: cleanup() will be called automatically due to the trap