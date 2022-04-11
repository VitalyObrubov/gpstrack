# Docker-команда FROM указывает базовый образ контейнера
# Наш базовый образ - это Linux с предустановленным python-3.7
FROM python:3.9
# Скопируем файл с зависимостями в контейнер
#WORKDIR /app#

COPY requirements.txt .
# Установим зависимости внутри контейнера
RUN pip3 install -r requirements.txt
# Скопируем остальные файлы в контейнер
COPY . .
# запускаем скрипт
EXPOSE 8000
CMD ["uvicorn", "gpstrack.asgi:application", "--host", "0.0.0.0", "--port", "8000"]