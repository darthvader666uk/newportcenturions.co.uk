#!/bin/bash
# Build script for Newport Centurions website

echo "🏗️  Building Newport Centurions website..."

# Install dependencies
echo "📦 Installing dependencies..."
bundle install

# Build the site
echo "🚀 Building Jekyll site..."
bundle exec jekyll build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "📁 Site built in _site/ directory"
    echo "🌐 Ready for deployment to GitHub Pages"
else
    echo "❌ Build failed!"
    exit 1
fi
