import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse

def create_dict(text,link,date_info) :
    '''Функция формирует словарь'''
    return {
            "date" : date_info,
            "title" : text,
            "link" : link
        }

def get_data(url, KEYWORDS, args):
    '''Функция делает запрос и возвращает результат работы в виде кортежа'''
    article, title__link, href, time_tag = args
    list_scraping_data_dict_format = []
    list_scraping_data = []

    parsed_url = urlparse(url)
    base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    get_data = requests.get(url)
    soup = BeautifulSoup(get_data.text, "html.parser")
    articles_ = soup.select(article)
    
    for article_ in articles_ :
        title_tag = article_.select_one(title__link)
        if not title_tag :
            continue
            
        title = title_tag.text.strip()
        raw_link = title_tag.get(href)
        if not raw_link :
            continue

        if raw_link.startswith("http") :
            link = raw_link
        else :
            link = f"{base_domain}{raw_link}"

        
        date_tag = article_.select_one(time_tag)
        date = date_tag.get("title") if date_tag else "Даты нет"
        
        is_match = False
        
        article_text = article_.text.lower()
        if any(word in article_text for word in KEYWORDS):
            is_match = True
            
        if not is_match:
            try:
                data_in_page = requests.get(link)
                another_soup = BeautifulSoup(data_in_page.text, "html.parser")
                article_body = another_soup.select_one(".tm-article-body")
                full_text = article_body.text.lower() if article_body else another_soup.text.lower()
                    
                if any(word in full_text for word in KEYWORDS):
                        is_match = True 
            except Exception:
                pass 
                
        if is_match:
            list_scraping_data_dict_format.append(create_dict(title, link, date))
            list_scraping_data.append(f'{date} - {title} - {link}')

    return (list_scraping_data, list_scraping_data_dict_format)

if __name__ == "__main__" :
    # Слова для поиска
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    # аргументы для поиска
    args = ("article",".tm-title__link","href","time")
    # Ссылка
    url = "https://habr.com/ru/articles/"
    # Вывод словаря 
    res = get_data(url,KEYWORDS,args)
    pprint(res[1])
    # Вывод списка
    print(res[0])