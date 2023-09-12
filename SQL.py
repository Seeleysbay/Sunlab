import sqlite3
import bcrypt


def setup_database():
    conn = sqlite3.connect('sun_lab.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        username TEXT PRIMARY KEY,
        password_hash BLOB
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        student_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        status TEXT DEFAULT 'allowed' CHECK(status IN ('allowed', 'revoked'))
    )''')

    # Swipes table setup
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS swipes (
        id INTEGER PRIMARY KEY,
        student_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        direction TEXT CHECK(direction IN ('IN', 'OUT')),
        FOREIGN KEY(student_id) REFERENCES users(student_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS access_history (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        direction TEXT CHECK(direction IN ('IN', 'OUT')),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    admin_password = "password"
    hashed = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT OR IGNORE INTO admins (username, password_hash) VALUES (?, ?)", ("admin", hashed))

    conn.commit()
    conn.close()


setup_database()
