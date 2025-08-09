import psycopg2
from psycopg2 import sql
from datetime import datetime
import os

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432)
    )
#for test 
# DB_CONFIG = {
#     'dbname': 'postgres',
#     'user': 'root',
#     'password': '3Ir6oReEd5k2cdsIZsWAh2zG',
#     'host': 'grande-casse.liara.cloud', 
#     'port': 31377
# }

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            image_base64 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

def save_user(user_id: int, first_name: str, last_name: str, username: str, language: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        cursor.close()
        conn.close()
        return False

    cursor.execute('''
        INSERT INTO users (user_id, first_name, last_name, username, language) 
        VALUES (%s, %s, %s, %s, %s)
    ''', (user_id, first_name, last_name, username, language))

    conn.commit()
    cursor.close()
    conn.close()
    return True

def save_message(user_id: int, message: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (user_id, message) VALUES (%s, %s)
    ''', (user_id, message))
    conn.commit()
    cursor.close()
    conn.close()

def save_image(user_id: int, image_base64: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO images (user_id, image_base64) VALUES (%s, %s)
        ''', (user_id, image_base64))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

create_tables()
