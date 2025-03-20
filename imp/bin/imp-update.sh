#!/bin/bash
#chmod +x /root/imp/bin/imp-update.sh

echo "🔄 Fetching latest updates for IMP..."
git -C /root/imp pull origin main
python3 /root/imp/self-improvement/imp-code-updater.py
echo "✅ IMP AI has been updated."
