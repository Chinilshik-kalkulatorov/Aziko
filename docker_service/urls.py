from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from services import views as service_views
from rest_framework.authtoken import views as drf_views  # Импортируем представление для получения токена

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', drf_views.obtain_auth_token, name='api_token_auth'),
    path('api/', include('services.urls')),
]
