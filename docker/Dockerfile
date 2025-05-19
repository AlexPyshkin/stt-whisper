# docker/Dockerfile

FROM spbiffi/whisper-base:latest

WORKDIR /app

# Копируем requirements и ставим зависимости без whisper (она уже в base)
COPY ../requirements.txt /app/requirements.txt

# Установим зависимости без whisper (она уже в образе)
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://pypi.org/simple/

# Копируем проект
COPY ../ /app/

# Копируем SSL сертификаты
COPY ../cert.pem /app/cert.pem
COPY ../key.pem /app/key.pem

# Открываем порт
EXPOSE 9099

# Запускаем с SSL
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9099", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]
