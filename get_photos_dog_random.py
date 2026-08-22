import requests
from time import sleep
from tqdm import tqdm

def get_photos_random() :
    '''Функция возвращает ссылку на случайное фото собаки'''
    max_retries = 3
    delay = 2
    for retries in range(1,max_retries+1) :
        try:
            response_get_photo_url = requests.get('https://dog.ceo/api/breeds/image/random',timeout=4).json()['message']
            return response_get_photo_url
        except (requests.exceptions.RequestException,KeyError) as e :
            print(f'Попытка {retries}/{max_retries} Ошибка сети {e}')
            if retries < max_retries :
                print(f'Жду {delay} сек соединения с сервером : ')
                sleep(delay)
            else:
                print("Сервер не отвечает")
                return "error"

if __name__ == "__main__" :

    print("Старт теста")
    progress_line = tqdm(range(1,5),desc="Скачивание любой породы",unit="шт")
    for line in progress_line :
        file = get_photos_random()
        
    print("\nТест завершен")