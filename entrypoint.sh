#!/bin/sh
set -e

# 🔥 FORZAR VARIABLES (NO confiar en root)
export ODOO_DATABASE_HOST=${PGHOST}
export ODOO_DATABASE_PORT=${PGPORT}
export ODOO_DATABASE_USER=${PGUSER}
export ODOO_DATABASE_PASSWORD=${PGPASSWORD}
export ODOO_DATABASE_NAME=${PGDATABASE}

echo "DB HOST: $ODOO_DATABASE_HOST"
echo "DB USER: $ODOO_DATABASE_USER"

echo "Esperando conexión a PostgreSQL..."

while ! nc -z "$ODOO_DATABASE_HOST" "$ODOO_DATABASE_PORT"; do
  sleep 2
done

echo "Base de datos lista 🚀"

# 🔥 MUY IMPORTANTE: crear DB limpia si no existe
exec odoo \
  --http-port="${PORT:-8069}" \
  --db_host="$ODOO_DATABASE_HOST" \
  --db_port="$ODOO_DATABASE_PORT" \
  --db_user="$ODOO_DATABASE_USER" \
  --db_password="$ODOO_DATABASE_PASSWORD" \
  --database="$ODOO_DATABASE_NAME" \
  --init=base \
  --without-demo=True \
  --addons-path="/mnt/custom_addons,/usr/lib/python3/dist-packages/odoo/addons"