#!/bin/bash
set -e

CONTAINER="av3-postgres"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Resetting database..."
docker exec -i $CONTAINER psql -U postgres -d av3 -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

echo "Running migrations..."
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/migrations/001_initial.sql"
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/migrations/002_proposals.sql"
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/migrations/003_fonts.sql"
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/migrations/004_activities_moment_type.sql"
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/migrations/005_coordination_doc_updates.sql"
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/migrations/006_resources.sql"
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/migrations/007_add_phone.sql"

echo "Running seeds..."
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/seeds/seed.sql"
docker exec -i $CONTAINER psql -U postgres -d av3 < "$PROJECT_DIR/seeds/seed_proposals.sql"

echo "Database reset complete!"
