import requests
from time import sleep
def get_photos_random() :
    '''Функция возвращает ссылку на случайное фото собаки'''
    max_retries = 3
    delay = 2
    for retries in range(1,max_retries+1) :
        try:
            response_get_photo_url = requests.get('https://dog.ceo/api/breeds/image/random',timeout=4).json()['message']
            return response_get_photo_url
        except (requests.exceptions.RequestException,KeyError) as e :
            if retries < max_retries :
                print('Жду соединения с сервером : ')
                sleep(delay)
            else:
                return "error"