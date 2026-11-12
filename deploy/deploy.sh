#!/bin/sh
# Деплой на сервере: синхронизирует конфиги из репозитория, тянет образ и
# перезапускает стек. Запускается по SSH пользователем deploy (docker без sudo).
#
#   IMAGE_TAG=<sha или тег> ./deploy.sh
set -eu

# Скрипт работает в своём каталоге: прод-стек живёт у пользователя zhdocker
cd "$(dirname "$0")"
: "${IMAGE_TAG:=latest}"
export IMAGE_TAG

echo "[deploy] тянем образ $IMAGE_TAG"
docker compose -f docker-compose.prod.yml pull web

echo "[deploy] поднимаем стек"
docker compose -f docker-compose.prod.yml up -d --remove-orphans

# Конфиг nginx примонтирован файлом: compose его не пересоздаёт, поэтому без
# reload контейнер продолжает работать со старыми правилами. Сначала проверка —
# кривой конфиг не должен уронить сайт, тогда остаёмся на прежнем.
echo "[deploy] перечитываем конфиг nginx"
docker compose -f docker-compose.prod.yml exec -T nginx nginx -t
docker compose -f docker-compose.prod.yml exec -T nginx nginx -s reload

# Кэш хранит «веб-размер» картинок: чистим старые копии и греем новые в фоне,
# чтобы первые посетители не ждали скачивания из Nextcloud.
echo "[deploy] обновляем кэш медиа в фоне"
docker compose -f docker-compose.prod.yml exec -T web python manage.py media_cache --clear >/dev/null 2>&1 || true
docker compose -f docker-compose.prod.yml exec -d -T web python manage.py media_cache >/dev/null 2>&1 || true

# Старые образы копятся по ~380 МБ на деплой. Любой прошлый sha можно снова
# скачать из GHCR, поэтому локально держим только свежие.
echo "[deploy] чистим старые образы"
docker image prune -af --filter "until=72h" >/dev/null 2>&1 || true

echo "[deploy] ждём health"
i=0
while [ "$i" -lt 40 ]; do
    if curl -fsS --max-time 5 https://zh-gallery.ru/healthz/ >/dev/null 2>&1; then
        echo "[deploy] ok: $IMAGE_TAG"
        exit 0
    fi
    i=$((i + 1))
    sleep 5
done

echo "[deploy] smoke не прошёл"
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs --tail 40 web
exit 1
