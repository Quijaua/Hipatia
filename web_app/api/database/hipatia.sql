PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    is_activated BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    role TEXT NOT NULL DEFAULT 'common',
    is_activated BOOLEAN NOT NULL DEFAULT 1,
    phone TEXT,
    cpf TEXT
);
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    autor TEXT NOT NULL,
    editor TEXT,
    publish_year INTEGER,
    isbn TEXT,
    category TEXT, localization TEXT
, is_activated BOOLEAN NOT NULL DEFAULT 1);
COMMIT;
