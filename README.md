# stt-whisper

pip install -r requirements.txt

sudo apt-get install ffmpeg
brew install ffmpeg

pip install git+https://github.com/openai/whisper.git
pip install torch

check:
curl -X POST "http://localhost:9099/transcribe?file_path=/Users/alex_pyshkin/All/repo/public-gateway-api/message-handler/target/voices/voice_1746856294684.ogg"
curl -X POST "http://localhost:9099/transcribe?file_url=https://api.telegram.org/file/bot7947470891:AAHxLjsc9yUWOUBcKewmuB9-wiZAKkNmay4/voice/file_18.oga"
curl -X POST "http://localhost:9099/transcribe" -F "uploaded_file=@/path/to/audio.ogg"