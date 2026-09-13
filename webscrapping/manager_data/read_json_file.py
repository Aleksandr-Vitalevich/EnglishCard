from pathlib import Path
import json
from pprint import pprint

def read_json(file) :
    '''Функция принимает файл в формате json и читает его'''
    with open(file,'r',encoding="utf-8") as f :
        text = json.load(f)
        return text


if __name__ == "__main__" :
    pprint(read_json("manager_data/habr com-dictionarys.json"))