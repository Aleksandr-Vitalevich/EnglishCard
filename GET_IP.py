import requests
from dotenv import load_dotenv
import os
load_dotenv()
ipify = os.getenv('IPIFY_TOKEN')

class GET_IP :
    url_ip = "https://api.ipify.org"
    url_geo = 'https://geo.ipify.org/api/v2/country,city'
    def __init__(self,ip_token):
        self.ip_token = ip_token
        self.response_ip = None
        self.data_json = None

    def get_ip(self):
        '''Получение IP'''
        if not self.response_ip :
            try :
                self.response_ip = requests.get(self.url_ip).text.strip()
            except (requests.exceptions.RequestException,KeyError) as e :
                print('Ошибка сети')
        return self.response_ip

    def get_ip_geo(self) :
        '''Получение IP GEO'''
        if not self.data_json :
            try :
                ip = self.get_ip()
                params = {'apiKey' : self.ip_token,'ipAddress' : ip}
                self.data_json = requests.get(self.url_geo,params = params).json()
            except (requests.exceptions.RequestException,KeyError) as e :
                print('Ошибка сети')

        return self.data_json
    def get_city(self):
        '''Получение города пользователя'''
        data = self.get_ip_geo()
        return data.get('location',{}).get('city','Не найден')
    def __str__(self):
        ip = self.get_ip()
        city = self.get_city()
        return f'Ip адрес {ip} Город {city}'

if __name__ == "__main__" :
    user_adress = GET_IP(ipify)
    print(user_adress.get_ip())
    print(user_adress.get_city())