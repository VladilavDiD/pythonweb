# users/db.py
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'users.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Таблиця користувачів
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Таблиця турнірів (НОВЕ)
    c.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            game TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Таблиця учасників (хто куди записався) (НОВЕ)
    c.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tournament_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(tournament_id) REFERENCES tournaments(id)
        )
    ''')

    # Створення адміна
    try:
        admin_pass = generate_password_hash("admin123", method='pbkdf2:sha256')
        c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                  ("admin", admin_pass, "admin"))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()


# --- Функції користувачів (залишаються ті самі) ---
def create_user(username, password, role='user'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    p_hash = generate_password_hash(password, method='pbkdf2:sha256')
    try:
        c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', (username, p_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, username, password_hash, role FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[2], password):
        return {'id': user[0], 'username': user[1], 'role': user[3]}
    return None


# --- НОВІ ФУНКЦІЇ ДЛЯ ТУРНІРІВ ---

def create_tournament(name, game, date, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO tournaments (name, game, date, description) VALUES (?, ?, ?, ?)',
              (name, game, date, description))
    conn.commit()
    conn.close()


def get_all_tournaments():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Дозволяє звертатися по назві колонок
    c = conn.cursor()
    c.execute('SELECT * FROM tournaments ORDER BY id DESC')
    return c.fetchall()


def join_tournament_db(user_id, tournament_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Перевірка, чи вже зареєстрований
    c.execute('SELECT * FROM participants WHERE user_id=? AND tournament_id=?', (user_id, tournament_id))
    if c.fetchone():
        conn.close()
        return False  # Вже є

    c.execute('INSERT INTO participants (user_id, tournament_id) VALUES (?, ?)', (user_id, tournament_id))
    conn.commit()
    conn.close()
    return True

def get_user_tournaments(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    sql = '''
    SELECT t.name, t.game, t.date 
    FROM tournaments t
    JOIN participants p ON t.id = p.tournament_id
    WHERE p.user_id = ?
    '''
    c.execute(sql, (user_id,))
    items = c.fetchall()
    conn.close()
    return items