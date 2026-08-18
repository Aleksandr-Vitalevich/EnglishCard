import requests
import json
from pathlib import Path

def get_info_super_hero(id_hero) :
    '''Функция получения информации о супергероях'''
    path_hero_file = Path("all_heroes.json")
    if not path_hero_file.exists() :
        try :
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            url = "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json"
            response = requests.get(url,headers=headers,timeout=15)
            #response.raise_for_status() # код ответа 200
            res = response.json()
                
            with open('all_heroes.json','w',encoding='utf-8') as file :
                json.dump(res,file,indent=4,ensure_ascii=False)
        except Exception as e :
            print(f"Ошибка запроса {e}")
            return {}

    
    with open('all_heroes.json','r',encoding='utf-8') as file :
        heroes = json.load(file)

    id_hero = int(id_hero)
    
    for hero in heroes :
        if hero.get("id") == id_hero :
            return {
            "name" : hero.get("name"),
            "photo" : hero.get("images",{}).get("lg")
            }
    return {}
        


if __name__ == "__main__" :
    print(get_info_super_hero(2))
