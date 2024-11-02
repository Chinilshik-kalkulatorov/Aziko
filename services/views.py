import docker
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
from .models import Service

# Инициализация клиента Docker
docker_client = docker.from_env()

def create_docker_container(service):
    """
    Функция для создания Docker контейнера
    """
    try:
        # Проверка, что контейнер с таким именем уже не запущен
        try:
            existing_container = docker_client.containers.get(service.subdomain)
            if existing_container:
                return False, f"Контейнер с именем '{service.subdomain}' уже существует."
        except docker.errors.NotFound:
            pass  # Контейнер не найден, значит, можно продолжать

        # Создание нового контейнера
        container = docker_client.containers.run(
            "your_docker_image",  # Замените на ваше имя образа
            detach=True,
            name=service.subdomain,
            environment={"SERVICE_NAME": service.service_name},
            ports={'80/tcp': None}  # Пример привязки порта, можно изменить при необходимости
        )
        service.container_id = container.id
        service.save()
        return True, f"Сервис '{service.service_name}' успешно создан на поддомене '{service.subdomain}'."
    except docker.errors.APIError as e:
        return False, str(e)

def create_service_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            
            # Проверка уникальности поддомена
            if Service.objects.filter(subdomain=service.subdomain).exists():
                messages.error(request, "Поддомен уже используется другим сервисом.")
                return render(request, 'create_service.html', {'form': form})

            service.user = request.user  # Связать сервис с текущим пользователем
            success, message = create_docker_container(service)
            if success:
                messages.success(request, message)
                return redirect('dashboard')
            else:
                messages.error(request, f"Ошибка при создании контейнера: {message}")
    else:
        form = ServiceForm()

    return render(request, 'create_service.html', {'form': form})

@login_required
def dashboard(request):
    services = Service.objects.filter(user=request.user)  # Показываем только сервисы текущего пользователя
    return render(request, 'dashboard.html', {'services': services})
