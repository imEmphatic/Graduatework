from django.conf.urls.static import (
    static,
)  # Импортируем для обработки статических файлов
from django.contrib import admin  # Импортируем для использования админки Django
from django.urls import include, path  # Импортируем для маршрутизации URL
from drf_yasg import openapi  # Импортируем для работы с открытым API через drf-yasg
from drf_yasg.views import (
    get_schema_view,
)  # Импортируем для генерации документации Swagger
from rest_framework import permissions  # Импортируем классы разрешений для REST API

from config import settings  # Импортируем настройки проекта

# Генерация схемы API с использованием drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",  # Заголовок документации
        default_version="v1",  # Версия API по умолчанию
        description="Test description",  # Описание API
        terms_of_service="https://www.google.com/policies/terms/",  # Условия использования
        contact=openapi.Contact(
            email="contact@snippets.local"
        ),  # Контактный email для вопросов
        license=openapi.License(name="BSD License"),  # Лицензия на API
    ),
    public=True,  # Открытость схемы для всех
    permission_classes=(
        permissions.AllowAny,
    ),  # Разрешения для доступа ко всем (все пользователи)
)

# Маршруты URL для проекта
urlpatterns = [
    path("admin/", admin.site.urls),  # Админка Django
    path(
        "api/users/", include("users.urls", namespace="api_users")
    ),  # Роуты для API пользователей
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # Swagger UI
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),  # ReDoc UI для документации
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # Статические файлы для медиа (например, изображения)
