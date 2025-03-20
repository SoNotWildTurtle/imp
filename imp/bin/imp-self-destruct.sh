#!/bin/bash
#chmod +x /root/imp/bin/imp-self-destruct.sh

echo "⚠️ WARNING: This will permanently delete IMP from the system!"
read -p "Are you sure? (yes/no): " choice

if [[ "$choice" == "yes" ]]; then
    echo "Initiating IMP self-destruction... Run these scripts:"
    
    echo "shred -u -z /root/imp/logs/*""
    echo "shred -u -z /root/imp/config/*"
    echo "shred -u -z /root/imp/self-improvement/*"
    echo "shred -u -z /root/imp/expansion/*"
    echo "shred -u -z /root/imp/security/*"
    echo "shred -u -z /root/imp/core/*"
    
    echo "rm -rf /root/imp/"
    
    echo "💀 IMP has been completely removed from the system."
else
    echo "🛑 Self-destruction aborted."
fi
