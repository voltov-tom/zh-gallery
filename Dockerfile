# Используем официальный образ Python
FROM python:3.9.6-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Создаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (нужны для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем папку для статики (чтобы не было ошибок прав доступа)
RUN mkdir -p /app/static /app/media

# Указываем команду запуска (будет переопределена в docker-compose)
CMD ["gunicorn", "zh_gallery.wsgi:application", "--bind", "0.0.0.0:8000"]