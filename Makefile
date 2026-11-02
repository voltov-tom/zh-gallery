# Короткие команды для повседневной работы.
# Все docker-команды используют проект zh_gallery и порт 8080.

.DEFAULT_GOAL := help
PYTHON ?= python3

help:  ## Показать список команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# --- Docker ---------------------------------------------------------------
up:  ## Поднять стек (db, redis, web, nginx, mailpit)
	docker compose up --build -d

down:  ## Остановить стек
	docker compose down

logs:  ## Логи приложения
	docker compose logs -f web

migrate:  ## Применить миграции
	docker compose run --rm web python manage.py migrate

demo:  ## Наполнить базу демо-данными
	docker compose run --rm web python manage.py seed_demo --reset

superuser:  ## Создать суперпользователя
	docker compose run --rm web python manage.py createsuperuser

shell:  ## Django shell
	docker compose run --rm web python manage.py shell

# --- Разработка -----------------------------------------------------------
test:  ## Запустить тесты
	docker compose run --rm web pytest

test-cov:  ## Тесты с покрытием
	docker compose run --rm web pytest --cov --cov-report=term-missing

lint:  ## Проверить код ruff-ом
	docker compose run --rm web ruff check .

format:  ## Отформатировать код ruff-ом
	docker compose run --rm web ruff format .
	docker compose run --rm web ruff check --fix .

migrate-check:  ## Проверить, что миграции актуальны
	docker compose run --rm web python manage.py makemigrations --check --dry-run

# --- Локальный запуск без Docker -----------------------------------------
install:  ## Установить зависимости в текущее окружение
	$(PYTHON) -m pip install -r requirements-dev.txt

run:  ## Запустить dev-сервер (settings.local)
	cd zh_gallery && $(PYTHON) manage.py runserver

check:  ## django check + миграции
	cd zh_gallery && $(PYTHON) manage.py check
	cd zh_gallery && $(PYTHON) manage.py makemigrations --check --dry-run

messages:  ## Обновить .po после правки шаблонов
	cd zh_gallery && $(PYTHON) manage.py makemessages -l ru -e html,py --ignore=.venv

compile-messages:  ## Собрать .mo из .po
	cd zh_gallery && $(PYTHON) manage.py compilemessages --ignore=.venv

.PHONY: help up down logs migrate demo superuser shell test test-cov lint format migrate-check install run check messages compile-messages
