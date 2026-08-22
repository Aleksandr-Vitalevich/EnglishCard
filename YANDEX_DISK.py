import requests
from dotenv import load_dotenv
import os
load_dotenv()

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
            print(f'Ошибка сети {e}')

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