import streamlit as st
from db_manager.bd_manager import BD_MANAGER

def show_users_root(db) :
    '''Функция отвечает за нажатие кнопки в интерфейсе, показать всех пользователей в базе данных'''
    st.subheader("Список пользователей")
    with st.spinner("Загружаем список пользователей"):
        get_all_users = db.get_users_admin()
        if get_all_users :
            import pandas as pd
            df = pd.DataFrame(get_all_users)
            st.dataframe(df,use_container_width=True)