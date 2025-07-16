#!/bin/bash
# Development server script for Newport Centurions website

echo "🏆 Starting Newport Centurions development server..."

# Install dependencies if needed
if [ ! -d "vendor" ]; then
    echo "📦 Installing dependencies..."
    bundle install
fi

# Start development server
echo "🚀 Starting Jekyll development server..."
echo "🌐 Site will be available at: http://localhost:4000"
echo "🔄 Live reload enabled - changes will be reflected automatically"
echo "⏹️  Press Ctrl+C to stop the server"
echo

bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload --incremental
