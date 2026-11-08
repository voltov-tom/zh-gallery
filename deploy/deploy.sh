#!/bin/sh
# Деплой на сервере: тянем свежий образ из GHCR и перезапускаем стек.
# Запускается по SSH пользователем deploy (docker без sudo).
#
#   IMAGE_TAG=<sha или тег> ./deploy.sh
set -eu

cd /srv/zh-gallery
: "${IMAGE_TAG:=latest}"
export IMAGE_TAG

echo "[deploy] тянем образ $IMAGE_TAG"
docker compose -f docker-compose.prod.yml pull web

echo "[deploy] поднимаем стек"
docker compose -f docker-compose.prod.yml up -d --remove-orphans

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
