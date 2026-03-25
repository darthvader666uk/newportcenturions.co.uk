#!/bin/bash
# Development server script for Newport Centurions website
# 
# IMPORTANT: This is a Jekyll development server
# 
# WSL2 USERS: 
#   The server binds to 0.0.0.0:4000 (all network interfaces)
#   Access via: http://<YOUR-WSL-IP>:4000 (NOT localhost)
#   Find WSL IP: hostname -I
#   Example: http://172.30.182.118:4000
# 
# WINDOWS USERS (Direct):
#   Access via: http://localhost:4000
# 
# MAC/LINUX USERS:
#   Access via: http://localhost:4000

echo "🏆 Starting Newport Centurions development server..."
echo ""

# Install dependencies if needed
if [ ! -d "vendor" ]; then
    echo "📦 Installing dependencies (first run only)..."
    bundle install
fi

echo "🚀 Starting Jekyll development server..."
echo ""

# Detect if running in WSL2
# if grep -qi microsoft /proc/version 2>/dev/null; then
    WSL_IP=$(hostname -I | awk '{print $1}')
    echo "✅ WSL2 Detected"
    echo "🌐 Access the site at: http://$WSL_IP:4000"
# else
#     echo "✅ Native Linux/Docker Detected"
#     echo "🌐 Access the site at: http://localhost:4000"
# fi

echo ""
echo "📝 Documentation available at: /dev/docs/DEVELOPMENT.md"
echo "🔄 Changes to files will auto-reload"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

bundle exec jekyll serve --host 0.0.0.0 --port 4000
