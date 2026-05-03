CREATE TABLE IF NOT EXISTS documents (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    author      VARCHAR(255) NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    content     TEXT NOT NULL,
    word_count  INTEGER NOT NULL CHECK (word_count > 0),
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at  TIMESTAMP WITH TIME ZONE DEFAULT NULL
);