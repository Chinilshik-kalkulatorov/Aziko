from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ServiceViewSet, dashboard, create_service
from . import views


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', create_service, name='create_service'),
    path('create_service/', views.create_service, name='create_service'),
    path('api/services/<int:pk>/create_container/', views.ServiceViewSet.as_view({'post': 'create_container'}), name='create_container'),
    path('api/services/<int:pk>/stop_container/', views.ServiceViewSet.as_view({'post': 'stop_container'}), name='stop_container'),
    path('api/services/<int:pk>/remove_container/', views.ServiceViewSet.as_view({'post': 'remove_container'}), name='remove_container'),

]
