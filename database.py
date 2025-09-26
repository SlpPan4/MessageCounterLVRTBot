import sqlite3
from datetime import date

DB_NAME = "messages.db"

def init_db():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            user_id INTEGER,
            username TEXT,
            chat_id INTEGER,
            date DATE,
            count INTEGER,
            PRIMARY KEY (user_id, chat_id, date)
        )
        """)

def add_message(user_id: int, username: str, chat_id: int):
    today = date.today().isoformat()
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
        INSERT INTO messages (user_id, username, chat_id, date, count)
        VALUES (?, ?, ?, ?, 1)
        ON CONFLICT(user_id, chat_id, date)
        DO UPDATE SET count = count + 1
        """, (user_id, username, chat_id, today))
        db.commit()

def get_stats_today(chat_id: int):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.execute("""
        SELECT username, count FROM messages
        WHERE chat_id = ? AND date = date('now')
        ORDER BY count DESC
        """, (chat_id,))
        return cursor.fetchall()

def get_stats_month(chat_id: int):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.execute("""
        SELECT username, SUM(count) FROM messages
        WHERE chat_id = ? AND date >= date('now','-30 days')
        GROUP BY username
        ORDER BY count DESC
        """, (chat_id,))
        return cursor.fetchall()

def get_stats_week(chat_id: int):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.execute("""
        SELECT username, SUM(count) FROM messages
        WHERE chat_id = ? AND date >= date('now','-7 days')
        GROUP BY username
        ORDER BY count DESC
        """, (chat_id,))
        return cursor.fetchall()
