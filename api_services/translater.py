import requests
from dotenv import load_dotenv
import os

load_dotenv()

def translate_word(word : str,direction : str = "ru-en") -> str :
    '''Функция вызова API Yandex словаря используется как фича'''
    url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

    params = {
        "key": os.getenv("YANDEX_TOKEN"),
        "text": word,
        "lang": direction
    }
    try :
        response = requests.get(url,params=params).json()
        if response.get("def") and response["def"][0].get("tr") :
            trans_word = response["def"][0]["tr"][0]["text"]
            return trans_word
        return "Перевод не найден"
    except Exception as e :
        return f"Ошибка перевода {str(e)}"


if __name__ == '__main__':
    word = 'время'
    assert translate_word(word) == 'time'
    print(translate_word(word)=='time')