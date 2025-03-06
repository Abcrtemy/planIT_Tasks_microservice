# Используем официальный образ Python
FROM python:3.11

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1  # Не записывать .pyc файлы
ENV PYTHONUNBUFFERED 1        # Обеспечивает вывод в реальном времени

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем код проекта в контейнер
COPY . /app/

# Открываем порт 8000 для приложения
EXPOSE 8000

# Команда запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
