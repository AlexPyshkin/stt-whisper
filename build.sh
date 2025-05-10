
# Определяем путь к проекту относительно расположения скрипта
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_PATH="$SCRIPT_DIR"

# Имя приложения и Docker репозиторий
BASE_IMAGE_NAME="whisper-base"
APP_NAME="whisper-api"
DOCKER_USERNAME=${DOCKER_USERNAME:?Ошибка: переменная среды DOCKER_USERNAME не установлена}
DOCKER_PASSWORD=${DOCKER_PASSWORD:?Ошибка: переменная среды DOCKER_PASSWORD не установлена}
DOCKER_REPO="$DOCKER_USERNAME/$APP_NAME"

# Параметры для SSH
REMOTE_USER="biffi"
REMOTE_HOST="192.168.6.28"
REMOTE_DIR="/home/$REMOTE_USER/workspace/docker/services/$APP_NAME"

echo "Собираем Docker-образ '$APP_NAME' для репозитория '$DOCKER_REPO'..."

# Логинимся в Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin


# Собираем Docker-образ
# Пушим образ в Docker Hub

docker buildx build --platform linux/amd64 -f docker/Dockerfile.base -t "$DOCKER_USERNAME/$BASE_IMAGE_NAME":latest "$PROJECT_PATH"
docker push "$DOCKER_USERNAME/$BASE_IMAGE_NAME":latest

docker buildx build --platform linux/amd64 -f docker/Dockerfile -t "$DOCKER_USERNAME/$APP_NAME":latest "$PROJECT_PATH"
docker push "$DOCKER_USERNAME/$APP_NAME":latest





# Копируем файл .env и папку config на удалённый сервер
echo "Копируем деплой файлы на удалённый сервер..."

cp -r "$PROJECT_PATH/docker/." "/Users/alex_pyshkin/All/repo/Infrastructure/docker/services/$APP_NAME/"
scp -r "$PROJECT_PATH/docker/." "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

echo "Сборка завершёна и файлы успешно скопированы на сервер!"
