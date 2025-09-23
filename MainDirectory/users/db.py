import sqlite3
from .models import User

def create_user(username, password, role='user'):
    conn = sqlite3.connect('users/users.db')  # Змінено шлях до БД
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
              (username, User(username, password, role).password_hash, role))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('users/users.db')  # Змінено шлях до БД
    c = conn.cursor()
    c.execute('SELECT username, password_hash, role FROM users WHERE username=?', (username,))
    row = c.fetchone()
    conn.close()
    if row:
        user = User(row[0], '', row[2])
        user.password_hash = row[1]
        return user
    return None

def init_db():
    conn = sqlite3.connect('users/users.db')  # Змінено шлях до БД
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    conn.commit()
    conn.close()