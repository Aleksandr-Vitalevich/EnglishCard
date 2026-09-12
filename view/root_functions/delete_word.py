import streamlit as st
from db_manager.bd_manager import BD_MANAGER

def delete_word_root(db) :
    '''Функция отвечает за нажатие кнопки в интерфейсе, удаления слова из базы данных'''
    st.subheader("Удаление слова ")
    if st.session_state.current_user_name == "root" :
        st.text("Введите или русское или английское слово или оба слова ")
        english = st.text_input("Введите английское слово : ").strip()
        russian = st.text_input("Введите русское слово : ").strip()
        if english or russian :
            if st.button("Удалить") :
                delete_word = db.delete_word_admin(english=english,russian=russian)
                if delete_word == "not_found" :
                    st.warning("Запись не найдена в бд")
                elif delete_word :
                    st.success("Запись успешно удалена из бд")
                else :
                    st.error("Ошибка удаления")