#!/bin/sh
set -e

: "${ODOO_DATABASE_HOST:=$PGHOST}"
: "${ODOO_DATABASE_PORT:=$PGPORT}"
: "${ODOO_DATABASE_USER:=$PGUSER}"
: "${ODOO_DATABASE_PASSWORD:=$PGPASSWORD}"
: "${ODOO_DATABASE_NAME:=$PGDATABASE}"

echo "Esperando conexión a PostgreSQL..."

while ! nc -z "$ODOO_DATABASE_HOST" "$ODOO_DATABASE_PORT"; do
  sleep 2
done

echo "DB lista, iniciando Odoo..."

exec odoo \
  --http-port="${PORT:-8069}" \
  --db_host="$ODOO_DATABASE_HOST" \
  --db_port="$ODOO_DATABASE_PORT" \
  --db_user="$ODOO_DATABASE_USER" \
  --db_password="$ODOO_DATABASE_PASSWORD" \
  --database="$ODOO_DATABASE_NAME" \
  --addons-path="/mnt/custom_addons,/usr/lib/python3/dist-packages/odoo/addons"