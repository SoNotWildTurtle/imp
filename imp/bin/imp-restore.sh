#!/bin/bash
#chmod +x /root/imp/bin/imp-restore.sh

echo "🔄 Restoring IMP from backup..."
read -p "Enter the backup file name: " BACKUP_FILE

if [[ ! -f "/root/imp-backups/$BACKUP_FILE" ]]; then
    echo "❌ Backup file not found!"
    exit 1
fi

echo "🔓 Decrypting backup..."
gpg --output "/root/imp-restored.tar.gz" --decrypt "/root/imp-backups/$BACKUP_FILE"

echo "📦 Extracting backup..."
tar -xzf "/root/imp-restored.tar.gz" -C /root/

shred -u -z "/root/imp-restored.tar.gz"

echo "✅ IMP has been restored successfully."
