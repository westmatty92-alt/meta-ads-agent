#!/bin/bash
echo "🔄 Syncing from GitHub..."
git remote set-url origin https://github.com/westmatty92-alt/meta-ads-agent.git 2>/dev/null || git remote add origin https://github.com/westmatty92-alt/meta-ads-agent.git
git fetch origin
git reset --hard origin/main
echo "✅ Code synced to latest"
echo ""
echo "🟢 Done. Runbase Pulse is live."
