# Описание

API Reviews - API для сервиса публикации отзывов на произведения (музыка, фильмы, книги). 

# api_reviews
>API Reviews - это API без лишних деталей. Благодаря этому его легко освоить и доработать. Через приложение уже можно читать информацию о разных произведениях, оставлять отзывы и комментарии к отзывам. Эту основу легко расширить, добавляя новые возможности.

### Технологии:
+ Django==3.2.10
+ djangorestframework==3.12.4
+ PyJWT==2.1.0
+ djangorestframework-simplejwt==5.2.2

#### Как запустить проект:

+ клонируем репозиторий `git clone`
`https://github.com/sabina-045/api_reviews.git`
+ переходим в него `cd api_yamdb`
    + разворачиваем виртуальное окружение:
    `python3 -m venv env` (Windows: `python -m venv env`)
    + активируем его:
    `source env/bin/activate` (Windows: `source env/scripts/activate`)
    + устанавливаем зависимости из файла requirements.txt:
    `pip install -r requirements.txt`
+ выполняем миграции:
`python3 manage.py migrate` (Windows: `python manage.py migrate`)
+ запускаем проект:
`python3 manage.py runserver` (Windows: `python manage.py runserver).
И вперед!

#### Инструкции и примеры

>Основные эндпойнты `/api/v1/`:

/titles/ - список произведений, создается админом.

/titles/{title_id}/ - информация об отдельном произведении.

/titles/{title_id}/reviews/ - список отзывов к отдельному произведению, создание отзыва.

/titles/{title_id}/reviews/comments/{comment_id}/ - информация об отдельном комментарии, изменение комментария автором или модератором.

</br>

>Для доступа к API необходимо получить токен:

Нужно выполнить POST-запрос http://127.0.0.1:8000/api/v1/auth/signup/ передав поля username и email.
На указанный адрес придет письмо с confirmation_code.
Нужно отправить POST-запрос http://127.0.0.1:8000/api/v1/auth/token/ передав поля username и confirmation_code.

Полученный токен передаем в заголовке Authorization: Bearer <токен>

</br>


> Команда создателей:
Яндекс Практикум, Максим Габчак, Андрей Чернышев, Сабина Гаджиева
