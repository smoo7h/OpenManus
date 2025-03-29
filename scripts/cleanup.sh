#!/bin/bash

echo "🧹 Starting workspace cleanup..."

# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Clean logs directory
echo "Cleaning logs directory..."
rm -rf logs/*

# Clean workspace directory (including README.md)
echo "Cleaning workspace directory..."
rm -rf workspace/*

# Clean output directory
echo "Cleaning output directory..."
rm -rf output/*

# Clean memory-bank (optional - uncomment if needed)
# echo "Cleaning memory-bank..."
# rm -rf memory-bank/*

echo "✨ Cleanup complete!"