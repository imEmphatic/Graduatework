import os  # Модуль os для взаимодействия с операционной системой, например, для работы с файловой системой и переменными окружения
from datetime import (
    timedelta,
)  # Импортируем класс timedelta для работы с интервалами времени (например, для работы с токенами JWT)
from pathlib import (
    Path,
)  # Импортируем класс Path для работы с путями файлов в операционной системе

from dotenv import (
    load_dotenv,
)  # Функция load_dotenv для загрузки переменных окружения из файла .env

# Получаем путь к корневой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения из файла .env
dot_env = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dot_env)

# Ключ безопасности для проекта (необходим для защиты данных)
SECRET_KEY = os.getenv("SECRET_KEY")

# Режим отладки, рекомендуется отключать в продакшн-режиме
DEBUG = True

# Разрешённые хосты (пустой список означает, что все хосты разрешены)
ALLOWED_HOSTS = []

# Установленные приложения Django
INSTALLED_APPS = [
    "django.contrib.admin",  # Админ-панель Django
    "django.contrib.auth",  # Аутентификация и авторизация пользователей
    "django.contrib.contenttypes",  # Модели контента
    "django.contrib.sessions",  # Сессии пользователей
    "django.contrib.messages",  # Сообщения
    "django.contrib.staticfiles",  # Статические файлы (например, CSS, JS)
    "rest_framework",  # Django REST Framework
    "rest_framework_simplejwt",  # Поддержка JWT
    "users",  # Приложение пользователей
    "corsheaders",  # Заголовки CORS
    "drf_yasg",  # Документация API с помощью Swagger
]

# Middleware — обработчики запросов на сервере
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Безопасность
    "django.contrib.sessions.middleware.SessionMiddleware",  # Сессии
    "django.middleware.common.CommonMiddleware",  # Общие middleware
    "django.middleware.csrf.CsrfViewMiddleware",  # Защита от CSRF атак
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Аутентификация
    "django.contrib.messages.middleware.MessageMiddleware",  # Сообщения
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Защита от Clickjacking
    "corsheaders.middleware.CorsMiddleware",  # Middleware для CORS
]

# Основной URL-обработчик
ROOT_URLCONF = "config.urls"

# Настройки шаблонов Django
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Шаблонизатор Django
        "DIRS": [],  # Папки для поиска шаблонов
        "APP_DIRS": True,  # Автоматический поиск шаблонов в приложениях
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # Данные для отладки
                "django.template.context_processors.request",  # Данные для запросов
                "django.contrib.auth.context_processors.auth",  # Данные аутентификации
                "django.contrib.messages.context_processors.messages",  # Данные сообщений
            ],
        },
    },
]

# Настройки для WSGI (Web Server Gateway Interface)
WSGI_APPLICATION = "config.wsgi.application"

# Настройки базы данных (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Тип базы данных
        "NAME": os.getenv("DB_NAME"),  # Имя базы данных
        "USER": os.getenv("DB_USER"),  # Пользователь базы данных
        "PASSWORD": os.getenv("DB_PASSWORD"),  # Пароль пользователя
        "HOST": os.getenv("DB_HOST"),  # Хост базы данных
        "PORT": os.getenv("DB_PORT"),  # Порт базы данных
    }
}

# Валидаторы паролей для пользователей
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Настройки локализации и временных зон
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True  # Включение международной локализации
USE_TZ = True  # Включение использования часовых поясов

# Настройки для статических файлов
STATIC_URL = "static/"  # URL для статических файлов
MEDIA_URL = "media/"  # URL для медиафайлов
MEDIA_ROOT = (BASE_DIR / "media",)  # Папка для хранения медиафайлов

# Настройка модели пользователя
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

# Настройки Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # Поддержка JWT для аутентификации
    )
}

# Настройки Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # Время жизни Access-токена
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # Время жизни Refresh-токена
    "ROTATE_REFRESH_TOKENS": False,  # Отключение поворота Refresh-токенов
}

# Разрешённые источники для CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # Локальный сервер разработки
    "https://read-and-write.example.com",  # Пример внешнего источника
]

# Доверенные источники для CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://read-and-write.example.com",  # Пример внешнего источника для CSRF
]

# Настройки для Swagger документации
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {
            "type": "basic",  # Описание Basic-аутентификации
        },
        "Bearer": {
            "type": "apiKey",  # Описание Bearer-токенов
            "name": "Authorization",
            "in": "header",
        },
    },
    "JSON_EDITOR": True,  # Включение редактора JSON в Swagger
}

# Настройки CORS
CORS_ALLOW_ALL_ORIGINS = True  # Разрешить все источники
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]  # Разрешённые HTTP-методы
