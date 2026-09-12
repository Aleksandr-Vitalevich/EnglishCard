import streamlit as st
from db_manager.bd_manager import BD_MANAGER

def add_user_root(db) :
    '''Функция отвечает за нажатие кнопки в интерфейсе, добавления пользователя в базу данных'''
    st.subheader("Добавление нового пользователя")
    if st.session_state.current_user_name != "root" :
        st.error("Доступ запрещен")
        st.stop()
    user_name = st.text_input("Введите имя пользователя",key="add_user_new").strip().lower()
    user_password = st.text_input("Введите пароль",key="add_password_new_user",type="password").strip().lower()
    if st.button("Добавить пользователя",use_container_width=True,key="btn_add_user"):
        if user_name and user_password :
            add_new_user = db.add_user(user_name,user_password)
            if add_new_user :
                st.success(f"Пользователь успешно добавлен в базу {user_name}")
            elif add_new_user == "exists" :
                st.warning(f"Пользователь уже есть в системе {user_name}")
            else :
                st.error('Ошибка добавления')
        else :
            st.info("Необходимо заполнить все поля")