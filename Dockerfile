# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости
RUN poetry install --no-dev

# Копируем код приложения
COPY . /app/

# Запускаем сервер
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]