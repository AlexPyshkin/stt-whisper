-- Подключаемся к базе данных stt
\c stt;

-- Создаем схему, если она не существует
CREATE SCHEMA IF NOT EXISTS stt;

-- Создаем таблицу whisper
CREATE TABLE IF NOT EXISTS stt.whisper (
    id SERIAL PRIMARY KEY,
    audio_data BYTEA NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    transcribed_text TEXT,
    correct_text TEXT,
    is_processed BOOLEAN DEFAULT FALSE
);

-- Создаем индекс по дате создания для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_whisper_created_at ON stt.whisper(created_at);

-- Даем права на таблицу
GRANT ALL PRIVILEGES ON TABLE stt.whisper TO developer;
GRANT USAGE, SELECT ON SEQUENCE stt.whisper_id_seq TO developer; 