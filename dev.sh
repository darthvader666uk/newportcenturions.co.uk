#!/bin/bash
# Development server script for Newport Centurions website

echo "Starting Newport Centurions development server..."
echo ""

# Install dependencies if needed
if [ ! -d "vendor" ]; then
    echo "Installing dependencies (first run only)..."
    bundle install
fi

# Detect environment and print correct URL
if grep -qi microsoft /proc/version 2>/dev/null; then
    WSL_IP=$(hostname -I | awk '{print $1}')
    echo "WSL2 detected"
    echo ""
    echo "  >>>  http://${WSL_IP}:4000  <<<"
    echo ""
else
    echo "Native Linux detected"
    echo ""
    echo "  >>>  http://localhost:4000  <<<"
    echo ""
fi

echo "Changes auto-reload. Press Ctrl+C to stop."
echo ""

bundle exec jekyll serve --host 0.0.0.0 --port 4000
