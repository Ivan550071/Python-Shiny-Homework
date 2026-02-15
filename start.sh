#!/bin/sh
set -e

APP_PATH="${APP_PATH:-a4_ex1/app.py}"

echo "Starting Shiny app: ${APP_PATH}"
exec python -m shiny run --host 0.0.0.0 --port 8000 "$APP_PATH"
