from django.conf import settings
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)


class Service(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Внешний ключ, связывающий сервис с пользователем
    service_name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=255, unique=True)
    container_id = models.CharField(max_length=255, null=True, blank=True)  # Добавляем поле container_id

    def __str__(self):
        return f'{self.service_name} ({self.subdomain})'