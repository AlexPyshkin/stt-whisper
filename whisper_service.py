# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
import whisper

# Загружаем модель один раз при инициализации модуля
model = whisper.load_model("base")  # или "tiny", "small"

def transcribe_audio(audio_path: str, language: str = "ru") -> str:
    """
    Распознаёт текст из аудиофайла
    :param file_path: путь к аудиофайлу
    :return: распознанный текст
    """
    result = model.transcribe(audio_path, language=language)
    return result["text"]
