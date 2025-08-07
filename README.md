# Notifications service

Сервис для надежной отправки уведомлений пользователям

## Запуск без Docker

1. Установите зависимости:

```console
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

2. Создать базу данных
3. Заменить необходимое в конфигурациях
```console
$ cp .env.temp .env
$ nano .env
```

4. Применить миграции
```console
$ python manage.py migrate
```

4. Создать суперюзера
```console
$ python manage.py createsuperuser
```

5. Запустить сервер
```console
$ python manage.py runserver
```

5. В новой консоле запустить celery
```console
$ celery -A notification_service worker -l info
```

## Запуск с Docker

1. Заменить необходимое в конфигурациях
```console
$ cp .env.temp .env
$ nano .env
```

2. Запустить контейнеры
```console
$ docker compose up --build
```

2. В новой консоле создать суперюзера
```console
$ docker-compose exec web python manage.py createsuperuser
```

## Использование

### Создание пользователей
Перйдите на http://localhost:8000/admin/notifications/user/

### Создание и отправка уведомлеий
- Через UI: http://localhost:8000/admin/notifications/notification/add/
- Через API:
```console
$ curl -X POST http://localhost:8000/api/notifications/ \
  -H "Content-Type: application/json" \
  -d '{
        "user": 1,
        "title": "Test Notification",
        "message": "This is a test message"
      }'
```
