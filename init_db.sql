-- Create database if it doesn't exist
CREATE DATABASE stt;

-- Connect to the database
\c stt;

-- Create schema
CREATE SCHEMA IF NOT EXISTS stt;

-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA stt TO developer; 