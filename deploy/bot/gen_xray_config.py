"""Собирает конфиг xray для sidecar'а бота из vless-ссылки.

Бот ходит в Telegram через VLESS на KZ. Ссылку выдаёт панель 3x-ui, а
формат xray-конфига руками собирать больно, поэтому один разборщик:

    python deploy/bot/gen_xray_config.py 'vless://…' > config.json

Наружу отдаёт SOCKS5 на 0.0.0.0:1080 — порт не публикуется, доступен только
контейнеру бота внутри compose-сети. Сама ссылка содержит UUID и ключ
Reality, поэтому в репозиторий её не коммитим.
"""

from __future__ import annotations

import json
import sys
from urllib.parse import parse_qs, urlparse

SOCKS_PORT = 1080


def build_config(link: str, socks_port: int = SOCKS_PORT) -> dict:
    url = urlparse(link.strip())
    if url.scheme != "vless":
        raise SystemExit("ожидается vless:// ссылка")
    query = {key: value[0] for key, value in parse_qs(url.query).items()}

    network = query.get("type", "tcp")
    if network != "xhttp":
        raise SystemExit(f"поддерживается только xhttp, получено: {network}")

    extra_raw = query.get("extra", "{}")
    try:
        extra = json.loads(extra_raw)
    except ValueError as error:
        raise SystemExit(f"extra не JSON: {error}") from error
    if query.get("x_padding_bytes") and "xPaddingBytes" not in extra:
        extra["xPaddingBytes"] = query["x_padding_bytes"]

    xhttp = {"path": query.get("path", "/"), "mode": query.get("mode", "auto")}
    if query.get("host"):
        xhttp["host"] = query["host"]
    if extra:
        xhttp["extra"] = extra

    user = {"id": url.username or "", "encryption": query.get("encryption", "none")}
    if query.get("flow"):
        user["flow"] = query["flow"]

    return {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "tag": "socks",
                "listen": "0.0.0.0",
                "port": socks_port,
                "protocol": "socks",
                "settings": {"auth": "noauth", "udp": False},
            }
        ],
        "outbounds": [
            {
                "tag": "proxy",
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": url.hostname,
                            "port": url.port or 443,
                            "users": [user],
                        }
                    ]
                },
                "streamSettings": {
                    "network": network,
                    "security": query.get("security", "none"),
                    "realitySettings": {
                        "serverName": query.get("sni", ""),
                        "fingerprint": query.get("fp", "chrome"),
                        "publicKey": query.get("pbk", ""),
                        "shortId": query.get("sid", ""),
                        "spiderX": query.get("spx", "/"),
                    },
                    "xhttpSettings": xhttp,
                },
            }
        ],
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("использование: gen_xray_config.py 'vless://…'")
    json.dump(build_config(sys.argv[1]), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
