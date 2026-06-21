Create a file called sync.sh in /home/admin/meta-ads-agent/ with this content:

#!/bin/bash
# Runbase Pulse — One-command sync and deploy
# Run this in Replit Shell after every Claude Code push
# Usage: bash sync.sh

echo "🔄 Syncing from GitHub..."
git remote set-url origin https://github.com/westmatty92-alt/meta-ads-agent.git 2>/dev/null || git remote add origin https://github.com/westmatty92-alt/meta-ads-agent.git
git fetch origin
git reset --hard origin/main
echo "✅ Code synced to latest"

echo "🚀 Restarting server..."
pkill -f "python3 server.py" 2>/dev/null
pkill -f "python3 -m http.server" 2>/dev/null
sleep 1
python3 server.py &
echo "✅ Server restarted"

echo ""
echo "🟢 Done. Runbase Pulse is live."

Push this file to GitHub.
