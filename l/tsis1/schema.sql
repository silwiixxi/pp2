-- =========================
-- GROUPS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- базовые категории
INSERT INTO groups (name)
VALUES
('Family'),
('Work'),
('Friend'),
('Other')
ON CONFLICT (name) DO NOTHING;

-- =========================
-- CONTACTS TABLE (base must exist)
-- =========================
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- расширяем contacts
ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS email VARCHAR(100),
ADD COLUMN IF NOT EXISTS birthday DATE,
ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);

-- =========================
-- PHONES TABLE (1-to-many)
-- =========================
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);