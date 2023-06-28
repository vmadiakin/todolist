# Указываем базовый образ, содержащий Python 3.10 и уменьшенный размер (slim)
FROM python:3.11-slim

# Устанавливаем зависимости, необходимые для сборки некоторых пакетов
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry для управления зависимостями и создания виртуального окружения
RUN pip install poetry

# Копируем файлы с зависимостями проекта и файлы с poetry.lock и pyproject.toml
COPY poetry.lock pyproject.toml /app/

# Устанавливаем зависимости проекта с помощью poetry
WORKDIR /app
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем код проекта в контейнер
COPY . /app

# Открываем порт, на котором будет работать ваш бэкенд
EXPOSE 8000

# Запускаем команду, которая будет запускать ваше приложение при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
