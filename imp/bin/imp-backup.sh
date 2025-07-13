#!/bin/bash
# chmod +x ./imp/bin/imp-backup.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="$ROOT_DIR/backups"
BACKUP_FILE="$BACKUP_DIR/imp-backup-$(date +%F).tar.gz"
ENCRYPTED_BACKUP="$BACKUP_FILE.gpg"

mkdir -p "$BACKUP_DIR"

echo "Creating IMP backup..."
tar -czf "$BACKUP_FILE" "$ROOT_DIR/"

echo "Encrypting backup..."
gpg --symmetric --cipher-algo AES256 --output "$ENCRYPTED_BACKUP" "$BACKUP_FILE"

shred -u -z "$BACKUP_FILE"

echo "Backup completed and encrypted."
