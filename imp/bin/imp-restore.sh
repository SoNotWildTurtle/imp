#!/bin/bash
# chmod +x ./imp/bin/imp-restore.sh

echo "🔄 Restoring IMP from backup..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$ROOT_DIR/backups"

read -p "Enter the backup file name: " BACKUP_FILE

if [[ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]]; then
    echo "❌ Backup file not found!"
    exit 1
fi

echo "🔓 Decrypting backup..."
RESTORED_TAR="$ROOT_DIR/restored.tar.gz"
gpg --output "$RESTORED_TAR" --decrypt "$BACKUP_DIR/$BACKUP_FILE"

echo "📦 Extracting backup..."
PARENT_DIR="$(cd "$ROOT_DIR/.." && pwd)"
tar -xzf "$RESTORED_TAR" -C "$PARENT_DIR"

shred -u -z "$RESTORED_TAR"

echo "✅ IMP has been restored successfully."
