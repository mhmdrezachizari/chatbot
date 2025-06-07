import sqlite3
from datetime import datetime

# اتصال به دیتابیس
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# ساخت جدول کاربران
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language TEXT
)
""")

# ساخت جدول پیام‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    timestamp TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()

# ذخیره کاربر
def save_user(user_id, first_name, last_name, username, language):
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (id, first_name, last_name, username, language)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, first_name, last_name, username, language))
        conn.commit()
        return True
    return False

# ذخیره پیام
def save_message(user_id, text):
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO messages (user_id, text, timestamp)
        VALUES (?, ?, ?)
    """, (user_id, text, timestamp))
    conn.commit()
