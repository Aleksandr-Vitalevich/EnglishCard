import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

def create_json(list_dct,name) :
    '''Функция создает файл json принимает список словарей и название файла'''
    for el in range(len(list_dct)) :
        sub_name = "strings" if el == 0 else "dictionarys"
        path = RESULTS_DIR / f"{name}-{sub_name}.json"
        with open(path,'w',encoding="utf-8") as file :
            json.dump(list_dct[el],file,ensure_ascii=False,indent=4)
