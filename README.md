#  Django-проект Foodgram.

![](https://github.com/VladSmyslov/foodgram/actions/workflows/main.yml/badge.svg)

##  Описание проекта

Проект «Фудграм» — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд. Это полностью рабочий проект, который состоит из бэкенд-приложения на Django и фронтенд-приложения на React.

##  Адрес сервера, на котором запущен проект

- https://fdgrm.ddns.net/

##  Как работать с репозиторием финального проекта


### Как запустить проект:

Установить Docker

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/foodgram.git
```

Запустить проект:

```
docker compose up
```
Выполнить миграции:

```
docker compose exec backend python manage.py migrate
```

### Как заполнить .env:

Установите модуль python-dotenv с помощью pip.

Создайте файл .env со следующими переменными:
```
POSTGRES_USER - имя пользователя БД.
```
```
POSTGRES_PASSWORD - пароль пользователя БД.
```
```
POSTGRES_DB - название базы данных.
```
```
DB_HOST - адрес, по которому Django будет соединяться с базой данных.
```
```
DB_PORT - порт, по которому Django будет обращаться к базе данных. 5432 — это порт по умолчанию для PostgreSQL.
```
```
SECRET_KEY - секретный ключ
```
```
DEBUG - режим отладки
```
```
ALLOWED_HOSTS - список имен хостов / доменов, на которых может обслуживаться ваш веб-сервер.
```

Добавьте его в файл .gitignore, чтобы git не закоммитил его.

Загрузите конфигурацию в файлы Python с помощью модуля Python-dotenv.

## Стек используемых технологий

- Python. [![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
- Django. [![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
- Django REST Framework. [![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
- PostgreSQL. [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
- Docker. [![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
- Docker-compose. [![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
- GitHub Actions. [![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
- Nginx. [![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)

## Автор

Vladislav Smyslov<br>
**email**: vladisl.smislow2010@yandex.ru_<br>