import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "parser_history.db"

def create_init_db() :
    '''Функция создания БД'''
    with sqlite3.connect(DB_PATH) as connection :
        cursor = connection.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL,
                post_time TEXT,
                title TEXT NOT NULL,
                link TEXT UNIQUE NOT NULL,
                is_read INTEGER DEFAULT 0
                )
        ''')

if __name__ == "__main__" :
    create_init_db()