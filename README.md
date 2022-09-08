# API сервиса Yamdb

Эндпоинты для работы через API:

- auth - Регистрация пользователей и выдача токенов
  - auth/signup/ - Регистрация нового пользователя
  - auth/token/ - Получение JWT-токена
- categories/ - Категории (типы) произведений
- genres/ - Категории жанров
- titles/ - Произведения, к которым пишут отзывы (определённый фильм, книга
или песенка)
- titles/{title_id}/reviews/ - Отзывы
- titles/{title_id}/reviews/{review_id}/comments/ - Комментарии к отзывам
- users/ - Пользователи


## Как запустить проект
Клонировать репозиторий:
```
git clone git@github.com:enjoywg/infra_sp2.git
```

Перейти в каталог с docker-compose 
```
cd infra_sp2/infra
```

Запустить создание контейнеров:
```
docker-compose up -d
```

Выполнить миграции:
```
docker-compose exec web python manage.py migrate
```

Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```

Создать суперюзера
```
docker-compose exec web python manage.py createsuperuser
```

Выполнить первоначальное наполнение базы данных:
```
docker-compose exec web python manage.py fill_db
```


## Шаблон наполнения env-файла
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```


## Используемые технологии
- Django 2.2.16
- Django-rest-framework 3.12.4
- Simplejwt 5.2.0
- Docker


## Авторы
- [AnthonyBass](https://github.com/AnthonyBass)
- [Kilurk](https://github.com/Kilurk)
- [enjoywg](https://github.com/enjoywg)
