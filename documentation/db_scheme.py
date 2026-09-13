import streamlit as st
from streamlit_carousel import carousel

def run_db_scheme_screen() :
    '''Функция выполняет отображение схемы БД и истории ее изменения'''
    st.markdown("***История БД***")
    carousel_items=[
            {
                "title" : "",
                "text" : "",
                "img" : "documentation/Cхема_БД _1_этап.drawio.png"
            },
            {
                "title" : "",
                "text" : "",
                "img" : "documentation/Cхема_БД _2_этап.drawio.png"
            },
            {
                "title" : "",
                "text" : "",
                "img" : "documentation/Cхема_БД _3_этап.drawio.png"
            },
            {
                "title" : "",
                "text" : "",
                "img" : "documentation/Cхема_БД _4_этап.drawio.png"
            },
            {
                "title" : "",
                "text" : "",
                "img" : "webscrapping/manager_db/bd_scheme.drawio.png"
            }
        ]
    carousel(items=carousel_items,key="db_scheme_carousel",container_height=1200)
    st.write('---')
    with st.expander("📝 Почитать описание Этапа 1 (Базовая версия)"):
        st.markdown("**Схема БД (Этап 1)**")
        st.info("Первая базовая версия структуры таблиц, разработанная на старте проекта.")
                                  
    with st.expander("📝 Почитать описание Этапа 2 (Логирование IP)"):
        st.markdown("**Схема БД (Этап 2)**")
        st.info("Вторая версия структуры: добавили полноценное логирование сессий пользователей, включая сохранение IP-адреса, города, даты и времени входа.")

    with st.expander("📝 Почитать описание Этапа 3 (Таблица сохранения очков для сторонних тренажеров)"):
        st.markdown("**Схема БД (Этап 3)**")
        st.info("Третья версия структуры таблиц, добавлен функционал сохранения очков для сторонних тренажеров.")

    with st.expander("📝 Почитать описание Этапа 4 (Таблица слов для городов)"):
        st.markdown("**Схема БД (Этап 4)**")
        st.info("Четвертая версия структуры таблиц, добавлена таблица для названий городов.")

    with st.expander("📝 Почитать описание Этапа 5 (Таблица для скрапинга)"):
        st.markdown("**Схема БД (Этап 5)**")
        st.info("Независимая таблица для скрапинга статей на Sqlight")