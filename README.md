Реализован REST-сервис просмотра текущей зарплаты и даты следующего повышения. Сотрудник может видеть только свою сумму. Реализован
метод где по логину и паролю сотрудника будет выдан секретный токен, который действует в течение 30 мин. Запрос
данных о зарплате совершается только при предъявлении валидного токена.
## Запуск через Docker:
- Собираем образ:
  docker build -t my_fastapi_app .
- Запускаем контейнер:
  docker run -d -p 80:80 my_fastapi_app
- можно убедиться в работоспособности через SwaggerUI
  http://127.0.0.1/docs
  Тестовые данные для входа:
  логин: "petr"
  пароль: mameev

Запуск через виртуальное окружение:
### для Windows
- создаем виртуальное окружение:
  python -m venv .venv
- активируем:
  python venv/Scripts/activate
- устанавливаем зависимости:
  pip install -r requirements.txt
- запускаем сервер:
- uvicorn main:app --reload
- создаем базу данных:
  python sql_db.py 

### для IOS и Linux
- создаем виртуальное окружение:
  python3 -m venv .venv
- активируем:
  source venv/bin/activate
- устанавливаем зависимости:
  pip install -r requirements.txt
- запускаем сервер:
  uvicorn main:app --reload
- создаем базу данных:
  python3 sql_db.py


После запуска сервера, сервис будет доступен по адресу http://127.0.0.1:8000
Проверка API-эндпоинтов в SwaggerUI: http://127.0.0.1:8000/docs 
  
