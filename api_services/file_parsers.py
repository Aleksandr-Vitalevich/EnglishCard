import json

def read_file_json(path) :
        '''Функция для чтения файлов формата json
        Принимает путь к фвйлу'''
        with open(path,'r',encoding='utf-8') as file :
            file_read = json.load(file)
            return file_read

def read_xml(path) :
    '''Функция чтения файлов в формате xml'''
    from bs4 import BeautifulSoup
    import lxml
    with open(path,'r') as file :
        soup = BeautifulSoup(file,'lxml-xml')
        cities = soup.find_all('city')
        lst = []
        for city in cities :
            words_russian = city.russian.text.strip() if city.russian else ""
            words_english = city.english.text.strip() if city.english else ""
            dct = {
                "words_russian" : words_russian,
                "words_english" : words_english
            }
            lst.append(dct)
        return (lst)