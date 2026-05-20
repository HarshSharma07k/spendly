import os
import sqlite3

from flask import current_app
from werkzeug.security import generate_password_hash


def get_db():
    db_path = os.path.join(current_app.root_path, 'spendly.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    row = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return row


def create_user(name, email, password_hash):
    conn = get_db()
    conn.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        (name, email, password_hash),
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if count > 0:
        conn.close()
        return

    pw_hash = generate_password_hash('demo123')
    conn.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', pw_hash),
    )

    user_id = conn.execute(
        'SELECT id FROM users WHERE email = ?', ('demo@spendly.com',)
    ).fetchone()[0]

    expenses = [
        (user_id, 12.50,  'Food',          '2026-05-01', 'Lunch at cafe'),
        (user_id, 45.00,  'Transport',     '2026-05-03', 'Monthly bus pass'),
        (user_id, 120.00, 'Bills',         '2026-05-05', 'Electricity bill'),
        (user_id, 30.00,  'Health',        '2026-05-07', 'Pharmacy'),
        (user_id, 25.00,  'Entertainment', '2026-05-10', 'Movie ticket'),
        (user_id, 80.00,  'Shopping',      '2026-05-12', 'Clothing store'),
        (user_id, 15.00,  'Other',         '2026-05-14', 'Miscellaneous'),
        (user_id, 20.00,  'Food',          '2026-05-14', 'Dinner'),
    ]
    conn.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description)'
        ' VALUES (?, ?, ?, ?, ?)',
        expenses,
    )
    conn.commit()
    conn.close()
