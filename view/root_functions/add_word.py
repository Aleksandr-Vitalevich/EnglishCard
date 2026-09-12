import streamlit as st
from db_manager.bd_manager import BD_MANAGER

def add_word_root(db) :
    '''Функция отвечает за нажатие кнопки в интерфейсе, добавления слова в базу данных'''
    st.subheader("Добавление слова ")
    if st.session_state.current_user_name == "root" :
        english = st.text_input("Введите английское слово : ").strip()
        russian = st.text_input("Введите перевод слова : ").strip()
        if st.button("Добавить") :
            if english and russian :
                add_word_admin = db.add_word_admin(english,russian)
                if add_word_admin == "duplicate" :
                    st.warning("Слово уже есть в словаре")
                elif add_word_admin :
                    st.success("Слово добавлено в базу")
                else :
                    st.error("Ошибка добавления")
            else :
                st.error("Ошибка добавления , не все поля заполнены")