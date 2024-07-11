# Bike Rental API
Задачи:
Основные функции
Регистрация нового пользователя:
   - Реализовать API для регистрации нового пользователя.
   - Пользователь должен предоставить информацию: имя, электронную почту и пароль.
   - Пароль должен храниться в зашифрованном виде.

Авторизация пользователя:
   - Реализовать API для авторизации пользователя.
   - Использовать JWT (JSON Web Token) для управления сеансами.

Получение списка доступных велосипедов:
   - Реализовать API для получения списка всех доступных велосипедов.
   - Учитывать текущий статус велосипеда (доступен или арендован).

Аренда велосипеда:
   - Реализовать API для аренды велосипеда.
   - Пользователь может арендовать только один велосипед одновременно.
   - Учитывать время начала аренды.

Возврат велосипеда:
   - Реализовать API для возврата велосипеда.
   - Учитывать время окончания аренды и расчет стоимости аренды.

Получение истории аренды пользователя:
   - Реализовать API для получения истории аренды велосипедов текущего пользователя.

Дополнительные требования

Асинхронные задачи:
  - Используйте Celery для обработки асинхронных задач (например, расчет стоимости аренды).

Тестирование:
  - Реализовать модульные тесты с использованием PyTest.
  - Реализовать интеграционные тесты для проверки работы API.

Развертывание:
  - Используйте Docker для контейнеризации приложения.
  - Настройте CI/CD систему (например, GitLab CI) для автоматического тестирования и развертывания.

Интеграция с облачными технологиями:
  - Выберите одного из популярных облачных провайдеров (AWS, Google Cloud, Яндекс.Облако).
  - Реализуйте интеграцию с облаком для хранения данных или других сервисов (например, отправка уведомлений).

# Установка и запуск через Docker 
1) Клонировать репозиторий git clone https://github.com/fzdaze1/bike-rent.git
2) Перейти в директорию проекта (example: cd bike-rent)
3) Создать .env файл в корневой директории проекта и указать необходимые окружения - пример в файле .env.example
4) Выполнить команду для запуска проекта docker compose up -d --build. Эта команда соберёт и запустит все контейнеры, описанные в файле docker-compose.yml
5) Выполнить команду docker compose exec web pythom manage.py migrate для миграций в БД (также там заранее заложены велосипеды для примера)
6) Провести тесты при желании можно с помощью команды docker compose exec web python -m pytest (файл с тестами в директории app/rental/tests.py

# Ссылки для ручной проверки
1) 127.0.0.1:8000/api/register/ - регистрация пользователя
2) 127.0.0.1:8000/api/token/ - получение токена для пользователя
3) 127.0.0.1:8000/api/token/refresh - для обновления токена пользователя
4) 127.0.0.1:8000/api/bikes/ - GET список доступных велосипедов (отфильтрован по статусу 'available')
5) 127.0.0.1:8000/api/rent/<bike_id> - POST для аренды велосипеда
6) 127.0.0.1:8000/api/return/<bike_id> - POST для возврата велосипеда - будет рассчитано время аренды и стоимость с условной ценой 300 руб/час
7) 127.0.0.1:8000/api/history/ - GET для получения истории аренд пользователя - айди действия аренды, айди пользователя, айди байка и данные об аренде, включая времия и стоимость
8) 127.0.0.1:8000/api/docs/ - документация на SWAGGER UI




