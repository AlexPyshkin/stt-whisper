# docker/Dockerfile

FROM spbiffi/whisper-base:latest

WORKDIR /app

# Копируем requirements и ставим зависимости без whisper (она уже в base)
COPY ../requirements.txt /app/requirements.txt

# Установим зависимости без whisper (она уже в образе)
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://pypi.org/simple/

# Копируем проект
COPY ../ /app/

# Запускаем
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9099"]
