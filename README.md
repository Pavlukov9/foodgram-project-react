# Проект Foodgram

Сайт для публикации рецептов.

## Описание проекта

- это "продуктовый помощник". С помощью этого сервиса люди могут делиться своими рецептами, подписываться на рецепты других пользователей, добавлять рецепты в избранное, а также скачивать список продуктов, которые нужны для блюда.

## Технологии

- Python
- Django
- Django REST Framework
- PostgreSQL
- Nginx
- Gunicorn
- Docker
- GitHub Actions

## Запустить проект локально:

1. Склонировать репозиторий на Ваш компьютер:

``` 
https://github.com/Pavlukov9/foodgram-project-react.git 
```

2. Создать и активировать виртуальное окружение:

``` 
python -m venv venv 
```
```
 source venv/Scripts/activate
  ```

3. Установить зависимости:

``` 
pip install -r requirements.txt
```

4. Выполнить миграции:

``` 
python3 manage.py migrate
```

5. Запустить проект локально:

``` 
python manage.py runserver 
```

## Запустить проект на сервере:

1. Установить на сервер Docker и Docker-compose:

``` 
sudo apt update
 ```
``` 
sudo apt install curl 
```
```
sudo -fSL https://get.docker.com -o get-docker.sh 
```
``` 
sudo sh ./get-docker.sh 
```
``` 
sudo apt-get install docker-compose-plugin 
```

2. Скопировать на сервер файлы `docker-compose.yml`, `nginx.conf` и `.env`.

3. Добавить в .env следующие данные:

```
POSTGRES_DB= ... (имя БД)
POSTGRES_USER= ... (логин для подключения к БД)
POSTGRES_PASSWORD= ... (пароль для БД)
DB_HOST= ... (название БД)
DB_PORT=5432 
SECRET_KEY= ... (секретный ключ)
DEBUG= ...
ALLOWED_HOSTS= ...
```

4. Добавить в Secrets на GitHub следующие данные:

```
DOCKER_PASSWORD= # (пароль от аккаунта на DockerHub)
DOCKER_USERNAME= # (username в аккаунте на DockerHub)
HOST= # (IP удалённого сервера)
USER= # (логин на удалённом сервере)
SSH_KEY= # (SSH-key компьютера, с которого будет происходить подключение) к удалённому серверу
PASSPHRASE= # (фраза-пароль для ssh)
TELEGRAM_TO= # (ID пользователя в Telegram)
TELEGRAM_TOKEN= # (ID бота в Telegram)
```

5. Выполнить в терминате команды:

``` 
git add . 
```
``` 
git commit -m "<Название коммита>" 
```
``` 
git push 
```

6. При успешном исходе, Вам придет сообщение в Telegram о том, что деплой выполнен успешно.

7. После этого нужно создать суперпользователя:

``` 
sudo docker compose exec backend python manage.py createsuperuser
```

## Документация к API:

Документация доступна по ссылке:

(http://foodgramfinal.sytes.net/api/docs/)

## Сайт:

(http://foodgramfinal.sytes.net/)

## Автор проекта:

[Павлюков Даниил](https://github.com/Pavlukov9)
