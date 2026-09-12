import requests
from time import sleep
from tqdm import tqdm
import json

def get_photos_random() :
    '''Функция возвращает ссылку на случайное фото собаки и название породы'''
    max_retries = 3
    delay = 2
    for retries in range(1,max_retries+1) :
        try:
            response_get_photo_url = requests.get('https://dog.ceo/api/breeds/image/random',timeout=4).json()['message']
            breed = response_get_photo_url.split("/")
            img_bytes = requests.get(response_get_photo_url).content
            return (response_get_photo_url,breed[-2],img_bytes)
        
        except (requests.exceptions.RequestException,KeyError) as e :
            print(f'Попытка {retries}/{max_retries} Ошибка сети {e}')
            if retries < max_retries :
                print(f'Жду {delay} сек соединения с сервером : ')
                sleep(delay)
            else:
                print("Сервер не отвечает")
                return (None,None)

if __name__ == "__main__" :
    import os
    import json
    API_SERVICES_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(API_SERVICES_DIR)
    test_json_path = os.path.join(BASE_DIR, "media_cache", "test_dog_data.json")
    dog_data = {"status": "success", "message": "https://dog.ceo/api/breeds/image/random"}
    with open(test_json_path, 'w', encoding='utf-8') as file:
        json.dump(dog_data, file, indent=4, ensure_ascii=False)
    #response_get_photo_url = requests.get('https://dog.ceo/api/breeds/image/random',timeout=4).json()['message']
    #breed = response_get_photo_url.split("/")
    #print(breed[-2])
    #print("Старт теста")
    #progress_line = tqdm(range(1,5),desc="Скачивание любой породы",unit="шт")
    #for line in progress_line :
    #    file = get_photos_random()
        
    #print("\nТест завершен")