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

    response_get_photo_url = requests.get('https://dog.ceo/api/breeds/image/random',timeout=4).json()['message']
    breed = response_get_photo_url.split("/")
    print(breed[-2])
    #with open("test_api_dog.json",'w',encoding='utf-8') as file :
    #    json.dump(response_get_photo_url,file,indent=4,ensure_ascii=False)
    #print("Старт теста")
    #progress_line = tqdm(range(1,5),desc="Скачивание любой породы",unit="шт")
    #for line in progress_line :
    #    file = get_photos_random()
        
    #print("\nТест завершен")