#!/bin/bash
#chmod +x /root/imp/bin/imp-backup.sh

BACKUP_FILE="/root/imp-backups/imp-backup-$(date +%F).tar.gz"
ENCRYPTED_BACKUP="/root/imp-backups/imp-backup-$(date +%F).tar.gz.gpg"

mkdir -p /root/imp-backups

echo "📦 Creating IMP backup..."
tar -czf "$BACKUP_FILE" /root/imp/

echo "🔒 Encrypting backup..."
gpg --symmetric --cipher-algo AES256 --output "$ENCRYPTED_BACKUP" "$BACKUP_FILE"

shred -u -z "$BACKUP_FILE"

echo "✅ Backup completed and encrypted."
