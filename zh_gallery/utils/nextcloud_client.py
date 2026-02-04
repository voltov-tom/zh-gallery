"""
Клиент для работы с Nextcloud WebDAV
"""

import os
import logging
from django.conf import settings
from webdav3.client import Client
from webdav3.exceptions import RemoteResourceNotFound, RemoteParentNotFound

logger = logging.getLogger('nextcloud')


class NextcloudClient:
    """Клиент для работы с Nextcloud через WebDAV"""

    def __init__(self):
        self.config = getattr(settings, 'NEXTCLOUD_CONFIG', {})
        self.client = None
        self._connect()

    def _connect(self):
        """Устанавливает соединение с Nextcloud"""
        try:
            options = {
                'webdav_hostname': self.config.get('webdav_hostname', ''),
                'webdav_login': self.config.get('webdav_login', ''),
                'webdav_password': self.config.get('webdav_password', ''),
                'webdav_root': self.config.get('webdav_root', ''),
                'webdav_timeout': 30,
            }

            self.client = Client(options)
            # Тестируем соединение
            self.client.list()
            logger.info("Успешное подключение к Nextcloud")

        except Exception as e:
            logger.error(f"Ошибка подключения к Nextcloud: {e}")
            self.client = None

    def is_connected(self):
        """Проверяет, установлено ли соединение"""
        return self.client is not None

    def upload_file(self, local_path, remote_path):
        """
        Загружает файл в Nextcloud

        Args:
            local_path: Локальный путь к файлу
            remote_path: Относительный путь в Nextcloud (от корня webdav_root)

        Returns:
            bool: Успешно ли выполнена загрузка
        """
        if not self.is_connected():
            logger.error("Нет подключения к Nextcloud")
            return False

        try:
            # Проверяем существование локального файла
            if not os.path.exists(local_path):
                logger.error(f"Локальный файл не найден: {local_path}")
                return False

            # Создаем директории если нужно
            remote_dir = os.path.dirname(remote_path)
            if remote_dir:
                self._create_directory(remote_dir)

            # Загружаем файл
            self.client.upload_sync(remote_path=remote_path, local_path=local_path)
            logger.info(f"Файл загружен в Nextcloud: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"Ошибка загрузки файла в Nextcloud: {e}")
            return False

    def download_file(self, remote_path, local_path):
        """
        Скачивает файл из Nextcloud

        Args:
            remote_path: Относительный путь в Nextcloud
            local_path: Локальный путь для сохранения

        Returns:
            bool: Успешно ли выполнено скачивание
        """
        if not self.is_connected():
            logger.error("Нет подключения к Nextcloud")
            return False

        try:
            # Создаем локальную директорию если нужно
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)

            # Скачиваем файл
            self.client.download_sync(remote_path=remote_path, local_path=local_path)
            logger.info(f"Файл скачан из Nextcloud: {remote_path}")
            return True

        except RemoteResourceNotFound:
            logger.error(f"Файл не найден в Nextcloud: {remote_path}")
            return False
        except Exception as e:
            logger.error(f"Ошибка скачивания файла из Nextcloud: {e}")
            return False

    def delete_file(self, remote_path):
        """
        Удаляет файл из Nextcloud

        Args:
            remote_path: Относительный путь в Nextcloud

        Returns:
            bool: Успешно ли выполнено удаление
        """
        if not self.is_connected():
            logger.error("Нет подключения к Nextcloud")
            return False

        try:
            if self.client.check(remote_path):
                self.client.clean(remote_path)
                logger.info(f"Файл удален из Nextcloud: {remote_path}")
                return True
            else:
                logger.warning(f"Файл не найден в Nextcloud для удаления: {remote_path}")
                return False

        except Exception as e:
            logger.error(f"Ошибка удаления файла из Nextcloud: {e}")
            return False

    def file_exists(self, remote_path):
        """
        Проверяет существование файла в Nextcloud

        Args:
            remote_path: Относительный путь в Nextcloud

        Returns:
            bool: Существует ли файл
        """
        if not self.is_connected():
            return False

        try:
            return self.client.check(remote_path)
        except Exception:
            return False

    def list_files(self, remote_directory=''):
        """
        Список файлов в директории Nextcloud

        Args:
            remote_directory: Относительный путь к директории

        Returns:
            list: Список файлов или пустой список при ошибке
        """
        if not self.is_connected():
            return []

        try:
            return self.client.list(remote_directory)
        except Exception as e:
            logger.error(f"Ошибка получения списка файлов: {e}")
            return []

    def _create_directory(self, remote_directory):
        """
        Создает директорию в Nextcloud (рекурсивно)

        Args:
            remote_directory: Относительный путь к директории
        """
        if not self.is_connected():
            return

        try:
            # Проверяем существование директории
            if not self.client.check(remote_directory):
                # Создаем родительские директории
                parent_dir = os.path.dirname(remote_directory)
                if parent_dir and parent_dir != '.':
                    self._create_directory(parent_dir)

                # Создаем директорию
                self.client.mkdir(remote_directory)
                logger.debug(f"Создана директория в Nextcloud: {remote_directory}")

        except Exception as e:
            logger.error(f"Ошибка создания директории: {e}")


# Синглтон экземпляр клиента
_client_instance = None

def get_nextcloud_client():
    """
    Возвращает экземпляр клиента Nextcloud (синглтон)

    Returns:
        NextcloudClient: Экземпляр клиента
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = NextcloudClient()
    return _client_instance