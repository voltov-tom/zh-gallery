import os
import tempfile

from django.core.files.storage import Storage
from django.conf import settings
from webdav3.client import Client


class NextcloudStorage(Storage):
    """Хранилище, которое сохраняет файлы прямо в Nextcloud"""

    def __init__(self):
        # Получаем конфигурацию из settings
        self.config = getattr(settings, 'NEXTCLOUD_CONFIG', {})

        if not self.config:
            raise ValueError("NEXTCLOUD_CONFIG не найден в settings.py!")

        # Проверяем обязательные поля
        required = ['webdav_hostname', 'webdav_login', 'webdav_password', 'webdav_root']
        for field in required:
            if not self.config.get(field):
                raise ValueError(f"В NEXTCLOUD_CONFIG отсутствует поле: {field}")

        # Инициализируем клиент WebDAV
        try:
            options = {
                'webdav_hostname': self.config.get('webdav_hostname', ''),
                'webdav_login': self.config.get('webdav_login', ''),
                'webdav_password': self.config.get('webdav_password', ''),
                'webdav_root': self.config.get('webdav_root', '/'),
                'webdav_timeout': 30,
            }
            self.client = Client(options)

            # Проверяем подключение
            self.client.list()
        except Exception as e:
            raise ConnectionError(f"Ошибка подключения к Nextcloud: {e}")

    def _save(self, name, content):
        """Сохраняет файл в Nextcloud"""
        try:
            # Создаем временный файл
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(name)[1]) as temp_file:
                # Записываем содержимое во временный файл
                for chunk in content.chunks():
                    temp_file.write(chunk)
                temp_file.flush()

                # Создаем директории в Nextcloud если нужно
                remote_dir = os.path.dirname(name)
                if remote_dir:
                    try:
                        self.client.mkdir(remote_dir)
                    except:
                        pass  # Директория уже существует

                # Загружаем файл в Nextcloud
                self.client.upload_sync(
                    remote_path=name,
                    local_path=temp_file.name
                )

                # Удаляем временный файл
                os.unlink(temp_file.name)

            return name

        except Exception as e:
            raise IOError(f"Ошибка сохранения файла в Nextcloud: {e}")

    def url(self, name):
        """Возвращает публичную ссылку на файл"""
        return f"/media/{name}"

    def exists(self, name):
        """Проверяет, существует ли файл в Nextcloud"""
        try:
            return self.client.check(name)
        except:
            return False

    def size(self, name):
        try:
            info = self.client.info(name)
            return info.get('size', 0)
        except:
            return 0
