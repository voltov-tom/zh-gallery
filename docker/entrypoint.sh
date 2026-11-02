#!/bin/sh
# Точка входа контейнера приложения.
# Миграции и сбор статики выполняются только для gunicorn, чтобы `docker compose
# run --rm web pytest` не трогал базу и не зависел от собранной статики.
set -eu

if [ "${1:-}" = "gunicorn" ]; then
    echo "[entrypoint] компиляция переводов"
    python manage.py compilemessages --ignore=.venv >/dev/null 2>&1 || \
        echo "[entrypoint] compilemessages пропущен (нет gettext или .po)"

    echo "[entrypoint] миграции"
    python manage.py migrate --noinput

    echo "[entrypoint] сбор статики"
    python manage.py collectstatic --noinput --clear -v 0
fi

exec "$@"
