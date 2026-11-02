![LOGO](https://zh-gallery.ru/static/core/images/logo120x120.png)

# zh-gallery

Учебный Django-проект: галерея работ творческого человека. Категории → подкатегории →
медиа-элементы, лайки, комментарии, страница «О проекте», вход через django-allauth
(включая Google), переводы ru/en, JSON API для Telegram-бота и мобильного клиента.

Сайт: [zh-gallery.ru](https://zh-gallery.ru)

---

## Стек

| Слой | Технологии |
|------|------------|
| Бэкенд | Python 3.12, Django 5.2 LTS |
| Аутентификация | django-allauth 65 (локальные аккаунты + Google OAuth2) |
| БД | PostgreSQL 16 (в тестах — SQLite в памяти) |
| Кэш/сессии | Redis 7 через django-redis (без Redis работает на БД + locmem) |
| Медиа | локальный диск или Nextcloud WebDAV (собственный клиент на `requests`) |
| Фронтенд | Django-шаблоны + Bulma + нативные ES-модули (без Vue/CDN-фреймворков) |
| Деплой | Docker Compose: gunicorn + nginx + Postgres + Redis + Mailpit |
| Качество | pytest + pytest-django, ruff (lint + format), GitHub Actions |

---

## Быстрый старт (Docker)

```bash
cp .env.example .env          # при необходимости поменяйте SECRET_KEY и пароли
make up                       # docker compose up --build -d
make demo                     # демо-категории, картинки и комментарии
```

* сайт — <http://localhost:8080>
* письма (подтверждение регистрации) — <http://localhost:8025>
* админка — <http://localhost:8080/admin/> (`make superuser`)

Полезные команды: `make logs`, `make migrate`, `make shell`, `make down`.

Как устроен стек:

* `init` — короткоживущий сервис, который выставляет владельца томов `static`/`media`
  (иначе Docker создаёт их от root и `collectstatic`/загрузка картинок падают);
* `web` — gunicorn, при старте сам делает `compilemessages`, `migrate` и `collectstatic`;
* `nginx` — раздаёт `/static/` и `/media/` и проксирует остальное на `web:8000`
  (порт публикуется как `8080`, чтобы не мешать боевому стеку на 80/8000);
* `mailpit` — локальный SMTP + веб-интерфейс писем на <http://localhost:8025>;
* `test` (профиль `tools`) — образ с dev-зависимостями для `pytest`/`ruff`.

Перед публикацией по HTTPS выставьте `SECURE_SSL_REDIRECT=True`,
`SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True` и `SECURE_HSTS_SECONDS`,
затем `python manage.py check --deploy` должен быть чистым.

## Запуск без Docker

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
# в .env достаточно:
#   SECRET_KEY=dev
#   SQL_ENGINE=django.db.backends.sqlite3
#   SQL_DATABASE=db.sqlite3
cd zh_gallery && python manage.py migrate && python manage.py runserver
```

`manage.py` по умолчанию использует `zh_gallery.settings.local` (DEBUG=True, письма в консоль).

---

## Структура

```
.
├── docker/                 nginx.conf, entrypoint.sh
├── zh_gallery/             Django-проект
│   ├── core/               галерея
│   │   ├── models.py       категории, элементы, отзывы, About + чистка файлов
│   │   ├── selectors.py    запросы на чтение с annotate/prefetch (без N+1)
│   │   ├── services.py     лайки, просмотры, отзывы (единственное место записи)
│   │   ├── views/          CBV: страницы каталога, информационные страницы, healthz
│   │   ├── api/            JSON API: лайки/отзывы и Telegram-бот
│   │   ├── storage.py      NextcloudStorage (WebDAV) для Django STORAGES
│   │   ├── integrations/   минимальный WebDAV-клиент на requests
│   │   ├── adapters.py     allauth-адаптер: только HTML-письма
│   │   ├── forms.py        форма комментария
│   │   ├── signals.py      синхронизация Site с SITE_DOMAIN после migrate
│   │   └── tests/          pytest-тесты
│   ├── userprofile/        кабинет пользователя и формы allauth
│   ├── zh_gallery/
│   │   └── settings/       base.py / local.py / production.py / test.py
│   ├── templates/          переопределённые шаблоны account/* и robots.txt
│   └── locale/             переводы (po)
├── pyproject.toml          ruff + pytest
├── requirements*.txt
├── docker-compose.yml
└── Makefile
```

Ключевая идея: **вьюхи ничего не знают про ORM**. Чтение — `selectors`, запись — `services`.
Поэтому одна и та же логика лайка используется HTML-страницей, JSON API и Telegram-ботом.

## Настройки

`zh_gallery/settings/base.py` читает переменные окружения через `django-environ`
(файл `.env` в корне репозитория подхватывается автоматически). Полный список с
комментариями — в [`.env.example`](.env.example).

* `SECRET_KEY` — обязателен в production (иначе `ImproperlyConfigured`);
* `DEBUG` — строгий boolean (`DEBUG=False` больше не «истинно» из-за непустой строки);
* `DATABASE_URL` **или** `SQL_*`;
* `REDIS_URL` — пусто означает «работать без Redis»;
* `MEDIA_STORAGE=local|nextcloud`;
* `SITE_DOMAIN` / `SITE_NAME` — домен и имя сайта; после `migrate` объект `Site`
  приводится к этим значениям, иначе ссылки в письмах ведут на `example.com`;
* `TELEGRAM_BOT_TOKEN` — если задан, `/api/telegram_bot/...` требует заголовок `X-Bot-Token`.

Конкретное окружение: `DJANGO_SETTINGS_MODULE=zh_gallery.settings.{local,production,test}`.

## Как быстро проверить

```bash
make up && make demo
curl -s localhost:8080/healthz/            # {"status": "ok", ...}
curl -s localhost:8080/ | grep -c vue      # 0 — Vue больше нет
open http://localhost:8080                 # каталог, лайки, комментарии
open http://localhost:8025                 # письма после регистрации
make test && make lint                     # 105 тестов + ruff
```

## Медиа в Nextcloud

```env
MEDIA_STORAGE=nextcloud
# Вариант 1 — только домен, путь до файлов соберётся сам:
NEXTCLOUD_HOSTNAME=https://cloud.example.com
NEXTCLOUD_LOGIN=user
NEXTCLOUD_PASSWORD=app-password
NEXTCLOUD_ROOT=gallery
# Вариант 2 — полный адрес WebDAV-корня (так было в старом .env проекта,
# поддерживаются старые имена WEBDAV_HOSTNAME / WEBDAV_LOGIN / WEBDAV_PASSWORD / WEBDAV_ROOT):
# NEXTCLOUD_HOSTNAME=https://cloud.example.com/remote.php/dav/files/user/
```

Отдельно про отдачу файлов браузеру: в Nextcloud их нет в локальном каталоге,
поэтому `docker/nginx-nextcloud.conf` проксирует `/media/` в Django, а
`core/views/media.py` стримит файл из хранилища (с кэшем на неделю).
Для локального диска используется обычный `alias` в `docker/nginx.conf`.
Переключение — переменной `NGINX_CONF`.

Проверить связку с базой можно командой:

```bash
docker compose run --rm web python manage.py media_check --download
# Хранилище: core.storage.NextcloudStorage
# Файлов в БД: 31
# Найдено: 31, отсутствует: 0
# Все файлы на месте
```

## Юридические страницы

«Условия и положения» и «Политика конфиденциальности» лежат отдельными файлами
по языкам и подключаются по активной локали:

```
core/templates/core/legal/
├── terms_ru.html      # ГК РФ: авторские права, пользовательский контент, споры
├── terms_en.html
├── privacy_ru.html    # 152-ФЗ: оператор, данные, основания, права субъекта
└── privacy_en.html
```

Тексты — шаблоны под российское право: перед публикацией укажите полные реквизиты
оператора (ФИО/наименование, адрес). Переключение языка — тем же селектором
`ru / en` в шапке; страницы берут локаль из `LANGUAGE_CODE`.

## Переезд на существующую базу

Данные из старой копии проекта переносятся обычным дампом, структура миграций
совместима (0021–0023 дорабатывают её без потери строк):

```bash
# дамп со старого Postgres
docker exec old_db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner' > old.sql
# восстановление в новый контейнер
docker exec -i <new_db> sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
    -c "drop schema public cascade; create schema public;"'
docker exec -i <new_db> sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < old.sql
# затем обычные миграции — 0023 обнулит like_time там, где лайков нет
docker compose run --rm web python manage.py migrate
```

## Тесты и качество

```bash
make test          # pytest в контейнере
make test-cov      # с покрытием
make lint          # ruff check
make format        # ruff format + автофиксы
make migrate-check # миграции соответствуют моделям
```

Тесты идут на SQLite в памяти, с локальным хранилищем и locmem-почтой — внешние
сервисы не нужны.

## Переводы

* `.po` лежат в репозитории, `.mo` собираются при старте контейнера (`compilemessages`);
* после правки шаблонов: `make messages` (обновит `django.po`), затем перевод и `make compile-messages`.

---

## Что изменилось в рефакторинге

### Исправленные баги

| Было | Стало |
|------|-------|
| `like_time = DateTimeField(auto_now=now())` — время последнего *сохранения*, обновлялось при каждом заходе | время последнего лайка, `null` до первого лайка, индекс по убыванию |
| `media_item.likes.create()` в API создавал **пользователя** и падал на первом лайке | лайк через `services.toggle_like` + `select_for_update` |
| JSON API возвращал `200 {"success": false}` и падал 500 на битом body/без ключа | 400/403/404 + `JsonResponse`, разбор body с ошибками |
| `media_item.save()` на каждый просмотр перезаписывал всю строку | `UPDATE ... SET views = views + 1` (F-выражение) |
| Подкатегория и элемент искались только по `slug` → открывались по чужому URL | поиск по всей паре (категория, подкатегория, slug) |
| `get_value` — глобальный фильтр, зарегистрированный в `views.py` | счётчики приходят из `annotate`, фильтр удалён |
| N+1 в шаблонах (`reviews.count`, `total_likes`) | `with_stats()` + `prefetch_related` (зафиксировано тестами на число запросов) |
| `{{ reviews_data|safe }}` + `json.dumps` — XSS через текст комментария | рендер на сервере, данные экранируются Django |
| свои комментарии и лайки нельзя было отредактировать без Vue | нативный `reviews.js` с тем же API |
| `DefaultAccountAdapterCustom` лежал в `utils.py` и **не был подключён** → письма подтверждения не работали | `ACCOUNT_ADAPTER = core.adapters.AccountAdapter` + тест на HTML-письмо |
| `About.objects.all()[0]` — IndexError на пустой таблице | `.first()` + терпимые шаблоны |
| `Telegram: views += 1` без `save()`, `random.choice` падал на пустой базе, домен захардкожен | сохранение через сервис, 404 на пустой базе, `build_absolute_uri` |
| `user.likes` (непонятное имя) и дублирование `my_account`/`account` | `user.liked_items`, общий partial `profile.html` |
| `Vue 2` из CDN + инлайн-скрипты с подстановками шаблона | ES-модули `base.js`, `like.js`, `reviews.js` |
| `DEBUG = os.getenv('DEBUG')` (строка `"False"` — истинна) | `env.bool`, `SECRET_KEY` с проверкой в production |

### Изменения схемы БД

Три новые миграции (`0021`–`0023`): `like_time` становится nullable + индекс, `views` —
`PositiveIntegerField`, у тайтлов снята глобальная уникальность (слаги уникальны внутри
родителя и генерируются один раз), текстовые поля больше не `NULL`, добавлены индексы
по отзывам. Данные не удаляются; миграция 0023 обнуляет `like_time` там, где лайков
нет (раньше там было время последнего сохранения). Порядок миграций проверен на
живой базе старой копии проекта (6 пользователей, 27 работ, 6 комментариев).

### Осознанно не делалось

* **DRF** — пять эндпоинтов не окупают слой сериализаторов; контракт сохранён совместимым.
* **Переименование приложений** (`core` → `gallery`) — потребовало бы переписать историю
  миграций на живой БД; структура наведена внутри приложений.
* Публичные URL (`/api/like/`, `/api/telegram_bot/...`) не менялись, чтобы не сломать
  мобильный клиент и бота.
