#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Running migrations..."
for f in "$PROJECT_DIR"/migrations/*.sql; do
    echo "  Applying $(basename "$f")..."
    psql "$DATABASE_URL" < "$f"
done

echo "Running seeds..."
for f in "$PROJECT_DIR"/seeds/*.sql; do
    echo "  Seeding $(basename "$f")..."
    psql "$DATABASE_URL" < "$f" || true
done

echo "Migration complete!"
