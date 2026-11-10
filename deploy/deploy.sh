#!/bin/sh
# Деплой на сервере: синхронизирует конфиги из репозитория, тянет образ и
# перезапускает стек. Запускается по SSH пользователем deploy (docker без sudo).
#
#   IMAGE_TAG=<sha или тег> ./deploy.sh
set -eu

cd /srv/zh-gallery
: "${IMAGE_TAG:=latest}"
export IMAGE_TAG

# Конфиги (compose, nginx, страница техработ) держим в репозитории и
# раскладываем сюда — иначе на сервере остаются устаревшие копии.
if [ -d src/.git ]; then
    echo "[deploy] обновляем конфиги из репозитория"
    git -C src fetch -q origin refactor
    git -C src reset -q --hard origin/refactor
    cp -f src/deploy/docker-compose.prod.yml src/deploy/nginx-prod.conf \
          src/deploy/maintenance.html .
fi

echo "[deploy] тянем образ $IMAGE_TAG"
docker compose -f docker-compose.prod.yml pull web

echo "[deploy] поднимаем стек"
docker compose -f docker-compose.prod.yml up -d --remove-orphans

# Кэш хранит «веб-размер» картинок: чистим старые копии и греем новые в фоне,
# чтобы первые посетители не ждали скачивания из Nextcloud.
echo "[deploy] обновляем кэш медиа в фоне"
docker compose -f docker-compose.prod.yml exec -T web python manage.py media_cache --clear >/dev/null 2>&1 || true
docker compose -f docker-compose.prod.yml exec -d -T web python manage.py media_cache >/dev/null 2>&1 || true

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
