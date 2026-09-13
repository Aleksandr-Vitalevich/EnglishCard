import streamlit as st
from webscrapping.manager_db.create_db import create_init_db
from webscrapping.tabs_scrapping.tab1 import tab1_operation
from webscrapping.tabs_scrapping.tab2 import tab2_operation
from webscrapping.tabs_scrapping.tab3 import tab3_operation

create_init_db()

def main_scrapping() :
    '''Главная функция окна скрапинг'''
    st.title("***Scrapping Site Manager***")
    st.write("---")
    tab1,tab2,tab3 = st.tabs(["Работа с сайтами", "Работа с файлами","Работа с Базой Данных"])

    with tab1 :
        tab1_operation()
    with tab2 :
        tab2_operation()
    with tab3 :
        tab3_operation()
        