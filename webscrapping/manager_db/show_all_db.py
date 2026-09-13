import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "parser_history.db"

def select_all_files() :
    '''Функция возвращает весь список статей'''
    with sqlite3.connect(DB_PATH) as connection :
        df = pd.read_sql_query("SELECT id, site_name, post_time,title,link,is_read FROM articles",connection)
    return df

if __name__ == "__main__" :
    print(select_all_files())
