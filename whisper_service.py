import whisper

model = whisper.load_model("base")

def transcribe_audio(
    audio_path: str,
    language: str = "ru",
    temperature: float = 0.0,
    beam_size: int = 5,
    best_of: int = 5,
    patience: float = 1.0,
    fp16: bool = True
) -> str:
    result = model.transcribe(
        audio_path,
        language=language,
        temperature=temperature,
        beam_size=beam_size,
        best_of=best_of,
        patience=patience,
        fp16=fp16
    )
    return result["text"]
