# users/db.py
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'users.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Створюємо таблицю
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def create_user(username, password, role='user'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Хешуємо пароль (безпечно)
    # pbkdf2:sha256 - стандартний надійний метод
    p_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                  (username, p_hash, role))
        conn.commit()
        conn.close()
        return True  # Успішно
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Користувач вже існує


def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT username, password_hash, role FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()

    if user:
        stored_hash = user[1]
        # Перевіряємо пароль
        if check_password_hash(stored_hash, password):
            return {'username': user[0], 'role': user[2]}

    return None