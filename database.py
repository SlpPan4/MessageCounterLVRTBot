import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date

DATABASE_URL = os.getenv("DATABASE_URL")  # Railway выдаёт эту переменную

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                user_id BIGINT,
                username TEXT,
                chat_id BIGINT,
                date DATE,
                count INTEGER,
                PRIMARY KEY (user_id, chat_id, date)
            )
            """)
        conn.commit()

def add_message(user_id: int, username: str, chat_id: int):
    today = date.today()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO messages (user_id, username, chat_id, date, count)
            VALUES (%s, %s, %s, %s, 1)
            ON CONFLICT (user_id, chat_id, date)
            DO UPDATE SET count = messages.count + 1
            """, (user_id, username, chat_id, today))
        conn.commit()

def get_stats_today(chat_id: int):
    today = date.today()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT username, count
            FROM messages
            WHERE chat_id = %s AND date = %s
            ORDER BY total DESC
            """, (chat_id, today))
            return cur.fetchall()

def get_stats_month(chat_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT username, SUM(count) AS total
            FROM messages
            WHERE chat_id = %s AND DATE_TRUNC('month', date) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY username
            ORDER BY total DESC
            """, (chat_id,))
            return cur.fetchall()

def get_stats_prev_month(chat_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT username, SUM(count) AS total
            FROM messages
            WHERE chat_id = %s 
                AND DATE_TRUNC('month', date) = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
            GROUP BY username
            ORDER BY total DESC
            """, (chat_id,))
            return cur.fetchall()

def get_stats_week(chat_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT username, SUM(count) AS total
            FROM messages
            WHERE chat_id = %s 
                AND DATE_TRUNC('week', date) = DATE_TRUNC('week', CURRENT_DATE)
            GROUP BY username
            ORDER BY total DESC
            """, (chat_id,))
            return cur.fetchall()

def get_stats_prev_week(chat_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT username, SUM(count) AS total
            FROM messages
            WHERE chat_id = %s 
                AND DATE_TRUNC('week', date) = DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week')
            GROUP BY username
            ORDER BY total DESC
            """, (chat_id,))
            return cur.fetchall()
