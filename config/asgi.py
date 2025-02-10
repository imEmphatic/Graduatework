import os  # Модуль os для работы с операционной системой, например, для доступа к переменным окружения

from django.core.asgi import (
    get_asgi_application,
)  # Импортируем функцию для получения ASGI-приложения Django

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE, указывающую на настройки проекта Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Получаем ASGI-приложение для запуска асинхронного сервера
application = get_asgi_application()
