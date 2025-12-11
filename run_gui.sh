#!/bin/bash

echo "Starting Laravel Quality Assessor GUI..."
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""
echo "Launching GUI application..."
python3 laravel_quality_gui.py