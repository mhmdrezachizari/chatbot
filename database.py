import sqlite3
from datetime import datetime

DB_NAME = "bot_database.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # جدول کاربران
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول پیام‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول تصاویر (ذخیره base64)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            image_base64 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def save_user(user_id: int, first_name: str, last_name: str, username: str, language: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # بررسی وجود کاربر
    cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        conn.close()
        return False  # قبلا ذخیره شده

    cursor.execute('''
        INSERT INTO users (user_id, first_name, last_name, username, language) 
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, first_name, last_name, username, language))

    conn.commit()
    conn.close()
    return True  # کاربر جدید ذخیره شد

def save_message(user_id: int, message: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (user_id, message) VALUES (?, ?)
    ''', (user_id, message))
    conn.commit()
    conn.close()

def save_image(user_id: int, image_base64: str) -> bool:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO images (user_id, image_base64) VALUES (?, ?)
        ''', (user_id, image_base64))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False


# فقط یکبار موقع شروع برنامه اجرا کن برای ساخت جداول:
create_tables()
