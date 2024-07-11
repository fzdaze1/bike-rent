# Установка и запуск
# Через Docker
1) Клонировать репозиторий
   ```
   git clone https: // github.com/fzdaze1/bike-rent.git
   ```
2) Перейти в директорию проекта
   ```
   cd bike-rent
   ```
3) Создать .env файл в корневой директории проекта и указать необходимые окружения - пример в файле .env.example
4) Выполнить команду для запуска проекта. Эта команда соберёт и запустит все контейнеры, описанные в файле docker-compose.yml
   ```
   docker compose up - d - -build
   ```
5) Выполнить команду для миграций в БД(также там заранее заложены велосипеды для примера)
   ```
   docker compose exec web python manage.py migrate
   ```
6) Провести тесты при желании можно с помощью pytest(файл с тестами в директории app/rental/tests.py
   ```
   docker compose exec web python - m pytest
   ``` 

# Локальный запуск
1) Клонировать репозиторий и перейти в директорию
   ```
   git clone https: // github.com/fzdaze1/bike-rent.git
   git cd bike-rent
   ```
2) Создать и активировать виртуальное окружение
   ```
   python - m venv venv
   venv\Scripts\activate
   ```
3) Установить зависимости
   ```
   pip install - r requirements.txt
   ```
4) Создать .env файл в корневой директории проекта. Содержание в примере .env.example
5) Выполнить миграции
   ```
   python manage.py migrate
   ```
6) Запустить сервер разработки
   ```
   python manage.py runserver
   ```
# Ссылки для ручной проверки
1) localhost/api/register / - регистрация пользователя
```http
POST / api/users/register /
Content-Type: application/json

{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}
```
2) localhost/api/token / - получение токена для пользователя
```http
POST / api/token /
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpassword"
}
```
3) localhost/api/token/refresh - для обновления токена пользователя
```http
POST / api/users/token/refresh /
Content-Type: application/json

{
    "refresh": "token",
}
```
4) localhost/api/bikes / - GET список доступных велосипедов (отфильтрован по статусу 'available'), (Headers должен включать в себя ключ Authorization со значением Bearer < token > )
```http
GET / api/bikes /
Authorization: Bearer < token >
```
5) localhost/api/rent/<bike_id> - POST для аренды велосипеда (Headers должен включать в себя ключ Authorization со значением Bearer < token > )
```http
POST / api/rent/<bike: id > /
Authorization: Bearer < token >
```
6) localhost/api/return/<bike_id> - POST для возврата велосипеда - будет рассчитано время аренды и стоимость с условной ценой 300 руб/час (Headers должен включать в себя ключ Authorization со значением Bearer < token > )
```http
POST / api/return / <bike: id > /
Authorization: Bearer < token >
```
При возврате велосипеда вы получите сообщение Bike returned successfully. Mail error. Так как я использовал свою почту от google при уведомлении

7) localhost/api/history / - GET для получения истории аренд пользователя - айди действия аренды, айди пользователя, айди байка и данные об аренде, включая времия и стоимость, (Headers должен включать в себя ключ Authorization со значением Bearer < token > )
```http
POST / api/history /
Authorization: Bearer < token >
```
8)[Документация SWAGGER UI](localhost/api/docs/)
# Проект реализован с использованием Celery, Redis и PostgreSQL
