from fastapi import FastAPI, HTTPException, UploadFile, File, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from utils import wrap_response
from whisper_service import transcribe_audio
from typing import Optional
import shutil
import uvicorn
from sqlalchemy.orm import Session
from database import get_db, WhisperRecord

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
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
    uploaded_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
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

        # Читаем аудиофайл в бинарном режиме
        with open(audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()

        # Создаем запись в базе данных
        db_record = WhisperRecord(
            audio_data=audio_data,
            is_processed=False
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        # Транскрибируем аудио
        text = transcribe_audio(
            audio_path,
            language=lang,
            temperature=temperature,
            beam_size=beam_size,
            best_of=best_of,
            patience=patience,
            fp16=fp16
        )

        # Обновляем запись в базе данных
        db_record.transcribed_text = text
        db_record.is_processed = False
        db.commit()

        if file_url or uploaded_file:
            os.remove(audio_path)

        return wrap_response(text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transcriptions")
def get_transcriptions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Получить историю транскрибаций
    """
    records = db.query(WhisperRecord).order_by(WhisperRecord.created_at.desc()).offset(skip).limit(limit).all()
    return [
        {
            "id": record.id,
            "created_at": record.created_at,
            "transcribed_text": record.transcribed_text,
            "correct_text": record.correct_text,
            "is_processed": record.is_processed
        }
        for record in records
    ]

@app.put("/transcriptions/{record_id}/correct")
def update_correct_text(
    record_id: int,
    correct_text: str,
    db: Session = Depends(get_db)
):
    """
    Обновить правильный текст для записи
    """
    record = db.query(WhisperRecord).filter(WhisperRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    record.correct_text = correct_text
    db.commit()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )
