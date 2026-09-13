import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "parser_history.db"

def change_status(id) :
    '''Функция меняет статус статьи'''
    with sqlite3.connect(DB_PATH) as connection :
        cursor = connection.cursor()
        query = "UPDATE articles SET is_read = 1 WHERE id = ?"
        cursor.execute(query,(id,))