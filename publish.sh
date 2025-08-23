#!/bin/bash

# Build and publish to PyPI
# Usage: ./publish.sh [test|prod]

set -e

echo "🔨 Building package..."
rm -rf dist/ build/ *.egg-info/
python -m pip install --upgrade build twine
python -m build

echo "📦 Package built successfully!"
ls -la dist/

if [ "$1" == "test" ]; then
    echo "📤 Uploading to TestPyPI..."
    python -m twine upload --repository testpypi dist/*
    echo "✅ Package uploaded to TestPyPI!"
    echo "Install with: pip install --index-url https://test.pypi.org/simple/ pycwmanage"
elif [ "$1" == "prod" ]; then
    echo "📤 Uploading to PyPI..."
    echo "⚠️  WARNING: This will publish to the real PyPI!"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python -m twine upload dist/*
        echo "✅ Package uploaded to PyPI!"
        echo "Install with: pip install pycwmanage"
    else
        echo "❌ Upload cancelled"
    fi
else
    echo "Usage: ./publish.sh [test|prod]"
    echo "  test - Upload to TestPyPI"
    echo "  prod - Upload to PyPI (production)"
fi