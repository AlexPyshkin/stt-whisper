# stt-whisper

# prepare
pip install -r requirements.txt

sudo apt-get install ffmpeg
brew install ffmpeg

pip install git+https://github.com/openai/whisper.git
pip install torch

# run
uvicorn main:app --host 0.0.0.0 --port 9099


# check:
curl -X POST "https://localhost:9099/transcribe?file_path=/Users/alex_pyshkin/All/repo/public-gateway-api/message-handler/target/voices/voice_1746856294684.ogg&lang=ru&temperature=0&beam_size=10"

curl -X POST "https://localhost:9099/transcribe?file_url=https://api.telegram.org/file/bot7947470891:AAHxLjsc9yUWOUBcKewmuB9-wiZAKkNmay4/voice/file_18.oga&lang=ru&temperature=0.2&beam_size=5"

curl -X POST "https://localhost:9099/transcribe?lang=ru&temperature=0.2&beam_size=5" \
  -F "uploaded_file=@/Users/alex_pyshkin/All/repo/public-gateway-api/message-handler/target/voices/voice_1746856294684.ogg"