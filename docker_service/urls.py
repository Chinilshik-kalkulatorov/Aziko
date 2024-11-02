from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from services import views as service_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('services.urls')),
    path('dashboard/', service_views.dashboard, name='dashboard'),  # Добавляем маршрут для dashboard
    path('create/', service_views.create_service, name='create_service'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Добавляем путь для авторизации
]
