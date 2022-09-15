# API сервиса Yamdb

Yamdb - Сервис-отзовик на книги, фильмы и музыку

Реализован следующий функционал: Регистрация и управление пользователями, добавление отзывов, книг, фильмов, музыки, категорий, жанров и комментариев через api

Работал в команде, отвечал за всю часть, касающуюся управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с токеном, систему подтверждения через e-mail

## Эндпоинты для работы через API:
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


## Используемые технологии
- Python 3.7
- Django 2.2.16
- Django-rest-framework 3.12.4
- Simplejwt 5.2.0
- Docker


## Как запустить проект
Клонировать репозиторий:
```
git clone git@github.com:enjoywg/infra_sp2.git
```

Перейти в каталог с docker-compose 
```
cd infra_sp2/infra
```

Шаблон наполнения env-файла находится в файле .env.example
Скопировать шаблон в рабочее окружение
```
cp ../.env.example .env
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


## Авторы
- [AnthonyBass](https://github.com/AnthonyBass)
- [Kilurk](https://github.com/Kilurk)
- [enjoywg](https://github.com/enjoywg)
