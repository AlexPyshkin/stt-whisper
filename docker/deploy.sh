#!/bin/bash
source "$(dirname "$0")/.env"


# Прерываем выполнение при ошибке
set -e

# Определяем путь к проекту относительно расположения скрипта
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_PATH="$SCRIPT_DIR"

# Останавливаем и удаляем текущий контейнер, если он уже существует
echo "Удаляем контейнер $APP_NAME..."
docker rm -f "$APP_NAME" || true

# Логинимся в Docker Hub
echo "Выполняется вход в Docker Hub..."
echo $DOCKER_TOKEN | docker login -u "$DOCKER_USERNAME" --password-stdin

if [ $? -ne 0 ]; then
    echo "Ошибка входа в Docker Hub. Проверьте креды."
    exit 1
fi

# Переходим в директорию со скриптом, чтобы найти docker-compose.yml
cd "$SCRIPT_DIR" || exit 1

# Запускаем docker-compose
echo "Запускаем docker-compose..."
docker-compose pull
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "Приложение успешно запущено через Docker Compose!"
else
    echo "Ошибка запуска приложения. Проверьте настройки."
fi
