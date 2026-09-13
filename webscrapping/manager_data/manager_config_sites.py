import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE = BASE_DIR / "config.json"

def load_file_config() :
    '''Функция читает файл с настройками сайта'''
    default_config = {
        "Хабр" :
        {
            "url" : "https://habr.com/ru/articles/",
            "args": ["article", ".tm-title__link", "href", "time"]
        }
    }

    if FILE.exists() :
        with open(FILE,"r",encoding="utf-8") as f :
            return json.load(f)

    with open(FILE,'w',encoding="utf-8") as f :
        json.dump(default_config,f,ensure_ascii=False,indent=4)
    return default_config

def add_new_config(site_name,url,args) :
    '''Функция добавления новых данных'''
    current_data = load_file_config()
    current_data[site_name] = {
        "url" : url,
        "args" : list(args),
    }

    with open(FILE,'w',encoding="utf-8") as f :
        json.dump(current_data,f,ensure_ascii=False,indent=4)