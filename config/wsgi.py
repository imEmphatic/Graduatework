import os  # Модуль os для взаимодействия с операционной системой, например, для работы с переменными окружения

from django.core.wsgi import (
    get_wsgi_application,
)  # Импортируем функцию для получения WSGI-приложения Django

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE, указывающую на настройки проекта Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Получаем WSGI-приложение для запуска сервера
application = get_wsgi_application()
