import sqlite3
from pathlib import Path
import pandas
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "parser_history.db"

def update_table(name_site,select_rows) :
    '''Функция наполняет базу данных'''
    with sqlite3.connect(DB_PATH) as connection :
        cursor = connection.cursor()
        query_update = "INSERT OR IGNORE INTO articles (site_name,post_time,title,link) VALUES (?,?,?,?)"

        for _, row in select_rows.iterrows() :
            date =  row.get("date","Даты нет")
            title = row.get("title","Без заголовка")
            link =  row.get("link", "")
            if not link :
                continue
            values = (name_site,date,title,link)
            cursor.execute(query_update,values)

    return "success"
