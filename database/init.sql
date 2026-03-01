-- =============================================================================
-- database/init.sql – CareerCompass
-- Made by stealthcoderX | All rights reserved.
-- =============================================================================
-- This file is automatically executed by the MySQL Docker container on its
-- FIRST start (when the data volume is empty).
-- Path in docker-compose: ./database/init.sql:/docker-entrypoint-initdb.d/01_init.sql
--
-- To reset and re-run:
--   docker compose down -v      ← deletes the mysql_data volume
--   docker compose up --build
-- =============================================================================

-- The database itself is already created by MYSQL_DATABASE in docker-compose.
-- We switch to it and create the table.

USE career_quiz;

-- ── Users table ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id               INT          NOT NULL AUTO_INCREMENT,
    name             VARCHAR(100) NOT NULL,
    email            VARCHAR(150) NOT NULL,
    password_hash    VARCHAR(255) NOT NULL,
    predicted_career VARCHAR(100) DEFAULT NULL,
    score_json       TEXT         DEFAULT NULL,
    created_at       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT uq_users_email UNIQUE (email)
)
ENGINE  = InnoDB
DEFAULT CHARSET  = utf8mb4
COLLATE = utf8mb4_unicode_ci;

-- ── Index for fast authentication lookups ────────────────────────────────────
-- Note: The UNIQUE constraint on email already creates an index, so this is optional.
-- Commenting out to avoid redundancy. Uncomment if needed:
-- ALTER TABLE users ADD INDEX idx_users_email (email);

-- ── Confirm ───────────────────────────────────────────────────────────────────
SELECT CONCAT(
    'career_quiz.users table ready. Columns: ',
    GROUP_CONCAT(COLUMN_NAME ORDER BY ORDINAL_POSITION)
) AS status
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'career_quiz'
  AND TABLE_NAME   = 'users';
