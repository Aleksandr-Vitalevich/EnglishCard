import requests
from dotenv import load_dotenv
import os
load_dotenv()
from tqdm import tqdm
from time import sleep

ydt = os.getenv('YANDEX_DISK_TOKEN')

class YandexDiskService:
    '''Класс по работе с яндекс диском'''
    _url_yandex = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self,y_token):
        '''Инициализация'''
        self.y_token = y_token
        self.last_file_status = "Запрос не отправлялся"
        self.folder_sc = 'Не проверялась'
        self.headers = {"Authorization": f"OAuth {self.y_token}"}

    def create_folder(self,path):
        '''Создание папки на яндекс диск. Функция принимает путь'''
        max_retries = 3
        delay = 2
        for retries in range(1,max_retries+1) :
            try :
                response_get_place = requests.get(f'{self._url_yandex}',headers=self.headers,params={'path':path})
                if response_get_place.status_code == 404 :
                    requests_save_file_on_disk = requests.put(self._url_yandex,headers=self.headers,params={'path':path})
                    self.folder_sc = requests_save_file_on_disk.status_code
                elif response_get_place.status_code == 200 :
                    self.folder_sc = 'Папка уже есть '
                else :
                    self.folder_sc = f'Ошибка {response_get_place.status_code}'
                return self.folder_sc
            except (requests.exceptions.RequestException,KeyError) as e :
                print(f'Попытка {retries}/{max_retries} Ошибка сети {e}')
                if retries < max_retries :
                    print(f"\nЖду {delay} сек соединения с сервером")
                    sleep(delay)
                else :
                    print("Сервер не отвечает")
                    self.folder_sc = "Ошибка сети"
                    return self.folder_sc
                        

    def send_file(self,file_bytes,path):
        '''Функция отправки файла на яндекс диск'''
        try :
            main_path_folder = os.path.dirname(path)
            if main_path_folder :
                self.create_folder(main_path_folder)
            response_get_place = requests.get(f'{self._url_yandex}/upload',headers=self.headers,params={'path':path})
            if response_get_place.status_code != 200 :
                self.last_file_status = f'Ошибка в получении ссылки {response_get_place.status_code}'
                return self.last_file_status
            url_place = response_get_place.json().get('href')
            requests_save_file_on_disk = requests.put(url_place,data=file_bytes)
            self.last_file_status = requests_save_file_on_disk.status_code

        except (requests.exceptions.RequestException,KeyError) as e :
            print(f'Ошибка сети {e}')
        return self.last_file_status

    def __str__(self) :
        if self.last_file_status == "Запрос не отправлялся" :
            return 'Запрос еще не отправлялся'
        return f'Статус операций\n\tПапка статус {self.folder_sc}\n\tФайл статус {self.last_file_status} Запись файла произведена успешно'


if __name__ == "__main__" :
    uploader = YandexDiskService(y_token=ydt)
    
    test_files = [
        {"name": "test_word_1", "data": b"Hello from EnglishCard 1"},
        {"name": "test_word_2", "data": b"Hello from EnglishCard 2"},
        {"name": "test_word_3", "data": b"Hello from EnglishCard 3"},
        {"name": "test_word_4", "data": b"Hello from EnglishCard 4"},
        {"name": "test_word_5", "data": b"Hello from EnglishCard 5"},
    ]
        
    print("Старт синхронизации бэкапов с Яндекс.Диском:")
        
    for file_obj in tqdm(test_files, desc="Синхронизация бэкапов", unit="file"):
        cloud_path = f"disk:/Hero/TestBackups/{file_obj['name']}.txt"
        uploader.send_file(file_obj['data'], cloud_path)
            
    print("\nТест завершен")