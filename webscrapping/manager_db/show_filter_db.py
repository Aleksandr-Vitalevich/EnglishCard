import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "parser_history.db"

def select_filter_files(text=None) :
    '''Функция возвращает список статей или статью согласно фильтру. Принимает ключевое слово'''
    with sqlite3.connect(DB_PATH) as connection :
        df = pd.read_sql_query('''
                SELECT id, site_name, post_time,title,link,is_read FROM articles
        ''',connection)
        if not df.empty :
            mask = df["title"].str.contains(text,case=False,na=False)
        return df[mask]

if __name__ == "__main__" :
    print(select_filter_files(text="я"))
