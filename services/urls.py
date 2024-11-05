from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Подключение роутера для users
    path('server_name/<str:username>/', views.server_name, name='server_name'),
    path('server_name/', views.server_name, name='server_name_post'),
]
