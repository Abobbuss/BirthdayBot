import sqlite3
import os
from typing import Tuple, List, Optional

from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()
DB_PATH = os.getenv("DB_PATH", "database.db")

def init_db():
    """Инициализирует базу данных, если она не существует."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создание таблицы пользователей с новым полем username
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            username TEXT
        )
    ''')

    # Создание таблицы историй
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()


def user_exists(telegram_id) -> bool:
    """Проверяет, существует ли пользователь с заданным Telegram ID в БД."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists


def add_user(telegram_id, full_name, username=None) -> None:
    """Добавляет нового пользователя в БД."""
    if user_exists(telegram_id):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Вставка пользователя с полем username
    cursor.execute(
        "INSERT INTO users (telegram_id, full_name, username) VALUES (?, ?, ?)",
        (telegram_id, full_name, username)
    )

    conn.commit()
    conn.close()


def get_user_id_by_username(username):
    """Возвращает ID пользователя по его Telegram username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def get_full_name_by_user_id(user_id):
    """Возвращает полное имя пользователя по его ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT full_name FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def get_all_users_except(exclude_user_id):
    """Возвращает всех пользователей, кроме указанного."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT telegram_id FROM users WHERE id != ?", (exclude_user_id,))
    users = cursor.fetchall()

    conn.close()

    return [{"telegram_id": user[0]} for user in users]