# Проект: Django REST API с верификацией по номеру телефона

## Описание

Этот проект представляет собой RESTful API, созданный с использованием Django и Django REST Framework. Он включает в себя следующие возможности:

- **Валидация имени пользователя**: Проверка, содержит ли имя только латинские буквы, преобразование в нижний регистр и проверка на наличие в базе данных.
- **Регистрация пользователей**: Возможность зарегистрировать пользователя с именем и номером телефона.
- **Верификация номера телефона**: Отправка кода подтверждения на номер телефона пользователя и его проверка.
- **Фронтенд интерфейс**: Простые HTML-страницы для взаимодействия с API без необходимости использовать терминал.
- **Документация API**: Автоматически сгенерированная документация с использованием Swagger (drf-yasg).

## Функциональность

- **Валидация имени пользователя**:
  - Проверяет, что имя содержит только латинские буквы и пробелы.
  - Преобразует имя в нижний регистр перед сохранением.
  - Проверяет наличие имени в базе данных.
  
- **Регистрация пользователей**:
  - Принимает имя и номер телефона.
  - Отправляет шестизначный код подтверждения на указанный номер телефона.
  - Сохраняет пользователя в базе данных со статусом "не верифицирован".
  
- **Верификация номера телефона**:
  - Принимает номер телефона и код подтверждения.
  - Проверяет соответствие кода и обновляет статус пользователя на "верифицирован".
  
- **Фронтенд интерфейс**:
  - Страница регистрации пользователя.
  - Страница верификации номера телефона.
  
- **Документация API**:
  - Доступна через Swagger UI и ReDoc.
  - Автоматически генерируется на основе кода.

## Установка

### Предварительные требования

- Python 3.13
- PostgreSQL
- Virtualenv (рекомендуется)
- Аккаунт в сервисе отправки SMS (например, Twilio)

### Шаги установки

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Chinilshik-kalkulatorov/Aziko.git
   cd yourproject
   ```

2. **Создайте и активируйте виртуальное окружение:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env` для хранения конфиденциальных данных:**

   Создайте файл `.env` в корне проекта и добавьте следующие переменные:

   ```env
   SECRET_KEY=your_secret_key
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```

5. **Настройте базу данных PostgreSQL:**

   - Создайте базу данных и пользователя.
   - Обновите настройки базы данных в `settings.py`:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_database_name',
             'USER': 'your_database_user',
             'PASSWORD': 'your_database_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

6. **Выполните миграции:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Создайте суперпользователя (опционально):**

   ```bash
   python manage.py createsuperuser
   ```

## Использование

### Запуск сервера

```bash
python manage.py runserver
```

### API эндпоинты

#### 1. Валидация имени пользователя

- **GET** `/api/service_name/<str:username>/`

  **Описание**: Проверяет, содержит ли имя только латинские буквы, преобразует в нижний регистр и проверяет наличие в базе данных.

  **Пример запроса:**

  ```bash
  curl -X GET "http://127.0.0.1:8000/api/service_name/JohnDoe/"
  ```

  **Пример ответа:**

  ```json
  {"username": "Aki"}
  ```

#### 2. Регистрация пользователя

- **POST** `/api/register/`

  **Описание**: Регистрирует пользователя с именем и номером телефона, отправляет код подтверждения.

  **Тело запроса:**

  ```json
  {
    "name": "Aki",
    "phone_number": "+1234567890"
  }
  ```

  **Пример запроса:**

  ```bash
  curl -X POST "http://127.0.0.1:8000/api/register/" \
       -H "Content-Type: application/json" \
       -d '{"name": "Aki", "phone_number": "+1234567890"}'
  ```

  **Пример ответа:**

  ```json
  {"message": "Verification code sent to your phone"}
  ```

#### 3. Верификация номера телефона

- **POST** `/api/verify_phone/`

  **Описание**: Проверяет код подтверждения и обновляет статус пользователя.

  **Тело запроса:**

  ```json
  {
    "phone_number": "+1234567890",
    "verification_code": "123456"
  }
  ```

  **Пример запроса:**

  ```bash
  curl -X POST "http://127.0.0.1:8000/api/verify_phone/" \
       -H "Content-Type: application/json" \
       -d '{"phone_number": "+1234567890", "verification_code": "123456"}'
  ```

  **Пример ответа:**

  ```json
  {"message": "Phone number verified successfully"}
  ```

### Фронтенд интерфейс

#### 1. Страница регистрации пользователя

- **URL**: `/api/registration/`

**Описание**: Позволяет пользователю ввести имя и номер телефона для регистрации.

#### 2. Страница верификации номера телефона

- **URL**: `/api/phone_verification/`

**Описание**: Позволяет пользователю ввести номер телефона и полученный код для верификации.

### Документация API

Документация доступна в формате Swagger и ReDoc.

- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## Конфигурация

### Отправка SMS

Для отправки SMS используется сервис [Twilio](https://www.twilio.com/). Убедитесь, что вы зарегистрировались и получили необходимые данные для интеграции:

- **ACCOUNT SID**
- **AUTH TOKEN**
- **Номер телефона Twilio**

**Файл `services/utils.py`:**

```python
from twilio.rest import Client
from decouple import config

def send_sms(to_phone_number, verification_code):
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    from_phone_number = config('TWILIO_PHONE_NUMBER')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your verification code is: {verification_code}",
        from_=from_phone_number,
        to=to_phone_number
    )
```

### Переменные окружения

Все конфиденциальные данные должны храниться в файле `.env`.

**Пример `.env`:**

```env
SECRET_KEY=ваш_секретный_ключ
TWILIO_ACCOUNT_SID=ваш_account_sid
TWILIO_AUTH_TOKEN=ваш_auth_token
TWILIO_PHONE_NUMBER=ваш_номер_телефона
```

## Структура проекта

```
docker_service/
├── docker_service/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── services/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   │   └── services/
│   │       ├── register.html
│   │       └── verify_phone.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   └── serializers.py
└── manage.py
```

## Требования

**Файл `requirements.txt`:**

```
Django>=5.1.2
djangorestframework
django-rest-framework
django-rest-framework-simplejwt
psycopg2
twilio
drf-yasg
python-decouple
django-extensions
```

## Полезные команды

- **Применение миграций:**

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- **Создание суперпользователя:**

  ```bash
  python manage.py createsuperuser
  ```

- **Запуск сервера разработки:**

  ```bash
  python manage.py runserver
  ```

- **Просмотр зарегистрированных URL:**

  ```bash
  python manage.py show_urls
  ```
