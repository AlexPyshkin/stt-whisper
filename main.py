from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from utils import wrap_response
from whisper_service import transcribe_audio
from typing import Optional
import shutil
import uvicorn

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost:5173",
        "https://192.168.6.28:5173",  # Добавляем IP адрес
        "http://localhost:5173",
        "http://192.168.6.28:5173"    # Добавляем HTTP версию
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/transcribe")
def transcribe(
    file_path: Optional[str] = Query(None, description="Путь до локального файла"),
    file_url: Optional[str] = Query(None, description="URL до аудиофайла"),
    lang: str = Query("ru"),
    temperature: float = Query(0.0),
    beam_size: int = Query(5),
    best_of: int = Query(5),
    patience: float = Query(1.0),
    fp16: bool = Query(True),
    uploaded_file: Optional[UploadFile] = File(None)
):
    try:
        if file_path:
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="Файл не найден по указанному пути")
            audio_path = file_path

        elif file_url:
            local_filename = "temp_audio_from_url"
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            audio_path = local_filename

        elif uploaded_file:
            local_filename = f"temp_uploaded_{uploaded_file.filename}"
            with open(local_filename, "wb") as f:
                shutil.copyfileobj(uploaded_file.file, f)
            audio_path = local_filename

        else:
            raise HTTPException(status_code=400, detail="Нужен либо file_path, либо file_url, либо файл")

        text = transcribe_audio(
            audio_path,
            language=lang,
            temperature=temperature,
            beam_size=beam_size,
            best_of=best_of,
            patience=patience,
            fp16=fp16
        )

        if file_url or uploaded_file:
            os.remove(audio_path)

        return wrap_response(text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )
