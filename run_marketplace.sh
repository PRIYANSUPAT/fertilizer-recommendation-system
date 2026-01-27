#!/bin/bash

# FarmDirect Marketplace Startup Script

echo "============================================"
echo "  🌾 FarmDirect Marketplace"
echo "  Farmer to Consumer Direct Platform"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! python3 -m pip --version &> /dev/null; then
    echo "⚠️  pip not found. Attempting to install..."
    python3 -m ensurepip --default-pip 2>/dev/null || {
        echo "❌ Failed to install pip. Please install pip manually."
        exit 1
    }
fi

echo "✓ pip found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
python3 -m pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python3 -c "import database; print('✓ Database initialized')"

if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize database"
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -m streamlit version &> /dev/null; then
    echo "❌ Streamlit not installed properly"
    exit 1
fi

echo ""
echo "============================================"
echo "  🚀 Starting FarmDirect Marketplace..."
echo "============================================"
echo ""
echo "📍 The application will open in your browser"
echo "📍 Default URL: http://localhost:8501"
echo ""
echo "Test Accounts:"
echo "  Farmer: testfarmer / pass123"
echo "  Consumer: testconsumer / pass123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================"
echo ""

# Run the application
python3 -m streamlit run marketplace_app.py
