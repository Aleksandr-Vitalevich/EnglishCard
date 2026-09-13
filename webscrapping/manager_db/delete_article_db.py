import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "parser_history.db"

def delete_article(id_list=None) :
    '''Функция принимает id и удаляет статью или статьи'''
    if not id_list :
        return "Список пуст, не введена ни одна статья"
    with sqlite3.connect(DB_PATH) as connection :
        cursor = connection.cursor()
        get_placeholders = ', '.join(['?'] * len(id_list))
        query_delete = f"DELETE FROM articles WHERE id IN ({get_placeholders})"
        cursor.execute(query_delete,id_list)
    return "success"

if __name__ == "__main__" :
    print(delete_article())
    print(delete_article([6,7,8]))
