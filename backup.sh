#!/bin/bash

set -e

DATE=$(date +%F-%H-%M)
BACKUP_DIR="/tmp/mywebapp-backup-$DATE"

mkdir -p "$BACKUP_DIR"

echo "Starting database backup..."

DB_URL="$DATABASE_URL"

if [ -z "$DB_URL" ]; then
  echo "DATABASE_URL is missing."
  exit 1
fi

DB_USER=$(echo "$DB_URL" | sed -n 's|.*//\([^:]*\):.*|\1|p')
DB_PASS=$(echo "$DB_URL" | sed -n 's|.*//[^:]*:\([^@]*\)@.*|\1|p')
DB_HOST=$(echo "$DB_URL" | sed -n 's|.*@\([^/]*\)/.*|\1|p')
DB_NAME=$(echo "$DB_URL" | sed -n 's|.*/\([^?]*\).*|\1|p')

mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_DIR/db.sql"

gzip "$BACKUP_DIR/db.sql"

echo "Uploading backup to S3..."

aws s3 cp "$BACKUP_DIR/db.sql.gz" "s3://$S3_BUCKET_NAME/backups/$DATE/db.sql.gz"

echo "Backup completed successfully."
