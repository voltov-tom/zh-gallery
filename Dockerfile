# Образ для прода: Python 3.12 + Django 5.2, запуск от непривилегированного пользователя.
# Стадия `dev` дополнительно ставит инструменты разработки (pytest, ruff) и
# используется сервисом `test` в docker-compose.
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=zh_gallery.settings.production

# gettext нужен для compilemessages (.po -> .mo), libpq — запасной вариант для psycopg
RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Каталоги под тома создаём заранее и отдаём пользователю app:
# иначе named volume достаётся root и collectstatic не сможет писать.
RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/zh_gallery/static /app/zh_gallery/media \
    && chown -R app:app /app

USER app

WORKDIR /app/zh_gallery

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "zh_gallery.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]


FROM base AS dev

USER root
WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements-dev.txt

USER app
WORKDIR /app/zh_gallery

ENTRYPOINT []
CMD ["pytest"]
